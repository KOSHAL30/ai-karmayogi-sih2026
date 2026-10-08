import sys
import re

file_path = 'frontend/src/components/layout/Navbar.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove Subtle Demo Quick-Launcher
pattern1 = re.compile(r'\{\/\* Subtle Demo Quick-Launcher \(Discreet for SIH Evaluation\) \*\/\}[\s\S]*?<\/button>', re.MULTILINE)
content = re.sub(pattern1, '', content)

# Remove Discreet Demo Switcher Modal
pattern2 = re.compile(r'\{\/\* Discreet Demo Switcher Modal \(Activated via subtle trigger for SIH Evaluation\) \*\/\}[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*\)}', re.MULTILINE)
content = re.sub(pattern2, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Navbar Demo removed.")
