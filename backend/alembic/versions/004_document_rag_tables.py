"""004_document_rag_tables

Revision ID: 004_document_rag_tables
Revises: 003_recommendation_learning_tables
Create Date: 2026-09-13 00:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = "004_document_rag_tables"
down_revision: Union[str, None] = "003_recommendation_learning_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable pgvector extension if not exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2. documents table
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("document_title", sa.String(255), nullable=False),
        sa.Column("document_type", sa.String(50), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("file_size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("file_hash", sa.String(64), nullable=False),
        sa.Column("processing_status", sa.String(50), server_default="PENDING", nullable=False),
        sa.Column("total_pages", sa.Integer(), server_default="0", nullable=False),
        sa.Column("ministry", sa.String(255), server_default="Department of Personnel & Training", nullable=False),
        sa.Column("department", sa.String(255), nullable=True),
        sa.Column("om_number", sa.String(100), nullable=True),
        sa.Column("issue_date", sa.String(50), nullable=True),
        sa.Column("language", sa.String(50), server_default="English", nullable=False),
        sa.Column("summary", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.CheckConstraint("document_type IN ('ACT', 'RULE', 'CIRCULAR', 'OM', 'MANUAL', 'TRAINING_COLLATERAL')", name="chk_document_type"),
        sa.CheckConstraint("processing_status IN ('PENDING', 'PARSING', 'CHUNKED', 'EMBEDDED', 'FAILED', 'PROCESSED')", name="chk_doc_status"),
    )
    op.create_index("idx_documents_uploaded_by", "documents", ["uploaded_by"])
    op.create_index("idx_documents_status", "documents", ["processing_status"])
    op.create_index("idx_documents_hash", "documents", ["file_hash"])

    # 3. document_chunks table
    op.create_table(
        "document_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("chunk_content", sa.Text(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False),
        sa.Column("section_reference", sa.String(150), nullable=True),
        sa.Column("breadcrumb", sa.String(255), server_default="Document", nullable=True),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("document_id", "chunk_index", name="uq_doc_chunk_index"),
    )
    op.create_index("idx_chunks_doc_id", "document_chunks", ["document_id"])
    op.create_index("idx_chunks_section", "document_chunks", ["section_reference"])

    # 4. embeddings table
    op.create_table(
        "embeddings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("chunk_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("document_chunks.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("embedding_vector_768", Vector(768), nullable=False),
        sa.Column("model_version", sa.String(100), server_default="nomic-embed-text", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("idx_embeddings_chunk_id", "embeddings", ["chunk_id"])


def downgrade() -> None:
    op.drop_table("embeddings")
    op.drop_table("document_chunks")
    op.drop_table("documents")
