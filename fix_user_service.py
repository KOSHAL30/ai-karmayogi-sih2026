import re

with open('backend/services/user_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the import
content = re.sub(r"try:\n    from services\.auth_service import DEMO_PERSONAS_AUTH\nexcept ImportError:\n    from app\.services\.auth_service import DEMO_PERSONAS_AUTH", "", content)

# 2. Remove the fallback in get_profile
fallback = r"        # Fallback check for demo accounts\n        for demo in DEMO_PERSONAS_AUTH\.values\(\):\n            if demo\[\"id\"\] == str\(user_id\) or demo\[\"id\"\] == user_id:\n                logger\.warning\(\"DATABASE OFFLINE: Using demo fallback persona\.\"\)\n                return UserProfileResponse\(\n                    id=demo\[\"id\"\],\n                    full_name=demo\[\"full_name\"\],\n                    email=demo\[\"email\"\],\n                    designation=demo\[\"designation\"\],\n                    role=demo\[\"role\"\],\n                    department=demo\[\"department\"\],\n                    work_role=demo\[\"work_role\"\],\n                    is_active=True\n                \)\n"
content = re.sub(fallback, "", content, flags=re.MULTILINE | re.DOTALL)

with open('backend/services/user_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
