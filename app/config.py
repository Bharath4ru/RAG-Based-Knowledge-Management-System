import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY') 
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') 
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    VECTOR_DB_PATH = 'vector_db'

    
