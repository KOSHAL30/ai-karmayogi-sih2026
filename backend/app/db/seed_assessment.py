# ==============================================================================
# AI KARMAYOGI — ASSESSMENT SEED DATA (30 REALISTIC GOVERNMENT SCENARIOS)
# FRAC Competencies & Psychometric MCQs Aligned with GFR 2017, CSMOP, CCS Rules, & GeM
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

# 1. FRAC Competencies definitions across 3 Work Roles
COMPETENCIES_SEED = [
    # Work Role 1: Under Secretary (Desk Officer)
    {
        "_id": "44444444-4444-4444-4444-444444444401",
        "role_code": "WBR-DESK-OFFICER",
        "competency_type": "FUNCTIONAL",
        "competency_code": "COMP-GFR-01",
        "competency_name": "Public Procurement & GFR 2017 Compliance",
        "mandated_level": 4,
        "description": "Applies Rule 149 (GeM), Rule 166 (Proprietary Article), and financial thresholds with precision.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444402",
        "role_code": "WBR-DESK-OFFICER",
        "competency_type": "FUNCTIONAL",
        "competency_code": "COMP-MOP-01",
        "competency_name": "Central Secretariat File Management & CSMOP",
        "mandated_level": 4,
        "description": "Proficiency in noting, drafting, e-Office lifecycle, and parliamentary question replies.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444403",
        "role_code": "WBR-DESK-OFFICER",
        "competency_type": "BEHAVIORAL",
        "competency_code": "COMP-ETH-01",
        "competency_name": "Ethical Governance & Conflict of Interest",
        "mandated_level": 4,
        "description": "Upholds transparency, impartiality, and zero tolerance for conflict of interest under CCS Conduct Rules.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444404",
        "role_code": "WBR-DESK-OFFICER",
        "competency_type": "BEHAVIORAL",
        "competency_code": "COMP-CIT-01",
        "competency_name": "Citizen-Centric Public Grievance Disposal",
        "mandated_level": 3,
        "description": "Prioritizes prompt public grievance redressal on CPGRAMS and proactive citizen communication.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444405",
        "role_code": "WBR-DESK-OFFICER",
        "competency_type": "DOMAIN",
        "competency_code": "COMP-RTI-01",
        "competency_name": "Right to Information & Statutory Appeals",
        "mandated_level": 3,
        "description": "Interprets RTI exemptions under Section 8(1) and complies with CIC statutory timelines.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444406",
        "role_code": "WBR-DESK-OFFICER",
        "competency_type": "DOMAIN",
        "competency_code": "COMP-EST-01",
        "competency_name": "Establishment Rules & Disciplinary Proceedings",
        "mandated_level": 3,
        "description": "Adjudicates fundamental rules, leave sanction, and disciplinary proceedings under CCS (CCA) Rules.",
    },
    # Work Role 2: Section Officer
    {
        "_id": "44444444-4444-4444-4444-444444444407",
        "role_code": "WBR-SECTION-OFFICER",
        "competency_type": "FUNCTIONAL",
        "competency_code": "COMP-GEM-01",
        "competency_name": "Government e-Marketplace (GeM) Bidding",
        "mandated_level": 4,
        "description": "Direct purchase, L-1 bidding, custom catalogue creation, and CRAC receipt generation.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444408",
        "role_code": "WBR-SECTION-OFFICER",
        "competency_type": "FUNCTIONAL",
        "competency_code": "COMP-BUD-01",
        "competency_name": "Budget Monitoring & Re-appropriation",
        "mandated_level": 3,
        "description": "Monitors monthly expenditure plan (MEP), re-appropriation, and utilization certificates.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444409",
        "role_code": "WBR-SECTION-OFFICER",
        "competency_type": "BEHAVIORAL",
        "competency_code": "COMP-DEC-01",
        "competency_name": "Evidence-Based Scrutiny & Fact Analysis",
        "mandated_level": 3,
        "description": "Extracts key legal precedents and audit objections from complex historical records.",
    },
    {
        "_id": "44444444-4444-4444-4444-444444444410",
        "role_code": "WBR-SECTION-OFFICER",
        "competency_type": "DOMAIN",
        "competency_code": "COMP-AUD-01",
        "competency_name": "Audit Paras & PAC Recommendations Resolution",
        "mandated_level": 3,
        "description": "Formulates Action Taken Notes (ATNs) addressing C&AG audit inspection reports.",
    },
]

# 2. 30 Realistic Assessment Scenario Questions
QUESTIONS_SEED = [
    # 1. GFR Procurement (Recall)
    {
        "competency_code": "COMP-GFR-01",
        "bloom_level": "REMEMBER",
        "stem": "[Office Memorandum Scenario - GeM Procurement Thresholds]\nUnder General Financial Rules (GFR) 2017, Rule 149(i), what is the maximum monetary threshold up to which an authorized officer can make direct purchases on the Government e-Marketplace (GeM) without comparative quotation, subject to reasonable quality and price?",
        "options": [
            {"id": "A", "text": "Up to ₹10,000 through any available supplier on GeM"},
            {"id": "B", "text": "Up to ₹25,000 through any of the available suppliers on GeM meeting requisites"},
            {"id": "C", "text": "Up to ₹50,000 provided financial concurrence of IFD is obtained"},
            {"id": "D", "text": "Up to ₹1,00,000 provided the vendor is MSME certified"}
        ],
        "correct_index": 1,
        "rationale": "As per Rule 149(i) of GFR 2017, direct purchase up to ₹25,000 can be made through any of the available suppliers on the GeM portal, meeting the requisite quality, specification and delivery period.",
        "citation": "GFR 2017, Rule 149(i) & DoPT Procurement Guidelines"
    },
    # 2. GFR Procurement (Application)
    {
        "competency_code": "COMP-GFR-01",
        "bloom_level": "APPLY",
        "stem": "[DDO Case Study - Single Bidder Scenario]\nA division floats an open tender for cloud hardware migration on GeM with an estimated value of ₹45 Lakhs. Upon bid opening, only one valid technical bid is received. The project deadline is 3 weeks away. How must the Procurement Committee proceed under GFR Rule 173(xx)?",
        "options": [
            {"id": "A", "text": "Instantly cancel the tender and re-invite bids across national newspapers."},
            {"id": "B", "text": "Award the contract immediately if the single price bid is within 10% of estimated cost."},
            {"id": "C", "text": "Scrutinize bid conditions for restrictive clauses; if procurement was transparent, competitive and price is fair, single bid may be considered with competent authority approval."},
            {"id": "D", "text": "Invoke Proprietary Article Certificate (PAC) post-facto to regularize single bid."}
        ],
        "correct_index": 2,
        "rationale": "Under GFR Rule 173(xx) and Manual for Procurement of Goods (Para 5.6.6), receipt of a single bid does not automatically invalidate the tender. If requirements were widely publicized, qualification criteria non-restrictive, and prices fair, single bid may be accepted with approval of Competent Authority and IFD concurrence.",
        "citation": "GFR 2017 Rule 173(xx) & Ministry of Finance Procurement Manual"
    },
    # 3. GFR Procurement (Scenario-Based Analysis)
    {
        "competency_code": "COMP-GFR-01",
        "bloom_level": "ANALYZE",
        "stem": "[Secretariat Docket - Proprietary Article Certificate (PAC)]\nA technical wing proposes purchasing specialized software updates worth ₹12 Lakhs from an original equipment manufacturer (OEM) invoking PAC under GFR Rule 166. Upon examining the file, the Under Secretary notes that alternative third-party tools exist that offer 90% interoperability at half the cost. What is the legally sound administrative advice?",
        "options": [
            {"id": "A", "text": "Clear the file without queries because the user wing has sovereign prerogative over software choice."},
            {"id": "B", "text": "Return the file requesting an objective market benchmarking note and justification why functional alternatives cannot fulfill operational requirements before invoking Rule 166."},
            {"id": "C", "text": "Reject the proposal permanently and refer the technical officer to Vigilance for procedural violation."},
            {"id": "D", "text": "Advise splitting the sanction into three ₹4 Lakh purchase orders to bypass tender requirements."}
        ],
        "correct_index": 1,
        "rationale": "PAC under Rule 166 requires certification that only this particular firm can manufacture or deliver the item and no other alternative is acceptable. The Under Secretary must uphold fiduciary duty by seeking explicit justification and market benchmarking before processing single-source PAC.",
        "citation": "GFR 2017 Rule 166 & CVC Guidelines on Proprietary Procurement"
    },
    # 4. CSMOP File Management (Recall)
    {
        "competency_code": "COMP-MOP-01",
        "bloom_level": "REMEMBER",
        "stem": "[CSMOP 16th Edition - Urgency Labeling Standards]\nAccording to the Central Secretariat Manual of Office Procedure (CSMOP), within what statutory timeline must an official file bearing an 'IMMEDIATE' priority label be disposed of by a desk?",
        "options": [
            {"id": "A", "text": "Within 2 hours of receipt by the concerned Section"},
            {"id": "B", "text": "Within 24 hours of receipt, or before close of the next working day"},
            {"id": "C", "text": "Within 7 calendar days"},
            {"id": "D", "text": "Within 3 working days"}
        ],
        "correct_index": 1,
        "rationale": "CSMOP classifies urgency labels: 'Immediate' signifies cases that should be attended to within 24 hours or before close of the next working day. 'Most Immediate' requires disposal on the same day.",
        "citation": "CSMOP 16th Edition, Chapter 8 (Priority Marking)"
    },
    # 5. CSMOP File Management (Application)
    {
        "competency_code": "COMP-MOP-01",
        "bloom_level": "APPLY",
        "stem": "[Parliamentary Assurance - Starred Question File Preparation]\nA Lok Sabha Starred Question regarding rural digital kiosks is admitted for oral reply in 48 hours. A critical data point from a State Mission Directorate is contradictory. How should the Under Secretary construct the Notes for Supplementary (NFS)?",
        "options": [
            {"id": "A", "text": "Conceal the contradiction to avoid embarrassing the Minister on the floor of the House."},
            {"id": "B", "text": "Include the verified central figures in the main reply, highlight the state discrepancy in the NFS with an explanatory background note, and prepare a contingency briefing for supplementary queries."},
            {"id": "C", "text": "Request the Lok Sabha Secretariat to defer the question indefinitely due to missing data."},
            {"id": "D", "text": "Transfer the entire Starred Question to another Ministry without inter-ministerial consultation."}
        ],
        "correct_index": 1,
        "rationale": "CSMOP rules on Parliamentary business dictate absolute factual integrity. Contradictions or caveats must be explicitly analyzed in the 'Notes for Supplementaries' (NFS) so that the Minister is completely briefed on potential supplementary inquiries.",
        "citation": "CSMOP Chapter 13 (Parliamentary Procedures)"
    },
    # 6. CSMOP File Management (Analysis)
    {
        "competency_code": "COMP-MOP-01",
        "bloom_level": "ANALYZE",
        "stem": "[e-Office Note Sheet Integrity Dilemma]\nA draft cabinet note is circulated in e-Office. A senior officer instructs an Assistant Section Officer to physically delete and replace a previous dissenting minute recorded by the Internal Financial Advisor (IFA). As Under Secretary scrutinizing the e-file, what is the mandatory protocol?",
        "options": [
            {"id": "A", "text": "Delete the IFA minute using administrator privileges as instructed."},
            {"id": "B", "text": "Affirm that e-Office maintains an immutable audit trail; the IFA minute cannot be expunged. The administrative section must record its counter-reasoning in a subsequent note for decision by the Secretary."},
            {"id": "C", "text": "Create a new duplicate file and abandon the existing e-file record entirely."},
            {"id": "D", "text": "Mark the entire file confidential to conceal the disagreement from future audit scrutiny."}
        ],
        "correct_index": 1,
        "rationale": "Under CSMOP and Central Government e-Office protocols, notes once digitally signed and committed are immutable and part of the permanent sovereign record. Differing opinions must be constructively addressed through supplementary reasoning rather than alteration.",
        "citation": "CSMOP Para 7.8 (Recording of Notes) & NIC e-Office Security Architecture"
    },
    # 7. Ethical Governance (Recall)
    {
        "competency_code": "COMP-ETH-01",
        "bloom_level": "REMEMBER",
        "stem": "[CCS Conduct Rules 1964 - Rule 3(1)]\nRule 3(1) of the Central Civil Services (Conduct) Rules 1964 mandates that every government servant shall at all times maintain:",
        "options": [
            {"id": "A", "text": "Strict neutrality only during election periods"},
            {"id": "B", "text": "Absolute integrity, devotion to duty, and do nothing which is unbecoming of a Government servant"},
            {"id": "C", "text": "Compliance with executive orders regardless of statutory legality"},
            {"id": "D", "text": "Confidentiality of all office matters even when summoned by statutory courts"}
        ],
        "correct_index": 1,
        "rationale": "Rule 3(1) of CCS (Conduct) Rules, 1964 states: Every Government servant shall at all times (i) maintain absolute integrity; (ii) maintain devotion to duty; and (iii) do nothing which is unbecoming of a Government servant.",
        "citation": "Central Civil Services (Conduct) Rules, 1964, Rule 3(1)"
    },
    # 8. Ethical Governance (Application)
    {
        "competency_code": "COMP-ETH-01",
        "bloom_level": "APPLY",
        "stem": "[Conflict of Interest - Tender Evaluation Board]\nAn Under Secretary is nominated as member of a Technical Tender Evaluation Committee. During vendor pre-qualification, the officer notices that one of the consortium partners is headed by their first cousin. The officer has not interacted with the cousin in two years. What action is mandated under CCS Conduct Rules?",
        "options": [
            {"id": "A", "text": "Remain on the committee since the cousin is only a partner, not the sole proprietor."},
            {"id": "B", "text": "Submit a formal written recusal disclosure to the Chairman of the Committee and Head of Department, seeking replacement to preserve institutional neutrality."},
            {"id": "C", "text": "Award lowest marks to the cousin's consortium to prove impartial standing."},
            {"id": "D", "text": "Recuse informally by abstaining from attendance on the day of scoring."}
        ],
        "correct_index": 1,
        "rationale": "Public procurement integrity rules and CCS Conduct Rules mandate that any actual or potential conflict of interest must be disclosed formally in writing immediately, followed by official recusal to eliminate perception of bias.",
        "citation": "CVC Vigilance Manual & DoPT OM No. 11013/4/2011-Estt.(A)"
    },
    # 9. Ethical Governance (Scenario Analysis)
    {
        "competency_code": "COMP-ETH-01",
        "bloom_level": "ANALYZE",
        "stem": "[Post-Retirement Employment & Commercial Association]\nA retiring Joint Secretary approaches the Under Secretary to expedite the processing of a consultancy tender in which an agency that recently offered post-retirement employment to the Joint Secretary is a lead bidder. What is the ethical and procedural imperative for the Under Secretary?",
        "options": [
            {"id": "A", "text": "Expedite the file promptly out of respect for hierarchical seniority."},
            {"id": "B", "text": "Process the file strictly on merits according to standard chronological queue, document all procedural compliances, and immediately flag the conflict of interest to the Chief Vigilance Officer (CVO)."},
            {"id": "C", "text": "Leak the tender documents to the press to halt the award anonymously."},
            {"id": "D", "text": "Delay the file intentionally until after the Joint Secretary's date of superannuation without noting reasons."}
        ],
        "correct_index": 1,
        "rationale": "Civil servants must maintain absolute integrity and resist undue influence. Factual processing according to rules, transparency, and reporting potential vigilance conflicts to the CVO protects both the officer and public interest.",
        "citation": "Prevention of Corruption Act 1988 (Amended 2018) & CVC Guidelines"
    },
    # 10. Citizen Grievance (Recall)
    {
        "competency_code": "COMP-CIT-01",
        "bloom_level": "REMEMBER",
        "stem": "[DARPG Guidelines - CPGRAMS Disposal Timeline]\nUnder the latest Department of Administrative Reforms and Public Grievances (DARPG) standardized guidelines, what is the maximum prescribed timeline for grievance redressal on the CPGRAMS portal?",
        "options": [
            {"id": "A", "text": "Within 21 days (reduced from 30 days)"},
            {"id": "B", "text": "Within 60 calendar days"},
            {"id": "C", "text": "Within 90 calendar days"},
            {"id": "D", "text": "Within 7 working days"}
        ],
        "correct_index": 0,
        "rationale": "DARPG circular OM No. S-15/21/2021-O/o DS(PG)-DARPG revised the maximum standard grievance redressal period to 21 days, emphasizing proactive, speaking-order disposals.",
        "citation": "DARPG Office Memorandum on CPGRAMS Redressal Norms"
    },
    # 11. Citizen Grievance (Application)
    {
        "competency_code": "COMP-CIT-01",
        "bloom_level": "APPLY",
        "stem": "[Senior Citizen Pension Grievance]\nA 78-year-old retired official lodges a CPGRAMS grievance stating that their revised pension arrears have been withheld for 9 months due to an untraceable physical service book between two merging Directorates. The Dealing Assistant proposes issuing a generic interim reply. As Under Secretary, what is the empathetic administrative direction?",
        "options": [
            {"id": "A", "text": "Approve the generic interim reply stating 'Matter is under active consideration'."},
            {"id": "B", "text": "Close the grievance on CPGRAMS immediately and advise the citizen to approach the Central Administrative Tribunal (CAT)."},
            {"id": "C", "text": "Convene an inter-directorate nodal meeting within 48 hours to reconstruct the service records based on duplicate salary slips, authorize provisional pension, and issue a speaking order."},
            {"id": "D", "text": "Impose a penalty on the pensioner for not retaining their original service book."}
        ],
        "correct_index": 2,
        "rationale": "Citizen-centricity under Mission Karmayogi requires proactive resolution of citizen hardships. Generic closure is unacceptable under DARPG guidelines; officers are empowered to reconstruct records and authorize provisional relief under CCS (Pension) Rules.",
        "citation": "DARPG Standard Operating Procedures for Grievance Redressal & CCS (Pension) Rules"
    },
    # 12. Citizen Grievance (Analysis)
    {
        "competency_code": "COMP-CIT-01",
        "bloom_level": "ANALYZE",
        "stem": "[Systemic Grievance Root Cause Analysis]\nAnalysis of a Ministry's CPGRAMS dashboard indicates that 62% of grievances in the past quarter pertain to delay in scholarship disbursements for underprivileged students. What systemic intervention should the administrative section recommend to the Senior Management?",
        "options": [
            {"id": "A", "text": "Deploy more staff to draft replies to individual grievances on the portal."},
            {"id": "B", "text": "Conduct a Business Process Re-engineering (BPR) study of the disbursement pipeline, transition to API-based Direct Benefit Transfer (DBT) verification, and institute an automated milestone tracking dashboard."},
            {"id": "C", "text": "Disable online grievance filing during peak disbursement months."},
            {"id": "D", "text": "Outsource the entire grievance handling mechanism to a third-party call center without administrative access."}
        ],
        "correct_index": 1,
        "rationale": "Effective public administration addresses root causes rather than symptoms. High grievance clusters signal procedural bottlenecks requiring Business Process Re-engineering (BPR) and technological integration (DBT/PFMS).",
        "citation": "Capacity Building Commission (CBC) Citizen-Centric Governance Module"
    },
    # 13. RTI Act (Recall)
    {
        "competency_code": "COMP-RTI-01",
        "bloom_level": "REMEMBER",
        "stem": "[RTI Act 2005 - Life or Liberty Exemption Timeline]\nUnder Section 7(1) of the Right to Information Act 2005, if the information sought concerns the 'life or liberty' of an individual, within what timeframe must the Central Public Information Officer (CPIO) provide the information?",
        "options": [
            {"id": "A", "text": "Within 24 hours of receipt of the request"},
            {"id": "B", "text": "Within 48 hours of receipt of the request"},
            {"id": "C", "text": "Within 5 calendar days"},
            {"id": "D", "text": "Within 10 working days"}
        ],
        "correct_index": 1,
        "rationale": "Section 7(1) proviso of RTI Act 2005 stipulates that where information sought concerns the life or liberty of a person, the same shall be provided within forty-eight hours of the receipt of the request.",
        "citation": "Right to Information Act 2005, Section 7(1)"
    },
    # 14. RTI Act (Application)
    {
        "competency_code": "COMP-RTI-01",
        "bloom_level": "APPLY",
        "stem": "[CPIO Dilemma - Third Party Commercial Information]\nAn RTI applicant requests the itemized unit-cost breakup and proprietary technical schematics submitted by a winning defense telecom vendor in a closed tender. The vendor formally objects under Section 11(1). How must the CPIO adjudicate the disclosure?",
        "options": [
            {"id": "A", "text": "Disclose all blueprints immediately since the contract has already been awarded and paid for."},
            {"id": "B", "text": "Deny disclosure under Section 8(1)(d) (Commercial Confidence & Trade Secrets) unless a larger public interest that outweighs commercial harm is explicitly demonstrated."},
            {"id": "C", "text": "Transfer the RTI application to the vendor for direct response to the citizen."},
            {"id": "D", "text": "Burn the records under departmental archive destruction policies."}
        ],
        "correct_index": 1,
        "rationale": "Section 8(1)(d) of RTI Act 2005 exempts information including commercial confidence, trade secrets or intellectual property, the disclosure of which would harm competitive position, unless competent authority is satisfied that larger public interest warrants disclosure.",
        "citation": "RTI Act 2005, Section 8(1)(d) & Section 11"
    },
    # 15. RTI Act (Analysis)
    {
        "competency_code": "COMP-RTI-01",
        "bloom_level": "ANALYZE",
        "stem": "[Section 8(1)(j) Personal Information vs Public Interest]\nAn applicant seeks copies of the Annual Performance Assessment Reports (APARs) and medical reimbursement claims of five Section Officers in a Department, alleging promotions were biased. As First Appellate Authority (FAA), how should you rule?",
        "options": [
            {"id": "A", "text": "Order unconditional disclosure of all APARs and medical invoices to promote complete openness."},
            {"id": "B", "text": "Uphold exemption under Section 8(1)(j) as APARs and personal medical records are personal information without proven public interest, as settled by the Supreme Court in Girish Ramchandra Deshpande."},
            {"id": "C", "text": "Direct the CPIO to furnish handwritten summaries omitting names."},
            {"id": "D", "text": "Direct the applicant to pay a penalty of ₹50,000 for filing a vexatious appeal."}
        ],
        "correct_index": 1,
        "rationale": "Supreme Court of India in Girish Ramchandra Deshpande vs CIC (2012) held that performance appraisals and personal service records of an employee are personal information exempted under Section 8(1)(j) of RTI Act, unless overriding public interest is established.",
        "citation": "Supreme Court Ruling in Girish Ramchandra Deshpande (2012) & RTI Act Section 8(1)(j)"
    },
    # 16. Establishment & Disciplinary Rules (Recall)
    {
        "competency_code": "COMP-EST-01",
        "bloom_level": "REMEMBER",
        "stem": "[CCS (CCA) Rules 1965 - Rule 14 & 16 Distinction]\nUnder the Central Civil Services (Classification, Control and Appeal) Rules 1965, which procedural rule governs the institution of formal inquiry for imposing 'Major Penalties'?",
        "options": [
            {"id": "A", "text": "Rule 11 (List of Penalties)"},
            {"id": "B", "text": "Rule 14 (Procedure for imposing major penalties)"},
            {"id": "C", "text": "Rule 16 (Procedure for imposing minor penalties)"},
            {"id": "D", "text": "Rule 19 (Special procedure in certain cases)"}
        ],
        "correct_index": 1,
        "rationale": "Rule 14 of CCS (CCA) Rules, 1965 specifies the detailed multi-stage procedure for imposing major penalties, including framing Article of Charges, appointment of Inquiring Authority and Presenting Officer.",
        "citation": "CCS (CCA) Rules 1965, Rule 14"
    },
    # 17. Establishment Rules (Application)
    {
        "competency_code": "COMP-EST-01",
        "bloom_level": "APPLY",
        "stem": "[LTC Discrepancy & Fraud Investigation]\nAn official submits a Leave Travel Concession (LTC) claim for self and family with boarding passes from a private travel portal instead of authorized travel agents (Balmer Lawrie, Ashok Travels, IRCTC). Furthermore, flight fare is 30% higher than Air India LTC-80 rates. How should the Under Secretary handle the claim?",
        "options": [
            {"id": "A", "text": "Pass the bill in full to avoid employee dissatisfaction."},
            {"id": "B", "text": "Restrict reimbursement strictly to authorized agent rates or lowest applicable slab, seek explanation for non-compliance with DoPT mandatory agent guidelines, and refer to IFD."},
            {"id": "C", "text": "Immediately dismiss the employee without opportunity of being heard."},
            {"id": "D", "text": "Request the employee to submit altered receipts dated prior to the journey."}
        ],
        "correct_index": 1,
        "rationale": "DoPT OM mandates purchase of flight tickets through authorized travel agents only. In case of non-compliance, financial sanction must be restricted to lowest permissible entitlement, with inquiry into potential fraudulent intent before settlement.",
        "citation": "DoPT OM No. 31011/12/2022-Estt.A-IV (Air Travel on LTC)"
    },
    # 18. Establishment Rules (Analysis)
    {
        "competency_code": "COMP-EST-01",
        "bloom_level": "ANALYZE",
        "stem": "[Unauthorized Absence & Dies Non Determination]\nAn employee has remained absent without sanctioned leave for 45 consecutive days despite two registered directives to resume duties. The section proposes treating the entire period as 'Dies Non'. What are the exact administrative and service consequences of invoking Dies Non?",
        "options": [
            {"id": "A", "text": "It results in automatic termination of service under Article 311 of the Constitution."},
            {"id": "B", "text": "The period does not count as service for pension, increment, or leave calculation, but does not constitute a break in service unless specifically ordered by the Disciplinary Authority."},
            {"id": "C", "text": "It entitles the employee to full subsistence allowance for the duration."},
            {"id": "D", "text": "It converts the absence into earned leave automatically."}
        ],
        "correct_index": 1,
        "rationale": "Dies Non under Fundamental Rule 17-A implies a day that does not count for any service benefits (pay, pension, increment), but does not wipe out past qualifying service unless distinct break in service is ordered following due process.",
        "citation": "Fundamental Rules (FR 17-A) & DoPT Establishment Guidelines"
    },
    # 19. GeM Operations (Recall)
    {
        "competency_code": "COMP-GEM-01",
        "bloom_level": "REMEMBER",
        "stem": "[GeM Portal - CRAC Generation Timeline]\nUpon delivery of goods at the consignee site on GeM, within how many days must the Consignee Receipt and Acceptance Certificate (CRAC) be generated to trigger payments to the supplier?",
        "options": [
            {"id": "A", "text": "Within 2 working days"},
            {"id": "B", "text": "Within 10 calendar days of physical delivery"},
            {"id": "C", "text": "Within 30 days"},
            {"id": "D", "text": "Within 45 days after final internal audit clearance"}
        ],
        "correct_index": 1,
        "rationale": "GeM guidelines mandate that the consignee must issue the CRAC within 10 days of goods delivery. Failure to do so results in auto-generation of CRAC to ensure prompt payments to MSMEs.",
        "citation": "GeM Special Terms and Conditions (STC) Para 12"
    },
    # 20. GeM Operations (Application)
    {
        "competency_code": "COMP-GEM-01",
        "bloom_level": "APPLY",
        "stem": "[Custom Catalogue vs Standard GeM Category]\nA Section Officer is tasked with procuring specialized interactive touch displays with bespoke multilingual voice-assist software for a training academy. The exact item is not catalogued on GeM. How should the procurement proceed according to Department of Expenditure OMs?",
        "options": [
            {"id": "A", "text": "Procure from local offline open market immediately without GeM interface."},
            {"id": "B", "text": "Utilize the 'Custom Bid' or 'BoQ' feature on GeM after obtaining a non-availability certificate / GeM Availability Report (GAR) ID."},
            {"id": "C", "text": "Modify the functional requirement to match an obsolete existing product on GeM."},
            {"id": "D", "text": "Purchase hardware from GeM and software from an unregistered vendor in cash."}
        ],
        "correct_index": 1,
        "rationale": "Department of Expenditure OM mandates generation of GeM Availability Report and Non-Availability Certificate (GAR&NAC). If goods/services are not available, buyers must use Custom Bid / BoQ feature on GeM portal or obtain exemption before open tender.",
        "citation": "Ministry of Finance OM No. F.6/18/2019-PPD on GeM Procurement"
    },
    # 21. Budget Monitoring (Recall)
    {
        "competency_code": "COMP-BUD-01",
        "bloom_level": "REMEMBER",
        "stem": "[GFR Rule 67 - Rush of Expenditure in March]\nUnder GFR 2017 Rule 67(1), the rush of expenditure, particularly in the closing month of the financial year (March), is regarded as a breach of financial regularity. What is the standard ceiling prescribed for expenditure in the last quarter (Q4)?",
        "options": [
            {"id": "A", "text": "Expenditure in March should not exceed 10% and in Q4 should not exceed 33% of Revised Estimates (RE)"},
            {"id": "B", "text": "Expenditure in Q4 can be up to 75% of budget allocation"},
            {"id": "C", "text": "There are no restrictions provided funds do not lapse"},
            {"id": "D", "text": "Entire budget must be surrendered by February 15"}
        ],
        "correct_index": 0,
        "rationale": "Ministry of Finance guidelines and GFR Rule 67 stipulate that expenditure in the last quarter (Jan-March) should not exceed 33% of the budget allocation, and in March alone should not exceed 10-15% of RE to prevent fiscal rush.",
        "citation": "GFR 2017 Rule 67 & Ministry of Finance Cash Management Circular"
    },
    # 22. Budget Monitoring (Application)
    {
        "competency_code": "COMP-BUD-01",
        "bloom_level": "APPLY",
        "stem": "[Re-Appropriation of Funds - Legal Constraints]\nA division faces an anticipated deficit of ₹50 Lakhs under 'Salaries' (Voted) due to recent dearness allowance hikes, while having surplus savings of ₹60 Lakhs under 'Capital Outlay'. Can the Section Officer propose re-appropriating funds from Capital to Revenue (Salaries)?",
        "options": [
            {"id": "A", "text": "Yes, re-appropriation between any heads is permitted with Joint Secretary approval."},
            {"id": "B", "text": "No, re-appropriation from Capital to Revenue head or between Charged and Voted heads is strictly prohibited under financial delegation rules."},
            {"id": "C", "text": "Yes, provided the funds are utilized before March 31st."},
            {"id": "D", "text": "Yes, if the Comptroller and Auditor General issues an oral clearance."}
        ],
        "correct_index": 1,
        "rationale": "Article 114(3) of the Constitution and Delegation of Financial Powers Rules (DFPR) strictly prohibit re-appropriation of funds from a Capital Grant to a Revenue Grant or vice versa, and between Voted and Charged items without Parliament's supplementary grant.",
        "citation": "Delegation of Financial Powers Rules (DFPR), Rule 10 & GFR Rule 61"
    },
    # 23. Fact Analysis & Scrutiny (Analysis)
    {
        "competency_code": "COMP-DEC-01",
        "bloom_level": "ANALYZE",
        "stem": "[Audit Objection Scrutiny - Price Variation Clause]\nA road construction contractor submits a price escalation claim of ₹2.4 Crores citing sudden international crude bitumen price inflation. The agreement is a standard item-rate contract containing a Price Variation Clause (PVC) with base indices tied to the Wholesale Price Index (WPI). The contractor substituted global spot market prices in their formula. As Section Officer reviewing the bill, what is the finding?",
        "options": [
            {"id": "A", "text": "Admit the claim because crude oil is imported and global spot prices reflect real commercial distress."},
            {"id": "B", "text": "Reject the substitution; escalation must be strictly computed using the contractually mandated WPI index series published by the Office of the Economic Adviser for the specified reference period."},
            {"id": "C", "text": "Cancel the entire contract for fraudulent calculation without notice."},
            {"id": "D", "text": "Split the difference 50-50 as an ex-gratia compromise."}
        ],
        "correct_index": 1,
        "rationale": "Administrative contracts are legally binding instruments. Escalation calculations must adhere strictly to the agreed contractual formula and authoritative official indices (WPI/CPI). Unilateral substitution of indices violates financial sanctity.",
        "citation": "CPWD Works Manual & GFR 2017 Rule 225"
    },
    # 24. Audit Paras & PAC Resolution (Recall)
    {
        "competency_code": "COMP-AUD-01",
        "bloom_level": "REMEMBER",
        "stem": "[Public Accounts Committee (PAC) - Action Taken Note (ATN) Deadline]\nWhat is the statutory timeline within which a Ministry/Department is required to furnish Action Taken Notes (ATNs) to the Monitoring Cell on audit paragraphs included in the C&AG Report tabled in Parliament?",
        "options": [
            {"id": "A", "text": "Within 4 months of the tabling of the C&AG Report"},
            {"id": "B", "text": "Within 12 months"},
            {"id": "C", "text": "Within 15 days"},
            {"id": "D", "text": "Within 3 years"}
        ],
        "correct_index": 0,
        "rationale": "Committee on Public Accounts (PAC) guidelines mandate that Action Taken Notes on audit paragraphs appearing in C&AG reports must be submitted to the PAC Secretariat/Monitoring Cell within 4 months of tabling.",
        "citation": "Public Accounts Committee (PAC) Procedural Directives"
    },
    # 25. Audit Paras (Application)
    {
        "competency_code": "COMP-AUD-01",
        "bloom_level": "APPLY",
        "stem": "[Settlement of C&AG Audit Para on Unfruitful Expenditure]\nA C&AG draft audit para highlights 'Unfruitful expenditure of ₹3.8 Crores' on an automated telemetry laboratory that remained non-operational for two years due to lack of three-phase power supply. How should the Section Officer formulate the Action Taken Note (ATN)?",
        "options": [
            {"id": "A", "text": "Deny all allegations and state that C&AG lacks technical jurisdiction over lab installations."},
            {"id": "B", "text": "Acknowledge the inter-agency coordination lapse, detail remedial commissioning of the dedicated power substation with operational logs, fix administrative accountability for oversight, and request dropping of the para."},
            {"id": "C", "text": "Surrender the laboratory machinery as scrap to close the physical audit trail."},
            {"id": "D", "text": "Keep the file pending until the audit officers rotate to another assignment."}
        ],
        "correct_index": 1,
        "rationale": "A compliant Action Taken Note requires: (1) factual position acknowledgment, (2) verification of corrective measures taken to operationalize assets, (3) fixation of administrative responsibility for lapse, and (4) preventive guidelines to avoid recurrence.",
        "citation": "Monitoring Cell Guidelines on C&AG Audit Paragraph Disposal"
    },
    # 26. GFR Evaluation (Evaluate)
    {
        "competency_code": "COMP-GFR-01",
        "bloom_level": "EVALUATE",
        "stem": "[Liquidated Damages vs Force Majeure Adjudication]\nA vendor delivering national census tablets delays supply by 90 days beyond the contractual delivery date, invoking Force Majeure due to localized semiconductor factory shutdowns abroad. The contract provides for Liquidated Damages (LD) at 0.5% per week up to 10%. As Desk Officer evaluating the claim, how should you balance legal equity and government interest?",
        "options": [
            {"id": "A", "text": "Waive LD unconditionally because supply chain disruptions are universally acknowledged."},
            {"id": "B", "text": "Review if the vendor gave timely statutory notice of Force Majeure within the contractual window (e.g. 10 days of event), verify certified proof, and if valid, grant extension of delivery period (EDP) without LD, otherwise impose LD."},
            {"id": "C", "text": "Terminate the contract immediately and confiscate the vendor's bank accounts without notice."},
            {"id": "D", "text": "Double the LD penalty to 20% to deter future delays."}
        ],
        "correct_index": 1,
        "rationale": "Force Majeure clauses require prompt formal notification with documentary evidence from competent authorities (e.g. Chamber of Commerce). If procedural criteria are met, extension without LD is granted; if not, LD must be levied as per contract.",
        "citation": "Manual for Procurement of Goods 2022, Para 9.7.9 (Force Majeure & LD)"
    },
    # 27. CSMOP Drafting (Evaluate)
    {
        "competency_code": "COMP-MOP-01",
        "bloom_level": "EVALUATE",
        "stem": "[Inter-Ministerial Cabinet Note Drafting Protocol]\nA Ministry prepares a Cabinet Note proposing amendments to the National Cyber Security Directive. The Department of Legal Affairs and Ministry of Finance raise reservations during circulation. How should the administrative desk finalize the Cabinet Note for the Cabinet Secretariat?",
        "options": [
            {"id": "A", "text": "Remove the opposing comments of Legal Affairs and Finance to present a harmonious proposal."},
            {"id": "B", "text": "Incorporate the verbatim comments of Ministry of Finance and Legal Affairs in a dedicated paragraph ('Views of Consulted Ministries'), state the sponsoring Ministry's counter-comments, and submit the balanced note."},
            {"id": "C", "text": "Bypass Cabinet approval and issue the directive via an executive gazette notification."},
            {"id": "D", "text": "Submit the note directly to the Prime Minister's Office without Cabinet Secretariat routing."}
        ],
        "correct_index": 1,
        "rationale": "Cabinet Secretariat instructions (Handbook on Cabinet Notes) mandate that views of all consulted Ministries—including dissenting perspectives—must be explicitly presented alongside the sponsoring Ministry's rejoinder to enable informed collective cabinet decision-making.",
        "citation": "Cabinet Secretariat Handbook on Preparation of Notes for the Cabinet"
    },
    # 28. Ethical Governance (Evaluate)
    {
        "competency_code": "COMP-ETH-01",
        "bloom_level": "EVALUATE",
        "stem": "[Whistleblower Disclosure & Vigilance Protection]\nA young contractual programmer reveals to the Under Secretary concrete digital proof that a private software vendor is deliberately siphoning beneficiary Aadhaar data onto an unencrypted commercial server. The Project Director instructs the Under Secretary to bury the complaint. What is the lawful course of action under the Whistle Blowers Protection Act?",
        "options": [
            {"id": "A", "text": "Comply with the Project Director to preserve employment harmony."},
            {"id": "B", "text": "Instantly preserve digital forensic evidence, report the unauthorized breach to the Chief Vigilance Officer (CVO) and CERT-In, and extend institutional confidentiality and protection to the whistleblower."},
            {"id": "C", "text": "Advise the programmer to sell the data to a cybersecurity research firm."},
            {"id": "D", "text": "Terminate the contractual programmer for unauthorized database access."}
        ],
        "correct_index": 1,
        "rationale": "Whistleblower protection and CERT-In mandatory incident reporting guidelines obligate public officials to safeguard sensitive citizen data, prevent corruption, protect the disclosure source, and notify statutory vigilance and cyber emergency channels.",
        "citation": "Whistle Blowers Protection Act 2014 & Information Technology Act (CERT-In Rules)"
    },
    # 29. Citizen Grievance (Evaluate)
    {
        "competency_code": "COMP-CIT-01",
        "bloom_level": "EVALUATE",
        "stem": "[Public Service Delivery Benchmark - Citizen Charter Audit]\nA field office reports 99% grievance disposal on paper within the 21-day timeline, but random telephone audits by the Quality Council of India (QCI) reveal that 70% of citizens report their problems were unresolved and closed with stock phrases. How should the Supervisory Officer evaluate this finding?",
        "options": [
            {"id": "A", "text": "Commend the field office for achieving 99% statistical compliance on the IT dashboard."},
            {"id": "B", "text": "Classify the disposals as superficial 'statistical compliance'; issue directives that closures must be backed by verifiable speaking orders, and tie officer performance ratings to citizen feedback satisfaction scores."},
            {"id": "C", "text": "Cancel the QCI third-party audit agreement to eliminate negative reports."},
            {"id": "D", "text": "Block citizens who gave negative feedback from filing future CPGRAMS grievances."}
        ],
        "correct_index": 1,
        "rationale": "Under Mission Karmayogi's outcome-based governance model, process metrics without citizen satisfaction represent administrative failure. DARPG directives mandate qualitative review, speaking orders, and citizen satisfaction ratings as the true metric of performance.",
        "citation": "DARPG Guidelines on Qualitative Disposal of Public Grievances"
    },
    # 30. RTI Disclosure (Evaluate)
    {
        "competency_code": "COMP-RTI-01",
        "bloom_level": "EVALUATE",
        "stem": "[Section 4 Proactive Disclosure Compliance]\nA citizen files 40 separate RTI applications every month asking for routine expenditure details of a public sector undertaking. The CPIO proposes rejecting all applications as 'frivolous and vexatious'. As First Appellate Authority, what systemic directive should you issue?",
        "options": [
            {"id": "A", "text": "Issue an order barring the citizen from invoking the RTI Act forever."},
            {"id": "B", "text": "Direct the immediate proactive digital publishing of all procurement and expenditure records under Section 4(1)(b) of the RTI Act on the official website, rendering repetitive requests unnecessary."},
            {"id": "C", "text": "File a police complaint against the applicant for obstructing government work."},
            {"id": "D", "text": "Double the photocopy fee to ₹50 per page to discourage the citizen."}
        ],
        "correct_index": 1,
        "rationale": "The Central Information Commission and DoPT have repeatedly emphasized that widespread proactive disclosure under Section 4(1)(b) of the RTI Act eliminates the need for repetitive individual requests and fosters transparent administrative governance.",
        "citation": "DoPT OM No. 1/6/2011-IR (Implementation of Section 4 of RTI Act 2005)"
    }
]


async def seed_database(db=None):
    owns_client = False
    client = None
    if db is None:
        print(f"[AI Karmayogi] Connecting to MongoDB: {settings.MONGODB_DATABASE}...")
        client = AsyncMongoClient(settings.MONGODB_URI, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)
        db = client[settings.MONGODB_DATABASE]
        owns_client = True

    print("[AI Karmayogi] Starting assessment & FRAC competency seed...")

    # 1. Fetch Work Roles to bind competencies
    role_map = {
        "WBR-DESK-OFFICER": "33333333-3333-3333-3333-333333333301",
        "WBR-SECTION-OFFICER": "33333333-3333-3333-3333-333333333302",
    }
    for r_code in ["WBR-DESK-OFFICER", "WBR-SECTION-OFFICER"]:
        res = await db["work_roles"].find_one({"role_code": r_code})
        if res:
            role_map[r_code] = str(res["_id"])

    # 2. Seed FRAC Competencies
    comp_map = {}
    for comp_data in COMPETENCIES_SEED:
        existing = await db["competencies"].find_one({"competency_code": comp_data["competency_code"]})
        wr_id = role_map.get(comp_data["role_code"])

        if not existing:
            new_comp = {
                "_id": comp_data["_id"],
                "work_role_id": wr_id,
                "role_code": comp_data["role_code"],
                "competency_type": comp_data["competency_type"],
                "competency_name": comp_data["competency_name"],
                "competency_code": comp_data["competency_code"],
                "mandated_level": comp_data["mandated_level"],
                "description": comp_data["description"],
                "created_at": utcnow(),
                "updated_at": utcnow(),
            }
            await db["competencies"].insert_one(new_comp)
            comp_map[comp_data["competency_code"]] = comp_data["_id"]
            print(f"  + Added FRAC Competency: {comp_data['competency_code']} - {comp_data['competency_name']}")
        else:
            comp_map[comp_data["competency_code"]] = str(existing["_id"])

    # 3. Fetch Admin user for quiz author attribution
    admin_user = await db["users"].find_one({})
    admin_id = str(admin_user["_id"]) if admin_user else "00000000-0000-0000-0000-000000000003"

    # 4. Seed Master Diagnostic Quiz
    quiz_id = "55555555-5555-5555-5555-555555555501"
    quiz = await db["quizzes"].find_one({"_id": quiz_id})

    if not quiz:
        quiz_doc = {
            "_id": quiz_id,
            "created_by": admin_id,
            "title": "Mission Karmayogi Role-Based Diagnostic Assessment",
            "quiz_type": "DIAGNOSTIC",
            "passing_percentage": 60,
            "status": "PUBLISHED",
            "created_at": utcnow(),
            "updated_at": utcnow(),
        }
        await db["quizzes"].insert_one(quiz_doc)
        print("  + Added Master Diagnostic Quiz Container")

    # 5. Seed 30 Assessment Questions
    for idx, q_data in enumerate(QUESTIONS_SEED, start=1):
        comp_id = comp_map.get(q_data["competency_code"])
        q_id = f"66666666-6666-6666-6666-{idx:012d}"

        existing_q = await db["questions"].find_one({"_id": q_id})

        if not existing_q:
            new_q = {
                "_id": q_id,
                "quiz_id": quiz_id,
                "competency_id": comp_id,
                "competency_code": q_data["competency_code"],
                "question_stem": q_data["stem"],
                "bloom_level": q_data["bloom_level"],
                "options": q_data["options"],
                "correct_option_index": q_data["correct_index"],
                "pedagogical_rationale": q_data["rationale"],
                "source_citation": q_data["citation"],
                "created_at": utcnow(),
                "updated_at": utcnow(),
            }
            await db["questions"].insert_one(new_q)
            print(f"  + Added Question {idx:02d} [{q_data['bloom_level']}]: {q_data['competency_code']}")

    print("[AI Karmayogi] Assessment seed completed successfully with 30 realistic questions!")
    if owns_client and client:
        await client.close()


seed_assessment = seed_database
run_seed = seed_database

if __name__ == "__main__":
    asyncio.run(seed_database())
