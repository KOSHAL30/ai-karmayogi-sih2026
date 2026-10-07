# ==============================================================================
# AI KARMAYOGI — ADMIN ANALYTICS, CERTIFICATES & NOTIFICATIONS SCHEMAS
# Strictly Typed Pydantic Contracts Matching Phase 4 Part 6 Specifications
# ==============================================================================

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# --- KPI & DASHBOARD SCHEMAS ---

class KPICardItem(BaseModel):
    key: str
    label: str
    value: Any
    display_value: str
    change_pct: float
    trend: str = Field(..., description="'up' | 'down' | 'neutral'")
    period: str = "vs last month"
    description: str


class MonthlyLearningTrend(BaseModel):
    month: str
    active_learners: int
    courses_completed: int
    assessments_taken: int
    hours_logged: float


class DepartmentComparisonItem(BaseModel):
    department_code: str
    department_name: str
    ministry: str
    officer_count: int
    avg_competency: float
    completion_pct: float
    total_hours: float
    highest_gap: str
    rank: int


class CompetencyDistribution(BaseModel):
    exemplary_pct: float
    competent_pct: float
    moderate_deficit_pct: float
    acute_deficit_pct: float


class FunnelStage(BaseModel):
    stage: str
    count: int
    conversion_pct: float


class AdminDashboardResponse(BaseModel):
    kpis: Dict[str, KPICardItem]
    monthly_trends: List[MonthlyLearningTrend]
    department_comparison: List[DepartmentComparisonItem]
    competency_distribution: CompetencyDistribution
    completion_funnel: List[FunnelStage]
    timestamp: str
    data_source: Optional[str] = Field("live", description="Data source indicator: 'live' or 'demo baseline'")
    is_demo_baseline: Optional[bool] = Field(False, description="Flag indicating if payload contains static demo baseline data")
    data_mode: Optional[str] = Field("live", description="Mode identifier: 'live' or 'demo baseline'")


# --- DEPARTMENT ANALYTICS SCHEMAS ---

class HeatmapCell(BaseModel):
    department_code: str
    department_name: str
    pillar: str  # BEHAVIORAL, FUNCTIONAL, DOMAIN
    avg_score: float
    deficit_pct: float
    risk_level: str  # LOW, MODERATE, HIGH


class DepartmentAnalyticsResponse(BaseModel):
    total_departments: int
    departments: List[DepartmentComparisonItem]
    heatmap_matrix: List[HeatmapCell]
    leaderboard: List[DepartmentComparisonItem]
    data_source: Optional[str] = Field("live", description="Data source indicator: 'live' or 'demo baseline'")
    is_demo_baseline: Optional[bool] = Field(False, description="Flag indicating if payload contains static demo baseline data")
    data_mode: Optional[str] = Field("live", description="Mode identifier: 'live' or 'demo baseline'")


# --- COMPETENCY INTELLIGENCE SCHEMAS ---

class RadarPoint(BaseModel):
    competency_code: str
    competency_name: str
    pillar: str
    mandated_level: float
    demonstrated_level: float
    national_benchmark: float


class CriticalDeficitItem(BaseModel):
    competency_code: str
    competency_name: str
    pillar: str
    deficit_percentage: float
    affected_officers_count: int
    remediation_priority: str  # URGENT, HIGH, MEDIUM


class CompetencyIntelligenceResponse(BaseModel):
    radar_data: List[RadarPoint]
    pillar_breakdown: Dict[str, Dict[str, Any]]
    top_critical_competencies: List[CriticalDeficitItem]
    improvement_trends: List[Dict[str, Any]]
    data_source: Optional[str] = Field("live", description="Data source indicator: 'live' or 'demo baseline'")
    is_demo_baseline: Optional[bool] = Field(False, description="Flag indicating if payload contains static demo baseline data")
    data_mode: Optional[str] = Field("live", description="Mode identifier: 'live' or 'demo baseline'")


# --- CERTIFICATES SCHEMAS ---

class CertificateItem(BaseModel):
    id: str
    user_id: str
    officer_name: str
    designation: str
    department: str
    ministry: str
    certificate_number: str
    certificate_type: str  # COURSE_COMPLETION, ASSESSMENT_MASTERY, LEARNING_PATH_COMPLETION
    title: str
    issuing_authority: str
    issued_at: str
    verification_code: str
    verification_url: str
    qr_code_data: str
    metadata: Dict[str, Any]


class CertificateListResponse(BaseModel):
    total_certificates: int
    certificates: List[CertificateItem]


class CertificateGenerateRequest(BaseModel):
    user_id: Optional[str] = None
    certificate_type: str = "COURSE_COMPLETION"
    title: str
    course_id: Optional[str] = None
    quiz_attempt_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# --- NOTIFICATIONS SCHEMAS ---

class NotificationItem(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    notification_type: str  # COURSE_ASSIGNED, ASSESSMENT_REMINDER, CERTIFICATE_AVAILABLE, MILESTONE, ANNOUNCEMENT
    priority: str = "NORMAL"  # LOW, NORMAL, HIGH, URGENT
    action_url: Optional[str] = None
    is_read: bool
    created_at: str


class NotificationListResponse(BaseModel):
    total_notifications: int
    unread_count: int
    notifications: List[NotificationItem]


class NotificationReadRequest(BaseModel):
    notification_id: str
