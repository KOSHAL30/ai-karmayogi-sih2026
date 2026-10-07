# ==============================================================================
# AI KARMAYOGI — COMMON RESPONSE SCHEMAS
# Standard API Response Envelope & Error Formats
# ==============================================================================

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class APIResponse(BaseModel, Generic[DataT]):
    """Standard success envelope matching Phase 2 specifications."""
    status: str = "success"
    data: DataT
    message: Optional[str] = None

    @classmethod
    def success(cls, data: DataT, message: Optional[str] = None) -> "APIResponse[DataT]":
        return cls(status="success", data=data, message=message)

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: str

class ErrorPayload(BaseModel):
    code: str
    message: str
    details: Optional[list[ErrorDetail]] = None
    timestamp: str

class ErrorResponse(BaseModel):
    """Standard RFC 7807 compliant error envelope."""
    status: str = "error"
    error: ErrorPayload

class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
