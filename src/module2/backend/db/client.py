from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import certifi

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb+srv://abhinaviit2024_db_user:DMBS_A2@cluster1.uyxn7et.mongodb.net/"
    PORT: int = 8000
    MODULE1_URL: str = "https://patient-demographics-api.onrender.com/api"
    MODULE19_URL: str = "http://localhost:8019/api"
    MODULE25_URL: str = "http://localhost:8025/api"
    MODULE33_URL: str = "http://localhost:8033/api"
    JWT_SECRET: str = "secret"
    
    class Config:
        env_file = ".env"

settings = Settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_config = MongoDB()

async def connect_to_mongo():
    db_config.client = AsyncIOMotorClient(
        settings.MONGO_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
    )
    db_config.db = db_config.client.chronic_care
    # Verify connection actually works
    await db_config.client.admin.command('ping')
    print("Connected to MongoDB")

async def close_mongo_connection():
    if db_config.client:
        db_config.client.close()
        print("Closed connection to MongoDB")

def get_database():
    if db_config.db is None:
        # Lazy reconnect if startup connection failed
        db_config.client = AsyncIOMotorClient(
            settings.MONGO_URI,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000,
        )
        db_config.db = db_config.client.chronic_care
        print("Lazy-connected to MongoDB")
    return db_config.db
