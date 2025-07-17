import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    MONGO_URI = os.getenv("MONGO_URI")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLITE_URI", "sqlite:///instance/database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
