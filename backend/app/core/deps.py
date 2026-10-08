# ==============================================================================
# AI KARMAYOGI — AUTHENTICATION & RBAC DEPENDENCIES (MongoDB)
# 3-Role Architecture (Learner, Trainer, Admin) with Dependency Injection
# ==============================================================================

import logging
import uuid
from typing import Annotated, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request
from app.core.database import get_db
from app.core.security import decode_access_token
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)
# Bearer token security scheme
security = HTTPBearer(auto_error=True)


async def get_current_user_payload(
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
    return payload


async def get_current_user(
    payload: dict = Depends(get_current_user_payload),
    db=Depends(get_db)
):
    """
    Retrieves the fully populated User from MongoDB using the token subject.
    """
    user_id_str = payload.get("sub")
    try:
        uuid.UUID(user_id_str)  # validate format
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed user identity claim.")

    user = None
    try:
        if db is not None:
            repo = UserRepository(db)
            user = await repo.get_by_id(user_id_str)
        else:
            logger.warning("DATABASE OFFLINE: User lookup cannot proceed because db is None.")
    except Exception as e:
        logger.warning("DATABASE OFFLINE: User lookup failed (%s: %s).", type(e).__name__, e)
        # We don't raise here immediately, we let the 'if not user:' block below handle it
        # so that we return a standard 401.

    if not user or not getattr(user, "is_active", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account not found or deactivated.")

    return user


def require_role(allowed_roles: list[str]) -> Callable:
    """
    Role-Based Access Control (RBAC) guard factory.
    Enforces that user role belongs to the allowed 3-role set: Learner, Trainer, Admin.
    """
    async def role_checker(user=Depends(get_current_user)):
        user_role = user.role.role_code.lower() if user.role else "learner"

        # Normalize 'administrator' to 'admin' for universal compatibility
        if user_role == "administrator":
            user_role = "admin"

        normalized_allowed = [r.lower() for r in allowed_roles]
        if "admin" in normalized_allowed and "administrator" not in normalized_allowed:
            normalized_allowed.append("administrator")

        if user_role not in normalized_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {', '.join(allowed_roles)}. Current role: '{user_role}'.",
            )
        return user
    return role_checker

# Predefined Dependency Guards for the 3 Core Roles:
RequireLearner = Depends(require_role(["learner", "admin"]))
RequireTrainer = Depends(require_role(["trainer", "admin"]))
RequireAdmin = Depends(require_role(["admin"]))
