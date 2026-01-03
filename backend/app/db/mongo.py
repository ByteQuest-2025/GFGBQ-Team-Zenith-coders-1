from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from typing import Optional
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client
client = None


async def connect_to_mongo():
    """
    Connect to MongoDB and create indexes
    Called on application startup
    """
    global client
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        
        # Ping to verify connection
        await client.admin.command('ping')
        logger.info("✅ Connected to MongoDB successfully")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection
    Called on application shutdown
    """
    global client
    if client:
        client.close()
        logger.info("🔌 MongoDB connection closed")


async def get_database():
    """
    Get database instance
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database instance
    """
    return client[settings.DB_NAME]


async def get_collection(collection_name: str):
    """
    Get a collection from the database
    
    Args:
        collection_name (str): Name of the collection
        
    Returns:
        AsyncIOMotorCollection: MongoDB collection instance
    """
    db = await get_database()
    return db[collection_name]


async def create_indexes():
    """
    Create database indexes for optimal query performance
    """
    db = await get_database()
    
    try:
        # ==================== USERS COLLECTION ====================
        await db.users.create_index([("user_id", ASCENDING)], unique=True)
        await db.users.create_index([("email", ASCENDING)])
        await db.users.create_index([("role", ASCENDING)])
        logger.info("✅ Users collection indexes created")
        
        # ==================== COMPLAINTS COLLECTION ====================
        # Unique complaint ID
        await db.complaints.create_index([("complaint_id", ASCENDING)], unique=True)
        
        # Query by user
        await db.complaints.create_index([("user_id", ASCENDING)])
        
        # Query by status
        await db.complaints.create_index([("status", ASCENDING)])
        
        # Sort by creation time (most recent first)
        await db.complaints.create_index([("created_at", DESCENDING)])
        
        # Officer inbox queries
        await db.complaints.create_index([("routing.assigned_officer_id", ASCENDING)])
        
        # Urgency filtering
        await db.complaints.create_index([("triage.urgency_level", ASCENDING)])
        
        # Category filtering
        await db.complaints.create_index([("triage.category", ASCENDING)])
        
        # Compound index for officer inbox (assigned + status + urgency)
        await db.complaints.create_index([
            ("routing.assigned_officer_id", ASCENDING),
            ("status", ASCENDING),
            ("triage.urgency_level", ASCENDING)
        ])
        
        logger.info("✅ Complaints collection indexes created")
        
        # ==================== DEPARTMENTS COLLECTION ====================
        await db.departments.create_index([("department_id", ASCENDING)], unique=True)
        await db.departments.create_index([("name", ASCENDING)])
        logger.info("✅ Departments collection indexes created")
        
        logger.info("🎉 All database indexes created successfully")
        
    except Exception as e:
        logger.error(f"❌ Error creating indexes: {e}")
        raise
