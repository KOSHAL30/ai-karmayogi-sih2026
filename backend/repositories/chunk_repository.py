# ==============================================================================
# AI KARMAYOGI - CHUNK & VECTOR REPOSITORY (MongoDB)
# MongoDB Atlas Vector Search with application-level cosine fallback
#
# REQUIRED MONGODB ATLAS VECTOR INDEX:
# Collection: document_chunks
# Index Name: vector_index
# Path: embedding
# Dimensions: 768
# Similarity: cosine
# ==============================================================================
from typing import List, Dict, Any, Optional
from app.models.entities import new_uuid, utcnow
from ai.embedding_service import EmbeddingService


class ChunkRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["document_chunks"]

    async def create_chunks_with_embeddings(self, chunks: List[Dict[str, Any]]) -> None:
        """Insert chunks with embedded vectors in a single batch."""
        if not chunks:
            return
        for chunk in chunks:
            if "_id" not in chunk:
                chunk["_id"] = new_uuid()
            chunk.setdefault("created_at", utcnow())
            chunk.setdefault("embedding_model", "nomic-embed-text")
        await self.collection.insert_many(chunks)

    async def get_by_document_id(self, document_id: str) -> list:
        cursor = self.collection.find({"document_id": document_id}).sort("chunk_index", 1)
        return await cursor.to_list(length=5000)

    async def search_similar_chunks(
        self,
        query_vector: List[float],
        top_k: int = 5,
        document_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves Top-K most semantically similar chunks.
        Tries MongoDB Atlas $vectorSearch first, falls back to application-level cosine.
        """
        # Attempt Atlas Vector Search
        try:
            vs_filter = {}
            if document_id:
                vs_filter = {"document_id": document_id}

            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": max(top_k * 10, 50),
                        "limit": top_k,
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "document_id": 1,
                        "chunk_index": 1,
                        "chunk_content": 1,
                        "section_reference": 1,
                        "breadcrumb": 1,
                        "page_number": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
            ]

            # Add filter if document_id specified
            if document_id:
                pipeline[0]["$vectorSearch"]["filter"] = {"document_id": document_id}

            results = await self.collection.aggregate(pipeline).to_list(length=top_k)
            if results:
                return [
                    {
                        "chunk_id": str(r["_id"]),
                        "document_id": str(r.get("document_id", "")),
                        "chunk_index": r.get("chunk_index", 0),
                        "chunk_content": r.get("chunk_content", ""),
                        "section_reference": r.get("section_reference") or "General Clause",
                        "breadcrumb": r.get("breadcrumb") or "Document",
                        "page_number": r.get("page_number") or 1,
                        "similarity": r.get("score", 0.85),
                    }
                    for r in results
                ]
        except Exception:
            pass  # Atlas Vector Search not available, fall back

        # Fallback: application-level cosine similarity
        query = {}
        if document_id:
            query["document_id"] = document_id

        cursor = self.collection.find(query)
        all_chunks = await cursor.to_list(length=5000)

        scored = []
        for chunk in all_chunks:
            emb = chunk.get("embedding")
            if emb and isinstance(emb, list) and len(emb) > 0:
                sim = EmbeddingService.cosine_similarity(query_vector, emb)
            else:
                sim = 0.75  # baseline heuristic

            scored.append({
                "chunk_id": str(chunk["_id"]),
                "document_id": str(chunk.get("document_id", "")),
                "chunk_index": chunk.get("chunk_index", 0),
                "chunk_content": chunk.get("chunk_content", ""),
                "section_reference": chunk.get("section_reference") or "General Clause",
                "breadcrumb": chunk.get("breadcrumb") or "Document",
                "page_number": chunk.get("page_number") or 1,
                "similarity": sim,
            })

        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]
