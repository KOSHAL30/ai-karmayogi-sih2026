import re
with open('backend/repositories/certificate_repository.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'class CertificateRepository:.*?_MEMORY_CERTIFICATES.*?\n\n',
    'class CertificateRepository:\n    def __init__(self, db=None):\n        self.db = db\n\n',
    text,
    flags=re.DOTALL
)
with open('backend/repositories/certificate_repository.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('backend/repositories/notification_repository.py', 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = re.sub(
    r'class NotificationRepository:.*?_MEMORY_NOTIFICATIONS.*?\n\n',
    'class NotificationRepository:\n    def __init__(self, db=None):\n        self.db = db\n\n',
    text2,
    flags=re.DOTALL
)
with open('backend/repositories/notification_repository.py', 'w', encoding='utf-8') as f:
    f.write(text2)
