# AI Karmayogi — 5-Minute SIH 2026 Presentation Script

**Project Title:** AI-Enabled Competency Diagnostic & Personalized Training Ecosystem for Mission Karmayogi  
**Problem Statement ID:** `SIH26101`  
**Target Audience:** Smart India Hackathon Jury, Ministry of Personnel / DoPT Observers, Capacity Building Commission (CBC) Representatives  
**Presentation Duration:** Exactly 5 Minutes (300 Seconds)

---

## Pre-Demo Setup Checklist (1 Minute Before Going on Stage)
1. Ensure the stack is running: `run.bat` or `docker compose up -d`.
2. Open browser to `http://localhost`.
3. Press `Ctrl + Shift + D` to verify the **SIH Evaluator Demo Cockpit** is responsive.
4. Set browser to full-screen mode (`F11`).

---

## ⏱️ Minute-by-Minute Demonstration Roadmap

| Timestamp | Phase | Presenter Focus | Screen Action |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:45** | **The National Problem & Sovereign Solution** | The Challenge of Civil Service Training | Landing Page (`/`) |
| **0:45 – 1:45** | **Competency Diagnostic & FRAC Gap Heatmap** | Adaptive Assessment & 3-Pillar Measurement | Diagnostic Player (`/assessment/take`) & Result (`/assessment/result/1`) |
| **1:45 – 2:45** | **Explainable iGOT Recommendation Engine** | Gap-to-Course Mapping & 4-Week Roadmap | Recommendations (`/recommendations`) & Timeline (`/learning-path`) |
| **2:45 – 3:45** | **Sovereign PDF Intelligence, RAG & MCQ Studio** | Ingestion of GFR 2017 & Automated Quizzes | Trainer Studio (`/trainer/documents`) |
| **3:45 – 4:30** | **Executive Telemetry & Cadre Heatmap** | 12 Departments, 10-Axis Radar & Monitoring | Executive Dashboard (`/admin`) & Heatmap (`/admin/departments`) |
| **4:30 – 5:00** | **Cryptographic Credentials & Closing** | Verifiable Credentials & SIH Impact | Certificate Vault (`/certificates`) & Print Modal |

---

## Detailed Script & Live Screen Directions

### [0:00 – 0:45] The Problem & The Sovereign Vision (45 Seconds)

**What to Show on Screen:**
- Main Landing Screen (`http://localhost/`).
- Show the national tricolor sovereign banner, the 3 role archetypes, and press `Ctrl + K` to demonstrate the **Spotlight Command Palette**.

**What to Say:**
> *"Respected Jury Members, India has over 3 million civil servants driving public governance. Under Mission Karmayogi, the government envisioned a transition from 'rule-based' to 'role-based' capacity building.*
> 
> *However, today departments face three critical bottlenecks: First, training is static and one-size-fits-all rather than diagnostic. Second, competency gaps across Behavioral, Functional, and Domain pillars are never quantified. Third, converting complex statutory circulars and Office Memorandums into actionable assessments takes weeks of manual faculty effort.*
> 
> *We present **AI Karmayogi** — a 100% sovereign, self-hosted AI ecosystem that diagnoses competency gaps, maps explainable learning roadmaps to the iGOT Karmayogi repository, and auto-generates statutory assessments from government PDFs with zero external cloud dependencies."*

---

### [0:45 – 1:45] Competency Diagnostic & FRAC Gap Heatmap (60 Seconds)

**What to Show on Screen:**
- Press `Ctrl + Shift + D` (opens Demo Cockpit), click **Rajesh Kumar (Learner)**.
- Navigate to **Assessments** (`/assessment/take`).
- Answer 2 scenario questions on Public Procurement (GFR 2017 Rule 149).
- Show the **Assessment Result & FRAC Heatmap** (`/assessment/result/1`).

**What to Say:**
> *"Let us experience the platform through the eyes of our learner, Shri Rajesh Kumar, an Under Secretary in DoPT.*
> 
> *Instead of generic multiple-choice quizzes, Rajesh faces an adaptive scenario-based assessment mapped directly to the FRAC framework. As he answers questions on Public Procurement and GFR 2017, the engine dynamically adjusts difficulty and measures his decision-making.*
> 
> *Upon submission, look at this instant diagnostic output: The system doesn't just give a percentage score — it generates a granular 3-Pillar Competency Profile. Rajesh scores 82% in Interpersonal Behavioral skills, but the AI highlights an acute 40% deficit in Functional Public Procurement, specifically under Rule 149 for GeM procurement.*
> 
> *Every single score is explainable, grounded in official work-role mandates."*

---

### [1:45 – 2:45] Explainable iGOT Recommendation Engine & 4-Week Roadmap (60 Seconds)

**What to Show on Screen:**
- Navigate to **Recommendations** (`/recommendations`).
- Highlight the **Deficit-to-Course Rationale Badge** on the top card: *"Prescribed to close 40.0% deficit in Public Procurement & GeM"*.
- Click **View 4-Week Structured Trajectory** (`/learning-path`).

**What to Say:**
> *"How does AI Karmayogi bridge this gap? It immediately activates our Explainable Recommendation Engine.*
> 
> *Unlike conventional platforms that simply sort by popular courses, our algorithm calculates the exact deficit delta between Rajesh's demonstrated proficiency and his mandated work-role benchmark.*
> 
> *Notice the course recommendation: 'GFR 2017 & GeM Masterclass'. The AI explicitly states the pedagogical rationale: 'Prescribed to close 40.0% capability gap in Public Procurement'.*
> 
> *Moving to the **4-Week Structured Roadmap**, the platform organizes learning into digestible weekly micro-milestones that fit into a busy civil servant's schedule, projecting a +18.5% competency uplift upon completion. No commercial cloud APIs are called; the ranking and path generation occur in real-time in milliseconds using local algorithms."*

---

### [2:45 – 3:45] Sovereign PDF Intelligence, Local RAG & MCQ Studio (60 Seconds)

**What to Show on Screen:**
- Press `Ctrl + Shift + D`, switch to **Dr. Sunita Deshmukh (Trainer)**.
- Navigate to **Trainer Studio** (`/trainer/documents`).
- Select the pre-loaded statutory document: `General Financial Rules 2017 (GFR 2017)`.
- In RAG Chat, enter query: *"What is the mandatory threshold for procurement through GeM under Rule 149?"*
- Click on the **MCQ Studio** tab and show the Bloom's Taxonomy-classified questions with distractor rationales.

**What to Say:**
> *"Now let's view the platform from the perspective of our training faculty, Dr. Sunita Deshmukh at ISTM.*
> 
> *Government trainers routinely deal with 200-page gazette notifications, circulars, and manuals. Here, Dr. Deshmukh uploads an official government PDF. Our PyMuPDF structural extractor parses the text while preserving statutory hierarchies — Act, Chapter, Rule, and Clause.*
> 
> *Let's ask the sovereign RAG engine a statutory question: 'What is the mandatory threshold for procurement through GeM under Rule 149?'*
> 
> *Look at the output: Local Qwen3 synthesizes a precise answer with zero hallucinations, complete with exact citations: Rule 149(i), Page 48. Clicking the citation immediately scrolls the viewer to the exact statutory paragraph.*
> 
> *Simultaneously, look at the **MCQ Studio**: The AI automatically generates Bloom's Taxonomy-classified assessment items — categorized into Remember, Understand, Apply, and Analyze — each with pedagogical distractor rationales ready for faculty one-click approval."*

---

### [3:45 – 4:30] Executive Cadre Analytics & 12-Department Heatmap (45 Seconds)

**What to Show on Screen:**
- Press `Ctrl + Shift + D`, switch to **Dr. Priya Nair (Admin)**.
- Navigate to **Executive Dashboard** (`/admin`).
- Scroll through the 6 KPI cards, learning trends, and completion funnel.
- Click **Department Heatmap** (`/admin/departments`) showing the 12 Central Departments matrix.
- Click **Competency Radar** (`/admin/competencies`) showing the 10-axis radar chart.

**What to Say:**
> *"For line ministries and the Capacity Building Commission, macro-level visibility is vital. We switch to Dr. Priya Nair, Governance Lead.*
> 
> *Here is the **Executive Cadre Dashboard**: Real-time telemetry tracking 300 officers, 246 active learners, and 600 completed diagnostics across 12 central departments in Finance, Personnel, and MeitY.*
> 
> *This **36-Cell Cross-Pillar Heatmap** instantly identifies structural vulnerabilities: For example, the Department of Expenditure leads at 74.5% proficiency, while another department exhibits an acute procurement deficit.*
> 
> *And our **10-Axis Competency Radar** overlays Mandated Level vs Demonstrated Level against the National Benchmark, pinpointing exactly where institutional interventions are required."*

---

### [4:30 – 5:00] Cryptographic Credentials & Closing (30 Seconds)

**What to Show on Screen:**
- Navigate to **Certificates Vault** (`/certificates`).
- Click on the top certificate to open the **Official Printable A4 Modal**.
- Show the gold borders, CBC insignia, SHA-256 hash, and QR code.
- Click **Print / Download PDF** (shows browser print preview).

**What to Say:**
> *"Finally, when an officer achieves mastery, AI Karmayogi issues a Sovereign Digital Credential. Every certificate contains an immutable SHA-256 verification hash and tamper-proof QR code, printable in standard A4 format without external PDF SaaS fees.*
> 
> *In summary: AI Karmayogi solves Problem Statement SIH26101 with **100% data sovereignty**, **zero recurring API costs**, and **turnkey alignment with Mission Karmayogi**.*
> 
> *Thank you. We welcome your questions."*

---

## Emergency Troubleshooting & Fallbacks During Live Presentation
- **If network/WiFi disconnects:** The entire application runs on `localhost`. All AI models and vector databases are offline and self-contained; the demo will continue uninterrupted.
- **If an evaluator asks to see another role:** Press `Ctrl + Shift + D` to instantly switch to any persona in 1 click without entering passwords.
- **If an evaluator asks to search a page:** Press `Ctrl + K` to open the Spotlight Command Palette and navigate in 1 second.
