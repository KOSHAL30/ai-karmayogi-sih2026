import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def ping():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    try:
        await client.server_info()
        print("MongoDB is running and reachable!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

asyncio.run(ping())
