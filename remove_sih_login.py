import sys
import re

file_path = 'frontend/src/pages/auth/Login.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("t('login.sih_quick_logins', 'SIH 2026 Quick Logins:')", "t('login.quick_logins', 'Quick Logins:')")
content = content.replace("{/* SIH 2026 Evaluation Quick Logins */}", "{/* Quick Logins */}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Login SIH reference removed.")
