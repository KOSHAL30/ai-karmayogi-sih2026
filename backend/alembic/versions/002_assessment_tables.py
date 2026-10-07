"""002_assessment_tables

Revision ID: 002_assessment_tables
Revises: 001_auth_tables
Create Date: 2026-09-12 18:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "002_assessment_tables"
down_revision: Union[str, None] = "001_auth_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. frac_competencies table
    op.create_table(
        "frac_competencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("work_role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("work_roles.id", ondelete="SET NULL"), nullable=True),
        sa.Column("competency_type", sa.String(50), nullable=False),
        sa.Column("competency_name", sa.String(255), nullable=False),
        sa.Column("competency_code", sa.String(100), nullable=False, unique=True),
        sa.Column("mandated_level", sa.Integer(), server_default="3", nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("idx_frac_comp_code", "frac_competencies", ["competency_code"])
    op.create_index("idx_frac_comp_type", "frac_competencies", ["competency_type"])
    op.create_index("idx_frac_comp_work_role", "frac_competencies", ["work_role_id"])

    # 2. quizzes table
    op.create_table(
        "quizzes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("quiz_type", sa.String(50), server_default="DIAGNOSTIC", nullable=False),
        sa.Column("passing_percentage", sa.Integer(), server_default="60", nullable=False),
        sa.Column("status", sa.String(50), server_default="PUBLISHED", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("idx_quizzes_type", "quizzes", ["quiz_type"])
    op.create_index("idx_quizzes_status", "quizzes", ["status"])

    # 3. questions table
    op.create_table(
        "questions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("quiz_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("competency_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("frac_competencies.id", ondelete="SET NULL"), nullable=True),
        sa.Column("question_stem", sa.Text(), nullable=False),
        sa.Column("bloom_level", sa.String(50), server_default="APPLY", nullable=False),
        sa.Column("options", postgresql.JSONB(), nullable=False),
        sa.Column("correct_option_index", sa.Integer(), nullable=False),
        sa.Column("pedagogical_rationale", sa.Text(), nullable=False),
        sa.Column("source_citation", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("idx_questions_quiz_id", "questions", ["quiz_id"])
    op.create_index("idx_questions_competency_id", "questions", ["competency_id"])
    op.create_index("idx_questions_bloom", "questions", ["bloom_level"])

    # 4. quiz_attempts table
    op.create_table(
        "quiz_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("quiz_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("quizzes.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("score_achieved", sa.Integer(), nullable=False),
        sa.Column("total_questions", sa.Integer(), nullable=False),
        sa.Column("is_passed", sa.Boolean(), nullable=False),
        sa.Column("time_taken_seconds", sa.Integer(), nullable=False),
        sa.Column("answer_log", postgresql.JSONB(), nullable=False),
        sa.Column("attempted_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("idx_quiz_attempts_user_id", "quiz_attempts", ["user_id"])
    op.create_index("idx_quiz_attempts_quiz_id", "quiz_attempts", ["quiz_id"])


def downgrade() -> None:
    op.drop_table("quiz_attempts")
    op.drop_table("questions")
    op.drop_table("quizzes")
    op.drop_table("frac_competencies")
