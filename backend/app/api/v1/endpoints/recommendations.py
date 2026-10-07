# ==============================================================================
# AI KARMAYOGI — RECOMMENDATION & LEARNING PATH ROUTER
# Endpoints for Course Curation, Dynamic Roadmaps, Timelines & Telemetry
# ==============================================================================

import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.core.deps import get_current_user_payload
from app.schemas.common import APIResponse
from app.schemas.recommendation import (
    CourseResponse,
    RecommendationDashboardResponse,
    LearningPathResponse,
    CompleteCourseRequest,
    CompleteCourseResponse,
)
try:
    from services.learning_path_service import LearningPathService
    from services.recommendation_service import RecommendationService
    from repositories.course_repository import CourseRepository
except ImportError:
    from app.services.learning_path_service import LearningPathService
    from app.services.recommendation_service import RecommendationService
    from app.repositories.course_repository import CourseRepository

router = APIRouter()
learning_path_router = APIRouter()

# ------------------------------------------------------------------------------
# 1. Recommendation Dashboard
# ------------------------------------------------------------------------------
@router.get("", response_model=APIResponse[RecommendationDashboardResponse])
@router.get("/", response_model=APIResponse[RecommendationDashboardResponse])
async def get_recommendation_dashboard(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Returns the comprehensive AI Recommendation Dashboard containing:
    - Overall score & top 3 critical gaps
    - Curated learning roadmaps (Immediate, This Week, Advanced, Optional)
    - Predictive skill forecast and telemetry KPI metrics
    """
    try:
        user_id = uuid.UUID(str(payload.get("sub")))
        service = LearningPathService(db)
        data = await service.get_dashboard_summary(user_id)
        return APIResponse.success(
            data=data,
            message="Recommendation dashboard retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

# ------------------------------------------------------------------------------
# 2. Personalized Learning Path / Milestones
# ------------------------------------------------------------------------------
@router.get("/path", response_model=APIResponse[LearningPathResponse])
async def get_learning_path(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Retrieves the 4-week structured milestone trajectory and telemetry progress.
    """
    try:
        user_id = uuid.UUID(str(payload.get("sub")))
        service = LearningPathService(db)
        milestones = await service.generate_weekly_timeline(user_id)
        telemetry = await service.rec_repo.get_telemetry_metrics(user_id)
        is_demo = any(bool(m.get("is_demo", False)) for m in milestones) if milestones else True
        return APIResponse.success(
            data={
                "milestones": milestones,
                "telemetry": telemetry,
                "is_demo": is_demo,
                "data_source": "demo" if is_demo else "live",
            },
            message="Learning trajectory retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve learning path: {str(e)}"
        )

# ------------------------------------------------------------------------------
# 3. Course Details by ID
# ------------------------------------------------------------------------------
@router.get("/course/{course_id}", response_model=APIResponse[CourseResponse])
async def get_course_details(
    course_id: uuid.UUID,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Retrieves complete syllabus, outcomes, and metadata for a specific iGOT course.
    """
    course_repo = CourseRepository(db)
    course = await course_repo.get_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found"
        )
    return APIResponse.success(
        data=course,
        message="Course details retrieved successfully"
    )

# ------------------------------------------------------------------------------
# 4. Regenerate Recommendations
# ------------------------------------------------------------------------------
@router.post("/regenerate", response_model=APIResponse[RecommendationDashboardResponse])
async def regenerate_recommendations(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Clears cached recommendations and recalculates multi-objective course rankings.
    """
    try:
        user_id = uuid.UUID(str(payload.get("sub")))
        rec_service = RecommendationService(db)
        await rec_service.get_or_generate_recommendations(user_id, force_regenerate=True)
        
        path_service = LearningPathService(db)
        dashboard_data = await path_service.get_dashboard_summary(user_id)
        return APIResponse.success(
            data=dashboard_data,
            message="Recommendations regenerated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to regenerate recommendations: {str(e)}"
        )

# ------------------------------------------------------------------------------
# 5. Complete Course / Progress Telemetry
# ------------------------------------------------------------------------------
@router.post("/complete", response_model=APIResponse[CompleteCourseResponse])
async def complete_course(
    request: CompleteCourseRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    """
    Marks an iGOT course as completed, records time spent, and updates competency telemetry.
    """
    try:
        user_id = uuid.UUID(str(payload.get("sub")))
        service = LearningPathService(db)
        res = await service.mark_course_completed(
            user_id=user_id,
            course_id=request.course_id,
            time_spent_minutes=request.time_spent_minutes
        )
        return APIResponse.success(
            data=res,
            message="Course completion telemetry recorded"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record course completion: {str(e)}"
        )

# Mirror endpoints on learning_path_router for dedicated /learning-path prefix
@learning_path_router.get("", response_model=APIResponse[LearningPathResponse])
@learning_path_router.get("/", response_model=APIResponse[LearningPathResponse])
async def get_learning_path_root(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    return await get_learning_path(payload, db)

@learning_path_router.post("/complete", response_model=APIResponse[CompleteCourseResponse])
async def complete_learning_path_course(
    request: CompleteCourseRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db)
):
    return await complete_course(request, payload, db)
