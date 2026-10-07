# ==============================================================================
# AI KARMAYOGI — SEED ANALYTICS & EXECUTIVE CADRE DATA
# Seeds 3 Ministries, 12 Departments, 300 Officers & 250 Certificates
# PyMongo AsyncMongoClient Seed Script
# ==============================================================================

import asyncio
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.config import settings
from app.models.entities import new_uuid, utcnow
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

MINISTRIES_AND_DEPARTMENTS = [
    # Ministry 1: Ministry of Finance
    {
        "ministry": "Ministry of Finance",
        "depts": [
            ("DEPT-EXP-01", "Department of Expenditure"),
            ("DEPT-REV-01", "Department of Revenue"),
            ("DEPT-DEA-01", "Department of Economic Affairs"),
            ("DEPT-DIPAM-01", "DIPAM (Asset Management)"),
        ],
    },
    # Ministry 2: Ministry of Personnel, Public Grievances and Pensions
    {
        "ministry": "Ministry of Personnel, PG & Pensions",
        "depts": [
            ("DEPT-DOPT-01", "Department of Personnel & Training"),
            ("DEPT-DARPG-01", "DARPG (Administrative Reforms)"),
            ("DEPT-DOPPW-01", "Department of Pension & Pensioners' Welfare"),
            ("DEPT-SSC-01", "Staff Selection Commission Secretariat"),
        ],
    },
    # Ministry 3: Ministry of Home Affairs
    {
        "ministry": "Ministry of Home Affairs",
        "depts": [
            ("DEPT-IS-01", "Internal Security Division"),
            ("DEPT-POL-01", "Police-I Wing"),
            ("DEPT-DM-01", "Disaster Management Wing"),
            ("DEPT-UT-01", "Union Territories Wing"),
        ],
    },
]

OFFICER_DESIGNATIONS = [
    "Under Secretary",
    "Deputy Secretary",
    "Director",
    "Joint Secretary",
    "Section Officer",
    "Assistant Section Officer",
]

FIRST_NAMES = ["Rajesh", "Sunita", "Amit", "Priya", "Vikram", "Ananya", "Ramesh", "Deepika", "Sanjay", "Meenakshi"]
LAST_NAMES = ["Kumar", "Deshmukh", "Sharma", "Nair", "Verma", "Patel", "Singh", "Iyer", "Chauhan", "Gupta"]


async def seed_analytics_data(db):
    """Deterministically populates departments, officers, and certificates."""
    print("--- Seeding Canonical Ministries & Departments ---")
    dept_map = {}
    for group in MINISTRIES_AND_DEPARTMENTS:
        ministry_name = group["ministry"]
        for code, name in group["depts"]:
            dept = await db["departments"].find_one({"department_code": code})
            if not dept:
                dept = {
                    "_id": new_uuid(),
                    "department_code": code,
                    "name": name,
                    "ministry_name": ministry_name,
                    "tier": "CENTRAL",
                    "created_at": utcnow(),
                    "updated_at": utcnow(),
                }
                await db["departments"].insert_one(dept)
                print(f"  + Added department: {code} - {name}")
            dept_map[code] = dept

    # Get standard roles
    learner_role = await db["roles"].find_one({"role_code": "learner"})
    if not learner_role:
        learner_role = await db["roles"].find_one({})

    if not learner_role:
        learner_role = {
            "_id": "11111111-1111-1111-1111-111111111101",
            "role_code": "learner",
            "role_name": "Civil Services Official / Learner",
            "display_name": "Learner",
            "description": "Civil Servant",
            "created_at": utcnow(),
            "updated_at": utcnow(),
        }
        await db["roles"].insert_one(learner_role)

    print("--- Seeding 300 Officer Cadre across 12 Departments ---")
    dept_list = list(dept_map.values())
    officers = []
    for i in range(1, 301):
        email = f"officer.{i:03d}@nic.in"
        user = await db["users"].find_one({"email": email})
        if not user:
            assigned_dept = dept_list[i % len(dept_list)]
            designation = OFFICER_DESIGNATIONS[i % len(OFFICER_DESIGNATIONS)]
            first = FIRST_NAMES[i % len(FIRST_NAMES)]
            last = LAST_NAMES[(i * 3) % len(LAST_NAMES)]
            full_name = f"{first} {last}"

            user = {
                "_id": new_uuid(),
                "role_id": str(learner_role["_id"]),
                "role_code": "learner",
                "department_id": str(assigned_dept["_id"]),
                "department_name": assigned_dept.get("name", ""),
                "ministry_name": assigned_dept.get("ministry_name", ""),
                "government_id_hash": f"GOV-ID-2026-{i:04d}",
                "email": email,
                "password_hash": "$2b$12$e8Y0N0g.X7u/o3W3r3z8weZ0eF9uA9cQfB.kP5u7Y4V7l0J1W9Z1.",  # dummy hash
                "full_name": full_name,
                "designation": designation,
                "is_active": True,
                "created_at": utcnow(),
                "updated_at": utcnow(),
            }
            await db["users"].insert_one(user)
        officers.append(user)

    print("--- Seeding 250 Verifiable Certificates ---")
    cert_types = ["COURSE_COMPLETION", "ASSESSMENT_MASTERY", "LEARNING_PATH_COMPLETION"]
    cert_topics = [
        "General Financial Rules (GFR) 2017 & GeM Procurement Mastery",
        "Central Secretariat Procedures & CSMOP 16th Edition Compliance",
        "Ethical Governance & Conflict of Interest Mitigation Framework",
        "Citizen-Centric Public Grievance Disposal under CPGRAMS 7.0",
        "RTI Act Section 8(1) Transparency & CPIO Adjudication",
        "Rule 14 Disciplinary Proceedings & Inquiry Officer Protocols",
        "PFMS Budget Monitoring & Cash Management System",
        "Public Accounts Committee (PAC) Audit Para Settlement",
    ]

    for c_idx in range(1, 251):
        cert_num = f"AK-2026-CERT-{c_idx:06d}"
        existing_cert = await db["certificates"].find_one({"certificate_number": cert_num})
        if not existing_cert:
            officer = officers[c_idx % len(officers)]
            topic = cert_topics[c_idx % len(cert_topics)]
            c_type = cert_types[c_idx % len(cert_types)]
            verif_code = f"VK-{c_idx:04d}-{uuid.uuid4().hex[:4].upper()}-IN"
            officer_name = officer.get("full_name", "Officer")
            officer_desig = officer.get("designation", "Officer")
            officer_dept = officer.get("department_name", "Central Secretariat")
            officer_min = officer.get("ministry_name", "Government of India")
            officer_id = str(officer["_id"])

            meta = {
                "score_achieved": 85.0 + (c_idx % 15),
                "credits_earned": 3.0 + (c_idx % 3),
                "course_hours": 2.5 + (c_idx % 4),
                "signatory_title": "Director General, Mission Karmayogi Bharat",
            }

            cert = {
                "_id": new_uuid(),
                "user_id": officer_id,
                "officer_name": officer_name,
                "designation": officer_desig,
                "department": officer_dept,
                "ministry": officer_min,
                "certificate_number": cert_num,
                "certificate_type": c_type,
                "title": topic,
                "issuing_authority": "Mission Karmayogi Bharat • Capacity Building Commission",
                "issued_at": utcnow().isoformat(),
                "verification_code": verif_code,
                "verification_url": f"https://karmayogi.gov.in/verify?cert={cert_num}",
                "qr_code_data": f"AI-KARMAYOGI-VERIFY:{cert_num}:{officer_name.replace(' ', '_')}:{c_type}:VALID",
                "metadata": meta,
                "metadata_json": meta,
                "created_at": utcnow(),
                "updated_at": utcnow(),
            }
            await db["certificates"].insert_one(cert)

    print("--- Analytics Seed Completed Successfully [300 Officers, 250 Certificates] ---")


async def seed_database(db=None):
    owns_client = False
    client = None
    if db is None:
        print(f"[AI Karmayogi] Connecting to MongoDB: {settings.MONGODB_DATABASE}...")
        client = AsyncMongoClient(settings.MONGODB_URI, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)
        db = client[settings.MONGODB_DATABASE]
        owns_client = True
    await seed_analytics_data(db)
    if owns_client and client:
        await client.close()


seed_analytics = seed_database
run_seed = seed_database

if __name__ == "__main__":
    asyncio.run(seed_database())
