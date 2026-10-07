import asyncio
import os
import sys

# We will test the AuthService logic directly
sys.path.insert(0, os.path.abspath('backend'))
from app.core.database import init_mongodb
from services.auth_service import AuthService
from fastapi import HTTPException
from pymongo import AsyncMongoClient
import uuid

async def run():
    try:
        # Connecting to empty db
        client = AsyncMongoClient('mongodb://localhost:27017')
        db = client['ai_karmayogi_empty_test']
        await db.drop_collection("roles")
        await db.drop_collection("departments")
        await db.drop_collection("users")
        service = AuthService(db)
        
        email = f"test.empty.{uuid.uuid4().hex[:6]}@gov.in"
        res = await service.register(
            email=email,
            password='Password@123',
            full_name='Test Empty User',
            designation='Tester',
            role_code='learner',
            department_code='DEPT-DOPT'
        )
        print("FAILURE: Should have raised 404")
    except HTTPException as e:
        print(f"SUCCESS: Caught Expected Exception: {e.status_code} - {e.detail}")
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(run())
