import sys
import re

file_path = 'backend/app/schemas/auth.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''class LoginResponseData(BaseModel):
    user: UserProfileResponse'''
    
content = re.sub(r'class LoginResponseData\(BaseModel\):[\s\S]*?user: UserProfileResponse', replacement, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Schemas patched")
