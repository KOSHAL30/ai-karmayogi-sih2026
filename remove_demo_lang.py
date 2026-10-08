import sys
import re

file_path = 'frontend/src/context/LanguageContext.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'login.sih_quick_logins': 'SIH 2026 Quick Logins:'", "'login.quick_logins': 'Quick Logins:'")
content = re.sub(r"'login\.sih_quick_logins': '.*?'", "'login.quick_logins': 'Quick Logins:'", content)
content = re.sub(r"'overview\.badge': '.*?'", "'overview.badge': 'Mission Karmayogi Bharat Sovereign Portal'", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Language files updated.")
