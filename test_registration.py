import asyncio
import os
import sys

# We will test the AuthService logic directly to avoid FastAPI port conflicts
sys.path.insert(0, os.path.abspath('backend'))
from app.core.database import init_mongodb
from services.auth_service import AuthService
from fastapi import HTTPException
import uuid

async def run():
    try:
        db = await init_mongodb()
        service = AuthService(db)
        
        email = f"test.seeded.{uuid.uuid4().hex[:6]}@gov.in"
        res = await service.register(
            email=email,
            password='Password@123',
            full_name='Test Seeded User',
            designation='Tester',
            role_code='learner',
            department_code='DEPT-DOPT'
        )
        print("SUCCESS")
        print(f"User ID: {res.id}")
        print(f"Role: {res.role}")
        print(f"Department: {res.department}")
    except HTTPException as e:
        print(f"HTTPException: {e.status_code} - {e.detail}")
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(run())
