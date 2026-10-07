import re
with open('backend/services/auth_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'Database is offline and this account is not an official demo persona.*?priya\.nair@karmayogi\.gov\.in\.'
content = re.sub(pattern, 'Database is offline. Authentication requires active database connectivity.', content, flags=re.MULTILINE|re.DOTALL)

with open('backend/services/auth_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
