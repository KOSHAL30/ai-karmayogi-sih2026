import asyncio
import os
import sys
from pymongo import AsyncMongoClient

async def run():
    client = AsyncMongoClient("mongodb+srv://sainlucky489_db_user:Ab33DkX8c7Mj2vdW@aikarmayogi.ruao4nw.mongodb.net/?appName=AIKarmayogi", serverSelectionTimeoutMS=5000)
    db = client["ai_karmayogi"]
    depts = await db["departments"].find().to_list(10)
    print("DEPTS:", depts)

asyncio.run(run())
