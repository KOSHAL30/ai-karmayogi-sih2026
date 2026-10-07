# ==============================================================================
# AI KARMAYOGI — CENTRAL API V1 ROUTER
# Mounts Sub-Routers for Auth, Users, Health, Assessment, etc.
# ==============================================================================

from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.assessment import router as assessment_router
from app.api.v1.endpoints.recommendations import router as recommendations_router, learning_path_router
from app.api.v1.endpoints.documents import (
    router as documents_router,
    rag_router,
    mcq_router
)
from app.api.v1.endpoints.admin import router as admin_router
from app.api.v1.endpoints.certificates import router as certificates_router
from app.api.v1.endpoints.notifications import router as notifications_router

api_router = APIRouter()

# Core Infrastructure Endpoints
api_router.include_router(health_router, tags=["System Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication & Session"])
api_router.include_router(users_router, prefix="/users", tags=["User Profile & Management"])
api_router.include_router(assessment_router, prefix="/assessment", tags=["Competency Assessment & Diagnostics"])
api_router.include_router(recommendations_router, prefix="/recommendations", tags=["Personalized Recommendations"])
api_router.include_router(learning_path_router, prefix="/learning-path", tags=["Learning Trajectory & Progress"])
api_router.include_router(documents_router, prefix="/documents", tags=["Document Intelligence & Uploads"])
api_router.include_router(rag_router, prefix="/rag", tags=["Sovereign RAG & Knowledge Base"])
api_router.include_router(mcq_router, prefix="/mcq", tags=["AI MCQ Generation Studio"])
api_router.include_router(admin_router, prefix="/admin", tags=["Executive Admin & Cadre Analytics"])
api_router.include_router(certificates_router, prefix="/certificates", tags=["Verifiable Digital Certificates"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["In-App Notifications & Alerts"])
