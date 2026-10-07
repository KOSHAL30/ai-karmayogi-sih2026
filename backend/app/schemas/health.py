# ==============================================================================
# AI KARMAYOGI — SYSTEM HEALTH SCHEMAS
# Diagnostics for Database, Redis, and Local Ollama Models
# ==============================================================================

from typing import Optional, Dict
from pydantic import BaseModel

class ServiceHealth(BaseModel):
    status: str  # "healthy" | "unhealthy" | "degraded"
    latency_ms: Optional[float] = None
    details: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str
    environment: str
    version: str
    services: Dict[str, ServiceHealth]
