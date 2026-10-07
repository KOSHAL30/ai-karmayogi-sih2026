with open('backend/services/auth_service.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('logger.warning("DATABASE OFFLINE: User lookup failed (%s: %s).", type(e).__name__, e)', 'print("DB EXCEPTION:", type(e).__name__, e)')
with open('backend/services/auth_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
