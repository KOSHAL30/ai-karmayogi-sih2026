with open('backend/services/auth_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('detail=\\"User account is inactive or deleted.\\"', 'detail="User account is inactive or deleted."')

with open('backend/services/auth_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
