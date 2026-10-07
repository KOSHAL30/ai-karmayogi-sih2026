"""003_recommendation_learning_tables

Revision ID: 003_recommendation_learning_tables
Revises: 002_assessment_tables
Create Date: 2026-09-12 23:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "003_recommendation_learning_tables"
down_revision: Union[str, None] = "002_assessment_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. courses table
    op.create_table(
        "courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("competency_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("frac_competencies.id", ondelete="SET NULL"), nullable=True),
        sa.Column("igot_course_id", sa.String(100), nullable=False, unique=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ministry", sa.String(255), server_default="Department of Personnel and Training", nullable=False),
        sa.Column("duration_minutes", sa.Integer(), server_default="30", nullable=False),
        sa.Column("target_level", sa.Integer(), server_default="3", nullable=False),
        sa.Column("difficulty", sa.String(50), server_default="INTERMEDIATE", nullable=False),
        sa.Column("language", sa.String(50), server_default="English", nullable=False),
        sa.Column("tags", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("learning_outcomes", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("course_url", sa.Text(), nullable=False),
        sa.Column("is_published", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.CheckConstraint("target_level BETWEEN 1 AND 5", name="chk_target_level"),
    )
    op.create_index("idx_courses_competency", "courses", ["competency_id"])
    op.create_index("idx_courses_igot_id", "courses", ["igot_course_id"])
    op.create_index("idx_courses_published", "courses", ["is_published"])

    # 2. recommendations table
    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("competency_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("frac_competencies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("deficit_score", sa.Numeric(5, 2), nullable=False),
        sa.Column("priority", sa.Integer(), server_default="1", nullable=False),
        sa.Column("confidence", sa.Numeric(4, 3), server_default="0.850", nullable=False),
        sa.Column("estimated_improvement", sa.String(150), server_default="+1 Level", nullable=False),
        sa.Column("trajectory_stage", sa.String(50), server_default="RECOMMENDED_THIS_WEEK", nullable=False),
        sa.Column("explainable_rationale", sa.Text(), nullable=False),
        sa.Column("status", sa.String(50), server_default="ACTIVE", nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.CheckConstraint("deficit_score BETWEEN 0.00 AND 100.00", name="chk_deficit_score"),
        sa.CheckConstraint("status IN ('ACTIVE', 'ENROLLED', 'DISMISSED', 'COMPLETED')", name="chk_rec_status"),
    )
    op.create_index("idx_recommendations_user_status", "recommendations", ["user_id", "status"])
    op.create_index("idx_recommendations_course", "recommendations", ["course_id"])
    op.create_index("idx_recommendations_competency", "recommendations", ["competency_id"])

    # 3. learning_progress table
    op.create_table(
        "learning_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("progress_percentage", sa.Integer(), server_default="0", nullable=False),
        sa.Column("time_spent_minutes", sa.Integer(), server_default="0", nullable=False),
        sa.Column("completion_status", sa.String(50), server_default="IN_PROGRESS", nullable=False),
        sa.Column("last_accessed_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "course_id", name="uq_user_course_progress"),
        sa.CheckConstraint("progress_percentage BETWEEN 0 AND 100", name="chk_progress_pct"),
        sa.CheckConstraint("completion_status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED')", name="chk_completion_status"),
    )
    op.create_index("idx_progress_user", "learning_progress", ["user_id"])
    op.create_index("idx_progress_status", "learning_progress", ["completion_status"])


def downgrade() -> None:
    op.drop_table("learning_progress")
    op.drop_table("recommendations")
    op.drop_table("courses")
