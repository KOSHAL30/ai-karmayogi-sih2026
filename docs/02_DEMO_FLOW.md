# AI Karmayogi — Intended SIH Jury Demo Sequence

## Step 1: Authentication
1. **UI action**: Navigate to `/login`, enter seeded credentials (e.g., Rajesh Kumar), and click Login. Alternatively, use the `DemoModeModal` (Ctrl+Shift+D) to switch personas.
2. **API endpoint**: `POST /auth/login`
3. **Backend service**: `AuthService.login`
4. **DB/AI dependency**: Queries `users` collection in MongoDB.
5. **Expected visible result**: Redirection to the authenticated Learner Dashboard (`OverviewPage`).
6. **Verification status**: PASS

## Step 2: Diagnostic Assessment
1. **UI action**: Click "Start Diagnostic Assessment". Answer dynamic questions.
2. **API endpoint**: `GET /assessment/start` followed by `POST /assessment/submit`.
3. **Backend service**: `AssessmentService.start_assessment`
4. **DB/AI dependency**: Queries `competencies` and `questions` from MongoDB based on user role. Saves `quiz_attempts`.
5. **Expected visible result**: Adaptive assessment player, followed by a scored results screen showing competencies mapped.
6. **Verification status**: PASS

## Step 3: Personalized Learning Path
1. **UI action**: Navigate to Learning Path (`/learning-path`), click "Generate Custom Path".
2. **API endpoint**: `GET /recommendations/path`
3. **Backend service**: `LearningPathService.generate_path`
4. **DB/AI dependency**: Fetches gap recommendations from DB, then calls Groq Qwen via `LLMProvider` to generate a 4-week structured JSON timeline.
5. **Expected visible result**: A 4-week chronological timeline of recommended courses and milestones rendered in the UI.
6. **Verification status**: PASS

## Step 4: Trainer Document Studio (RAG Ingestion)
1. **UI action**: Switch to Trainer persona. Navigate to Trainer Studio (`/trainer/documents`). Upload a PDF (e.g., `sample_gfr_om.pdf`).
2. **API endpoint**: `POST /documents/upload`
3. **Backend service**: `DocumentService.process_document` -> `EmbeddingService` -> `ChunkRepository`
4. **DB/AI dependency**: PyMuPDF extracts text, `nomic-embed-text` generates embeddings, saved to `document_chunks` in MongoDB.
5. **Expected visible result**: Document appears in the studio list, indicating successful ingestion and chunking.
6. **Verification status**: PASS

## Step 5: Document Q&A (Sovereign RAG)
1. **UI action**: Click on the ingested document. Enter a question in the RAG Chat widget (e.g., "What are the rules for procurement?").
2. **API endpoint**: `POST /rag/query`
3. **Backend service**: `RAGService.answer_query`
4. **DB/AI dependency**: Atlas `$vectorSearch` retrieves relevant chunks; Groq Qwen synthesizes a grounded answer.
5. **Expected visible result**: An AI-generated answer with explicit, clickable source citations (Rule, Chapter, Page).
6. **Verification status**: PASS

## Step 6: AI MCQ Generation
1. **UI action**: In the Document Viewer, click "Generate MCQs".
2. **API endpoint**: `POST /mcq/generate`
3. **Backend service**: `MCQService.generate_mcqs_ai`
4. **DB/AI dependency**: Groq Qwen generates a JSON array of questions based strictly on the document chunks.
5. **Expected visible result**: A list of generated multiple-choice questions with options and pedagogical explanations.
6. **Verification status**: PASS

## Step 7: Executive Dashboard (Pending Repair)
1. **UI action**: Switch to Admin persona. Navigate to `/admin`.
2. **API endpoint**: `GET /admin/dashboard`
3. **Backend service**: `AnalyticsService`
4. **DB/AI dependency**: *Currently queries DB but inflates numbers artificially.*
5. **Expected visible result**: High-level KPIs, 12-department heatmap, and competency radar.
6. **Verification status**: FAIL (Data integrity compromised by hardcoded demo structures).
