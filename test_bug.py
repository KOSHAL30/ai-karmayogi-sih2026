import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath('backend'))
from app.core.database import init_mongodb
from backend.repositories.user_repository import UserRepository

async def run():
    db = await init_mongodb()
    repo = UserRepository(db)
    dept = await repo.get_department_by_code("DEPT-DOPT")
    print(dept)
    try:
        print(dept.name)
    except Exception as e:
        print("ERROR:", repr(e))

asyncio.run(run())
