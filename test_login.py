import asyncio
import os
import sys

# We will test the AuthService logic directly
sys.path.insert(0, os.path.abspath('backend'))
from app.core.database import init_mongodb
from services.auth_service import AuthService
from fastapi import HTTPException

async def run():
    try:
        # We simulate offline DB by passing None or a mock to AuthService
        service = AuthService(db=None)
        
        # Test offline login attempt (which would have used a demo persona before)
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
