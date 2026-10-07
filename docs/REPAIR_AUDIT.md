# AI Karmayogi — Runtime Truth Audit

## 1. Executive Finding
The application is a **MIXTURE** of authentic, data-driven systems and hardcoded presentation layers. The core workflows—Authentication, Adaptive Assessments, Algorithmic Recommendations, and Sovereign AI (RAG, Learning Paths, MCQs)—are genuinely connected to the MongoDB Atlas backend and Groq Qwen API, operating dynamically on real user interactions. However, the macro-level Admin and Analytics dashboards heavily rely on static, hardcoded arrays and mathematical baseline inflations designed to simulate a massive enterprise deployment for demo purposes, obscuring the actual database truth.

## 2. Feature Runtime Matrix

| Feature | UI | API | Service | Repository | DB | AI | Runtime Classification | Working? |
|---------|----|-----|---------|------------|----|----|------------------------|----------|
| Login / auth | `Login.tsx` | `POST /auth/login` | `AuthService` | `UserRepository` | Yes | No | MIXED (Auth fallback) | Yes |
| Learner dashboard | `OverviewPage.tsx` | JWT State | `AuthService` | `UserRepository` | Yes | No | REAL_DB | Yes |
| Profile | `Profile.tsx` | `GET /auth/me` | `UserService` | `UserRepository` | Yes | No | REAL_DB | Yes |
| Assessment dashboard | `AssessmentDashboard.tsx`| `GET /assessment/history`| `AssessmentService`| `AssessmentRepository`| Yes | No | REAL_DB | Yes |
| Assessment player | `AssessmentPlayer.tsx`| `GET /assessment/start`| `AssessmentService`| `Assessment/Competency`| Yes | No | REAL_DB | Yes |
| Assessment result | `AssessmentResult.tsx`| `POST /assessment/submit`| `AssessmentService`| `AssessmentRepository`| Yes | No | REAL_DB | Yes |
| Recommendations | `RecommendationDashboard`| `GET /recommendations`| `RecommendationService`| `RecommendationRepository`| Yes | No | REAL_DB | Yes |
| Learning Path | `LearningPath.tsx`| `GET /recommendations/path`| `LearningPathService`| `RecommendationRepository`| Yes | Yes | REAL_DB_PLUS_AI | Yes |
| Trainer Document Studio| `DocumentStudio.tsx`| `GET /documents` | `DocumentService`| `DocumentRepository` | Yes | No | REAL_DB | Yes |
| PDF upload | `DocumentStudio.tsx`| `POST /documents/upload`| `PDFService/Embed`| `Document/ChunkRepo` | Yes | Yes | REAL_DB_PLUS_AI | Yes |
| Document viewer | `DocumentViewer.tsx`| `GET /documents/{id}`| `DocumentService`| `DocumentRepository` | Yes | No | REAL_DB | Yes |
| RAG chat | `RAGChat.tsx` | `POST /rag/query` | `RAGService` | `ChunkRepository` | Yes | Yes | REAL_DB_PLUS_AI | Yes |
| AI MCQ generation | `DocumentStudio.tsx`| `POST /mcq/generate`| `MCQService` | `ChunkRepository` | Yes | Yes | REAL_AI | Yes |
| Certificates | `CertificateCenter.tsx`| `GET /certificates` | `CertificateService`| `CertificateRepository`| Yes | No | MIXED (Fallback) | Yes |
| Notifications | `Navbar.tsx` | `GET /notifications`| `NotificationService`| `NotificationRepository`| Yes | No | MIXED (Fallback) | Yes |
| Admin dashboard | `AdminDashboard.tsx`| `GET /admin/dashboard`| `AnalyticsService` | `AnalyticsRepository` | Yes | No | MIXED (Inflated) | Yes |
| Competency insights | `CompetencyInsights.tsx`| `GET /admin/competencies`| `AnalyticsService` | `AnalyticsRepository` | No | No | HARDCODED_RUNTIME | Yes |
| Department analytics | `DepartmentAnalytics.tsx`| `GET /admin/departments`| `AnalyticsService` | `AnalyticsRepository` | No | No | HARDCODED_RUNTIME | Yes |

## 3. Hardcoded Runtime Data

| File | Data | Why It Is Fake/Static | Runtime Reachable? | Replacement |
|------|------|-----------------------|--------------------|-------------|
| `analytics_repository.py` | `CANONICAL_DEPARTMENTS` array | Simulates 12 government departments with fake aggregate stats | Yes | Query `learning_progress` mapped to `departments` collection |
| `analytics_repository.py` | 10-axis FRAC radar array | Invented competency levels | Yes | Aggregate actual `demonstrated_level` from `quiz_attempts` |
| `analytics_repository.py` | Top Critical Competencies | Invented deficit percentages | Yes | DB aggregation on competency gaps |
| `analytics_repository.py` | Monthly Trends array | Hardcoded 6-month historical activity | Yes | Group `created_at` records by month |
| `certificate_repository.py` | `FALLBACK_CERTIFICATES` | Injected when DB has 0 certs | Yes | Return empty array `[]` |
| `notification_repository.py`| `FALLBACK_NOTIFICATIONS`| Injected when DB has 0 notifications | Yes | Return empty array `[]` |
| `deps.py` | `_DEMO_PERSONAS` | Fast-tracks auth if DB fails | Yes | Return 401 Unauthorized |

## 4. Demo/Fallback Systems

| System | Trigger | Runtime Reachable | User Visible | Risk | Action |
|--------|---------|-------------------|--------------|------|--------|
| `DemoModeModal.tsx` | Ctrl+Shift+D | Yes | Only if triggered | Very Low (Executes real `POST /login` with seeded credentials; no bypass) | Retain |
| Embedding Fallback | Ollama offline | Yes | No | Low (Generates deterministic vectors allowing pipeline to proceed without crashing) | Retain |
| RAG Deterministic Fallback | Groq API failure | Yes | Yes | Medium (Swaps generated answer with direct chunk citation) | Retain |
| MCQ Deterministic Fallback | Groq API failure | Yes | Yes | Medium (Swaps generated MCQs with NLP grammar extracted questions) | Retain |
| Admin KPI Inflation | Executive Dashboard Load | Yes | Yes | High (Misrepresents actual DB records using `max(300, ...)` to simulate enterprise scale) | Remove |

## 5. AI Runtime Verification

| AI Feature | UI Trigger | Endpoint | LLMProvider | Provider | Fresh AI Request? | Output Used by UI? |
|------------|------------|----------|-------------|----------|-------------------|--------------------|
| Learning Path | Click "Generate Path" | `/recommendations/path` | Yes | Groq Qwen | Yes | Yes, JSON parsed into timeline |
| RAG Chat | Send message in Studio | `/rag/query` | Yes | Groq Qwen | Yes | Yes, answer rendered with citations |
| MCQ Gen | Click "Generate MCQs" | `/mcq/generate` | Yes | Groq Qwen | Yes | Yes, JSON parsed into options |

## 6. Database Runtime Verification

| Entity | Collection | Repository | API | UI | Real Data? |
|--------|------------|------------|-----|----|------------|
| User | `users` | `UserRepository` | `auth.py` | `Profile.tsx` | Yes |
| Department | `departments` | `DepartmentRepository` | Indirect | `AdminDashboard.tsx` | No (Bypassed by hardcoded `CANONICAL_DEPARTMENTS`) |
| Competency | `competencies` | `CompetencyRepository` | `assessment.py` | `AssessmentPlayer.tsx`| Yes |
| Quiz | `quizzes` | `AssessmentRepository` | `assessment.py` | `AssessmentPlayer.tsx`| Yes |
| Attempt | `quiz_attempts` | `AssessmentRepository` | `assessment.py` | `AssessmentDashboard` | Yes |
| Course | `courses` | `CourseRepository` | `recommendations.py`| `LearningPath.tsx` | Yes |
| Recommendation | `recommendations` | `RecommendationRepository`| `recommendations.py`| `RecommendationDashboard`| Yes (Saved algorithmic output) |
| Document | `documents` | `DocumentRepository` | `documents.py` | `DocumentStudio.tsx` | Yes |
| Chunk | `document_chunks` | `ChunkRepository` | `documents.py` | RAG retrieval | Yes |

## 7. Broken Feature Chains

1. **Admin Dashboard KPIs**: Fetches actual database counts but obscures them with math modifiers (e.g., `total_officers = max(300, db_total_users)`).
2. **Department Analytics**: Bypasses the `DepartmentRepository` entirely and serves a hardcoded literal array.
3. **Competency Insights**: Bypasses user assessment histories and serves a hardcoded 10-axis radar array.
4. **Certificate & Notification Repositories**: Return hardcoded fake arrays if the database naturally yields zero results, preventing true empty-state rendering in the UI.

## 8. Repair Priority

*   **P0 (Data Integrity Blocker)**: Remove Admin KPI Baseline math inflations in `analytics_repository.py`.
*   **P0 (Data Integrity Blocker)**: Remove `FALLBACK_CERTIFICATES` and `FALLBACK_NOTIFICATIONS`.
*   **P1 (Core SIH Demo Feature)**: Refactor `analytics_repository.py` to source Department Analytics and Competency Insights from actual DB aggregations.
*   **P2 (Secondary Feature)**: Remove `_DEMO_PERSONAS` fast-track bypass in `deps.py`.
*   **P3 (Cosmetic)**: N/A.

## 9. First Repair Batch

The smallest coherent batch of files to change first to restore structural truth:
1. `backend/repositories/analytics_repository.py`
2. `backend/repositories/certificate_repository.py`
3. `backend/repositories/notification_repository.py`
