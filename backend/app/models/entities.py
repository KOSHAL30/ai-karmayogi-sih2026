# ==============================================================================
# AI KARMAYOGI — DOCUMENT MODELS
# MongoDB-compatible field definitions (no ORM — pure reference constants)
# Repositories work with raw dicts; Pydantic schemas handle API validation
# ==============================================================================
# This module replaces the former SQLAlchemy ORM entities.
# MongoDB collections use string UUIDs as _id for frontend/JWT compatibility.
# ==============================================================================

import uuid
import types
from datetime import datetime, timezone


def new_uuid() -> str:
    """Generate a new UUID4 string for use as MongoDB _id."""
    return str(uuid.uuid4())


def utcnow() -> datetime:
    """Current UTC timestamp."""
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Collection name constants
# ---------------------------------------------------------------------------
ROLES = "roles"
DEPARTMENTS = "departments"
WORK_ROLES = "work_roles"
USERS = "users"
COMPETENCIES = "competencies"
COURSES = "courses"
QUIZZES = "quizzes"
QUESTIONS = "questions"
QUIZ_ATTEMPTS = "quiz_attempts"
RECOMMENDATIONS = "recommendations"
LEARNING_PROGRESS = "learning_progress"
DOCUMENTS = "documents"
DOCUMENT_CHUNKS = "document_chunks"
CERTIFICATES = "certificates"
NOTIFICATIONS = "notifications"
AUDIT_LOGS = "audit_logs"


# ---------------------------------------------------------------------------
# Utility: convert MongoDB documents to attribute-accessible objects
# ---------------------------------------------------------------------------
def _to_obj(doc):
    """
    Convert a MongoDB document (dict) into an attribute-accessible
    SimpleNamespace object.  Renames '_id' → 'id' for consistency.
    Handles nested dicts recursively so `user.role.role_code` still works
    when role data is embedded/denormalized in the user document.
    Returns None if doc is None.
    """
    if doc is None:
        return None
    if isinstance(doc, list):
        return [_to_obj(item) for item in doc]
    if not isinstance(doc, dict):
        return doc

    out = {}
    for k, v in doc.items():
        key = "id" if k == "_id" else k
        if isinstance(v, dict):
            out[key] = _to_obj(v)
        elif isinstance(v, list):
            out[key] = [_to_obj(i) if isinstance(i, dict) else i for i in v]
        else:
            out[key] = v
    return types.SimpleNamespace(**out)


def _to_list(docs):
    """Convert a list of MongoDB documents to SimpleNamespace objects."""
    return [_to_obj(d) for d in docs]


def _to_dict(obj):
    if isinstance(obj, types.SimpleNamespace):
        return {k: _to_dict(v) for k, v in vars(obj).items()}
    if isinstance(obj, list):
        return [_to_dict(i) for i in obj]
    return obj
