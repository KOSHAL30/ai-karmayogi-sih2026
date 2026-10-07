import asyncio
from pymongo import AsyncMongoClient

async def run():
    client = AsyncMongoClient("mongodb://localhost:27017")
    db = client["ai_karmayogi"]
    c = await db['departments'].count_documents({})
    print("DEPT COUNT:", c)
    r = await db['roles'].count_documents({})
    print("ROLE COUNT:", r)

asyncio.run(run())
