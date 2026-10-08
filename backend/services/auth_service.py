# ==============================================================================
# AI KARMAYOGI — AUTHENTICATION SERVICE (MongoDB)
# Business Logic for Registration, Credential Verification, and Token Lifecycle
# ==============================================================================

import logging
import uuid
from typing import Optional
from fastapi import HTTPException, status
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)
from app.models.entities import new_uuid, utcnow
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    validate_password_strength,
)
from app.schemas.auth import LoginResponseData, UserProfileResponse


class AuthService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    async def register(
        self,
        email: str,
        password: str,
        full_name: str,
        designation: str,
        role_code: str = "learner",
        department_code: Optional[str] = None
    ) -> UserProfileResponse:
        # 1. Check if user already exists
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An account with email '{email}' already exists."
            )

        # 2. Validate password strength
        is_strong, err_msg = validate_password_strength(password)
        if not is_strong:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)

        # 3. Resolve role
        role = await self.repo.get_role_by_code(role_code)
        if not role:
            role = await self.repo.get_role_by_code("learner")
            if not role:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested role and default learner role are unavailable. Please seed the database.")

        # 4. Resolve department
        dept = None
        if department_code:
            dept = await self.repo.get_department_by_code(department_code)
        if not dept:
            dept = await self.repo.get_default_department()
            if not dept:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested department and default department are unavailable. Please seed the database.")

        # 5. Create user document
        user_id = new_uuid()
        user_data = {
            "_id": user_id,
            "email": email.lower().strip(),
            "password_hash": get_password_hash(password),
            "full_name": full_name.strip(),
            "designation": designation.strip(),
            "role_id": role.id,
            "role_code": role.role_code,
            "role_name": getattr(role, "role_name", role.role_code.title()),
            "department_id": dept.id,
            "department_code": dept.department_code,
            "department_name": dept.name,
            "ministry_name": getattr(dept, "ministry_name", "Government of India"),
            "work_role_id": None,
            "work_role_code": None,
            "work_role_title": None,
            "government_id_hash": f"GOV-ID-{uuid.uuid4().hex[:10].upper()}",
            "is_active": True,
        }

        user = await self.repo.create(user_data)

        return UserProfileResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            designation=user.designation,
            role=user.role.role_code,
            department=user.department.name,
            work_role=None,
            is_active=user.is_active
        )

    async def login(self, email: str, password: str) -> LoginResponseData:
        normalized_email = email.lower().strip()
        user = None
        db_connected = True
        try:
            user = await self.repo.get_by_email(normalized_email)
        except Exception as e:
            db_connected = False
            logger.warning("DATABASE OFFLINE: User lookup failed (%s: %s).", type(e).__name__, e)

        if user and user.is_active:
            is_valid = False
            try:
                    is_valid = verify_password(password, user.password_hash)
            except Exception:
                is_valid = False

            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials or inactive account."
                )

            role_code = user.role.role_code if user.role else "learner"
            dept_name = user.department.name if user.department else "General Administration"
            wbr_title = user.work_role.role_title if user.work_role else None

            access_token = create_access_token(
                subject=str(user.id),
                role=role_code,
                department_id=str(user.department_id) if hasattr(user, 'department_id') and user.department_id else None,
                work_role=wbr_title
            )
            refresh_token = create_refresh_token(subject=str(user.id))

            profile = UserProfileResponse(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                designation=user.designation,
                role=role_code,
                department=dept_name,
                work_role=wbr_title,
                is_active=user.is_active
            )

            return LoginResponseData(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer",
                expires_in=3600,
                user=profile
            )


        if not db_connected:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is offline. Authentication requires active database connectivity."
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or inactive account."
        )

    async def refresh_access_token(self, refresh_token: str) -> tuple[str, str]:
        payload = decode_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token."
            )

        user_id_str = payload.get("sub")
        try:
            uuid.UUID(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token subject.")

        user = None
        try:
            user = await self.repo.get_by_id(user_id_str)
        except Exception:
            pass

        if user and user.is_active:
            role_code = user.role.role_code if user.role else "learner"
            wbr_title = user.work_role.role_title if user.work_role else None
            dept_id = str(user.department_id) if hasattr(user, 'department_id') and user.department_id else None
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive or deleted.")

        new_access_token = create_access_token(
            subject=str(user_id_str),
            role=role_code,
            department_id=dept_id,
            work_role=wbr_title
        )
        new_refresh_token = create_refresh_token(subject=str(user_id_str))

        return new_access_token, new_refresh_token
