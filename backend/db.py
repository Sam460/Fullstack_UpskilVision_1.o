from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env if present
load_dotenv()

def get_db_connection():
    try:
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI is not set in environment variables.")
        
        client = MongoClient(mongo_uri)
        db = client['upskill_vision']
        return db
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        sys.exit(1)

# Get database connection
try:
    db = get_db_connection()

    # Initialize all collections
    courses_collection = db['courses']
    enrollments_collection = db['enrollments']
    users_collection = db['users']
    modules_collection = db['modules']
    assignments_collection = db['assignments']
    quizzes_collection = db['quizzes']
    submissions_collection = db['submissions']
    audit_log_collection = db['audit_log']

    # Create indexes for performance
    modules_collection.create_index([("course_id", 1), ("order", 1)])
    assignments_collection.create_index([("course_id", 1), ("due_date", 1)])
    quizzes_collection.create_index([("course_id", 1)])
    submissions_collection.create_index([("assignment_id", 1), ("student_id", 1)])
    audit_log_collection.create_index([("course_id", 1), ("timestamp", -1)])
    modules_collection.create_index([('instructor_id', 1)])

    print("✅ Database and collections are ready!")
except Exception as e:
    print(f"❌ Failed to initialize database: {str(e)}")
    sys.exit(1)

# Test the connection
try:
    test_id = courses_collection.insert_one({"test": True}).inserted_id
    courses_collection.delete_one({"_id": test_id})
    print("✅ MongoDB connection test successful!")
except Exception as e:
    print(f"❌ MongoDB connection test failed: {str(e)}")
    sys.exit(1)

# Export all collections
__all__ = [
    'courses_collection',
    'enrollments_collection',
    'users_collection',
    'modules_collection',
    'assignments_collection',
    'quizzes_collection',
    'submissions_collection',
    'audit_log_collection'
]
