import re

with open('backend/services/assessment_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'attempt.attempted_at.isoformat() if attempt.attempted_at else None',
    'attempt.attempted_at if isinstance(attempt.attempted_at, str) else attempt.attempted_at.isoformat() if attempt.attempted_at else None'
)

content = content.replace(
    'att.attempted_at.isoformat() if att.attempted_at else None',
    'att.attempted_at if isinstance(att.attempted_at, str) else att.attempted_at.isoformat() if att.attempted_at else None'
)

with open('backend/services/assessment_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
