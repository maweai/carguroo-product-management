"""
RAG Module Database Models
Story 1.1: Upload de Manuais Técnicos (PDF)
"""
from sqlalchemy import Column, String, BigInteger, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from database import Base


class Document(Base):
    """
    Documents table - stores metadata for uploaded PDF manuals

    Schema from solution-architecture.md lines 677-695
    """
    __tablename__ = "documents"
    __table_args__ = {"schema": "rag"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    s3_key = Column(String(500), nullable=False)
    file_size_bytes = Column(BigInteger)
    status = Column(
        String(50),
        nullable=False,
        default="pending",
        server_default="pending"
    )
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    total_chunks = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Document(id={self.id}, name={self.name}, status={self.status})>"


class Chunk(Base):
    """
    Chunks table - stores metadata for document chunks
    (Vectors are stored in Qdrant)

    Schema from solution-architecture.md lines 697-712
    """
    __tablename__ = "chunks"
    __table_args__ = {"schema": "rag"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rag.documents.id", ondelete="CASCADE"),
        nullable=False
    )
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    section_title = Column(String(500), nullable=True)
    qdrant_point_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Chunk(id={self.id}, document_id={self.document_id}, chunk_index={self.chunk_index})>"
