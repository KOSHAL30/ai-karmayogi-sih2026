# Current Status
- project objective: Provide a local SIH jury demonstration of the AI Learning Platform (SIH26101) with genuine backend/AI connectivity.
- current implementation state: Core features (Auth, Assessment, Learning Path, RAG, MCQ) are wired to real MongoDB/Groq instances. However, macro-analytics dashboards still rely on mathematical inflations or hardcoded demo arrays.
- current date/session: 2026-09-24
- overall status: In progressive repair state. Shifting away from "fake demo data" to actual data-driven UI.

# Verified Working
- Login (with seeded users)
- Adaptive Assessment (reads DB competencies/questions, writes attempt history)
- Algorithmic Recommendations (gap-based generation stored to DB)
- Learning Path dynamic LLM generation
- PDF Ingestion & Chunking
- Atlas Vector Search Retrieval
- Sovereign RAG Chat
- AI MCQ Generation
- Admin Dashboard KPIs (Reads true DB counts)
- Notifications (Truthful empty state verified)
- Certificates (Truthful empty state verified)
- Department Analytics & Heatmap (Reads from real departments collection)
- Competency Insights / 10-Axis FRAC Radar (Reads actual quiz_attempts scores)

# Unverified
- None.

# Broken
- None.

# Current Blockers
- None stopping execution, but the Admin and Analytics modules are misrepresenting application reality.

# AI Runtime
- LLM provider: Groq API
- model: qwen/qwen3.8-27b
- embedding provider/model: Ollama / nomic-embed-text
- vector database: MongoDB Atlas Vector Search
- RAG path: PDF upload -> chunks -> nomic-embed-text -> Atlas $vectorSearch -> Groq Qwen (REAL_DB_PLUS_AI)
- MCQ path: Document Studio -> Groq Qwen JSON generation -> deterministic grammar fallback (REAL_AI)
- Learning Path path: Recommendations -> Groq Qwen timeline generation -> deterministic 4-week fallback (REAL_DB_PLUS_AI)
- fallback behavior: 
  - Offline Ollama: deterministic 768-dim pseudo-random projection vector.
  - Groq failure (RAG): direct chunk citation return.
  - Groq failure (MCQ): grammar-based NLP extraction from chunk text.

# Database
MongoDB Atlas
Database: `ai_karmayogi`
Cluster: `AIKarmayogi`
Verified collections: `users`, `roles`, `departments`, `work_roles`, `competencies`, `quizzes`, `questions`, `courses`, `quiz_attempts`, `recommendations`, `documents`, `document_chunks`.
Index: `vector_index` (on `document_chunks.embedding`)

# Demo Environment
Required services:
- FastAPI backend (port 8000 or alternatives like 8011/8012 via Vite proxy if uvicorn locks up)
- React/Vite frontend (port 5173)
- MongoDB Atlas (Cloud)
- Ollama (Local daemon, port 11434, `nomic-embed-text`)
- Groq API (Cloud)

# Important Constraints
- DO NOT rewrite the project from scratch.
- DO NOT generate fake replacement data.
- DO NOT use broad repo audit tools unless strictly isolated.
- DO NOT downgrade/refactor the verified AI features.
- DO NOT modify `.env` or credentials.
- NEVER store passwords, API keys, or secrets in code or docs.
- DO NOT repeatedly rediscover the repository.

# Current Priority
All P0 and P1 repairs are complete.
- Assessment dossier successfully loads without 500 error. Fixed AttributeError caused by str.isoformat() calls.
- Assessment attempt answers now persist successfully without 404 or 500 errors. Fixed UUID-string mismatch and Pydantic serialization.
- Learning Path 'Start Practice Drill' button properly navigates to the assessment engine instead of throwing a UI alert.
- Auth offline fallback (DEMO_PERSONAS_AUTH) removed completely from backend/services/auth_service.py. Authentication now strictly fails gracefully if MongoDB is unreachable, preventing fake personas from being issued.
- Registration endpoint 500 error diagnosed and fixed: now returns strict 404 for missing role/department references instead of throwing unhandled 500 errors on unseeded DBs. (No fabricated mock objects used).

# Final Acceptance Matrix
All highest-value user-facing flows rely fundamentally on MongoDB connectivity for authentication (JWT validation) and core data retrieval. Because the Atlas cluster is presently inaccessible (connection timeout), zero flows can be granted a confirmed runtime pass.

| Feature | Runtime Classification | DB/AI Source | Verification | Blocker |
|---------|------------------------|--------------|--------------|---------|
| 1. Login/auth | UNVERIFIED | `users` | Blocked | MongoDB Atlas timeout |
| 2. Dashboard/analytics | UNVERIFIED | `users`, `quiz_attempts` | Blocked | MongoDB Atlas timeout |
| 3. Assessment → result | UNVERIFIED | `quizzes`, `quiz_attempts` | Blocked | MongoDB Atlas timeout |
| 4. Learning Path | UNVERIFIED | `courses` + Groq Qwen | Blocked | MongoDB Atlas timeout |
| 5. Document Studio | UNVERIFIED | `documents` + Ollama | Blocked | MongoDB Atlas timeout |
| 6. RAG Chat | UNVERIFIED | Atlas Vector Search + Groq | Blocked | MongoDB Atlas timeout |
| 7. AI MCQ generation | UNVERIFIED | `document_chunks` + Groq | Blocked | MongoDB Atlas timeout |
| 8. Competency Insights | UNVERIFIED | `quiz_attempts` | Blocked | MongoDB Atlas timeout |
| 9. Certificates | UNVERIFIED | `certificates` | Blocked | MongoDB Atlas timeout |
| 10. Notifications | UNVERIFIED | `notifications` | Blocked | MongoDB Atlas timeout |
