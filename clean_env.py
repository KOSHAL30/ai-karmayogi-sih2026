import sys
import re

file_path = 'backend/.env'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('GROQ_API_KEY=gsk_your_groq_api_key_here\n', '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned .env")
