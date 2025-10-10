# CarGuroo - Technical Specifications

**Project:** CarGuroo MVP
**Date:** 2025-10-10
**Author:** Allan
**Status:** Ready for Development
**References:**
- PRD: `PRD-CarGuroo-2025-10-10.md`
- Epics: `epics-CarGuroo-2025-10-10.md`
- Architecture: `solution-architecture.md`

---

## Document Purpose

Este documento fornece especificações técnicas detalhadas para implementação dos 5 epics do CarGuroo MVP. Cada epic inclui:
- API endpoints (formato OpenAPI)
- Fluxos de dados e integrações
- Code patterns e exemplos
- Database schemas (referência para `solution-architecture.md`)
- Testing strategies
- Implementation notes para BMAD + Claude Code

---

## Table of Contents

1. [Epic 1: RAG Infrastructure](#epic-1-rag-infrastructure)
2. [Epic 2: Copiloto MVP](#epic-2-copiloto-mvp)
3. [Epic 3: Sistema de Avaliação](#epic-3-sistema-de-avaliação)
4. [Epic 4: Dashboard](#epic-4-dashboard)
5. [Epic 5: Auth & Observability](#epic-5-auth--observability)
6. [Shared Components](#shared-components)
7. [Testing Strategy](#testing-strategy)

---

## Epic 1: RAG Infrastructure

**Goal**: Infraestrutura compartilhada de Retrieval Augmented Generation

**Stories**: US-RAG-01 a US-RAG-09 (9 stories)

**Priority**: CRÍTICA (deve ser primeira a ser implementada)

---

### 1.1 Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Module                               │
│                                                             │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐  │
│  │Ingestion │→ │Processing │→ │Embedding │→ │Indexing  │  │
│  │          │  │           │  │          │  │          │  │
│  └────┬─────┘  └─────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │              │             │        │
│       ▼              ▼              ▼             ▼        │
│     S3/          Celery         OpenAI API     Qdrant      │
│   Storage        Worker                                    │
│                                                             │
│                   ┌──────────┐                             │
│                   │  Search  │  ← API Endpoint             │
│                   └────┬─────┘                             │
│                        │                                   │
│                        ▼                                   │
│                  Top-K Chunks                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 1.2 API Specifications

#### POST /api/v1/documents/upload

**Purpose**: Upload de manual técnico (PDF)

**Request**:
```http
POST /api/v1/documents/upload
Content-Type: multipart/form-data
Authorization: Bearer <jwt_token>

{
  "file": <binary_pdf>,
  "metadata": {
    "document_type": "manual_tecnico",
    "vehicle_model": "XYZ-2023",
    "tags": ["freios", "motor", "eletrica"]
  }
}
```

**Response** (202 Accepted):
```json
{
  "document_id": "uuid",
  "name": "Manual_Tecnico_XYZ_2023.pdf",
  "size_bytes": 52428800,
  "status": "pending",
  "uploaded_at": "2025-10-10T14:30:00Z",
  "processing_eta_seconds": 180
}
```

**Implementation Notes**:
```python
# backend/rag/routes.py
from fastapi import APIRouter, UploadFile, File, Depends
from app.rag.services import DocumentService
from app.auth.dependencies import get_current_admin

router = APIRouter(prefix="/api/v1/documents", tags=["RAG"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    metadata: dict = {},
    service: DocumentService = Depends(),
    user = Depends(get_current_admin)  # Only admins can upload
):
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # Validate file size (max 50MB)
    file_size = await file.read()
    if len(file_size) > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large (max 50MB)")

    # Upload to S3
    s3_key = await service.upload_to_s3(file, file_size)

    # Create document record
    document = await service.create_document(
        name=file.filename,
        s3_key=s3_key,
        size_bytes=len(file_size),
        uploaded_by=user.id,
        metadata=metadata
    )

    # Trigger async processing
    from app.rag.tasks import process_document_task
    process_document_task.delay(document.id)

    return {
        "document_id": document.id,
        "name": document.name,
        "size_bytes": document.file_size_bytes,
        "status": document.status,
        "uploaded_at": document.uploaded_at,
        "processing_eta_seconds": estimate_processing_time(document.file_size_bytes)
    }
```

---

#### GET /api/v1/search

**Purpose**: Busca semântica na base de conhecimento

**Request**:
```http
GET /api/v1/search?q=como+trocar+pastilha+de+freio&top_k=5&threshold=0.6
Authorization: Bearer <jwt_token>
```

**Query Parameters**:
- `q` (required): Query em linguagem natural
- `top_k` (optional, default=5): Número de chunks a retornar
- `threshold` (optional, default=0.6): Similarity score mínimo
- `document_filter` (optional): Filtrar por documento específico

**Response** (200 OK):
```json
{
  "query": "como trocar pastilha de freio",
  "results": [
    {
      "chunk_id": "uuid",
      "score": 0.87,
      "chunk_text": "Para trocar a pastilha de freio dianteira: 1. Remova a roda...",
      "document_name": "Manual_Tecnico_XYZ_2023.pdf",
      "page_number": 142,
      "section_title": "Procedimento de Troca - Freios Dianteiros",
      "metadata": {
        "vehicle_model": "XYZ-2023",
        "tags": ["freios"]
      }
    },
    {
      "chunk_id": "uuid",
      "score": 0.82,
      "chunk_text": "Especificações técnicas da pastilha: espessura mínima 3mm...",
      "document_name": "Manual_Tecnico_XYZ_2023.pdf",
      "page_number": 145,
      "section_title": "Especificações Técnicas",
      "metadata": {}
    }
  ],
  "total_results": 2,
  "latency_ms": 234
}
```

**Implementation**:
```python
# backend/rag/routes.py
@router.get("/search")
async def semantic_search(
    q: str,
    top_k: int = 5,
    threshold: float = 0.6,
    document_filter: str = None,
    service: RAGService = Depends(),
    user = Depends(get_current_user)
):
    start_time = time.time()

    # Check cache first
    cache_key = f"search:{hash(q)}:{top_k}:{threshold}"
    cached_result = await redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    # Generate embedding for query
    query_embedding = await service.generate_embedding(q)

    # Search in Qdrant
    search_results = await service.vector_search(
        query_embedding=query_embedding,
        top_k=top_k,
        score_threshold=threshold,
        document_filter=document_filter
    )

    # Format response
    response = {
        "query": q,
        "results": [
            {
                "chunk_id": r.id,
                "score": r.score,
                "chunk_text": r.payload["chunk_text"],
                "document_name": r.payload["document_name"],
                "page_number": r.payload.get("page_number"),
                "section_title": r.payload.get("section_title"),
                "metadata": r.payload.get("metadata", {})
            }
            for r in search_results
        ],
        "total_results": len(search_results),
        "latency_ms": int((time.time() - start_time) * 1000)
    }

    # Cache result (TTL 1 hour)
    await redis_client.setex(cache_key, 3600, json.dumps(response))

    return response
```

---

### 1.3 Celery Background Task: Document Processing

**Task Flow**:
```
Upload → S3 → Trigger Task → [Extract PDF Text] → [Chunk Text] →
[Generate Embeddings] → [Index in Qdrant] → Update Status
```

**Implementation**:
```python
# backend/rag/tasks.py
from celery import shared_task
from app.rag.services import ProcessingService
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_document_task(self, document_id: str):
    """
    Background task to process PDF document:
    1. Extract text (with OCR if needed)
    2. Chunk text
    3. Generate embeddings
    4. Index in Qdrant
    """
    try:
        service = ProcessingService()

        # Update status to processing
        await service.update_document_status(document_id, "processing")

        # Step 1: Extract text from PDF
        logger.info(f"[{document_id}] Starting text extraction")
        text_pages = await service.extract_text_from_pdf(document_id)
        logger.info(f"[{document_id}] Extracted {len(text_pages)} pages")

        # Step 2: Chunk text
        logger.info(f"[{document_id}] Starting chunking")
        chunks = await service.chunk_document(text_pages, document_id)
        logger.info(f"[{document_id}] Created {len(chunks)} chunks")

        # Step 3: Generate embeddings (batch)
        logger.info(f"[{document_id}] Generating embeddings")
        embeddings = await service.generate_embeddings_batch(
            chunks,
            batch_size=100
        )
        logger.info(f"[{document_id}] Generated {len(embeddings)} embeddings")

        # Step 4: Index in Qdrant
        logger.info(f"[{document_id}] Indexing in Qdrant")
        await service.index_chunks_in_qdrant(chunks, embeddings, document_id)

        # Update status to completed
        await service.update_document_status(
            document_id,
            "completed",
            total_chunks=len(chunks)
        )

        logger.info(f"[{document_id}] Processing completed successfully")

    except Exception as e:
        logger.error(f"[{document_id}] Processing failed: {str(e)}")

        # Update status to error
        await service.update_document_status(
            document_id,
            "error",
            error_message=str(e)
        )

        # Retry if transient error
        if "rate limit" in str(e).lower() or "timeout" in str(e).lower():
            raise self.retry(exc=e, countdown=60)  # Retry after 1 min

        raise e
```

---

### 1.4 Chunking Strategy (Hybrid)

**Implementation**:
```python
# backend/rag/chunking.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

class HybridChunker:
    """
    Chunking strategy:
    1. Try to chunk by section (detect headers)
    2. If section > 1000 tokens, split further with overlap
    """

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=[
                "\n## ",    # H2 headers
                "\n### ",   # H3 headers
                "\n\n",     # Paragraphs
                "\n",       # Lines
                " ",        # Words
            ],
            length_function=self._count_tokens
        )

    def _count_tokens(self, text: str) -> int:
        """Estimate tokens (rough approximation)"""
        return len(text) // 4  # ~4 chars per token

    def chunk_document(
        self,
        text_pages: list[dict],  # [{page_num, text, headers}]
        document_id: str
    ) -> list[dict]:
        """
        Returns list of chunks with metadata
        """
        chunks = []
        chunk_index = 0

        for page in text_pages:
            page_num = page["page_num"]
            page_text = page["text"]

            # Attempt to detect sections
            sections = self._detect_sections(page_text)

            if sections:
                # Chunk by section
                for section in sections:
                    section_chunks = self._chunk_section(
                        section["text"],
                        max_tokens=1000
                    )

                    for chunk_text in section_chunks:
                        chunks.append({
                            "chunk_id": f"{document_id}_{chunk_index}",
                            "chunk_index": chunk_index,
                            "chunk_text": chunk_text,
                            "page_number": page_num,
                            "section_title": section.get("title"),
                            "document_id": document_id
                        })
                        chunk_index += 1
            else:
                # No sections detected, use fixed-size chunking
                page_chunks = self.splitter.split_text(page_text)

                for chunk_text in page_chunks:
                    chunks.append({
                        "chunk_id": f"{document_id}_{chunk_index}",
                        "chunk_index": chunk_index,
                        "chunk_text": chunk_text,
                        "page_number": page_num,
                        "section_title": None,
                        "document_id": document_id
                    })
                    chunk_index += 1

        return chunks

    def _detect_sections(self, text: str) -> list[dict]:
        """Detect sections via header patterns"""
        # Regex for common technical manual headers
        header_pattern = r'^(##?\s+[\d\.]+\s+[A-Z][^\n]+)$'
        matches = re.finditer(header_pattern, text, re.MULTILINE)

        sections = []
        positions = [(m.start(), m.end(), m.group(1)) for m in matches]

        for i, (start, end, title) in enumerate(positions):
            section_start = end
            section_end = positions[i + 1][0] if i + 1 < len(positions) else len(text)

            section_text = text[section_start:section_end].strip()

            if section_text:  # Ignore empty sections
                sections.append({
                    "title": title.strip(),
                    "text": section_text
                })

        return sections if sections else None

    def _chunk_section(self, section_text: str, max_tokens: int) -> list[str]:
        """Chunk a section if it exceeds max_tokens"""
        if self._count_tokens(section_text) <= max_tokens:
            return [section_text]

        # Section too large, split it
        return self.splitter.split_text(section_text)
```

---

### 1.5 Embedding Generation (Batch)

**Implementation**:
```python
# backend/rag/embedding.py
import openai
from typing import List
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class EmbeddingService:
    def __init__(self):
        self.model = "text-embedding-ada-002"
        self.max_batch_size = 100  # OpenAI allows up to 2048, but 100 is safer
        openai.api_key = settings.OPENAI_API_KEY

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_embedding(self, text: str) -> list[float]:
        """Generate single embedding"""
        response = await openai.Embedding.acreate(
            model=self.model,
            input=text
        )
        return response['data'][0]['embedding']

    async def generate_embeddings_batch(
        self,
        chunks: list[dict],
        batch_size: int = 100
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple chunks (batched)
        Returns list of embeddings in same order as chunks
        """
        embeddings = []

        # Process in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_texts = [chunk["chunk_text"] for chunk in batch]

            # Check cache first
            cached_embeddings = await self._check_cache(batch_texts)

            # Generate only for non-cached
            texts_to_embed = [
                text for text, cached in zip(batch_texts, cached_embeddings)
                if cached is None
            ]

            if texts_to_embed:
                response = await openai.Embedding.acreate(
                    model=self.model,
                    input=texts_to_embed
                )

                new_embeddings = [item['embedding'] for item in response['data']]

                # Cache new embeddings
                await self._cache_embeddings(texts_to_embed, new_embeddings)
            else:
                new_embeddings = []

            # Merge cached and new
            batch_embeddings = []
            new_idx = 0
            for cached in cached_embeddings:
                if cached is not None:
                    batch_embeddings.append(cached)
                else:
                    batch_embeddings.append(new_embeddings[new_idx])
                    new_idx += 1

            embeddings.extend(batch_embeddings)

            # Rate limiting: wait 1s between batches
            if i + batch_size < len(chunks):
                await asyncio.sleep(1)

        return embeddings

    async def _check_cache(self, texts: list[str]) -> list[list[float] | None]:
        """Check Redis cache for existing embeddings"""
        cache_keys = [f"emb:{hash(text)}" for text in texts]
        cached = await redis_client.mget(cache_keys)
        return [json.loads(emb) if emb else None for emb in cached]

    async def _cache_embeddings(self, texts: list[str], embeddings: list[list[float]]):
        """Cache embeddings in Redis (TTL 30 days)"""
        pipeline = redis_client.pipeline()
        for text, embedding in zip(texts, embeddings):
            cache_key = f"emb:{hash(text)}"
            pipeline.setex(cache_key, 30 * 24 * 3600, json.dumps(embedding))
        await pipeline.execute()
```

---

### 1.6 Qdrant Integration

**Implementation**:
```python
# backend/rag/vector_db.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List
import uuid

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            timeout=30
        )
        self.collection_name = "knowledge_base"
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        collections = self.client.get_collections().collections

        if self.collection_name not in [c.name for c in collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # OpenAI embedding dimension
                    distance=Distance.COSINE
                ),
                hnsw_config={
                    "m": 16,
                    "ef_construct": 100
                }
            )

    async def index_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        document_id: str
    ):
        """
        Index chunks in Qdrant
        chunks: list of {chunk_id, chunk_text, page_number, section_title, ...}
        embeddings: list of vectors (same order as chunks)
        """
        points = []

        for chunk, embedding in zip(chunks, embeddings):
            point = PointStruct(
                id=str(uuid.uuid4()),  # Qdrant point ID
                vector=embedding,
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "document_id": document_id,
                    "chunk_text": chunk["chunk_text"],
                    "page_number": chunk.get("page_number"),
                    "section_title": chunk.get("section_title"),
                    "chunk_index": chunk["chunk_index"]
                }
            )
            points.append(point)

        # Upsert in batches of 1000
        batch_size = 1000
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )

    async def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        score_threshold: float = 0.6,
        document_filter: str = None
    ):
        """Vector similarity search"""
        search_params = {
            "collection_name": self.collection_name,
            "query_vector": query_vector,
            "limit": top_k,
            "score_threshold": score_threshold,
            "with_payload": True
        }

        # Optional document filter
        if document_filter:
            search_params["query_filter"] = {
                "must": [
                    {
                        "key": "document_id",
                        "match": {"value": document_filter}
                    }
                ]
            }

        results = self.client.search(**search_params)
        return results

    async def delete_by_document(self, document_id: str):
        """Delete all chunks of a document"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector={
                "filter": {
                    "must": [
                        {
                            "key": "document_id",
                            "match": {"value": document_id}
                        }
                    ]
                }
            }
        )
```

---

### 1.7 Testing Strategy for Epic 1

**Unit Tests**:
```python
# tests/unit/test_chunking.py
import pytest
from app.rag.chunking import HybridChunker

def test_chunk_simple_text():
    chunker = HybridChunker()

    text_pages = [{
        "page_num": 1,
        "text": "Simple text that fits in one chunk."
    }]

    chunks = chunker.chunk_document(text_pages, "doc_123")

    assert len(chunks) == 1
    assert chunks[0]["page_number"] == 1
    assert "Simple text" in chunks[0]["chunk_text"]

def test_chunk_with_sections():
    chunker = HybridChunker()

    text = """
    ## 1.1 Introduction
    This is the introduction section.

    ## 1.2 Procedure
    This is the procedure section with steps.
    """

    text_pages = [{"page_num": 1, "text": text}]
    chunks = chunker.chunk_document(text_pages, "doc_123")

    # Should detect 2 sections
    assert len(chunks) >= 2
    assert any("Introduction" in c.get("section_title", "") for c in chunks)
```

**Integration Tests**:
```python
# tests/integration/test_rag_pipeline.py
import pytest
from app.rag.services import ProcessingService

@pytest.mark.asyncio
async def test_full_rag_pipeline(test_pdf_path):
    """Test full pipeline: PDF → chunks → embeddings → Qdrant"""
    service = ProcessingService()

    # Upload test PDF
    document_id = await service.create_document_from_file(test_pdf_path)

    # Process
    await service.process_document(document_id)

    # Verify chunks created
    chunks = await service.get_chunks(document_id)
    assert len(chunks) > 0

    # Verify indexed in Qdrant
    qdrant = QdrantService()
    results = await qdrant.search(
        query_vector=await service.generate_embedding("test query"),
        top_k=5
    )

    assert len(results) > 0
```

**Acceptance Criteria Validation** (US-RAG-09):
```python
# tests/acceptance/test_rag_accuracy.py
import pytest

GOLD_STANDARD_QUERIES = [
    {
        "query": "como trocar pastilha de freio dianteira",
        "expected_doc": "Manual_Tecnico_XYZ_2023.pdf",
        "expected_page_range": (140, 150)
    },
    # ... 19 more queries
]

@pytest.mark.asyncio
async def test_search_accuracy():
    """Validate search accuracy >80% (NFR-04)"""
    service = RAGService()

    correct_results = 0
    total_queries = len(GOLD_STANDARD_QUERIES)

    for item in GOLD_STANDARD_QUERIES:
        results = await service.search(item["query"], top_k=5)

        # Check if expected document is in top-5
        top_5_docs = [r["document_name"] for r in results]

        if item["expected_doc"] in top_5_docs:
            # Check page range
            matching_results = [
                r for r in results
                if r["document_name"] == item["expected_doc"]
                and item["expected_page_range"][0] <= r["page_number"] <= item["expected_page_range"][1]
            ]

            if matching_results:
                correct_results += 1

    accuracy = correct_results / total_queries

    assert accuracy >= 0.80, f"Search accuracy {accuracy:.2%} < 80%"
```

---

## Epic 2: Copiloto MVP

**Goal**: Interface conversacional para diagnóstico assistido

**Stories**: US-COP-01 a US-COP-11 (11 stories)

**Priority**: CRÍTICA

---

### 2.1 Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Copiloto Module                             │
│                                                             │
│  WhatsApp      Chat          LLM           Voice            │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐        │
│  │Webhook │→  │Session │→  │Prompt  │→  │STT API │        │
│  │Handler │   │Manager │   │LLM Call│   │        │        │
│  └────┬───┘   └───┬────┘   └───┬────┘   └────────┘        │
│       │           │            │                            │
│       └───────────┴────────────┘                            │
│                   │                                         │
│                   ▼                                         │
│         ┌──────────────────┐                                │
│         │  RAG Module      │                                │
│         │  (Search API)    │                                │
│         └──────────────────┘                                │
│                                                             │
│         ┌──────────────────┐                                │
│         │  PostgreSQL      │                                │
│         │  (Conversations, │                                │
│         │   Messages)      │                                │
│         └──────────────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

---

### 2.2 WhatsApp Webhook Integration

**Webhook Endpoint**: `POST /api/v1/whatsapp/webhook`

**Meta Webhook Verification**:
```python
# backend/copiloto/whatsapp/routes.py
from fastapi import APIRouter, Request, Query
from app.copiloto.services import WhatsAppService

router = APIRouter(prefix="/api/v1/whatsapp", tags=["WhatsApp"])

@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    """
    Meta webhook verification
    https://developers.facebook.com/docs/graph-api/webhooks/getting-started
    """
    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(challenge)
    else:
        return {"error": "Invalid verification token"}, 403

@router.post("/webhook")
async def handle_webhook(request: Request, service: WhatsAppService = Depends()):
    """
    Receive messages from WhatsApp
    """
    body = await request.json()

    # Extract message data
    entry = body.get("entry", [])[0]
    changes = entry.get("changes", [])[0]
    value = changes.get("value", {})
    messages = value.get("messages", [])

    if not messages:
        return {"status": "ok"}  # No messages, just status update

    message = messages[0]

    # Extract relevant fields
    from_number = message["from"]
    message_id = message["id"]
    timestamp = message["timestamp"]

    # Handle different message types
    if message["type"] == "text":
        text = message["text"]["body"]
        await service.handle_text_message(from_number, text, message_id)

    elif message["type"] == "audio":
        audio_id = message["audio"]["id"]
        await service.handle_audio_message(from_number, audio_id, message_id)

    return {"status": "ok"}
```

**Send Message to WhatsApp**:
```python
# backend/copiloto/whatsapp/client.py
import httpx
from typing import Optional

class WhatsAppClient:
    def __init__(self):
        self.api_url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        self.token = settings.WHATSAPP_ACCESS_TOKEN

    async def send_text_message(self, to: str, text: str) -> dict:
        """
        Send text message to WhatsApp user
        to: recipient phone number (E.164 format, e.g., +5511999999999)
        text: message text (max 4096 chars)
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text}
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    async def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "pt_BR",
        parameters: list = None
    ) -> dict:
        """
        Send template message (for notifications)
        Templates must be pre-approved by Meta
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": [
                    {
                        "type": "body",
                        "parameters": parameters or []
                    }
                ]
            }
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
```

---

### 2.3 Conversation Management

**Session Flow**:
```
User sends WhatsApp message → Webhook → Authenticate (CPF) →
Create/Resume Conversation → Process Message → Generate Response →
Send via WhatsApp → Store Message
```

**Implementation**:
```python
# backend/copiloto/services.py
from app.copiloto.whatsapp.client import WhatsAppClient
from app.rag.services import RAGService
from app.copiloto.llm import LLMService
import redis

class ConversationService:
    def __init__(self):
        self.whatsapp = WhatsAppClient()
        self.rag = RAGService()
        self.llm = LLMService()
        self.redis = redis.from_url(settings.REDIS_URL)

    async def handle_text_message(
        self,
        from_number: str,
        text: str,
        message_id: str
    ):
        """Main message handler"""

        # Check for duplicate message (WhatsApp sometimes sends duplicates)
        if await self._is_duplicate(message_id):
            return

        # Get or create session
        session = await self._get_session(from_number)

        if not session.get("authenticated"):
            # User not authenticated yet
            await self._handle_authentication(from_number, text)
            return

        user_id = session["user_id"]

        # Check for special commands
        if text.lower() in ["sair", "quit", "exit"]:
            await self._end_conversation(session["conversation_id"])
            await self.whatsapp.send_text_message(
                from_number,
                "Conversa encerrada. Até logo! 👋"
            )
            return

        # Check for OS association
        os_match = self._extract_os_number(text)
        if os_match:
            await self._associate_os(session["conversation_id"], os_match)
            await self.whatsapp.send_text_message(
                from_number,
                f"OK! Vou registrar essa conversa na OS #{os_match}."
            )
            # Continue processing the rest of the message if there's more
            text = text.replace(os_match, "").strip()
            if not text:
                return

        # Store user message
        await self._store_message(
            conversation_id=session["conversation_id"],
            sender="mechanic",
            text=text
        )

        # Generate response
        await self.whatsapp.send_text_message(from_number, "💬 Digitando...")

        response_text = await self._generate_response(
            user_id=user_id,
            conversation_id=session["conversation_id"],
            query=text
        )

        # Send response
        await self.whatsapp.send_text_message(from_number, response_text)

        # Store assistant message
        await self._store_message(
            conversation_id=session["conversation_id"],
            sender="copiloto",
            text=response_text
        )

        # Ask for feedback
        await asyncio.sleep(2)  # Small delay
        await self.whatsapp.send_text_message(
            from_number,
            "Esta resposta foi útil? 👍 👎"
        )

    async def _get_session(self, phone_number: str) -> dict:
        """Get or create session from Redis"""
        session_key = f"whatsapp_session:{phone_number}"
        session_data = await self.redis.get(session_key)

        if session_data:
            return json.loads(session_data)
        else:
            # New session
            session = {
                "phone_number": phone_number,
                "authenticated": False,
                "created_at": datetime.utcnow().isoformat()
            }
            await self.redis.setex(
                session_key,
                24 * 3600,  # TTL 24 hours
                json.dumps(session)
            )
            return session

    async def _handle_authentication(self, phone_number: str, text: str):
        """Authenticate user via CPF"""
        # Extract CPF from message
        cpf = self._extract_cpf(text)

        if not cpf:
            await self.whatsapp.send_text_message(
                phone_number,
                "Olá! Para começar, por favor envie seu CPF (apenas números)."
            )
            return

        # Validate CPF and lookup user
        user = await self._get_user_by_cpf(cpf)

        if not user:
            await self.whatsapp.send_text_message(
                phone_number,
                "CPF não encontrado. Por favor, contate seu gestor."
            )
            return

        # Create conversation
        conversation_id = await self._create_conversation(
            user_id=user.id,
            phone_number=phone_number
        )

        # Update session
        session = {
            "phone_number": phone_number,
            "authenticated": True,
            "user_id": user.id,
            "user_name": user.name,
            "conversation_id": conversation_id,
            "authenticated_at": datetime.utcnow().isoformat()
        }

        session_key = f"whatsapp_session:{phone_number}"
        await self.redis.setex(
            session_key,
            24 * 3600,
            json.dumps(session)
        )

        # Send welcome message
        await self.whatsapp.send_text_message(
            phone_number,
            f"Bem-vindo, {user.name}! 👋\n\n"
            "Eu sou o Copiloto do Mecânico. Como posso te ajudar hoje?"
        )

    async def _generate_response(
        self,
        user_id: str,
        conversation_id: str,
        query: str
    ) -> str:
        """
        Generate response using RAG + LLM
        """
        # Step 1: Semantic search
        search_results = await self.rag.search(query, top_k=5, threshold=0.6)

        if not search_results["results"]:
            # No relevant chunks found
            return (
                "Desculpe, não encontrei informações específicas sobre isso. "
                "Pode reformular a pergunta ou tentar descrever o problema com mais detalhes?"
            )

        # Step 2: Build context from chunks
        context_chunks = [
            f"[Fonte: {r['document_name']}, pág. {r['page_number']}]\n{r['chunk_text']}"
            for r in search_results["results"]
        ]
        context = "\n\n---\n\n".join(context_chunks)

        # Step 3: Generate response with LLM
        response = await self.llm.generate_response(
            query=query,
            context=context,
            conversation_history=await self._get_recent_messages(conversation_id, limit=5)
        )

        # Step 4: Add source citations
        sources = [
            f"📘 {r['document_name']}, pág. {r['page_number']}"
            for r in search_results["results"][:3]  # Top 3 sources
        ]

        response_with_sources = f"{response}\n\n**Fontes:**\n" + "\n".join(sources)

        return response_with_sources
```

---

### 2.4 LLM Service (Prompt Engineering)

**Implementation**:
```python
# backend/copiloto/llm.py
import openai
from typing import List, Optional

class LLMService:
    def __init__(self):
        self.model = "gpt-4"
        openai.api_key = settings.OPENAI_API_KEY

    async def generate_response(
        self,
        query: str,
        context: str,
        conversation_history: List[dict] = None
    ) -> str:
        """
        Generate response using GPT-4 with RAG context
        """
        # Build system prompt
        system_prompt = """
Você é um assistente técnico especializado em manutenção automotiva.
Sua função é ajudar mecânicos durante a execução de serviços, fornecendo:
- Diagnósticos precisos
- Procedimentos passo a passo
- Especificações técnicas
- Próximos passos sugeridos

REGRAS IMPORTANTES:
1. Seja conciso e direto (mecânico está trabalhando)
2. Use linguagem simples e clara
3. Cite sempre as fontes (manual técnico, página)
4. Se não souber, admita e sugira alternativas
5. Para diagnósticos, faça perguntas para refinar
6. Formate respostas em tópicos quando apropriado

FORMATO DE RESPOSTA:
- Para consultas simples: resposta direta + fonte
- Para diagnósticos: perguntas de refinamento OU diagnóstico + probabilidade + próximos passos
"""

        # Build user prompt
        user_prompt = f"""
**Contexto (Manuais Técnicos):**
{context}

**Pergunta do Mecânico:**
{query}

Por favor, responda baseado no contexto fornecido. Se o contexto não tiver informação suficiente, admita.
"""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history (for context)
        if conversation_history:
            for msg in conversation_history[-3:]:  # Last 3 messages
                role = "user" if msg["sender"] == "mechanic" else "assistant"
                messages.append({"role": role, "content": msg["text"]})

        # Add current query
        messages.append({"role": "user", "content": user_prompt})

        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            temperature=0.3,  # Lower temp for factual responses
            max_tokens=500,   # Limit response length
            top_p=0.9
        )

        return response.choices[0].message.content.strip()
```

---

### 2.5 Speech-to-Text (Audio Handling)

**Implementation**:
```python
# backend/copiloto/voice.py
import openai
import httpx

class SpeechToTextService:
    async def transcribe_whatsapp_audio(self, audio_id: str) -> str:
        """
        Download audio from WhatsApp and transcribe
        """
        # Step 1: Get audio URL from WhatsApp
        audio_url = await self._get_audio_url(audio_id)

        # Step 2: Download audio file
        audio_bytes = await self._download_audio(audio_url)

        # Step 3: Transcribe with Whisper
        transcription = await self._transcribe(audio_bytes)

        return transcription

    async def _get_audio_url(self, audio_id: str) -> str:
        """Get download URL for audio from WhatsApp API"""
        url = f"https://graph.facebook.com/v18.0/{audio_id}"
        headers = {"Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["url"]

    async def _download_audio(self, audio_url: str) -> bytes:
        """Download audio file"""
        headers = {"Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(audio_url, headers=headers)
            response.raise_for_status()
            return response.content

    async def _transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio using OpenAI Whisper"""
        # Whisper expects file-like object
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.ogg"  # WhatsApp uses OGG format

        response = await openai.Audio.atranscribe(
            model="whisper-1",
            file=audio_file,
            language="pt"  # Portuguese
        )

        return response["text"]
```

---

### 2.6 Rate Limiting (US-COP-09)

**Implementation**:
```python
# backend/copiloto/middleware.py
from fastapi import Request, HTTPException
from app.auth.dependencies import get_current_user

class RateLimitMiddleware:
    """
    Rate limit: 50 queries/day per mechanic
    """

    async def __call__(self, request: Request, call_next):
        # Skip rate limiting for non-Copiloto endpoints
        if not request.url.path.startswith("/api/v1/copiloto"):
            return await call_next(request)

        # Get user from session
        user = await get_current_user(request)

        if user.role == "admin":
            # Admins bypass rate limit
            return await call_next(request)

        # Check rate limit
        today = datetime.utcnow().date().isoformat()
        rate_key = f"rate_limit:copiloto:{user.id}:{today}"

        current_count = await redis_client.get(rate_key)

        if current_count and int(current_count) >= 50:
            raise HTTPException(
                status_code=429,
                detail="Você atingiu o limite diário de consultas (50/dia). Tente novamente amanhã."
            )

        # Increment counter
        pipe = redis_client.pipeline()
        pipe.incr(rate_key)
        pipe.expire(rate_key, 24 * 3600)  # TTL 24 hours
        await pipe.execute()

        # Continue
        response = await call_next(request)
        return response
```

---

### 2.7 Testing for Epic 2

**Integration Test - Full Conversation Flow**:
```python
# tests/integration/test_copiloto_flow.py
import pytest
from app.copiloto.services import ConversationService

@pytest.mark.asyncio
async def test_full_conversation_flow():
    """Test complete conversation flow"""
    service = ConversationService()
    phone = "+5511999999999"

    # Step 1: Authentication
    await service.handle_text_message(phone, "12345678900", "msg_001")

    # Verify session created
    session = await service._get_session(phone)
    assert session["authenticated"] == True

    # Step 2: Send query
    await service.handle_text_message(
        phone,
        "Como trocar pastilha de freio?",
        "msg_002"
    )

    # Verify response sent (mock WhatsApp client)
    # Check that RAG was called
    # Check that LLM was called
    # Check that message was stored

    messages = await service._get_recent_messages(session["conversation_id"], 10)
    assert len(messages) >= 2
    assert any("pastilha" in m["text"].lower() for m in messages)
```

---

## Epic 3: Sistema de Avaliação

**Goal**: Criação, execução e correção automatizada de avaliações

**Stories**: US-AVA-01 a US-AVA-09 (9 stories)

**Priority**: ALTA

---

### 3.1 API: Criar Ciclo de Avaliação

**POST /api/v1/assessments/cycles**

**Request**:
```json
{
  "name": "Avaliação Q2-2025",
  "phase": "phase_2",
  "start_date": "2025-10-15",
  "end_date": "2025-10-30",
  "target_audience": {
    "type": "all_mechanics",  // ou "specific_mechanics" ou "dealerships"
    "dealership_ids": ["uuid1", "uuid2"],  // optional
    "mechanic_ids": []  // optional
  },
  "competency_areas": ["diagnostico_geral", "freios", "eletrica"]
}
```

**Response**:
```json
{
  "cycle_id": "uuid",
  "name": "Avaliação Q2-2025",
  "status": "draft",
  "created_at": "2025-10-10T14:00:00Z",
  "total_target_mechanics": 450
}
```

---

### 3.2 API: Gerar Questões via IA

**POST /api/v1/assessments/cycles/{cycle_id}/generate-questions**

**Request**:
```json
{
  "num_questions": 30,
  "difficulty_distribution": {
    "easy": 10,
    "medium": 15,
    "hard": 5
  }
}
```

**Implementation**:
```python
# backend/avaliacao/question_generation.py
from app.rag.services import RAGService
from app.copiloto.llm import LLMService

class QuestionGenerationService:
    def __init__(self):
        self.rag = RAGService()
        self.llm = LLMService()

    async def generate_questions(
        self,
        cycle_id: str,
        competency_areas: list[str],
        num_questions: int,
        target_level: str  # iniciante, adequado, experiente
    ) -> list[dict]:
        """
        Generate contextual situational questions using LLM + RAG
        """
        questions = []

        questions_per_area = num_questions // len(competency_areas)

        for area in competency_areas:
            # Get relevant technical content from RAG
            search_results = await self.rag.search(
                query=f"procedimentos e diagnósticos em {area}",
                top_k=10
            )

            context = "\n\n".join([
                r["chunk_text"] for r in search_results["results"]
            ])

            # Generate questions for this area
            area_questions = await self._generate_questions_for_area(
                area=area,
                context=context,
                num_questions=questions_per_area,
                target_level=target_level
            )

            questions.extend(area_questions)

        # Store questions in database
        await self._store_questions(cycle_id, questions)

        return questions

    async def _generate_questions_for_area(
        self,
        area: str,
        context: str,
        num_questions: int,
        target_level: str
    ) -> list[dict]:
        """Use LLM to generate situational questions"""

        prompt = f"""
Você é um especialista em avaliação de competências para mecânicos automotivos.

**Área Técnica:** {area}
**Nível Alvo:** {target_level}
**Número de Questões:** {num_questions}

**Contexto Técnico (Manuais):**
{context}

Por favor, gere {num_questions} questões situacionais contextualizadas para avaliar mecânicos.

**Formato de Cada Questão:**
1. Enunciado: Descreva uma situação realista (cliente chega com problema X, mecânico observa sintoma Y)
2. Pergunta: O que o mecânico deve fazer? Como diagnosticar? Como resolver?
3. Rubrica de 4 Níveis:
   - Nível 1 (Inadequado): Resposta incorreta ou superficial
   - Nível 2 (Parcial): Identifica parte do problema mas falta profundidade
   - Nível 3 (Adequado): Diagnóstico correto e solução apropriada
   - Nível 4 (Excelente): Solução completa + considerações adicionais (segurança, prevenção)

Retorne em formato JSON:
```json
[
  {
    "question_text": "Um cliente chega relatando...",
    "rubric": {
      "level_1": "Descrição...",
      "level_2": "Descrição...",
      "level_3": "Descrição...",
      "level_4": "Descrição..."
    },
    "metadata": {
      "bloom_level": "aplicar",
      "estimated_difficulty": "medium"
    }
  }
]
```
"""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em avaliação de competências."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Higher temp for creativity
            max_tokens=3000
        )

        # Parse JSON response
        questions_json = json.loads(response.choices[0].message.content)

        return questions_json
```

---

### 3.3 Auto-Grading (US-AVA-07)

**Implementation**:
```python
# backend/avaliacao/grading.py
class AutoGradingService:
    async def grade_response(
        self,
        question: dict,  # {question_text, rubric}
        response_text: str
    ) -> dict:
        """
        Grade mechanic's response using LLM
        Returns: {score: 1-4, rationale: str, confidence: 0-1}
        """

        prompt = f"""
Você é um avaliador especializado em competências de mecânicos automotivos.

**Questão:**
{question["question_text"]}

**Rubrica de Avaliação:**
- Nível 1 (Inadequado): {question["rubric"]["level_1"]}
- Nível 2 (Parcial): {question["rubric"]["level_2"]}
- Nível 3 (Adequado): {question["rubric"]["level_3"]}
- Nível 4 (Excelente): {question["rubric"]["level_4"]}

**Resposta do Mecânico:**
{response_text}

Por favor, avalie a resposta segundo a rubrica e retorne em JSON:
```json
{
  "score": 1-4,
  "rationale": "Justificativa da nota...",
  "confidence": 0.0-1.0,
  "strengths": ["Ponto forte 1", ...],
  "improvements": ["Área para melhorar 1", ...]
}
```

**IMPORTANTE:**
- Seja justo e consistente
- Se a resposta está no limite entre dois níveis, indique confidence < 0.7
- Foque no conhecimento técnico demonstrado, não na gramática
"""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um avaliador imparcial e consistente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # Lower temp for consistency
            max_tokens=500
        )

        grading_result = json.loads(response.choices[0].message.content)

        return grading_result
```

---

### 3.4 Testing - Inter-Rater Reliability

**Validate Auto-Grading Accuracy**:
```python
# tests/acceptance/test_grading_reliability.py
import pytest
from app.avaliacao.grading import AutoGradingService

# Gold standard: 50 responses manually graded by 3 experts
GOLD_STANDARD = [
    {
        "question_id": "q1",
        "response_text": "Primeiro eu verificaria...",
        "expert_scores": [3, 3, 4],  # 3 experts gave these scores
        "consensus_score": 3
    },
    # ... 49 more
]

@pytest.mark.asyncio
async def test_inter_rater_reliability():
    """
    Validate AI grading has >80% agreement with human experts
    (NFR-04: Concordância inter-rater > 80%, Kappa > 0.75)
    """
    service = AutoGradingService()

    ai_scores = []
    human_scores = []

    for item in GOLD_STANDARD:
        question = await get_question(item["question_id"])

        result = await service.grade_response(
            question=question,
            response_text=item["response_text"]
        )

        ai_scores.append(result["score"])
        human_scores.append(item["consensus_score"])

    # Calculate agreement rate
    exact_matches = sum(ai == human for ai, human in zip(ai_scores, human_scores))
    agreement_rate = exact_matches / len(GOLD_STANDARD)

    # Calculate Cohen's Kappa
    kappa = calculate_cohens_kappa(ai_scores, human_scores)

    assert agreement_rate >= 0.80, f"Agreement rate {agreement_rate:.2%} < 80%"
    assert kappa >= 0.75, f"Cohen's Kappa {kappa:.2f} < 0.75"
```

---

## Epic 4: Dashboard

**Goal**: Analytics e visibilidade de competências

**Stories**: US-DASH-01 a US-DASH-07 (7 stories)

---

### 4.1 API: Dashboard Overview

**GET /api/v1/dashboard/overview**

**Query Params**:
- `dealership_id` (optional): Filter by dealership
- `period_start` (optional): Start date
- `period_end` (optional): End date

**Response**:
```json
{
  "total_mechanics": 450,
  "assessed_mechanics": 420,
  "distribution_by_level": {
    "iniciante": 85,
    "adequado": 250,
    "experiente": 85
  },
  "assessment_completion_rate": 0.93,
  "average_score": 76.5,
  "weekly_active_users_copiloto": 380,
  "top_competency_gaps": [
    {
      "area": "Sistemas Elétricos Modernos",
      "mechanics_below_adequate": 270,
      "percentage": 0.60
    }
  ],
  "trends": {
    "score_change_vs_last_cycle": +5.2,
    "classification_improvements": 45
  }
}
```

**Implementation** (Optimized with Materialized Views):
```python
# backend/dashboard/services.py
class DashboardService:
    async def get_overview(
        self,
        dealership_id: str = None,
        period_start: date = None,
        period_end: date = None
    ) -> dict:
        """
        Get dashboard overview with aggregated metrics
        Uses materialized views for performance
        """

        # Build query
        query = """
        SELECT
            COUNT(DISTINCT m.id) as total_mechanics,
            COUNT(DISTINCT ma.mechanic_id) as assessed_mechanics,
            AVG(ma.score_percentage) as average_score,
            COUNT(DISTINCT CASE WHEN ma.classification = 'iniciante' THEN ma.mechanic_id END) as iniciante_count,
            COUNT(DISTINCT CASE WHEN ma.classification = 'adequado' THEN ma.mechanic_id END) as adequado_count,
            COUNT(DISTINCT CASE WHEN ma.classification = 'experiente' THEN ma.mechanic_id END) as experiente_count
        FROM auth.users m
        LEFT JOIN avaliacao.mechanic_assessments ma ON m.id = ma.mechanic_id
        WHERE m.role = 'mecanico'
        """

        # Add filters
        if dealership_id:
            query += f" AND m.dealership_id = '{dealership_id}'"

        if period_start and period_end:
            query += f" AND ma.completed_at BETWEEN '{period_start}' AND '{period_end}'"

        # Execute
        result = await db.execute(query)
        row = result.fetchone()

        # Get gaps
        gaps = await self._get_competency_gaps(dealership_id)

        # Get trends
        trends = await self._get_trends(dealership_id)

        return {
            "total_mechanics": row.total_mechanics,
            "assessed_mechanics": row.assessed_mechanics,
            "distribution_by_level": {
                "iniciante": row.iniciante_count,
                "adequado": row.adequado_count,
                "experiente": row.experiente_count
            },
            "assessment_completion_rate": row.assessed_mechanics / row.total_mechanics if row.total_mechanics > 0 else 0,
            "average_score": round(row.average_score, 1),
            "top_competency_gaps": gaps[:5],  # Top 5
            "trends": trends
        }
```

---

### 4.2 Materialized Views for Performance

**Database Schema**:
```sql
-- Materialized view for dashboard aggregations (refreshed daily)
CREATE MATERIALIZED VIEW dashboard.mv_competency_summary AS
SELECT
    m.id as mechanic_id,
    m.name as mechanic_name,
    m.dealership_id,
    d.name as dealership_name,
    ma.classification,
    ma.score_percentage,
    ma.completed_at,
    -- Scores by competency area (from responses metadata)
    AVG(CASE WHEN q.metadata->>'area_tecnica' = 'diagnostico_geral' THEN r.ai_score END) as score_diagnostico,
    AVG(CASE WHEN q.metadata->>'area_tecnica' = 'freios' THEN r.ai_score END) as score_freios,
    AVG(CASE WHEN q.metadata->>'area_tecnica' = 'eletrica' THEN r.ai_score END) as score_eletrica
FROM auth.users m
LEFT JOIN auth.dealerships d ON m.dealership_id = d.id
LEFT JOIN avaliacao.mechanic_assessments ma ON m.id = ma.mechanic_id
LEFT JOIN avaliacao.responses r ON r.assessment_id = ma.id
LEFT JOIN avaliacao.questions q ON r.question_id = q.id
WHERE m.role = 'mecanico'
GROUP BY m.id, m.name, m.dealership_id, d.name, ma.classification, ma.score_percentage, ma.completed_at;

CREATE INDEX idx_mv_competency_dealership ON dashboard.mv_competency_summary(dealership_id);
CREATE INDEX idx_mv_competency_classification ON dashboard.mv_competency_summary(classification);

-- Refresh daily via cron job
CREATE OR REPLACE FUNCTION refresh_dashboard_views() RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard.mv_competency_summary;
END;
$$ LANGUAGE plpgsql;
```

---

## Epic 5: Auth & Observability

**Goal**: SSO, RBAC, logs, métricas, alertas

**Stories**: US-AUTH-01 a US-AUTH-08 (8 stories)

---

### 5.1 SAML SSO Integration

**Implementation**:
```python
# backend/auth/saml.py
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from fastapi import Request

class SAMLService:
    def __init__(self):
        self.settings = self._load_saml_settings()

    def _load_saml_settings(self) -> dict:
        """Load SAML configuration"""
        return {
            "sp": {  # Service Provider (CarGuroo)
                "entityId": "https://app.carguroo.com/saml/metadata",
                "assertionConsumerService": {
                    "url": "https://app.carguroo.com/api/v1/auth/saml/acs",
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                },
                "singleLogoutService": {
                    "url": "https://app.carguroo.com/api/v1/auth/saml/sls",
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                }
            },
            "idp": {  # Identity Provider (DMS da montadora)
                "entityId": settings.SAML_IDP_ENTITY_ID,
                "singleSignOnService": {
                    "url": settings.SAML_IDP_SSO_URL,
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                "x509cert": settings.SAML_IDP_X509_CERT
            },
            "security": {
                "nameIdEncrypted": False,
                "authnRequestsSigned": True,
                "wantAssertionsSigned": True,
                "wantNameIdEncrypted": False
            }
        }

    def prepare_request(self, request: Request) -> dict:
        """Prepare request data for python-saml"""
        return {
            "https": "on" if request.url.scheme == "https" else "off",
            "http_host": request.url.hostname,
            "server_port": request.url.port,
            "script_name": request.url.path,
            "get_data": dict(request.query_params),
            "post_data": {}  # Populated if POST
        }

    async def initiate_login(self, request: Request) -> str:
        """Redirect user to IdP for authentication"""
        req = self.prepare_request(request)
        auth = OneLogin_Saml2_Auth(req, self.settings)

        return auth.login()  # Returns redirect URL

    async def handle_assertion(self, request: Request) -> dict:
        """Process SAML assertion from IdP"""
        req = self.prepare_request(request)
        auth = OneLogin_Saml2_Auth(req, self.settings)

        auth.process_response()

        errors = auth.get_errors()
        if errors:
            raise HTTPException(status_code=401, detail=f"SAML error: {errors}")

        if not auth.is_authenticated():
            raise HTTPException(status_code=401, detail="SAML authentication failed")

        # Extract user attributes
        attributes = auth.get_attributes()

        user_data = {
            "cpf": attributes.get("cpf", [None])[0],
            "name": attributes.get("name", [None])[0],
            "email": attributes.get("email", [None])[0],
            "role": attributes.get("role", ["mecanico"])[0],
            "dealership_id": attributes.get("dealership_id", [None])[0]
        }

        return user_data
```

---

### 5.2 Structured Logging

**Implementation**:
```python
# backend/common/logging.py
import structlog
from uuid import uuid4
from contextvars import ContextVar

# Context variable for trace ID (propagated across async calls)
trace_id_var: ContextVar[str] = ContextVar("trace_id", default=None)

def setup_logging():
    """Configure structlog for JSON logging"""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # Merge trace_id
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Middleware to inject trace_id
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or extract trace ID
        trace_id = request.headers.get("X-Trace-ID", str(uuid4()))

        # Set in context var
        trace_id_var.set(trace_id)

        # Bind to structlog
        structlog.contextvars.bind_contextvars(trace_id=trace_id)

        # Add to response headers
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id

        return response

# Usage in application code
logger = structlog.get_logger()

logger.info(
    "Generated LLM response",
    user_id="uuid",
    query="como trocar pastilha",
    latency_ms=1234,
    tokens_used=1500
)

# Output (JSON):
# {
#   "timestamp": "2025-10-10T14:30:00.123Z",
#   "level": "info",
#   "trace_id": "a1b2c3d4-...",
#   "event": "Generated LLM response",
#   "user_id": "uuid",
#   "query": "como trocar pastilha",
#   "latency_ms": 1234,
#   "tokens_used": 1500
# }
```

---

### 5.3 Prometheus Metrics

**Implementation**:
```python
# backend/common/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import APIRouter

# Business Metrics
copiloto_queries_total = Counter(
    "carguroo_copiloto_queries_total",
    "Total number of Copiloto queries",
    ["user_id", "dealership_id"]
)

active_users_weekly = Gauge(
    "carguroo_active_users_weekly",
    "Number of weekly active users"
)

assessment_completion_rate = Gauge(
    "carguroo_assessment_completion_rate",
    "Assessment completion rate (0-1)"
)

# Technical Metrics
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint", "status_code"]
)

llm_api_calls_total = Counter(
    "carguroo_llm_api_calls_total",
    "Total LLM API calls",
    ["model", "operation"]
)

rag_search_latency_seconds = Histogram(
    "carguroo_rag_search_latency_seconds",
    "RAG search latency in seconds"
)

# Metrics endpoint
router = APIRouter()

@router.get("/metrics")
async def metrics():
    """Prometheus scrape endpoint"""
    return generate_latest()

# Usage in application
from time import time

start = time()
results = await rag_service.search(query)
rag_search_latency_seconds.observe(time() - start)

copiloto_queries_total.labels(
    user_id=user.id,
    dealership_id=user.dealership_id
).inc()
```

---

## Shared Components

### Database Connection Pool

```python
# backend/common/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Check connections before using
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency for FastAPI"""
    async with AsyncSessionLocal() as session:
        yield session
```

---

### Redis Client

```python
# backend/common/redis_client.py
import redis.asyncio as redis

redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
    max_connections=50
)

# Health check
async def ping_redis():
    try:
        await redis_client.ping()
        return True
    except:
        return False
```

---

## Testing Strategy

### Unit Tests

**Coverage Target**: >80%

**Tools**: pytest + pytest-asyncio + pytest-cov

**Run**:
```bash
cd backend
pytest --cov=app --cov-report=html --cov-report=term
```

**Key Areas**:
- RAG chunking logic
- LLM prompt engineering (mock OpenAI responses)
- Auto-grading logic
- RBAC permissions

---

### Integration Tests

**Tools**: pytest + docker-compose (test database)

**Setup**:
```bash
docker-compose -f docker-compose.test.yml up -d
pytest tests/integration/
```

**Key Areas**:
- Full RAG pipeline (PDF → Qdrant)
- Copiloto conversation flow
- Assessment creation → execution → grading
- Dashboard aggregations

---

### E2E Tests

**Tools**: Playwright (frontend) + API tests

**Run**:
```bash
cd frontend
npm run test:e2e
```

**Scenarios**:
- Gestor creates assessment cycle → Mecânico completes via WhatsApp simulator → Dashboard shows results
- Admin uploads PDF → Mecânico queries via Copiloto → Receives accurate response

---

### Load Testing

**Tool**: Locust

**Scenario**: Simulate 450 concurrent mechanics using Copiloto

**locustfile.py**:
```python
from locust import HttpUser, task, between

class CopiloUser(HttpUser):
    wait_time = between(5, 15)  # Mechanics query every 5-15 seconds

    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "cpf": "12345678900",
            "password": "test"
        })
        self.token = response.json()["access_token"]

    @task
    def query_copiloto(self):
        self.client.post(
            "/api/v1/copiloto/message",
            json={"text": "Como trocar pastilha de freio?"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
```

**Run**:
```bash
locust -f locustfile.py --host=https://staging.carguroo.com
```

**Target**: p95 latency <5s for 450 concurrent users

---

## Implementation Priority

### Phase 1 (Semana 1-4): Foundation

1. **Setup Infra**: PostgreSQL, Redis, Qdrant, S3
2. **Backend Skeleton**: FastAPI app, database models, migrations
3. **Epic 1**: RAG Infrastructure (US-RAG-01 to US-RAG-09)
4. **POC Técnico**: Validate RAG accuracy with 1 manual

### Phase 2 (Semana 5-8): Copiloto MVP

1. **Epic 2**: Copiloto (US-COP-01 to US-COP-11)
2. **WhatsApp Integration**: Full flow (webhook → LLM → response)
3. **Speech-to-Text**: Audio handling
4. **Testing**: Integration tests, pilot with 15 mecânicos

### Phase 3 (Semana 9-12): Avaliação + Dashboard

1. **Epic 3**: Avaliação (US-AVA-01 to US-AVA-09)
2. **Epic 4**: Dashboard (US-DASH-01 to US-DASH-07)
3. **Epic 5**: Auth SSO + Observability (US-AUTH-01 to US-AUTH-08)
4. **Refinements**: Based on pilot feedback
5. **Rollout Prep**: 450 mecânicos

---

## Success Criteria

- [x] All 41 user stories have technical specifications
- [ ] POC técnico de RAG executado (accuracy >80%)
- [ ] Copiloto MVP funcional end-to-end
- [ ] Avaliação auto-grading com inter-rater reliability >80%
- [ ] Dashboard mostrando métricas em tempo real
- [ ] All tests passing (unit + integration + E2E)
- [ ] Ready for development (BMAD + Claude Code can start implementing)

---

**Última Atualização**: 2025-10-10
**Status**: Ready for Development

---

_Estas tech specs fornecem detalhamento suficiente para Allan (solo dev) começar desenvolvimento usando BMAD + Claude Code, com código patterns, exemplos de implementação e testes para cada epic._
