import sys
import re

file_path = 'frontend/src/lib/api.ts'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace localStorage logic
content = re.sub(r"const token = localStorage.getItem\('karmayogi_token'\);", "const token = null;", content)
content = re.sub(r"if \(token\) \{[\s\S]*?\}", "", content)

# Make fetch include credentials
content = content.replace("const config: RequestInit = {", "const config: RequestInit = {\n      credentials: 'include',")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("api.ts patched")
