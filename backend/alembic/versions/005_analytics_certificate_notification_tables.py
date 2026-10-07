"""create certificates and enhance notifications table

Revision ID: 005
Revises: 004
Create Date: 2026-09-13 09:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers, used by Alembic.
revision: str = '005_analytics_certificate_notification_tables'
down_revision: Union[str, None] = '004_document_rag_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create certificates table
    op.create_table(
        'certificates',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('certificate_number', sa.String(length=100), nullable=False, unique=True),
        sa.Column('certificate_type', sa.String(length=50), nullable=False, server_default='COURSE_COMPLETION'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('issuing_authority', sa.String(length=255), nullable=False, server_default='Mission Karmayogi Bharat'),
        sa.Column('ministry', sa.String(length=255), nullable=False, server_default='Government of India'),
        sa.Column('issued_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('verification_code', sa.String(length=100), nullable=False, unique=True),
        sa.Column('verification_url', sa.String(length=255), nullable=False),
        sa.Column('qr_code_data', sa.Text(), nullable=False),
        sa.Column('metadata', JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )
    op.create_index('ix_certificates_user_id', 'certificates', ['user_id'])
    op.create_index('ix_certificates_number', 'certificates', ['certificate_number'])
    op.create_index('ix_certificates_type', 'certificates', ['certificate_type'])

    # 2. Add columns to notifications table if not already present
    conn = op.get_bind()
    # Safely inspect and add priority & action_url
    try:
        op.add_column('notifications', sa.Column('priority', sa.String(length=20), server_default='NORMAL', nullable=False))
    except Exception:
        pass

    try:
        op.add_column('notifications', sa.Column('action_url', sa.String(length=255), nullable=True))
    except Exception:
        pass


def downgrade() -> None:
    op.drop_index('ix_certificates_type', table_name='certificates')
    op.drop_index('ix_certificates_number', table_name='certificates')
    op.drop_index('ix_certificates_user_id', table_name='certificates')
    op.drop_table('certificates')
    try:
        op.drop_column('notifications', 'action_url')
        op.drop_column('notifications', 'priority')
    except Exception:
        pass
