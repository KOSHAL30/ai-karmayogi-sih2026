import asyncio
import os
import sys
sys.path.insert(0, os.path.abspath('backend'))
from app.core.database import init_mongodb

async def run():
    db = await init_mongodb()
    dept = await db['departments'].find_one()
    print(dept)

asyncio.run(run())
