# ==============================================================================
# AI KARMAYOGI — PERSONALIZED RECOMMENDATION SERVICE
# Multi-Objective Course Ranking, Bayesian Calibration & Deterministic XAI
# ==============================================================================

import math
import uuid
from typing import Optional, Sequence, Any, List, Dict

from app.models.entities import _to_obj, _to_list, new_uuid, utcnow
try:
    from repositories.user_repository import UserRepository
    from repositories.course_repository import CourseRepository
    from repositories.recommendation_repository import RecommendationRepository
    from repositories.competency_repository import CompetencyRepository
    from repositories.assessment_repository import AssessmentRepository
except ImportError:
    from app.repositories.user_repository import UserRepository
    from app.repositories.course_repository import CourseRepository
    from app.repositories.recommendation_repository import RecommendationRepository
    from app.repositories.competency_repository import CompetencyRepository
    from app.repositories.assessment_repository import AssessmentRepository

# Production Model Weight Coefficients (docs/02_Recommendation_Engine.md)
OMEGA_DEFICIT = 0.40
OMEGA_SEMANTIC = 0.30
OMEGA_DURATION = 0.20
OMEGA_CADRE = 0.10

FALLBACK_RECOMMENDATIONS_DATA = [
    {
        "_id": "55555555-5555-5555-5555-555555550001",
        "id": "55555555-5555-5555-5555-555555550001",
        "course_id": "44444444-4444-4444-4444-444444444001",
        "competency_id": "44444444-4444-4444-4444-444444444401",
        "priority": 1,
        "confidence": 0.94,
        "deficit_score": 50.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "IMMEDIATE",
        "explainable_rationale": "[Critical Desk Priority] Cold-start fallback recommended to bridge foundational compliance under GFR 2017.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444001",
            "_id": "44444444-4444-4444-4444-444444444001",
            "igot_course_id": "IGOT-GFR-101",
            "title": "General Financial Rules 2017: Core Principles & Delegated Powers",
            "ministry": "Ministry of Finance (Department of Expenditure)",
            "duration_minutes": 15,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "Bilingual (Hindi/English)",
            "tags": ["GFR 2017", "Public Finance", "Delegation of Powers", "Expenditure Control"],
            "learning_outcomes": [
                "Understand fundamental principles of government expenditure (Rule 21)",
                "Identify standard expenditure sanctions and Financial Adviser concurrence workflows"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-101",
            "competency_id": "44444444-4444-4444-4444-444444444401",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444401",
            "_id": "44444444-4444-4444-4444-444444444401",
            "competency_code": "COMP-GFR-01",
            "competency_name": "Public Procurement & GFR 2017 Compliance",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550002",
        "id": "55555555-5555-5555-5555-555555550002",
        "course_id": "44444444-4444-4444-4444-444444444002",
        "competency_id": "44444444-4444-4444-4444-444444444401",
        "priority": 2,
        "confidence": 0.91,
        "deficit_score": 50.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "IMMEDIATE",
        "explainable_rationale": "[Critical Desk Priority] Procedural walkthrough of tender documents and EMD under GFR 2017.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444002",
            "_id": "44444444-4444-4444-4444-444444444002",
            "igot_course_id": "IGOT-GFR-201",
            "title": "Public Procurement Rulebook: Tenders, EMD & Performance Security",
            "ministry": "Ministry of Finance (Department of Expenditure)",
            "duration_minutes": 20,
            "target_level": 2,
            "difficulty": "INTERMEDIATE",
            "language": "English",
            "tags": ["Tendering", "EMD", "Performance Guarantee", "Bid Security"],
            "learning_outcomes": [
                "Calculate Earnest Money Deposit and Performance Bank Guarantee requirements",
                "Execute standard two-stage bidding systems compliant with CVC guidelines"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-201",
            "competency_id": "44444444-4444-4444-4444-444444444401",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444401",
            "_id": "44444444-4444-4444-4444-444444444401",
            "competency_code": "COMP-GFR-01",
            "competency_name": "Public Procurement & GFR 2017 Compliance",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550003",
        "id": "55555555-5555-5555-5555-555555550003",
        "course_id": "44444444-4444-4444-4444-444444444003",
        "competency_id": "44444444-4444-4444-4444-444444444402",
        "priority": 3,
        "confidence": 0.89,
        "deficit_score": 50.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "IMMEDIATE",
        "explainable_rationale": "[Critical Desk Priority] Master official file noting, draft types and reference protocols under CSMOP.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444003",
            "_id": "44444444-4444-4444-4444-444444444003",
            "igot_course_id": "IGOT-MOP-101",
            "title": "CSMOP 16th Edition: Fundamentals of Noting, Drafting & Official Files",
            "ministry": "Ministry of Personnel (DARPG)",
            "duration_minutes": 15,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "Bilingual (Hindi/English)",
            "tags": ["CSMOP", "Noting and Drafting", "Secretariat Practice", "File Management"],
            "learning_outcomes": [
                "Structure official notes compliant with CSMOP Paragraph 32 style rules",
                "Select appropriate draft formats for Inter-Departmental references"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-MOP-101",
            "competency_id": "44444444-4444-4444-4444-444444444402",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444402",
            "_id": "44444444-4444-4444-4444-444444444402",
            "competency_code": "COMP-MOP-01",
            "competency_name": "Central Secretariat File Management & CSMOP",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550004",
        "id": "55555555-5555-5555-5555-555555550004",
        "course_id": "44444444-4444-4444-4444-444444444004",
        "competency_id": "44444444-4444-4444-4444-444444444402",
        "priority": 4,
        "confidence": 0.88,
        "deficit_score": 37.5,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "RECOMMENDED_THIS_WEEK",
        "explainable_rationale": "[Targeted Functional Enhancement] Operational practice on e-Office electronic file movement & DSC validation.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444004",
            "_id": "44444444-4444-4444-4444-444444444004",
            "igot_course_id": "IGOT-MOP-201",
            "title": "e-Office 7.0 Mastery: Lifecycle, Electronic Movement & Auditing",
            "ministry": "National Informatics Centre (NIC)",
            "duration_minutes": 20,
            "target_level": 2,
            "difficulty": "INTERMEDIATE",
            "language": "English",
            "tags": ["e-Office", "NIC", "Digital Files", "DSC", "File Tracking"],
            "learning_outcomes": [
                "Navigate e-File creation, electronic diarization, and docketing lifecycle",
                "Apply Digital Signature Certificate signing compliant with CCA guidelines"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-MOP-201",
            "competency_id": "44444444-4444-4444-4444-444444444402",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444402",
            "_id": "44444444-4444-4444-4444-444444444402",
            "competency_code": "COMP-MOP-01",
            "competency_name": "Central Secretariat File Management & CSMOP",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550005",
        "id": "55555555-5555-5555-5555-555555550005",
        "course_id": "44444444-4444-4444-4444-444444444005",
        "competency_id": "44444444-4444-4444-4444-444444444403",
        "priority": 5,
        "confidence": 0.86,
        "deficit_score": 25.0,
        "estimated_improvement": "+1 Level (Level 3 → Level 4)",
        "trajectory_stage": "RECOMMENDED_THIS_WEEK",
        "explainable_rationale": "[Continuous Capability Building] Deepens ethical conduct standards under CCS Conduct Rules 1964.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444005",
            "_id": "44444444-4444-4444-4444-444444444005",
            "igot_course_id": "IGOT-ETH-101",
            "title": "CCS Conduct Rules 1964: Professional Ethics & Public Interest",
            "ministry": "Ministry of Personnel (DoPT)",
            "duration_minutes": 20,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "Bilingual (Hindi/English)",
            "tags": ["CCS Rules", "Code of Conduct", "Integrity", "Ethics in Governance"],
            "learning_outcomes": [
                "Interpret Rule 3 fundamental duties of civil servants with case law",
                "Comply with regulations regarding gifts, hospitality, and public demonstrations"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-ETH-101",
            "competency_id": "44444444-4444-4444-4444-444444444403",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444403",
            "_id": "44444444-4444-4444-4444-444444444403",
            "competency_code": "COMP-ETH-01",
            "competency_name": "Ethical Governance & Conflict of Interest",
            "competency_type": "BEHAVIORAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550006",
        "id": "55555555-5555-5555-5555-555555550006",
        "course_id": "44444444-4444-4444-4444-444444444006",
        "competency_id": "44444444-4444-4444-4444-444444444403",
        "priority": 6,
        "confidence": 0.85,
        "deficit_score": 25.0,
        "estimated_improvement": "+1 Level (Level 3 → Level 4)",
        "trajectory_stage": "RECOMMENDED_THIS_WEEK",
        "explainable_rationale": "[Targeted Functional Enhancement] Protocol for identifying conflicts of interest and formal recusal.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444006",
            "_id": "44444444-4444-4444-4444-444444444006",
            "igot_course_id": "IGOT-ETH-201",
            "title": "Identifying & Managing Conflicts of Interest in Administration",
            "ministry": "Central Vigilance Commission (CVC)",
            "duration_minutes": 25,
            "target_level": 2,
            "difficulty": "INTERMEDIATE",
            "language": "English",
            "tags": ["Conflict of Interest", "Recusal", "Probity", "Vigilance"],
            "learning_outcomes": [
                "Recognize pecuniary, commercial, and familial conflicts of interest",
                "Execute formal written recusal from tender evaluation and recruitment boards"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-ETH-201",
            "competency_id": "44444444-4444-4444-4444-444444444403",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444403",
            "_id": "44444444-4444-4444-4444-444444444403",
            "competency_code": "COMP-ETH-01",
            "competency_name": "Ethical Governance & Conflict of Interest",
            "competency_type": "BEHAVIORAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550007",
        "id": "55555555-5555-5555-5555-555555550007",
        "course_id": "44444444-4444-4444-4444-444444444007",
        "competency_id": "44444444-4444-4444-4444-444444444404",
        "priority": 7,
        "confidence": 0.84,
        "deficit_score": 25.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "RECOMMENDED_THIS_WEEK",
        "explainable_rationale": "[Targeted Functional Enhancement] Accelerates Sevottam compliance and 21-day grievance disposal on CPGRAMS.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444007",
            "_id": "44444444-4444-4444-4444-444444444007",
            "igot_course_id": "IGOT-CIT-101",
            "title": "CPGRAMS 7.0: Fundamentals of Grievance Redressal & Citizen Charter",
            "ministry": "Ministry of Personnel (DARPG)",
            "duration_minutes": 15,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "Bilingual (Hindi/English)",
            "tags": ["CPGRAMS", "Public Grievances", "Citizen Charter", "Sevottam Framework"],
            "learning_outcomes": [
                "Navigate CPGRAMS 7.0 grievance lifecycle, classification, and assignment",
                "Adhere to the mandatory 21-day disposal SLA prescribed by DARPG"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-CIT-101",
            "competency_id": "44444444-4444-4444-4444-444444444404",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444404",
            "_id": "44444444-4444-4444-4444-444444444404",
            "competency_code": "COMP-CIT-01",
            "competency_name": "Citizen-Centric Public Grievance Disposal",
            "competency_type": "BEHAVIORAL",
            "mandated_level": 3,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550008",
        "id": "55555555-5555-5555-5555-555555550008",
        "course_id": "44444444-4444-4444-4444-444444444008",
        "competency_id": "44444444-4444-4444-4444-444444444405",
        "priority": 8,
        "confidence": 0.83,
        "deficit_score": 25.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "ADVANCED",
        "explainable_rationale": "[Targeted Functional Enhancement] Scrutinizes statutory timeline compliance and Section 8 exemptions under RTI.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444008",
            "_id": "44444444-4444-4444-4444-444444444008",
            "igot_course_id": "IGOT-RTI-101",
            "title": "Right to Information Act 2005: Role & Duties of PIOs",
            "ministry": "Central Information Commission (CIC)",
            "duration_minutes": 20,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "English",
            "tags": ["RTI Act", "CPIO", "Transparency", "Statutory Deadlines"],
            "learning_outcomes": [
                "Process RTI applications within the statutory 30-day window",
                "Apply third-party information disclosure rules under Section 11"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-RTI-101",
            "competency_id": "44444444-4444-4444-4444-444444444405",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444405",
            "_id": "44444444-4444-4444-4444-444444444405",
            "competency_code": "COMP-RTI-01",
            "competency_name": "Right to Information & Statutory Appeals",
            "competency_type": "DOMAIN",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550009",
        "id": "55555555-5555-5555-5555-555555550009",
        "course_id": "44444444-4444-4444-4444-444444444009",
        "competency_id": "44444444-4444-4444-4444-444444444406",
        "priority": 9,
        "confidence": 0.82,
        "deficit_score": 25.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "ADVANCED",
        "explainable_rationale": "[Continuous Capability Building] Formulates compliant charge sheets under CCS (CCA) Rule 14.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444009",
            "_id": "44444444-4444-4444-4444-444444444009",
            "igot_course_id": "IGOT-EST-101",
            "title": "Fundamental Rules & Supplementary Rules (FRSR): Service Matters",
            "ministry": "Ministry of Personnel (DoPT)",
            "duration_minutes": 20,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "English",
            "tags": ["FRSR", "Pay Fixation", "Seniority", "Service Book"],
            "learning_outcomes": [
                "Interpret Fundamental Rules governing pay fixation, allowances, and probation",
                "Audit Service Book entries and calculate Leave Encashment entitlements"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-EST-101",
            "competency_id": "44444444-4444-4444-4444-444444444406",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444406",
            "_id": "44444444-4444-4444-4444-444444444406",
            "competency_code": "COMP-EST-01",
            "competency_name": "Establishment Rules & Disciplinary Proceedings",
            "competency_type": "DOMAIN",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550010",
        "id": "55555555-5555-5555-5555-555555550010",
        "course_id": "44444444-4444-4444-4444-444444444010",
        "competency_id": "44444444-4444-4444-4444-444444444407",
        "priority": 10,
        "confidence": 0.85,
        "deficit_score": 25.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "ADVANCED",
        "explainable_rationale": "[Targeted Functional Enhancement] Direct purchase, L1 comparison, and reverse auction under GeM Rule 149.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444010",
            "_id": "44444444-4444-4444-4444-444444444010",
            "igot_course_id": "IGOT-GEM-101",
            "title": "GeM Portal Operations: Direct Purchase, L1 Comparison & Procurement",
            "ministry": "Ministry of Commerce and Industry (GeM SPV)",
            "duration_minutes": 20,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "Bilingual (Hindi/English)",
            "tags": ["GeM", "Rule 149", "Direct Purchase", "L1 Comparison"],
            "learning_outcomes": [
                "Execute direct purchases up to ₹25,000 threshold compliant with Rule 149",
                "Conduct mandatory 3-vendor L1 price comparisons on GeM"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GEM-101",
            "competency_id": "44444444-4444-4444-4444-444444444407",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444407",
            "_id": "44444444-4444-4444-4444-444444444407",
            "competency_code": "COMP-GEM-01",
            "competency_name": "Government e-Marketplace (GeM) Bidding",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550011",
        "id": "55555555-5555-5555-5555-555555550011",
        "course_id": "44444444-4444-4444-4444-444444444011",
        "competency_id": "44444444-4444-4444-4444-444444444408",
        "priority": 11,
        "confidence": 0.81,
        "deficit_score": 20.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "OPTIONAL_ENRICHMENT",
        "explainable_rationale": "[Continuous Capability Building] Electronic sanction generation and bill passing in PFMS.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444011",
            "_id": "44444444-4444-4444-4444-444444444011",
            "igot_course_id": "IGOT-BUD-101",
            "title": "PFMS 101: Public Financial Management System Navigation & Payment",
            "ministry": "Ministry of Finance (CGA)",
            "duration_minutes": 20,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "English",
            "tags": ["PFMS", "CGA", "EAT Module", "DBT", "Expenditure Control"],
            "learning_outcomes": [
                "Navigate PFMS user hierarchy (Maker, Checker, Approver)",
                "Generate electronic sanctions and verify vendor bank account credentials"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-BUD-101",
            "competency_id": "44444444-4444-4444-4444-444444444408",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444408",
            "_id": "44444444-4444-4444-4444-444444444408",
            "competency_code": "COMP-BUD-01",
            "competency_name": "Budget Monitoring & Re-appropriation",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    },
    {
        "_id": "55555555-5555-5555-5555-555555550012",
        "id": "55555555-5555-5555-5555-555555550012",
        "course_id": "44444444-4444-4444-4444-444444444012",
        "competency_id": "44444444-4444-4444-4444-444444444410",
        "priority": 12,
        "confidence": 0.80,
        "deficit_score": 20.0,
        "estimated_improvement": "+1 Level (Level 2 → Level 3)",
        "trajectory_stage": "OPTIONAL_ENRICHMENT",
        "explainable_rationale": "[Continuous Capability Building] Foundational grounding in public audit mechanisms and audit memo handling.",
        "status": "ACTIVE",
        "is_demo": True,
        "data_source": "demo",
        "course": {
            "id": "44444444-4444-4444-4444-444444444012",
            "_id": "44444444-4444-4444-4444-444444444012",
            "igot_course_id": "IGOT-AUD-101",
            "title": "Government Audit Architecture: Role of C&AG, DGACR & Internal Audit",
            "ministry": "Comptroller and Auditor General of India (C&AG)",
            "duration_minutes": 15,
            "target_level": 1,
            "difficulty": "FOUNDATION",
            "language": "Bilingual (Hindi/English)",
            "tags": ["Audit", "C&AG", "Audit Paras", "Internal Audit"],
            "learning_outcomes": [
                "Understand the constitutional mandate of the C&AG",
                "Comply with initial audit memos within 24 to 48 hours"
            ],
            "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-AUD-101",
            "competency_id": "44444444-4444-4444-4444-444444444410",
            "is_demo": True,
            "data_source": "demo",
        },
        "competency": {
            "id": "44444444-4444-4444-4444-444444444410",
            "_id": "44444444-4444-4444-4444-444444444410",
            "competency_code": "COMP-AUD-01",
            "competency_name": "Audit Paras & PAC Recommendations Resolution",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
            "is_demo": True,
            "data_source": "demo",
        }
    }
]


class RecommendationService:
    def __init__(self, db):
        self.db = db
        if db is not None:
            self.user_repo = UserRepository(db)
            self.recommendation_repo = RecommendationRepository(db)
            self.competency_repo = CompetencyRepository(db)
            self.course_repo = CourseRepository(db)
            self.assessment_repo = AssessmentRepository(db)
        else:
            self.user_repo = None
            self.recommendation_repo = None
            self.competency_repo = None
            self.course_repo = None
            self.assessment_repo = None
        self.rec_repo = self.recommendation_repo
        self.comp_repo = self.competency_repo
        self.assess_repo = self.assessment_repo

    def calculate_duration_efficiency(self, duration_minutes: int) -> float:
        """
        Micro-learning duration efficiency score:
        S_dur = 1.0 if t <= 20 min, else e^(-(t - 20)/40)
        """
        if duration_minutes <= 20:
            return 1.0
        return float(math.exp(-(duration_minutes - 20) / 40.0))

    def calculate_semantic_similarity(self, course: Any, comp: Any) -> float:
        """
        Calculates deterministic semantic alignment score between course metadata and competency.
        Returns score in [0.70, 0.98].
        """
        course_title = getattr(course, "title", "") or ""
        course_desc = getattr(course, "description", "") or ""
        course_tags = getattr(course, "tags", []) or []
        course_text = f"{course_title} {course_desc} {' '.join(course_tags)}".lower()

        comp_name = getattr(comp, "competency_name", "") or ""
        comp_desc = getattr(comp, "description", "") or ""
        comp_type = getattr(comp, "competency_type", "") or ""
        comp_text = f"{comp_name} {comp_desc} {comp_type}".lower()

        keywords = [word for word in comp_text.replace("&", "").replace("-", " ").split() if len(word) > 3]
        matches = sum(1 for kw in keywords if kw in course_text)
        ratio = matches / max(1, len(keywords))

        # Base similarity floor 0.70 with bonus for keyword density
        similarity = 0.72 + (0.26 * min(1.0, ratio * 1.5))
        return round(min(0.98, similarity), 3)

    def calculate_cadre_relevance(self, course: Any, user: Any, comp: Any, target_needed: int) -> float:
        """
        Evaluates role alignment, ministry relevance, and difficulty suitability.
        """
        score = 0.75
        dept = getattr(user, "department", None)
        if dept:
            ministry_name = getattr(dept, "ministry_name", "") or ""
            course_ministry = getattr(course, "ministry", "") or ""
            if ministry_name and course_ministry and ministry_name.lower() in course_ministry.lower():
                score += 0.15

        course_target = getattr(course, "target_level", 0)
        if course_target == target_needed:
            score += 0.10
        elif abs(course_target - target_needed) == 1:
            score += 0.05

        return min(1.0, score)

    def compute_bayesian_confidence(self, cps: float, n_eval: int) -> float:
        """
        Bayesian adjustment penalizing sparse diagnostic sample sizes:
        Gamma = CPS * sqrt(N_eval / (N_eval + 5))
        """
        factor = math.sqrt(n_eval / (n_eval + 5.0)) if (n_eval + 5) > 0 else 0.5
        calibrated = cps * factor
        return round(min(0.98, max(0.60, calibrated)), 3)

    def synthesize_explainable_rationale(
        self,
        course: Any,
        comp: Any,
        demonstrated_level: int,
        mandated_level: int,
        deficit_pct: float
    ) -> str:
        """
        Synthesizes deterministic, legally grounded civil service administrative rationale.
        """
        comp_name = getattr(comp, "competency_name", "") or ""
        comp_type = getattr(comp, "competency_type", "") or ""
        type_str = comp_type.capitalize()
        level_gap_str = f"Level {demonstrated_level} → Level {mandated_level}"

        name_lower = comp_name.lower()
        if "procurement" in name_lower or "gfr" in name_lower:
            rule_ref = "GFR 2017 (Rule 149 GeM thresholds & Rule 166 PAC provisions)"
        elif "csmop" in name_lower or "file" in name_lower:
            rule_ref = "CSMOP 16th Edition (Noting, drafting, and e-Office audit custody)"
        elif "ethics" in name_lower or "conflict" in name_lower:
            rule_ref = "CCS (Conduct) Rules 1964 (Rule 3(1) integrity & recusal standards)"
        elif "grievance" in name_lower or "citizen" in name_lower:
            rule_ref = "DARPG CPGRAMS guidelines (21-day disposal timelines & Sevottam framework)"
        elif "rti" in name_lower:
            rule_ref = "RTI Act 2005 (Section 8(1) exemption scrutiny & statutory response deadlines)"
        elif "disciplinary" in name_lower or "establishment" in name_lower:
            rule_ref = "CCS (CCA) Rules 1965 (Rule 14 charge sheet drafting & natural justice)"
        elif "gem" in name_lower:
            rule_ref = "GeM SPV Procurement Manual (Direct purchase & reverse auction SLAs)"
        elif "budget" in name_lower:
            rule_ref = "Ministry of Finance Cash Management Rules (MEP/QEL & PFMS reconciliation)"
        elif "audit" in name_lower or "pac" in name_lower:
            rule_ref = "C&AG Regulations & Public Accounts Committee (PAC) Action Taken Notes protocol"
        else:
            rule_ref = "Mission Karmayogi Civil Service Competency Framework"

        if deficit_pct >= 50:
            urgency = "Critical Desk Priority"
            detail = f"Identified an acute {deficit_pct:.1f}% capability deficit in {comp_name}."
        elif deficit_pct >= 25:
            urgency = "Targeted Functional Enhancement"
            detail = f"Addresses an active {deficit_pct:.1f}% competency gap in {comp_name}."
        else:
            urgency = "Continuous Capability Building"
            detail = f"Refines demonstrated mastery in {comp_name} ({type_str})."

        return f"[{urgency}] {detail} Recommended to bridge {level_gap_str} compliant with {rule_ref}."

    def get_fallback_recommendations(self, user_id: Any = None) -> Sequence[Any]:
        """
        Generates deterministic cold-start fallback recommendations.
        Always exposes is_demo=True and data_source="demo".
        """
        uid_str = str(user_id) if user_id else "11111111-1111-1111-1111-111111111101"
        results = []
        for item in FALLBACK_RECOMMENDATIONS_DATA:
            rec_dict = dict(item)
            rec_dict["user_id"] = uid_str
            rec_dict["is_demo"] = True
            rec_dict["data_source"] = "demo"
            results.append(rec_dict)
        return _to_list(results)

    async def get_or_generate_recommendations(
        self,
        user_id: Any,
        force_regenerate: bool = False
    ) -> Sequence[Any]:
        """
        Retrieves active recommendations from DB or generates fresh ones using 
        Multi-Objective Course Ranking Algorithm.
        Cold-start and fallback recommendations explicitly include is_demo=True and data_source="demo".
        """
        if not force_regenerate and self.rec_repo:
            try:
                existing = await self.rec_repo.get_active_recommendations(user_id)
                if existing and len(existing) >= 6:
                    return existing
            except Exception:
                pass

        # Fetch user with enriched relationships
        user = None
        if self.user_repo:
            try:
                user = await self.user_repo.get_by_id(user_id)
            except Exception:
                user = None

        if not user:
            return self.get_fallback_recommendations(user_id)

        # Fetch latest completed diagnostic attempt
        latest_attempt = None
        if self.assess_repo:
            try:
                latest_attempt = await self.assess_repo.get_latest_completed_attempt(user_id)
            except Exception:
                latest_attempt = None
        
        # Load user competencies
        work_role_id = getattr(user, "work_role_id", None)
        user_competencies = []
        if self.comp_repo:
            try:
                if work_role_id:
                    user_competencies = await self.comp_repo.list_by_work_role(work_role_id)
                if not user_competencies:
                    user_competencies = await self.comp_repo.list_all()
            except Exception:
                user_competencies = []

        # Build deficit map from attempt or fallback to cold-start baseline
        deficit_map = {}
        n_eval_map = {}
        answer_log = getattr(latest_attempt, "answer_log", None) if latest_attempt else None
        comp_scores = None
        if isinstance(answer_log, dict):
            comp_scores = answer_log.get("competency_scores")
        elif answer_log is not None and hasattr(answer_log, "competency_scores"):
            comp_scores = getattr(answer_log, "competency_scores")
            if hasattr(comp_scores, "__dict__"):
                comp_scores = vars(comp_scores)

        is_cold_start = False
        if comp_scores:
            items = comp_scores.items() if hasattr(comp_scores, "items") else vars(comp_scores).items()
            for comp_code, score_info in items:
                if isinstance(score_info, dict):
                    dem = score_info.get("demonstrated_level", 2)
                    mand = score_info.get("mandated_level", 4)
                    def_sc = score_info.get("deficit_score", 1.5)
                    def_pct = score_info.get("deficit_pct", 37.5)
                else:
                    dem = getattr(score_info, "demonstrated_level", 2)
                    mand = getattr(score_info, "mandated_level", 4)
                    def_sc = getattr(score_info, "deficit_score", 1.5)
                    def_pct = getattr(score_info, "deficit_pct", 37.5)
                deficit_map[comp_code] = {
                    "demonstrated_level": dem,
                    "mandated_level": mand,
                    "deficit_score": def_sc,
                    "deficit_pct": def_pct,
                }
                n_eval_map[comp_code] = 5  # default items evaluated
        else:
            # Cold-start heuristic: Set default baseline levels (Demonstrated 2, Mandated 4)
            is_cold_start = True
            for c in user_competencies:
                mandated = getattr(c, "mandated_level", 4)
                code = getattr(c, "competency_code", "")
                if code:
                    deficit_map[code] = {
                        "demonstrated_level": max(1, mandated - 2),
                        "mandated_level": mandated,
                        "deficit_score": 2.0,
                        "deficit_pct": 50.0,
                    }
                    n_eval_map[code] = 2

        # Clear previous active recommendations if regenerating
        if self.rec_repo:
            try:
                await self.rec_repo.clear_user_recommendations(user_id)
            except Exception:
                pass

        # Retrieve all candidate published courses
        all_courses = []
        if self.course_repo:
            try:
                all_courses = await self.course_repo.get_all(skip=0, limit=100)
            except Exception:
                all_courses = []

        if not all_courses:
            return self.get_fallback_recommendations(user_id)

        comp_by_id = {}
        for c in user_competencies:
            cid = getattr(c, "id", None)
            if cid:
                comp_by_id[str(cid)] = c

        ranked_candidates = []

        for course in all_courses:
            course_comp_id = getattr(course, "competency_id", None)
            if not course_comp_id or str(course_comp_id) not in comp_by_id:
                continue

            comp = comp_by_id[str(course_comp_id)]
            comp_code = getattr(comp, "competency_code", "")
            comp_mandated = getattr(comp, "mandated_level", 4)
            comp_info = deficit_map.get(comp_code, {
                "demonstrated_level": 2,
                "mandated_level": comp_mandated,
                "deficit_score": 1.0,
                "deficit_pct": 25.0
            })

            demonstrated_lvl = comp_info["demonstrated_level"]
            mandated_lvl = comp_info["mandated_level"]
            deficit_pct = comp_info["deficit_pct"]
            n_eval = n_eval_map.get(comp_code, 3)

            # Prerequisite filter: Any target level should guide from demonstrated to mandated
            # Target level within [demonstrated_lvl, mandated_lvl + 1]
            course_target_level = getattr(course, "target_level", 1)
            if course_target_level < demonstrated_lvl:
                # Already mastered
                continue

            # Sub-scores
            s_def = deficit_pct / 100.0
            s_sim = self.calculate_semantic_similarity(course, comp)
            s_dur = self.calculate_duration_efficiency(getattr(course, "duration_minutes", 20))
            s_cad = self.calculate_cadre_relevance(course, user, comp, demonstrated_lvl + 1)

            # Multi-objective Course Priority Score (CPS)
            cps = (OMEGA_DEFICIT * s_def) + (OMEGA_SEMANTIC * s_sim) + (OMEGA_DURATION * s_dur) + (OMEGA_CADRE * s_cad)
            confidence = self.compute_bayesian_confidence(cps, n_eval)

            # Determine estimated improvement
            next_lvl = min(5, demonstrated_lvl + 1)
            estimated_imp = f"+1 Level (Level {demonstrated_lvl} → Level {next_lvl})"

            # Categorize into Roadmap Trajectory Stages
            course_duration = getattr(course, "duration_minutes", 20)
            if deficit_pct >= 50.0 and course_duration <= 30:
                stage = "IMMEDIATE"
            elif course_target_level <= demonstrated_lvl + 1:
                stage = "RECOMMENDED_THIS_WEEK"
            elif course_target_level > demonstrated_lvl + 1:
                stage = "ADVANCED"
            else:
                stage = "OPTIONAL_ENRICHMENT"

            rationale = self.synthesize_explainable_rationale(
                course, comp, demonstrated_lvl, mandated_lvl, deficit_pct
            )

            ranked_candidates.append({
                "course": course,
                "comp": comp,
                "cps": cps,
                "confidence": confidence,
                "deficit_score": comp_info["deficit_score"],
                "deficit_pct": deficit_pct,
                "estimated_imp": estimated_imp,
                "stage": stage,
                "rationale": rationale
            })

        # Sort strictly by CPS descending, then confidence descending
        ranked_candidates.sort(key=lambda x: (x["cps"], x["confidence"]), reverse=True)

        if not ranked_candidates:
            return self.get_fallback_recommendations(user_id)

        # Select top 12 to 16 recommendations across categories
        new_recommendations = []
        priority = 1

        for item in ranked_candidates[:16]:
            course_id = getattr(item["course"], "id", None)
            comp_id = getattr(item["comp"], "id", None)
            rec = {
                "_id": new_uuid(),
                "user_id": str(user_id),
                "course_id": str(course_id) if course_id else None,
                "competency_id": str(comp_id) if comp_id else None,
                "deficit_score": round(item["deficit_pct"], 2),
                "priority": priority,
                "confidence": item["confidence"],
                "estimated_improvement": item["estimated_imp"],
                "trajectory_stage": item["stage"],
                "explainable_rationale": item["rationale"],
                "status": "ACTIVE",
                "is_demo": is_cold_start,
                "data_source": "demo" if is_cold_start else "live",
                "generated_at": utcnow(),
            }
            new_recommendations.append(rec)
            priority += 1

        if self.rec_repo:
            try:
                await self.rec_repo.create_batch(new_recommendations)
                active_recs = await self.rec_repo.get_active_recommendations(user_id)
                if active_recs:
                    return active_recs
            except Exception:
                pass

        return self.get_fallback_recommendations(user_id)
