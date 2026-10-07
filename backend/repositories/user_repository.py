# ==============================================================================
# AI KARMAYOGI — USER REPOSITORY (MongoDB)
# User CRUD, Role & Department Lookups with Denormalized Fields
# ==============================================================================

import types
from typing import Optional
from app.models.entities import _to_obj, new_uuid, utcnow


class UserRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["users"] if db is not None else None

    def _enrich_user(self, doc: dict) -> types.SimpleNamespace:
        """
        Convert MongoDB user doc to SimpleNamespace with nested role/department
        objects for backward compatibility with service-layer attribute access
        (e.g. user.role.role_code, user.department.name).
        """
        if doc is None:
            return None
        doc["id"] = doc.pop("_id", doc.get("id"))
        # Build nested role namespace
        doc["role"] = types.SimpleNamespace(
            id=doc.get("role_id"),
            role_code=doc.get("role_code", "learner"),
            role_name=doc.get("role_name", "Learner"),
        )
        # Build nested department namespace
        doc["department"] = types.SimpleNamespace(
            id=doc.get("department_id"),
            department_code=doc.get("department_code", ""),
            name=doc.get("department_name", "General Administration"),
            ministry_name=doc.get("ministry_name", "Government of India"),
        )
        # Build nested work_role namespace
        if doc.get("work_role_id"):
            doc["work_role"] = types.SimpleNamespace(
                id=doc.get("work_role_id"),
                role_code=doc.get("work_role_code", ""),
                role_title=doc.get("work_role_title", ""),
            )
        else:
            doc["work_role"] = None

        return types.SimpleNamespace(**doc)

    async def get_by_id(self, user_id) -> Optional[types.SimpleNamespace]:
        if self.collection is None:
            return None
        user_id_str = str(user_id)
        doc = await self.collection.find_one({"_id": user_id_str})
        return self._enrich_user(doc)

    async def get_by_email(self, email: str) -> Optional[types.SimpleNamespace]:
        if self.collection is None:
            return None
        normalized = email.lower().strip()
        doc = await self.collection.find_one({"email": normalized})
        return self._enrich_user(doc)

    async def create(self, user_data) -> types.SimpleNamespace:
        """
        Create a new user. Accepts either a dict or a SimpleNamespace with
        the required fields.
        """
        if isinstance(user_data, dict):
            data = user_data
        else:
            # Handle SimpleNamespace / object with attributes
            data = vars(user_data) if hasattr(user_data, '__dict__') else dict(user_data)

        if "_id" not in data and "id" in data:
            data["_id"] = str(data.pop("id"))
        elif "_id" not in data:
            data["_id"] = new_uuid()
        else:
            data["_id"] = str(data["_id"])

        now = utcnow()
        data.setdefault("created_at", now)
        data.setdefault("updated_at", now)
        data.setdefault("is_active", True)

        await self.collection.insert_one(data)
        return self._enrich_user(data)

    async def update_profile(self, user_id, full_name: Optional[str] = None, designation: Optional[str] = None):
        user_id_str = str(user_id)
        update_fields = {"updated_at": utcnow()}
        if full_name is not None:
            update_fields["full_name"] = full_name
        if designation is not None:
            update_fields["designation"] = designation
        await self.collection.update_one({"_id": user_id_str}, {"$set": update_fields})
        doc = await self.collection.find_one({"_id": user_id_str})
        return self._enrich_user(doc)

    async def update_password(self, user_id, hashed_password: str):
        user_id_str = str(user_id)
        await self.collection.update_one(
            {"_id": user_id_str},
            {"$set": {"password_hash": hashed_password, "updated_at": utcnow()}}
        )

    async def get_role_by_code(self, role_code: str):
        doc = await self.db["roles"].find_one({"role_code": role_code})
        return _to_obj(doc)

    async def get_department_by_code(self, dept_code: str):
        doc = await self.db["departments"].find_one({"department_code": dept_code})
        return _to_obj(doc)

    async def get_default_department(self):
        doc = await self.db["departments"].find_one()
        return _to_obj(doc)

    async def list_all_roles(self):
        cursor = self.db["roles"].find().sort("role_name", 1)
        docs = await cursor.to_list(length=100)
        return [_to_obj(d) for d in docs]
