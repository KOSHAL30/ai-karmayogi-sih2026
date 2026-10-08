import sys

file_path = 'backend/app/core/deps.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials',
    'from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials\nfrom fastapi import Request'
)

old_payload = '''async def get_current_user_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """
    Validates the Bearer JWT and extracts the user claims payload.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid access token. Please re-authenticate.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload'''

new_payload = '''async def get_current_user_payload(
    request: Request
) -> dict:
    """
    Validates the JWT from HttpOnly cookies and extracts the user claims payload.
    """
    token = request.cookies.get("access_token")
    if not token:
        # Fallback to Bearer for programmatic API access
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token. Please log in.",
        )
        
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid access token. Please re-authenticate.",
        )
    return payload'''

content = content.replace(old_payload, new_payload)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Deps patched.")
