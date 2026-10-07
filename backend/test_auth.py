import asyncio
from fastapi import HTTPException
from app.core.deps import get_current_user

async def run_test():
    try:
        user = await get_current_user(payload={'sub': '00000000-0000-0000-0000-000000000003'}, db=None)
        print(f"FAILED: User returned {user}")
    except HTTPException as e:
        if e.status_code == 401:
            print("SUCCESS: Threw 401 Unauthorized")
        else:
            print(f"FAILED: Threw HTTP {e.status_code}")
    except Exception as e:
        print(f"FAILED: Threw unexpected error: {e}")

asyncio.run(run_test())
