# ==============================================================================
# AI KARMAYOGI — iGOT KARMAYOGI COURSE SEED DATA (40 ACCREDITED COURSES)
# High-Fidelity Micro-Modules Mapped to FRAC Competencies & Government Ministries
# PyMongo AsyncMongoClient Seed Script
# ==============================================================================

import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.config import settings
from app.models.entities import new_uuid, utcnow
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

COURSES_SEED = [
    # --------------------------------------------------------------------------
    # 1. Public Procurement & GFR 2017 Compliance (COMP-GFR-01) - 6 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-GFR-101",
        "competency_code": "COMP-GFR-01",
        "title": "General Financial Rules 2017: Core Principles & Delegated Powers",
        "ministry": "Ministry of Finance (Department of Expenditure)",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["GFR 2017", "Public Finance", "Delegation of Powers", "Expenditure Control"],
        "learning_outcomes": [
            "Understand fundamental principles of government expenditure (Rule 21)",
            "Identify standard expenditure sanctions and Financial Adviser concurrence workflows",
            "Differentiate between Capital and Revenue expenditure classifications"
        ],
        "description": "Essential orientation for gazetted officers on financial propriety, canons of public spending, and financial code regulations.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-101"
    },
    {
        "igot_course_id": "IGOT-GFR-201",
        "competency_code": "COMP-GFR-01",
        "title": "Public Procurement Rulebook: Tenders, EMD & Performance Security",
        "ministry": "Ministry of Finance (Department of Expenditure)",
        "duration_minutes": 20,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Tendering", "EMD", "Performance Guarantee", "Bid Security", "GFR Rule 170"],
        "learning_outcomes": [
            "Calculate Earnest Money Deposit (EMD) and Performance Bank Guarantee requirements (Rule 170 & 171)",
            "Execute standard two-stage and two-envelope bidding systems compliant with CVC guidelines",
            "Review tender documents for transparency and non-restrictive eligibility specifications"
        ],
        "description": "Detailed procedural walkthrough of bid documentation, security deposits, and contract enforcement under GFR 2017.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-201"
    },
    {
        "igot_course_id": "IGOT-GFR-301",
        "competency_code": "COMP-GFR-01",
        "title": "Proprietary Article Certificate (PAC) & Single Tender Scrutiny",
        "ministry": "Ministry of Finance (Department of Expenditure)",
        "duration_minutes": 18,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["PAC", "Single Tender", "GFR Rule 166", "Sole Source", "Audit Defense"],
        "learning_outcomes": [
            "Apply statutory conditions for invoking PAC under GFR Rule 166 without audit objections",
            "Evaluate single bid scenarios under Rule 173(xx) to avoid arbitrary contract cancelation",
            "Formulate legally defensible procurement justifications for original equipment spare parts"
        ],
        "description": "Targeted micro-module for Section Officers and Under Secretaries handling sole-source procurement and single-bid justifications.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-301"
    },
    {
        "igot_course_id": "IGOT-GFR-401",
        "competency_code": "COMP-GFR-01",
        "title": "Contract Management, Liquidated Damages & Force Majeure in Procurement",
        "ministry": "Ministry of Finance (Department of Expenditure)",
        "duration_minutes": 35,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Contract Law", "Liquidated Damages", "Force Majeure", "Arbitration", "Dispute Resolution"],
        "learning_outcomes": [
            "Compute Liquidated Damages (LD) and extension of delivery period with denial clauses",
            "Adjudicate Force Majeure notices compliant with Department of Expenditure circulars",
            "Mitigate vendor litigation risk in multi-crore EPC and turn-key infrastructure contracts"
        ],
        "description": "Advanced executive module on enforcing contractual obligations, risk mitigation, and commercial dispute handling for Desk Officers.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-401"
    },
    {
        "igot_course_id": "IGOT-GFR-402",
        "competency_code": "COMP-GFR-01",
        "title": "Public Private Partnerships (PPP) & Complex Concession Agreements",
        "ministry": "NITI Aayog & Ministry of Finance",
        "duration_minutes": 45,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["PPP", "VGF", "Concession Agreement", "Infrastructure", "NITI Aayog"],
        "learning_outcomes": [
            "Appraise Viability Gap Funding (VGF) models and model concession agreements",
            "Structure risk allocation matrices between public authorities and private concessionaires",
            "Navigate Public Investment Board (PIB) and Expenditure Finance Committee (EFC) approvals"
        ],
        "description": "Comprehensive curriculum for senior desk officers appraising major capital projects, BOT concessions, and PPP project financing.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-402"
    },
    {
        "igot_course_id": "IGOT-GFR-501",
        "competency_code": "COMP-GFR-01",
        "title": "Strategic Procurement Governance & CVC Regulatory Oversight",
        "ministry": "Central Vigilance Commission (CVC) & DoPT",
        "duration_minutes": 50,
        "target_level": 5,
        "difficulty": "EXECUTIVE",
        "language": "English",
        "tags": ["CVC Guidelines", "Integrity Pact", "Vigilance Audit", "Procurement Reforms"],
        "learning_outcomes": [
            "Design institutional anti-corruption frameworks and mandatory Integrity Pacts",
            "Conduct systematic root-cause analyses on repetitive C&AG procurement audit queries",
            "Author department-wide procurement policy circulars in harmonization with national standards"
        ],
        "description": "Mastery program for Joint Secretaries and Directors directing ministry procurement policy, vigilance oversight, and compliance architecture.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GFR-501"
    },

    # --------------------------------------------------------------------------
    # 2. Central Secretariat File Management & CSMOP (COMP-MOP-01) - 5 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-MOP-101",
        "competency_code": "COMP-MOP-01",
        "title": "CSMOP 16th Edition: Fundamentals of Notes, Drafts & Communications",
        "ministry": "Department of Administrative Reforms and Public Grievances (DARPG)",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["CSMOP", "Noting", "Drafting", "Official Communication", "Office Procedure"],
        "learning_outcomes": [
            "Format precise official communications (Office Memorandum, D.O. Letter, Notification, Order)",
            "Structure green sheet notes with clear statement of problem, factual context, and recommended decisions",
            "Apply priority markings ('Immediate', 'Priority', 'Today') strictly according to secretariat guidelines"
        ],
        "description": "Standardized secretariat training on noting, drafting, and managing paper/electronic files according to the 16th Edition of CSMOP.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-MOP-101"
    },
    {
        "igot_course_id": "IGOT-MOP-201",
        "competency_code": "COMP-MOP-01",
        "title": "e-Office 7.0 Mastery: Lifecycle, Electronic Movements & Security",
        "ministry": "National Informatics Centre (NIC) & DARPG",
        "duration_minutes": 20,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["e-Office", "Digital Governance", "File Tracking System", "Digital Signature", "DSC"],
        "learning_outcomes": [
            "Manage electronic receipt diarisations, file creation, and hierarchical movement workflows",
            "Affix Cryptographic Digital Signature Certificates (DSC) and e-Signatures securely",
            "Inspect electronic audit trails to maintain evidentiary chain of custody for official decisions"
        ],
        "description": "Hands-on operational guidance for processing files, dispatches, and notes in the sovereign National e-Office 7.x platform.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-MOP-201"
    },
    {
        "igot_course_id": "IGOT-MOP-301",
        "competency_code": "COMP-MOP-01",
        "title": "Parliamentary Matters: Answering Starred & Unstarred Questions",
        "ministry": "Ministry of Parliamentary Affairs & Lok Sabha Secretariat",
        "duration_minutes": 25,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Parliamentary Questions", "Lok Sabha", "Rajya Sabha", "Assurances", "Starred Questions"],
        "learning_outcomes": [
            "Compile bullet-proof draft replies for Starred and Unstarred Parliamentary Questions within strict 72-hour deadlines",
            "Prepare Note for Supplementaries (NFS) anticipating oral supplementaries by Members of Parliament",
            "Track, fulfill, and drop Parliamentary Assurances before the Committee on Government Assurances"
        ],
        "description": "Critical desk procedure course for handling legislative inquiries, zero-hour mentions, and parliamentary accountability.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-MOP-301"
    },
    {
        "igot_course_id": "IGOT-MOP-401",
        "competency_code": "COMP-MOP-01",
        "title": "Cabinet Note Drafting & Inter-Ministerial Consultations",
        "ministry": "Cabinet Secretariat & DARPG",
        "duration_minutes": 35,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Cabinet Note", "Inter-Ministerial", "Legislative Drafting", "Cabinet Committee on Economic Affairs"],
        "learning_outcomes": [
            "Draft high-impact Notes for the Union Cabinet conforming to Cabinet Secretariat instructions",
            "Conduct inter-ministerial consultations and synthesize ministries' appraisal comments within 15 days",
            "Draft Statements of Objects and Reasons (SOR) for primary legislation and presidential ordinances"
        ],
        "description": "Executive masterclass on structuring Cabinet and Committee Notes for major national policies, bills, and statutory changes.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-MOP-401"
    },
    {
        "igot_course_id": "IGOT-MOP-501",
        "competency_code": "COMP-MOP-01",
        "title": "Governance Process Re-engineering & Secretariat Institutional Reform",
        "ministry": "DARPG & NITI Aayog",
        "duration_minutes": 45,
        "target_level": 5,
        "difficulty": "EXECUTIVE",
        "language": "English",
        "tags": ["BPR", "Administrative Reform", "Desk Officer System", "Work Delegation", "Civil Service Modernization"],
        "learning_outcomes": [
            "Re-engineer hierarchical departmental workflows to compress decision levels from 5 layers to 2 layers",
            "Implement paperless desk officer regimes with automated performance telemetry",
            "Benchmark administrative productivity against international civil service governance models"
        ],
        "description": "Strategic leadership curriculum on driving administrative simplification, process streamlining, and bureaucratic modernization.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-MOP-501"
    },

    # --------------------------------------------------------------------------
    # 3. Ethical Governance & Conflict of Interest (COMP-ETH-01) - 4 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-ETH-101",
        "competency_code": "COMP-ETH-01",
        "title": "CCS Conduct Rules 1964: Professional Ethics & Statutory Boundaries",
        "ministry": "Department of Personnel & Training (DoPT)",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["CCS Conduct Rules", "Ethics", "Rule 3", "Integrity", "Civil Service Code"],
        "learning_outcomes": [
            "Internalize core tenets of CCS Conduct Rule 3(1) regarding absolute integrity, devotion to duty, and non-misconduct",
            "Recognize statutory boundaries regarding gifts, hospitality, private investments, and commercial employment",
            "Uphold political neutrality and non-partisan conduct in official communications"
        ],
        "description": "Foundational civil service integrity course exploring statutory duties, code of conduct, and public accountability.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-ETH-101"
    },
    {
        "igot_course_id": "IGOT-ETH-201",
        "competency_code": "COMP-ETH-01",
        "title": "Identifying & Managing Conflicts of Interest in Tender & Committee Decisions",
        "ministry": "Central Vigilance Commission (CVC)",
        "duration_minutes": 20,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Conflict of Interest", "Recusal", "Tender Committee", "Impartiality", "Ethics in Government"],
        "learning_outcomes": [
            "Identify apparent, perceived, and real pecuniary conflicts of interest in tender and grant evaluation panels",
            "Execute formal written recusal procedures prior to opening commercial bids or selecting vendors",
            "Establish verifiable transparency safeguards in procurement and recruitment boards"
        ],
        "description": "Practical ethical dilemma analysis for committee members, scrutinizers, and procurement board officials.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-ETH-201"
    },
    {
        "igot_course_id": "IGOT-ETH-301",
        "competency_code": "COMP-ETH-01",
        "title": "Whistleblower Protection, Vigilance Mechanisms & Public Interest Disclosures",
        "ministry": "Central Vigilance Commission (CVC) & DoPT",
        "duration_minutes": 30,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Whistleblower", "PIDPI", "CVC Act", "Vigilance Enquiry", "Anti-Corruption"],
        "learning_outcomes": [
            "Handle Public Interest Disclosure and Protection of Informers (PIDPI) complaints confidentially",
            "Protect identity of whistleblowers while screening out anonymous/pseudonymous frivolous grievances",
            "Coordinate with Chief Vigilance Officers (CVO) during preliminary fact-finding inquiries"
        ],
        "description": "Operational guide on vigilance governance, anonymous complaints protocol, and statutory informant safety provisions.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-ETH-301"
    },
    {
        "igot_course_id": "IGOT-ETH-401",
        "competency_code": "COMP-ETH-01",
        "title": "Integrity Systems, Anti-Corruption Oversight & Moral Leadership",
        "ministry": "LBSNAA (DoPT)",
        "duration_minutes": 40,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Moral Leadership", "LBSNAA", "Public Trust", "Institutional Culture", "Whistleblower Redressal"],
        "learning_outcomes": [
            "Cultivate an institutional culture of transparent decision-making and resistance to external lobbying",
            "Resolve high-stakes ethical dilemmas balancing procedural adherence against humanitarian imperatives",
            "Design organizational audit and vigilance risk assessments for sensitive public offices"
        ],
        "description": "Leadership-level ethics curriculum designed by LBSNAA for directors and heads of departments navigating complex political-administrative pressures.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-ETH-401"
    },

    # --------------------------------------------------------------------------
    # 4. Citizen-Centric Public Grievance Disposal (COMP-CIT-01) - 4 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-CIT-101",
        "competency_code": "COMP-CIT-01",
        "title": "CPGRAMS 7.0: Fundamentals of Grievance Registration & Timelines",
        "ministry": "Department of Administrative Reforms and Public Grievances (DARPG)",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["CPGRAMS", "Citizen Grievance", "Public Services", "Citizen Charter"],
        "learning_outcomes": [
            "Navigate the Centralized Public Grievance Redress and Monitoring System (CPGRAMS) dashboard",
            "Adhere strictly to the mandated 21-day disposal timeline set by DARPG",
            "Correctly categorize incoming grievances across operational schemes and attached subordinate offices"
        ],
        "description": "Essential orientation on handling citizen complaints, tracking disposal SLAs, and adhering to citizen charter commitments.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-CIT-101"
    },
    {
        "igot_course_id": "IGOT-CIT-201",
        "competency_code": "COMP-CIT-01",
        "title": "Empathetic Communication & Non-Standard Grievance Resolution",
        "ministry": "DARPG & Ministry of Social Justice and Empowerment",
        "duration_minutes": 20,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Empathy", "Citizen Centricity", "Pension Grievance", "Disability Access", "Communication"],
        "learning_outcomes": [
            "Draft humane, compassionate, and clear explanatory letters to citizens avoiding cold bureaucratic jargon",
            "Expedite urgent distress grievances involving elderly pensions, emergency medical aid, and disability entitlements",
            "Coordinate cross-ministerial transfers of misdirected grievances without ping-pong rejections"
        ],
        "description": "Skill enhancement in drafting respectful citizen correspondences and resolving complex welfare/pension grievances.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-CIT-201"
    },
    {
        "igot_course_id": "IGOT-CIT-301",
        "competency_code": "COMP-CIT-01",
        "title": "Root Cause Analysis of Public Grievances & Policy Remediation",
        "ministry": "DARPG & Quality Council of India (QCI)",
        "duration_minutes": 30,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Root Cause Analysis", "QCI", "Grievance Analytics", "Feedback Loops", "Policy Reform"],
        "learning_outcomes": [
            "Perform systemic root-cause analyses on repetitive grievance clusters (e.g., PF delay, land records)",
            "Interpret Citizen Feedback Call Centre ratings and Quality Council of India (QCI) audit scores",
            "Formulate systemic circulars and software changes to eliminate chronic complaint origins"
        ],
        "description": "Advanced analytical approaches to transforming recurring public grievances into systemic administrative and software improvements.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-CIT-301"
    },
    {
        "igot_course_id": "IGOT-CIT-401",
        "competency_code": "COMP-CIT-01",
        "title": "Executive Public Grievance Governance & Service Delivery Charters",
        "ministry": "DARPG",
        "duration_minutes": 45,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Sevottam", "Service Delivery", "Appellate Authority", "Administrative Accountability"],
        "learning_outcomes": [
            "Institutionalize the Sevottam Framework for excellence in public service delivery",
            "Act as First Appellate Authority under the Grievance Redressal framework to overturn unjustified rejections",
            "Audit subordinate field office grievance disposal efficacy using algorithmic anomaly detection"
        ],
        "description": "Strategic leadership course for Directors and Nodal Grievance Officers supervising ministerial grievance ecosystems.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-CIT-401"
    },

    # --------------------------------------------------------------------------
    # 5. Right to Information & Statutory Appeals (COMP-RTI-01) - 4 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-RTI-101",
        "competency_code": "COMP-RTI-01",
        "title": "Right to Information Act 2005: Role & Duties of the CPIO",
        "ministry": "Ministry of Personnel, Public Grievances and Pensions & CIC",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["RTI Act", "CPIO", "Section 6", "Transparency", "Statutory Timelines"],
        "learning_outcomes": [
            "Master duties and liabilities of Central Public Information Officers (CPIO) under Section 5 & 6",
            "Comply with statutory timelines: 30 days for general queries, 48 hours for life or liberty emergencies",
            "Properly compute and collect RTI application and reproduction fees under DoPT fee rules"
        ],
        "description": "Statutory orientation for newly designated CPIOs and Assistant CPIOs on managing RTI requests without attracting penalties.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-RTI-101"
    },
    {
        "igot_course_id": "IGOT-RTI-201",
        "competency_code": "COMP-RTI-01",
        "title": "Exemption Clauses Under Section 8(1) & Severability Under Section 10",
        "ministry": "Central Information Commission (CIC) & Ministry of Law",
        "duration_minutes": 25,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Section 8", "Exemptions", "Commercial Confidence", "Personal Privacy", "Severability"],
        "learning_outcomes": [
            "Interpret Section 8(1)(d) commercial confidence and Section 8(1)(j) personal privacy exemptions correctly",
            "Apply Section 10 doctrine of severability to disclose non-exempt portions of official documents",
            "Formulate legally sustainable speaking rejection orders citing judicial precedents"
        ],
        "description": "Rigorous case study examination of statutory exemptions, third-party notices under Section 11, and judicial rulings.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-RTI-201"
    },
    {
        "igot_course_id": "IGOT-RTI-301",
        "competency_code": "COMP-RTI-01",
        "title": "Defending Appeals Before the First Appellate Authority & Central Information Commission",
        "ministry": "Central Information Commission (CIC)",
        "duration_minutes": 30,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["CIC Hearing", "Appeals", "Section 19", "Section 20 Penalties", "Legal Defense"],
        "learning_outcomes": [
            "Conduct First Appeal hearings under Section 19(1) as an independent quasi-judicial authority",
            "Prepare official affidavits and defense statements for Central Information Commission (CIC) second appeals",
            "Protect the department from personal Section 20 monetary penalties for non-supply of data"
        ],
        "description": "Comprehensive guide for appellate authorities and CPIOs to draft quasi-judicial appeal orders and represent ministries before the CIC.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-RTI-301"
    },
    {
        "igot_course_id": "IGOT-RTI-401",
        "competency_code": "COMP-RTI-01",
        "title": "Proactive Disclosure Under Section 4 & Institutional Open Data Strategies",
        "ministry": "DARPG & Ministry of Electronics and IT (MeitY)",
        "duration_minutes": 35,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Section 4", "Suo Motu Disclosure", "Open Data", "Transparency Audit", "CIC Audit"],
        "learning_outcomes": [
            "Formulate proactive Suo Motu disclosure packages under Section 4(1)(b) on departmental portals",
            "Achieve top scores in annual Third-Party Transparency Audits commissioned by the CIC",
            "Automate open dataset publishing on data.gov.in to curtail redundant individual RTI queries"
        ],
        "description": "Executive policy module on moving from reactive information supply to proactive digital transparency regimes.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-RTI-401"
    },

    # --------------------------------------------------------------------------
    # 6. Establishment Rules & Disciplinary Proceedings (COMP-EST-01) - 4 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-EST-101",
        "competency_code": "COMP-EST-01",
        "title": "Fundamental Rules & Supplementary Rules (FRSR): Leave, Pay & LTC",
        "ministry": "Department of Personnel & Training (DoPT)",
        "duration_minutes": 20,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["FRSR", "Leave Rules", "LTC", "Pay Fixation", "Service Book"],
        "learning_outcomes": [
            "Calculate leave entitlements (Earned Leave, Half Pay Leave, Child Care Leave) under CCS (Leave) Rules 1972",
            "Process Leave Travel Concession (LTC) claims verifying approved travel modes and airfare guidelines",
            "Maintain service books, pay fixation entries, and annual increment determinations accurately"
        ],
        "description": "Operational grounding in civil service establishment matters, entitlements, and statutory employee benefits.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-EST-101"
    },
    {
        "igot_course_id": "IGOT-EST-201",
        "competency_code": "COMP-EST-01",
        "title": "CCS (CCA) Rules 1965: Drafting Charge Sheets for Minor & Major Penalties",
        "ministry": "DoPT & UPSC",
        "duration_minutes": 30,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["CCS CCA Rules", "Charge Sheet", "Rule 14", "Rule 16", "Disciplinary Action"],
        "learning_outcomes": [
            "Distinguish between Minor Penalty (Rule 16) and Major Penalty (Rule 14) proceedings",
            "Draft Articles of Charge, Statement of Imputations, List of Documents, and List of Witnesses with evidentiary rigor",
            "Prevent procedural infirmities that cause tribunals and High Courts to quash disciplinary inquiries"
        ],
        "description": "Mastery of disciplinary proceedings documentation, formulation of charge memos, and compliance with natural justice.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-EST-201"
    },
    {
        "igot_course_id": "IGOT-EST-301",
        "competency_code": "COMP-EST-01",
        "title": "Role & Procedure of the Inquiry Officer & Presenting Officer",
        "ministry": "DoPT (Institute of Secretariat Training and Management - ISTM)",
        "duration_minutes": 35,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Inquiry Officer", "Presenting Officer", "Oral Inquiry", "Natural Justice", "ISTM"],
        "learning_outcomes": [
            "Conduct oral inquiry hearings adhering to principles of natural justice and fair trial",
            "Execute examination, cross-examination, and re-examination of official and defense witnesses",
            "Author an unbiased, evidence-based Inquiry Report evaluating charges without prejudice"
        ],
        "description": "Practical simulation course by ISTM on presiding over departmental inquiries and representing administration as Presenting Officer.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-EST-301"
    },
    {
        "igot_course_id": "IGOT-EST-401",
        "competency_code": "COMP-EST-01",
        "title": "Disciplinary Authority Adjudication & UPSC Consultation Protocols",
        "ministry": "DoPT & Union Public Service Commission (UPSC)",
        "duration_minutes": 45,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Disciplinary Authority", "UPSC Consultation", "Speaking Order", "Central Administrative Tribunal"],
        "learning_outcomes": [
            "Draft independent Speaking Final Orders accepting or dissenting from Inquiry Officer findings",
            "Execute mandatory consultations with the Union Public Service Commission (UPSC) under Article 320(3)(c)",
            "Defend administration actions before the Central Administrative Tribunal (CAT) in service jurisprudence"
        ],
        "description": "Executive curriculum for Disciplinary Authorities evaluating inquiry reports and pronouncing statutory penalties.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-EST-401"
    },

    # --------------------------------------------------------------------------
    # 7. Government e-Marketplace (GeM) Bidding (COMP-GEM-01) - 4 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-GEM-101",
        "competency_code": "COMP-GEM-01",
        "title": "GeM Portal Operations: Direct Purchase, L-1 Comparison & Orders",
        "ministry": "Ministry of Commerce & Industry (GeM SPV)",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["GeM", "Direct Purchase", "L-1", "CRAC", "Government e-Marketplace"],
        "learning_outcomes": [
            "Execute direct purchases up to ₹25,000 on GeM with verified vendor verification",
            "Perform automated L-1 price comparisons for purchases between ₹25,000 and ₹5,000,000 across 3 manufacturers",
            "Generate Consignee Receipt and Acceptance Certificate (CRAC) within 10 days of physical delivery"
        ],
        "description": "Hands-on operational training on navigating the GeM portal, placing orders, and generating payment receipts.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GEM-101"
    },
    {
        "igot_course_id": "IGOT-GEM-201",
        "competency_code": "COMP-GEM-01",
        "title": "GeM Customized Bidding & Reverse Auctions for Complex Services",
        "ministry": "Ministry of Commerce & Industry (GeM SPV)",
        "duration_minutes": 25,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["GeM Bidding", "Reverse Auction", "Service Procurement", "SLA Drafting"],
        "learning_outcomes": [
            "Float customized electronic bids and electronic Reverse Auctions (e-RA) on GeM",
            "Structure clear Service Level Agreements (SLAs) for manpower, catering, security, and facility management",
            "Evaluate technical parameters objectively without creating vendor-specific brand restrictive clauses"
        ],
        "description": "Advanced procurement methodology for floating electronic tenders and conducting dynamic reverse auctions on GeM.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GEM-201"
    },
    {
        "igot_course_id": "IGOT-GEM-301",
        "competency_code": "COMP-GEM-01",
        "title": "GeM Contract Incident Management, Vendor Debarment & Quality Rejections",
        "ministry": "Ministry of Commerce & Industry (GeM SPV) & Ministry of Finance",
        "duration_minutes": 30,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Incident Management", "Vendor Rating", "Debarment", "Blacklisting", "Quality Audit"],
        "learning_outcomes": [
            "Raise and escalate contractual Incident Management flags on GeM for delivery default or substandard goods",
            "Execute vendor rating deductions and initiate formal debarment/blacklisting proceedings under GFR Rule 151",
            "Manage goods rejection, vendor appeal handling, and alternative risk purchases at seller's cost"
        ],
        "description": "Critical dispute handling and vendor compliance enforcement protocols on the sovereign GeM portal.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GEM-301"
    },
    {
        "igot_course_id": "IGOT-GEM-401",
        "competency_code": "COMP-GEM-01",
        "title": "Strategic GeM Procurement Planning & Public Expenditure Optimization",
        "ministry": "GeM SPV & Department of Expenditure",
        "duration_minutes": 40,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["GeM Strategy", "Spend Analytics", "Annual Procurement Plan", "MSME Procurement Policy"],
        "learning_outcomes": [
            "Formulate Annual Procurement Plans aggregating departmental demands to achieve bulk economies of scale",
            "Enforce mandatory 25% procurement quotas from Micro & Small Enterprises (MSEs) including SC/ST and women entrepreneurs",
            "Audit departmental GeM purchase patterns to eliminate artificial splitting of contract sanctions"
        ],
        "description": "Strategic institutional procurement course for Head of Department (HOD) and senior financial advisers.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-GEM-401"
    },

    # --------------------------------------------------------------------------
    # 8. Budget Monitoring & Re-appropriation (COMP-BUD-01) - 4 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-BUD-101",
        "competency_code": "COMP-BUD-01",
        "title": "PFMS 101: Public Financial Management System & Expenditure Filing",
        "ministry": "Controller General of Accounts (CGA) & Ministry of Finance",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["PFMS", "CGA", "DDO Module", "EAT Module", "Public Financial Management"],
        "learning_outcomes": [
            "Operate PFMS Drawing and Disbursing Officer (DDO) and Program Division (PD) modules",
            "Track Expenditure, Advance, and Transfer (EAT) flows for central sector schemes",
            "Generate Electronic Payment Orders (EPO) and reconcile monthly treasury expenditure statements"
        ],
        "description": "Standardized operational course on navigating the sovereign PFMS portal for fund sanctioning and disbursals.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-BUD-101"
    },
    {
        "igot_course_id": "IGOT-BUD-201",
        "competency_code": "COMP-BUD-01",
        "title": "Monthly Expenditure Plans (MEP) & Quarterly Expenditure Limits (QEL)",
        "ministry": "Ministry of Finance (Department of Economic Affairs - Budget Division)",
        "duration_minutes": 20,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Budget Monitoring", "MEP", "QEL", "Rush of Expenditure", "Rule 62"],
        "learning_outcomes": [
            "Monitor scheme fund burn rates against approved Monthly Expenditure Plans (MEP)",
            "Enforce Quarterly Expenditure Limits (QEL) to prevent the rush of expenditure in March (GFR Rule 62)",
            "Draft formal justifications for relaxed cash management guidelines before the Budget Division"
        ],
        "description": "Essential financial discipline course on cash flow smoothing, pace of spending, and preventing fiscal year-end rushes.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-BUD-201"
    },
    {
        "igot_course_id": "IGOT-BUD-301",
        "competency_code": "COMP-BUD-01",
        "title": "Budget Re-appropriation, Revised Estimates (RE) & Supplementary Demands",
        "ministry": "Department of Economic Affairs & Department of Expenditure",
        "duration_minutes": 30,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Re-appropriation", "Revised Estimates", "Supplementary Demands for Grants", "Appropriation Act"],
        "learning_outcomes": [
            "Execute legal re-appropriation of budget savings across sub-heads within delegated powers",
            "Prepare data-backed Revised Estimates (RE) and Budget Estimates (BE) for annual Parliamentary submission",
            "Draft Proposals for Supplementary Demands for Grants distinguishing between Token, Technical, and Substantive grants"
        ],
        "description": "Advanced financial administration course on managing mid-year fiscal reallocations and parliamentary grant revisions.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-BUD-301"
    },
    {
        "igot_course_id": "IGOT-BUD-401",
        "competency_code": "COMP-BUD-01",
        "title": "Utilization Certificates (UCs), SNA Governance & DBT Public Spending Control",
        "ministry": "Ministry of Finance & DBT Mission (Cabinet Secretariat)",
        "duration_minutes": 45,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Utilization Certificate", "GFR 238", "SNA", "Single Nodal Agency", "DBT"],
        "learning_outcomes": [
            "Enforce strict GFR Rule 238(1) compliance requiring Form GFR 12-A Utilization Certificates before subsequent releases",
            "Monitor state treasury fund transfers via the Single Nodal Agency (SNA) zero-balance account dashboard",
            "Audit Direct Benefit Transfer (DBT) beneficiary seeding to eliminate leakages in centrally sponsored welfare schemes"
        ],
        "description": "Executive curriculum for Section Officers and Under Secretaries tracking grants-in-aid to state governments, autonomous bodies, and NGOs.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-BUD-401"
    },

    # --------------------------------------------------------------------------
    # 9. Evidence-Based Scrutiny & Fact Analysis (COMP-DEC-01) - 4 Courses
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-DEC-101",
        "competency_code": "COMP-DEC-01",
        "title": "Fact Scrutiny & File Investigation: Analyzing Precedents & Audit History",
        "ministry": "Institute of Secretariat Training and Management (ISTM)",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["Fact Analysis", "Precedent Scrutiny", "Administrative Evidence", "File History"],
        "learning_outcomes": [
            "Verify factual assertions and cross-check historical file references before putting up notes",
            "Distinguish between binding administrative precedents and distinguishable past exceptions",
            "Extract pertinent data points from multi-volume historical docket files systematically"
        ],
        "description": "Core cognitive skills training for Section Officers and Assistant Section Officers in objective factual verification.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-DEC-101"
    },
    {
        "igot_course_id": "IGOT-DEC-201",
        "competency_code": "COMP-DEC-01",
        "title": "Data-Driven Public Policy Evaluation & Dashboard Telemetry",
        "ministry": "NITI Aayog & Ministry of Statistics and Programme Implementation (MoSPI)",
        "duration_minutes": 25,
        "target_level": 2,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Data Analytics", "Policy Evaluation", "KPI Dashboards", "NITI Aayog", "Evidence-Based Governance"],
        "learning_outcomes": [
            "Utilize quantitative indicators and dashboard metrics to evaluate welfare scheme performance",
            "Conduct basic statistical trend analysis to detect emerging district-level operational bottlenecks",
            "Synthesize data visualisations into actionable executive briefing memos for senior leadership"
        ],
        "description": "Skill building in using statistical indicators, district ranking dashboards, and data analytics in policy review.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-DEC-201"
    },
    {
        "igot_course_id": "IGOT-DEC-301",
        "competency_code": "COMP-DEC-01",
        "title": "Complex Administrative Fact-Finding & Preliminary Inquiries",
        "ministry": "DoPT & Central Bureau of Investigation (CBI Academy)",
        "duration_minutes": 35,
        "target_level": 3,
        "difficulty": "INTERMEDIATE",
        "language": "English",
        "tags": ["Fact Finding", "Preliminary Inquiry", "Administrative Investigation", "Evidence Preservation"],
        "learning_outcomes": [
            "Structure and execute comprehensive administrative preliminary inquiries into procedural lapses",
            "Corroborate documentary evidence against witness depositions to establish objective timelines",
            "Draft impartial Preliminary Inquiry Reports without speculative or unsubstantiated conclusions"
        ],
        "description": "Techniques for conducting rigorous administrative inquiries, document seizures, and fact verification.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-DEC-301"
    },
    {
        "igot_course_id": "IGOT-DEC-401",
        "competency_code": "COMP-DEC-01",
        "title": "Strategic Decision Science & Crisis Governance for Senior Administrators",
        "ministry": "LBSNAA & National Disaster Management Authority (NDMA)",
        "duration_minutes": 45,
        "target_level": 4,
        "difficulty": "ADVANCED",
        "language": "English",
        "tags": ["Decision Science", "Crisis Governance", "Strategic Planning", "Heuristics", "Administrative Leadership"],
        "learning_outcomes": [
            "Navigate high-uncertainty crisis situations applying structured decision frameworks",
            "Overcome bureaucratic cognitive biases (status-quo bias, sunk cost fallacy, groupthink)",
            "Coordinate inter-agency emergency responses balancing rapid delivery with accountability"
        ],
        "description": "Executive decision-making course from LBSNAA on high-stakes crisis response, risk-taking, and strategic leadership.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-DEC-401"
    },

    # --------------------------------------------------------------------------
    # 10. Audit Paras & PAC Recommendations Resolution (COMP-AUD-01) - 1 Course
    # --------------------------------------------------------------------------
    {
        "igot_course_id": "IGOT-AUD-101",
        "competency_code": "COMP-AUD-01",
        "title": "Government Audit Architecture: Role of C&AG, DGACR & Internal Audit",
        "ministry": "Comptroller and Auditor General of India (C&AG)",
        "duration_minutes": 15,
        "target_level": 1,
        "difficulty": "FOUNDATION",
        "language": "Bilingual (Hindi/English)",
        "tags": ["Audit", "C&AG", "Audit Paras", "Internal Audit", "Public Accountability"],
        "learning_outcomes": [
            "Understand the constitutional mandate of the C&AG under Articles 148-151 of the Constitution",
            "Distinguish between Compliance Audit, Financial Audit, and Performance Audit queries",
            "Comply with initial audit memos during on-site inspections within 24 to 48 hours"
        ],
        "description": "Foundational grounding in public audit mechanisms, C&AG entry/exit conferences, and audit memo handling.",
        "course_url": "https://igotkarmayogi.gov.in/learn/course/IGOT-AUD-101"
    }
]

# Canonical Competency ID mapping from seed_assessment.py
CANONICAL_COMPETENCY_IDS = {
    "COMP-GFR-01": "44444444-4444-4444-4444-444444444401",
    "COMP-MOP-01": "44444444-4444-4444-4444-444444444402",
    "COMP-ETH-01": "44444444-4444-4444-4444-444444444403",
    "COMP-CIT-01": "44444444-4444-4444-4444-444444444404",
    "COMP-RTI-01": "44444444-4444-4444-4444-444444444405",
    "COMP-EST-01": "44444444-4444-4444-4444-444444444406",
    "COMP-GEM-01": "44444444-4444-4444-4444-444444444407",
    "COMP-BUD-01": "44444444-4444-4444-4444-444444444408",
    "COMP-DEC-01": "44444444-4444-4444-4444-444444444409",
    "COMP-AUD-01": "44444444-4444-4444-4444-444444444410",
}


async def seed_database(db=None):
    owns_client = False
    client = None
    if db is None:
        print(f"[AI Karmayogi] Connecting to MongoDB: {settings.MONGODB_DATABASE}...")
        client = AsyncMongoClient(settings.MONGODB_URI, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)
        db = client[settings.MONGODB_DATABASE]
        owns_client = True

    print("\n--- Seeding AI Karmayogi 40+ iGOT-Style Courses ---")

    # Load existing competencies from MongoDB
    comp_cursor = db["competencies"].find({})
    comp_docs = await comp_cursor.to_list(length=None)
    competencies = {c["competency_code"]: str(c["_id"]) for c in comp_docs if "competency_code" in c}
    print(f"Loaded {len(competencies)} existing FRAC Competencies from database.")

    seeded_count = 0
    updated_count = 0

    for c_data in COURSES_SEED:
        comp_id = competencies.get(c_data["competency_code"]) or CANONICAL_COMPETENCY_IDS.get(c_data["competency_code"])
        if not comp_id:
            print(f"Warning: Competency {c_data['competency_code']} not found for course {c_data['igot_course_id']}")
            continue

        existing = await db["courses"].find_one({"igot_course_id": c_data["igot_course_id"]})

        if existing:
            await db["courses"].update_one(
                {"_id": existing["_id"]},
                {
                    "$set": {
                        "title": c_data["title"],
                        "description": c_data["description"],
                        "ministry": c_data["ministry"],
                        "duration_minutes": c_data["duration_minutes"],
                        "target_level": c_data["target_level"],
                        "difficulty": c_data["difficulty"],
                        "language": c_data["language"],
                        "tags": c_data["tags"],
                        "learning_outcomes": c_data["learning_outcomes"],
                        "course_url": c_data["course_url"],
                        "competency_id": comp_id,
                        "competency_code": c_data["competency_code"],
                        "is_published": True,
                        "updated_at": utcnow(),
                    }
                },
            )
            updated_count += 1
        else:
            course_doc = {
                "_id": new_uuid(),
                "competency_id": comp_id,
                "competency_code": c_data["competency_code"],
                "igot_course_id": c_data["igot_course_id"],
                "title": c_data["title"],
                "description": c_data["description"],
                "ministry": c_data["ministry"],
                "duration_minutes": c_data["duration_minutes"],
                "target_level": c_data["target_level"],
                "difficulty": c_data["difficulty"],
                "language": c_data["language"],
                "tags": c_data["tags"],
                "learning_outcomes": c_data["learning_outcomes"],
                "course_url": c_data["course_url"],
                "is_published": True,
                "created_at": utcnow(),
                "updated_at": utcnow(),
            }
            await db["courses"].insert_one(course_doc)
            seeded_count += 1

    print(f"Successfully seeded {seeded_count} new courses, updated {updated_count} courses (Total: {len(COURSES_SEED)}).")
    if owns_client and client:
        await client.close()


seed_courses = seed_database
run_seed = seed_database

if __name__ == "__main__":
    asyncio.run(seed_database())
