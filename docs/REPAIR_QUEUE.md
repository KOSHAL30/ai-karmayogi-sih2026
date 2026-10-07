# AI Karmayogi — Repair Queue

## P0 (Data Integrity Blockers)
- [x] Remove mathematical KPI inflation from `analytics_repository.py` and restore true DB-backed counts.
- [x] Remove `FALLBACK_CERTIFICATES` and `FALLBACK_NOTIFICATIONS` so empty states are truthful.

## P1 (Core SIH Demo Features)
- [x] Refactor Department Analytics to aggregate the real `departments` collection.
- [x] Refactor Competency Insights to compute the 10-axis FRAC radar from actual `quiz_attempts`.
- [x] Remove `_DEMO_PERSONAS` auth fallback from `deps.py` so DB failure produces real 401 behavior.

## Current Audit Truth
- **HARDCODED_RUNTIME**: 2 (Department Analytics, Competency Insights)
- **MIXED**: 4 (Login fallback, Admin Dashboard KPIs, Certificates fallback, Notifications fallback)
- **BROKEN**: 4 (Admin Dashboard KPIs mathematical manipulation, Department Analytics bypass, Competency Insights bypass, Certificate/Notification false empty states)
- **End-to-end AI verified**: Learning Path dynamic generation, Sovereign RAG Chat, AI MCQ Generation via Groq Qwen.
- **Rule**: Do not downgrade verified AI features without new evidence.
