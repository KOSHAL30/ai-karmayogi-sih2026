import requests

url = "http://localhost:8000/api/v1/auth/register"
data = {
    "email": "test.admin@gov.in",
    "password": "Password@123",
    "full_name": "Test Admin",
    "designation": "Tester",
    "role_code": "admin",
    "department_code": "DEPT-DOPT"
}
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
