import os
import re

file_path = 'backend/app/api/v1/endpoints/documents.py'
with open(file_path, 'r') as f:
    content = f.read()

# Remove SQLAlchemy models import
content = re.sub(
    r'from app\.models\.entities import\s*\([^)]*\)',
    'from app.models.entities import new_uuid, utcnow',
    content,
    flags=re.MULTILINE
)
content = re.sub(
    r'from app\.models\.entities import.*',
    'from app.models.entities import new_uuid, utcnow',
    content
)

with open(file_path, 'w') as f:
    f.write(content)
