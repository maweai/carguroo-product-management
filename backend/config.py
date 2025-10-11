"""
CarGuroo Backend Configuration
Story 1.1: Upload de Manuais Técnicos (PDF)
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # AWS S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Environment
    ENV: str = "development"

    # File Upload Limits
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB in bytes
    ALLOWED_FILE_EXTENSIONS: List[str] = [".pdf"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
