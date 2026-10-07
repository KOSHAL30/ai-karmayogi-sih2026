import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath('backend'))
from services.auth_service import AuthService
from fastapi import HTTPException
from pymongo import AsyncMongoClient

async def run():
    try:
        # Use local db that is seeded
        client = AsyncMongoClient('mongodb://localhost:27017')
        db = client['ai_karmayogi']
        
        service = AuthService(db=db)
        
        try:
            res = await service.login(
                email="rajesh.kumar@gov.in",
                password="Karmayogi2026!"
            )
            print("SUCCESS: Genuine Login")
            print(f"Token: {res.access_token[:20]}...")
            print(f"User: {res.user.full_name}")
            print(f"Role: {res.user.role}")
        except HTTPException as e:
            print(f"FAILURE: {e.status_code} - {e.detail}")

    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(run())
