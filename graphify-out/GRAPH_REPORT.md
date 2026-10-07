# Graph Report - AI-Karmayogi  (2026-09-18)

## Corpus Check
- 177 files · ~135,007 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: .bat 3, .example 1, (none) 1)

## Summary
- 1197 nodes · 2513 edges · 96 communities (58 shown, 38 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 166 edges (avg confidence: 0.95)
- Token cost: 12,000 input · 3,200 output

## Community Hubs (Navigation)
- Diagnostic Assessment Engine
- Course Catalog & Repositories
- Frontend TypeScript Types
- Verifiable Certificate Management
- Notification Center & Alerts
- Frontend Root App & Navigation
- Adaptive Learning Pathways
- Cadre Analytics & Reporting
- Database Engine & Connection Pool
- Authentication & Session Security
- Department & Cadre Hierarchy
- JWT Cryptography & Security
- FRAC Competency Taxonomy
- Administrative KPI & UI Components
- Admin Analytics Endpoints
- PyMuPDF Document Ingestion Pipeline
- Item Response Theory Scoring Engine
- Ollama RAG & Vector Retrieval
- Automated Item MCQ Generation
- UI Design System & Primitives
- Trainer Studio & Document Parsing
- System Architecture & Documentation
- Theme & Indicator Context
- Radar & Performance Charting
- Mission Karmayogi PRD & Vision
- Assessment Repositories Repository Module
- Ref Package React Module
- Components Documents Certificates Module
- Pdf Test Service Module
- Components Assessment Pages Module
- Repositories Repository Analytics Module
- Admin Components Trendchart Module
- Components Card Button Module
- Api Endpoints Users Module
- Package Dependencies React Module
- Tsconfig Node Compileroptions Module
- Embedding Service Embeddingservice Module
- Schemas Common Core Module
- Document Repositories Repository Module
- Api Endpoints Admin Module
- Rag Service Ragservice Module
- Main Fastapi System Module
- Alembic Env Run Module
- Package Devdependencies Types Module
- Mcq Service Mcqservice Module
- Health Main Api Module
- Components Documents Questioneditor Module
- Toastcontext Context Notify Module
- Health Schemas Core Module
- Test Tests Recommendation Module
- Languagecontext Context Languagecontexttype Module
- Ref Components Documents Module
- Main Middleware Exception Module
- Test Tests Assessment Module
- Test Tests Rag Module
- Skeleton Components Cardskeleton Module
- Themecontext Context Theme Module
- Assessment Assessmentresult Pages Module
- Package Scripts Build Module
- Run All Tests Module
- Assessmentplayer Assessment Pages Module
- Ref Vite Config Module
- Core Deps Get Module
- Core Deps Role Module
- Deployment Guide Operations Module
- Tsconfig Files References Module
- Demo Script Sih Module
- Docker Models Entry Module
- Admindashboard Ref Pages Module
- Assessmentdashboard Ref Pages Module
- Assessmentplayer Ref Pages Module
- Assessmentresult Ref Pages Module
- Certificatecenter Ref Pages Module
- Competencyinsights Ref Pages Module
- Departmentanalytics Ref Pages Module
- Documentstudio Ref Pages Module
- Forgotpassword Ref Pages Module
- Learningpath Ref Pages Module
- Login Ref Pages Module
- Overviewpage Checkhealth Module
- Profile Ref Pages Module
- Recommendationdashboard Ref Pages Module
- Register Ref Pages Module
- Unauthorized Ref Pages Module
- Project Status Readiness Module
- Run Entry Module
- Data Docs Flow Module
- Docs Sequence Diagrams Module
- Docs Prompt Library Module
- Docs Prd Product Module
- Sdg Docs And Module
- Pkg Karmayogi Backend Module

## God Nodes (most connected - your core abstractions)
1. `react` - 52 edges
2. `lucide-react` - 42 edges
3. `APIResponse` - 39 edges
4. `User` - 29 edges
5. `FRACCompetency` - 28 edges
6. `UserRepository` - 28 edges
7. `RecommendationService` - 26 edges
8. `AssessmentRepository` - 25 edges
9. `AssessmentService` - 24 edges
10. `Base` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Officer Capacity Building User Journey` --implements--> `LearningPathService`  [INFERRED]
  docs/User_Journey.md → backend/services/learning_path_service.py
- `Civil Services Role Archetypes & Personas` --conceptually_related_to--> `UserService`  [INFERRED]
  docs/User_Personas.md → backend/services/user_service.py
- `Automated Item Generation (AIG) Bloom Taxonomy Engine` --implements--> `MCQService`  [EXTRACTED]
  docs/05_MCQ_Generation_Engine.md → backend/ai/mcq_service.py
- `Automated PDF Ingestion & Sovereign Parsing Pipeline` --implements--> `PDFService`  [EXTRACTED]
  docs/03_PDF_Processing_Pipeline.md → backend/ai/pdf_service.py
- `Sovereign RAG Architecture & Local LLM Specification` --implements--> `RAGService`  [EXTRACTED]
  docs/04_RAG_Architecture.md → backend/ai/rag_service.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Core Cognitive AI Engines Trio** — docs_01_competency_gap_engine_gap_engine, docs_02_recommendation_engine_rec_engine, docs_05_mcq_generation_engine_aig_engine [EXTRACTED 0.95]

## Communities (96 total, 38 thin omitted)

### Community 0 - "Diagnostic Assessment Engine"
Cohesion: 0.06
Nodes (48): app_schemas_assessment, app_services_assessment_service, finalize_assessment(), get_assessment_history(), get_assessment_result(), pymongo, get, post (+40 more)

### Community 1 - "Course Catalog & Repositories"
Cohesion: 0.06
Nodes (30): seed_courses(), Course, Recommendation, CourseRepository, pymongo, UUID, pymongo, UUID (+22 more)

### Community 2 - "Frontend TypeScript Types"
Cohesion: 0.04
Nodes (47): AdminDashboardData, AnswerSubmitResult, AssessmentHistoryItemData, AssessmentQuestion, AssessmentQuestionOption, AssessmentResultData, AuthState, BloomLevel (+39 more)

### Community 3 - "Verifiable Certificate Management"
Cohesion: 0.08
Nodes (36): generate_certificate(), get_certificate(), list_certificates(), pymongo, get, post, Retrieves certificates: - Learners retrieve their personal verifiable…, Publicly verifiable certificate lookup by UUID or certificate number. (+28 more)

### Community 4 - "Notification Center & Alerts"
Cohesion: 0.07
Nodes (19): NotificationRepository, Any, pymongo, Marks a single notification as read., Marks all notifications for a user as read., Manages notifications, read states, priority filtering and broadcast dispatches., Dispatches a new notification to a user., Fetches notifications for a user, calculates unread counts, and returns list. (+11 more)

### Community 5 - "Frontend Root App & Navigation"
Cohesion: 0.08
Nodes (19): App(), DemoModeModalProps, LanguageOption, LanguageSelectorProps, SUPPORTED_LANGUAGES, ProtectedRouteProps, CommandItem, CommandPaletteProps (+11 more)

### Community 6 - "Adaptive Learning Pathways"
Cohesion: 0.11
Nodes (33): app_repositories_course_repository, app_schemas_recommendation, app_services_learning_path_service, app_services_recommendation_service, complete_course(), complete_learning_path_course(), get_course_details(), get_learning_path() (+25 more)

### Community 7 - "Cadre Analytics & Reporting"
Cohesion: 0.10
Nodes (19): AnalyticsRepository, Any, pymongo, Calculates macro-level KPIs from the live database with canonical baseline…, Provides high-performance aggregation queries for executive leadership and…, Returns 6-month historical trajectory of learning and assessment adoptions., Returns department comparison list, ranked by average competency., Generates cross-pillar matrix heatmap data for 12 departments. (+11 more)

### Community 8 - "Database Engine & Connection Pool"
Cohesion: 0.18
Nodes (21): app_core_database, asyncio, Base, main(), pymongo, Deterministically populates departments, officers, assessments, and…, seed_analytics_data(), seed_assessment() (+13 more)

### Community 9 - "Authentication & Session Security"
Cohesion: 0.15
Nodes (24): app_schemas_common, get_current_user(), login(), logout(), pymongo, get, post, Acknowledge client logout and signal token discard. (+16 more)

### Community 10 - "Department & Cadre Hierarchy"
Cohesion: 0.13
Nodes (8): Department, DepartmentRepository, pymongo, UUID, pymongo, UUID, UserRepository, pymongo

### Community 11 - "JWT Cryptography & Security"
Cohesion: 0.14
Nodes (21): app_core_security_guard, create_access_token(), create_refresh_token(), decode_access_token(), decode_refresh_token(), Any, Decodes and validates a refresh token., Verifies a plain password against the stored bcrypt hash. (+13 more)

### Community 12 - "FRAC Competency Taxonomy"
Cohesion: 0.18
Nodes (11): app_models_entities, FRACCompetency, CompetencyRepository, pymongo, UUID, datetime, utcnow(), CompetencyService (+3 more)

### Community 13 - "Administrative KPI & UI Components"
Cohesion: 0.14
Nodes (16): KPICardProps, CourseCard(), CourseCardProps, RecommendationReason(), RecommendationReasonProps, SkillForecast(), SkillForecastProps, WeeklyTimeline() (+8 more)

### Community 14 - "Admin Analytics Endpoints"
Cohesion: 0.13
Nodes (21): app_core_deps, app_schemas_analytics, get_admin_dashboard(), get_admin_trends(), get_competency_intelligence(), get_department_analytics(), pymongo, get (+13 more)

### Community 15 - "PyMuPDF Document Ingestion Pipeline"
Cohesion: 0.17
Nodes (13): app_core_security, app_repositories_user_repository, app_schemas_auth, app_services_auth_service, get_password_hash(), Computes a secure bcrypt hash for a password., UserProfileResponse, AuthService (+5 more)

### Community 16 - "Item Response Theory Scoring Engine"
Cohesion: 0.15
Nodes (21): delete_document(), get_document(), list_documents(), publish_mcqs(), pymongo, get, post, put (+13 more)

### Community 17 - "Ollama RAG & Vector Retrieval"
Cohesion: 0.14
Nodes (14): CertificateRepository, Any, pymongo, Retrieves a single certificate by ID or certificate number., Manages official certificate issuance, retrieval, and verification lookups., Creates and stores a new certificate with unique verification keys., Lists certificates from DB with memory fallback., CertificateService (+6 more)

### Community 18 - "Automated Item MCQ Generation"
Cohesion: 0.10
Nodes (5): ref_components_demo_demomodemodal, ref_components_layout_navbar, ref_components_layout_protectedroute, ref_components_navigation_commandpalette, ref_components_ui_skeleton

### Community 19 - "UI Design System & Primitives"
Cohesion: 0.10
Nodes (10): DocumentViewer(), DocumentViewerProps, SummaryPanelProps, AuthContext, AuthContextType, DEMO_PERSONAS, ref_components_admin_departmentheatmap, ref_components_certificates_certificatecard (+2 more)

### Community 20 - "Trainer Studio & Document Parsing"
Cohesion: 0.23
Nodes (18): app_schemas_document, CitationItem, Config, DocumentChunkItem, DocumentResponse, DocumentSummaryResponse, FAQItem, ImportantClause (+10 more)

### Community 21 - "System Architecture & Documentation"
Cohesion: 0.15
Nodes (11): DocumentChunk, Embedding, ChunkRepository, Any, pymongo, UUID, Retrieves Top-K most semantically similar chunks using Cosine Distance., hashlib (+3 more)

### Community 22 - "Theme & Indicator Context"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleDetection (+11 more)

### Community 23 - "Radar & Performance Charting"
Cohesion: 0.12
Nodes (4): alembic, pymongo, pymongo, pymongo

### Community 24 - "Mission Karmayogi PRD & Vision"
Cohesion: 0.12
Nodes (10): UploadFile, Sovereign defense heuristics for input sanitization and threat prevention., Escapes HTML characters, removes non-printable control characters, and…, Scans queries and RAG input against known prompt injection and jailbreak…, Validates query length, checks for adversarial injection, and returns sanitized…, Performs strict verification of uploaded government PDFs: 1. Checks filename…, SecurityGuard, TestAuthAndSecurity (+2 more)

### Community 25 - "Assessment Repositories Repository Module"
Cohesion: 0.23
Nodes (5): Question, QuizAttempt, AssessmentRepository, pymongo, UUID

### Community 26 - "Ref Package React Module"
Cohesion: 0.11
Nodes (18): name, private, type, version, autoprefixer, clsx, framer-motion, @hookform/resolvers (+10 more)

### Community 27 - "Components Documents Certificates Module"
Cohesion: 0.11
Nodes (9): CertificateCardProps, CertificateModalProps, DOCUMENT_TYPES, MINISTRIES, PDFUploadProps, ChatMessage, RAGChatProps, NotificationCenterProps (+1 more)

### Community 28 - "Pdf Test Service Module"
Cohesion: 0.18
Nodes (14): PDFService, Any, Extracts sovereign administrative metadata from document headers and content., Parses PDF using PyMuPDF, extracts text with breadcrumb references, and…, create_sample_government_pdf(), main(), Creates a valid synthetic government Office Memorandum PDF using PyMuPDF., test_fastapi_document_endpoints() (+6 more)

### Community 29 - "Components Assessment Pages Module"
Cohesion: 0.14
Nodes (6): CompetencyHeatmapProps, GapSummaryCardProps, ScenarioQuestionProps, ref_components_ui_card, ref_components_ui_input, ref_components_ui_label

### Community 30 - "Repositories Repository Analytics Module"
Cohesion: 0.30
Nodes (7): datetime, fastapi_security, pathlib, pymongo, pymongo, typing, uuid

### Community 31 - "Admin Components Trendchart Module"
Cohesion: 0.14
Nodes (7): DepartmentHeatmapProps, TrendChartProps, RadarChartCardProps, ref_components_admin_kpicard, ref_components_admin_trendchart, recharts, ref_types

### Community 32 - "Components Card Button Module"
Cohesion: 0.12
Nodes (13): Button, ButtonProps, Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle (+5 more)

### Community 33 - "Api Endpoints Users Module"
Cohesion: 0.18
Nodes (14): app_schemas_user, app_services_user_service, change_my_password(), get_my_profile(), pymongo, get, put, Fetch the complete profile of the currently authenticated civil servant. (+6 more)

### Community 34 - "Package Dependencies React Module"
Cohesion: 0.15
Nodes (13): dependencies, clsx, framer-motion, @hookform/resolvers, lucide-react, react, react-dom, react-hook-form (+5 more)

### Community 35 - "Tsconfig Node Compileroptions Module"
Cohesion: 0.15
Nodes (12): compilerOptions, allowImportingTsExtensions, isolatedModules, lib, module, moduleDetection, moduleResolution, noEmit (+4 more)

### Community 36 - "Embedding Service Embeddingservice Module"
Cohesion: 0.24
Nodes (8): EmbeddingService, Deterministic pseudo-random projection vector generator for fallback/offline…, Generates 768-dimensional dense vector using local Ollama nomic-embed-text.…, Batch processes text strings into 768-dimensional embeddings., Computes cosine similarity between two normalized vectors: Cosine = (A . B) /…, query_rag(), Executes grounded semantic vector search with statutory citations., test_embeddings()

### Community 37 - "Schemas Common Core Module"
Cohesion: 0.21
Nodes (10): Settings, ErrorDetail, ErrorPayload, ErrorResponse, PaginationParams, BaseModel, Standard RFC 7807 compliant error envelope., BaseSettings (+2 more)

### Community 38 - "Document Repositories Repository Module"
Cohesion: 0.33
Nodes (4): Document, DocumentRepository, pymongo, UUID

### Community 39 - "Api Endpoints Admin Module"
Cohesion: 0.18
Nodes (10): app_api_v1_endpoints_admin, app_api_v1_endpoints_assessment, app_api_v1_endpoints_auth, app_api_v1_endpoints_certificates, app_api_v1_endpoints_documents, app_api_v1_endpoints_health, app_api_v1_endpoints_notifications, app_api_v1_endpoints_recommendations (+2 more)

### Community 40 - "Rag Service Ragservice Module"
Cohesion: 0.27
Nodes (8): Any, RAGService, Generates 6-part structured civil service summary from document text., Calls local Groq Qwen 3.8 27B.8 27B model with timeout handling., Assembles context from Top-K statutory chunks, calls Qwen3, and enforces…, get_document_summary(), test_rag_and_summary(), Sovereign RAG Architecture & Local LLM Specification

### Community 41 - "Main Fastapi System Module"
Cohesion: 0.20
Nodes (9): app_api_v1_router, lifespan(), Manages application startup and graceful shutdown cycles., collections, contextlib, AI Karmayogi System Architecture Specification, fastapi_exceptions, fastapi_middleware_cors (+1 more)

### Community 42 - "Alembic Env Run Module"
Cohesion: 0.27
Nodes (9): do_run_migrations(), get_url(), Return synchronous database URL for Alembic migrations., Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 43 - "Package Devdependencies Types Module"
Cohesion: 0.20
Nodes (10): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 44 - "Mcq Service Mcqservice Module"
Cohesion: 0.25
Nodes (7): MCQService, Any, Generates grounded, Bloom-classified multiple-choice questions from document…, generate_mcqs(), Generates Bloom-classified MCQs (5, 10, or 20) with citations., Automated Item Generation (AIG) Bloom Taxonomy Engine, random

### Community 45 - "Health Main Api Module"
Cohesion: 0.22
Nodes (9): check_system_health(), pymongo, get, Evaluates end-to-end service health across MongoDB Atlas (with Vector Search) and…, get, Root endpoint for quick health / discovery., Root health endpoint for container healthchecks, proxy routing, and local…, root() (+1 more)

### Community 46 - "Components Documents Questioneditor Module"
Cohesion: 0.29
Nodes (5): MCQStudioProps, BLOOM_LEVELS, DIFFICULTY_TIERS, QuestionEditor(), QuestionEditorProps

### Community 47 - "Toastcontext Context Notify Module"
Cohesion: 0.25
Nodes (4): ToastContext, ToastContextType, ToastItem, ToastType

### Community 48 - "Health Schemas Core Module"
Cohesion: 0.38
Nodes (5): app_core_config, app_schemas_health, HealthCheckResponse, BaseModel, ServiceHealth

### Community 50 - "Languagecontext Context Languagecontexttype Module"
Cohesion: 0.29
Nodes (4): LanguageContext, LanguageContextType, SupportedLanguage, TRANSLATIONS

### Community 51 - "Ref Components Documents Module"
Cohesion: 0.29
Nodes (5): ref_components_documents_documentviewer, ref_components_documents_mcqstudio, ref_components_documents_pdfupload, ref_components_documents_ragchat, ref_components_documents_summarypanel

### Community 52 - "Main Middleware Exception Module"
Cohesion: 0.33
Nodes (6): security_and_rate_limit_middleware(), validation_exception_handler(), exception_handler, middleware, Request, RequestValidationError

### Community 56 - "Themecontext Context Theme Module"
Cohesion: 0.33
Nodes (3): Theme, ThemeContext, ThemeContextType

### Community 57 - "Assessment Assessmentresult Pages Module"
Cohesion: 0.33
Nodes (4): AssessmentResult(), ref_components_assessment_competencyheatmap, ref_components_assessment_gapsummarycard, ref_components_assessment_radarchartcard

### Community 58 - "Package Scripts Build Module"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 61 - "Ref Vite Config Module"
Cohesion: 0.50
Nodes (3): ref_path, vite, @vitejs/plugin-react

### Community 62 - "Core Deps Get Module"
Cohesion: 0.67
Nodes (3): get_current_user(), pymongo, Retrieves the fully populated User entity from the database using the token…

### Community 64 - "Deployment Guide Operations Module"
Cohesion: 0.67
Nodes (3): Production Deployment & Operations Runbook, Docker Compose Multi-Container Orchestration, Docker Compose & Sovereign Infrastructure Topology

## Knowledge Gaps
- **204 isolated node(s):** `Config`, `Config`, `ai-karmayogi-backend`, `init_models.sh script`, `name` (+199 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 541 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `APIResponse` connect `Item Response Theory Scoring Engine` to `Diagnostic Assessment Engine`, `Api Endpoints Users Module`, `Embedding Service Embeddingservice Module`, `Schemas Common Core Module`, `Adaptive Learning Pathways`, `Rag Service Ragservice Module`, `Authentication & Session Security`, `Mcq Service Mcqservice Module`, `Health Main Api Module`, `Health Schemas Core Module`, `Trainer Studio & Document Parsing`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `react` connect `Administrative KPI & UI Components` to `Components Card Button Module`, `Frontend Root App & Navigation`, `Components Documents Questioneditor Module`, `Toastcontext Context Notify Module`, `Automated Item MCQ Generation`, `UI Design System & Primitives`, `Languagecontext Context Languagecontexttype Module`, `Ref Components Documents Module`, `Skeleton Components Cardskeleton Module`, `Themecontext Context Theme Module`, `Assessment Assessmentresult Pages Module`, `Ref Package React Module`, `Components Documents Certificates Module`, `Assessmentplayer Assessment Pages Module`, `Components Assessment Pages Module`, `Admin Components Trendchart Module`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `AssessmentService` connect `Diagnostic Assessment Engine` to `Database Engine & Connection Pool`, `Assessment Repositories Repository Module`, `Department & Cadre Hierarchy`, `FRAC Competency Taxonomy`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `APIResponse` (e.g. with `finalize_assessment()` and `get_assessment_history()`) actually correct?**
  _`APIResponse` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Config`, `ai-karmayogi-backend` to the rest of the system?**
  _204 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Diagnostic Assessment Engine` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._
- **Should `Course Catalog & Repositories` be split into smaller, more focused modules?**
  _Cohesion score 0.057859703020993344 - nodes in this community are weakly interconnected._

### MANUAL SYNCHRONIZATION UPDATE (2026-09-24)
The runtime architecture has been verified against MongoDB Atlas Vector Search.
Flow: documents.py -> pdf_service.py -> embedding_service.py -> chunk_repository.py -> document_chunks -> vector_index ->  -> rag_service.py
The Atlas Vector Search index ector_index is now VERIFIED. The Graphify CLI is unavailable locally, so this graph report is manually synchronized.
