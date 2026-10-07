# ==============================================================================
# AI KARMAYOGI — ASSESSMENT SCHEMAS
# Request and Response Models for Diagnostic Assessment & FRAC Evaluation
# ==============================================================================

from uuid import UUID
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field

class QuestionOption(BaseModel):
    id: str
    text: str

class QuestionResponse(BaseModel):
    id: UUID
    question_stem: str
    bloom_level: str
    options: List[Union[QuestionOption, Dict[str, Any], str]]
    competency_name: str
    competency_type: str
    source_citation: str

class StartAssessmentResponse(BaseModel):
    attempt_id: UUID
    quiz_id: UUID
    quiz_title: str
    question: Optional[QuestionResponse] = None
    current_question_index: int
    max_questions: int
    min_questions: int
    competencies: List[Dict[str, Any]]
    timer_minutes: int

class AnswerSubmitRequest(BaseModel):
    attempt_id: UUID
    question_id: UUID
    selected_option_index: int = Field(..., ge=0, le=3)
    time_spent_seconds: int = Field(default=15, ge=0)

class AnswerSubmitResponse(BaseModel):
    attempt_id: UUID
    is_completed: bool
    current_question_index: int
    total_answered: int
    max_questions: int
    next_question: Optional[QuestionResponse] = None
    progress_percentage: float

class AssessmentFinalSubmitRequest(BaseModel):
    attempt_id: UUID

class CompetencyDeficitResult(BaseModel):
    competency_id: str
    competency_code: str
    competency_name: str
    competency_type: str
    mandated_level: int
    demonstrated_level: int
    theta_score: float
    deficit_level: int
    deficit_pct: float
    status: str
    xai_explanation: str
    questions_answered: int
    questions_correct: int

class AssessmentResultResponse(BaseModel):
    attempt_id: UUID
    officer_name: str
    designation: str
    department: str
    work_role: str
    attempted_at: Optional[str] = None
    time_taken_seconds: int
    score_achieved: int
    total_questions: int
    is_passed: bool
    overall_score: float
    overall_status: str
    behavioral_score: float
    functional_score: float
    domain_score: float
    composite_deficit_pct: float
    competency_results: List[CompetencyDeficitResult]
    strengths: List[str]
    weaknesses: List[str]
    recommended_action: str

class AssessmentHistoryItem(BaseModel):
    attempt_id: UUID
    quiz_title: str
    attempted_at: Optional[str] = None
    status: str
    score_achieved: int
    total_questions: int
    overall_score: Optional[float] = None
    is_passed: bool
    time_taken_seconds: int
