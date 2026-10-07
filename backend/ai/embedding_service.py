# ==============================================================================
# AI KARMAYOGI - SOVEREIGN LOCAL EMBEDDING PIPELINE
# nomic-embed-text 768-dim Embeddings with Standby Fallback & Cosine Math
#
# REQUIRED MONGODB ATLAS VECTOR INDEX:
# Collection: document_chunks
# Index Name: vector_index
# Path: embedding
# Dimensions: 768
# Similarity: cosine
# ==============================================================================
import math
import hashlib
from typing import List
import httpx

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DIMENSION = 768

class EmbeddingService:
    _OLLAMA_OFFLINE = False
    @staticmethod
    def _deterministic_local_vector(text: str, dim: int = VECTOR_DIMENSION) -> List[float]:
        """
        Deterministic pseudo-random projection vector generator for fallback/offline testing.
        Guarantees exact 768 dimensions and unit Euclidean norm (L2 = 1.0).
        """
        words = text.lower().split()
        raw = [0.0] * dim
        for word in words:
            h = int(hashlib.sha256(word.encode('utf-8')).hexdigest(), 16)
            for i in range(4): # Spread word hash across 4 buckets
                idx = (h >> (i * 12)) % dim
                weight = ((h >> (i * 8)) & 0xFF) / 255.0 - 0.5
                raw[idx] += weight

        # Add constant bias to avoid zero vector
        if all(v == 0.0 for v in raw):
            raw[0] = 1.0

        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in raw))
        if norm > 0:
            return [round(x / norm, 6) for x in raw]
        return [0.0] * dim

    @classmethod
    async def generate_embedding(cls, text: str) -> List[float]:
        
        clean_text = text.strip()
        if not clean_text:
            return [0.0] * VECTOR_DIMENSION

        if not cls._OLLAMA_OFFLINE:
            try:
                async with httpx.AsyncClient(timeout=1.0) as client:
                    res = await client.post(
                        OLLAMA_EMBED_URL,
                        json={"model": EMBEDDING_MODEL, "prompt": clean_text}
                    )
                    if res.status_code == 200:
                        data = res.json()
                        vec = data.get("embedding", [])
                        if len(vec) == VECTOR_DIMENSION:
                            return vec
            except Exception:
                cls._OLLAMA_OFFLINE = True

        return cls._deterministic_local_vector(clean_text, VECTOR_DIMENSION)


    @classmethod
    async def generate_batch_embeddings(cls, texts: List[str]) -> List[List[float]]:
        """
        Batch processes text strings into 768-dimensional embeddings.
        """
        results = []
        for t in texts:
            vec = await cls.generate_embedding(t)
            results.append(vec)
        return results

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes cosine similarity between two normalized vectors:
        Cosine = (A . B) / (||A|| * ||B||)
        """
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        sim = dot_product / (norm_a * norm_b)
        return round(max(0.0, min(1.0, (sim + 1.0) / 2.0)), 4)
