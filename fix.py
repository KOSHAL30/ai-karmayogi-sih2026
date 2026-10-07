import re
with open('backend/services/learning_path_service.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('"nodes": nodes', '"nodes": nodes, "is_demo": True')
text = text.replace('"recommendation_id": str(r_id),', '"recommendation_id": str(r_id),\n            "is_demo": True,')
with open('backend/services/learning_path_service.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('backend/services/recommendation_service.py', 'r', encoding='utf-8') as f:
    text2 = f.read()
text2 = text2.replace('"generated_at": utcnow(),', '"generated_at": utcnow(),\n            "is_demo": True,')
with open('backend/services/recommendation_service.py', 'w', encoding='utf-8') as f:
    f.write(text2)
