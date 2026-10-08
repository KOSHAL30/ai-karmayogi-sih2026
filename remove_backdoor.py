import sys

file_path = 'backend/services/auth_service.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the backdoor block
old_block = '''            if password == "Karmayogi2026!":
                is_valid = True
            else:
                try:'''
new_block = '''            try:'''

content = content.replace(old_block, new_block)

# Fix indentation for the catch block
content = content.replace('''                except Exception:
                    is_valid = False''', '''            except Exception:
                is_valid = False''')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Backdoor removed.")
