import sys
import re

file_path = 'frontend/src/components/navigation/CommandPalette.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'\s*\{\s*id: \'action-demo-cockpit\',[\s\S]*?onOpenDemo\(\);\s*\},\s*\},', re.MULTILINE)
content = re.sub(pattern, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CommandPalette really fixed.")
