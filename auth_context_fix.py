import sys

file_path = 'frontend/src/context/AuthContext.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("localStorage.getItem('karmayogi_token')", "null")
content = content.replace("localStorage.setItem('karmayogi_token', res.access_token);", "")
content = content.replace("localStorage.setItem('karmayogi_refresh_token', res.refresh_token);", "")
content = content.replace("localStorage.removeItem('karmayogi_token');", "")
content = content.replace("localStorage.removeItem('karmayogi_refresh_token');", "")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("AuthContext patched.")
