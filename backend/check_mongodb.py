from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

# Load .env file if present
load_dotenv()

def check_mongodb():
    try:
        # Get MongoDB URI from environment variable
        mongo_uri = os.getenv('MONGO_URI')

        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in environment variables")

        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

        # Ping server to test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        return True

    except ConnectionFailure as e:
        print("❌ MongoDB connection failed:")
        print(str(e))
        return False

    except ValueError as ve:
        print("❌ Configuration error:")
        print(str(ve))
        return False

if __name__ == "__main__":
    check_mongodb()
