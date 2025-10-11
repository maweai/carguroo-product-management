"""
Audit Logging Service
Story 1.1: Upload de Manuais Técnicos (PDF) - Subtask 6.1, 6.2
"""
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional, Dict
import logging

from auth.models import AuditLog

logger = logging.getLogger(__name__)


class AuditService:
    """Service for audit logging - LGPD compliance"""

    @staticmethod
    async def log_document_upload(
        db: AsyncSession,
        user_id: UUID,
        document_id: UUID,
        metadata: Dict,
        ip_address: Optional[str] = None
    ) -> None:
        """
        Log document upload action to audit table

        Args:
            db: Database session
            user_id: UUID of admin who performed upload
            document_id: UUID of uploaded document
            metadata: Dict with filename, size_bytes, s3_key
            ip_address: Optional IP address of client

        Implementation from story context - interfaces.internal.AuditService
        Constraint: sec-4 (Audit Logging Required)
        """
        audit_log = AuditLog(
            user_id=user_id,
            action='document_uploaded',
            resource_type='document',
            resource_id=document_id,
            event_metadata=metadata,
            ip_address=ip_address
        )

        db.add(audit_log)
        # Don't commit here - will be committed with main transaction

        logger.info(
            f"Audit log created: action=document_uploaded, "
            f"user_id={user_id}, document_id={document_id}"
        )

    @staticmethod
    async def log_action(
        db: AsyncSession,
        user_id: Optional[UUID],
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        metadata: Optional[Dict] = None,
        ip_address: Optional[str] = None
    ) -> None:
        """
        Generic method to log any action to audit table

        Args:
            db: Database session
            user_id: UUID of user who performed action
            action: Action name (e.g., 'document_deleted', 'user_created')
            resource_type: Type of resource affected
            resource_id: ID of resource affected
            metadata: Additional metadata as JSON
            ip_address: Optional IP address of client
        """
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            event_metadata=metadata,
            ip_address=ip_address
        )

        db.add(audit_log)

        logger.info(f"Audit log created: action={action}, user_id={user_id}")


# Singleton instance
audit_service = AuditService()
