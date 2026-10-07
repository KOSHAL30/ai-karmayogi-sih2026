import asyncio
import os
import sys
from pymongo import AsyncMongoClient

async def run():
    client = AsyncMongoClient("mongodb+srv://sainlucky489_db_user:Ab33DkX8c7Mj2vdW@aikarmayogi.ruao4nw.mongodb.net/?appName=AIKarmayogi")
    db = client["ai_karmayogi"]
    dopt = await db["departments"].find_one({"department_code": "DEPT-DOPT"})
    print("DOPT:", dopt)
    learner = await db["roles"].find_one({"role_code": "learner"})
    print("LEARNER:", learner)

asyncio.run(run())
