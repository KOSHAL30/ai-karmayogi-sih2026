# ==============================================================================
# AI KARMAYOGI — UNIFIED MASTER SEED SCRIPT
# Sequentially executes all seed scripts using a single MongoDB connection:
#   1. app.db.seed            (Roles, Departments, Work Roles, Initial Personas)
#   2. app.db.seed_assessment (FRAC Competencies, Master Diagnostic Quiz, Questions)
#   3. app.db.seed_courses    (40 iGOT Accredited Micro-Courses)
#
# Idempotent & safe to run repeatedly.
# ==============================================================================

import asyncio
import logging
import os
import sys
import time

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from app.core.config import settings

# Import seed step runners
from app.db.seed import run_seed as seed
from app.db.seed_assessment import run_seed as seed_assessment
from app.db.seed_courses import run_seed as seed_courses

seed_foundation = seed

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ai_karmayogi.seed_all")


async def _execute_step(step_number: int, total_steps: int, title: str, step_coro_fn, db):
    """Execute a single seed step with structured logging and timing."""
    print(f"\n{'=' * 72}")
    print(f"  PHASE [{step_number}/{total_steps}]: {title.upper()}")
    print(f"{'=' * 72}")
    t0 = time.perf_counter()
    try:
        # Pass db if accepted, else invoke without arguments
        import inspect
        sig = inspect.signature(step_coro_fn)
        if len(sig.parameters) > 0:
            await step_coro_fn(db)
        else:
            await step_coro_fn()
        elapsed = time.perf_counter() - t0
        print(f"  >>> Phase [{step_number}/{total_steps}] finished successfully in {elapsed:.2f}s")
    except Exception as exc:
        print(f"  >>> Phase [{step_number}/{total_steps}] FAILED with error: {exc}")
        logger.error(f"Error during {title}: {exc}", exc_info=True)
        raise


async def _print_verification_summary(db):
    """Print count of documents across all seeded collections for verification."""
    print(f"\n{'=' * 72}")
    print("  AI KARMAYOGI -- DATABASE VERIFICATION SUMMARY")
    print(f"{'=' * 72}")
    collections = [
        ("roles", "System Roles"),
        ("departments", "Departments & Ministries"),
        ("work_roles", "FRAC Work Roles"),
        ("users", "User & Officer Profiles"),
        ("competencies", "FRAC Competencies"),
        ("quizzes", "Diagnostic Quizzes"),
        ("questions", "Assessment Questions"),
        ("courses", "iGOT Accredited Courses"),
    ]
    for col_name, desc in collections:
        try:
            count = await db[col_name].count_documents({})
            print(f"  * {desc:<32} [{col_name:<14}]: {count:>5} documents")
        except Exception as err:
            print(f"  * {desc:<32} [{col_name:<14}]: Error ({err})")
    print(f"{'=' * 72}\n")


async def seed_all(db=None):
    """
    Unified master entrypoint that executes all AI Karmayogi demo seeds.
    
    Instantiates an AsyncMongoClient once if db is not provided, passes the db
    instance to each seed sub-script, prints progress logs, and outputs a
    verification count summary.
    """
    owns_client = False
    client = None

    if db is None:
        print(f"[AI Karmayogi] Connecting to MongoDB: {settings.MONGODB_DATABASE}...")
        client = AsyncMongoClient(
            settings.MONGODB_URI,
            server_api=ServerApi("1"),
            serverSelectionTimeoutMS=5000,
        )
        db = client[settings.MONGODB_DATABASE]
        owns_client = True
        # Verify connection
        await client.admin.command("ping")
        print(f"[AI Karmayogi] Verified connection to database: '{settings.MONGODB_DATABASE}'")

    print("\n" + "#" * 72)
    print("  MISSION KARMAYOGI BHARAT -- MASTER DATABASE SEED")
    print("  Populating sovereign competency, learning & executive data...")
    print("#" * 72)

    total_start = time.perf_counter()

    try:
        # Step 1: Core RBAC & Foundational Users
        await _execute_step(
            1, 3,
            "Core RBAC, Departments & Foundational Users",
            seed,
            db
        )

        # Step 2: FRAC Competencies & Diagnostic Assessments (Must precede courses for linking)
        await _execute_step(
            2, 3,
            "FRAC Competency Taxonomy & Diagnostic Assessments",
            seed_assessment,
            db
        )

        # Step 3: iGOT Karmayogi Courses (Maps to Competencies)
        await _execute_step(
            3, 3,
            "iGOT Karmayogi Accredited Micro-Courses (40)",
            seed_courses,
            db
        )

        # Print audit verification table
        await _print_verification_summary(db)

        total_elapsed = time.perf_counter() - total_start
        print(f"[AI Karmayogi] [OK] Complete demo seed suite finished successfully in {total_elapsed:.2f}s!")
        print("#" * 72 + "\n")

    finally:
        if owns_client and client:
            await client.close()
            print("[AI Karmayogi] MongoDB client connection closed.")


# Alias standard callable name
run_seed = seed_all


if __name__ == "__main__":
    asyncio.run(seed_all())
