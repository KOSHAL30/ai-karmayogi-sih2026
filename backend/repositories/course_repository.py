# ==============================================================================
# AI KARMAYOGI — COURSE REPOSITORY (MongoDB)
# ==============================================================================

import re
from typing import Optional, List
from app.models.entities import _to_obj, _to_list


class CourseRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["courses"]

    async def get_by_id(self, course_id: str):
        doc = await self.collection.find_one({"_id": course_id})
        if doc and doc.get("competency_id"):
            comp = await self.db["competencies"].find_one({"_id": doc["competency_id"]})
            if comp:
                comp["id"] = comp.pop("_id", None)
                doc["competency"] = comp
        return _to_obj(doc)

    async def get_by_igot_id(self, igot_course_id: str):
        doc = await self.collection.find_one({"igot_course_id": igot_course_id})
        return _to_obj(doc)

    async def get_by_competency_id(self, competency_id: str):
        cursor = self.collection.find(
            {"competency_id": competency_id, "is_published": True}
        ).sort([("target_level", 1), ("duration_minutes", 1)])
        docs = await cursor.to_list(length=500)
        return _to_list(docs)

    async def get_by_competency_ids(self, competency_ids: list):
        if not competency_ids:
            return []
        cursor = self.collection.find(
            {"competency_id": {"$in": [str(cid) for cid in competency_ids]}, "is_published": True}
        )
        docs = await cursor.to_list(length=500)
        return _to_list(docs)

    async def get_all(self, skip: int = 0, limit: int = 50, ministry: str = None, difficulty: str = None, search: str = None):
        query = {"is_published": True}
        if ministry:
            query["ministry"] = ministry
        if difficulty:
            query["difficulty"] = difficulty
        if search:
            pattern = re.escape(search)
            query["$or"] = [
                {"title": {"$regex": pattern, "$options": "i"}},
                {"description": {"$regex": pattern, "$options": "i"}},
                {"igot_course_id": {"$regex": pattern, "$options": "i"}},
            ]
        cursor = self.collection.find(query).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return _to_list(docs)

    async def count_all(self):
        return await self.collection.count_documents({"is_published": True})
