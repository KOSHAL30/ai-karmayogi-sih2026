-- ============================================================================
-- AI KARMAYOGI — PRODUCTION POSTGRESQL SCHEMA
-- Problem Statement: SIH26101
-- Database: PostgreSQL 16 with pgvector Extension
-- Key Format: UUID v4 (Sovereign Distributed Identity)
-- Embedding Dimensions: 768 (nomic-embed-text via Ollama)
-- ============================================================================

-- 1. Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ============================================================================
-- 2. ADMINISTRATIVE & IDENTITY CLUSTER
-- ============================================================================

-- Table 1: roles
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code VARCHAR(50) UNIQUE NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_role_code CHECK (role_code IN ('learner', 'trainer', 'department_head', 'administrator'))
);

COMMENT ON TABLE roles IS 'Authoritative system access roles for RBAC enforcement.';

-- Table 2: departments
CREATE TABLE IF NOT EXISTS departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    department_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    ministry_name VARCHAR(255) NOT NULL,
    tier VARCHAR(50) DEFAULT 'CENTRAL' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_department_tier CHECK (tier IN ('CENTRAL', 'STATE', 'LOCAL', 'AUTONOMOUS'))
);

COMMENT ON TABLE departments IS 'Ministries, Directorates, and Administrative Departments.';

-- Table 3: work_roles
CREATE TABLE IF NOT EXISTS work_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    department_id UUID NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
    role_title VARCHAR(200) NOT NULL,
    role_code VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE work_roles IS 'Specific Work-Based Roles (WBR) defined under Mission Karmayogi.';

-- Table 4: frac_competencies
CREATE TABLE IF NOT EXISTS frac_competencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    work_role_id UUID REFERENCES work_roles(id) ON DELETE SET NULL,
    competency_type VARCHAR(50) NOT NULL,
    competency_name VARCHAR(255) NOT NULL,
    competency_code VARCHAR(100) UNIQUE NOT NULL,
    mandated_level INT NOT NULL DEFAULT 3,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_competency_type CHECK (competency_type IN ('BEHAVIORAL', 'FUNCTIONAL', 'DOMAIN')),
    CONSTRAINT chk_mandated_level CHECK (mandated_level BETWEEN 1 AND 5)
);

COMMENT ON TABLE frac_competencies IS 'Framework of Roles, Activities, and Competencies (FRAC) Dictionary.';

-- Table 5: users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    department_id UUID NOT NULL REFERENCES departments(id) ON DELETE RESTRICT,
    work_role_id UUID REFERENCES work_roles(id) ON DELETE SET NULL,
    government_id_hash VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    designation VARCHAR(150) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE users IS 'Civil servants, Trainers, Department Heads, and System Administrators.';

-- ============================================================================
-- 3. COMPETENCY & LEARNING CLUSTER
-- ============================================================================

-- Table 6: courses
CREATE TABLE IF NOT EXISTS courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    competency_id UUID REFERENCES frac_competencies(id) ON DELETE SET NULL,
    igot_course_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_minutes INT DEFAULT 30 NOT NULL,
    target_level INT DEFAULT 3 NOT NULL,
    course_url TEXT NOT NULL,
    is_published BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_target_level CHECK (target_level BETWEEN 1 AND 5)
);

COMMENT ON TABLE courses IS 'Courses and micro-modules available on the iGOT Karmayogi ecosystem.';

-- Table 7: recommendations
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    competency_id UUID NOT NULL REFERENCES frac_competencies(id) ON DELETE CASCADE,
    deficit_score NUMERIC(5, 2) NOT NULL,
    explainable_rationale TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'ACTIVE' NOT NULL,
    generated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_rec_status CHECK (status IN ('ACTIVE', 'ENROLLED', 'DISMISSED', 'COMPLETED')),
    CONSTRAINT chk_deficit_score CHECK (deficit_score BETWEEN 0.00 AND 100.00)
);

COMMENT ON TABLE recommendations IS 'Targeted course recommendations generated based on diagnosed FRAC gaps.';

-- Table 8: learning_progress
CREATE TABLE IF NOT EXISTS learning_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    progress_percentage INT DEFAULT 0 NOT NULL,
    time_spent_minutes INT DEFAULT 0 NOT NULL,
    completion_status VARCHAR(50) DEFAULT 'IN_PROGRESS' NOT NULL,
    last_accessed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMPTZ,
    CONSTRAINT uq_user_course_progress UNIQUE (user_id, course_id),
    CONSTRAINT chk_progress_pct CHECK (progress_percentage BETWEEN 0 AND 100),
    CONSTRAINT chk_completion_status CHECK (completion_status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED'))
);

COMMENT ON TABLE learning_progress IS 'Civil servant course interaction and completion telemetry.';

-- Table 9: certificates
CREATE TABLE IF NOT EXISTS certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    certificate_number VARCHAR(100) UNIQUE NOT NULL,
    verification_hash VARCHAR(255) UNIQUE NOT NULL,
    issued_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL
);

COMMENT ON TABLE certificates IS 'Accredited micro-credentials issued upon verified competency gap closure.';

-- ============================================================================
-- 4. COGNITIVE AI & DOCUMENT CLUSTER
-- ============================================================================

-- Table 10: documents
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    uploaded_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    document_title VARCHAR(255) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    processing_status VARCHAR(50) DEFAULT 'PENDING' NOT NULL,
    total_pages INT DEFAULT 0 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_document_type CHECK (document_type IN ('ACT', 'RULE', 'CIRCULAR', 'OM', 'MANUAL', 'TRAINING_COLLATERAL')),
    CONSTRAINT chk_doc_status CHECK (processing_status IN ('PENDING', 'PARSING', 'CHUNKED', 'EMBEDDED', 'FAILED', 'PROCESSED'))
);

COMMENT ON TABLE documents IS 'Uploaded sovereign government training documents, Acts, and OMs.';

-- Table 11: document_chunks
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    chunk_content TEXT NOT NULL,
    token_count INT NOT NULL,
    section_reference VARCHAR(150),
    page_number INT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_doc_chunk_index UNIQUE (document_id, chunk_index)
);

COMMENT ON TABLE document_chunks IS 'Statutory text segments preserved with legal provisos and section markers.';

-- Table 12: embeddings
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id UUID UNIQUE NOT NULL REFERENCES document_chunks(id) ON DELETE CASCADE,
    embedding_vector_768 vector(768) NOT NULL,
    model_version VARCHAR(100) DEFAULT 'nomic-embed-text' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE embeddings IS '768-dimensional dense semantic vectors generated by local nomic-embed-text.';

-- ============================================================================
-- 5. PEDAGOGICAL ASSESSMENT & GOVERNANCE CLUSTER
-- ============================================================================

-- Table 13: quizzes
CREATE TABLE IF NOT EXISTS quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    quiz_type VARCHAR(50) DEFAULT 'FORMATIVE' NOT NULL,
    passing_percentage INT DEFAULT 60 NOT NULL,
    status VARCHAR(50) DEFAULT 'DRAFT' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_quiz_type CHECK (quiz_type IN ('DIAGNOSTIC', 'FORMATIVE', 'SUMMATIVE', 'SPACED_RETRIEVAL')),
    CONSTRAINT chk_quiz_status CHECK (status IN ('DRAFT', 'SME_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED')),
    CONSTRAINT chk_quiz_passing CHECK (passing_percentage BETWEEN 40 AND 100)
);

COMMENT ON TABLE quizzes IS 'Accredited assessment containers aligned with FRAC and Bloom Taxonomy.';

-- Table 14: questions
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    competency_id UUID REFERENCES frac_competencies(id) ON DELETE SET NULL,
    question_stem TEXT NOT NULL,
    bloom_level VARCHAR(50) DEFAULT 'APPLY' NOT NULL,
    options JSONB NOT NULL,
    correct_option_index INT NOT NULL,
    pedagogical_rationale TEXT NOT NULL,
    source_citation VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_bloom_level CHECK (bloom_level IN ('REMEMBER', 'UNDERSTAND', 'APPLY', 'ANALYZE', 'EVALUATE')),
    CONSTRAINT chk_correct_index CHECK (correct_option_index BETWEEN 0 AND 3)
);

COMMENT ON TABLE questions IS 'Psychometrically robust MCQs featuring realistic administrative distractors.';

-- Table 15: quiz_attempts
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE RESTRICT,
    score_achieved INT NOT NULL,
    total_questions INT NOT NULL,
    is_passed BOOLEAN NOT NULL,
    time_taken_seconds INT NOT NULL,
    answer_log JSONB NOT NULL,
    attempted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_score_valid CHECK (score_achieved <= total_questions AND score_achieved >= 0)
);

COMMENT ON TABLE quiz_attempts IS 'Immutable submission logs measuring demonstrated capability.';

-- Table 16: notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'INFO' NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_notif_type CHECK (notification_type IN ('INFO', 'GAP_ALERT', 'QUIZ_AVAILABLE', 'BADGE_EARNED'))
);

COMMENT ON TABLE notifications IS 'Contextual alerts for capability building triggers.';

-- Table 17: audit_logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE RESTRICT,
    action_name VARCHAR(100) NOT NULL,
    entity_name VARCHAR(100) NOT NULL,
    entity_id UUID,
    ip_address VARCHAR(45) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

COMMENT ON TABLE audit_logs IS 'Immutable security audit trail for statutory non-repudiation.';

-- ============================================================================
-- 6. INDEXING & PERFORMANCE OPTIMIZATION
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);
CREATE INDEX IF NOT EXISTS idx_users_department_id ON users(department_id);
CREATE INDEX IF NOT EXISTS idx_users_work_role_id ON users(work_role_id);
CREATE INDEX IF NOT EXISTS idx_work_roles_department_id ON work_roles(department_id);
CREATE INDEX IF NOT EXISTS idx_frac_work_role_id ON frac_competencies(work_role_id);
CREATE INDEX IF NOT EXISTS idx_frac_competency_type ON frac_competencies(competency_type);

CREATE INDEX IF NOT EXISTS idx_courses_competency_id ON courses(competency_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_status ON recommendations(status);
CREATE INDEX IF NOT EXISTS idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_certificates_user_id ON certificates(user_id);

CREATE INDEX IF NOT EXISTS idx_documents_uploaded_by ON documents(uploaded_by);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(processing_status);
CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON document_chunks(document_id);

CREATE INDEX IF NOT EXISTS idx_quizzes_document_id ON quizzes(document_id);
CREATE INDEX IF NOT EXISTS idx_quizzes_created_by ON quizzes(created_by);
CREATE INDEX IF NOT EXISTS idx_questions_quiz_id ON questions(quiz_id);
CREATE INDEX IF NOT EXISTS idx_questions_bloom_level ON questions(bloom_level);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_quiz_id ON quiz_attempts(quiz_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id_unread ON notifications(user_id) WHERE is_read = FALSE;
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- GIN Indexes on JSONB Columns
CREATE INDEX IF NOT EXISTS idx_questions_options_gin ON questions USING GIN (options);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_answer_log_gin ON quiz_attempts USING GIN (answer_log);
CREATE INDEX IF NOT EXISTS idx_audit_logs_metadata_gin ON audit_logs USING GIN (metadata);

-- HNSW Vector Index on pgvector (Cosine Distance)
CREATE INDEX IF NOT EXISTS idx_embeddings_hnsw ON embeddings 
USING hnsw (embedding_vector_768 vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
