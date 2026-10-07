// ==============================================================================
// AI KARMAYOGI — COMPLETE TYPESCRIPT TYPE DEFINITIONS
// Fully Typed Frontend Contracts Matching Phase 2 & 3 Specifications
// ==============================================================================

export type UserRole = 'learner' | 'trainer' | 'admin' | 'department_head' | 'administrator';

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  designation: string;
  role: UserRole;
  department: string;
  work_role?: string;
  is_active: boolean;
}

export interface AuthState {
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export type CompetencyType = 'BEHAVIORAL' | 'FUNCTIONAL' | 'DOMAIN';

export interface FRACCompetency {
  id: string;
  competency_code: string;
  competency_name: string;
  competency_type: CompetencyType;
  mandated_level: number;
  demonstrated_level?: number;
  deficit_percentage?: number;
  description?: string;
}

export interface CompetencyGap {
  competency_code: string;
  competency_name: string;
  competency_type: CompetencyType;
  mandated_level: number;
  demonstrated_level: number;
  deficit_score: number;
  status: 'ACUTE_DEFICIT' | 'MODERATE_DEFICIT' | 'COMPETENT';
  remediation_focus: string;
}

export interface CourseRecommendation {
  recommendation_id: string;
  course_id: string;
  igot_course_id: string;
  course_title: string;
  duration_minutes: number;
  target_level: number;
  deficit_score: number;
  explainable_rationale: string;
  course_url: string;
  status: 'ACTIVE' | 'ENROLLED' | 'COMPLETED';
}

export type BloomLevel = 'REMEMBER' | 'UNDERSTAND' | 'APPLY' | 'ANALYZE' | 'EVALUATE';
export type DifficultyTier = 'EASY' | 'MEDIUM' | 'HARD';

export interface AssessmentQuestionOption {
  id: string;
  text: string;
}

export interface AssessmentQuestion {
  id: string;
  question_stem: string;
  bloom_level: string;
  options: AssessmentQuestionOption[];
  competency_name: string;
  competency_type: string;
  source_citation: string;
}

export interface StartAssessmentData {
  attempt_id: string;
  quiz_id: string;
  quiz_title: string;
  question: AssessmentQuestion | null;
  current_question_index: number;
  max_questions: number;
  min_questions: number;
  competencies: Array<{
    id: string;
    competency_code: string;
    competency_name: string;
    competency_type: string;
    mandated_level: number;
    description?: string;
  }>;
  timer_minutes: number;
}

export interface AnswerSubmitResult {
  attempt_id: string;
  is_completed: boolean;
  current_question_index: number;
  total_answered: number;
  max_questions: number;
  next_question: AssessmentQuestion | null;
  progress_percentage: number;
}

export interface CompetencyDeficitItem {
  competency_id: string;
  competency_code: string;
  competency_name: string;
  competency_type: string;
  mandated_level: number;
  demonstrated_level: number;
  theta_score: number;
  deficit_level: number;
  deficit_pct: number;
  status: 'ACUTE_DEFICIT' | 'MODERATE_DEFICIT' | 'COMPETENT';
  xai_explanation: string;
  questions_answered: number;
  questions_correct: number;
}

export interface AssessmentResultData {
  attempt_id: string;
  officer_name: string;
  designation: string;
  department: string;
  work_role: string;
  attempted_at: string | null;
  time_taken_seconds: number;
  score_achieved: number;
  total_questions: number;
  is_passed: boolean;
  overall_score: number;
  overall_status: 'EXEMPLARY' | 'COMPETENT' | 'MODERATE_DEFICIT' | 'ACUTE_DEFICIT';
  behavioral_score: number;
  functional_score: number;
  domain_score: number;
  composite_deficit_pct: number;
  competency_results: CompetencyDeficitItem[];
  strengths: string[];
  weaknesses: string[];
  recommended_action: string;
}

export interface AssessmentHistoryItemData {
  attempt_id: string;
  quiz_title: string;
  attempted_at: string | null;
  status: string;
  score_achieved: number;
  total_questions: number;
  overall_score: number | null;
  is_passed: boolean;
  time_taken_seconds: number;
}

export interface DepartmentHeatmapItem {
  competency_code: string;
  competency_name: string;
  competency_type: CompetencyType;
  mandated_average_level: number;
  demonstrated_average_level: number;
  cadre_gap_percentage: number;
  risk_classification: 'HIGH_PRIORITY' | 'MODERATE_PRIORITY' | 'LOW_PRIORITY';
}

export interface SystemHealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  environment: string;
  version: string;
  services: {
    postgresql: { status: string; latency_ms?: number; details?: string };
    ollama: { status: string; latency_ms?: number; details?: string };
  };
}

// --- PART 4: PERSONALIZED RECOMMENDATIONS & LEARNING PATH TYPES ---

export interface RecommendationItem {
  recommendation_id: string;
  course_id: string;
  igot_course_id: string;
  title: string;
  ministry: string;
  duration_minutes: number;
  target_level: number;
  difficulty: 'FOUNDATION' | 'INTERMEDIATE' | 'ADVANCED' | 'EXECUTIVE';
  language: string;
  tags: string[];
  learning_outcomes: string[];
  course_url: string;
  competency_name: string;
  competency_code: string;
  competency_type: CompetencyType;
  priority: number;
  confidence: number;
  estimated_improvement: string;
  trajectory_stage: 'IMMEDIATE' | 'RECOMMENDED_THIS_WEEK' | 'ADVANCED' | 'OPTIONAL_ENRICHMENT';
  reason: string;
  status: 'ACTIVE' | 'ENROLLED' | 'DISMISSED' | 'COMPLETED';
  is_completed: boolean;
}

export interface CriticalGapItem {
  competency_code: string;
  competency_name: string;
  competency_type: CompetencyType;
  mandated_level: number;
  demonstrated_level: number;
  deficit_pct: number;
  deficit_score: number;
}

export interface TelemetryMetrics {
  completion_percentage: number;
  hours_learned: number;
  completed_modules: number;
  enrolled_modules: number;
  acceptance_rate: number;
  gap_reduction_achieved: number;
}

export interface PillarForecast {
  pillar_name: string;
  current_level: number;
  predicted_level: number;
  uplift: string;
  mandated_target: number;
}

export interface SkillForecast {
  current_composite_score: number;
  projected_composite_score: number;
  projected_score_uplift: string;
  pillars: {
    functional: PillarForecast;
    domain: PillarForecast;
    behavioral: PillarForecast;
  };
}

export interface RoadmapCategories {
  immediate: RecommendationItem[];
  recommended_this_week: RecommendationItem[];
  advanced_modules: RecommendationItem[];
  optional_enrichment: RecommendationItem[];
}

export interface RecommendationDashboardData {
  overall_competency_score: number;
  top_critical_gaps: CriticalGapItem[];
  estimated_completion_hours: number;
  total_recommended_modules: number;
  telemetry: TelemetryMetrics;
  roadmaps: RoadmapCategories;
  skill_forecast: SkillForecast;
  is_demo?: boolean;
  data_source?: string;
}

export interface PracticeQuiz {
  title: string;
  question_count: number;
  estimated_minutes: number;
}

export interface TrajectoryMilestone {
  week_number: number;
  title: string;
  focus: string;
  micro_learning_focus: string;
  expected_gain: string;
  practice_quiz: PracticeQuiz;
  courses: RecommendationItem[];
  status: 'IN_PROGRESS' | 'UPCOMING' | 'COMPLETED';
}

export interface LearningPathData {
  milestones: TrajectoryMilestone[];
  telemetry: TelemetryMetrics;
  is_demo?: boolean;
  data_source?: string;
}

// --- PART 5: PDF INTELLIGENCE, SOVEREIGN RAG & AI MCQ GENERATION TYPES ---

export interface FAQItem {
  question: string;
  answer: string;
  rule_ref?: string;
}

export interface DocumentSummary {
  executive_summary: string;
  key_policy_changes: string[];
  important_clauses: string[];
  compliance_checklist: string[];
  action_points: string[];
  faqs: FAQItem[];
}

export interface DocumentItem {
  id: string;
  document_title: string;
  document_type: string;
  ministry: string;
  department?: string | null;
  om_number?: string | null;
  issue_date?: string | null;
  file_hash: string;
  file_size_bytes: number;
  total_pages: number;
  total_chunks: number;
  processing_status: 'PROCESSING' | 'INDEXED' | 'FAILED' | string;
  summary_json?: DocumentSummary | null;
  created_at: string;
}

export interface DocumentChunkItem {
  id: string;
  document_id: string;
  chunk_index: number;
  page_number: number;
  breadcrumb: string;
  content: string;
  token_count: number;
}

export interface CitationItem {
  chunk_id: string;
  document_id: string;
  document_title: string;
  page_number: number;
  breadcrumb: string;
  snippet: string;
  relevance_score: number;
}

export interface RAGResponse {
  answer: string;
  confidence_score: number;
  citations: CitationItem[];
  model: string;
  latency_ms: number;
}

export interface DraftMCQOption {
  id: string;
  option_text: string;
  is_correct: boolean;
  distractor_rationale?: string;
}

export interface DraftMCQ {
  id: string;
  question_stem: string;
  bloom_level: BloomLevel;
  difficulty: DifficultyTier;
  competency_id?: string;
  competency_name?: string;
  source_citation: string;
  pedagogical_explanation: string;
  options: DraftMCQOption[];
  is_approved?: boolean;
}

export interface GenerateMCQResponse {
  quiz_id: string;
  document_id: string;
  title: string;
  total_questions: number;
  questions: DraftMCQ[];
}

// --- PART 6: ADMIN ANALYTICS, CERTIFICATES & NOTIFICATIONS TYPES ---

export interface KPICardItem {
  key: string;
  label: string;
  value: any;
  display_value: string;
  change_pct: number;
  trend: 'up' | 'down' | 'neutral';
  period: string;
  description: string;
}

export interface MonthlyLearningTrend {
  month: string;
  active_learners: number;
  courses_completed: number;
  assessments_taken: number;
  hours_logged: number;
}

export interface DepartmentComparisonItem {
  department_code: string;
  department_name: string;
  ministry: string;
  officer_count: number;
  avg_competency: number;
  completion_pct: number;
  total_hours: number;
  highest_gap: string;
  rank: number;
}

export interface CompetencyDistribution {
  exemplary_pct: number;
  competent_pct: number;
  moderate_deficit_pct: number;
  acute_deficit_pct: number;
}

export interface FunnelStage {
  stage: string;
  count: number;
  conversion_pct: number;
}

export interface AdminDashboardData {
  kpis: Record<string, KPICardItem>;
  monthly_trends: MonthlyLearningTrend[];
  department_comparison: DepartmentComparisonItem[];
  competency_distribution: CompetencyDistribution;
  completion_funnel: FunnelStage[];
  timestamp: string;
}

export interface HeatmapCell {
  department_code: string;
  department_name: string;
  pillar: string;
  avg_score: number;
  deficit_pct: number;
  risk_level: 'LOW' | 'MODERATE' | 'HIGH';
}

export interface DepartmentAnalyticsData {
  total_departments: number;
  departments: DepartmentComparisonItem[];
  heatmap_matrix: HeatmapCell[];
  leaderboard: DepartmentComparisonItem[];
}

export interface RadarPoint {
  competency_code: string;
  competency_name: string;
  pillar: string;
  mandated_level: number;
  demonstrated_level: number;
  national_benchmark: number;
}

export interface CriticalDeficitItem {
  competency_code: string;
  competency_name: string;
  pillar: string;
  deficit_percentage: number;
  affected_officers_count: number;
  remediation_priority: 'URGENT' | 'HIGH' | 'MEDIUM';
}

export interface CompetencyIntelligenceData {
  radar_data: RadarPoint[];
  pillar_breakdown: Record<string, {
    pillar_name: string;
    mandated_avg: number;
    demonstrated_avg: number;
    gap_percentage: number;
    status: string;
    lead_deficit: string;
  }>;
  top_critical_competencies: CriticalDeficitItem[];
  improvement_trends: Array<{
    quarter: string;
    behavioral: number;
    functional: number;
    domain: number;
    composite: number;
  }>;
}

export interface CertificateItem {
  id: string;
  user_id: string;
  officer_name: string;
  designation: string;
  department: string;
  ministry: string;
  certificate_number: string;
  certificate_type: 'COURSE_COMPLETION' | 'ASSESSMENT_MASTERY' | 'LEARNING_PATH_COMPLETION';
  title: string;
  issuing_authority: string;
  issued_at: string;
  verification_code: string;
  verification_url: string;
  qr_code_data: string;
  metadata: {
    score_achieved?: number;
    credits_earned?: number;
    course_hours?: number;
    signatory_title?: string;
    [key: string]: any;
  };
}

export interface NotificationItem {
  id: string;
  user_id: string;
  title: string;
  message: string;
  notification_type: 'COURSE_ASSIGNED' | 'ASSESSMENT_REMINDER' | 'CERTIFICATE_AVAILABLE' | 'MILESTONE' | 'ANNOUNCEMENT';
  priority: 'LOW' | 'NORMAL' | 'HIGH' | 'URGENT';
  action_url?: string | null;
  is_read: boolean;
  created_at: string;
}

export interface NotificationListData {
  total_notifications: number;
  unread_count: number;
  notifications: NotificationItem[];
}
