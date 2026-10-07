# ==============================================================================
# AI KARMAYOGI — PDF INTELLIGENCE, SOVEREIGN RAG & MCQ UNIT TEST SUITE
# PyMuPDF Chunking, Breadcrumbs, nomic-embed-text Vectors, RAG & Bloom MCQs
# ==============================================================================

import os
import sys
import asyncio
import tempfile
import pymupdf

# Force utf-8 stdout for Windows console
sys.stdout.reconfigure(encoding='utf-8')

from ai.pdf_service import PDFService
from ai.embedding_service import EmbeddingService
from ai.rag_service import RAGService
from ai.mcq_service import MCQService

def create_sample_government_pdf(file_path: str):
    """
    Creates a valid synthetic government Office Memorandum PDF using PyMuPDF.
    """
    doc = pymupdf.open()
    
    # Page 1: Header & Preamble
    p1 = doc.new_page()
    text_p1 = (
        "GOVERNMENT OF INDIA\n"
        "MINISTRY OF FINANCE\n"
        "DEPARTMENT OF EXPENDITURE\n\n"
        "F.No. 1/24/2026-PPD\n"
        "Dated: 15th January, 2026\n\n"
        "OFFICE MEMORANDUM\n\n"
        "Subject: Revised Guidelines on Public Procurement and GeM Portal Thresholds under GFR 2017\n\n"
        "CHAPTER I: PRELIMINARY MANDATES\n"
        "Rule 149(i): Mandatory Direct Purchase on GeM\n"
        "All Central Ministries, Departments, and Subordinate Offices shall procure goods and services "
        "available on the Government e-Marketplace (GeM). Up to ₹25,000, direct purchase may be made through "
        "any supplier meeting specifications, quality, and delivery schedules. The Drawing and Disbursing "
        "Officer (DDO) must record online verification.\n\n"
        "Rule 149(ii): L-1 Comparison Bidding\n"
        "For procurements between ₹25,000 and ₹5,00,000, the buyer shall view at least three different "
        "manufacturers meeting requisites and select the L-1 lowest quotation vendor on GeM."
    )
    p1.insert_text((50, 60), text_p1, fontsize=11)

    # Page 2: Proprietary Articles & Dispute Adjudication
    p2 = doc.new_page()
    text_p2 = (
        "CHAPTER II: PROPRIETARY & SOLE TENDER EXCEPTIONS\n\n"
        "Rule 166: Proprietary Article Certificate (PAC) Purchase\n"
        "Procurement from a single source may only be resorted to if the required item is manufactured "
        "exclusively by the original equipment manufacturer (OEM), or no alternative product will meet the "
        "technical operational requirements. A PAC certificate signed by an officer not below the rank of "
        "Deputy Secretary with IFD financial concurrence must be placed in the audit file.\n\n"
        "Section 7: Liquidated Damages & Contractual Penalties\n"
        "In the event of vendor delivery delay, liquidated damages at 0.5% per week subject to a maximum "
        "of 10% of total contract value shall be deducted prior to issuing the Consignee Receipt and "
        "Acceptance Certificate (CRAC)."
    )
    p2.insert_text((50, 60), text_p2, fontsize=11)

    doc.save(file_path)
    doc.close()

async def test_pdf_extraction_and_chunking():
    print("\n--- Test 1: Testing PyMuPDF Extraction & Recursive Chunking ---")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        create_sample_government_pdf(tmp_path)
        parsed = PDFService.process_pdf(tmp_path)
        meta = parsed["metadata"]
        chunks = parsed["chunks"]

        assert meta["total_pages"] == 2, f"Expected 2 pages, got {meta['total_pages']}"
        assert "Ministry of Finance" in meta["ministry"], f"Expected Ministry of Finance, got {meta['ministry']}"
        assert len(chunks) >= 2, f"Expected at least 2 chunks, got {len(chunks)}"

        first_chunk = chunks[0]
        assert "Rule 149" in first_chunk["section_reference"] or "Page 1" in first_chunk["section_reference"]
        assert ">" in first_chunk["breadcrumb"], f"Expected breadcrumb hierarchy, got {first_chunk['breadcrumb']}"
        assert first_chunk["token_count"] > 15, "Chunk must contain substantial tokens"

        print(f"[PASS] PyMuPDF Extraction Verified:")
        print(f"       Ministry: {meta['ministry']}")
        print(f"       Pages: {meta['total_pages']} | Chunks Generated: {len(chunks)}")
        print(f"       Sample Breadcrumb: {first_chunk['breadcrumb']}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

async def test_embeddings():
    print("\n--- Test 2: Testing 768-dim Embedding Generation & Cosine Math ---")
    text_a = "Public procurement via GeM portal up to twenty-five thousand rupees direct purchase."
    text_b = "Government e-Marketplace direct procurement and supplier quotation threshold under GFR 149."
    text_c = "Civil service annual performance appraisal report APAR writing procedure."

    vec_a = await EmbeddingService.generate_embedding(text_a)
    vec_b = await EmbeddingService.generate_embedding(text_b)
    vec_c = await EmbeddingService.generate_embedding(text_c)

    assert len(vec_a) == 768, f"Expected 768 dimensions, got {len(vec_a)}"
    assert len(vec_b) == 768, f"Expected 768 dimensions, got {len(vec_b)}"

    sim_self = EmbeddingService.cosine_similarity(vec_a, vec_a)
    sim_related = EmbeddingService.cosine_similarity(vec_a, vec_b)
    sim_unrelated = EmbeddingService.cosine_similarity(vec_a, vec_c)

    assert abs(sim_self - 1.0) < 1e-3, f"Self-similarity must be ~1.0, got {sim_self}"
    assert sim_related > sim_unrelated, f"Related texts must have higher similarity ({sim_related} vs {sim_unrelated})"
    print(f"[PASS] Embedding Vectors Verified (768-dim):")
    print(f"       Self Similarity: {sim_self:.4f}")
    print(f"       Related Procurement Similarity: {sim_related:.4f}")
    print(f"       Unrelated APAR Similarity: {sim_unrelated:.4f}")

async def test_rag_and_summary():
    print("\n--- Test 3: Testing Sovereign Grounded RAG & AI Summarization ---")
    chunks = [
        {
            "chunk_content": "Rule 149(i): Direct purchase on GeM up to ₹25,000 allowed through any supplier meeting quality requisites.",
            "section_reference": "Rule 149(i)",
            "page_number": 1,
            "breadcrumb": "GFR 2017 > Chapter I > Rule 149(i)",
            "similarity": 0.94
        },
        {
            "chunk_content": "Rule 166: Single source procurement permitted only under Proprietary Article Certificate (PAC) approved by Deputy Secretary.",
            "section_reference": "Rule 166",
            "page_number": 2,
            "breadcrumb": "GFR 2017 > Chapter II > Rule 166",
            "similarity": 0.88
        }
    ]

    # Test RAG query
    rag_res = await RAGService.answer_query(
        query="What is the direct purchase monetary limit on GeM?",
        retrieved_chunks=chunks,
        document_title="GFR 2017 Procurement Guidelines"
    )
    assert "Rule 149(i)" in rag_res["answer"] or "₹25,000" in rag_res["answer"]
    assert len(rag_res["citations"]) == 2
    assert rag_res["confidence_score"] >= 0.70
    print(f"[PASS] Grounded RAG Answer Generated (Confidence: {rag_res['confidence_score']}):")
    print(f"       First Citation: {rag_res['citations'][0]['section_reference']} (Page {rag_res['citations'][0]['page_number']})")

    # Test Document Summary
    summary = await RAGService.generate_document_summary(
        document_title="GFR 2017 Procurement Guidelines",
        ministry="Ministry of Finance",
        chunks=chunks
    )
    assert "executive_summary" in summary
    assert len(summary["key_policy_changes"]) > 0
    assert len(summary["compliance_checklist"]) > 0
    assert len(summary["faqs"]) > 0
    print(f"[PASS] 6-Part AI Summary Generated:")
    print(f"       Policy Changes: {len(summary['key_policy_changes'])} items")
    print(f"       Compliance Checklist: {len(summary['compliance_checklist'])} items")

def test_mcq_generation():
    print("\n--- Test 4: Testing Bloom-Classified AI MCQ Generation ---")
    chunks = [
        {
            "chunk_content": "Under Rule 149(i), direct purchase on GeM is permitted up to ₹25,000. For ₹25,000 to ₹5,00,000, L-1 comparison across 3 manufacturers is mandatory.",
            "section_reference": "Rule 149",
            "page_number": 1,
            "breadcrumb": "GFR 2017 > Chapter I > Rule 149"
        },
        {
            "chunk_content": "Under Rule 166, Proprietary Article Certificate (PAC) requires prior approval from an officer not below Deputy Secretary with IFD concurrence.",
            "section_reference": "Rule 166",
            "page_number": 2,
            "breadcrumb": "GFR 2017 > Chapter II > Rule 166"
        }
    ]

    mcqs = MCQService.generate_mcqs_from_chunks(
        document_title="GFR 2017 Guidelines",
        ministry="Ministry of Finance",
        chunks=chunks,
        num_questions=5
    )
    assert len(mcqs) == 5, f"Expected 5 MCQs, got {len(mcqs)}"

    for q in mcqs:
        assert len(q["options"]) == 4, "MCQ must have 4 options"
        assert q["correct_answer"] in ["A", "B", "C", "D"], f"Invalid answer key: {q['correct_answer']}"
        assert q["bloom_level"] in ["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE", "EVALUATE"]
        assert len(q["explanation"]) > 10, "Pedagogical explanation must be substantive"
        assert "Rule" in q["citation"], "Citation must reference rule/clause"

    print(f"[PASS] 5 Bloom-Classified MCQs Generated:")
    print(f"       Q1 Bloom: {mcqs[0]['bloom_level']} | Diff: {mcqs[0]['difficulty']}")
    print(f"       Q1 Citation: {mcqs[0]['citation']}")

def test_fastapi_document_endpoints():
    print("\n--- Test 5: Verifying Document Intelligence Route Table Mounting ---")
    from app.main import app
    openapi_schema = app.openapi()
    paths = list(openapi_schema.get("paths", {}).keys())

    expected_routes = [
        "/api/v1/documents/upload",
        "/api/v1/documents",
        "/api/v1/documents/{document_id}",
        "/api/v1/documents/{document_id}/summary",
        "/api/v1/rag/query",
        "/api/v1/mcq/generate",
        "/api/v1/mcq/publish"
    ]
    for exp in expected_routes:
        assert any(exp == p or exp.rstrip("/") == p.rstrip("/") for p in paths), f"Route {exp} missing in FastAPI app! Found paths: {paths}"
        print(f"  [FOUND] {exp}")
    print("[PASS] All Document Intelligence & RAG endpoints verified in FastAPI router.")

async def main():
    print("\n==================================================")
    print("AI KARMAYOGI — PDF INTELLIGENCE & SOVEREIGN RAG TESTS")
    print("==================================================")
    await test_pdf_extraction_and_chunking()
    await test_embeddings()
    await test_rag_and_summary()
    test_mcq_generation()
    test_fastapi_document_endpoints()
    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! [OK]")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
