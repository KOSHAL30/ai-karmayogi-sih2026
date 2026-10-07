import re

with open('backend/services/assessment_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the user_id mismatch in submit_assessment and process_answer 
content = content.replace("attempt.user_id != user_id:", "attempt.user_id != str(user_id):")

# Fix _serialize_question to use _to_dict(options)
content = content.replace('"options": options,', '"options": _to_dict(options),')

with open('backend/services/assessment_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
