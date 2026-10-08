import sys

file_path = 'backend/.env'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert MongoDB to local
import re
content = re.sub(r'^MONGODB_URI=.*$', 'MONGODB_URI=mongodb://localhost:27017', content, flags=re.MULTILINE)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Reverted to local DB, kept new API key.")
