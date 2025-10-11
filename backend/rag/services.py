"""
RAG Module Services
Story 1.1: Upload de Manuais Técnicos (PDF)
"""
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID, uuid4
import logging

from rag.models import Document
from common.s3 import s3_client
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document operations"""

    @staticmethod
    async def upload_to_s3(file: UploadFile, file_bytes: bytes) -> str:
        """
        Upload file to S3 with SSE-S3 encryption

        Args:
            file: FastAPI UploadFile object
            file_bytes: File content as bytes

        Returns:
            str: S3 key (path) where file was uploaded

        Raises:
            ClientError: If S3 upload fails

        Implementation from story context - interfaces.internal.DocumentService
        """
        # Generate unique S3 key: {uuid}/{original_filename}
        document_id = uuid4()
        s3_key = f"{document_id}/{file.filename}"

        # Upload to S3 with encryption
        s3_client.upload_file(
            file_bytes=file_bytes,
            s3_key=s3_key,
            content_type=file.content_type or 'application/pdf'
        )

        logger.info(f"File uploaded to S3: {s3_key} (size: {len(file_bytes)} bytes)")
        return s3_key

    @staticmethod
    async def create_document(
        db: AsyncSession,
        name: str,
        s3_key: str,
        file_size_bytes: int,
        uploaded_by: UUID
    ) -> Document:
        """
        Create document record in rag.documents table

        Args:
            db: Database session
            name: Original filename
            s3_key: S3 key where file is stored
            file_size_bytes: File size in bytes
            uploaded_by: UUID of user who uploaded

        Returns:
            Document: Created document ORM instance

        Raises:
            Exception: If database insertion fails

        Implementation from story context - interfaces.internal.DocumentService
        """
        # Extract document_id from s3_key (format: {uuid}/{filename})
        document_id = UUID(s3_key.split('/')[0])

        document = Document(
            id=document_id,
            name=name,
            s3_key=s3_key,
            file_size_bytes=file_size_bytes,
            status='pending',  # Initial status
            uploaded_by=uploaded_by
        )

        db.add(document)
        await db.flush()  # Flush to get ID, but don't commit yet

        logger.info(f"Created document record: {document.id} (status: pending)")
        return document

    @staticmethod
    async def list_documents(
        db: AsyncSession,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Document], int]:
        """
        List documents with optional status filter and pagination

        Args:
            db: Database session
            status: Optional status filter (pending, processing, completed, error)
            limit: Maximum number of documents to return
            offset: Number of documents to skip

        Returns:
            tuple: (list of documents, total count)
        """
        # Build query
        query = select(Document)

        if status:
            query = query.where(Document.status == status)

        # Order by uploaded_at DESC (newest first)
        query = query.order_by(Document.uploaded_at.desc())

        # Get total count
        count_query = select(func.count()).select_from(Document)
        if status:
            count_query = count_query.where(Document.status == status)

        result = await db.execute(count_query)
        total = result.scalar_one()

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        result = await db.execute(query)
        documents = result.scalars().all()

        logger.info(f"Listed {len(documents)} documents (total: {total}, status: {status})")
        return documents, total

    @staticmethod
    async def rollback_s3_upload(s3_key: str) -> None:
        """
        Rollback S3 upload by deleting the file

        Args:
            s3_key: S3 key of file to delete
        """
        s3_client.delete_file(s3_key)
        logger.info(f"Rolled back S3 upload: {s3_key}")


# Fix import for func
from sqlalchemy import func
