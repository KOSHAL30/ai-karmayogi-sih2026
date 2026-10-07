# ==============================================================================
# AI KARMAYOGI — ASSESSMENT ROUTER
# Adaptive Diagnostic API, 2PL IRT Submission, and Explainable Heatmap Retrieval
# ==============================================================================

import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.core.deps import get_current_user_payload
from app.schemas.common import APIResponse
from app.schemas.assessment import (
    StartAssessmentResponse,
    AnswerSubmitRequest,
    AnswerSubmitResponse,
    AssessmentFinalSubmitRequest,
    AssessmentResultResponse,
    AssessmentHistoryItem,
)
try:
    from services.assessment_service import AssessmentService
except ImportError:
    from app.services.assessment_service import AssessmentService

router = APIRouter()

@router.get("/start", response_model=APIResponse[StartAssessmentResponse])
async def start_assessment(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Initializes or resumes an adaptive diagnostic assessment for the civil servant.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = AssessmentService(db)
    session_data = await service.start_assessment(user_id)
    return APIResponse(
        status="success",
        data=session_data,
        message="Assessment session initialized."
    )

@router.post("/answer", response_model=APIResponse[AnswerSubmitResponse])
async def submit_answer(
    data: AnswerSubmitRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Submits an answer to a question, recalibrates latent trait theta, and delivers next adaptive item.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = AssessmentService(db)
    response_data = await service.process_answer(
        user_id=user_id,
        attempt_id=data.attempt_id,
        question_id=data.question_id,
        selected_option_index=data.selected_option_index,
        time_spent_seconds=data.time_spent_seconds
    )
    return APIResponse(
        status="success",
        data=response_data,
        message="Answer registered and adaptive state updated."
    )

@router.post("/submit", response_model=APIResponse[Dict[str, Any]])
async def finalize_assessment(
    data: AssessmentFinalSubmitRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Concludes the assessment session and computes overall score, gap percentages, and XAI rationales.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = AssessmentService(db)
    result_data = await service.submit_assessment(user_id, data.attempt_id)
    return APIResponse(
        status="success",
        data=result_data,
        message="Assessment submitted and competency diagnostic compiled successfully."
    )

@router.get("/result/{attempt_id}", response_model=APIResponse[AssessmentResultResponse])
async def get_assessment_result(
    attempt_id: uuid.UUID,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Retrieves the complete diagnostic dossier including radar chart data, heatmap, and XAI explanations.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = AssessmentService(db)
    result_dossier = await service.get_result(user_id, attempt_id)
    return APIResponse(
        status="success",
        data=result_dossier,
        message="Diagnostic report retrieved successfully."
    )

@router.get("/history", response_model=APIResponse[List[AssessmentHistoryItem]])
async def get_assessment_history(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Retrieves the historical record of diagnostic assessments undertaken by the officer.
    """
    user_id = uuid.UUID(payload.get("sub"))
    service = AssessmentService(db)
    history_list = await service.get_history(user_id)
    return APIResponse(
        status="success",
        data=history_list,
        message="Assessment history retrieved."
    )
