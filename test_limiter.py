import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as c:
        for i in range(8):
            r = await c.post("http://127.0.0.1:8000/api/v1/auth/login", json={"email": "rajesh.kumar@gov.in", "password": "wrong"})
            print(f"Attempt {i+1}: {r.status_code}")

asyncio.run(test())
