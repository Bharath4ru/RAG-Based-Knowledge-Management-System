from flask import Flask, request, render_template, jsonify
from models.vector_store import VectorStore
from services.llm_service import LLMService
from services.storage_service import S3Storage
from config import Config
import os
import tempfile
import logging
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = Flask(__name__)
vector_store = VectorStore(Config.VECTOR_DB_PATH)
storage_service = S3Storage()
llm_service = LLMService(vector_store)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def process_document(file):
    """Process document based on file type and return text chunks"""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    
    try:
        file.save(temp_path)
        
        if file.filename.endswith('.pdf'):
            loader = PyPDFLoader(temp_path)
        elif file.filename.endswith('.txt'):
            loader = TextLoader(temp_path)
        else:
            raise ValueError("Unsupported file type")
        
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_documents(documents)
        
        return text_chunks
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(temp_dir)

@app.route('/upload', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file.filename.endswith(('.txt', '.pdf')):
            return jsonify({'error': 'Only .txt and .pdf files are supported'}), 400
        
        text_chunks = process_document(file)
        file.seek(0)  # Reset file pointer
        storage_service.upload_file(file, file.filename)
        vector_store.add_documents(text_chunks)

        return jsonify({'message': 'File uploaded and processed successfully', 'chunks_processed': len(text_chunks)})
    
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    if 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400

    try:
        response = llm_service.get_response(data['question'])
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
