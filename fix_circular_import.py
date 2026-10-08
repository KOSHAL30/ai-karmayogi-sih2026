import sys

# Patch main.py
file_path_main = 'backend/app/main.py'
with open(file_path_main, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from slowapi import Limiter, _rate_limit_exceeded_handler\nfrom slowapi.util import get_remote_address\nfrom slowapi.errors import RateLimitExceeded',
    'from slowapi import _rate_limit_exceeded_handler\nfrom slowapi.errors import RateLimitExceeded\nfrom app.core.rate_limit import limiter'
)

content = content.replace(
    'limiter = Limiter(key_func=get_remote_address)\n\napp = FastAPI(',
    'app = FastAPI('
)

with open(file_path_main, 'w', encoding='utf-8') as f:
    f.write(content)

# Patch auth.py
file_path_auth = 'backend/app/api/v1/endpoints/auth.py'
with open(file_path_auth, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from app.main import limiter',
    'from app.core.rate_limit import limiter'
)

with open(file_path_auth, 'w', encoding='utf-8') as f:
    f.write(content)

print("Circular import fixed.")
