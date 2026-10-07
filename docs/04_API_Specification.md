# 04_API_Specification.md

# REST API Specification: AI Karmayogi

**Production OpenAPI / REST Interface Specifications, Request/Response Schemas, and Error Contracts for Mission Karmayogi**

**Document Version:** 1.0.0  
**Target Program:** Smart India Hackathon 2026  
**Problem Statement ID:** SIH26101  
**Project Name:** AI Karmayogi  
**Classification:** Enterprise Government Specification — Phase 2 API Interface  

---

## Table of Contents
1. [API Architecture & Standards](#1-api-architecture--standards)
2. [Authentication & Session Endpoints](#2-authentication--session-endpoints)
3. [Assessment & Competency Diagnostic Endpoints](#3-assessment--competency-diagnostic-endpoints)
4. [Semantic Recommendation Endpoints](#4-semantic-recommendation-endpoints)
5. [Document Upload & Ingestion Endpoints](#5-document-upload--ingestion-endpoints)
6. [Automated Quiz Generation & SME Review Endpoints](#6-automated-quiz-generation--sme-review-endpoints)
7. [Dashboard & Capability Analytics Endpoints](#7-dashboard--capability-analytics-endpoints)
8. [Administration & FRAC Taxonomy Endpoints](#8-administration--frac-taxonomy-endpoints)
9. [Standard Error Envelope & HTTP Status Codes](#9-standard-error-envelope--http-status-codes)

---

## 1. API Architecture & Standards

- **Base URL:** `https://karmayogi.gov.in/api/v1`
- **Protocol:** HTTPS (TLS 1.3 enforced)
- **Data Format:** `application/json` (except multipart file uploads)
- **Authentication:** Bearer Token via JSON Web Token (`Authorization: Bearer <JWT>`)
- **Pagination Standard:** Limit-Offset (`?limit=20&offset=0`)
- **Date/Time Standard:** ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`)

---

## 2. Authentication & Session Endpoints

### 2.1 User Login
- **Method / Path:** `POST /auth/login`
- **Description:** Authenticates a civil servant or official and returns a signed JWT with role claims.

#### Request Headers:
```http
Content-Type: application/json
```

#### Request Body:
```json
{
  "email": "rajesh.kumar@gov.in",
  "password": "SecurePassword123!"
}
```

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMmUzNGU1Ni03OGFjLTkwZGUtYmNmMC0xMjM0NTY3ODkwYWIiLCJyb2xlIjoibGVhcm5lciIsImRlcHQiOiJNaW5pc3RyeSBvZiBIZWF2eSBJbmR1c3RyaWVzIiwiZXhwIjoxNzk4NTMwMDAwfQ.signature",
    "token_type": "Bearer",
    "expires_in": 28800,
    "user": {
      "id": "12e34e56-78ac-90de-bcf0-1234567890ab",
      "full_name": "Rajesh Kumar",
      "email": "rajesh.kumar@gov.in",
      "designation": "Under Secretary",
      "role": "learner",
      "department": "Ministry of Heavy Industries",
      "work_role": "Drawing & Disbursing Officer"
    }
  }
}
```

---

### 2.2 Get Current User Profile
- **Method / Path:** `GET /auth/me`
- **Description:** Retrieves the authenticated user's profile and active FRAC role binding.

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "id": "12e34e56-78ac-90de-bcf0-1234567890ab",
    "full_name": "Rajesh Kumar",
    "email": "rajesh.kumar@gov.in",
    "designation": "Under Secretary",
    "role": "learner",
    "work_role": {
      "id": "99f88d77-66c5-44b3-22a1-001122334455",
      "role_code": "WBR-DDO-001",
      "role_title": "Drawing & Disbursing Officer"
    }
  }
}
```

---

## 3. Assessment & Competency Diagnostic Endpoints

### 3.1 Fetch Adaptive Role Diagnostic
- **Method / Path:** `GET /assessment/diagnostic`
- **Description:** Returns an adaptive, dynamic baseline assessment tailored to the user’s Work-Based Role.

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "diagnostic_id": "33b22a11-44c5-66d7-88e9-aabbccddeeff",
    "work_role": "Drawing & Disbursing Officer",
    "total_questions": 15,
    "questions": [
      {
        "question_id": "aa11bb22-33cc-44dd-55ee-66ff77889900",
        "competency_code": "FC-PROC-001",
        "competency_name": "Public Procurement (GeM & GFR)",
        "bloom_level": "APPLY",
        "stem": "An Assistant Section Officer is procuring IT hardware valued at ₹48,000. A lower quote is offered offline. Which step complies with GFR 2017?",
        "options": [
          "Purchase offline since the price is lower",
          "Procure via GeM portal as mandated by Rule 149",
          "Split the purchase order into two separate requisitions",
          "Publish a physical open tender notice in newspapers"
        ]
      }
    ]
  }
}
```

---

### 3.2 Submit Diagnostic & Compute FRAC Gaps
- **Method / Path:** `POST /assessment/diagnostic/submit`
- **Description:** Evaluates submitted diagnostic answers and computes the civil servant's Competency Deficit Matrix (CDM).

#### Request Body:
```json
{
  "diagnostic_id": "33b22a11-44c5-66d7-88e9-aabbccddeeff",
  "time_taken_seconds": 720,
  "responses": [
    {
      "question_id": "aa11bb22-33cc-44dd-55ee-66ff77889900",
      "selected_option_index": 1
    }
  ]
}
```

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "attempt_id": "ff55ee44-dd33-cc22-bb11-aa0099887766",
    "score_percentage": 66.7,
    "is_passed": true,
    "competency_gaps": [
      {
        "competency_code": "FC-PROC-001",
        "competency_name": "Public Procurement (GeM & GFR)",
        "mandated_level": 4,
        "demonstrated_level": 2,
        "deficit_score": 45.00,
        "status": "ACUTE_DEFICIT",
        "remediation_focus": "Proprietary bidding exceptions under Rule 166"
      }
    ]
  }
}
```

---

## 4. Semantic Recommendation Endpoints

### 4.1 Get Personalized Learning Recommendations
- **Method / Path:** `GET /recommendations`
- **Description:** Returns tailored iGOT courses mapped to the user's active FRAC competency deficit vectors with explainable rationales.

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "total_recommendations": 3,
    "items": [
      {
        "recommendation_id": "88a77b66-55c4-33d2-11e0-ffeeddccbbaa",
        "course_id": "77e66d55-44c3-22b1-00a9-887766554433",
        "igot_course_id": "IGOT-PROC-166",
        "course_title": "Proprietary Articles & Single Tender Procurement on GeM",
        "duration_minutes": 18,
        "target_level": 4,
        "deficit_score": 45.00,
        "explainable_rationale": "Recommended because your active role as Drawing & Disbursing Officer mandates Level 4 in GFR 2017, where a 45% deficit was identified in baseline diagnostics.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-PROC-166"
      }
    ]
  }
}
```

---

## 5. Document Upload & Ingestion Endpoints

### 5.1 Upload Government Document
- **Method / Path:** `POST /documents/upload`
- **Description:** Ingests official government PDFs (Acts, Circulars, OMs) for text extraction, chunking, and Atlas Vector Search embeddings.
- **Content-Type:** `multipart/form-data`

#### Form Parameters:
- `file`: Binary PDF file (Max 50MB)
- `document_title`: String (e.g., "Public Procurement Local Preference Amendment 2026")
- `document_type`: String (`CIRCULAR` | `ACT` | `RULE` | `OM` | `MANUAL`)

#### Response (202 Accepted):
```json
{
  "status": "accepted",
  "data": {
    "document_id": "44d33c22-bb11-aa00-9988-776655443322",
    "document_title": "Public Procurement Local Preference Amendment 2026",
    "file_size_bytes": 4194304,
    "processing_status": "PROCESSING",
    "message": "Document submitted for asynchronous PyMuPDF extraction and nomic-embed-text vectorization."
  }
}
```

---

### 5.2 Get Document Processing Status
- **Method / Path:** `GET /documents/{document_id}/status`
- **Description:** Polls the status of PDF extraction, statutory chunking, and Atlas Vector Search embeddings.

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "document_id": "44d33c22-bb11-aa00-9988-776655443322",
    "processing_status": "EMBEDDED",
    "total_pages": 45,
    "total_chunks": 128,
    "embeddings_generated": 128,
    "completed_at": "2026-09-12T10:15:30Z"
  }
}
```

---

## 6. Automated Quiz Generation & SME Review Endpoints

### 6.1 Generate Assessment from Ingested Document (AIG)
- **Method / Path:** `POST /quizzes/generate`
- **Description:** Triggers local Ollama LLM to synthesize scenario-based MCQs across Bloom's Taxonomy from embedded document chunks.

#### Request Body:
```json
{
  "document_id": "44d33c22-bb11-aa00-9988-776655443322",
  "title": "Public Procurement Amendment 2026 - Formative Quiz",
  "total_questions": 20,
  "bloom_distribution": {
    "REMEMBER": 20,
    "UNDERSTAND": 30,
    "APPLY": 35,
    "ANALYZE": 15
  },
  "passing_percentage": 60
}
```

#### Response (201 Created):
```json
{
  "status": "created",
  "data": {
    "quiz_id": "99e88d77-66c5-44b3-22a1-001122334455",
    "title": "Public Procurement Amendment 2026 - Formative Quiz",
    "status": "SME_REVIEW",
    "questions_generated": 20,
    "message": "Assessment items generated successfully. Ready for Human-in-the-Loop SME review."
  }
}
```

---

### 6.2 SME Review: Fetch Questions for Curation
- **Method / Path:** `GET /quizzes/{quiz_id}/curation`
- **Description:** Retrieves all generated questions, options, distractors, and pedagogical rationales for SME verification.

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "quiz_id": "99e88d77-66c5-44b3-22a1-001122334455",
    "status": "SME_REVIEW",
    "questions": [
      {
        "question_id": "11a22b33-44c5-55d6-66e7-77f88a9900bb",
        "question_stem": "Under the amended Local Content Order, what is the minimum local value addition required for Class-I local suppliers in civil works?",
        "bloom_level": "APPLY",
        "options": [
          "20% local value addition",
          "50% local value addition",
          "60% local value addition",
          "75% local value addition"
        ],
        "correct_option_index": 1,
        "pedagogical_rationale": "Option B (50%) is correct pursuant to Clause 3(a) of OM No. P-45021/2/2017-PP (BE-II). Options A, C, and D represent common thresholds for Class-II suppliers or outdated norms.",
        "source_citation": "OM No. P-45021/2/2017-PP, Page 4, Paragraph 3(a)"
      }
    ]
  }
}
```

---

### 6.3 SME Review: Update / Approve Question
- **Method / Path:** `PUT /quizzes/questions/{question_id}`
- **Description:** Allows an authorized Trainer/SME to edit stems, adjust distractors, or approve questions.

#### Request Body:
```json
{
  "question_stem": "Under the amended Local Content Order, what is the minimum local value addition required for Class-I local suppliers in central infrastructure projects?",
  "options": [
    "20% local value addition",
    "50% local value addition",
    "60% local value addition",
    "75% local value addition"
  ],
  "correct_option_index": 1,
  "pedagogical_rationale": "Updated rationale reflecting central infrastructure caveats under GFR Rule 153."
}
```

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "question_id": "11a22b33-44c5-55d6-66e7-77f88a9900bb",
    "is_approved": true,
    "updated_at": "2026-09-12T10:30:00Z"
  }
}
```

---

## 7. Dashboard & Capability Analytics Endpoints

### 7.1 Departmental Capability Heatmap (Department Head / CCA)
- **Method / Path:** `GET /analytics/department-heatmap`
- **Description:** Provides aggregated, anonymized competency gap metrics across divisions to inform Annual Capacity Building Plans (ACBPs).

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "department": "Ministry of Heavy Industries",
    "total_officers_evaluated": 240,
    "competency_health_index": 78.4,
    "competency_matrix": [
      {
        "competency_code": "FC-PROC-001",
        "competency_name": "Public Procurement (GeM & GFR)",
        "competency_type": "FUNCTIONAL",
        "mandated_average_level": 3.8,
        "demonstrated_average_level": 2.4,
        "cadre_gap_percentage": 58.2,
        "risk_classification": "HIGH_PRIORITY"
      },
      {
        "competency_code": "BC-ETH-001",
        "competency_name": "Ethics & Citizen Centricity",
        "competency_type": "BEHAVIORAL",
        "mandated_average_level": 4.0,
        "demonstrated_average_level": 3.7,
        "cadre_gap_percentage": 12.5,
        "risk_classification": "LOW_PRIORITY"
      }
    ]
  }
}
```

---

## 8. Administration & FRAC Taxonomy Endpoints

### 8.1 Synchronize FRAC Competency Taxonomy
- **Method / Path:** `POST /admin/frac/sync`
- **Description:** Ingests updated national FRAC competency schemas from the Capacity Building Commission (CBC).

#### Request Body:
```json
{
  "version": "2.1.0",
  "source": "Capacity Building Commission",
  "competencies": [
    {
      "competency_code": "DC-EV-001",
      "competency_type": "DOMAIN",
      "competency_name": "Electric Vehicle Subsidies & Standards",
      "mandated_level": 3,
      "description": "Scrutiny of FAME subsidy claims and national battery safety standards."
    }
  ]
}
```

#### Response (200 OK):
```json
{
  "status": "success",
  "data": {
    "inserted_count": 1,
    "updated_count": 0,
    "sync_timestamp": "2026-09-12T10:45:00Z"
  }
}
```

---

## 9. Standard Error Envelope & HTTP Status Codes

All API errors return a standard RFC 7807 compliant error envelope:

```json
{
  "status": "error",
  "error": {
    "code": "STATUTORY_VALIDATION_ERROR",
    "message": "The uploaded document contains conflicting procurement threshold figures.",
    "details": [
      {
        "field": "document_content",
        "issue": "Clause 14 contradicts Section 149 of GFR 2017."
      }
    ],
    "timestamp": "2026-09-12T10:50:00Z"
  }
}
```

### Common HTTP Status Codes:
- `200 OK`: Successful synchronous request.
- `201 Created`: Resource successfully created (Quiz, User, Recommendation).
- `202 Accepted`: Asynchronous request queued (Document parsing, LLM batch generation).
- `400 Bad Request`: Payload validation failed.
- `401 Unauthorized`: Missing or expired JWT token.
- `403 Forbidden`: Insufficient RBAC permission.
- `404 Not Found`: Resource does not exist.
- `422 Unprocessable Entity`: Semantic or schema mismatch.
- `500 Internal Server Error`: Unhandled server exception.

---
*End of REST API Specification*
