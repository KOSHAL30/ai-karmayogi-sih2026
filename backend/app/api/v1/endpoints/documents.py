import os
import types
import uuid
import hashlib
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from pydantic import BaseModel

from app.core.config import settings
from app.core.deps import get_current_user_payload, RequireTrainer
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.schemas.document import (
    DocumentResponse,
    DocumentChunkItem,
    DocumentSummaryResponse,
    RAGQueryRequest,
    RAGQueryResponse,
    MCQGenerateRequest,
    MCQGenerateResponse,
    MCQUpdateRequest,
    MCQItem,
    MCQPublishRequest,
    MCQPublishResponse
)
from repositories.document_repository import DocumentRepository
from repositories.chunk_repository import ChunkRepository
from ai.pdf_service import PDFService
from ai.embedding_service import EmbeddingService
from ai.rag_service import RAGService
from ai.mcq_service import MCQService
from app.models.entities import new_uuid, utcnow

router = APIRouter()
rag_router = APIRouter()
mcq_router = APIRouter()

MAX_FILE_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
UPLOAD_DIR = "/tmp/uploads" if os.environ.get("VERCEL") else settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory store for draft MCQs pending trainer approval
DRAFT_MCQ_CACHE: Dict[str, dict] = {}

# 1. Document Upload Studio
# ------------------------------------------------------------------------------
@router.post("/upload", response_model=APIResponse[DocumentResponse])
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("OM"),
    ministry: Optional[str] = Form(None),
    user = RequireTrainer,
    db = Depends(get_db)
):
    """
    Validates, extracts, chunks and embeds sovereign government PDFs.
    """
    # 1. Path Traversal Fix: Sanitize filename
    safe_filename = os.path.basename(file.filename) if file.filename else "unknown.pdf"
    safe_filename = safe_filename.replace("/", "").replace("\\", "").replace("..", "")

    if not safe_filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported for sovereign intelligence parsing."
        )

    # 2. DoS Fix: Check size before loading fully into memory
    if file.size and file.size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of 50 MB."
        )
        
    # Read content safely
    contents = await file.read()
    file_size = len(contents)
    
    # 3. File Signature Spoofing Fix: Verify Magic Bytes
    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file signature. File is not a genuine PDF."
        )

    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of 50 MB ({round(file_size / (1024*1024), 2)} MB)."
        )

    # Compute SHA-256 for duplicate detection
    file_hash = hashlib.sha256(contents).hexdigest()
    doc_repo = DocumentRepository(db)
    chunk_repo = ChunkRepository(db)

    existing_doc = await doc_repo.get_by_hash(file_hash)
    if existing_doc:
        return APIResponse.success(
            data=existing_doc,
            message="Document already processed in sovereign registry (Duplicate Hash Match)."
        )

    # Save to local uploads disk
    user_id_str = str(payload.get("sub"))
    doc_id = new_uuid()
    save_filename = f"{doc_id}_{safe_filename}"
    file_path = os.path.join(UPLOAD_DIR, save_filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        # Extract structure and recursive statutory chunks via PyMuPDF
        parsed = PDFService.process_pdf(file_path)
        meta = parsed["metadata"]
        raw_chunks = parsed["chunks"]

        # Instantiate Document dict
        doc_dict = {
            "_id": doc_id,
            "uploaded_by": user_id_str,
            "document_title": meta["title"] or file.filename.replace(".pdf", ""),
            "document_type": document_type.upper(),
            "file_path": file_path,
            "file_size_bytes": file_size,
            "file_hash": file_hash,
            "processing_status": "COMPLETED",
            "total_pages": meta["total_pages"],
            "ministry": ministry or meta["ministry"],
            "department": meta["department"],
            "om_number": meta["om_number"],
            "issue_date": meta["issue_date"],
            "language": meta["language"],
            "summary_json": {},
            "created_at": utcnow(),
            "updated_at": utcnow()
        }
        created_doc = await doc_repo.create(doc_dict)

        # Batch insert chunks & embeddings
        chunk_entities = []
        for rc in raw_chunks:
            # Generate local 768-dim embedding
            emb_vec = await EmbeddingService.generate_embedding(rc["chunk_content"])
            
            c_dict = {
                "_id": new_uuid(),
                "document_id": doc_id,
                "chunk_index": rc["chunk_index"],
                "chunk_content": rc["chunk_content"],
                "token_count": rc["token_count"],
                "section_reference": rc["section_reference"],
                "breadcrumb": rc["breadcrumb"],
                "page_number": rc["page_number"],
                "embedding": emb_vec,
                "embedding_model": "nomic-embed-text",
                "created_at": utcnow()
            }
            chunk_entities.append(c_dict)

        await chunk_repo.create_chunks_with_embeddings(chunk_entities)

        return APIResponse.success(
            data=created_doc,
            message="Document parsed, chunked, and embedded successfully"
        )
    except Exception as e:
        # Cleanup partial upload on failure
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Sovereign PDF parsing failed: {str(e)}")

# ------------------------------------------------------------------------------
# 2. Document Registry Queries
# ------------------------------------------------------------------------------
def recursive_vars(obj):
    if isinstance(obj, types.SimpleNamespace):
        return {k: recursive_vars(v) for k, v in vars(obj).items()}
    elif isinstance(obj, list):
        return [recursive_vars(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: recursive_vars(v) for k, v in obj.items()}
    return obj

@router.get("", response_model=APIResponse[list])
async def get_documents(
    user = RequireTrainer,
    db = Depends(get_db)
):
    repo = DocumentRepository(db)
    data = await repo.get_all()
    dict_data = [recursive_vars(d) for d in data]
    return APIResponse.success(data=dict_data, message="Documents retrieved successfully")

@router.get("/{document_id}", response_model=APIResponse[DocumentResponse])
async def get_document(
    document_id: str,
    user = RequireTrainer,
    db = Depends(get_db)
):
    repo = DocumentRepository(db)
    resp = await repo.get_by_id(str(document_id))
    if not resp:
        raise HTTPException(status_code=404, detail="Document not found")
    return APIResponse.success(data=resp, message="Document retrieved successfully")

@router.delete("/{document_id}", response_model=APIResponse[dict])
async def delete_document(
    document_id: str,
    user = RequireTrainer,
    db = Depends(get_db)
):
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(str(document_id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    await repo.delete(str(document_id))
    if getattr(doc, "file_path", None) and os.path.exists(getattr(doc, "file_path", None)):
        try:
            os.remove(getattr(doc, "file_path", None))
        except:
            pass
            
    return APIResponse.success(data={"deleted": True}, message="Document purged from sovereign registry")

# ------------------------------------------------------------------------------
# 3. AI Summarization Studio
# ------------------------------------------------------------------------------
@router.get("/{document_id}/summary", response_model=APIResponse[DocumentSummaryResponse])
async def get_document_summary(
    document_id: str,
    user = RequireTrainer,
    db = Depends(get_db)
):
    repo = DocumentRepository(db)
    doc = await repo.get_by_id(str(document_id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    summary_data = getattr(doc, "summary_json", {}) or {}
    if not summary_data:
        # Fallback generation
        chunk_repo = ChunkRepository(db)
        chunks = await chunk_repo.get_by_document_id(str(document_id))
        raw_chunks = [{"chunk_content": c.get("chunk_content", ""), "section_reference": c.get("section_reference", ""), "page_number": c.get("page_number", 1)} for c in chunks]
        summary_data = await RAGService.generate_document_summary(getattr(doc, "document_title", ""), getattr(doc, "ministry", ""), raw_chunks)
        await repo.update_summary(str(document_id), summary_data)

    resp = DocumentSummaryResponse(
        document_id=str(getattr(doc, "id", None)),
        document_title=getattr(doc, "document_title", ""),
        executive_summary=summary_data.get("executive_summary", ""),
        key_policy_changes=summary_data.get("key_policy_changes", []),
        important_clauses=summary_data.get("important_clauses", []),
        compliance_checklist=summary_data.get("compliance_checklist", []),
        action_points=summary_data.get("action_points", []),
        faqs=summary_data.get("faqs", [])
    )
    return APIResponse.success(data=resp, message="Document summary retrieved successfully")

# ------------------------------------------------------------------------------
# 4. Sovereign RAG Query Engine
# ------------------------------------------------------------------------------
@router.post("/query", response_model=APIResponse[RAGQueryResponse])
@rag_router.post("/query", response_model=APIResponse[RAGQueryResponse])
async def query_rag(
    request: RAGQueryRequest,
    user = RequireTrainer,
    db = Depends(get_db)
):
    """
    Executes grounded semantic vector search with statutory citations.
    """
    try:
        chunk_repo = ChunkRepository(db)
        doc_repo = DocumentRepository(db)

        # Generate query vector
        query_vec = await EmbeddingService.generate_embedding(request.query)

        # Retrieve Top-K matching chunks
        doc_id_str = str(request.document_id) if request.document_id else None
        matched_chunks = await chunk_repo.search_similar_chunks(
            query_vector=query_vec,
            top_k=request.top_k,
            document_id=doc_id_str
        )

        doc_title = "Central Civil Services Regulations"
        if doc_id_str:
            doc = await doc_repo.get_by_id(doc_id_str)
            if doc:
                doc_title = getattr(doc, "document_title", doc_title)

        # Grounded answer generation via Qwen 3
        rag_res = await RAGService.answer_query(
            query=request.query,
            retrieved_chunks=matched_chunks,
            document_title=doc_title
        )

        return APIResponse.success(
            data=rag_res,
            message="RAG query executed with verified citations"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Sovereign RAG execution failed: {str(e)}"
        )

# ------------------------------------------------------------------------------
# 5. AI MCQ Generation & Human Review Studio
# ------------------------------------------------------------------------------
@router.post("/generate", response_model=APIResponse[MCQGenerateResponse])
@mcq_router.post("/generate", response_model=APIResponse[MCQGenerateResponse])
async def generate_mcqs(
    request: MCQGenerateRequest,
    user = RequireTrainer,
    db = Depends(get_db)
):
    """
    Generates Bloom-classified MCQs (5, 10, or 20) with citations.
    """
    doc_repo = DocumentRepository(db)
    chunk_repo = ChunkRepository(db)

    doc_id_str = str(request.document_id)
    doc = await doc_repo.get_by_id(doc_id_str)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    chunks = await chunk_repo.get_by_document_id(doc_id_str)
    raw_chunks = [
        {
            "chunk_content": c.get("chunk_content", ""),
            "section_reference": c.get("section_reference", ""),
            "breadcrumb": c.get("breadcrumb", ""),
            "page_number": c.get("page_number", 1)
        }
        for c in chunks
    ]

    questions = MCQService.generate_mcqs_from_chunks(
        document_title=getattr(doc, "document_title", ""),
        ministry=getattr(doc, "ministry", ""),
        chunks=raw_chunks,
        num_questions=request.num_questions,
        target_bloom=request.target_bloom,
        target_difficulty=request.target_difficulty
    )

    # Cache drafted questions in session store
    for q in questions:
        DRAFT_MCQ_CACHE[q["id"]] = q

    return APIResponse.success(
        data={
            "document_id": str(getattr(doc, "id", None)),
            "document_title": getattr(doc, "document_title", ""),
            "total_generated": len(questions),
            "questions": questions
        },
        message=f"Generated {len(questions)} Bloom-classified MCQs successfully"
    )

@router.put("/mcq/{question_id}", response_model=APIResponse[MCQItem])
@mcq_router.put("/{question_id}", response_model=APIResponse[MCQItem])
async def update_draft_mcq(
    question_id: str,
    request: MCQUpdateRequest,
    user = RequireTrainer
):
    """
    Allows Trainer to modify stem, options, difficulty, Bloom level, or citations.
    """
    draft = DRAFT_MCQ_CACHE.get(question_id)
    if not draft:
        # Create or update entry
        draft = {"id": question_id, "source_page": 1, "status": "EDITED"}

    draft.update({
        "question": request.question,
        "options": [opt.model_dump() for opt in request.options],
        "correct_answer": request.correct_answer,
        "correct_option_index": request.correct_option_index,
        "difficulty": request.difficulty,
        "bloom_level": request.bloom_level,
        "explanation": request.explanation,
        "citation": request.citation,
        "status": "APPROVED"
    })
    DRAFT_MCQ_CACHE[question_id] = draft

    return APIResponse.success(
        data=draft,
        message="MCQ updated in Human Review Studio"
    )

@router.post("/publish", response_model=APIResponse[MCQPublishResponse])
@mcq_router.post("/publish", response_model=APIResponse[MCQPublishResponse])
async def publish_mcqs(
    request: MCQPublishRequest,
    user = RequireTrainer,
    db = Depends(get_db)
):
    """
    Publishes approved MCQs directly into the accredited Quiz & Question tables.
    """
    user_id_str = str(payload.get("sub"))
    quiz_id = new_uuid()

    quiz_dict = {
        "_id": quiz_id,
        "document_id": str(request.document_id),
        "created_by": user_id_str,
        "title": request.quiz_title,
        "quiz_type": "FORMATIVE",
        "passing_percentage": 60,
        "status": "PUBLISHED",
        "created_at": utcnow(),
        "updated_at": utcnow()
    }
    await db["quizzes"].insert_one(quiz_dict)

    q_dicts = []
    for q_item in request.questions:
        q_obj = {
            "_id": new_uuid(),
            "quiz_id": quiz_id,
            "competency_id": None,
            "question_stem": q_item.question,
            "bloom_level": q_item.bloom_level.upper() if q_item.bloom_level else "APPLY",
            "options": [opt.model_dump() for opt in q_item.options],
            "correct_option_index": q_item.correct_option_index,
            "pedagogical_rationale": q_item.explanation,
            "source_citation": q_item.citation,
            "created_at": utcnow(),
            "updated_at": utcnow()
        }
        q_dicts.append(q_obj)

    if q_dicts:
        await db["questions"].insert_many(q_dicts)

    return APIResponse.success(
        data={
            "message": f"Successfully published {len(q_dicts)} MCQs into accredited quiz repository",
            "published_count": len(q_dicts),
            "quiz_id": quiz_id
        },
        message="MCQs published to Mission Karmayogi assessment engine"
    )
