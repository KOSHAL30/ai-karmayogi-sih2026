# ==============================================================================
# AI KARMAYOGI — HEALTH CHECK ENDPOINT
# Verifies Database, Groq API, and Ollama AI Health
# ==============================================================================

import time
from fastapi import APIRouter, Depends
import httpx
from typing import Optional
from app.core.database import get_db
from app.core.config import settings
from app.schemas.common import APIResponse
from app.schemas.health import HealthCheckResponse, ServiceHealth

router = APIRouter()

@router.get("/health", response_model=APIResponse[HealthCheckResponse])
async def check_system_health(db = Depends(get_db)):
    """
    Evaluates end-to-end service health across MongoDB, Groq, and Ollama.
    """
    services: dict[str, ServiceHealth] = {}
    overall_status = "healthy"

    # 1. Check MongoDB Database
    t0 = time.perf_counter()
    try:
        await db.command("ping")
        db_latency = round((time.perf_counter() - t0) * 1000, 2)
        services["mongodb"] = ServiceHealth(
            status="healthy",
            latency_ms=db_latency,
            details="Connected to MongoDB persistence engine"
        )
    except Exception as e:
        overall_status = "degraded"
        services["mongodb"] = ServiceHealth(status="unhealthy", details=str(e))

    # 2. Check Groq AI API (Primary)
    if settings.GROQ_API_KEY:
        t0 = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(
                    "https://api.groq.com/openai/v1/models",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
                )
                groq_latency = round((time.perf_counter() - t0) * 1000, 2)
                if resp.status_code == 200:
                    services["groq"] = ServiceHealth(
                        status="healthy",
                        latency_ms=groq_latency,
                        details="Connected. Groq API is operational."
                    )
                else:
                    services["groq"] = ServiceHealth(status="degraded", details=f"HTTP {resp.status_code}")
        except Exception as e:
            services["groq"] = ServiceHealth(status="unhealthy", details=f"Groq error: {str(e)}")
    else:
        services["groq"] = ServiceHealth(status="unconfigured", details="GROQ_API_KEY is not set")

    # 3. Check Sovereign Local Ollama AI Engine (Fallback)
    t0 = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/tags")
            ollama_latency = round((time.perf_counter() - t0) * 1000, 2)
            if resp.status_code == 200:
                models_info = resp.json().get("models", [])
                model_names = [m.get("name") for m in models_info]
                services["ollama"] = ServiceHealth(
                    status="healthy",
                    latency_ms=ollama_latency,
                    details=f"Connected. Loaded models: {', '.join(model_names) if model_names else 'None loaded yet'} (Fallback)"
                )
            else:
                services["ollama"] = ServiceHealth(status="degraded", details=f"Ollama returned HTTP {resp.status_code}")
    except Exception as e:
        services["ollama"] = ServiceHealth(status="optional", details=f"Ollama not running: {str(e)}")

    health_data = HealthCheckResponse(
        status=overall_status,
        environment=settings.ENVIRONMENT,
        version="1.0.0",
        services=services
    )

    return APIResponse(
        status="success",
        data=health_data,
        message="System health check evaluated successfully."
    )
