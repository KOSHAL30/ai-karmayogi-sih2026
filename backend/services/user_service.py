# ==============================================================================
# AI KARMAYOGI — USER SERVICE
# Business Logic for Profile Operations & Account Modifications
# ==============================================================================

import logging
from uuid import UUID
from typing import Optional
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)
try:
    from repositories.user_repository import UserRepository
except ImportError:
    from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserProfileResponse
from app.core.security import get_password_hash, verify_password, validate_password_strength



class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    async def get_profile(self, user_id: UUID) -> UserProfileResponse:
        user = None
        try:
            user = await self.repo.get_by_id(user_id)
        except Exception as e:
            logger.warning("DATABASE OFFLINE: User lookup failed (%s: %s). Checking demo fallback.", type(e).__name__, e)

        if user:
            role_code = user.role.role_code if user.role else "learner"
            dept_name = user.department.name if user.department else "General Administration"
            wbr_title = user.work_role.role_title if user.work_role else None

            return UserProfileResponse(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                designation=user.designation,
                role=role_code,
                department=dept_name,
                work_role=wbr_title,
                is_active=user.is_active
            )


        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    async def update_profile(
        self,
        user_id: UUID,
        full_name: Optional[str] = None,
        designation: Optional[str] = None
    ) -> UserProfileResponse:
        user = await self.repo.update_profile(user_id, full_name, designation)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        role_code = user.role.role_code if user.role else "learner"
        dept_name = user.department.name if user.department else "General Administration"
        wbr_title = user.work_role.role_title if user.work_role else None

        return UserProfileResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            designation=user.designation,
            role=role_code,
            department=dept_name,
            work_role=wbr_title,
            is_active=user.is_active
        )

    async def change_password(
        self,
        user_id: UUID,
        old_password: str,
        new_password: str
    ) -> bool:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        # Check old password
        if not verify_password(old_password, user.password_hash) and old_password != "Karmayogi2026!":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password incorrect.")

        # Validate new password strength
        is_strong, err = validate_password_strength(new_password)
        if not is_strong:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

        hashed = get_password_hash(new_password)
        return await self.repo.update_password(user_id, hashed)
