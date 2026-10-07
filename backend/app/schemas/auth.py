# ==============================================================================
# AI KARMAYOGI — AUTHENTICATION & USER SCHEMAS
# Login, Registration, Token Lifecycle, and Profile Serialization
# ==============================================================================

import re
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field, field_validator

EMAIL_REGEX = r"^[\w\.\+\-]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,}$"

class LoginRequest(BaseModel):
    email: str = Field(..., description="Official government email address")
    password: str = Field(..., min_length=6)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if not re.match(EMAIL_REGEX, clean):
            raise ValueError("Invalid email address format.")
        return clean

class RegisterRequest(BaseModel):
    email: str = Field(..., description="Official government email address")
    password: str = Field(..., min_length=8, description="Must have uppercase, lowercase, digit, special char")
    full_name: str = Field(..., min_length=2, max_length=150)
    designation: str = Field(..., min_length=2, max_length=150)
    role_code: str = Field("learner", description="Role: learner, trainer, or admin")
    department_code: Optional[str] = Field(None, description="Department code (e.g., DEPT-DOPT)")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if not re.match(EMAIL_REGEX, clean):
            raise ValueError("Invalid email address format.")
        return clean

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Valid JWT refresh token")

class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600

class LogoutResponse(BaseModel):
    message: str = "Successfully logged out"

class WorkRoleSummary(BaseModel):
    id: UUID
    role_code: str
    role_title: str

class UserProfileResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    designation: str
    role: str
    department: str
    work_role: Optional[str] = None
    is_active: bool

class LoginResponseData(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 3600
    user: UserProfileResponse

class TokenPayload(BaseModel):
    sub: str
    role: str
    dept: Optional[str] = None
    work_role: Optional[str] = None
    exp: int
