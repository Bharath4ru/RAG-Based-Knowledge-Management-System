import chromadb
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import Config

class VectorStore:
    def __init__(self, path):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=Config.GOOGLE_API_KEY
        )
        self.vector_store = Chroma(
            collection_name="my_collection",
            persist_directory=path,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents):
        try:
            self.vector_store.add_documents(documents)
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")

    def similarity_search(self, query, k=100):
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
