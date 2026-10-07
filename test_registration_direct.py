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
        # Connecting to the seeded local db
        client = AsyncMongoClient('mongodb://localhost:27017')
        db = client['ai_karmayogi']
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
        
        # Test nonexistent role to verify 404
        try:
            res_fail = await service.register(
                email=f"test.seeded.{uuid.uuid4().hex[:6]}@gov.in",
                password='Password@123',
                full_name='Test Seeded User',
                designation='Tester',
                role_code='nonexistent',
                department_code='DEPT-DOPT'
            )
            print("FAILURE: Should have raised 404")
        except HTTPException as e:
            print(f"Expected Exception: {e.status_code} - {e.detail}")

    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(run())
