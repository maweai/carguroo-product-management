"""
Celery Worker Configuration
Story 1.1: Upload de Manuais Técnicos (PDF)
"""
from celery import Celery
from config import settings

# Create Celery app
celery_app = Celery(
    'carguroo',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=1800,  # 30 minutes
    task_soft_time_limit=1500,  # 25 minutes
)


@celery_app.task(bind=True, max_retries=3, name='process_document_task')
def process_document_task(self, document_id: str):
    """
    Process uploaded document asynchronously

    This is a STUB for Story 1.1. Actual implementation will be in US-RAG-02/03.
    Currently just logs that task was triggered.

    Args:
        document_id: UUID of document to process

    Note from story context:
        "Task implementation will be in US-RAG-02/03. For this story, just trigger it (stub OK)."
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"[STUB] Processing document: {document_id}")
    logger.info(f"[STUB] Document processing will be implemented in US-RAG-02/03")
    logger.info(f"[STUB] Future steps: Extract text → Chunk → Generate embeddings → Index in Qdrant")

    # Return stub result
    return {
        'document_id': document_id,
        'status': 'stub_completed',
        'message': 'Document processing stub executed. Full implementation in US-RAG-02/03'
    }
