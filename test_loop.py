import asyncio
import httpx
import uuid

async def run():
    url = "http://localhost:8000/api/v1/auth/register"
    async with httpx.AsyncClient() as client:
        for i in range(10):
            data = {
                "email": f"test.{uuid.uuid4().hex[:6]}@gov.in",
                "password": "Password@123",
                "full_name": "Test User",
                "designation": "Tester",
                "role_code": "learner",
                "department_code": "DEPT-DOPT"
            }
            res = await client.post(url, json=data)
            if res.status_code != 201:
                print(f"FAILED: {res.status_code} - {res.text}")
                return
        print("ALL SUCCESS")

asyncio.run(run())
