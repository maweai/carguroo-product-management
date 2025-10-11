"""
S3 Client Wrapper
Story 1.1: Upload de Manuais Técnicos (PDF)
"""
import boto3
from botocore.exceptions import ClientError
from config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class S3Client:
    """Wrapper for AWS S3 operations"""

    def __init__(self):
        """Initialize S3 client with configuration from settings"""
        client_config = {
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'region_name': settings.AWS_REGION
        }

        # Use LocalStack endpoint for development
        if settings.ENV == "development":
            client_config['endpoint_url'] = 'http://localstack:4566'

        self.client = boto3.client('s3', **client_config)
        self.bucket_name = settings.S3_BUCKET_NAME

    def upload_file(
        self,
        file_bytes: bytes,
        s3_key: str,
        content_type: str = 'application/pdf'
    ) -> bool:
        """
        Upload file to S3 with SSE-S3 encryption

        Args:
            file_bytes: File content as bytes
            s3_key: S3 key (path) for the file
            content_type: MIME type of the file

        Returns:
            bool: True if upload successful

        Raises:
            ClientError: If S3 upload fails
        """
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_bytes,
                ContentType=content_type,
                ServerSideEncryption='AES256'  # SSE-S3 encryption
            )
            logger.info(f"Successfully uploaded file to S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {s3_key}, error: {str(e)}")
            raise

    def delete_file(self, s3_key: str) -> bool:
        """
        Delete file from S3

        Args:
            s3_key: S3 key (path) of the file to delete

        Returns:
            bool: True if deletion successful
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            logger.info(f"Successfully deleted file from S3: {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {s3_key}, error: {str(e)}")
            return False

    def file_exists(self, s3_key: str) -> bool:
        """
        Check if file exists in S3

        Args:
            s3_key: S3 key (path) to check

        Returns:
            bool: True if file exists
        """
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError:
            return False

    def get_file_metadata(self, s3_key: str) -> Optional[dict]:
        """
        Get file metadata from S3

        Args:
            s3_key: S3 key (path) of the file

        Returns:
            dict: File metadata including ServerSideEncryption
        """
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response
        except ClientError as e:
            logger.error(f"Failed to get file metadata from S3: {s3_key}, error: {str(e)}")
            return None


# Singleton instance
s3_client = S3Client()
