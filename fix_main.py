with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_msg = 'print("[AI Karmayogi] Running in demo-fallback mode (auth will use hardcoded personas).")'
new_msg = 'print("[AI Karmayogi] Database is unreachable. Authentication and data retrieval will fail.")'
content = content.replace(old_msg, new_msg)

with open('backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
