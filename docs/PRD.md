# Product Requirements Document (PRD): AI Karmayogi

**AI-Enabled Competency Diagnostic, Personalized Learning Recommendation, and Automated Pedagogical Assessment Platform**

**Document Version:** 1.0.0  
**Target Program:** Smart India Hackathon 2026  
**Problem Statement ID:** SIH26101  
**Project Name:** AI Karmayogi  
**Classification:** Enterprise Government Specification — Phase 1 Product Foundation  

---

## Table of Contents
1. [Product Overview](#1-product-overview)
2. [Strategic Business & Governance Objectives](#2-strategic-business--governance-objectives)
3. [Stakeholder Ecosystem & Governance Structure](#3-stakeholder-ecosystem--governance-structure)
4. [User Personas Summary](#4-user-personas-summary)
5. [Epics & User Stories (with Given-When-Then Criteria)](#5-epics--user-stories-with-given-when-then-criteria)
6. [Functional Goals & System Capabilities](#6-functional-goals--system-capabilities)
7. [Non-Functional Requirements (NFRs)](#7-non-functional-requirements-nfrs)
8. [Scope Matrix (MoSCoW Framework)](#8-scope-matrix-moscow-framework)
9. [Out-of-Scope Declarations](#9-out-of-scope-declarations)
10. [Comprehensive Risk Assessment & Mitigation Matrix](#10-comprehensive-risk-assessment--mitigation-matrix)
11. [Product Key Performance Indicators (KPIs) & Success Scorecard](#11-product-key-performance-indicators-kpis--success-scorecard)

---

## 1. Product Overview

**AI Karmayogi** is an enterprise-grade, domain-specialized artificial intelligence platform designed to integrate directly with the **iGOT Karmayogi** digital learning ecosystem under the **National Programme for Civil Services Capacity Building (NPCSCB - Mission Karmayogi)**.

The platform addresses the critical operational divide between massive digital course availability and demonstrable on-ground civil service competency. It delivers:
1. **Dynamic Competency Diagnostics:** Automatically evaluates civil servants against the standardized **Framework of Roles, Activities, and Competencies (FRAC)** established by the **Capacity Building Commission (CBC)**.
2. **Hyper-Personalized Recommendation Trajectories:** Traverses semantic knowledge graphs to prescribe micro-learning modules mapped to diagnosed capability deficits.
3. **Automated Item Generation (AIG) Engine:** Ingests unstructured sovereign government collateral (Acts, Rules, Gazette Notifications, Office Memorandums, and Training Collateral) and autonomously generates scenario-grounded Multiple Choice Questions (MCQs), distractors, and pedagogical rationales aligned to Bloom’s Revised Taxonomy.

```
+----------------------------------------------------------------------------------------------------+
|                                AI KARMAYOGI SYSTEM TOPOLOGY                                        |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|    +-----------------------------+               +--------------------------------------------+    |
|    |    GOVERNMENT COLLATERAL    |               |            CIVIL SERVANT PROFILE           |    |
|    |  Acts, Rules, OMs, Manuals  |               |        Work-Based Role (WBR) & Desk        |    |
|    +-----------------------------+               +--------------------------------------------+    |
|                   |                                                     |                          |
|                   v                                                     v                          |
|    +-----------------------------+               +--------------------------------------------+    |
|    |   AUTOMATED ITEM & QUIZ     |               |             COMPETENCY GAP &               |    |
|    |     GENERATION ENGINE       |               |           RECOMMENDATION ENGINE            |    |
|    +-----------------------------+               +--------------------------------------------+    |
|                   |                                                     |                          |
|                   +----------------------+------------------------------+                          |
|                                          |                                                         |
|                                          v                                                         |
|                       +--------------------------------------+                                     |
|                       |    iGOT KARMAYOGI LEARNING ENGINE    |                                     |
|                       | Personalized Trajectory & Validation |                                     |
|                       +--------------------------------------+                                     |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Strategic Business & Governance Objectives

The strategic imperatives governing AI Karmayogi are aligned with Department of Personnel and Training (DoPT) and CBC mandates:

| Objective ID | Strategic Objective | Target Milestone | Primary Metric |
| :--- | :--- | :--- | :--- |
| **SBO-01** | Transition civil service training from *rules-based* to *roles-based* capability building. | Full pilot in 5 Central Ministries within 9 months. | 100% of pilot participants mapped to verified FRAC WBR profiles. |
| **SBO-02** | Eliminate the content authoring bottleneck for training academies and SMEs. | Production deployment across ISTM, LBSNAA, and 5 ATIs. | 95% reduction in time required to generate accredited assessments (< 30 min). |
| **SBO-03** | Elevate pedagogical assessment rigor from rote recall to applied administrative decision-making. | Ongoing across all ingested modules. | > 65% of generated items verified at Bloom's Levels 3 (Apply) and 4 (Analyze). |
| **SBO-04** | Optimize public resource utilization in Annual Capacity Building Plans (ACBPs). | Implementation by CBC for FY 2027–28 planning. | 100% data-driven ACBP budget allocation based on empirical gap heatmaps. |

---

## 3. Stakeholder Ecosystem & Governance Structure

The implementation and ongoing governance of AI Karmayogi involve multi-tiered institutional ownership:

```
+----------------------------------------------------------------------------------------------------+
|                                 STAKEHOLDER GOVERNANCE MATRIX                                      |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ APEX OVERSIGHT ]                                                                                |
|  * Prime Minister's Public Human Resources Council (Strategic Directive)                           |
|  * Capacity Building Commission (CBC) (Standards, FRAC Taxonomy, Quality Audit)                   |
|                                                                                                    |
|  [ PLATFORM OPERATOR & IMPLEMENTER ]                                                               |
|  * Karmayogi Bharat SPV (Digital Architecture, Infrastructure, iGOT Core Integration)              |
|  * National Informatics Centre (NIC) / MeitY (Cloud Hosting & Security Audit)                     |
|                                                                                                    |
|  [ TRAINING ACADEMIES & CONTENT PRODUCERS ]                                                        |
|  * LBSNAA, ISTM, SVPNPA, IIPA, State ATIs (Content Ingestion, SME Review, Pedagogical Oversight)  |
|                                                                                                    |
|  [ CONSUMING BODIES & LEARNERS ]                                                                   |
|  * Central Ministries, Departments, Attached Offices (Cadre Controlling Authorities - CCAs)        |
|  * Individual Civil Servants (Groups A, B, and C across India)                                     |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. User Personas Summary

AI Karmayogi serves four distinct administrative archetypes (detailed exhaustively in `User_Personas.md`):

| Persona Archetype | Representative Profile | Core Responsibility | Primary Value Realized |
| :--- | :--- | :--- | :--- |
| **1. The Learner** | Rajesh Kumar, Under Secretary / Section Officer (CSS) | File management, procurement approval, RTI disposal. | Discovers exact competency deficits; receives targeted micro-learning instead of catalog clutter. |
| **2. The Trainer / SME** | Dr. Sunita Deshmukh, Course Director (National / State Academy) | Designing curricula, authoring assessments, lecturing. | Eliminates manual drafting drudgery; generates 50 scenario-based MCQs from new circulars in minutes. |
| **3. Department Head (CCA)** | Amitabh Sharma, IAS, Joint Secretary / Cadre Authority | Directorate leadership, desk assignments, performance. | Accesses empirical capability heatmaps; identifies team weaknesses before procedural errors occur. |
| **4. Platform Administrator** | Priya Nair, Lead Systems & Pedagogical Admin (Karmayogi Bharat) | Platform uptime, FRAC sync, audit logging, security. | Seamlessly updates FRAC taxonomies, monitors model latency, ensures zero data exfiltration. |

---

## 5. Epics & User Stories (with Given-When-Then Criteria)

### EPIC 1: Dynamic Competency Diagnostic & FRAC Gap Mapping

#### User Story 1.1: Automated Role-Based Baseline Diagnostic
- **As a:** Civil Servant (Learner)
- **I want to:** Complete a dynamic, adaptive baseline diagnostic tailored to my specific Work-Based Role (WBR)
- **So that:** I can understand my precise behavioral, functional, and domain competency gaps without manual search.

**Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Civil Servant initiates dynamic role diagnostic
  Given the learner has an active iGOT profile with a verified Work-Based Role (e.g., "Drawing & Disbursing Officer")
  When the learner navigates to the "Competency Diagnostic" dashboard
  Then the system dynamically generates an adaptive 15-question assessment aligned to the required FRAC competencies
  And the questions reflect the required proficiency levels (e.g., Level 3 in GFR 2017)
  And upon completion, the system renders a visual Competency Gap Matrix showing demonstrated vs. mandated proficiency.
```

#### User Story 1.2: Explainable Recommendation Rationale
- **As a:** Civil Servant (Learner)
- **I want to:** View a transparent, administrative justification for every recommended course
- **So that:** I understand why the training is necessary for my active administrative duties.

**Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Learner reviews recommended learning pathway
  Given the learner has completed a competency diagnostic displaying a gap in "Public Procurement (GeM)"
  When the recommendation engine suggests the micro-module "Direct Purchase & L1 Evaluation on GeM"
  Then the course card must display an explicit explanation: "Recommended because your role requires Level 3 in GeM Procurement, where a 40% deficit was identified."
  And clicking the card launches the specific module directly on iGOT.
```

---

### EPIC 2: Automated Pedagogical Item & Quiz Generation (AIG)

#### User Story 2.1: Unstructured Document Ingestion & Parsing
- **As a:** Training Academy Course Director / SME (Trainer)
- **I want to:** Upload an official government PDF (Act, Rule, Gazette, or Office Memorandum)
- **So that:** The AI can autonomously parse its legal hierarchy and extract key pedagogical concepts.

**Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Trainer uploads a newly issued Office Memorandum
  Given the trainer is authenticated with SME credentials on the AI Karmayogi Admin Portal
  When the trainer uploads a 25-page PDF of the "General Financial Rules (Amendment) OM"
  Then the system parses the document, preserves section hierarchies and provisos, and extracts learning objectives within 60 seconds
  And displays a confirmation summary with extracted key entities (e.g., monetary limits, statutory authorities).
```

#### User Story 2.2: Bloom’s Taxonomy-Stratified Item Generation
- **As a:** Training Academy Course Director / SME (Trainer)
- **I want to:** Generate Multiple Choice Questions stratified across Bloom’s Taxonomy (Levels 1 to 4)
- **So that:** I can evaluate higher-order analytical decision-making rather than simple memorization.

**Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Autonomous generation of scenario-based MCQs
  Given an ingested government circular on "Public Procurement"
  When the trainer selects "Generate Assessment" and sets the target distribution to "30% Recall, 40% Application, 30% Analysis"
  Then the engine outputs 20 structured MCQs matching the requested distribution
  And each question includes 1 verified correct key, 3 plausible administrative distractors, and an explanatory citation referencing the source clause.
```

#### User Story 2.3: Human-in-the-Loop (HITL) SME Curation Interface
- **As a:** Subject Matter Expert (Trainer)
- **I want to:** Review, edit, approve, or regenerate individual AI-generated questions and distractors
- **So that:** Institutional accuracy and statutory correctness are 100% verified prior to publishing.

**Acceptance Criteria (Gherkin):**
```gherkin
Scenario: SME edits an AI-generated distractor
  Given a generated scenario MCQ where Distractor C is slightly ambiguous
  When the SME clicks "Edit Item", modifies the text of Distractor C, and clicks "Approve & Save"
  Then the question is flagged as "SME-Verified"
  And the updated item is committed to the accredited question bank ready for live iGOT student delivery.
```

---

### EPIC 3: Cadre Capability Telemetry & Administrative Oversight

#### User Story 3.1: Anonymized Departmental Competency Heatmap
- **As a:** Joint Secretary / Cadre Controlling Authority (Department Head)
- **I want to:** View an aggregated, anonymized competency heatmap of my directorate
- **So that:** I can identify organizational capability vulnerabilities and prioritize targeted training drives.

**Acceptance Criteria (Gherkin):**
```gherkin
Scenario: Department Head inspects division capability health
  Given the Department Head accesses the "Cadre Competency Analytics" portal
  When they filter by "Division: Public Works & Infrastructure"
  Then the dashboard renders a color-coded matrix of all FRAC competencies
  And highlights that 62% of staff exhibit a gap in "Contract Dispute Arbitration"
  And provides an exportable summary to inform the Annual Capacity Building Plan (ACBP).
```

---

## 6. Functional Goals & System Capabilities

The functional requirements are partitioned into four core modules:

```
+----------------------------------------------------------------------------------------------------+
|                                    FUNCTIONAL CAPABILITY STACK                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ MODULE 1: COMPETENCY DIAGNOSTIC ENGINE ]                                                        |
|  * FRAC Taxonomy Repository Sync (DoPT/CBC standard).                                              |
|  * Dynamic Adaptive Testing (Item Response Theory calibration).                                   |
|  * Individual Competency Deficit Matrix (CDM) computation.                                         |
|                                                                                                    |
|  [ MODULE 2: SEMANTIC RECOMMENDATION ENGINE ]                                                      |
|  * Multi-dimensional Knowledge Graph traversal (Learner -> Deficit -> Course -> Outcome).          |
|  * Collaborative filtering with cold-start cadre heuristics.                                       |
|  * Dynamic learning trajectory re-ranking post-assessment.                                         |
|                                                                                                    |
|  [ MODULE 3: AUTOMATED ITEM & QUIZ GENERATION ENGINE (AIG) ]                                       |
|  * Multi-format document parser (PDF, DOCX, Gazette scans via OCR).                                |
|  * Statutory chunking engine preserving legal caveats and clauses.                                 |
|  * Bloom's Taxonomy item generator (Levels 1–4).                                                   |
|  * Administrative distractor synthesis with citation-backed remediation.                          |
|  * Human-in-the-loop (HITL) review and bulk export to iGOT QTI/SCORM format.                       |
|                                                                                                    |
|  [ MODULE 4: GOVERNANCE & TELEMETRY DASHBOARD ]                                                    |
|  * Role-based access control (Learner, SME, CCA, CBC Admin).                                      |
|  * Real-time competency gap heatmaps and ACBP planning telemetry.                                  |
|  * Immutable audit logging of all AI-generated and SME-approved items.                             |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 7. Non-Functional Requirements (NFRs)

To meet the rigorous standards of Government of India digital infrastructure, the system enforces the following non-functional specifications:

| Dimension | Specification Requirement | Validation / Compliance Method |
| :--- | :--- | :--- |
| **Data Residency & Sovereignty** | 100% of data, embeddings, and models must reside within Indian borders. | Hosted strictly on MeitY-empanelled cloud infrastructure (NIC / MeghRaj). Zero third-party foreign API egress. |
| **System Concurrency & Throughput** | Must support **50,000 concurrent active assessment takers** with p95 API response times < 800ms. | Validated via distributed load testing using JMeter simulating national peak training hours (*Karmayogi Saptah*). |
| **AIG Generation Latency** | Autonomous generation of a 20-item accredited quiz from a 30-page PDF in **< 120 seconds**. | Monitored via asynchronous Celery/Redis queue telemetry. |
| **Accessibility Compliance** | Strict adherence to **Guidelines for Indian Government Websites (GIGW 3.0)** and **WCAG 2.1 Level AA**. | Automated Axe-core audits and screen-reader accessibility verification (NVDA / JAWS). |
| **Security & Privacy** | Decoupling of diagnostic competency gap scores from official performance appraisal records (APAR). | Cryptographic hashing of learner IDs in analytics stores; Role-Based Access Control (RBAC); CERT-In security audit clearance. |
| **Availability & RPO/RTO** | **99.9% uptime** during active administrative hours (08:00 to 22:00 IST). RPO < 15 minutes, RTO < 1 hour. | Multi-zone redundant database clustering with automated snapshot failover. |

---

## 8. Scope Matrix (MoSCoW Framework)

The product scope for Phase 1 (MVP) is strictly prioritized using the MoSCoW framework:

```
+----------------------------------------------------------------------------------------------------+
|                                    MOSCOW SCOPE SPECIFICATION                                      |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  MUST HAVE (Phase 1 MVP - SIH 2026 Core)                                                           |
|  * Ingestion & parsing of government text/PDF documents (circulars, rules, acts).                  |
|  * Automated generation of MCQs across Bloom's Levels 1 to 4 with distractors & rationales.        |
|  * Human-in-the-loop SME review and approval dashboard.                                           |
|  * Standardized FRAC competency dictionary mapping (Behavioral, Functional, Domain).               |
|  * Baseline competency diagnostic assessment module for civil servants.                            |
|  * Basic explainable course recommendation linking gaps to iGOT modules.                           |
|                                                                                                    |
|  SHOULD HAVE (Phase 1.5 - Fast Follow Pilot)                                                       |
|  * OCR parsing for degraded scanned historical gazettes.                                          |
|  * Departmental competency gap heatmaps for Cadre Controlling Authorities.                         |
|  * Export of approved assessments in SCORM 1.2 / QTI formats for direct iGOT LMS import.           |
|                                                                                                    |
|  COULD HAVE (Phase 2 - Planned Roadmap)                                                            |
|  * Integration with Project Bhashini for automated translation into 22 Indic languages.            |
|  * Interactive branching scenario-based dilemma simulations.                                       |
|                                                                                                    |
|  WON'T HAVE (Deferred to Phase 3 / Long-Term)                                                      |
|  * Live video/audio conversational proctoring.                                                     |
|  * Direct read/write linkage to APAR appraisal or confidential service dossiers.                   |
|  * Fully autonomous publishing without SME approval.                                               |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 9. Out-of-Scope Declarations

To maintain rigorous development boundaries and ensure delivery during Phase 1, the following features are explicitly declared **OUT OF SCOPE**:

1. **Direct Modification of Core iGOT Video Player / LMS Database:** AI Karmayogi acts as an intelligence microservice layer; it does not replace the existing open-source Sunbird platform powering iGOT.
2. **Automated Appraisal (APAR) Scoring:** The system shall under no circumstances calculate or feed scores into an officer's Annual Performance Appraisal Report.
3. **Fully Autonomous Unchecked Item Publishing:** Every generated assessment item must pass through a human SME review gate before being served to learners.
4. **General Public or Commercial EdTech Deployment:** The platform is purpose-built solely for Indian sovereign public administrative personnel.

---

## 10. Comprehensive Risk Assessment & Mitigation Matrix

```
+----------------------------------------------------------------------------------------------------+
|                                    RISK SEVERITY & MITIGATION MATRIX                               |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ RISK 1: AI Hallucination in Legal Nuances ] (High Severity)                                     |
|  * Mitigation: Human-in-the-Loop SME gate + Strict retrieval grounding in source text chunks.      |
|                                                                                                    |
|  [ RISK 2: Civil Servant Apprehension of Punitive Tagging ] (High Severity)                        |
|  * Mitigation: Explicit policy & architectural decoupling from APAR; encrypted anonymized gap data.|
|                                                                                                    |
|  [ RISK 3: Degradation on Scanned Government PDFs ] (Medium Severity)                             |
|  * Mitigation: Multi-stage pre-processing pipeline using specialized Indian OCR models.            |
|                                                                                                    |
|  [ RISK 4: Model Drift from Changing Policy Guidelines ] (Medium Severity)                         |
|  * Mitigation: Version-tagged document chunks; automatic invalidation of obsolete question items.  |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### Detailed Risk Management Table:

| Risk ID | Risk Description | Probability | Impact | Risk Level | Preventative Mitigation Strategy |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **RSK-01** | **Statutory Hallucination:** LLM generates a quiz question with an inaccurate legal interpretation of an Act. | Medium | Critical | **HIGH** | Strict RAG (Retrieval-Augmented Generation) pipeline constraining the model exclusively to provided text; mandatory SME verification gate before live deployment. |
| **RSK-02** | **Apprehension of Surveillance:** Civil servants deliberately game or avoid diagnostics fearing negative APAR impacts. | High | High | **HIGH** | DoPT circular issued establishing the strictly formative, non-punitive nature of the platform; technical separation of gap telemetry from cadre dossiers. |
| **RSK-03** | **OCR Degradation:** Inability to accurately parse scanned, low-resolution gazette notifications. | High | Medium | **MEDIUM** | Deployment of specialized document restoration filters and adaptive OCR binarization prior to semantic chunking. |
| **RSK-04** | **Regulatory Obsolescence:** Questions generated from superseded OMs remain active in the assessment bank. | Medium | High | **MEDIUM** | Strict document versioning metadata; automated expiry flags triggered when newer OMs citing the same rule are ingested. |
| **RSK-05** | **Sovereign Cloud Latency Spikes:** Compute resource bottlenecks during peak national learning drives. | Medium | Medium | **MEDIUM** | Auto-scaling Kubernetes deployment on NIC MeghRaj; asynchronous queueing for assessment generation tasks. |

---

## 11. Product Key Performance Indicators (KPIs) & Success Scorecard

| KPI ID | Performance Metric | Baseline Metric | Target MVP (Phase 1) | Target Scale (Year 1) | Measurement Frequency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-01** | Assessment Authoring Turnaround | 15–20 Business Days | **< 30 Minutes** | **< 15 Minutes** | Per Module Ingestion |
| **KPI-02** | Bloom's Higher-Order Item Share | < 15% | **> 60%** (Apply/Analyze) | **> 70%** (Apply/Analyze) | Bi-weekly Audit |
| **KPI-03** | SME Item Acceptance Rate | N/A (Manual) | **> 80%** without rewrite | **> 90%** without rewrite | Monthly Assessment |
| **KPI-04** | Competency Diagnostic Completion | < 20% (Manual APAR) | **> 65%** in pilot units | **> 80%** across cadres | Quarterly Cohort |
| **KPI-05** | Learner Course Recommendation CTR | < 12% | **> 45%** | **> 60%** | Weekly Telemetry |
| **KPI-06** | 60-Day Competency Retention Rate | < 25% | **> 60%** | **> 75%** | Post-Training Re-test |

---
*End of Product Requirements Document*
