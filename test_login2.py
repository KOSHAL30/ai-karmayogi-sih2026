import asyncio
import os
import sys
import logging

logging.basicConfig(level=logging.WARNING)

sys.path.insert(0, os.path.abspath('backend'))
from services.auth_service import AuthService
from fastapi import HTTPException

async def run():
    try:
        service = AuthService(db=None)
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
