"""
RAG Module API Routes
Story 1.1: Upload de Manuais Técnicos (PDF)
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
import logging

from database import get_db
from rag.services import DocumentService
from auth.audit import audit_service
from worker import process_document_task
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])


# Mock dependency for current user (will be replaced with real auth in Epic 5)
async def get_current_user(request: Request):
    """Mock current user for development - returns admin user"""
    # This is a stub - real implementation will be in Epic 5 (Auth)
    return {
        'id': UUID('00000000-0000-0000-0000-000000000001'),
        'role': 'admin',
        'name': 'Admin User'
    }


@router.post("/upload", status_code=202)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """
    Upload PDF document with validation and S3 storage

    Story 1.1: Task 1 - Criar rota de upload de documentos
    Subtasks 1.1-1.4: File validation, size check, permission check, error handling

    Acceptance Criteria: AC1, AC2, AC5, AC6
    Constraints: sec-1, sec-2, sec-3, db-2
    """
    # Subtask 1.3: Verify admin permission (AC2, sec-1)
    if current_user['role'] != 'admin':
        logger.warning(f"Upload attempt by non-admin user: {current_user['id']}")
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions. Only admins can upload documents."
        )

    # Subtask 1.1: Validate file type (AC2, sec-2)
    if not file.filename.lower().endswith('.pdf'):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    # Read file bytes
    file_bytes = await file.read()

    # Subtask 1.2: Validate file size (AC1, AC2, sec-2)
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE:
        logger.warning(
            f"File too large: {len(file_bytes)} bytes (max: {settings.MAX_UPLOAD_SIZE})"
        )
        raise HTTPException(
            status_code=413,
            detail=f"File too large (max {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB)"
        )

    try:
        # Subtask 2.1-2.4: Upload to S3 with encryption (AC5, Task 2)
        s3_key = await DocumentService.upload_to_s3(file, file_bytes)

        # Subtask 3.1-3.3: Create DB record with transaction handling (AC6, Task 3)
        document = await DocumentService.create_document(
            db=db,
            name=file.filename,
            s3_key=s3_key,
            file_size_bytes=len(file_bytes),
            uploaded_by=current_user['id']
        )

        # Subtask 6.1-6.2: Audit logging (AC6, Task 6)
        await audit_service.log_document_upload(
            db=db,
            user_id=current_user['id'],
            document_id=document.id,
            metadata={
                'filename': file.filename,
                'size_bytes': len(file_bytes),
                's3_key': s3_key
            },
            ip_address=request.client.host if request else None
        )

        # Commit transaction (Task 3, db-2 constraint)
        await db.commit()

        # Subtask 4.1: Trigger async processing (AC4, Task 4)
        process_document_task.delay(str(document.id))

        # Subtask 4.3: Calculate processing ETA (Task 4)
        processing_eta_seconds = int(len(file_bytes) / 1024 / 1024 / 10 * 60)  # ~1 min per 10MB

        # Subtask 4.2: Return 202 Accepted (not 200 OK) (arch-2 constraint)
        return {
            'document_id': str(document.id),
            'name': document.name,
            'size_bytes': document.file_size_bytes,
            'status': document.status,
            'uploaded_at': document.uploaded_at.isoformat(),
            'processing_eta_seconds': processing_eta_seconds
        }

    except Exception as e:
        # Subtask 3.3 & 2.3: Rollback handling (db-2 constraint)
        logger.error(f"Upload failed: {str(e)}")
        await db.rollback()

        # If S3 upload succeeded but DB failed, delete S3 file
        if 's3_key' in locals():
            await DocumentService.rollback_s3_upload(s3_key)

        # Subtask 1.4: Return appropriate error
        raise HTTPException(
            status_code=500,
            detail="Internal server error during upload"
        )


@router.get("", status_code=200)
async def list_documents(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100, description="Pagination limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List documents with optional status filter and pagination

    Story 1.1: Task 5 - Criar endpoint de listagem de documentos
    Subtasks 5.1-5.3: Filter, order, pagination

    Acceptance Criteria: AC4
    """
    # Subtask 5.1: Implement filtering by status
    # Subtask 5.2: Order by uploaded_at DESC
    # Subtask 5.3: Pagination
    documents, total = await DocumentService.list_documents(
        db=db,
        status=status,
        limit=limit,
        offset=offset
    )

    # Format response
    return {
        'documents': [
            {
                'id': str(doc.id),
                'name': doc.name,
                'size_bytes': doc.file_size_bytes,
                'status': doc.status,
                'uploaded_at': doc.uploaded_at.isoformat(),
                'uploaded_by': str(doc.uploaded_by) if doc.uploaded_by else None
            }
            for doc in documents
        ],
        'total': total,
        'limit': limit,
        'offset': offset
    }
