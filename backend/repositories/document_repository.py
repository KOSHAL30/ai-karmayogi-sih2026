# ==============================================================================
# AI KARMAYOGI — DOCUMENT REPOSITORY (MongoDB)
# ==============================================================================

import re
from typing import Optional, List
from app.models.entities import _to_obj, _to_list, new_uuid, utcnow


class DocumentRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["documents"]

    async def create(self, data: dict):
        if "_id" not in data:
            data["_id"] = new_uuid()
        now = utcnow()
        data.setdefault("created_at", now)
        data.setdefault("updated_at", now)
        await self.collection.insert_one(data)
        return _to_obj(data)

    async def get_by_id(self, document_id: str):
        doc = await self.collection.find_one({"_id": document_id})
        if doc:
            chunks_cursor = self.db["document_chunks"].find({"document_id": document_id}).sort("chunk_index", 1)
            doc["chunks"] = await chunks_cursor.to_list(length=5000)
        return _to_obj(doc)

    async def get_by_hash(self, file_hash: str):
        doc = await self.collection.find_one({"file_hash": file_hash})
        return _to_obj(doc)

    async def get_all(self, skip: int = 0, limit: int = 50, status: str = None, search: str = None):
        query = {}
        if status:
            query["processing_status"] = status
        if search:
            pat = re.escape(search)
            query["$or"] = [
                {"document_title": {"$regex": pat, "$options": "i"}},
                {"ministry": {"$regex": pat, "$options": "i"}},
                {"om_number": {"$regex": pat, "$options": "i"}},
            ]
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
        docs = await cursor.to_list(length=limit)
        return _to_list(docs)

    async def update_status(self, document_id: str, status: str):
        await self.collection.update_one(
            {"_id": document_id},
            {"$set": {"processing_status": status, "updated_at": utcnow()}}
        )

    async def update_summary(self, document_id: str, summary_json: dict):
        await self.collection.update_one(
            {"_id": document_id},
            {"$set": {"summary_json": summary_json, "updated_at": utcnow()}}
        )

    async def delete(self, document_id: str):
        await self.db["document_chunks"].delete_many({"document_id": document_id})
        await self.collection.delete_one({"_id": document_id})
