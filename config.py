import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    # GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')