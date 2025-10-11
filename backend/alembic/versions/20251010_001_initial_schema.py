"""Initial schema: auth and rag modules

Revision ID: 001_initial_schema
Revises:
Create Date: 2025-10-10

Story 1.1: Upload de Manuais Técnicos (PDF)
Creates schemas and tables for:
- auth.dealerships
- auth.users
- auth.audit_log
- rag.documents
- rag.chunks
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create schemas
    op.execute('CREATE SCHEMA IF NOT EXISTS auth')
    op.execute('CREATE SCHEMA IF NOT EXISTS rag')

    # Create auth.dealerships table
    op.create_table(
        'dealerships',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('region', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        schema='auth'
    )

    # Create auth.users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('cpf', sa.String(11), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=True, unique=True),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('dealership_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['dealership_id'], ['auth.dealerships.id']),
        sa.CheckConstraint("role IN ('admin', 'gestor', 'mecanico')", name='users_role_check'),
        schema='auth'
    )
    op.create_index('idx_users_cpf', 'users', ['cpf'], schema='auth')
    op.create_index('idx_users_role', 'users', ['role'], schema='auth')

    # Create auth.audit_log table
    op.create_table(
        'audit_log',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(100), nullable=True),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('event_metadata', postgresql.JSONB, nullable=True),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['auth.users.id']),
        schema='auth'
    )
    op.create_index('idx_audit_user', 'audit_log', ['user_id'], schema='auth')
    op.create_index('idx_audit_timestamp', 'audit_log', ['timestamp'], schema='auth')

    # Create rag.documents table
    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('s3_key', sa.String(500), nullable=False),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('uploaded_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_chunks', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['uploaded_by'], ['auth.users.id']),
        sa.CheckConstraint("status IN ('pending', 'processing', 'completed', 'error')", name='documents_status_check'),
        schema='rag'
    )
    op.create_index('idx_documents_status', 'documents', ['status'], schema='rag')

    # Create rag.chunks table
    op.create_table(
        'chunks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('chunk_text', sa.Text(), nullable=False),
        sa.Column('page_number', sa.Integer(), nullable=True),
        sa.Column('section_title', sa.String(500), nullable=True),
        sa.Column('qdrant_point_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['document_id'], ['rag.documents.id'], ondelete='CASCADE'),
        schema='rag'
    )
    op.create_index('idx_chunks_document_id', 'chunks', ['document_id'], schema='rag')
    op.create_index('idx_chunks_qdrant_point_id', 'chunks', ['qdrant_point_id'], schema='rag')


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('chunks', schema='rag')
    op.drop_table('documents', schema='rag')
    op.drop_table('audit_log', schema='auth')
    op.drop_table('users', schema='auth')
    op.drop_table('dealerships', schema='auth')

    # Drop schemas
    op.execute('DROP SCHEMA IF EXISTS rag CASCADE')
    op.execute('DROP SCHEMA IF EXISTS auth CASCADE')
