# 02_ER_Diagram.md

# Entity-Relationship (ER) Architecture: AI Karmayogi

**Complete Relational Model, Cardinality Mappings, Foreign Key Schematics, and Mermaid ERD for Mission Karmayogi**

**Document Version:** 1.0.0  
**Target Program:** Smart India Hackathon 2026  
**Problem Statement ID:** SIH26101  
**Project Name:** AI Karmayogi  
**Classification:** Enterprise Government Specification — Phase 2 Data Architecture  

---

## Table of Contents
1. [Data Architecture Overview](#1-data-architecture-overview)
2. [Complete Entity-Relationship Diagram (Mermaid)](#2-complete-entity-relationship-diagram-mermaid)
3. [Entity Descriptions & Domain Boundaries](#3-entity-descriptions--domain-boundaries)
4. [Cardinality & Relationship Matrix](#4-cardinality--relationship-matrix)
5. [Integrity Constraints & Indexing Strategy](#5-integrity-constraints--indexing-strategy)

---

## 1. Data Architecture Overview

The **AI Karmayogi** data layer is structured around an ACID-compliant MongoDB Atlas relational database extended with the **Atlas Vector Search** module. The schema is normalized (3NF) to guarantee transactional consistency while supporting high-throughput vector similarity lookups.

All primary keys use universally unique identifiers (**UUID v4**) to allow distributed key generation, prevent sequential key enumeration attacks, and ensure seamless synchronization across future federal state nodes.

The data model is partitioned into four logical clusters:
1. **Administrative & Identity Cluster:** `roles`, `departments`, `work_roles`, `users`.
2. **Competency & Learning Cluster:** `frac_competencies`, `courses`, `recommendations`, `learning_progress`, `certificates`.
3. **Cognitive AI & Document Cluster:** `documents`, `document_chunks`, `embeddings`.
4. **Pedagogical Assessment & Governance Cluster:** `quizzes`, `questions`, `quiz_attempts`, `notifications`, `audit_logs`.

---

## 2. Complete Entity-Relationship Diagram (Mermaid)

```mermaid
erDiagram
    ROLES ||--o{ USERS : "assigned_to"
    DEPARTMENTS ||--o{ USERS : "employs"
    DEPARTMENTS ||--o{ WORK_ROLES : "defines"
    WORK_ROLES ||--o{ USERS : "designates"
    WORK_ROLES ||--o{ FRAC_COMPETENCIES : "mandates"
    
    FRAC_COMPETENCIES ||--o{ COURSES : "addressed_by"
    FRAC_COMPETENCIES ||--o{ QUESTIONS : "evaluates"
    FRAC_COMPETENCIES ||--o{ RECOMMENDATIONS : "targets_deficit"
    
    USERS ||--o{ DOCUMENTS : "uploads"
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : "partitioned_into"
    DOCUMENT_CHUNKS ||--|| EMBEDDINGS : "vectorized_as"
    
    DOCUMENTS ||--o{ QUIZZES : "sources"
    QUIZZES ||--o{ QUESTIONS : "contains"
    
    USERS ||--o{ QUIZ_ATTEMPTS : "undertakes"
    QUIZZES ||--o{ QUIZ_ATTEMPTS : "evaluated_in"
    
    USERS ||--o{ RECOMMENDATIONS : "receives"
    COURSES ||--o{ RECOMMENDATIONS : "suggested_course"
    
    USERS ||--o{ LEARNING_PROGRESS : "tracks"
    COURSES ||--o{ LEARNING_PROGRESS : "monitored_in"
    
    USERS ||--o{ CERTIFICATES : "awarded_to"
    COURSES ||--o{ CERTIFICATES : "accredits"
    
    USERS ||--o{ NOTIFICATIONS : "notified_via"
    USERS ||--o{ AUDIT_LOGS : "acted_by"

    ROLES {
        uuid id PK
        string role_code UK
        string role_name
        string description
        timestamp created_at
    }

    DEPARTMENTS {
        uuid id PK
        string department_code UK
        string name
        string ministry_name
        string tier
        timestamp created_at
    }

    WORK_ROLES {
        uuid id PK
        uuid department_id FK
        string role_title
        string role_code UK
        string description
        timestamp created_at
    }

    FRAC_COMPETENCIES {
        uuid id PK
        uuid work_role_id FK
        string competency_type
        string competency_name
        string competency_code UK
        int mandated_level
        text description
        timestamp created_at
    }

    USERS {
        uuid id PK
        uuid role_id FK
        uuid department_id FK
        uuid work_role_id FK
        string government_id_hash UK
        string email UK
        string password_hash
        string full_name
        string designation
        boolean is_active
        timestamp created_at
    }

    COURSES {
        uuid id PK
        uuid competency_id FK
        string igot_course_id UK
        string title
        text description
        string duration_minutes
        int target_level
        string course_url
        timestamp created_at
    }

    DOCUMENTS {
        uuid id PK
        uuid uploaded_by FK
        string document_title
        string document_type
        string file_path
        int file_size_bytes
        string file_hash
        string processing_status
        timestamp created_at
    }

    DOCUMENT_CHUNKS {
        uuid id PK
        uuid document_id FK
        int chunk_index
        text chunk_content
        int token_count
        string section_reference
        timestamp created_at
    }

    EMBEDDINGS {
        uuid id PK
        uuid chunk_id FK
        vector embedding_vector_768
        string model_version
        timestamp created_at
    }

    QUIZZES {
        uuid id PK
        uuid document_id FK
        uuid created_by FK
        string title
        string quiz_type
        int passing_percentage
        string status
        timestamp created_at
    }

    QUESTIONS {
        uuid id PK
        uuid quiz_id FK
        uuid competency_id FK
        text question_stem
        string bloom_level
        jsonb options
        int correct_option_index
        text pedagogical_rationale
        string source_citation
        timestamp created_at
    }

    QUIZ_ATTEMPTS {
        uuid id PK
        uuid user_id FK
        uuid quiz_id FK
        int score_achieved
        int total_questions
        boolean is_passed
        int time_taken_seconds
        jsonb answer_log
        timestamp attempted_at
    }

    RECOMMENDATIONS {
        uuid id PK
        uuid user_id FK
        uuid course_id FK
        uuid competency_id FK
        decimal deficit_score
        text explainable_rationale
        string status
        timestamp generated_at
    }

    LEARNING_PROGRESS {
        uuid id PK
        uuid user_id FK
        uuid course_id FK
        int progress_percentage
        int time_spent_minutes
        string completion_status
        timestamp last_accessed_at
    }

    CERTIFICATES {
        uuid id PK
        uuid user_id FK
        uuid course_id FK
        string certificate_number UK
        string verification_hash UK
        timestamp issued_at
    }

    NOTIFICATIONS {
        uuid id PK
        uuid user_id FK
        string title
        text message
        string notification_type
        boolean is_read
        timestamp created_at
    }

    AUDIT_LOGS {
        uuid id PK
        uuid user_id FK
        string action_name
        string entity_name
        uuid entity_id
        string ip_address
        jsonb metadata
        timestamp created_at
    }
```

---

## 3. Entity Descriptions & Domain Boundaries

### 1. Administrative & Identity Cluster
- **ROLES:** Authoritative system access permissions (`learner`, `trainer`, `department_head`, `administrator`).
- **DEPARTMENTS:** Government administrative divisions (Central Ministries, Attached Directorates, State Departments).
- **WORK_ROLES:** Specific Work-Based Roles (WBRs) defined under Mission Karmayogi (e.g., Drawing & Disbursing Officer, Section Officer).
- **USERS:** Civil servants, trainers, administrators, and leadership personnel authenticated into the system.

### 2. Competency & Learning Cluster
- **FRAC_COMPETENCIES:** Standardized behavioral, functional, and domain capability nodes, each mapped with mandatory proficiency levels (1 to 5).
- **COURSES:** Curated courses and micro-modules available on the iGOT Karmayogi platform.
- **RECOMMENDATIONS:** Algorithmic learning pathways prescribed to close diagnosed competency gaps with explicit administrative justifications.
- **LEARNING_PROGRESS:** Granular tracking of user completion, interaction time, and module status.
- **CERTIFICATES:** Digitally verifiable micro-credentials issued upon validated competency attainment.

### 3. Cognitive AI & Document Cluster
- **DOCUMENTS:** Raw government regulatory texts, Acts, Rules, circulars, and training PDFs uploaded for processing.
- **DOCUMENT_CHUNKS:** Semantically coherent text segments preserving statutory sections, provisos, and legal sub-clauses.
- **EMBEDDINGS:** Dense 768-dimensional mathematical vector representations generated by `nomic-embed-text` for vector similarity matching in `Atlas Vector Search`.

### 4. Assessment & Governance Cluster
- **QUIZZES:** Formative assessments, baseline diagnostics, and module quizzes generated from documents.
- **QUESTIONS:** Psychometrically structured evaluation items specifying Bloom’s Taxonomy level, 4 options, distractors, and remediation citations.
- **QUIZ_ATTEMPTS:** Immutable logs of civil servant assessment submissions, response choices, and timing metrics.
- **NOTIFICATIONS:** In-app and push triggers informing users of gap closures, new circular quizzes, and course recommendations.
- **AUDIT_LOGS:** Non-repudiable audit trails recording every security, authentication, and content publication event.

---

## 4. Cardinality & Relationship Matrix

| Primary Entity (1) | Related Entity (Many) | Relationship | Cardinality | Business Rule & Governance Constraint |
| :--- | :--- | :--- | :---: | :--- |
| **ROLES** | **USERS** | Assigned To | 1 : N | Every user must possess exactly one active system role. |
| **DEPARTMENTS** | **USERS** | Employs | 1 : N | A user belongs to one administrative department or ministry. |
| **DEPARTMENTS** | **WORK_ROLES** | Defines | 1 : N | A department establishes multiple specialized Work-Based Roles (WBRs). |
| **WORK_ROLES** | **FRAC_COMPETENCIES** | Mandates | 1 : N | Each WBR requires a set of behavioral, functional, and domain competencies. |
| **DOCUMENTS** | **DOCUMENT_CHUNKS** | Partitioned Into | 1 : N | A document is split into ordered, overlapping statutory chunks. |
| **DOCUMENT_CHUNKS** | **EMBEDDINGS** | Vectorized As | 1 : 1 | Each chunk possesses exactly one 768-dim vector embedding. |
| **DOCUMENTS** | **QUIZZES** | Sources | 1 : N | Multiple quizzes (baseline, formative, comprehensive) can derive from one document. |
| **QUIZZES** | **QUESTIONS** | Contains | 1 : N | A quiz contains an ordered sequence of scenario MCQs. |
| **FRAC_COMPETENCIES** | **QUESTIONS** | Evaluates | 1 : N | Every question directly assesses an explicit FRAC competency node. |
| **USERS** | **QUIZ_ATTEMPTS** | Undertakes | 1 : N | A user may attempt a quiz multiple times to demonstrate competency remediation. |
| **USERS** | **RECOMMENDATIONS** | Receives | 1 : N | A user receives targeted recommendations matching their current deficit vectors. |
| **USERS** | **LEARNING_PROGRESS** | Tracks | 1 : N | Tracks real-time engagement and completion across multiple iGOT courses. |
| **USERS** | **CERTIFICATES** | Awarded To | 1 : N | A user earns immutable certificates upon passing accredited competency thresholds. |
| **USERS** | **AUDIT_LOGS** | Acted By | 1 : N | Every administrative and authoring action is captured for non-repudiation. |

---

## 5. Integrity Constraints & Indexing Strategy

1. **Foreign Key Cascades:**
   - Deleting a `DOCUMENT` cascades to delete associated `DOCUMENT_CHUNKS` and `EMBEDDINGS`.
   - Deleting a `QUIZ` cascades to delete associated `QUESTIONS`.
   - User references in `AUDIT_LOGS` are set to `ON DELETE RESTRICT` to preserve legal audit trails.
2. **Unique Business Keys:**
   - `roles(role_code)`, `departments(department_code)`, `work_roles(role_code)`.
   - `frac_competencies(competency_code)`, `courses(igot_course_id)`.
   - `certificates(certificate_number, verification_hash)`.
3. **Optimized Indexes:**
   - Standard B-tree indexes on foreign keys (`user_id`, `course_id`, `quiz_id`, `document_id`).
   - Composite B-tree index on `quiz_attempts(user_id, quiz_id, attempted_at)`.
   - **HNSW Cosine Vector Index** on `embeddings(embedding_vector_768)` for sub-15ms nearest neighbor searches.

---
*End of ER Diagram Specification*
