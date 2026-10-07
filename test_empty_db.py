import asyncio
from pymongo import AsyncMongoClient
import httpx
import sys
import os

async def run():
    client = AsyncMongoClient("mongodb://localhost:27017")
    db = client["ai_karmayogi_empty_test"]
    # Ensure it's empty
    await db.drop_collection("roles")
    await db.drop_collection("departments")
    await db.drop_collection("users")
    
    # We will test the AuthService logic directly to avoid FastAPI port conflicts
    sys.path.insert(0, os.path.abspath('backend'))
    from services.auth_service import AuthService
    service = AuthService(db)
    
    res = await service.register(
        email='test.empty@gov.in',
        password='Password@123',
        full_name='Test Empty',
        designation='Tester',
        role_code='learner',
        department_code='DEPT-DOPT'
    )
    print("SUCCESS")
    print(res)

asyncio.run(run())
