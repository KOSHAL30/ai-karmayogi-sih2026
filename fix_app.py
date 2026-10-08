import sys
import re

file_path = 'frontend/src/App.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'\s*\/\/\s*Ctrl \+ Shift \+ D[\s\S]*?if \(\(e\.ctrlKey \|\| e\.metaKey\) && e\.shiftKey && \(e\.key === \'D\' \|\| e\.key === \'d\'\)\) \{[\s\S]*?\}[\s\S]*?else if', '        if', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

file_path2 = 'frontend/src/components/navigation/CommandPalette.tsx'
with open(file_path2, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(', onOpenDemo', '')

# Also remove the whole block for action-demo-cockpit
pattern = re.compile(r'\{\s*id:\s*\'action-demo-cockpit\',[\s\S]*?perform:\s*\(\)\s*=>\s*\{[\s\S]*?\}\s*\},', re.MULTILINE)
content = re.sub(pattern, '', content)

with open(file_path2, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax errors.")
