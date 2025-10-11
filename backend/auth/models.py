"""
Auth Module Database Models
Story 1.1: Upload de Manuais Técnicos (PDF) - Required for user references
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.sql import func
import uuid

from database import Base


class Dealership(Base):
    """
    Dealerships table - stores dealership/concessionária information

    Schema from solution-architecture.md lines 665-673
    """
    __tablename__ = "dealerships"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    region = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Dealership(id={self.id}, name={self.name})>"


class User(Base):
    """
    Users table - stores user information and roles

    Schema from solution-architecture.md lines 647-663
    """
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    role = Column(
        String(50),
        nullable=False,
        index=True
    )  # admin, gestor, mecanico
    dealership_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.dealerships.id"),
        nullable=True
    )
    is_active = Column(Boolean, default=True, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, cpf={self.cpf}, role={self.role})>"


class AuditLog(Base):
    """
    Audit log table - stores all system actions for LGPD compliance

    Schema from solution-architecture.md lines 975-989
    """
    __tablename__ = "audit_log"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id"),
        nullable=True,
        index=True
    )
    action = Column(String(100), nullable=False)  # e.g., 'document_uploaded'
    resource_type = Column(String(100), nullable=True)  # e.g., 'document'
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    event_metadata = Column(JSONB, nullable=True)  # {filename, size_bytes, s3_key, etc.}
    ip_address = Column(INET, nullable=True)
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, timestamp={self.timestamp})>"
