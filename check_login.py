import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

async def run():
    async with httpx.AsyncClient() as client:
        login_res = await client.post(f"{BASE_URL}/auth/login", json={"email": "rajesh.kumar@gov.in", "password": "Karmayogi2026!"})
        print(login_res.status_code)
        print(login_res.json())

asyncio.run(run())
