import asyncio
import httpx

async def run():
    url = "http://localhost:8000/api/v1/auth/register"
    data = {
        "email": "test.500@gov.in",
        "password": "Password@123",
        "full_name": "Test User",
        "designation": "Tester",
        "role_code": "learner",
        "department_code": "DEPT-DOPT"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=data)
        print(res.status_code)
        print(res.text)

asyncio.run(run())
