# CarGuroo - Solution Architecture

**Project:** CarGuroo MVP
**Date:** 2025-10-10
**Architect:** Allan
**Status:** Draft v1.0
**PRD Reference:** PRD-CarGuroo-2025-10-10.md
**Epics Reference:** epics-CarGuroo-2025-10-10.md

---

## Executive Summary

Este documento define a arquitetura de solução do **CarGuroo MVP**, uma plataforma SaaS B2B de IA generativa para transformação do pós-venda automotivo. A solução integra dois produtos principais:

1. **Copiloto do Mecânico**: Assistente conversacional para diagnóstico em tempo real
2. **Sistema de Avaliação**: Mapeamento e capacitação de competências baseado em metodologias científicas

**Características Arquiteturais Principais**:
- **Pattern**: Modular Monolith com módulos bem definidos
- **Deployment**: Single-instance containerizado (Docker) para MVP
- **Scale Target**: 450 mecânicos, 30 concessionárias (cliente piloto único)
- **Infrastructure**: Infraestrutura RAG compartilhada entre produtos
- **Development**: Solo developer com BMAD + Claude Code para velocidade máxima

**Complexidades Técnicas Críticas**:
- RAG moderno com vector search para base de conhecimento automotiva
- LLM orchestration para conversação e correção automatizada
- Processamento multimodal (PDF, OCR, speech-to-text)
- Integração WhatsApp Business API
- Compliance LGPD e SSO com sistemas legacy

---

## Table of Contents

1. [System Context](#system-context)
2. [Architecture Decisions (ADRs)](#architecture-decisions-adrs)
3. [High-Level Architecture](#high-level-architecture)
4. [Component Breakdown](#component-breakdown)
5. [Data Architecture](#data-architecture)
6. [Security Architecture](#security-architecture)
7. [Deployment Architecture](#deployment-architecture)
8. [Technology Stack](#technology-stack)
9. [Critical Technical Challenges](#critical-technical-challenges)
10. [Integration Points](#integration-points)
11. [Observability & Operations](#observability--operations)
12. [Next Steps & Open Questions](#next-steps--open-questions)

---

## System Context

### Users and Stakeholders

**Primary Users** (450 total no cliente piloto):
- **Mecânicos** (450): Usuários finais do Copiloto e executantes de avaliações
- **Gestores** (30-50): Gestores de concessionárias e regionais que criam avaliações e analisam dashboards
- **Administradores** (5-10): Equipe de TI da montadora que gerencia usuários e monitora sistema

**External Systems**:
- **DMS (Dealer Management System)**: Sistema legado da montadora para SSO e associação com OS
- **WhatsApp Business API**: Canal primário de comunicação com mecânicos
- **LLM APIs**: OpenAI GPT-4 ou Anthropic Claude para IA generativa
- **Embedding APIs**: OpenAI text-embedding-ada-002 para geração de embeddings
- **Speech-to-Text APIs**: OpenAI Whisper ou Google Cloud Speech para transcrição de áudio
- **OCR Services**: Azure Document Intelligence ou Tesseract para processamento de PDFs escaneados

### Business Context

**Deployment Intent**: MVP single-tenant para validação com único cliente piloto (montadora brasileira)

**Simplificações Críticas do MVP**:
- Single-tenant (sem multi-tenancy)
- Single-instance deployment (sem distributed architecture)
- Escalabilidade moderada (450 users, não 10K+)
- Observabilidade básica (não APM enterprise)
- Deploy cloud OU on-premise (não híbrido)

**Non-MVP Features** (explicitamente fora de escopo):
- Multimodalidade completa (análise de imagem/vídeo)
- Integrações profundas com DMS (apenas SSO no MVP)
- Multi-tenancy e escalabilidade enterprise
- Mobile apps nativos (usa WhatsApp + web responsivo)

---

## Architecture Decisions (ADRs)

### ADR-001: Modular Monolith vs. Microservices

**Decision**: Implementar como **Modular Monolith** com módulos bem definidos

**Context**:
- Solo developer com timeline agressivo (2-3 meses)
- Infraestrutura RAG compartilhada entre Copiloto e Avaliação
- Cliente piloto único (single-tenant)
- Necessidade de iteração rápida

**Rationale**:
- ✅ **Simplicidade**: Desenvolvimento, deploy e debug mais simples
- ✅ **Velocidade**: Menos overhead de comunicação entre serviços
- ✅ **Shared Infrastructure**: RAG naturalmente compartilhado
- ✅ **Refactoring Path**: Pode ser dividido em microservices futuramente se necessário
- ❌ **Tradeoff**: Menos isolamento de falhas, scaling menos granular

**Consequences**:
- Backend único (FastAPI) com módulos: `rag`, `copiloto`, `avaliacao`, `dashboard`, `auth`
- Deploy single-instance (não distribuído)
- Banco de dados compartilhado (PostgreSQL) com schemas separados por módulo
- Future path: Módulos podem ser extraídos para serviços separados se scaling exigir

---

### ADR-002: Monorepo vs. Polyrepo

**Decision**: Usar **Monorepo** para todo o projeto

**Context**:
- Solo developer gerenciando backend, frontend, docs e infra
- Integração tight entre backend/frontend (tipos compartilhados)
- BMAD + Claude Code para geração acelerada de código

**Rationale**:
- ✅ **Atomic Commits**: Mudanças cross-stack em único commit
- ✅ **Shared Types**: Contratos de API compartilhados entre backend/frontend
- ✅ **Simplified CI/CD**: Pipeline único
- ✅ **Easier Navigation**: Developer vê tudo em um lugar
- ❌ **Tradeoff**: Repo pode ficar grande com o tempo

**Structure**:
```
/carguroo
  /backend          # FastAPI application
    /rag            # RAG module
    /copiloto       # Copiloto module
    /avaliacao      # Avaliação module
    /dashboard      # Dashboard/analytics module
    /auth           # Authentication module
    /common         # Shared utilities
  /frontend         # React application
    /src
      /components
      /pages
      /api          # API client (generated from OpenAPI)
  /docs             # Documentation (PRD, architecture, etc.)
  /infra            # Infrastructure as code
    /docker
    /terraform      # or equivalent
    /scripts
  /tests            # E2E tests
```

---

### ADR-003: Vector Database Selection

**Decision**: **Qdrant** (self-hosted) como Vector Database

**Alternatives Considered**:
1. **Pinecone** (managed): Mais caro ($70-200/mês), vendor lock-in, excelente DX
2. **Weaviate** (self-hosted): Mais features, mais complexo, maior footprint
3. **Qdrant** (self-hosted): Performance excelente, simples, Docker-friendly
4. **pgvector** (PostgreSQL extension): Mais simples, mas limitado em scale e features

**Rationale**:
- ✅ **Performance**: HNSW index com <100ms query latency
- ✅ **Cost**: Self-hosted → custo apenas de infra (vs. $70-200/mês do Pinecone)
- ✅ **Simplicity**: Deploy via Docker, API simples
- ✅ **MVP-Friendly**: Fácil de rodar local para desenvolvimento
- ✅ **Future-Proof**: Pode escalar para 10M+ vectors se necessário
- ❌ **Tradeoff**: Precisa gerenciar infra (backup, updates)

**Configuration**:
- Collection: `knowledge_base` com dimensão 1536 (OpenAI embeddings)
- Index: HNSW com `m=16`, `ef_construct=100`
- Payload: `chunk_text`, `document_name`, `page_number`, `chunk_id`
- Distance: Cosine similarity

---

### ADR-004: LLM Provider

**Decision**: **OpenAI GPT-4** como LLM primário para MVP

**Alternatives Considered**:
1. **OpenAI GPT-4**: Mature, alta qualidade, ~$0.03/1K tokens (input)
2. **Anthropic Claude (Opus/Sonnet)**: Competitivo, bom para português, ~$0.015/1K tokens
3. **Open-source (Llama 3)**: Mais barato (infra only), mas requer hosting e fine-tuning

**Rationale**:
- ✅ **Maturity**: API estável, documentação excelente
- ✅ **Quality**: Alta acurácia para tarefas técnicas
- ✅ **Ecosystem**: Integração com LangChain/LlamaIndex
- ✅ **Speed to Market**: Não requer hosting/fine-tuning
- ❌ **Tradeoff**: Custo mais alto (~$0.03/1K tokens input, $0.06/1K output)

**Usage Patterns**:
- **Copiloto**: Geração de respostas técnicas com RAG
- **Avaliação**: Geração de questões situacionais + correção automatizada
- **Estimated Cost**: 450 users × 50 queries/day × ~2K tokens/query × $0.03/1K = ~$2,700/mês

**Cost Optimization**:
- Caching de respostas similares (Redis, TTL 1h)
- Usar GPT-3.5-turbo para tarefas simples (classificação, validação)
- Rate limiting: 50 queries/dia por mecânico

**Fallback Strategy**:
- Se custo > budget: migrar para Claude (Anthropic) ou Llama 3 self-hosted

---

### ADR-005: Chunking Strategy para Manuais Técnicos

**Decision**: **Hybrid Chunking** (section-aware + fixed-size fallback)

**Context**:
- Manuais técnicos automotivos têm estrutura hierárquica (capítulos → seções → procedimentos)
- Chunks precisam ser semanticamente coerentes para busca eficaz
- Chunks muito grandes → embeddings perdem granularidade
- Chunks muito pequenos → perdem contexto

**Rationale**:
- **Primary**: Chunk por seção/procedimento (detectar headers via regex/heurística)
- **Fallback**: Se seção > 1000 tokens, dividir em chunks de 500-1000 tokens com overlap de 100
- ✅ **Semantic Coherence**: Chunks respeitam boundaries naturais do documento
- ✅ **Balanced Size**: ~500-1000 tokens (sweet spot para embeddings)
- ✅ **Context Preservation**: Overlap garante que informações-chave não sejam cortadas

**Implementation**:
- Biblioteca: LangChain `RecursiveCharacterTextSplitter`
- Config: `chunk_size=1000`, `chunk_overlap=100`, `separators=["\n## ", "\n### ", "\n\n", "\n"]`
- Metadados preservados: `document_name`, `page_number`, `section_title` (se detectado)

---

### ADR-006: Deployment Target

**Decision**: Iniciar com **AWS** como deployment target primário, com portabilidade para on-premise

**Context**:
- Cliente pode exigir on-premise por compliance
- Solo developer precisa de velocidade (managed services ajudam)
- MVP não precisa de multi-cloud

**Rationale**:
- ✅ **AWS**: Mature, managed services (RDS, ElastiCache, ALB), bem documentado
- ✅ **Portability**: Containerizado (Docker) → pode migrar para on-premise se necessário
- ✅ **Cost**: Free tier + reasonable pricing para MVP scale
- ❌ **Tradeoff**: Vendor lock-in (mitigado por usar Docker + IaC)

**AWS Services Used** (MVP):
- **Compute**: EC2 (t3.large ou similar) ou ECS (Fargate) para containers
- **Database**: RDS PostgreSQL (db.t3.medium)
- **Cache**: ElastiCache Redis (cache.t3.micro)
- **Storage**: S3 para PDFs e assets
- **Load Balancer**: ALB para HTTPS/TLS
- **Networking**: VPC com subnets públicas/privadas

**On-Premise Fallback**:
- Docker Compose para orquestração simples
- Self-hosted PostgreSQL + Redis + Qdrant
- Nginx como reverse proxy

---

### ADR-007: Authentication & SSO Integration

**Decision**: **SAML 2.0** como protocolo de SSO primário

**Context**:
- Cliente enterprise com DMS legado
- SSO é requirement crítico (NFR-01)
- Mecânicos não devem criar nova senha

**Rationale**:
- ✅ **Enterprise Standard**: SAML 2.0 amplamente suportado por sistemas legados
- ✅ **Security**: Credenciais gerenciadas pelo cliente (não pelo CarGuroo)
- ✅ **Library Support**: python-saml (Python) bem mantido
- ❌ **Tradeoff**: Mais complexo que OAuth 2.0, requer setup com IdP do cliente

**Fallback**: OAuth 2.0 se DMS do cliente não suportar SAML

**Implementation**:
- Library: `python-saml` ou `python3-saml`
- Identity Provider (IdP): Configurado pela montadora
- Service Provider (SP): CarGuroo backend
- Atributos mapeados: `cpf`, `name`, `email`, `role`, `dealership_id`
- Session: JWT token com TTL 8h, armazenado em Redis

**Non-SSO Users** (Admin do CarGuroo):
- Login via username/password com bcrypt hash
- 2FA via TOTP (Google Authenticator)

---

### ADR-008: Message Queue for Async Processing

**Decision**: **Celery + Redis** como message queue/broker

**Alternatives Considered**:
1. **Celery + RabbitMQ**: Mais robusto, mais complexo
2. **Celery + Redis**: Mais simples, suficiente para MVP
3. **Dramatiq**: Moderno, mas menos maduro
4. **AWS SQS + Lambda**: Serverless, mas mais vendor lock-in

**Rationale**:
- ✅ **Simplicity**: Redis já usado para cache → reusar como broker
- ✅ **Mature**: Celery é battle-tested para background jobs
- ✅ **Good Enough**: Redis suficiente para ~1000 jobs/dia do MVP
- ✅ **DX**: Celery bem integrado com FastAPI/Python ecosystem
- ❌ **Tradeoff**: Redis menos durável que RabbitMQ (mas acceptable para MVP)

**Usage Patterns**:
- **Document Processing**: PDF → chunks → embeddings → vector DB (Epic 1)
- **Assessment Auto-Grading**: Correção de 30 questões após mecânico completar (Epic 3)
- **Notifications**: Batch send de WhatsApp messages (Epic 3)

**Configuration**:
- Task queue: `default` (priority normal), `high_priority` (notifications, grading)
- Concurrency: 4 workers (matching CPU cores)
- Result backend: Redis (TTL 24h)

---

### ADR-009: Frontend State Management

**Decision**: **React Query + Context API** (sem Redux)

**Context**:
- Frontend relativamente simples (dashboards + formulários)
- Solo developer → simplicidade over boilerplate
- Necessidade de server state caching para performance

**Rationale**:
- ✅ **React Query**: Excelente para server state (caching, invalidation, refetching)
- ✅ **Context API**: Suficiente para client state (user session, UI state)
- ✅ **Less Boilerplate**: Sem actions/reducers do Redux
- ✅ **DX**: Menos código para manter
- ❌ **Tradeoff**: Menos estrutura que Redux (mas desnecessário para MVP)

**State Categories**:
- **Server State**: React Query (dashboards, avaliações, usuários)
- **Client State**: Context API (tema, idioma, user session)
- **Form State**: React Hook Form (validação, submit)

---

### ADR-010: Observability Stack

**Decision**: **Prometheus + Grafana + ELK** (self-hosted) para MVP

**Alternatives Considered**:
1. **Datadog/New Relic** (managed): Easier setup, mais caro ($30-100/mês)
2. **Prometheus + Grafana** (self-hosted): Free, mais setup
3. **CloudWatch** (AWS native): OK, mas menos features

**Rationale**:
- ✅ **Cost**: Self-hosted → custo apenas de infra (~$20/mês)
- ✅ **Flexibility**: Full control, custom dashboards
- ✅ **Learning**: Allan ganha experiência com observability stack padrão da indústria
- ❌ **Tradeoff**: Mais setup e manutenção vs. managed

**Components**:
- **Metrics**: Prometheus (scraping) + Grafana (visualization)
- **Logs**: ELK stack (Elasticsearch + Logstash + Kibana) ou Loki (lightweight alternative)
- **Traces**: OpenTelemetry (opcional para MVP, pode adicionar depois)
- **Alerting**: Prometheus Alertmanager → Slack/Email

**Migration Path**: Se manutenção ficar pesada, migrar para Datadog após MVP validado

---

## High-Level Architecture

### Architecture Diagram (C4 Model - Level 1: System Context)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CarGuroo System                               │
│                                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │   Copiloto   │   │   Avaliação  │   │   Dashboard  │              │
│  │   do         │   │   Sistema    │   │   Gestores   │              │
│  │   Mecânico   │   │              │   │              │              │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘              │
│         │                  │                  │                       │
│         └──────────────────┼──────────────────┘                       │
│                            │                                          │
│                   ┌────────▼────────┐                                 │
│                   │  RAG Engine     │                                 │
│                   │  (Shared)       │                                 │
│                   └─────────────────┘                                 │
└─────────────────────────────────────────────────────────────────────────┘
         │                      │                      │
         │                      │                      │
         ▼                      ▼                      ▼
   ┌─────────┐           ┌──────────┐          ┌──────────┐
   │WhatsApp │           │   LLM    │          │   DMS    │
   │Business │           │   APIs   │          │  (SSO)   │
   │   API   │           │ (OpenAI) │          │          │
   └─────────┘           └──────────┘          └──────────┘

Users:
- Mecânicos (450) ──→ WhatsApp ──→ Copiloto
- Gestores (30-50) ──→ Web Dashboard ──→ Avaliação + Dashboard
- Admins (5-10) ──→ Web Dashboard ──→ Admin Interface
```

### Architecture Diagram (C4 Model - Level 2: Container)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CarGuroo Platform                                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Backend (FastAPI)                            │   │
│  │                                                                 │   │
│  │  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐     │   │
│  │  │   RAG    │  │ Copiloto  │  │Avaliação │  │Dashboard │     │   │
│  │  │  Module  │  │  Module   │  │  Module  │  │  Module  │     │   │
│  │  └────┬─────┘  └─────┬─────┘  └────┬─────┘  └────┬─────┘     │   │
│  │       │              │              │             │           │   │
│  │       └──────────────┴──────────────┴─────────────┘           │   │
│  │                              │                                 │   │
│  │                     ┌────────▼────────┐                       │   │
│  │                     │  Auth Module    │                       │   │
│  │                     │  (SSO, RBAC)    │                       │   │
│  │                     └─────────────────┘                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Frontend (React SPA)                           │   │
│  │                                                             │   │
│  │  Dashboard UI │ Assessment UI │ Admin UI │ Mobile-Responsive │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐         │
│  │  PostgreSQL   │  │     Redis     │  │    Qdrant     │         │
│  │  (Primary DB) │  │(Cache+Queue)  │  │  (Vector DB)  │         │
│  └───────────────┘  └───────────────┘  └───────────────┘         │
│                                                                     │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐         │
│  │  Celery       │  │  Prometheus   │  │  Elasticsearch│         │
│  │  Workers      │  │  + Grafana    │  │  + Kibana     │         │
│  └───────────────┘  └───────────────┘  └───────────────┘         │
└─────────────────────────────────────────────────────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
     ┌──────────┐       ┌──────────┐       ┌──────────┐
     │ WhatsApp │       │   LLM    │       │   DMS    │
     │    API   │       │   APIs   │       │   SSO    │
     └──────────┘       └──────────┘       └──────────┘
```

---

## Component Breakdown

### Backend Modules (FastAPI Monolith)

#### 1. RAG Module (`/backend/rag`)

**Responsibility**: Infraestrutura compartilhada de Retrieval Augmented Generation

**Sub-modules**:
- **Ingestion** (`rag/ingestion`): Upload, validação, armazenamento de PDFs
- **Processing** (`rag/processing`): Extração de texto, OCR, chunking
- **Embedding** (`rag/embedding`): Geração de embeddings via OpenAI API
- **Indexing** (`rag/indexing`): Inserção de vectors no Qdrant
- **Search** (`rag/search`): Busca semântica com similarity ranking

**Key APIs**:
- `POST /api/v1/documents/upload` - Upload de documento
- `GET /api/v1/search` - Busca semântica (query → top-K chunks)
- `GET /api/v1/documents` - Listar documentos indexados
- `DELETE /api/v1/documents/{id}` - Deletar documento + chunks

**Dependencies**:
- **External**: OpenAI Embedding API, Qdrant, S3 (storage)
- **Internal**: Celery (async processing), PostgreSQL (metadata)

**Epic Coverage**: Epic 1 (US-RAG-01 a US-RAG-09)

---

#### 2. Copiloto Module (`/backend/copiloto`)

**Responsibility**: Interface conversacional para diagnóstico assistido

**Sub-modules**:
- **Chat** (`copiloto/chat`): Gestão de conversação, state machine
- **LLM** (`copiloto/llm`): Orchestration de chamadas LLM, prompt engineering
- **WhatsApp** (`copiloto/whatsapp`): Integração com WhatsApp Business API
- **Voice** (`copiloto/voice`): Speech-to-text para áudio
- **History** (`copiloto/history`): Persistência de interações por OS

**Key APIs**:
- `POST /api/v1/copiloto/message` - Enviar mensagem (webhook do WhatsApp)
- `GET /api/v1/copiloto/history/{os_id}` - Histórico de conversa por OS
- `POST /api/v1/copiloto/feedback` - Registro de feedback de utilidade

**Key Workflows**:
1. **Consulta Simples**: Query → RAG search → LLM generation → Resposta com citações
2. **Diagnóstico Guiado**: Query → Detectar diagnóstico → Perguntas sequenciais → Diagnóstico final
3. **Input de Áudio**: Áudio → STT → Processar como texto

**Dependencies**:
- **External**: WhatsApp API (Twilio/Meta), OpenAI GPT-4, OpenAI Whisper
- **Internal**: RAG Module (search), Redis (sessions), PostgreSQL (messages)

**Epic Coverage**: Epic 2 (US-COP-01 a US-COP-11)

---

#### 3. Avaliação Module (`/backend/avaliacao`)

**Responsibility**: Criação, execução e correção automatizada de avaliações

**Sub-modules**:
- **Cycles** (`avaliacao/cycles`): CRUD de ciclos de avaliação
- **Questions** (`avaliacao/questions`): Geração de questões via LLM + RAG
- **Execution** (`avaliacao/execution`): Gestão de estado de avaliação do mecânico
- **Grading** (`avaliacao/grading`): Correção automatizada via LLM com rubricas
- **Classification** (`avaliacao/classification`): Classificação em níveis (Iniciante/Adequado/Experiente)

**Key APIs**:
- `POST /api/v1/assessments/cycles` - Criar ciclo de avaliação
- `POST /api/v1/assessments/cycles/{id}/generate-questions` - Gerar questões via IA
- `POST /api/v1/assessments/execute` - Responder questão (via WhatsApp webhook)
- `GET /api/v1/assessments/results/{mechanic_id}` - Resultados de mecânico
- `POST /api/v1/assessments/review` - Revisão manual de resposta ambígua

**Key Workflows**:
1. **Criação de Ciclo**: Wizard → Gerar questões (LLM + RAG) → Revisar → Publicar → Notificar mecânicos
2. **Execução**: Mecânico inicia → Questões sequenciais via chat → Salvar respostas
3. **Correção**: Auto-grading (LLM vs. rubrica) → Sinalizar ambíguos → Revisão manual → Classificação final

**Dependencies**:
- **External**: OpenAI GPT-4 (geração + correção), WhatsApp API (notificações)
- **Internal**: RAG Module (questões contextualizadas), Copiloto Module (chat interface), PostgreSQL

**Epic Coverage**: Epic 3 (US-AVA-01 a US-AVA-09)

---

#### 4. Dashboard Module (`/backend/dashboard`)

**Responsibility**: Analytics e visibilidade de competências para gestores

**Sub-modules**:
- **Aggregations** (`dashboard/aggregations`): Pré-computação de métricas (materialized views)
- **Exports** (`dashboard/exports`): Geração de CSVs, Excel, PDFs
- **Alerts** (`dashboard/alerts`): Detecção de gaps críticos e alertas proativos

**Key APIs**:
- `GET /api/v1/dashboard/overview` - Visão agregada (KPIs principais)
- `GET /api/v1/dashboard/mechanics/{id}` - Drill-down individual
- `GET /api/v1/dashboard/gaps` - Gaps críticos identificados
- `GET /api/v1/dashboard/trends` - Tendências temporais
- `POST /api/v1/dashboard/export` - Exportar dados (CSV/Excel/JSON)

**Key Metrics**:
- **Business**: WAU (Copiloto), Taxa de conclusão (Avaliação), Distribuição por nível
- **Operational**: Latência p95, Error rate, Custo de LLM

**Dependencies**:
- **Internal**: Avaliação Module (dados de competências), Copiloto Module (métricas de uso), PostgreSQL (agregações)

**Epic Coverage**: Epic 4 (US-DASH-01 a US-DASH-07)

---

#### 5. Auth Module (`/backend/auth`)

**Responsibility**: Autenticação, autorização e gestão de usuários

**Sub-modules**:
- **SSO** (`auth/sso`): Integração SAML 2.0 com DMS da montadora
- **RBAC** (`auth/rbac`): Controle de permissões por role
- **Users** (`auth/users`): CRUD de usuários, bulk import

**Key APIs**:
- `POST /api/v1/auth/login` - Login via SSO (SAML callback)
- `POST /api/v1/auth/logout` - Logout e invalidação de sessão
- `GET /api/v1/auth/me` - Informações do usuário autenticado
- `GET /api/v1/users` - Listar usuários (admin only)
- `POST /api/v1/users` - Criar usuário (admin only)

**Roles**:
- **Admin**: Full access (gestão de usuários, configuração)
- **Gestor**: Criar avaliações, ver dashboards, exportar dados
- **Mecânico**: Responder avaliações, usar Copiloto

**Dependencies**:
- **External**: DMS (Identity Provider SAML)
- **Internal**: Redis (sessions), PostgreSQL (users, roles)

**Epic Coverage**: Epic 5 (US-AUTH-01 a US-AUTH-03)

---

### Frontend Application (React SPA)

**Structure**:
```
/frontend/src
  /pages
    /dashboard         # Dashboards de gestores
    /assessments       # Criação e gestão de avaliações
    /copiloto-history  # Histórico de interações do Copiloto
    /admin             # Gestão de usuários e sistema
  /components
    /charts            # Componentes de visualização (Chart.js)
    /forms             # Formulários (React Hook Form)
    /common            # Botões, inputs, modals reutilizáveis
  /api
    /client.ts         # API client (gerado de OpenAPI spec)
  /hooks
    /useAuth.ts        # Hook de autenticação
    /useDashboard.ts   # React Query hooks
  /contexts
    /AuthContext.tsx   # Context API para session
```

**Key Technologies**:
- **Framework**: React 18 + TypeScript
- **Routing**: React Router v6
- **State**: React Query (server state) + Context API (client state)
- **Forms**: React Hook Form + Zod (validation)
- **Charts**: Chart.js + react-chartjs-2
- **Styling**: Tailwind CSS (utility-first)
- **Build**: Vite (fast dev server + HMR)

**Accessibility**: WCAG 2.1 Level AA compliance (NFR-07)

---

## Data Architecture

### PostgreSQL Database Schema

**Database**: `carguroo_db`

#### Schema: `auth`

**Table: `users`**
```sql
CREATE TABLE auth.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cpf VARCHAR(11) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'gestor', 'mecanico')),
  dealership_id UUID REFERENCES auth.dealerships(id),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_cpf ON auth.users(cpf);
CREATE INDEX idx_users_role ON auth.users(role);
```

**Table: `dealerships`**
```sql
CREATE TABLE auth.dealerships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  region VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

#### Schema: `rag`

**Table: `documents`**
```sql
CREATE TABLE rag.documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  s3_key VARCHAR(500) NOT NULL,
  file_size_bytes BIGINT,
  status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'error')),
  uploaded_by UUID REFERENCES auth.users(id),
  uploaded_at TIMESTAMP DEFAULT NOW(),
  processed_at TIMESTAMP,
  total_chunks INTEGER,
  error_message TEXT
);

CREATE INDEX idx_documents_status ON rag.documents(status);
```

**Table: `chunks`** (metadados, vectors ficam no Qdrant)
```sql
CREATE TABLE rag.chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES rag.documents(id) ON DELETE CASCADE,
  chunk_index INTEGER NOT NULL,
  chunk_text TEXT NOT NULL,
  page_number INTEGER,
  section_title VARCHAR(500),
  qdrant_point_id UUID NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chunks_document_id ON rag.chunks(document_id);
CREATE INDEX idx_chunks_qdrant_point_id ON rag.chunks(qdrant_point_id);
```

---

#### Schema: `copiloto`

**Table: `conversations`**
```sql
CREATE TABLE copiloto.conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mechanic_id UUID REFERENCES auth.users(id),
  os_number VARCHAR(50),
  whatsapp_number VARCHAR(20),
  started_at TIMESTAMP DEFAULT NOW(),
  last_message_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'closed'))
);

CREATE INDEX idx_conversations_mechanic ON copiloto.conversations(mechanic_id);
CREATE INDEX idx_conversations_os ON copiloto.conversations(os_number);
```

**Table: `messages`**
```sql
CREATE TABLE copiloto.messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES copiloto.conversations(id) ON DELETE CASCADE,
  sender VARCHAR(50) NOT NULL CHECK (sender IN ('mechanic', 'copiloto')),
  message_text TEXT NOT NULL,
  message_type VARCHAR(50) DEFAULT 'text' CHECK (message_type IN ('text', 'audio')),
  cited_sources JSONB,
  feedback BOOLEAN,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON copiloto.messages(conversation_id);
CREATE INDEX idx_messages_created_at ON copiloto.messages(created_at DESC);
```

---

#### Schema: `avaliacao`

**Table: `assessment_cycles`**
```sql
CREATE TABLE avaliacao.assessment_cycles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  phase VARCHAR(50) NOT NULL CHECK (phase IN ('phase_1', 'phase_2', 'phase_3')),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  created_by UUID REFERENCES auth.users(id),
  status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'in_progress', 'completed')),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cycles_status ON avaliacao.assessment_cycles(status);
```

**Table: `questions`**
```sql
CREATE TABLE avaliacao.questions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cycle_id UUID REFERENCES avaliacao.assessment_cycles(id) ON DELETE CASCADE,
  question_index INTEGER NOT NULL,
  question_text TEXT NOT NULL,
  rubric JSONB NOT NULL, -- 4-level rubric: inadequado, parcial, adequado, excelente
  metadata JSONB, -- area_tecnica, nivel_bloom, dificuldade
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_cycle ON avaliacao.questions(cycle_id);
```

**Table: `mechanic_assessments`**
```sql
CREATE TABLE avaliacao.mechanic_assessments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cycle_id UUID REFERENCES avaliacao.assessment_cycles(id),
  mechanic_id UUID REFERENCES auth.users(id),
  status VARCHAR(50) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
  current_question_index INTEGER DEFAULT 0,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  classification VARCHAR(50), -- iniciante, adequado, experiente, etc.
  score_percentage NUMERIC(5,2)
);

CREATE UNIQUE INDEX idx_mechanic_assessments_unique ON avaliacao.mechanic_assessments(cycle_id, mechanic_id);
```

**Table: `responses`**
```sql
CREATE TABLE avaliacao.responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  assessment_id UUID REFERENCES avaliacao.mechanic_assessments(id) ON DELETE CASCADE,
  question_id UUID REFERENCES avaliacao.questions(id),
  response_text TEXT NOT NULL,
  ai_score INTEGER CHECK (ai_score BETWEEN 1 AND 4),
  ai_rationale TEXT,
  ai_confidence NUMERIC(3,2),
  human_reviewed BOOLEAN DEFAULT FALSE,
  human_score INTEGER CHECK (human_score BETWEEN 1 AND 4),
  human_rationale TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_responses_assessment ON avaliacao.responses(assessment_id);
CREATE INDEX idx_responses_needs_review ON avaliacao.responses(human_reviewed) WHERE ai_confidence < 0.70;
```

---

### Qdrant Vector Database

**Collection**: `knowledge_base`

**Configuration**:
```python
{
  "vectors": {
    "size": 1536,  # OpenAI text-embedding-ada-002 dimension
    "distance": "Cosine"
  },
  "optimizers_config": {
    "indexing_threshold": 10000
  },
  "hnsw_config": {
    "m": 16,
    "ef_construct": 100
  }
}
```

**Point Payload Structure**:
```json
{
  "chunk_id": "uuid",
  "document_id": "uuid",
  "document_name": "Manual Técnico Modelo XYZ-2023.pdf",
  "chunk_text": "Para trocar a pastilha de freio...",
  "page_number": 142,
  "section_title": "Procedimento de Troca - Freios Dianteiros",
  "chunk_index": 87
}
```

**Query Example**:
```python
search_result = qdrant_client.search(
    collection_name="knowledge_base",
    query_vector=embedding,  # 1536-dim vector
    limit=5,
    score_threshold=0.6,
    with_payload=True
)
```

---

### Redis Data Structures

**Use Cases**:
1. **Session Storage**: JWT tokens, user sessions (TTL 8h)
2. **Rate Limiting**: Copiloto queries per mechanic (TTL 24h)
3. **Caching**: Query results, embeddings (TTL 1h)
4. **Message Queue**: Celery broker for background tasks
5. **Conversation State**: Mecânico's current assessment state (TTL 7 days)

**Key Patterns**:
```
# Session
session:{user_id} → {jwt_token, expires_at, metadata}

# Rate Limiting
rate_limit:copiloto:{mechanic_id}:{date} → count

# Query Cache
query_cache:hash({query_text}) → {search_results, timestamp}

# Conversation State
conv_state:{mechanic_id} → {assessment_id, current_question_index, responses[]}
```

---

## Security Architecture

### Authentication Flow (SAML SSO)

```
1. User → Access CarGuroo Dashboard
2. Backend → Redirect to DMS IdP (SAML AuthnRequest)
3. DMS IdP → User authenticates with corporate credentials
4. DMS IdP → SAML Assertion (signed) → CarGuroo SP
5. Backend → Validate assertion signature
6. Backend → Extract attributes (cpf, name, role, dealership)
7. Backend → Lookup/create user in DB
8. Backend → Generate JWT token (HS256, TTL 8h)
9. Backend → Store session in Redis
10. Backend → Return JWT to frontend
11. Frontend → Store JWT in memory (not localStorage for security)
12. Frontend → Include JWT in Authorization header for all API calls
```

**WhatsApp Authentication**:
- Mecânico envia CPF → Lookup em `users` table → Criar sessão
- Session armazenada em Redis: `whatsapp_session:{phone_number}` → `{user_id, cpf, authenticated_at}`

### Authorization (RBAC)

**Enforcement**:
```python
# Decorator-based
@require_role("gestor")
async def create_assessment_cycle(request):
    ...

# Middleware
if not has_permission(user, "dashboard:view"):
    raise HTTPException(status_code=403)
```

**Permission Matrix**:
| Resource               | Admin | Gestor | Mecânico |
|------------------------|-------|--------|----------|
| Criar Avaliação        | ✅     | ✅      | ❌        |
| Ver Dashboard Agregado | ✅     | ✅      | ❌        |
| Ver Perfil Individual  | ✅     | ✅      | ✅ (own)  |
| Usar Copiloto          | ✅     | ✅      | ✅        |
| Gestão de Usuários     | ✅     | ❌      | ❌        |
| Upload de Documentos   | ✅     | ❌      | ❌        |

### Data Encryption

**In Transit**:
- **TLS 1.3** em todas as conexões HTTP (enforced por ALB/Load Balancer)
- **Certificate**: Let's Encrypt ou AWS ACM

**At Rest**:
- **PostgreSQL**: Transparent Data Encryption (TDE) ou field-level encryption para CPF
- **S3**: Server-side encryption (SSE-S3 ou SSE-KMS)
- **Redis**: Não armazena dados sensíveis long-term (apenas sessions com TTL)
- **Qdrant**: Vectors não são sensíveis (apenas embeddings de texto técnico)

**Sensitive Fields Encryption** (CPF):
```python
# Encrypt before storing
encrypted_cpf = encrypt_aes_256(cpf, key=settings.ENCRYPTION_KEY)

# Decrypt on read
cpf = decrypt_aes_256(encrypted_cpf, key=settings.ENCRYPTION_KEY)
```

### LGPD Compliance

**Data Subject Rights**:
1. **Right to Access**: API endpoint `/api/v1/gdpr/data-export/{user_id}` → Exporta todos os dados do usuário
2. **Right to Deletion**: Soft delete + cascade delete após 48h
3. **Right to Rectification**: CRUD de usuários permite atualização
4. **Data Minimization**: Coletar apenas dados necessários (CPF, nome, role)

**Audit Logging**:
```sql
CREATE TABLE auth.audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  action VARCHAR(100) NOT NULL, -- 'user_created', 'user_deleted', 'data_accessed'
  resource_type VARCHAR(100),
  resource_id UUID,
  metadata JSONB,
  ip_address INET,
  timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON auth.audit_log(user_id);
CREATE INDEX idx_audit_timestamp ON auth.audit_log(timestamp DESC);
```

**Data Retention**:
- **Conversations**: 2 anos → auto-delete
- **Assessments**: 2 anos → auto-delete
- **Audit Logs**: 5 anos (compliance requirement)

---

## Deployment Architecture

### MVP Deployment (Single-Instance AWS)

**Infrastructure Components**:
```
┌──────────────────────────────────────────────────────────────┐
│                        AWS VPC                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Public Subnet (ALB)                         │   │
│  │                                                      │   │
│  │  ┌─────────────────────┐                            │   │
│  │  │  Application        │  ← HTTPS (TLS 1.3)        │   │
│  │  │  Load Balancer      │                            │   │
│  │  └──────────┬──────────┘                            │   │
│  └─────────────│─────────────────────────────────────┘   │
│                │                                          │
│  ┌─────────────▼─────────────────────────────────────┐   │
│  │          Private Subnet (Compute)                 │   │
│  │                                                    │   │
│  │  ┌─────────────────┐   ┌─────────────────┐       │   │
│  │  │  Backend        │   │  Frontend       │       │   │
│  │  │  (FastAPI)      │   │  (React SPA)    │       │   │
│  │  │  EC2/ECS        │   │  S3 + CloudFront│       │   │
│  │  └────────┬────────┘   └─────────────────┘       │   │
│  │           │                                        │   │
│  │  ┌────────▼──────────────────────────────────┐   │   │
│  │  │         Data Layer                        │   │   │
│  │  │                                           │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │   │
│  │  │  │PostgreSQL│  │  Redis   │  │ Qdrant │ │   │   │
│  │  │  │  RDS     │  │ElastiCache│ │ EC2    │ │   │   │
│  │  │  └──────────┘  └──────────┘  └────────┘ │   │   │
│  │  └───────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────┘   │
│                                                    │
│  ┌────────────────────────────────────────────┐   │
│  │  Storage & Monitoring                      │   │
│  │                                            │   │
│  │  S3 (PDFs) │ CloudWatch │ Prometheus+Grafana │
│  └────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

**AWS Resource Specifications** (MVP):
- **Compute**: EC2 t3.large (2 vCPU, 8GB RAM) ou ECS Fargate (1 task, 2 vCPU, 4GB)
- **Database**: RDS PostgreSQL db.t3.medium (2 vCPU, 4GB RAM, 100GB SSD)
- **Cache**: ElastiCache Redis cache.t3.micro (1 vCPU, 0.5GB RAM)
- **Vector DB**: EC2 t3.medium para Qdrant (2 vCPU, 4GB RAM, 50GB SSD)
- **Storage**: S3 Standard (50GB estimado para manuais técnicos)
- **Load Balancer**: ALB (Application Load Balancer)
- **CDN**: CloudFront para frontend (opcional para MVP)

**Estimated Monthly Cost** (AWS):
- EC2 (backend): ~$60/mês (t3.large)
- RDS PostgreSQL: ~$70/mês (db.t3.medium + storage)
- ElastiCache Redis: ~$15/mês (cache.t3.micro)
- EC2 (Qdrant): ~$40/mês (t3.medium)
- S3 + transfer: ~$10/mês
- ALB: ~$20/mês
- **Total**: ~$215/mês (infra) + ~$2,700/mês (LLM APIs) = **$2,915/mês (~R$ 14.5K/mês)**

---

### Docker Compose (Development & On-Premise Fallback)

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/carguroo_db
      - REDIS_URL=redis://redis:6379/0
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - postgres
      - redis
      - qdrant
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=carguroo_user
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=carguroo_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  qdrant:
    image: qdrant/qdrant:v1.7.4
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

  celery_worker:
    build: ./backend
    command: celery -A app.worker worker --loglevel=info --concurrency=4
    depends_on:
      - redis
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/carguroo_db
      - REDIS_URL=redis://redis:6379/0

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./infra/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  prometheus_data:
  grafana_data:
```

**Commands**:
```bash
# Development
docker-compose up -d

# Logs
docker-compose logs -f backend

# Rebuild after code changes
docker-compose up -d --build backend

# Stop all services
docker-compose down
```

---

### CI/CD Pipeline (GitHub Actions)

**Workflow**: `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: carguroo-backend
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG ./backend
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster carguroo-cluster --service backend --force-new-deployment
```

**Deployment Stages**:
1. **Develop Branch**: Auto-deploy to staging environment
2. **Main Branch**: Auto-deploy to production (after manual approval)
3. **Pull Requests**: Run tests only (no deploy)

---

## Technology Stack

### Backend Stack

| Component            | Technology                  | Version | Rationale |
|----------------------|----------------------------|---------|-----------|
| **Language**         | Python                     | 3.11+   | Ecossistema IA/ML rico, rápido desenvolvimento |
| **Web Framework**    | FastAPI                    | 0.104+  | Async, type hints, auto OpenAPI docs |
| **ORM**              | SQLAlchemy                 | 2.0+    | Mature, async support, type-safe |
| **Migrations**       | Alembic                    | 1.12+   | Padrão para SQLAlchemy |
| **Validation**       | Pydantic                   | 2.0+    | Type validation, JSON schemas |
| **LLM Orchestration**| LangChain                  | 0.1+    | RAG patterns, prompt templates |
| **Vector DB Client** | qdrant-client              | 1.7+    | Official Qdrant Python client |
| **Auth**             | python-saml                | 1.15+   | SAML 2.0 integration |
| **Background Jobs**  | Celery                     | 5.3+    | Async task processing |
| **HTTP Client**      | httpx                      | 0.25+   | Async HTTP, better than requests |
| **Testing**          | pytest + pytest-asyncio    | 7.4+    | Async test support |

### Frontend Stack

| Component            | Technology                  | Version | Rationale |
|----------------------|----------------------------|---------|-----------|
| **Framework**        | React                      | 18+     | Mature, large ecosystem |
| **Language**         | TypeScript                 | 5.0+    | Type safety, better DX |
| **Build Tool**       | Vite                       | 5.0+    | Fast HMR, modern |
| **Routing**          | React Router               | 6+      | Standard para SPAs |
| **State (Server)**   | React Query (TanStack)     | 5.0+    | Caching, refetching, mutations |
| **State (Client)**   | Context API                | -       | Simples, built-in |
| **Forms**            | React Hook Form            | 7.0+    | Performance, validation |
| **Validation**       | Zod                        | 3.22+   | Type-safe schemas |
| **Charts**           | Chart.js + react-chartjs-2 | 4.4+    | Flexible, bem documentado |
| **Styling**          | Tailwind CSS               | 3.3+    | Utility-first, produtivo |
| **HTTP Client**      | Axios                      | 1.6+    | Interceptors, type-safe |
| **Testing**          | Vitest + Testing Library   | 1.0+    | Fast, Vite-native |

### Data Stack

| Component            | Technology                  | Version | Rationale |
|----------------------|----------------------------|---------|-----------|
| **Relational DB**    | PostgreSQL                 | 15+     | ACID, mature, extensible |
| **Vector DB**        | Qdrant                     | 1.7+    | Performance, self-hosted |
| **Cache/Queue**      | Redis                      | 7+      | In-memory, versatile |
| **Object Storage**   | AWS S3 (or MinIO)          | -       | Scalable, durable |

### AI/ML Stack

| Component            | Technology                  | Version | Rationale |
|----------------------|----------------------------|---------|-----------|
| **LLM**              | OpenAI GPT-4               | -       | Alta qualidade, mature |
| **Embeddings**       | OpenAI text-embedding-ada-002 | -    | Padrão da indústria |
| **Speech-to-Text**   | OpenAI Whisper API         | -       | Acurácia excelente |
| **OCR**              | Azure Document Intelligence| -       | Melhor para PDFs técnicos |

### Infrastructure Stack

| Component            | Technology                  | Version | Rationale |
|----------------------|----------------------------|---------|-----------|
| **Containers**       | Docker                     | 24+     | Padrão de facto |
| **Orchestration**    | Docker Compose (MVP)       | 2.0+    | Simples para MVP |
| **Cloud**            | AWS                        | -       | Mature, managed services |
| **IaC**              | Terraform (future)         | 1.6+    | Infrastructure as Code |
| **CI/CD**            | GitHub Actions             | -       | Integrado com GitHub |
| **Monitoring**       | Prometheus + Grafana       | -       | Open-source, flexible |
| **Logging**          | ELK Stack or Loki          | -       | Centralized logs |

---

## Critical Technical Challenges

### Challenge 1: RAG Accuracy for Automotive Technical Content

**Problem**:
- Manuais técnicos automotivos têm linguagem específica, diagramas, tabelas
- Chunking inadequado → perda de contexto
- Embeddings genéricos podem não capturar semântica técnica

**Mitigation**:
1. **POC Técnico**: Testar 3 estratégias de chunking com amostra de 200 páginas
2. **Hybrid Search**: Combinar semantic search (embeddings) com keyword search (BM25)
3. **Re-ranking**: Usar LLM para re-rankar top-10 chunks antes de gerar resposta
4. **Feedback Loop**: Registrar queries com feedback negativo → melhorar chunking
5. **Human-in-the-Loop**: Curadoria de documentos críticos (manuais mais consultados)

**Success Metric**: Acurácia de busca >80% validada por especialistas (US-RAG-09)

---

### Challenge 2: LLM Cost Control

**Problem**:
- 450 mecânicos × 50 queries/dia × ~2K tokens/query × $0.03/1K = ~$2,700/mês
- Budget pode estourar se uso for maior que esperado

**Mitigation**:
1. **Caching Agressivo**: Redis cache para queries similares (hit rate target: 30%)
2. **Rate Limiting**: 50 queries/dia por mecânico (US-COP-09)
3. **Tiered Models**: GPT-3.5-turbo para tarefas simples (classificação, validação)
4. **Prompt Optimization**: Reduzir tokens de contexto sem perder qualidade
5. **Monitoring**: Alertas se custo diário > threshold ($100/dia)

**Fallback**: Migrar para Claude (Anthropic) ou Llama 3 self-hosted se custo > R$ 15K/mês

---

### Challenge 3: WhatsApp API Integration Complexity

**Problem**:
- WhatsApp Business API tem rate limits estritos
- Mensagens template precisam pré-aprovação do Meta
- Webhook pode receber mensagens duplicadas ou fora de ordem

**Mitigation**:
1. **Meta Business API**: Usar API oficial (não Twilio) para evitar custos adicionais
2. **Template Pre-approval**: Criar templates genéricos durante setup (US-AVA-04)
3. **Idempotency**: Usar `message_id` do WhatsApp para deduplicar mensagens
4. **Queue**: Enviar mensagens via Celery para respeitar rate limits (não enviar direto)
5. **Fallback**: Web chat como alternativa se WhatsApp falhar

**Success Metric**: 99% de mensagens entregues em <10s (p95)

---

### Challenge 4: Assessment Auto-Grading Reliability

**Problem**:
- Correção automatizada de respostas situacionais é complexa
- IA pode ter viés ou baixa concordância com humanos
- Mecânicos podem questionar justiça da correção

**Mitigation**:
1. **Human-in-the-Loop**: Respostas com confidence <70% vão para revisão manual (US-AVA-08)
2. **Rubric Engineering**: Rubricas detalhadas de 4 níveis validadas por especialistas
3. **Inter-rater Reliability**: Medir concordância IA vs. humano (target: Kappa >0.75)
4. **Calibration**: Revisar amostra de 50 respostas por ciclo para calibrar IA
5. **Transparency**: Mostrar rubrica e justificativa da IA para mecânico

**Success Metric**: Concordância >80% (NFR-04), <20% de respostas precisando revisão manual

---

### Challenge 5: SSO Integration with Legacy DMS

**Problem**:
- DMS legado pode ter APIs mal documentadas ou inexistentes
- SAML 2.0 pode não ser suportado
- Delay no setup de SSO pode bloquear desenvolvimento

**Mitigation**:
1. **Sprint 0**: Confirmar suporte a SAML/OAuth com TI da montadora (semana 1)
2. **Fallback**: Implementar login básico (username/password) como plano B
3. **Stub**: Criar IdP stub para desenvolvimento local (não bloqueia backend)
4. **Documentation**: Documentar fluxo SAML em detalhes para facilitar troubleshooting
5. **Timeline**: Integração SSO tem 2 semanas de buffer (não critical path para Copiloto MVP)

**Success Metric**: SSO funcional ou fallback implementado até Sprint 3

---

### Challenge 6: Solo Developer Velocity vs. Scope

**Problem**:
- 41 user stories em 2-3 meses = ~3-4 stories/semana
- Risco de burnout ou atraso crítico
- Dependências externas podem bloquear progresso

**Mitigation**:
1. **BMAD + Claude Code**: Usar IA para gerar boilerplate e acelerar desenvolvimento
2. **Ruthless Prioritization**: Focar em Epic 1 → 2 → 3 (Copiloto MVP primeiro)
3. **MVP dentro do MVP**: Entregar Copiloto funcional em 6 semanas, Avaliação em mais 4
4. **Buffer**: Planejar para 3 meses, ter flexibilidade para 4 se necessário
5. **Async Work**: Não bloquear em dependências externas (usar stubs/mocks)

**Success Metric**: Copiloto MVP funcional (Epic 1 + 2) em 6 semanas

---

## Integration Points

### External Integrations

#### 1. WhatsApp Business API (Meta)

**Provider**: Meta Business API (oficial)
**Purpose**: Canal primário para mecânicos interagirem com Copiloto e Avaliação

**Integration Details**:
- **Webhook**: `POST /api/v1/whatsapp/webhook` recebe mensagens
- **Send API**: `POST https://graph.facebook.com/v18.0/{phone_number_id}/messages`
- **Authentication**: Bearer token (gerado no Meta Business Manager)
- **Rate Limits**: 1000 mensagens/dia (tier inicial), 80 requests/segundo

**Message Flow**:
```
Mecânico → WhatsApp → Meta API → Webhook (CarGuroo) → Process → Send Response → Meta API → WhatsApp → Mecânico
```

**Challenges**:
- Rate limits podem ser atingidos em horários de pico
- Templates de mensagem precisam pré-aprovação (demora 24-48h)

**Mitigations**:
- Usar queue (Celery) para enviar mensagens respeitando rate limit
- Criar templates genéricos durante setup

---

#### 2. OpenAI APIs

**APIs Utilizadas**:
1. **GPT-4 (Chat Completions)**: Copiloto responses, question generation, auto-grading
2. **text-embedding-ada-002**: Embedding generation para RAG
3. **Whisper**: Speech-to-text para áudio

**Rate Limits** (Tier 1):
- GPT-4: 10K tokens/min, 500 requests/day
- Embeddings: 1M tokens/min
- Whisper: 50 requests/min

**Cost Monitoring**:
- Track tokens per request
- Alertas se custo diário > $100

---

#### 3. DMS (Dealer Management System)

**Purpose**: SSO (authentication) + OS lookup

**Integration Type**: SAML 2.0 SSO

**Data Flow**:
- **SSO**: DMS (IdP) → SAML Assertion → CarGuroo (SP)
- **OS Lookup** (optional): REST API call `GET /api/os/{os_number}` para validar OS

**Challenges**:
- DMS pode não ter API pública → usar apenas SSO no MVP
- Documentação pode ser escassa

---

### Internal Service Communication

**Pattern**: Modular Monolith → function calls diretos (não HTTP)

**Example**:
```python
# Copiloto calling RAG
from app.rag.search import semantic_search

chunks = await semantic_search(query="como trocar pastilha de freio", top_k=5)
```

**No Service Mesh** (não microservices, então não precisa de Envoy/Istio)

---

## Observability & Operations

### Logging Strategy

**Format**: Structured JSON logs

**Fields**:
```json
{
  "timestamp": "2025-10-10T14:23:45.123Z",
  "level": "INFO",
  "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "service": "copiloto",
  "endpoint": "/api/v1/copiloto/message",
  "user_id": "uuid",
  "message": "Generated response for query",
  "context": {
    "query_text": "como trocar pastilha",
    "latency_ms": 1234,
    "llm_tokens": 1500
  }
}
```

**Library**: `structlog` (Python)

**Aggregation**: Elasticsearch + Kibana (ou Loki + Grafana)

**Retention**: 90 dias (hot) → 1 ano (cold)

---

### Metrics

**Categories**:

1. **Business Metrics**:
   - `carguroo_copiloto_queries_total` (counter)
   - `carguroo_active_users_weekly` (gauge)
   - `carguroo_assessment_completion_rate` (gauge)
   - `carguroo_feedback_positive_rate` (gauge)

2. **Technical Metrics**:
   - `http_request_duration_seconds` (histogram)
   - `http_requests_total` (counter)
   - `llm_api_calls_total` (counter)
   - `rag_search_latency_seconds` (histogram)
   - `celery_task_duration_seconds` (histogram)

**Exposition**: Prometheus scrape endpoint `/metrics`

**Visualization**: Grafana dashboards (pré-configurados)

---

### Alerting Rules

**Critical Alerts** (PagerDuty/Slack):
1. Error rate >5% por 5 minutos
2. Latência p95 >10s por 5 minutos
3. Database connection pool exhausted
4. LLM API quota exceeded

**Warning Alerts** (Slack only):
1. LLM cost >$100/dia
2. Disk usage >80%
3. Assessment completion rate <70% a 3 dias do deadline

**Alertmanager Configuration**:
```yaml
route:
  group_by: ['alertname']
  receiver: 'slack-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#carguroo-alerts'
        api_url: '${SLACK_WEBHOOK_URL}'
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '${PAGERDUTY_KEY}'
```

---

### Backup & Disaster Recovery

**PostgreSQL**:
- **Automated Backups**: RDS automated backups (daily, retention 7 days)
- **Manual Snapshots**: Antes de cada deploy para prod
- **Point-in-Time Recovery**: Até 5 minutos (RDS feature)

**Qdrant** (Vector DB):
- **Snapshot**: Backup via API `POST /collections/{name}/snapshots`
- **Frequency**: Semanal (domingo 2am)
- **Storage**: S3

**Redis**:
- **Persistence**: RDB snapshots (daily)
- **Acceptable Data Loss**: Até 24h (apenas sessions, não critical)

**RTO/RPO**:
- **RTO** (Recovery Time Objective): 4 horas
- **RPO** (Recovery Point Objective): 24 horas

---

## Next Steps & Open Questions

### Open Architecture Questions

**Q1**: Vector DB final choice - Qdrant vs. pgvector?
- **Current Decision**: Qdrant (ADR-003)
- **Re-evaluate if**: Performance não atender requisitos no POC técnico
- **Alternative**: pgvector (PostgreSQL extension) se simplicidade > performance

**Q2**: Deploy cloud ou on-premise?
- **Current Decision**: AWS como primário, portabilidade para on-premise (ADR-006)
- **Pending**: Confirmação com InfoSec da montadora (Sprint 0)
- **Impact**: Se on-premise, não usar RDS/ElastiCache (self-hosted PostgreSQL/Redis)

**Q3**: Observability stack - self-hosted vs. managed?
- **Current Decision**: Prometheus + Grafana self-hosted (ADR-010)
- **Re-evaluate if**: Manutenção ficar muito pesada
- **Alternative**: Datadog/New Relic após MVP validado

**Q4**: OCR provider - Azure Document Intelligence vs. Tesseract?
- **Pending**: Teste com amostra de 50 páginas de manuais escaneados
- **Decision criteria**: Acurácia >95% vs. custo
- **Fallback**: Tesseract (free) se Azure muito caro

---

### Immediate Next Actions

1. **POC Técnico de RAG** (Priority: CRITICAL, Timeline: Semana 1-2)
   - Ingerir 1 manual técnico (~200 páginas)
   - Testar 3 estratégias de chunking
   - Medir acurácia de busca semântica
   - Validar latência end-to-end
   - **Output**: Relatório de POC com decisões de chunking/embedding

2. **Confirmar Dependências Externas** (Priority: BLOCKER, Timeline: Semana 1)
   - ✅ Acesso a manuais técnicos da montadora
   - ✅ Aprovação de deployment (cloud ou on-premise)
   - ✅ Disponibilidade de APIs do DMS para SSO
   - ✅ Painel de especialistas para validação de rubricas

3. **Setup de Infra Base** (Priority: HIGH, Timeline: Semana 2-3)
   - Provisionar PostgreSQL (RDS ou self-hosted)
   - Provisionar Redis (ElastiCache ou Docker)
   - Provisionar Qdrant (EC2 + Docker)
   - Setup de S3 para storage de PDFs
   - Configurar ALB + TLS certificate

4. **Criar Database Schema** (Priority: HIGH, Timeline: Semana 3)
   - Implementar schemas: `auth`, `rag`, `copiloto`, `avaliacao`
   - Criar migrations (Alembic)
   - Seed inicial (admin user, test data)

5. **Implementar Skeleton Arquitetural** (Priority: HIGH, Timeline: Semana 3-4)
   - Backend: FastAPI app com módulos vazios
   - Autenticação básica (JWT, não SSO ainda)
   - Logging estruturado (structlog)
   - Health checks (`/health`)

6. **Gerar Tech Specs por Epic** (Priority: HIGH, Timeline: Semana 4)
   - Epic 1: RAG Infrastructure (detalhamento técnico)
   - Epic 2: Copiloto MVP
   - Epic 3: Avaliação
   - **Output**: Tech specs detalhadas para cada epic (input para desenvolvimento)

---

### Success Criteria for Architecture Phase

- [x] Solution architecture document completo
- [ ] POC técnico de RAG executado com sucesso
- [ ] Dependências externas confirmadas (BLOCKER resolved)
- [ ] Database schema design completo
- [ ] Tech specs geradas por epic (próximo documento)
- [ ] Infraestrutura base provisionada (dev environment)

---

## Document Status

- [x] High-level architecture defined
- [x] Component breakdown detailed
- [x] Data architecture designed
- [x] Security architecture specified
- [x] Deployment architecture planned
- [x] Technology stack finalized
- [x] Critical challenges identified with mitigations
- [ ] POC técnico executado (NEXT STEP)
- [ ] Tech specs por epic geradas (NEXT STEP)
- [ ] Ready for development (pending POC + specs)

---

**Última Atualização**: 2025-10-10
**Próxima Revisão**: Após POC técnico de RAG (Semana 2)
**Status**: Draft v1.0 - Ready for Review

---

_This architecture balances MVP speed with future scalability, leveraging modular monolith for simplicity while maintaining clear boundaries for future microservices extraction if needed._
