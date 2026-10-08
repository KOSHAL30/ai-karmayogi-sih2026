import sys
import re

file_path = 'backend/app/main.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Disable Swagger/Redoc
content = content.replace('docs_url="/api/v1/docs",', 'docs_url=None,')
content = content.replace('redoc_url="/api/v1/redoc",', 'redoc_url=None,')
content = content.replace('openapi_url="/api/v1/openapi.json",', 'openapi_url=None,')

# 2. Add CSP and remove Server header in middleware
middleware_replacement = '''    # Inject Sovereign Defense Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://sih20126.mkhejyz.mongodb.net;"
    response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
    if "server" in response.headers:
        del response.headers["server"]'''
        
content = re.sub(r'    # Inject Sovereign Defense Security Headers\n(?:.*?\n)+?    # Audit Logging', middleware_replacement + '\n\n    # Audit Logging', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("main.py patched")
