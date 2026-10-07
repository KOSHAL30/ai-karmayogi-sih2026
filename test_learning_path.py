import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

async def run():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        login_res = await client.post(f"{BASE_URL}/auth/login", json={"email": "rajesh.kumar@gov.in", "password": "Karmayogi2026!"})
        token = login_res.json().get("data", {}).get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            path_res = await client.get(f"{BASE_URL}/recommendations/path", headers=headers)
            print("Status Code:", path_res.status_code)
            print("Text:", path_res.text)
        except Exception as e:
            import traceback
            traceback.print_exc()

asyncio.run(run())
