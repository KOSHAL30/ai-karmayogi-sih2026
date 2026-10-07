# AI Karmayogi — Complete Project Status Reference

> **Last Audit**: 18 September 2026
> **Problem Statement**: SIH26101
> **Project Path**: `c:\Users\user\Desktop\Avengers\SIH2026\AI-Karmayogi`

---

## 1. Architecture Overview

- **Backend**: FastAPI (Python 3.13), SQLAlchemy 2.0 async, asyncpg, Atlas Vector Search
- **Frontend**: React 19, Vite 5, TypeScript 5.6, Tailwind CSS 3, Recharts
- **AI**: Ollama local inference (Qwen3:8b LLM, nomic-embed-text 768-dim embeddings)
- **DB**: MongoDB Atlas Vector Search (Document Collections)
- **No Redis** — deliberately excluded for MVP

---

## 2. Environment

| Item | Value |
|------|-------|
| OS | Windows |
| Python | 3.13.3 |
| Node | v24.20.0 |
| Frontend Port | http://localhost:5173 (Vite proxy → 8000) |
| Backend Port | http://localhost:8000 (uvicorn) |
| Docker | Not installed/configured on user's machine |
| MongoDB Atlas | Not running locally (demo fallback active) |

---

## 3. Demo Credentials (Locked)

| Role | Email | Password |
|------|-------|----------|
| Learner | rajesh.kumar@gov.in | Karmayogi2026! |
| Trainer | sunita.deshmukh@nic.in | Karmayogi2026! |
| Admin | priya.nair@karmayogi.gov.in | Karmayogi2026! |

---

## 4. Directory Structure

```
AI-Karmayogi/
├── .env / .env.example          # Docker container configs
├── README.md                    # Master project overview
├── DEMO_SCRIPT.md              # 5-min SIH presentation script
├── DEPLOYMENT_GUIDE.md         # Multi-tier deployment guide
├── JUDGE_QA.md                 # 25 jury Q&A defense answers
├── requirements.txt            # Root mirror of backend deps
├── docker-compose.yml          # 5-service sovereign stack
├── run.bat / run.sh            # Docker launchers
├── dev_start.bat               # Dual-server dev launcher
│
├── backend/
│   ├── requirements.txt        # 19 Python packages
│   ├── alembic.ini / alembic/  # 5 migration versions
│   ├── run_all_tests.py        # Master test runner (20 tests)
│   ├── test_*.py               # 6 test suite files (root)
│   ├── tests/                  # 4 additional test files
│   ├── app/
│   │   ├── main.py             # FastAPI app, CORS, rate limiting
│   │   ├── api/v1/router.py    # 12 router mounts
│   │   ├── api/v1/endpoints/   # 9 endpoint files (46 routes)
│   │   ├── core/               # config, database, security, deps
│   │   ├── models/entities.py  # 17 ORM entities
│   │   ├── schemas/            # 8 Pydantic schema files (50+ types)
│   │   └── db/                 # 4 seed scripts
│   ├── services/               # 10 service classes
│   ├── repositories/           # 11 repository classes
│   └── ai/                     # 4 AI service modules
│
├── frontend/
│   ├── package.json            # 11 prod + 8 dev deps
│   ├── vite.config.ts          # Proxy /api/v1 → localhost:8000
│   ├── src/
│   │   ├── App.tsx             # 17 routes, lazy-loaded
│   │   ├── context/            # Auth, Theme, Toast providers
│   │   ├── lib/                # API client, utils
│   │   ├── types/index.ts      # 50+ TypeScript interfaces
│   │   ├── pages/              # 15 page components
│   │   └── components/         # 29 UI components
│   └── dist/                   # Production build (exists)
│
├── database/
│   ├── schema.sql              # 17 tables + HNSW index
│   └── seed_data.sql           # Demo data (4 users, 4 courses, quiz)
│
├── docker/
│   ├── Dockerfile.backend/frontend
│   ├── nginx.conf
│   └── init_models.bat/.sh
│
└── docs/                       # 22 architecture specification docs
```

---

## 5. Backend Route Map (46 Endpoints)

### Auth (`/api/v1/auth`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| POST | /auth/register | register | ⚠️ HTTPException import missing |
| POST | /auth/login | login | ✅ Demo fallback works |
| POST | /auth/refresh | refresh_token | ✅ Demo fallback works |
| POST | /auth/logout | logout | ✅ |
| GET | /auth/me | get_current_user | ✅ Demo fallback works |

### Users (`/api/v1/users`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| GET | /users/me | get_my_profile | ✅ |
| PUT | /users/me | update_my_profile | ✅ |
| PUT | /users/me/password | change_my_password | ✅ |

### Assessment (`/api/v1/assessment`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| GET | /assessment/start | start_assessment | ✅ |
| POST | /assessment/answer | submit_answer | ✅ |
| POST | /assessment/submit | finalize_assessment | ✅ |
| GET | /assessment/result/{id} | get_assessment_result | ✅ |
| GET | /assessment/history | get_assessment_history | ✅ |

### Recommendations (`/api/v1/recommendations`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| GET | /recommendations | get_recommendation_dashboard | ❌ APIResponse.success() |
| GET | /recommendations/path | get_learning_path | ❌ APIResponse.success() |
| GET | /recommendations/course/{id} | get_course_details | ❌ APIResponse.success() |
| POST | /recommendations/regenerate | regenerate_recommendations | ❌ APIResponse.success() |
| POST | /recommendations/complete | complete_course | ❌ APIResponse.success() |

### Documents/RAG/MCQ (`/api/v1/documents`, `/api/v1/rag`, `/api/v1/mcq`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| POST | /documents/upload | upload_document | ❌ APIResponse.success() |
| GET | /documents | list_documents | ❌ APIResponse.success() |
| GET | /documents/{id} | get_document | ❌ APIResponse.success() |
| DELETE | /documents/{id} | delete_document | ❌ APIResponse.success() |
| GET | /documents/{id}/summary | get_document_summary | ❌ APIResponse.success() |
| POST | /documents/query (/rag/query) | query_rag | ❌ APIResponse.success() |
| POST | /documents/generate (/mcq/generate) | generate_mcqs | ❌ APIResponse.success() |
| PUT | /documents/mcq/{id} (/mcq/{id}) | update_draft_mcq | ❌ APIResponse.success() |
| POST | /documents/publish (/mcq/publish) | publish_mcqs | ❌ APIResponse.success() |

### Admin (`/api/v1/admin`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| GET | /admin/dashboard | get_admin_dashboard | ✅ |
| GET | /admin/departments | get_department_analytics | ✅ |
| GET | /admin/competencies | get_competency_intelligence | ✅ |
| GET | /admin/trends | get_admin_trends | ✅ |

### Certificates (`/api/v1/certificates`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| GET | /certificates | list_certificates | ✅ |
| GET | /certificates/{id} | get_certificate | ✅ |
| POST | /certificates/generate | generate_certificate | ✅ |

### Notifications (`/api/v1/notifications`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| GET | /notifications | list_notifications | ✅ |
| POST | /notifications/read | mark_notification_read | ✅ |
| POST | /notifications/read-all | mark_all_notifications_read | ✅ |

### Health (`/api/v1`)
| Method | Path | Function | Status |
|--------|------|----------|--------|
| GET | /health | check_system_health | ✅ |

---

## 6. Critical Bugs (Must Fix)

### 🔴 BUG 1: Missing HTTPException import in auth.py
- **File**: `backend/app/api/v1/endpoints/auth.py` line 6
- **Fix**: Add `HTTPException` to fastapi imports

### 🔴 BUG 2: APIResponse.success() does not exist
- **Files**: `documents.py` (10 calls), `recommendations.py` (5 calls)
- **Fix**: Add `.success()` classmethod to `app/schemas/common.py` APIResponse

### 🔴 BUG 3: Alembic migration chain broken
- **File**: `alembic/versions/005_analytics_certificate_notification_tables.py`
- **Fix**: Change `down_revision = '004'` → `'004_document_rag_tables'`

### 🔴 BUG 4: Missing repository methods
- `assessment_repository.py` missing `get_latest_completed_attempt()`
- Called by `recommendation_service.py:150` and `learning_path_service.py:40`

### 🔴 BUG 5: Wrong method names in recommendation_service.py
- Line 153: `self.comp_repo.get_by_work_role()` → should be `list_by_work_role()`
- Line 155: `self.comp_repo.get_all()` → should be `list_all()`

### 🔴 BUG 6: Docker build context mismatch
- `docker-compose.yml` sets `context: ./backend` but Dockerfiles reference `backend/requirements.txt`
- **Fix**: Change build context to `.` (project root)

### 🟡 BUG 7: seed_data.sql constraint violation
- `bloom_level = 'RECALL'` violates CHECK constraint (should be `'REMEMBER'`)

### 🟡 BUG 8: No .gitignore file
- `.env` with secrets will be tracked by git

### 🟡 BUG 9: Protected routes lack RBAC enforcement
- All routes in `App.tsx` use `<ProtectedRoute>` without `allowedRoles`
- Any authenticated user can access admin/trainer pages

### 🟡 BUG 10: Health endpoint route mismatch
- Actual: `/api/v1/health`, Scripts/docs reference: `/health`

---

## 7. Key Patterns

### Demo Fallback (No DB Required)
`DEMO_PERSONAS_AUTH` in `auth_service.py` provides hardcoded credentials.
Used by: `login()`, `refresh_access_token()`, `get_profile()`.
All 3 demo accounts work without MongoDB Atlas.

### Scoring Engine (2PL IRT)
`services/scoring_engine.py` implements Item Response Theory:
- `probability_2pl(theta, b, a)` — logistic model
- `estimate_theta()` — Newton-Raphson MLE
- `calculate_competency_deficits()` — multi-pillar gap analysis
- `generate_xai_rationale()` — explainable AI text

### Analytics (Hardcoded Demo Data)
`repositories/analytics_repository.py` has 12 canonical departments with hardcoded stats for SIH demo.

---

## 8. How to Run

### Dev Mode (No Docker):
```batch
cd AI-Karmayogi
dev_start.bat
```
This starts:
- Backend: `python -m uvicorn app.main:app --port 8000 --reload` (in `backend/`)
- Frontend: `npm run dev` (in `frontend/`)
- Opens browser to `http://localhost:5173`

### Run Tests:
```batch
cd AI-Karmayogi/backend
python run_all_tests.py
```
Expected: 20/20 tests pass (no DB needed)

### Build Frontend:
```batch
cd AI-Karmayogi/frontend
npm run build
```

---

## 9. Stitch Design System Reference

**Project ID**: `4462538756205177041`
**Design System**: `assets/17941009974369658982`
**Name**: Karmayogi Sovereign Design System

### Screens Generated:
| ID | Screen | Description |
|----|--------|-------------|
| a4f48164... | Sovereign Login | Split-layout, hero + auth card |
| d833b325... | Admin Dashboard | KPI tiles, trend charts, leaderboard |
| c63ebe52... | Assessment Player | Adaptive quiz with 2PL IRT |
| 2ea8c22d... | Recommendations | AI-curated courses, skill forecast |
| abe2a845... | Document Studio | 3-column RAG + MCQ workspace |
| da9d26d3... | Assessment Result | Radar chart, gap analysis, XAI |
| 5b56f5fd... | Overview/Home | Personalized welcome dashboard |
| b248b26f... | Certificate Center | Sovereign credential vault |

### Design Tokens:
- Primary: `#1e3a5f` (Deep Navy)
- Secondary: `#e8791d` (Saffron/Amber)
- Tertiary: `#138808` (Government Green)
- Headlines: Plus Jakarta Sans
- Body: Inter
- Roundness: 12px
- Style: Stripe + Linear + Government of India sovereignty
