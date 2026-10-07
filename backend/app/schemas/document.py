# ==============================================================================
# AI KARMAYOGI — DOCUMENT INTELLIGENCE & RAG PYDANTIC SCHEMAS
# Request & Response Models for Uploads, Sovereign RAG, Summaries & MCQs
# ==============================================================================

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class DocumentChunkItem(BaseModel):
    chunk_index: int
    chunk_content: str
    token_count: int
    section_reference: Optional[str] = None
    breadcrumb: Optional[str] = None
    page_number: Optional[int] = None

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: uuid.UUID
    document_title: str
    document_type: str
    file_size_bytes: int
    file_hash: str
    processing_status: str
    total_pages: int
    ministry: str
    department: Optional[str] = None
    om_number: Optional[str] = None
    issue_date: Optional[str] = None
    language: str
    created_at: datetime
    total_chunks: int = 0
    chunks: Optional[List[DocumentChunkItem]] = None

    class Config:
        from_attributes = True

class ImportantClause(BaseModel):
    clause: str
    page: int
    description: str

class FAQItem(BaseModel):
    question: str
    answer: str
    citation: str

class DocumentSummaryResponse(BaseModel):
    document_id: str
    document_title: str
    executive_summary: str
    key_policy_changes: List[str]
    important_clauses: List[ImportantClause]
    compliance_checklist: List[str]
    action_points: List[str]
    faqs: List[FAQItem]

class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    document_id: Optional[uuid.UUID] = None
    top_k: int = Field(default=5, ge=1, le=10)

class CitationItem(BaseModel):
    source_id: int
    document_title: str
    section_reference: str
    breadcrumb: str
    page_number: int
    relevance_score: float
    excerpt: str

class RAGQueryResponse(BaseModel):
    answer: str
    citations: List[CitationItem]
    confidence_score: float
    chunks_evaluated: int

class MCQOption(BaseModel):
    id: str
    text: str

class MCQItem(BaseModel):
    id: str
    question: str
    options: List[MCQOption]
    correct_answer: str
    correct_option_index: int
    difficulty: str
    bloom_level: str
    explanation: str
    citation: str
    source_page: int
    status: str = "DRAFT"
    document_title: Optional[str] = None

class MCQGenerateRequest(BaseModel):
    document_id: uuid.UUID
    num_questions: int = Field(default=5, ge=1, le=20)
    target_bloom: Optional[str] = None
    target_difficulty: Optional[str] = None

class MCQGenerateResponse(BaseModel):
    document_id: str
    document_title: str
    total_generated: int
    questions: List[MCQItem]

class MCQUpdateRequest(BaseModel):
    question: str
    options: List[MCQOption]
    correct_answer: str
    correct_option_index: int
    difficulty: str
    bloom_level: str
    explanation: str
    citation: str

class MCQPublishRequest(BaseModel):
    document_id: uuid.UUID
    quiz_title: str
    questions: List[MCQItem]

class MCQPublishResponse(BaseModel):
    message: str
    published_count: int
    quiz_id: str
