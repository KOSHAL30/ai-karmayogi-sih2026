# ==============================================================================
# AI KARMAYOGI — DEPARTMENT REPOSITORY (MongoDB)
# ==============================================================================

from typing import Optional, List
from app.models.entities import _to_obj, _to_list


class DepartmentRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["departments"]

    async def get_by_id(self, dept_id: str):
        doc = await self.collection.find_one({"_id": dept_id})
        return _to_obj(doc)

    async def get_by_code(self, dept_code: str):
        doc = await self.collection.find_one({"department_code": dept_code})
        return _to_obj(doc)

    async def list_all(self):
        cursor = self.collection.find().sort("name", 1)
        docs = await cursor.to_list(length=500)
        return _to_list(docs)
