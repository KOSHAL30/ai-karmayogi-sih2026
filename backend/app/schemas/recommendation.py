# ==============================================================================
# AI KARMAYOGI — RECOMMENDATION & LEARNING PATH PYDANTIC SCHEMAS
# Request and Response Models for Course Curation, Roadmaps & Telemetry
# ==============================================================================

import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class CourseResponse(BaseModel):
    id: uuid.UUID
    igot_course_id: str
    title: str
    description: Optional[str] = None
    ministry: str
    duration_minutes: int
    target_level: int
    difficulty: str
    language: str
    tags: List[str] = []
    learning_outcomes: List[str] = []
    course_url: str
    competency_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True

class RecommendationItemResponse(BaseModel):
    recommendation_id: str
    course_id: str
    igot_course_id: str
    title: str
    ministry: str
    duration_minutes: int
    target_level: int
    difficulty: str
    language: str
    tags: List[str] = []
    learning_outcomes: List[str] = []
    course_url: str
    competency_name: str
    competency_code: str
    competency_type: str
    priority: int
    confidence: float
    estimated_improvement: str
    trajectory_stage: str
    reason: str
    status: str
    is_completed: bool = False
    is_demo: Optional[bool] = False
    data_source: Optional[str] = "live"

class CriticalGapItem(BaseModel):
    competency_code: str
    competency_name: str
    competency_type: str
    mandated_level: int
    demonstrated_level: int
    deficit_pct: float
    deficit_score: float
    is_demo: Optional[bool] = False
    data_source: Optional[str] = "live"

class TelemetryMetrics(BaseModel):
    completion_percentage: float
    hours_learned: float
    completed_modules: int
    enrolled_modules: int
    acceptance_rate: float
    gap_reduction_achieved: float

class PillarForecast(BaseModel):
    pillar_name: str
    current_level: float
    predicted_level: float
    uplift: str
    mandated_target: float

class SkillForecastResponse(BaseModel):
    current_composite_score: float
    projected_composite_score: float
    projected_score_uplift: str
    pillars: Dict[str, PillarForecast]
    is_demo: Optional[bool] = False
    data_source: Optional[str] = "live"

class RoadmapCategories(BaseModel):
    immediate: List[RecommendationItemResponse]
    recommended_this_week: List[RecommendationItemResponse]
    advanced_modules: List[RecommendationItemResponse]
    optional_enrichment: List[RecommendationItemResponse]

class RecommendationDashboardResponse(BaseModel):
    overall_competency_score: float
    top_critical_gaps: List[CriticalGapItem]
    estimated_completion_hours: float
    total_recommended_modules: int
    telemetry: TelemetryMetrics
    roadmaps: RoadmapCategories
    skill_forecast: SkillForecastResponse
    is_demo: Optional[bool] = False
    data_source: Optional[str] = "live"

class PracticeQuiz(BaseModel):
    title: str
    question_count: int
    estimated_minutes: int
    is_demo: Optional[bool] = False
    data_source: Optional[str] = "live"

class TrajectoryMilestone(BaseModel):
    week_number: int
    title: str
    focus: str
    micro_learning_focus: str
    expected_gain: str
    practice_quiz: PracticeQuiz
    courses: List[RecommendationItemResponse]
    status: str
    is_demo: Optional[bool] = False
    data_source: Optional[str] = "live"

class LearningPathResponse(BaseModel):
    milestones: List[TrajectoryMilestone]
    telemetry: TelemetryMetrics
    is_demo: Optional[bool] = False
    data_source: Optional[str] = "live"

class CompleteCourseRequest(BaseModel):
    course_id: uuid.UUID
    time_spent_minutes: int = Field(default=20, ge=1, le=300)

class CompleteCourseResponse(BaseModel):
    message: str
    course_id: str
    progress_percentage: int
    completion_status: str
    telemetry: Dict[str, Any]
