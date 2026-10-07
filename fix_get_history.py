import re

with open('backend/services/assessment_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'eval_data = att.answer_log.get("evaluation", {})',
    'answer_log = _to_dict(att.answer_log) if hasattr(att, "answer_log") else {}\n            eval_data = answer_log.get("evaluation", {})'
)

content = content.replace(
    'att.answer_log.get("status", "IN_PROGRESS")',
    'answer_log.get("status", "IN_PROGRESS")'
)

with open('backend/services/assessment_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
