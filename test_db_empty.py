import asyncio
from pymongo import AsyncMongoClient

async def run():
    client = AsyncMongoClient("mongodb+srv://sainlucky489_db_user:Ab33DkX8c7Mj2vdW@aikarmayogi.ruao4nw.mongodb.net/?appName=AIKarmayogi")
    db = client["ai_karmayogi"]
    c = await db['departments'].count_documents({})
    print("DEPT COUNT:", c)
    r = await db['roles'].count_documents({})
    print("ROLE COUNT:", r)

asyncio.run(run())
