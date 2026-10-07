# ==============================================================================
# AI KARMAYOGI — USER SCHEMAS
# Request and Response schemas for profile management and password operations
# ==============================================================================

from typing import Optional
from pydantic import BaseModel, Field

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=150, description="Full name of the official")
    designation: Optional[str] = Field(None, min_length=2, max_length=150, description="Official government designation")

class PasswordChangeRequest(BaseModel):
    old_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password meeting complexity criteria")
