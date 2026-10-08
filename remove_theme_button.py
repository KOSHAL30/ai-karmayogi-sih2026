import sys
import re

file_path = 'frontend/src/components/layout/Navbar.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Match the Theme Toggle block in Navbar.tsx
pattern = re.compile(r'\s*\{\/\* Theme Toggle \*\/\}[\s\S]*?<\/button>', re.MULTILINE)
content = re.sub(pattern, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Theme Button removed.")
