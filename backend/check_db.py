import asyncio
from app.core.database import init_mongodb

async def check():
    db = await init_mongodb()
    user = await db["users"].find_one({"email": "rajesh.kumar@gov.in"})
    if user:
        print("Found user:", user.get("full_name"), "role:", user.get("role"))
        print("Has password_hash:", bool(user.get("password_hash")))
    else:
        print("User NOT FOUND - database may need re-seeding")
    count = await db["users"].count_documents({})
    print("Total users in DB:", count)

asyncio.run(check())
