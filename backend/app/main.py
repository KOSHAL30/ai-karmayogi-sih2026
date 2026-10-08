# ==============================================================================
# AI KARMAYOGI — MASTER FASTAPI APPLICATION
# ASGI Lifespan, MongoDB Init, Security Headers, Rate Limiting & Route Mounting
# ==============================================================================

import time
import logging
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.database import init_mongodb, close_mongodb
from app.api.v1.router import api_router

logger = logging.getLogger(__name__)

# In-memory sliding window rate limiter: IP -> list of timestamps
RATE_LIMIT_WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 120
ip_request_history: defaultdict = defaultdict(list)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and graceful shutdown cycles.
    Initializes MongoDB connection and ensures indexes on startup.
    """
    print(f"[AI Karmayogi] Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode...")
    # Initialize MongoDB connection
    try:
        db = await init_mongodb()
        # Create essential indexes (idempotent)
        await db["users"].create_index("email", unique=True)
        await db["roles"].create_index("role_code", unique=True)
        await db["departments"].create_index("department_code", unique=True)
        await db["work_roles"].create_index("role_code", unique=True)
        await db["competencies"].create_index("competency_code", unique=True)
        await db["courses"].create_index("igot_course_id", unique=True)
        await db["certificates"].create_index("certificate_number", unique=True)
        await db["documents"].create_index("file_hash", unique=True)
        await db["quiz_attempts"].create_index([("user_id", 1), ("attempted_at", -1)])
        await db["recommendations"].create_index([("user_id", 1), ("status", 1)])
        await db["notifications"].create_index([("user_id", 1), ("created_at", -1)])
        await db["learning_progress"].create_index([("user_id", 1), ("course_id", 1)], unique=True)
        await db["document_chunks"].create_index([("document_id", 1), ("chunk_index", 1)])
        print("[AI Karmayogi] MongoDB indexes created/verified.")
    except Exception as e:
        print(f"[AI Karmayogi] MongoDB connection failed: {e}")
        print("[AI Karmayogi] Database is unreachable. Authentication and data retrieval will fail.")

    yield

    # Shutdown
    await close_mongodb()
    print("[AI Karmayogi] Application shutdown complete.")

# Initialize FastAPI Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sovereign AI-Enabled Capacity Building & Competency Diagnostic Platform for Mission Karmayogi (SIH26101)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers & Rate Limiting Middleware
@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    client_ip = request.client.host if request.client else "unknown"

    # Bypass rate limits for health checks and static docs
    path = request.url.path
    if not (path.startswith("/api/v1/docs") or path.startswith("/api/v1/openapi") or path == "/health"):
        now = time.time()
        # Clean older requests outside the window
        timestamps = [ts for ts in ip_request_history[client_ip] if now - ts < RATE_LIMIT_WINDOW_SECONDS]
        if len(timestamps) >= MAX_REQUESTS_PER_WINDOW:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "status": "error",
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Rate limit exceeded ({MAX_REQUESTS_PER_WINDOW} req/min). Please wait before retrying.",
                    },
                },
                headers={"Retry-After": "60"},
            )
        timestamps.append(now)
        ip_request_history[client_ip] = timestamps

    # Execute request pipeline
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start_time) * 1000

    # Inject Sovereign Defense Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

    # Audit Logging for Administrative & RAG routes
    if path.startswith("/api/v1/admin") or path.startswith("/api/v1/documents") or path.startswith("/api/v1/certificates"):
        print(f"[AUDIT] {request.method} {path} | Status: {response.status_code} | IP: {client_ip} | Duration: {duration_ms:.2f}ms")

    return response

# Global Validation Error Handler (RFC 7807 compliance)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        {"field": ".".join(str(loc) for loc in err["loc"]), "issue": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": {
                "code": "REQUEST_VALIDATION_ERROR",
                "message": "The incoming payload failed schema validation.",
                "details": details,
            },
        },
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR] Unhandled exception on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred."
        }
    )

# Mount Central v1 API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint for quick health / discovery."""
    return {
        "project": "AI Karmayogi",
        "mandate": "National Programme for Civil Services Capacity Building (Mission Karmayogi)",
        "problem_statement": "SIH26101",
        "docs_url": "/api/v1/docs",
        "status": "operational",
    }

@app.get("/health")
async def root_health():
    """Root health endpoint for container healthchecks, proxy routing, and local monitoring."""
    from app.api.v1.endpoints.health import check_system_health
    return await check_system_health()
