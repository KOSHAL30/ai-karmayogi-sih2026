import sys
import re

file_path = 'backend/services/auth_service.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix enumeration
content = content.replace('detail="Invalid credentials."', 'detail="Invalid credentials or inactive account."')

# Change LoginResponseData return (Remove access_token and refresh_token from the schema in auth_service as well)
# Wait, auth_service returns eturn TokenPayload(...)?
# Let's see what auth_service.login returns.
