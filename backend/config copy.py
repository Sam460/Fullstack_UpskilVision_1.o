import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    MONGODB_URI = os.getenv('MONGO_URI', 'mongodb+srv://SamratBiswas:Sam%407001@cluster0.jhqnn0s.mongodb.net/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'upskill_vision')
