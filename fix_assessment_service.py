import re

with open('backend/services/assessment_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("attempt.user_id != user_id:", "attempt.user_id != str(user_id):")

with open('backend/services/assessment_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
