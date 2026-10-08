# ==============================================================================
# AI KARMAYOGI — AUTHENTICATION ROUTER
# Login, Registration, Token Lifecycle, and Logout Endpoints
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.core.rate_limit import limiter
from app.core.database import get_db
from app.core.deps import get_current_user_payload
from app.schemas.common import APIResponse
from app.schemas.auth import (
    LoginRequest,
    LoginResponseData,
    RegisterRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutResponse,
    UserProfileResponse,
)
try:
    from services.auth_service import AuthService
    from services.user_service import UserService
except ImportError:
    from app.services.auth_service import AuthService
    from app.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=APIResponse[UserProfileResponse], status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db = Depends(get_db)
):
    """
    Registers a new civil service official into AI Karmayogi.
    Assigns role ('learner', 'trainer', or 'admin') and binds to department.
    """
    try:
        service = AuthService(db)
        user_profile = await service.register(
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            designation=data.designation,
            role_code=data.role_code,
            department_code=data.department_code,
        )
        return APIResponse(
            status="success",
            data=user_profile,
            message="User registered successfully."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database service is offline ({type(e).__name__}). Please check MongoDB or use an existing demo account."
        )

@router.post("/login", response_model=APIResponse[LoginResponseData])
@limiter.limit("5/minute")
async def login(
    request: Request,
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
    )

@router.post("/refresh", response_model=APIResponse[RefreshTokenResponse])
async def refresh_token(
    data: RefreshTokenRequest,
    db = Depends(get_db)
):
    """
    Exchanges a valid refresh token for a newly rotated access and refresh token pair.
    """
    service = AuthService(db)
    new_access, new_refresh = await service.refresh_access_token(data.refresh_token)
    return APIResponse(
        status="success",
        data=RefreshTokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="Bearer",
            expires_in=3600
        ),
        message="Tokens refreshed successfully."
    )

@router.post("/logout", response_model=APIResponse[LogoutResponse])
async def logout(
    payload: dict = Depends(get_current_user_payload)
):
    """
    Acknowledge client logout and signal token discard.
    """
    return APIResponse(
        status="success",
        data=LogoutResponse(message="Successfully logged out."),
        message="Session terminated."
    )

@router.get("/me", response_model=APIResponse[UserProfileResponse])
async def get_current_user(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Returns the authenticated user's profile details.
    """
    import uuid
    user_id = uuid.UUID(payload.get("sub"))
    service = UserService(db)
    profile = await service.get_profile(user_id)
    return APIResponse(
        status="success",
        data=profile,
        message="User profile retrieved."
    )
