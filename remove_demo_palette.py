import sys
import re

file_path = 'frontend/src/components/navigation/CommandPalette.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 'onOpenDemo' prop entirely
content = re.sub(r'onOpenDemo: \(\) => void;', '', content)
content = re.sub(r'onOpenDemo,', '', content)

# Remove the action-demo-cockpit object
content = re.sub(r"\{\s*id: 'action-demo-cockpit',[\s\S]*?\},", '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CommandPalette Demo removed.")
