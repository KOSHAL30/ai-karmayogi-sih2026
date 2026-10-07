# ==============================================================================
# AI KARMAYOGI — COMPETENCY REPOSITORY (MongoDB)
# ==============================================================================

from typing import Optional, List
from app.models.entities import _to_obj, _to_list, new_uuid, utcnow


class CompetencyRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["competencies"]

    async def get_by_id(self, competency_id: str):
        doc = await self.collection.find_one({"_id": competency_id})
        return _to_obj(doc)

    async def get_by_code(self, code: str):
        doc = await self.collection.find_one({"competency_code": code})
        return _to_obj(doc)

    async def list_by_work_role(self, work_role_id: str):
        cursor = self.collection.find({"work_role_id": work_role_id}).sort([("competency_type", 1), ("competency_name", 1)])
        docs = await cursor.to_list(length=500)
        return _to_list(docs)

    async def list_all(self):
        cursor = self.collection.find().sort([("competency_type", 1), ("competency_name", 1)])
        docs = await cursor.to_list(length=500)
        return _to_list(docs)

    async def create(self, data: dict):
        if "_id" not in data:
            data["_id"] = new_uuid()
        now = utcnow()
        data.setdefault("created_at", now)
        data.setdefault("updated_at", now)
        await self.collection.insert_one(data)
        return _to_obj(data)
