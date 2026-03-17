import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "ChronicDiseaseManagement")

def get_database():
    """
    Establishes a connection to MongoDB Atlas and returns the database object.
    """
    if not MONGO_URI:
        raise ValueError("No MONGO_URI found in environment variables. Please check your .env file.")
        
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    
    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client[DB_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

# Example usage/test for Member 1 to verify
if __name__ == "__main__":
    db = get_database()
    print(f"Successfully connected to the database: {db.name}")
