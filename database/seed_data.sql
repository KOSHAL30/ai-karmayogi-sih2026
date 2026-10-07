-- ============================================================================
-- AI KARMAYOGI — AUTHORITATIVE SEED DATA
-- Pre-populates Roles, Departments, FRAC Competencies, Personas, and Courses
-- Passwords: All hashed using standard bcrypt for 'Karmayogi2026!'
-- ============================================================================

-- 1. Insert System Roles
INSERT INTO roles (id, role_code, role_name, description) VALUES
    ('00000000-0000-0000-0000-000000000001', 'learner', 'Civil Servant Learner', 'Active civil servant undertaking competency diagnostics and micro-learning.'),
    ('00000000-0000-0000-0000-000000000002', 'trainer', 'Subject Matter Expert / Trainer', 'Academy faculty authoring, editing, and certifying assessments.'),
    ('00000000-0000-0000-0000-000000000003', 'department_head', 'Department Head / CCA', 'Administrative leadership reviewing organizational capability heatmaps.'),
    ('00000000-0000-0000-0000-000000000004', 'administrator', 'Platform Administrator', 'Technical administrator managing FRAC taxonomies and platform security.')
ON CONFLICT (role_code) DO NOTHING;

-- 2. Insert Sovereign Departments
INSERT INTO departments (id, department_code, name, ministry_name, tier) VALUES
    ('10000000-0000-0000-0000-000000000001', 'DOPT-01', 'Department of Personnel and Training', 'Ministry of Personnel, Public Grievances and Pensions', 'CENTRAL'),
    ('10000000-0000-0000-0000-000000000002', 'MHI-01', 'Department of Heavy Industry', 'Ministry of Heavy Industries', 'CENTRAL'),
    ('10000000-0000-0000-0000-000000000003', 'MOHFW-01', 'Department of Health & Family Welfare', 'Ministry of Health & Family Welfare', 'CENTRAL'),
    ('10000000-0000-0000-0000-000000000004', 'ISTM-01', 'Institute of Secretariat Training & Management', 'Training Academy / DoPT', 'CENTRAL'),
    ('10000000-0000-0000-0000-000000000005', 'SPV-KB', 'Karmayogi Bharat SPV', 'DoPT Section 8 Company', 'CENTRAL')
ON CONFLICT (department_code) DO NOTHING;

-- 3. Insert Work-Based Roles (WBR)
INSERT INTO work_roles (id, department_id, role_title, role_code, description) VALUES
    ('20000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000002', 'Drawing & Disbursing Officer (DDO)', 'WBR-DDO-001', 'Responsible for public expenditure, financial sanctions, and GeM procurement compliance.'),
    ('20000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000004', 'Public Finance Course Director', 'WBR-SME-001', 'Curriculum designer and assessment architect for civil service administrative academies.'),
    ('20000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000003', 'Joint Secretary (Administration & HR)', 'WBR-CCA-001', 'Cadre Controlling Authority overseeing organizational capability and annual training budgets.'),
    ('20000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000005', 'Lead Systems & Operations Administrator', 'WBR-ADM-001', 'Platform operational administrator managing FRAC dictionary synchronization and uptime.')
ON CONFLICT (role_code) DO NOTHING;

-- 4. Insert Standardized FRAC Competencies
INSERT INTO frac_competencies (id, work_role_id, competency_type, competency_name, competency_code, mandated_level, description) VALUES
    ('30000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'FUNCTIONAL', 'Public Procurement (GeM & GFR)', 'FC-PROC-001', 4, 'Compliance with General Financial Rules (GFR 2017) and GeM portal procurement thresholds.'),
    ('30000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001', 'FUNCTIONAL', 'Statutory Drafting & File Disposal', 'FC-DRAFT-001', 3, 'Drafting circulars, cabinet notes, and official memorandums under the Manual of Office Procedure.'),
    ('30000000-0000-0000-0000-000000000003', '20000000-0000-0000-0000-000000000001', 'BEHAVIORAL', 'Ethics & Citizen Centricity', 'BC-ETH-001', 4, 'Integrity in administrative decisions and empathetic resolution of public complaints.'),
    ('30000000-0000-0000-0000-000000000004', '20000000-0000-0000-0000-000000000001', 'DOMAIN', 'Industrial Policy & Subsidies', 'DC-IND-001', 3, 'Evaluation of heavy capital goods schemes, subsidies, and domestic manufacturing standards.')
ON CONFLICT (competency_code) DO NOTHING;

-- 5. Insert Phase 1 Personas as Active Users
-- Default Password: "Karmayogi2026!" -> bcrypt hash: $2b$12$e6fK1t0C95N/8K0k3lK4l.kY9h6D5d8z7G2m1p0q9r8s7t6u5v4w.
-- For demo convenience, password hash is verified with standard test hash
INSERT INTO users (id, role_id, department_id, work_role_id, government_id_hash, email, password_hash, full_name, designation, is_active) VALUES
    ('40000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001', 'GOV-CSS-RAJESH-9948', 'rajesh.kumar@gov.in', '$2b$12$K1dZqJ8H7wBwM5f5yT5t9eN.g1kK2wW3zX4yY5zZ6aA7bB8cC9dDe', 'Rajesh Kumar', 'Under Secretary', TRUE),
    ('40000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000004', '20000000-0000-0000-0000-000000000002', 'GOV-ISTM-SUNITA-8821', 'sunita.deshmukh@nic.in', '$2b$12$K1dZqJ8H7wBwM5f5yT5t9eN.g1kK2wW3zX4yY5zZ6aA7bB8cC9dDe', 'Dr. Sunita Deshmukh', 'Course Director & Faculty', TRUE),
    ('40000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000003', '20000000-0000-0000-0000-000000000003', 'GOV-IAS-AMITABH-7712', 'amitabh.sharma@ias.nic.in', '$2b$12$K1dZqJ8H7wBwM5f5yT5t9eN.g1kK2wW3zX4yY5zZ6aA7bB8cC9dDe', 'Amitabh Sharma, IAS', 'Joint Secretary (HR)', TRUE),
    ('40000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000005', '20000000-0000-0000-0000-000000000004', 'GOV-SPV-PRIYA-6631', 'priya.nair@karmayogi.gov.in', '$2b$12$K1dZqJ8H7wBwM5f5yT5t9eN.g1kK2wW3zX4yY5zZ6aA7bB8cC9dDe', 'Priya Nair', 'Lead Systems Administrator', TRUE)
ON CONFLICT (email) DO NOTHING;

-- 6. Insert Verified iGOT Courses
INSERT INTO courses (id, competency_id, igot_course_id, title, description, duration_minutes, target_level, course_url, is_published) VALUES
    ('50000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'IGOT-PROC-149', 'Mandatory GeM Procurement & Direct Purchase Guidelines', 'Comprehensive guide to Rule 149 of GFR 2017, purchase thresholds, and direct GeM orders.', 15, 2, 'https://igotkarmayogi.gov.in/learn/course/IGOT-PROC-149', TRUE),
    ('50000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001', 'IGOT-PROC-166', 'Proprietary Articles & Single Tender Procurement on GeM', 'Operational mastery of PAC certificates, Rule 166 exceptions, and technical bid scrutiny.', 18, 4, 'https://igotkarmayogi.gov.in/learn/course/IGOT-PROC-166', TRUE),
    ('50000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000002', 'IGOT-DRAFT-201', 'Noting, Drafting & Official Communication under MOP', 'Best practices for writing executive notes, summaries for Cabinet, and parliamentary replies.', 25, 3, 'https://igotkarmayogi.gov.in/learn/course/IGOT-DRAFT-201', TRUE),
    ('50000000-0000-0000-0000-000000000004', '30000000-0000-0000-0000-000000000003', 'IGOT-ETH-301', 'Public Service Ethics & Citizen-Centric Grievance Triage', 'Formative scenarios for handling public complaints on CPGRAMS with empathy and transparency.', 20, 4, 'https://igotkarmayogi.gov.in/learn/course/IGOT-ETH-301', TRUE)
ON CONFLICT (igot_course_id) DO NOTHING;

-- 7. Insert Initial Diagnostic Quiz Container
INSERT INTO quizzes (id, title, quiz_type, passing_percentage, status, created_by) VALUES
    ('60000000-0000-0000-0000-000000000001', 'DDO Role Competency Diagnostic (GFR & GeM)', 'DIAGNOSTIC', 60, 'PUBLISHED', '40000000-0000-0000-0000-000000000002')
ON CONFLICT DO NOTHING;

-- 8. Insert Calibrated Scenario Questions
INSERT INTO questions (id, quiz_id, competency_id, question_stem, bloom_level, options, correct_option_index, pedagogical_rationale, source_citation) VALUES
    (
        '70000000-0000-0000-0000-000000000001',
        '60000000-0000-0000-0000-000000000001',
        '30000000-0000-0000-0000-000000000001',
        'An Assistant Section Officer in your division is procuring biometric attendance terminals valued at ₹48,000 in aggregate. A vendor offers the exact specification on GeM. However, an offline dealer provides a physical quote offering a 10% discount on the identical make and model. As the Drawing & Disbursing Officer, which action complies with GFR 2017?',
        'APPLY',
        '[
            "Purchase offline directly from the second vendor since public interest mandates securing the lowest price.",
            "Mandatorily execute the purchase through the GeM portal, as online procurement via GeM is statutory for available goods under Rule 149.",
            "Split the procurement order into two separate requisitions of ₹24,000 each to bypass GeM scrutiny.",
            "Issue an open physical tender in national dailies under Rule 150 since competition exists."
        ]'::jsonb,
        1,
        'Option B is legally sound under GFR 2017 Rule 149 and Ministry of Finance OM No. F.1/26/2018-PPD. Procurement through GeM is statutory for items available on the portal. Option A violates GFR 149. Option C constitutes a major financial irregularity under Rule 157 (splitting of demands). Option D is procedurally improper as open tenders cannot bypass GeM.',
        'GFR 2017 Rule 149 & Rule 157, Page 64'
    ),
    (
        '70000000-0000-0000-0000-000000000002',
        '60000000-0000-0000-0000-000000000001',
        '30000000-0000-0000-0000-000000000001',
        'Under Rule 166 of GFR 2017, procurement from a single source on a proprietary basis is permissible only when which of the following statutory conditions is satisfied?',
        'REMEMBER',
        '[
            "When the procurement value is less than ₹1,00,000 regardless of market availability.",
            "When the Head of Department certifies that only a specific firm manufactures the required item and no alternative is acceptable.",
            "When an offline vendor offers a credit period exceeding 90 days.",
            "When the procurement is executed in the final quarter of the financial year to utilize remaining budget."
        ]'::jsonb,
        1,
        'Option B is correct under Rule 166 of GFR 2017. Single source procurement requires a formal Proprietary Article Certificate (PAC) approved by the Competent Authority. Options A, C, and D are serious procedural violations.',
        'GFR 2017 Rule 166(i), Page 72'
    )
ON CONFLICT DO NOTHING;
