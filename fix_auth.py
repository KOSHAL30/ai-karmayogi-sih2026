import sys
import re

# 1. Restore LoginResponseData schema with tokens so backend logic doesn't break,
# but we will just return the user field in the route.
file_path = 'backend/app/schemas/auth.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''class LoginResponseData(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 3600
    user: UserProfileResponse'''
    
content = re.sub(r'class LoginResponseData\(BaseModel\):\n    user: UserProfileResponse', replacement, content)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update auth.py to not leak tokens in body
file_path = 'backend/app/api/v1/endpoints/auth.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('data=login_data,', 'data={"user": login_data.user},')
# Remove LoginResponseData from response_model
content = content.replace('response_model=APIResponse[LoginResponseData]', 'response_model=APIResponse')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Fix enumeration in auth_service.py
file_path = 'backend/services/auth_service.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('detail="Invalid credentials."', 'detail="Invalid credentials or inactive account."')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Auth fixes applied.")
