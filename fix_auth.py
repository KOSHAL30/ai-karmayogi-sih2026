import re

with open('backend/services/auth_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove DEMO_PERSONAS_AUTH block
content = re.sub(r"DEMO_PERSONAS_AUTH = \{.*?^\}\n\n", "", content, flags=re.MULTILINE | re.DOTALL)

# 2. Remove fallback logic in login()
login_fallback = r"        # Fallback: Canonical SIH Demo Personas when database is unseeded or offline.*?is_active=True\n            \)\n\n            return LoginResponseData\(\n                access_token=access_token,\n                refresh_token=refresh_token,\n                token_type=\"Bearer\",\n                expires_in=3600,\n                user=profile\n            \)\n"
content = re.sub(login_fallback, "", content, flags=re.MULTILINE | re.DOTALL)

# Also update the db_connected if block in login() to remove demo persona message
offline_err = r"Database is offline and this account is not an official demo persona\. Please use rajesh\.kumar@gov\.in, sunita\.deshmukh@nic\.in, or priya\.nair@karmayogi\.gov\.in\."
content = content.replace(offline_err, "Database is offline. Authentication requires active database connectivity.")

# 3. Remove fallback logic in refresh_token()
refresh_fallback = r"        else:\n            demo_match = None\n            for p in DEMO_PERSONAS_AUTH\.values\(\):\n                if p\[\"id\"\] == user_id_str:\n                    demo_match = p\n                    break\n            if not demo_match:\n                raise HTTPException\(status_code=status\.HTTP_401_UNAUTHORIZED, detail=\"User account is inactive or deleted\.\"\)\n            logger\.warning\(\"DATABASE OFFLINE: Using demo fallback persona\.\"\)\n            role_code = demo_match\[\"role\"\]\n            wbr_title = demo_match\[\"work_role\"\]\n            dept_id = demo_match\[\"department_id\"\]\n"
refresh_replacement = r"        else:\n            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"User account is inactive or deleted.\")\n"
content = re.sub(refresh_fallback, refresh_replacement, content, flags=re.MULTILINE | re.DOTALL)

with open('backend/services/auth_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
