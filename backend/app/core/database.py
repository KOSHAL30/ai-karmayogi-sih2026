import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

logger = logging.getLogger(__name__)

_client = None
_db = None

async def init_mongodb():
    global _client, _db
    
    _client = AsyncIOMotorClient(settings.MONGODB_URI)
    _db = _client[settings.MONGODB_DATABASE]
    
    # Run the seed data so the demo has data
    try:
        from app.db.seed import seed_database as seed_main
        from app.db.seed_assessment import seed_database as seed_assessments
        from app.db.seed_courses import seed_database as seed_learning_courses
        
        await seed_main(_db)
        await seed_assessments(_db)
        await seed_learning_courses(_db)
    except Exception as e:
        logger.error(f"Error seeding DB: {e}")
        
    logger.info(f"Local MongoDB connected to {settings.MONGODB_URI}, Database: {settings.MONGODB_DATABASE}")
    return _db

async def close_mongodb():
    global _client
    if _client:
        _client.close()
        logger.info("Local MongoDB connection closed.")

def get_database():
    return _db

async def get_db():
    return _db
