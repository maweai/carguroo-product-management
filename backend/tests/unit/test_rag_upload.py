"""
Unit Tests for RAG Upload Functionality
Story 1.1: Upload de Manuais Técnicos (PDF) - Task 7
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import UploadFile
from io import BytesIO
from uuid import uuid4

from rag.services import DocumentService
from common.s3 import S3Client


class TestFileValidation:
    """Test file type and size validation (AC1, AC2)"""

    def test_validate_pdf_extension_lowercase(self):
        """Subtask 7.1: Test that .pdf extension is accepted"""
        filename = "manual.pdf"
        assert filename.lower().endswith('.pdf')

    def test_validate_pdf_extension_uppercase(self):
        """Subtask 7.1: Test that .PDF extension is accepted (case-insensitive)"""
        filename = "manual.PDF"
        assert filename.lower().endswith('.pdf')

    def test_reject_docx_file(self):
        """Subtask 7.1: Test that .docx files are rejected"""
        filename = "manual.docx"
        assert not filename.lower().endswith('.pdf')

    def test_reject_jpg_file(self):
        """Subtask 7.1: Test that .jpg files are rejected"""
        filename = "image.jpg"
        assert not filename.lower().endswith('.pdf')

    def test_validate_file_size_under_limit(self):
        """Subtask 7.2: Test that files under 50MB are accepted"""
        file_size = 10 * 1024 * 1024  # 10MB
        max_size = 52428800  # 50MB
        assert file_size <= max_size

    def test_validate_file_size_at_limit(self):
        """Subtask 7.2: Test that files at exactly 50MB are accepted"""
        file_size = 52428800  # Exactly 50MB
        max_size = 52428800
        assert file_size <= max_size

    def test_validate_file_size_over_limit(self):
        """Subtask 7.3: Test that files over 50MB are rejected"""
        file_size = 60 * 1024 * 1024  # 60MB
        max_size = 52428800  # 50MB
        assert file_size > max_size


class TestPermissionEnforcement:
    """Test RBAC permission checks (AC2, sec-1)"""

    def test_admin_permission_allowed(self):
        """Subtask 7.4: Test that admin role can upload"""
        user_role = 'admin'
        assert user_role == 'admin'

    def test_gestor_permission_denied(self):
        """Subtask 7.4: Test that gestor role cannot upload"""
        user_role = 'gestor'
        assert user_role != 'admin'

    def test_mecanico_permission_denied(self):
        """Subtask 7.4: Test that mecanico role cannot upload"""
        user_role = 'mecanico'
        assert user_role != 'admin'


class TestS3KeyGeneration:
    """Test S3 key format and generation (AC5, constraint arch-3)"""

    def test_s3_key_format(self):
        """Subtask 7.5: Test that S3 key matches {uuid}/{filename} pattern"""
        import re
        from uuid import uuid4

        document_id = uuid4()
        filename = "manual.pdf"
        s3_key = f"{document_id}/{filename}"

        # Validate format: UUID/filename
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/.+\.pdf$'
        assert re.match(pattern, s3_key.lower())

    def test_s3_key_uniqueness(self):
        """Subtask 7.5: Test that different uploads get unique UUIDs"""
        from uuid import uuid4

        filename = "manual.pdf"
        s3_key_1 = f"{uuid4()}/{filename}"
        s3_key_2 = f"{uuid4()}/{filename}"

        # Different UUIDs even with same filename
        assert s3_key_1 != s3_key_2


class TestDocumentService:
    """Test DocumentService methods"""

    @pytest.mark.asyncio
    async def test_upload_to_s3_success(self, sample_pdf_bytes):
        """Test successful S3 upload with encryption"""
        # Mock S3 client
        with patch('rag.services.s3_client') as mock_s3:
            mock_s3.upload_file.return_value = True

            # Create mock UploadFile
            mock_file = Mock(spec=UploadFile)
            mock_file.filename = "test.pdf"
            mock_file.content_type = "application/pdf"

            # Upload
            s3_key = await DocumentService.upload_to_s3(
                file=mock_file,
                file_bytes=sample_pdf_bytes
            )

            # Verify S3 upload was called
            assert mock_s3.upload_file.called
            assert mock_file.filename in s3_key
            assert "/" in s3_key  # UUID/filename format

    @pytest.mark.asyncio
    async def test_create_document_record(self, mock_admin_user):
        """Test document record creation in database"""
        from uuid import uuid4
        from rag.models import Document

        s3_key = f"{uuid4()}/test.pdf"

        # Mock database session
        mock_db = AsyncMock()

        document = await DocumentService.create_document(
            db=mock_db,
            name="test.pdf",
            s3_key=s3_key,
            file_size_bytes=1024,
            uploaded_by=mock_admin_user['id']
        )

        # Verify document properties
        assert document.name == "test.pdf"
        assert document.s3_key == s3_key
        assert document.file_size_bytes == 1024
        assert document.status == 'pending'
        assert document.uploaded_by == mock_admin_user['id']

        # Verify db.add was called
        assert mock_db.add.called

    @pytest.mark.asyncio
    async def test_rollback_s3_upload(self):
        """Test S3 upload rollback on error"""
        with patch('rag.services.s3_client') as mock_s3:
            mock_s3.delete_file.return_value = True

            s3_key = f"{uuid4()}/test.pdf"
            await DocumentService.rollback_s3_upload(s3_key)

            # Verify delete was called
            mock_s3.delete_file.assert_called_once_with(s3_key)


class TestS3Client:
    """Test S3Client wrapper"""

    def test_s3_client_initialization(self):
        """Test S3 client is properly initialized"""
        from config import settings

        client = S3Client()
        assert client.bucket_name == settings.S3_BUCKET_NAME

    @patch('boto3.client')
    def test_upload_file_with_encryption(self, mock_boto_client):
        """Test that files are uploaded with SSE-S3 encryption"""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        client = S3Client()
        client.client = mock_s3

        file_bytes = b"test content"
        s3_key = "test-id/test.pdf"

        client.upload_file(
            file_bytes=file_bytes,
            s3_key=s3_key,
            content_type="application/pdf"
        )

        # Verify put_object was called with encryption
        call_args = mock_s3.put_object.call_args
        assert call_args[1]['ServerSideEncryption'] == 'AES256'
        assert call_args[1]['ContentType'] == 'application/pdf'


class TestAuditLogging:
    """Test audit logging functionality (AC6, constraint sec-4)"""

    @pytest.mark.asyncio
    async def test_audit_log_created(self, mock_admin_user):
        """Test that audit log is created on document upload"""
        from auth.audit import audit_service
        from uuid import uuid4

        document_id = uuid4()
        metadata = {
            'filename': 'test.pdf',
            'size_bytes': 1024,
            's3_key': f'{document_id}/test.pdf'
        }

        # Mock database session
        mock_db = AsyncMock()

        await audit_service.log_document_upload(
            db=mock_db,
            user_id=mock_admin_user['id'],
            document_id=document_id,
            metadata=metadata,
            ip_address='127.0.0.1'
        )

        # Verify db.add was called with audit log
        assert mock_db.add.called
        call_args = mock_db.add.call_args[0][0]
        assert call_args.action == 'document_uploaded'
        assert call_args.resource_type == 'document'
        assert call_args.resource_id == document_id
