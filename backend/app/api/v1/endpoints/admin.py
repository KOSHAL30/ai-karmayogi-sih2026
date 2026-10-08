# ==============================================================================
# AI KARMAYOGI — EXECUTIVE ADMIN & ANALYTICS ENDPOINTS
# Real-Time Telemetry, Departmental Heatmaps, Competency Radar & Funnels
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db
from app.core.deps import get_current_user_payload, RequireAdmin
from app.schemas.analytics import (
    AdminDashboardResponse,
    DepartmentAnalyticsResponse,
    CompetencyIntelligenceResponse,
)
try:
    from services.analytics_service import AnalyticsService
except ImportError:
    from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/dashboard", response_model=AdminDashboardResponse)
async def get_admin_dashboard(
    user = RequireAdmin,
    db = Depends(get_db),
):
    """
    Returns high-level executive dashboard metrics:
    - 6 Executive KPI Cards (Total Officers, Active Learners, Assessments, etc.)
    - 6-Month Monthly Learning Trend
    - Departmental Comparative Benchmarks
    - Competency Tier Distribution (Exemplary -> Acute Deficit)
    - Completion Funnel from Cadre Enrollment to Certification
    """
    try:
        data = await analytics_service.get_dashboard_data(db)
        return data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compile executive dashboard analytics: {str(e)}",
        )


@router.get("/departments", response_model=DepartmentAnalyticsResponse)
async def get_department_analytics(
    user = RequireAdmin,
    db = Depends(get_db),
):
    """
    Returns department-level intelligence:
    - 12 Central Government Departments with officer count & learning hours
    - 3-Pillar Cross-Matrix Heatmap (Behavioral, Functional, Domain)
    - Department Performance Leaderboard & Risk Classifications
    """
    try:
        return await analytics_service.get_department_analytics(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch departmental analytics: {str(e)}",
        )


@router.get("/competencies", response_model=CompetencyIntelligenceResponse)
async def get_competency_intelligence(
    user = RequireAdmin,
    db = Depends(get_db),
):
    """
    Returns 3-Pillar FRAC Competency Intelligence:
    - 10-Axis Radar Chart (Mandated vs Demonstrated vs National Benchmark)
    - Functional, Domain, and Behavioral Deficit Summaries
    - Ranked List of Critical Civil Service Capability Gaps
    - Longitudinal Improvement Trajectories
    """
    try:
        return await analytics_service.get_competency_intelligence(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assemble competency intelligence: {str(e)}",
        )


@router.get("/trends")
async def get_admin_trends(
    user = RequireAdmin,
    db = Depends(get_db),
):
    """Returns longitudinal time-series trends and predictive growth targets."""
    try:
        return await analytics_service.get_time_series_trends(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute learning trajectory trends: {str(e)}",
        )
