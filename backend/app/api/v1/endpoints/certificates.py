# ==============================================================================
# AI KARMAYOGI — CERTIFICATES ENDPOINTS
# Verifiable Digital Credentials, Public Validation Hashes & PDF Export Payloads
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from app.core.database import get_db
from app.core.deps import get_current_user_payload
from app.schemas.analytics import (
    CertificateItem,
    CertificateListResponse,
    CertificateGenerateRequest,
)
try:
    from services.certificate_service import CertificateService
except ImportError:
    from app.services.certificate_service import CertificateService

router = APIRouter()
cert_service = CertificateService()


@router.get("", response_model=CertificateListResponse)
async def list_certificates(
    all_cadre: bool = Query(False, description="If true and user is admin/trainer, lists all certificates"),
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db),
):
    """
    Retrieves certificates:
    - Learners retrieve their personal verifiable certificates.
    - Admins and Trainers can query all issued credentials across the cadre.
    """
    try:
        user_role = payload.get("role", "learner")
        user_id = payload.get("sub")
        user_filter = None if (all_cadre and user_role in ["admin", "administrator", "trainer", "department_head"]) else user_id
        certs = await cert_service.list_certificates(db, user_id=user_filter)
        return {"total_certificates": len(certs), "certificates": certs}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch certificates: {str(e)}",
        )


@router.get("/{certificate_id}", response_model=CertificateItem)
async def get_certificate(
    certificate_id: str,
    db = Depends(get_db),
):
    """Publicly verifiable certificate lookup by UUID or certificate number."""
    cert = await cert_service.get_certificate(db, certificate_id=certificate_id)
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate record not found in the sovereign verification database.",
        )
    return cert


@router.post("/generate", response_model=CertificateItem, status_code=status.HTTP_201_CREATED)
async def generate_certificate(
    req: CertificateGenerateRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db),
):
    """Issues an official verifiable certificate upon course, assessment or milestone completion."""
    try:
        target_user_id = req.user_id or payload.get("sub", "00000000-0000-0000-0000-000000000001")
        cert = await cert_service.generate_certificate(
            db=db,
            user_id=target_user_id,
            certificate_type=req.certificate_type,
            title=req.title,
            course_id=req.course_id,
            quiz_attempt_id=req.quiz_attempt_id,
            metadata=req.metadata,
        )
        return cert
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate digital credential: {str(e)}",
        )
