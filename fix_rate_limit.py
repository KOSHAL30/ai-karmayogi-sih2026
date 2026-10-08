import sys

# Patch main.py
file_path_main = 'backend/app/main.py'
with open(file_path_main, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from fastapi import FastAPI, Request, status',
    'from fastapi import FastAPI, Request, status\nfrom slowapi import Limiter, _rate_limit_exceeded_handler\nfrom slowapi.util import get_remote_address\nfrom slowapi.errors import RateLimitExceeded'
)

# Initialize limiter
content = content.replace(
    'app = FastAPI(',
    '''limiter = Limiter(key_func=get_remote_address)

app = FastAPI('''
)

# Add limiter state and exception handler
content = content.replace(
    '# Configure Cross-Origin Resource Sharing (CORS)',
    '''app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure Cross-Origin Resource Sharing (CORS)'''
)

with open(file_path_main, 'w', encoding='utf-8') as f:
    f.write(content)

# Patch auth.py
file_path_auth = 'backend/app/api/v1/endpoints/auth.py'
with open(file_path_auth, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from fastapi import APIRouter, Depends, HTTPException, status, Response',
    'from fastapi import APIRouter, Depends, HTTPException, status, Response, Request\nfrom app.main import limiter'
)

# Add limiter to login
old_login = '''@router.post("/login", response_model=APIResponse[LoginResponseData])
async def login(
    data: LoginRequest,
    response: Response,
    db = Depends(get_db)
):'''

new_login = '''@router.post("/login", response_model=APIResponse[LoginResponseData])
@limiter.limit("5/minute")
async def login(
    request: Request,
    data: LoginRequest,
    response: Response,
    db = Depends(get_db)
):'''

content = content.replace(old_login, new_login)

with open(file_path_auth, 'w', encoding='utf-8') as f:
    f.write(content)

print("Rate limiting implemented.")
