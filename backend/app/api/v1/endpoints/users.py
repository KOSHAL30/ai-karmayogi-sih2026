# ==============================================================================
# AI KARMAYOGI — USERS ROUTER
# Profile Retrieval, Profile Updates, and Password Management
# ==============================================================================

import uuid
from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.core.deps import get_current_user_payload
from app.schemas.common import APIResponse
from app.schemas.auth import UserProfileResponse
from app.schemas.user import UserUpdateRequest, PasswordChangeRequest
try:
    from services.user_service import UserService
except ImportError:
    from app.services.user_service import UserService

router = APIRouter()

@router.get("/me", response_model=APIResponse[UserProfileResponse])
async def get_my_profile(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Fetch the complete profile of the currently authenticated civil servant.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = UserService(db)
    profile = await service.get_profile(user_id)
    return APIResponse(
        status="success",
        data=profile,
        message="Profile retrieved successfully."
    )

@router.put("/me", response_model=APIResponse[UserProfileResponse])
async def update_my_profile(
    data: UserUpdateRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Update profile attributes (name, designation) for the authenticated official.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = UserService(db)
    updated_profile = await service.update_profile(
        user_id=user_id,
        full_name=data.full_name,
        designation=data.designation
    )
    return APIResponse(
        status="success",
        data=updated_profile,
        message="Profile updated successfully."
    )

@router.put("/me/password", response_model=APIResponse[dict])
async def change_my_password(
    data: PasswordChangeRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Securely rotate password after validating current password and enforcing strength policy.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = UserService(db)
    await service.change_password(
        user_id=user_id,
        old_password=data.old_password,
        new_password=data.new_password
    )
    return APIResponse(
        status="success",
        data={"updated": True},
        message="Password updated successfully."
    )
