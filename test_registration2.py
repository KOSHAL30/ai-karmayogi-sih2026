import asyncio
import httpx
import uuid

async def run():
    url = "http://localhost:8000/api/v1/auth/register"
    email = f"test.seeded.{uuid.uuid4().hex[:6]}@gov.in"
    data = {
        "email": email,
        "password": "Password@123",
        "full_name": "Test Seeded User",
        "designation": "Tester",
        "role_code": "learner",
        "department_code": "DEPT-DOPT"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=data)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
        
    print("Testing nonexistent role_code")
    data["role_code"] = "nonexistent"
    data["email"] = f"test.seeded.{uuid.uuid4().hex[:6]}@gov.in"
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=data)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")

asyncio.run(run())
