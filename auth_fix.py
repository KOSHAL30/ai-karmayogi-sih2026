import sys

file_path = 'backend/app/api/v1/endpoints/auth.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from fastapi import APIRouter, Depends, HTTPException, status',
    'from fastapi import APIRouter, Depends, HTTPException, status, Response'
)

old_login = '''@router.post("/login", response_model=APIResponse[LoginResponseData])
async def login(
    data: LoginRequest,
    db = Depends(get_db)
):
    """
    Authenticates an official and issues signed JWT access and refresh tokens.
    """
    service = AuthService(db)
    login_data = await service.login(
        email=data.email,
        password=data.password
    )
    return APIResponse(
        status="success",
        data=login_data,
        message="Authentication successful."
    )'''

new_login = '''@router.post("/login", response_model=APIResponse[LoginResponseData])
async def login(
    data: LoginRequest,
    response: Response,
    db = Depends(get_db)
):
    """
    Authenticates an official and issues signed JWT access and refresh tokens via HttpOnly cookies.
    """
    service = AuthService(db)
    login_data = await service.login(
        email=data.email,
        password=data.password
    )
    
    # Issue Secure HttpOnly Cookies
    response.set_cookie(
        key="access_token",
        value=login_data.access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=3600 # 1 hour
    )
    response.set_cookie(
        key="refresh_token",
        value=login_data.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=604800 # 7 days
    )
    
    return APIResponse(
        status="success",
        data=login_data,
        message="Authentication successful."
    )'''

content = content.replace(old_login, new_login)

old_logout = '''@router.post("/logout", response_model=APIResponse[LogoutResponse])
async def logout(
    payload: dict = Depends(get_current_user_payload)
):
    """
    Invalidates the current session.
    """
    # Note: In a stateless JWT architecture, actual invalidation requires a token blocklist.
    # We rely on client-side deletion for this iteration.
    return APIResponse(
        status="success",
        data=LogoutResponse(message="Successfully logged out."),
        message="Session terminated."
    )'''

new_logout = '''@router.post("/logout", response_model=APIResponse[LogoutResponse])
async def logout(
    response: Response,
    payload: dict = Depends(get_current_user_payload)
):
    """
    Invalidates the current session.
    """
    response.delete_cookie("access_token", secure=True, httponly=True, samesite="none")
    response.delete_cookie("refresh_token", secure=True, httponly=True, samesite="none")
    return APIResponse(
        status="success",
        data=LogoutResponse(message="Successfully logged out."),
        message="Session terminated."
    )'''

content = content.replace(old_logout, new_logout)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Auth endpoints patched.")
