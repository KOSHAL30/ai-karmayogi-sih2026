import requests
import time

BASE_URL = "http://localhost:8000/api/v1"
headers = {}

def test_endpoint(method, endpoint, json_data=None):
    global headers
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == 'GET':
            res = requests.get(url, headers=headers, timeout=5)
        else:
            res = requests.post(url, headers=headers, json=json_data, timeout=5)
        
        print(f"[{method}] {endpoint} - Status: {res.status_code}")
        
        if endpoint == '/auth/login' and res.status_code == 200:
            token = res.json().get('data', {}).get('access_token')
            if token:
                headers['Authorization'] = f"Bearer {token}"
                print("   -> Got Token")
        
        if res.status_code != 200:
            print(f"  Error: {res.text[:200]}")
    except Exception as e:
        print(f"[{method}] {endpoint} - FAILED: {str(e)}")

print("--- Testing API Endpoints ---")
test_endpoint('POST', '/auth/login', {"email": "rajesh.kumar@gov.in", "password": "Karmayogi2026!"})
test_endpoint('GET', '/assessment/start')
test_endpoint('POST', '/assessment/answer', {"question_id": "q1", "answer": "a"})
test_endpoint('POST', '/assessment/submit', {"assessment_id": "a1"})
test_endpoint('GET', '/recommendations')
test_endpoint('GET', '/recommendations/path')
test_endpoint('GET', '/learning-path')
test_endpoint('POST', '/documents/upload')
test_endpoint('POST', '/rag/query', {"query": "test"})
test_endpoint('POST', '/mcq/generate', {"document_id": "doc1"})
test_endpoint('GET', '/admin/dashboard')
test_endpoint('GET', '/admin/departments')
test_endpoint('POST', '/certificate/generate', {"course_id": "c1"})

