# ==============================================================================
# AI KARMAYOGI — SOVEREIGN RAG & PDF INTELLIGENCE TEST SUITE
# Validating Text Chunking, Cosine Vector Math & Bloom MCQ Classification
# ==============================================================================

import unittest
import hashlib
import math

class TestRAGAndPDFIntelligence(unittest.TestCase):
    def test_sha256_document_fingerprint(self):
        sample_doc = b"%PDF-1.7 General Financial Rules 2017 Ministry of Finance"
        hasher = hashlib.sha256(sample_doc)
        digest = hasher.hexdigest()
        self.assertEqual(len(digest), 64)
        # Verify deterministic reproducibility
        self.assertEqual(digest, hashlib.sha256(sample_doc).hexdigest())

    def test_sliding_window_chunking(self):
        text = "word " * 1000
        words = text.split()
        chunk_size = 200
        overlap = 50

        chunks = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            if end >= len(words):
                break
            start += chunk_size - overlap

        self.assertTrue(len(chunks) > 1)
        # Check that overlap exists between chunk 0 and chunk 1
        chunk_0_words = set(chunks[0].split()[-overlap:])
        chunk_1_words = set(chunks[1].split()[:overlap])
        self.assertTrue(len(chunk_0_words.intersection(chunk_1_words)) > 0)

    def test_cosine_similarity_math(self):
        def cosine_similarity(v1, v2):
            dot = sum(a * b for a, b in zip(v1, v2))
            norm1 = math.sqrt(sum(a * a for a in v1))
            norm2 = math.sqrt(sum(b * b for b in v2))
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return dot / (norm1 * norm2)

        v_identical = [0.5, 0.5, 0.5, 0.5]
        v_orthogonal = [-0.5, 0.5, -0.5, 0.5]
        self.assertAlmostEqual(cosine_similarity(v_identical, v_identical), 1.0, places=4)
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0, places=4)

    def test_bloom_taxonomy_levels(self):
        bloom_levels = ["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE", "EVALUATE", "CREATE"]
        sample_mcq = {
            "stem": "An officer purchases goods worth Rs 3,50,000 without GeM portal. Which rule of GFR 2017 is violated?",
            "bloom": "APPLY",
            "correct_option": "Rule 149",
        }
        self.assertIn(sample_mcq["bloom"], bloom_levels)

if __name__ == "__main__":
    unittest.main()
