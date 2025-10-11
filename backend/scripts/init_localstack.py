"""
Script to initialize LocalStack S3 bucket for development
Story 1.1: Upload de Manuais Técnicos (PDF)
"""
import boto3
import os
from botocore.exceptions import ClientError

def init_s3_bucket():
    """Create S3 bucket in LocalStack for development"""

    # Configure S3 client for LocalStack
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localstack:4566',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )

    bucket_name = os.getenv('S3_BUCKET_NAME', 'carguroo-documents-dev')

    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✓ Bucket '{bucket_name}' already exists")
    except ClientError:
        # Create bucket
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"✓ Created bucket '{bucket_name}'")

        # Enable versioning
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print(f"✓ Enabled versioning on '{bucket_name}'")

        # Configure CORS for frontend uploads
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'POST', 'PUT', 'DELETE'],
                'AllowedOrigins': ['http://localhost:3000', 'http://localhost:8000'],
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3000
            }]
        }
        s3_client.put_bucket_cors(
            Bucket=bucket_name,
            CORSConfiguration=cors_configuration
        )
        print(f"✓ Configured CORS on '{bucket_name}'")

if __name__ == "__main__":
    init_s3_bucket()
    print("\n✅ LocalStack S3 initialization complete!")
