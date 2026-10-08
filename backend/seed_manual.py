import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def seed():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['ai_karmayogi']
    
    try:
        from app.db.seed import seed_database as seed_main
        from app.db.seed_assessment import seed_database as seed_assessments
        from app.db.seed_courses import seed_database as seed_learning_courses
        
        print("Starting seed_main...")
        await seed_main(db)
        print("Starting seed_assessments...")
        await seed_assessments(db)
        print("Starting seed_learning_courses...")
        await seed_learning_courses(db)
        print("Seed success!")
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(seed())
