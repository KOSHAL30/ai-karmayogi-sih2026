# ==============================================================================
# AI KARMAYOGI — MONGODB SEED SCRIPT (Unified)
# Populates Roles, Departments, Work Roles, and Initial Users
# ==============================================================================

import asyncio
import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.entities import new_uuid, utcnow
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

DEFAULT_PASSWORD = get_password_hash("Karmayogi2026!")

ROLES_DATA = [
    {
        "_id": "11111111-1111-1111-1111-111111111101",
        "role_code": "learner",
        "role_name": "Civil Services Official / Learner",
        "description": "Officer undertaking competency diagnostics and continuous learning."
    },
    {
        "_id": "11111111-1111-1111-1111-111111111102",
        "role_code": "trainer",
        "role_name": "Capacity Building Faculty / Trainer",
        "description": "Training institution faculty authoring learning materials and quizzes."
    },
    {
        "_id": "11111111-1111-1111-1111-111111111103",
        "role_code": "admin",
        "role_name": "System Administrator & Department Lead",
        "description": "Governance lead managing users, taxonomy, and departmental health."
    },
]

DEPARTMENTS_DATA = [
    {
        "_id": "22222222-2222-2222-2222-222222222201",
        "department_code": "DEPT-DOPT",
        "name": "Department of Personnel and Training",
        "ministry_name": "Ministry of Personnel, Public Grievances and Pensions",
        "tier": "CENTRAL"
    },
    {
        "_id": "22222222-2222-2222-2222-222222222202",
        "department_code": "DEPT-MEITY",
        "name": "Ministry of Electronics and Information Technology",
        "ministry_name": "Ministry of Electronics and Information Technology",
        "tier": "CENTRAL"
    },
    {
        "_id": "22222222-2222-2222-2222-222222222203",
        "department_code": "DEPT-FIN",
        "name": "Department of Economic Affairs",
        "ministry_name": "Ministry of Finance",
        "tier": "CENTRAL"
    }
]

WORK_ROLES_DATA = [
    {
        "_id": "33333333-3333-3333-3333-333333333301",
        "department_id": "22222222-2222-2222-2222-222222222201",
        "role_code": "WBR-DESK-OFFICER",
        "role_title": "Desk Officer (Administration)",
        "description": "Handles administrative files, policy interpretation, and RTI queries."
    },
    {
        "_id": "33333333-3333-3333-3333-333333333302",
        "department_id": "22222222-2222-2222-2222-222222222201",
        "role_code": "WBR-SECTION-OFFICER",
        "role_title": "Section Officer (Establishment)",
        "description": "Supervises section staff and prepares parliamentary replies."
    }
]

USERS_DATA = [
    {
        "_id": "00000000-0000-0000-0000-000000000001",
        "email": "rajesh.kumar@gov.in",
        "full_name": "Rajesh Kumar",
        "designation": "Under Secretary (Establishment)",
        "role_id": "11111111-1111-1111-1111-111111111101",
        "role_code": "learner",
        "department_id": "22222222-2222-2222-2222-222222222201",
        "department_name": "Department of Personnel and Training",
        "work_role_id": "33333333-3333-3333-3333-333333333301",
        "government_id_hash": "GOV-ID-RAJESH-9842",
        "is_active": True
    },
    {
        "_id": "00000000-0000-0000-0000-000000000002",
        "email": "sunita.deshmukh@nic.in",
        "full_name": "Dr. Sunita Deshmukh",
        "designation": "Senior Training Faculty (ISTM)",
        "role_id": "11111111-1111-1111-1111-111111111102",
        "role_code": "trainer",
        "department_id": "22222222-2222-2222-2222-222222222202",
        "department_name": "Ministry of Electronics and Information Technology",
        "work_role_id": None,
        "government_id_hash": "GOV-ID-SUNITA-5192",
        "is_active": True
    },
    {
        "_id": "00000000-0000-0000-0000-000000000003",
        "email": "priya.nair@karmayogi.gov.in",
        "full_name": "Dr. Priya Nair",
        "designation": "Director (Capacity Building & Analytics)",
        "role_id": "11111111-1111-1111-1111-111111111103",
        "role_code": "admin",
        "department_id": "22222222-2222-2222-2222-222222222201",
        "department_name": "Department of Personnel and Training",
        "work_role_id": None,
        "government_id_hash": "GOV-ID-PRIYA-7731",
        "is_active": True
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
    
    print("[AI Karmayogi] Starting database seed...")
    
    # 1. Seed Roles
    for role_item in ROLES_DATA:
        existing = await db["roles"].find_one({"role_code": role_item["role_code"]})
        if not existing:
            role_item["created_at"] = utcnow()
            role_item["updated_at"] = utcnow()
            await db["roles"].insert_one(role_item)
            print(f"  + Added role: {role_item['role_code']}")

    # 2. Seed Departments
    for dept_item in DEPARTMENTS_DATA:
        existing = await db["departments"].find_one({"department_code": dept_item["department_code"]})
        if not existing:
            dept_item["created_at"] = utcnow()
            dept_item["updated_at"] = utcnow()
            await db["departments"].insert_one(dept_item)
            print(f"  + Added department: {dept_item['department_code']}")

    # 3. Seed Work Roles
    for wr_item in WORK_ROLES_DATA:
        existing = await db["work_roles"].find_one({"role_code": wr_item["role_code"]})
        if not existing:
            wr_item["created_at"] = utcnow()
            wr_item["updated_at"] = utcnow()
            await db["work_roles"].insert_one(wr_item)
            print(f"  + Added work role: {wr_item['role_code']}")

    # 4. Seed Users
    for user_item in USERS_DATA:
        existing = await db["users"].find_one({"email": user_item["email"]})
        if not existing:
            user_item["password_hash"] = DEFAULT_PASSWORD
            user_item["created_at"] = utcnow()
            user_item["updated_at"] = utcnow()
            await db["users"].insert_one(user_item)
            print(f"  + Added user: {user_item['email']}")

    print("[AI Karmayogi] Database seed completed successfully!")
    if owns_client and client:
        await client.close()

run_seed = seed_database

if __name__ == "__main__":
    asyncio.run(seed_database())
