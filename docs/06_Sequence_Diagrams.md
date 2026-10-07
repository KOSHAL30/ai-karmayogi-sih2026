# 06_Sequence_Diagrams.md

# Sequence Architecture: AI Karmayogi

**Detailed Interaction Protocols, Asynchronous Message Flows, and Execution Lifecycles Across System Tiers**

**Document Version:** 1.0.0  
**Target Program:** Smart India Hackathon 2026  
**Problem Statement ID:** SIH26101  
**Project Name:** AI Karmayogi  
**Classification:** Enterprise Government Specification — Phase 2 Interaction Design  

---

## Table of Contents
1. [Sequence Overview & Architectural Actors](#1-sequence-overview--architectural-actors)
2. [Sequence 1: Civil Servant Authentication & SSO Session Initialization](#2-sequence-1-civil-servant-authentication--sso-session-initialization)
3. [Sequence 2: Competency Diagnostic & Adaptive Assessment Execution](#3-sequence-2-competency-diagnostic--adaptive-assessment-execution)
4. [Sequence 3: Semantic Learning Recommendation & Knowledge Graph Traversal](#4-sequence-3-semantic-learning-recommendation--knowledge-graph-traversal)
5. [Sequence 4: Document Ingestion, Autonomous AIG, and SME Review](#5-sequence-4-document-ingestion-autonomous-aig-and-sme-review)

---

## 1. Sequence Overview & Architectural Actors

This document specifies the exact runtime message sequences across five primary system tiers:
1. **User / Presentation Tier:** React 19 SPA client running in the user's browser.
2. **Reverse Proxy / Edge Gateway:** Nginx edge server handling TLS, static assets, and proxying.
3. **Application Tier:** FastAPI backend server executing business logic and orchestrating tasks.
4. **Cache & Task Queue:** Redis 7 managing session states, token blacklists, and caching.
5. **Database & Vector Store:** MongoDB Atlas Vector Search extension storing relational data and 768-dim embeddings.
6. **Local Cognitive AI Tier:** PyMuPDF engine, Ollama `nomic-embed-text` embeddings, and Ollama `Llama 3.1:8b` / `Qwen 2.5:7b` LLM.

---

## 2. Sequence 1: Civil Servant Authentication & SSO Session Initialization

This diagram details the authentication sequence, credential verification, JWT issuance, and Redis session caching.

```mermaid
sequenceDiagram
    autonumber
    actor User as Civil Servant (Learner)
    participant UI as React 19 UI
    participant Nginx as Nginx Gateway
    participant API as FastAPI Backend
    participant DB as MongoDB Atlas
    participant Redis as Redis Cache

    User->>UI: Inputs credentials (email, password)
    UI->>Nginx: POST /api/v1/auth/login
    Nginx->>API: Proxy pass request with client IP headers
    
    API->>DB: Query user by email and verify is_active
    DB-->>API: Return user record + role + work_role

    alt Invalid Credentials or Inactive
        API-->>Nginx: 401 Unauthorized (Invalid credentials)
        Nginx-->>UI: 401 Unauthorized
        UI-->>User: Display authentication error toast
    else Valid Credentials
        API->>API: Verify argon2/bcrypt password hash
        API->>API: Generate signed JWT (claims: user_id, role, department_id, exp: 8h)
        API->>Redis: Setex session key (user_id -> session_data, TTL: 28800s)
        API->>DB: UPDATE users SET last_login_at = CURRENT_TIMESTAMP
        API-->>Nginx: 200 OK (access_token, user_profile)
        Nginx-->>UI: 200 OK (access_token, user_profile)
        UI->>UI: Store JWT in secure memory (TanStack Auth Context)
        UI-->>User: Redirect to Role-Based Dashboard
    end
```

---

## 3. Sequence 2: Competency Diagnostic & Adaptive Assessment Execution

This diagram details how baseline diagnostics are retrieved, dynamically administered, submitted, scored against FRAC benchmarks, and transformed into an explainable Competency Deficit Matrix.

```mermaid
sequenceDiagram
    autonumber
    actor User as Civil Servant (Learner)
    participant UI as React 19 UI
    participant API as FastAPI Backend
    participant DB as MongoDB Atlas
    participant Redis as Redis Cache

    User->>UI: Clicks "Start Role Diagnostic"
    UI->>API: GET /api/v1/assessment/diagnostic (Bearer JWT)
    API->>API: Extract work_role_id from token claims
    API->>DB: Query mandated FRAC competencies for work_role_id
    DB-->>API: Return list of Behavioral, Functional & Domain competencies
    API->>DB: Query accredited diagnostic questions matching competency codes
    DB-->>API: Return 15 calibrated assessment items
    API-->>UI: 200 OK (JSON question payload without correct keys)
    
    UI-->>User: Render interactive scenario questions (1 by 1)
    User->>UI: Selects options and clicks "Submit Assessment"
    
    UI->>API: POST /api/v1/assessment/diagnostic/submit (payload: responses, time_taken)
    API->>DB: Fetch correct answer keys & competency mappings
    DB-->>API: Return authoritative answer keys
    API->>API: Grade answers & calculate demonstrated proficiency levels (1 to 5)
    API->>API: Compute Deficit Vector: Delta = Mandated_Level - Demonstrated_Level
    
    API->>DB: INSERT INTO quiz_attempts (score, is_passed, answer_log)
    API->>DB: INSERT / UPDATE recommendations (user_id, deficit_scores)
    API->>Redis: Invalidate cached recommendations for user_id
    
    API-->>UI: 200 OK (Competency Gap Matrix, Radar Data, Score)
    UI-->>User: Render interactive Recharts Radar & Gap Summary Card
```

---

## 4. Sequence 3: Semantic Learning Recommendation & Knowledge Graph Traversal

This sequence details how the platform evaluates diagnosed deficit vectors, queries Atlas Vector Search embeddings for semantically matched iGOT courses, and delivers explainable recommendations.

```mermaid
sequenceDiagram
    autonumber
    actor User as Civil Servant (Learner)
    participant UI as React 19 UI
    participant API as FastAPI Backend
    participant Redis as Redis Cache
    participant DB as MongoDB Atlas Vector Search
    participant Ollama as Ollama (nomic-embed-text)

    User->>UI: Navigates to "My Learning Pathways"
    UI->>API: GET /api/v1/recommendations (Bearer JWT)
    
    API->>Redis: Check cached recommendations (key: recs:{user_id})
    alt Cache Hit
        Redis-->>API: Return cached JSON recommendations
    else Cache Miss
        API->>DB: Query active competency deficits from recommendations table
        DB-->>API: Return top acute deficits (e.g., FC-PROC-001: 45% deficit)
        
        API->>Ollama: POST /api/embeddings (prompt: "Training course for Public Procurement GFR 166 single tender")
        Ollama-->>API: Return 768-dim query embedding vector
        
        API->>DB: Execute Cosine Vector Search on course embeddings (<=> operator)
        DB-->>API: Return Top-3 semantically closest iGOT micro-courses
        
        API->>API: Synthesize explainable administrative justification for each item
        API->>Redis: Setex recommendations (TTL: 1800s)
    end

    API-->>UI: 200 OK (List of recommended courses with explainable rationales)
    UI-->>User: Render course cards with "Why Recommended" callouts and direct launch buttons
```

---

## 5. Sequence 4: Document Ingestion, Autonomous AIG, and SME Review

This sequence illustrates the end-to-end authoring lifecycle: uploading a government PDF, parsing via PyMuPDF, generating embeddings with `nomic-embed-text`, synthesizing scenario MCQs with Ollama `Llama 3.1`, and conducting Human-in-the-Loop (HITL) SME verification.

```mermaid
sequenceDiagram
    autonumber
    actor SME as Subject Matter Expert / Trainer
    participant UI as React 19 UI
    participant API as FastAPI Backend
    participant Fitz as PyMuPDF (fitz)
    participant DB as MongoDB Atlas Vector Search
    participant Embed as Ollama (nomic-embed-text)
    participant LLM as Ollama (Llama 3.1 / Qwen 2.5)

    SME->>UI: Uploads official government circular PDF (e.g., GFR Amendment OM)
    UI->>API: POST /api/v1/documents/upload (multipart/form-data)
    
    API->>DB: INSERT INTO documents (status: 'PROCESSING')
    DB-->>API: Return document_id
    API-->>UI: 202 Accepted (document_id, status: 'PROCESSING')
    
    Note over API,Fitz: Asynchronous Extraction & Chunking
    API->>Fitz: Parse PDF binary stream
    Fitz-->>API: Return extracted text blocks + page numbers
    API->>API: Execute Statutory Recursive Chunker (512 tokens, 64 overlap)
    API->>DB: Bulk INSERT INTO document_chunks
    
    Note over API,Embed: Local Vector Embedding
    loop For each chunk
        API->>Embed: POST /api/embeddings (chunk_content)
        Embed-->>API: 768-dim float vector
        API->>DB: INSERT INTO embeddings (chunk_id, vector)
    end
    API->>DB: UPDATE documents SET status = 'EMBEDDED'
    
    Note over SME,LLM: Autonomous Item Generation (AIG)
    SME->>UI: Requests "Generate 20-Question Quiz (Bloom Levels 2-4)"
    UI->>API: POST /api/v1/quizzes/generate (document_id, bloom_specs)
    API->>DB: Fetch top relevant document chunks
    DB-->>API: Return statutory chunks
    
    API->>LLM: POST /api/generate (System Prompt + Legal Chunks + Pydantic Schema)
    LLM-->>API: Return JSON with Stem, 1 Key, 3 Distractors & Citations
    API->>API: Validate schema via Pydantic validator
    API->>DB: INSERT INTO quizzes & questions (status: 'SME_REVIEW')
    API-->>UI: 201 Created (quiz_id, status: 'SME_REVIEW')
    
    Note over SME,UI: Human-in-the-Loop (HITL) Curation
    UI->>API: GET /api/v1/quizzes/{quiz_id}/curation
    API-->>UI: Return all 20 generated items with rationales
    UI-->>SME: Render Side-by-Side Verification Studio
    SME->>UI: Modifies Distractor B on Question 4 and clicks "Approve & Publish"
    UI->>API: PUT /api/v1/quizzes/questions/{question_id} (updated item)
    API->>DB: UPDATE questions & SET quiz status = 'PUBLISHED'
    API-->>UI: 200 OK (Published to Live iGOT Bank)
    UI-->>SME: Display success modal ("20 Accredited Items Live")
```

---
*End of Sequence Diagrams*
