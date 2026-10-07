import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath('backend'))
from app.core.config import settings
from services.auth_service import AuthService
from fastapi import HTTPException
from pymongo import AsyncMongoClient
import dns.resolver

async def run():
    try:
        # Use a fake unreachable IP to force a timeout immediately
        client = AsyncMongoClient('mongodb://192.0.2.1:27017', serverSelectionTimeoutMS=1000)
        db = client['ai_karmayogi']
        
        service = AuthService(db=db)
        
        try:
            res_fail = await service.login(
                email="rajesh.kumar@gov.in",
                password="Password@123"
            )
            print("FAILURE: Should have raised 503")
        except HTTPException as e:
            print(f"SUCCESS: Caught Expected Exception: {e.status_code} - {e.detail}")

    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(run())
