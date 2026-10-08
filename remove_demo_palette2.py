import sys
import re

file_path = 'frontend/src/components/navigation/CommandPalette.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 'onOpenDemo?: () => void;'
content = re.sub(r'\s*onOpenDemo\??: \(\) => void;', '', content)
# Remove 'onOpenDemo,' from props
content = re.sub(r'onOpenDemo,', '', content)

# Remove the action-demo-cockpit object from the COMMANDS array
# The object looks like:
# {
#   id: 'action-demo-cockpit',
#   ...
# },
pattern = re.compile(r'\{\s*id:\s*\'action-demo-cockpit\',[\s\S]*?perform:\s*\(\)\s*=>\s*\{[\s\S]*?\}\s*\},', re.MULTILINE)
content = re.sub(pattern, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CommandPalette fixed safely.")
