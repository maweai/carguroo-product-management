# CarGuroo - Epic Breakdown & User Stories

**Project:** CarGuroo MVP
**Date:** 2025-10-10
**Author:** Allan
**PRD Reference:** PRD-CarGuroo-2025-10-10.md

---

## Epic Overview

Este documento detalha o breakdown completo dos **5 epics principais** do CarGuroo MVP em **user stories** individuais com critérios de aceitação e notas técnicas.

**Total Estimado**: 41 user stories distribuídas em 5 epics
**Timeline**: 2-3 meses (desenvolvimento acelerado com BMAD + Claude Code)

---

## Epic 1: Infraestrutura RAG e Base de Conhecimento (Foundation)

**Objetivo**: Estabelecer fundação técnica compartilhada entre Copiloto e Avaliação para ingestão, processamento e busca semântica em base de conhecimento.

**Valor de Negócio**: Infraestrutura crítica sem a qual nenhum produto core funciona.

**Prioridade**: CRÍTICA | **Fase**: Mês 1 | **Total Stories**: 9

---

### US-RAG-01: Upload de Manuais Técnicos (PDF)

**Como** administrador da plataforma
**Quero** fazer upload de manuais técnicos em formato PDF via interface web
**Para que** eu possa alimentar a base de conhecimento do sistema

**Pré-requisitos**: Nenhum (primeira story)

**Critérios de Aceitação**:
1. Interface web permite upload de arquivos PDF (tamanho máximo 50MB)
2. Sistema valida formato do arquivo (apenas PDF aceito)
3. Upload mostra barra de progresso com % concluído
4. Após upload bem-sucedido, documento aparece em lista de "Pendentes de Processamento"
5. Sistema armazena PDF em storage seguro (S3 ou equivalente)
6. Metadados básicos são coletados: nome do arquivo, tamanho, data de upload, uploader

**Notas Técnicas**:
- Storage: AWS S3 ou Google Cloud Storage
- Backend: endpoint POST /api/v1/documents/upload
- Frontend: drag-and-drop interface (React Dropzone ou similar)

---

### US-RAG-02: Processamento e Chunking de Documentos PDF

**Como** sistema
**Quero** processar PDFs automaticamente após upload
**Para que** documentos sejam divididos em chunks otimizados para busca semântica

**Pré-requisitos**: US-RAG-01 (upload funcional)

**Critérios de Aceitação**:
1. Sistema detecta novo PDF em storage e inicia processamento automático
2. Extração de texto funciona para PDFs com texto nativo e OCR para PDFs escaneados
3. Documento é dividido em chunks de ~500-1000 tokens com overlap de 100 tokens
4. Metadados são preservados (nome do documento, número de página origem)
5. Chunks mal formados ou vazios são descartados
6. Status de processamento é atualizado em dashboard (Processando → Concluído/Erro)
7. Logs de erro detalham problemas (página específica, tipo de erro)

**Notas Técnicas**:
- Biblioteca OCR: Tesseract ou Azure Document Intelligence
- Chunking strategy: LangChain RecursiveCharacterTextSplitter
- Processamento assíncrono: Celery + RabbitMQ
- Estimativa: ~2-5 min para manual de 500 páginas

---

### US-RAG-03: Geração de Embeddings

**Como** sistema
**Quero** gerar embeddings vetoriais para cada chunk de texto
**Para que** chunks sejam indexados e busca semântica seja possível

**Pré-requisitos**: US-RAG-02 (chunking completo)

**Critérios de Aceitação**:
1. Sistema gera embedding para cada chunk via API de embedding (OpenAI ou similar)
2. Embeddings são vetores de dimensão fixa (ex: 1536 para text-embedding-ada-002)
3. Rate limiting está implementado para evitar exceder quota da API
4. Retry logic com exponential backoff em caso de falha temporária
5. Embeddings são armazenados junto com chunk_id e metadados
6. Custo de embedding é rastreado (tokens utilizados × preço)

**Notas Técnicas**:
- Embedding model: OpenAI text-embedding-ada-002 ou Anthropic equivalente
- Batch processing: até 100 chunks por request para eficiência
- Custo estimado: ~$0.40 por 1M tokens (~R$2 por manual de 500 páginas)

---

### US-RAG-04: Indexação em Vector Database

**Como** sistema
**Quero** indexar embeddings em vector database
**Para que** busca semântica de alta performance seja possível

**Pré-requisitos**: US-RAG-03 (embeddings gerados)

**Critérios de Aceitação**:
1. Sistema insere embeddings + metadados no vector database
2. Índice é criado automaticamente com configuração otimizada (HNSW ou IVF)
3. Bulk insert é usado para performance (batches de 1000 vectors)
4. Metadados incluem: chunk_text, document_name, page_number, chunk_id
5. Indexação é idempotente (re-processar documento não duplica chunks)
6. Dashboard mostra total de vectors indexados e status do índice

**Notas Técnicas**:
- Vector DB: Pinecone, Weaviate ou Qdrant (decisão arquitetural pendente)
- Índice: HNSW para latência <100ms em queries
- Namespace por tenant (preparação para futuro multi-tenancy)

---

### US-RAG-05: API de Busca Semântica

**Como** desenvolvedor
**Quero** uma API de busca semântica
**Para que** Copiloto e Avaliação possam consultar base de conhecimento

**Pré-requisitos**: US-RAG-04 (vector DB populado)

**Critérios de Aceitação**:
1. Endpoint GET /api/v1/search aceita query em linguagem natural
2. Query é convertida em embedding usando mesmo modelo da indexação
3. Vector database retorna top-K chunks mais similares (K=5 padrão, configurável)
4. Resultados incluem: chunk_text, similarity_score, metadados (documento, página)
5. Latência p95 < 500ms para queries típicas
6. API retorna resultados ordenados por similarity score (descendente)
7. Filtros opcionais por metadados (ex: apenas documento X, apenas páginas Y-Z)

**Notas Técnicas**:
- Similarity metric: Cosine similarity
- Caching: Redis para queries frequentes (TTL 1 hora)
- Autenticação: Bearer token (JWT)

---

### US-RAG-06: Monitoramento de Pipeline RAG

**Como** administrador
**Quero** dashboard de monitoramento do pipeline RAG
**Para que** eu possa identificar problemas e otimizar performance

**Pré-requisitos**: US-RAG-01 a US-RAG-05 (pipeline completo)

**Critérios de Aceitação**:
1. Dashboard mostra métricas de pipeline:
   - Total de documentos processados/pendentes/com erro
   - Total de chunks indexados
   - Taxa de processamento (docs/hora)
   - Latência média de busca (p50/p95/p99)
2. Gráficos de tendência (últimos 7 dias) para métricas principais
3. Alertas visuais para erros críticos (processamento falhando >10 min)
4. Logs de erros recentes (últimas 50 entradas) com filtro por tipo
5. Ação manual de "Reprocessar Documento" para documentos com erro

**Notas Técnicas**:
- Frontend: React + Chart.js ou Recharts
- Backend: agregação de métricas via PostgreSQL
- Refresh automático a cada 30s

---

### US-RAG-07: Gestão de Documentos Indexados

**Como** administrador
**Quero** gerenciar documentos na base de conhecimento
**Para que** eu possa atualizar, remover ou re-processar manuais técnicos

**Pré-requisitos**: US-RAG-06 (dashboard básico)

**Critérios de Aceitação**:
1. Interface lista todos os documentos indexados com metadados:
   - Nome, data de upload, status, total de chunks, uploader
2. Ações disponíveis por documento:
   - Visualizar prévia (primeiras 3 páginas)
   - Download do PDF original
   - Reprocessar (deleta chunks antigos e reprocessa)
   - Deletar permanentemente (PDF + todos os chunks)
3. Filtro e busca por nome de documento
4. Paginação (50 docs por página)
5. Ação de delete requer confirmação explícita
6. Após delete, chunks são removidos do vector DB em até 5 minutos

**Notas Técnicas**:
- Soft delete vs. hard delete: considerar auditoria
- Background job para limpeza de vector DB após delete

---

### US-RAG-08: Otimização de Custos de Embedding

**Como** sistema
**Quero** otimizar custos de chamadas de API de embedding
**Para que** processamento de documentos seja economicamente viável

**Pré-requisitos**: US-RAG-03 (embeddings funcionais)

**Critérios de Aceitação**:
1. Sistema detecta chunks duplicados (hash MD5) antes de gerar embedding
2. Embeddings de chunks duplicados são reutilizados (não re-processados)
3. Caching de embeddings para chunks frequentes
4. Batch processing reduz número de API calls em 80%+
5. Dashboard mostra custo acumulado de embeddings (R$ gastos vs. R$ economizados via cache)
6. Alertas se custo mensal exceder threshold configurável (ex: R$ 500/mês)

**Notas Técnicas**:
- Cache: Redis com TTL de 30 dias
- Key format: hash(chunk_text) → embedding_vector
- Monitoramento de custo: tracking em database + dashboard

---

### US-RAG-09: Testes de Acurácia de Busca Semântica

**Como** desenvolvedor
**Quero** suite de testes automatizados de acurácia
**Para que** busca semântica seja validada continuamente

**Pré-requisitos**: US-RAG-05 (API de busca)

**Critérios de Aceitação**:
1. Suite de 20+ query-resultado esperado pairs (gold standard)
2. Teste automatizado executa queries e compara top-5 resultados
3. Métrica de acurácia: % de queries onde resultado esperado está no top-5
4. Threshold de aceitação: acurácia > 80%
5. Testes rodados em CI/CD antes de deploy
6. Relatório de acurácia por categoria de query (diagnóstico, procedimento, etc.)

**Notas Técnicas**:
- Framework: pytest
- Gold standard: curado manualmente com mecânicos especialistas
- Run em staging antes de prod deployment

---

## Epic 2: Copiloto do Mecânico - MVP (Primary Product)

**Objetivo**: Interface conversacional funcional para mecânicos consultarem base de conhecimento e receberem diagnósticos assistidos.

**Valor de Negócio**: Produto core #1 que reduz tempo de diagnóstico e dependência de help desk.

**Prioridade**: CRÍTICA | **Fase**: Mês 2 | **Total Stories**: 11

---

### US-COP-01: Autenticação de Mecânico via WhatsApp

**Como** mecânico
**Quero** iniciar conversa com Copiloto via WhatsApp
**Para que** eu possa consultar informações técnicas durante trabalho

**Pré-requisitos**: Epic 1 completo (RAG funcional)

**Critérios de Aceitação**:
1. Mecânico envia primeira mensagem para número WhatsApp do Copiloto
2. Sistema solicita autenticação: "Olá! Por favor, envie seu CPF para autenticação."
3. Após validação de CPF, sistema confirma: "Bem-vindo João! Como posso ajudar?"
4. Sessão é criada com timeout de 24 horas de inatividade
5. Se mecânico não encontrado, sistema orienta: "CPF não encontrado. Contate seu gestor."

**Notas Técnicas**:
- WhatsApp Business API via Twilio ou Meta oficial
- Autenticação: lookup de CPF em database de usuários
- Sessão: armazenada em Redis com TTL 24h

---

### US-COP-02: Consulta Simples de Informação

**Como** mecânico
**Quero** fazer perguntas técnicas em linguagem natural
**Para que** eu receba informações relevantes rapidamente

**Pré-requisitos**: US-COP-01 (autenticação)

**Critérios de Aceitação**:
1. Mecânico envia mensagem: "Como trocar pastilha de freio do modelo XYZ?"
2. Sistema realiza busca semântica no RAG (top-5 chunks)
3. LLM gera resposta baseada nos chunks recuperados
4. Resposta inclui citação de fonte: "Fonte: Manual Técnico XYZ-2023, pág. 142"
5. Latência total < 5s (p95)
6. Se informação não encontrada, sistema responde: "Não encontrei essa informação específica. Posso te ajudar com algo relacionado?"

**Notas Técnicas**:
- LLM: GPT-4 ou Claude
- Prompt engineering: incluir chunks + instrução de resposta concisa com fontes
- Fallback: se similarity score < 0.6, admitir desconhecimento

---

### US-COP-03: Input de Áudio (Speech-to-Text)

**Como** mecânico
**Quero** enviar mensagens de áudio em vez de texto
**Para que** eu possa consultar Copiloto hands-free durante trabalho

**Pré-requisitos**: US-COP-02 (consulta básica funcional)

**Critérios de Aceitação**:
1. Mecânico envia áudio via WhatsApp (até 2 minutos)
2. Sistema transcreve áudio para texto usando API de speech-to-text
3. Transcrição é processada como query normal (mesma lógica de US-COP-02)
4. Resposta é enviada em texto formatado (não áudio no MVP)
5. Indicador "processando áudio..." é mostrado durante transcrição
6. Acurácia de transcrição > 90% para português brasileiro

**Notas Técnicas**:
- Speech-to-text: OpenAI Whisper API ou Google Cloud Speech
- Custo: ~$0.006/minuto ($0.36/hora de áudio)
- Timeout: se transcrição > 10s, avisar mecânico

---

### US-COP-04: Associação com Ordem de Serviço (OS)

**Como** mecânico
**Quero** vincular conversa a uma OS específica
**Para que** histórico de diagnóstico fique registrado no contexto correto

**Pré-requisitos**: US-COP-02 (consulta funcional)

**Critérios de Aceitação**:
1. Mecânico pode enviar: "OS 12345" ou "Trabalhando na OS 12345"
2. Sistema extrai número da OS via regex/NLP
3. Conversaé vinculada à OS e todas as mensagens subsequentes são registradas
4. Sistema confirma: "Entendido, vou registrar essa conversa na OS #12345."
5. Se OS não encontrada no DMS, sistema avisa: "OS #12345 não encontrada. Verifique o número."
6. Mecânico pode mudar de OS a qualquer momento enviando novo número

**Notas Técnicas**:
- Regex: r"OS\s*#?\s*(\d{4,8})"
- Validação: lookup em database de OS (se integração com DMS disponível)
- Contexto de sessão: armazenar os_number em Redis

---

### US-COP-05: Diagnóstico Assistido com Fluxo Guiado

**Como** mecânico
**Quero** receber perguntas sequenciais para refinar diagnóstico
**Para que** eu chegue a causa raiz do problema de forma estruturada

**Pré-requisitos**: US-COP-02 (consulta funcional)

**Critérios de Aceitação**:
1. Mecânico descreve sintoma: "Carro fazendo barulho no motor"
2. Sistema identifica que é diagnóstico (não pergunta simples de procedimento)
3. Sistema faz perguntas de refinamento:
   - "O barulho acontece em marcha lenta ou em movimento?"
   - "É um barulho metálico ou mais como um assobio?"
4. Baseado em respostas, sistema sugere diagnóstico com probabilidades:
   - "Correia dentada com folga (70% prob)"
   - "Rolamento do alternador (20% prob)"
5. Sistema sugere próximos passos de verificação
6. Fluxo tem máximo 5 perguntas (evitar cansaço do usuário)

**Notas Técnicas**:
- Lógica de diálogo: state machine ou LLM conversacional
- Few-shot prompting para LLM seguir formato de perguntas-resposta
- Probabilidades: heurística baseada em chunks recuperados + LLM reasoning

---

### US-COP-06: Histórico de Interações por OS

**Como** mecânico ou gestor
**Quero** visualizar histórico completo de interações do Copiloto por OS
**Para que** eu possa revisar diagnóstico e decisões tomadas

**Pré-requisitos**: US-COP-04 (associação com OS)

**Critérios de Aceitação**:
1. Interface web mostra lista de OS com interações do Copiloto
2. Ao clicar em OS, vejo transcrição completa da conversa:
   - Timestamp de cada mensagem
   - Autor (mecânico ou Copiloto)
   - Fontes citadas pelo Copiloto
3. Busca por número de OS ou nome de mecânico
4. Exportação de transcrição em PDF
5. Histórico preservado por 2 anos (compliance LGPD)

**Notas Técnicas**:
- Storage: PostgreSQL para mensagens estruturadas
- Indexação: por os_number e mechanic_id
- Frontend: timeline view (estilo chat)

---

### US-COP-07: Citação de Fontes com Links Diretos

**Como** mecânico
**Quero** acessar diretamente a página do manual citada
**Para que** eu possa validar informação e ver contexto completo

**Pré-requisitos**: US-COP-02 (consulta com citações)

**Critérios de Aceitação**:
1. Resposta do Copiloto inclui link clicável: "[Ver página 142 do Manual XYZ-2023](#)"
2. Link abre PDF diretamente na página citada (deep link)
3. Se PDF não tiver permissão de view, sistema exibe screenshot da página
4. Citações múltiplas são numeradas: "[1] Manual XYZ, pág. 142 [2] Boletim BT-2024-03"
5. Mecânico pode clicar em qualquer citação para ver fonte

**Notas Técnicas**:
- Deep linking: PDF.js com parâmetro #page=142
- Permissions: verificar RBAC antes de servir PDF
- Fallback: screenshot pré-renderizado da página (gerado durante ingestão)

---

### US-COP-08: Feedback de Utilidade de Resposta

**Como** mecânico
**Quero** informar se resposta foi útil
**Para que** sistema aprenda e melhore ao longo do tempo

**Pré-requisitos**: US-COP-02 (consulta funcional)

**Critérios de Aceitação**:
1. Após cada resposta, Copiloto pergunta: "Esta resposta foi útil? 👍 👎"
2. Mecânico pode clicar em emoji ou responder "sim"/"não"
3. Feedback é registrado com: query, resposta, chunks usados, utilidade (bool)
4. Se feedback negativo, sistema pergunta opcional: "O que faltou?"
5. Dashboard de analytics mostra taxa de feedback positivo (meta: >75%)

**Notas Técnicas**:
- Storage: feedback table com foreign key para interaction_id
- Analytics: agregação semanal de taxa de positividade
- Uso futuro: fine-tuning de LLM ou re-ranking de chunks

---

### US-COP-09: Limitação de Taxa de Uso (Rate Limiting)

**Como** administrador
**Quero** limitar taxa de uso do Copiloto por mecânico
**Para que** custos de LLM sejam controlados

**Pré-requisitos**: US-COP-02 (consulta funcional)

**Critérios de Aceitação**:
1. Cada mecânico tem limite de 50 queries/dia (configurável)
2. Após atingir limite, sistema avisa: "Você atingiu o limite diário de consultas. Tente novamente amanhã."
3. Exceção para mecânicos premium (configurável por admin)
4. Dashboard mostra consumo por mecânico (queries/dia, custo estimado)
5. Alertas se consumo de LLM exceder budget mensal

**Notas Técnicas**:
- Rate limiting: Redis com TTL de 24h
- Key: mechanic_id → count
- Custo estimado: $0.01/query × 50 queries/dia/mecânico × 450 mecânicos = $225/dia = $6750/mês

---

### US-COP-10: Modo Offline / Fallback para Indisponibilidade

**Como** mecânico
**Quero** receber aviso claro quando Copiloto estiver indisponível
**Para que** eu não fique esperando resposta indefinidamente

**Pré-requisitos**: US-COP-02 (consulta funcional)

**Critérios de Aceitação**:
1. Se backend está down, sistema responde em <10s: "Estou temporariamente indisponível. Tente novamente em alguns minutos."
2. Se LLM API está down, sistema tenta fallback (ex: busca direta sem LLM generation)
3. Se fallback também falha, orientar mecânico: "Sistema fora do ar. Contate help desk: (11) 9999-9999"
4. Status page pública mostra saúde do sistema (UP/DOWN/DEGRADED)
5. Alertas automáticos para equipe de ops em caso de downtime

**Notas Técnicas**:
- Health checks: endpoint /health com verificação de dependencies
- Circuit breaker: se LLM API falha >3x em 1min, ativar fallback mode
- Status page: hosted externally (Statuspage.io ou self-hosted)

---

### US-COP-11: Analytics de Uso do Copiloto

**Como** gestor
**Quero** visualizar analytics de uso do Copiloto
**Para que** eu possa avaliar adoção e identificar problemas

**Pré-requisitos**: US-COP-02 (consulta funcional)

**Critérios de Aceitação**:
1. Dashboard mostra métricas chave:
   - WAU (Weekly Active Users)
   - Total de queries por semana
   - Média de queries por mecânico ativo
   - Taxa de feedback positivo
   - Latência média (p50/p95)
2. Segmentação por concessionária
3. Gráficos de tendência (últimas 8 semanas)
4. Top 10 queries mais frequentes
5. Exportação de relatório em PDF

**Notas Técnicas**:
- Data warehouse: BigQuery ou PostgreSQL com agregações pré-computadas
- Refresh: diário (não tempo real para MVP)
- Visualização: Chart.js ou ferramenta BI (Metabase, Superset)

---

## Epic 3: Sistema de Avaliação - Criação e Execução (Secondary Product - Part 1)

**Objetivo**: Permitir gestores criarem ciclos de avaliação com questões geradas por IA, mecânicos responderem via chat, e correção automatizada.

**Valor de Negócio**: Produto core #2 que fornece visibilidade de competências em escala.

**Prioridade**: ALTA | **Fase**: Mês 2 | **Total Stories**: 9

---

### US-AVA-01: Criação de Ciclo de Avaliação (Wizard)

**Como** gestor
**Quero** criar ciclo de avaliação via wizard guiado
**Para que** eu possa avaliar mecânicos de forma estruturada

**Pré-requisitos**: Epic 1 completo

**Critérios de Aceitação**:
1. Wizard com 4 passos:
   - Passo 1: Selecionar fase (Fase 1/2/3)
   - Passo 2: Selecionar público-alvo (concessionárias, mecânicos específicos)
   - Passo 3: Definir período (data início/fim)
   - Passo 4: Configurar escopo de competências (áreas a avaliar)
2. Validações em cada passo (ex: data fim > data início)
3. Preview de configuração antes de finalizar
4. Ao finalizar, ciclo é criado com status "Rascunho"
5. Gestor pode editar rascunho antes de publicar

**Notas Técnicas**:
- Frontend: multi-step form com validação
- Backend: POST /api/v1/assessment-cycles
- Status: draft → published → in_progress → completed

---

### US-AVA-02: Geração Automática de Questões por IA

**Como** gestor
**Quero** que IA gere questões situacionais automaticamente
**Para que** eu não precise criar manualmente cada questão

**Pré-requisitos**: US-AVA-01 (ciclo criado)

**Critérios de Aceitação**:
1. Após configurar ciclo, gestor clica "Gerar Questões"
2. IA gera 30 questões situacionais baseadas em:
   - Área técnica selecionada
   - Nível alvo (Iniciante/Adequado/Experiente)
   - Manuais técnicos relevantes (via RAG)
3. Cada questão inclui:
   - Enunciado situacional (cenário)
   - Rubrica de correção (4 níveis: Inadequado/Parcial/Adequado/Excelente)
   - Metadata (área, nível cognitivo Bloom, dificuldade estimada)
4. Tempo de geração < 2 minutos para 30 questões
5. Preview de 5 questões aleatórias para gestor validar

**Notas Técnicas**:
- LLM: GPT-4 com few-shot examples de questões modelo
- Prompt engineering: incluir contexto de área técnica + exemplos de rubricas
- Validação: gestor pode regenerar questões específicas se não gostar

---

### US-AVA-03: Revisão e Aprovação de Questões

**Como** gestor
**Quero** revisar questões geradas antes de publicar ciclo
**Para que** eu garanta qualidade e relevância

**Pré-requisitos**: US-AVA-02 (questões geradas)

**Critérios de Aceitação**:
1. Interface lista todas as 30 questões geradas
2. Gestor pode:
   - Editar enunciado de qualquer questão
   - Editar rubrica
   - Deletar questão (gerar nova no lugar)
   - Aprovar questão (marca como revisada)
3. Indicador visual de progresso: "25/30 questões revisadas"
4. Botão "Publicar Ciclo" só ativa após todas revisadas
5. Ao publicar, mecânicos recebem notificação via WhatsApp

**Notas Técnicas**:
- Interface: list view com expand/collapse por questão
- Versionamento: salvar histórico de edições para auditoria
- Notificação: batch send via WhatsApp API (rate limit aware)

---

### US-AVA-04: Notificação de Novo Ciclo para Mecânicos

**Como** mecânico
**Quero** receber notificação de novo ciclo de avaliação
**Para que** eu saiba que preciso completar avaliação

**Pré-requisitos**: US-AVA-03 (ciclo publicado)

**Critérios de Aceitação**:
1. Ao publicar ciclo, todos os mecânicos do público-alvo recebem mensagem WhatsApp:
   - "Olá João! Novo ciclo de avaliação Q2-2025 está aberto."
   - "Prazo: até 30/Out. Você tem 30 questões situacionais."
   - "Responda 'iniciar avaliação' para começar."
2. Notificação não é enviada se mecânico já iniciou avaliação
3. Reminder automático 3 dias antes do deadline para quem não começou
4. Gestor vê dashboard de notificações enviadas/lidas

**Notas Técnicas**:
- WhatsApp API: template message (pré-aprovado pelo Meta)
- Scheduling: Cron job para reminders
- Tracking: marca timestamp de notificação enviada

---

### US-AVA-05: Execução de Avaliação via Chat (Texto)

**Como** mecânico
**Quero** responder questões de avaliação via chat de texto
**Para que** eu complete avaliação de forma conveniente

**Pré-requisitos**: US-AVA-04 (notificação recebida)

**Critérios de Aceitação**:
1. Mecânico responde "iniciar avaliação" → sistema apresenta instruções
2. Questões são enviadas sequencialmente (uma por vez)
3. Mecânico responde em texto livre (linguagem natural)
4. Sistema salva resposta e envia próxima questão
5. Progresso é exibido: "Questão 5 de 30"
6. Mecânico pode pausar a qualquer momento ("Vou continuar depois")
7. Estado é salvo e mecânico pode retomar de onde parou

**Notas Técnicas**:
- Estado de sessão: armazenado em Redis (current_question_index, responses[])
- Timeout: sessão expira após 7 dias de inatividade (aviso antes)
- Responses storage: PostgreSQL com foreign key para assessment_cycle_id

---

### US-AVA-06: Suporte a Respostas em Áudio

**Como** mecânico
**Quero** responder questões de avaliação em áudio
**Para que** eu não precise digitar respostas longas

**Pré-requisitos**: US-AVA-05 (avaliação via texto)

**Critérios de Aceitação**:
1. Mecânico pode enviar resposta em áudio (até 3 minutos)
2. Sistema transcreve áudio e armazena transcrição como resposta
3. Mecânico vê confirmação: "Sua resposta em áudio foi recebida e transcrita."
4. Opção de visualizar transcrição e corrigir se necessário
5. Áudio original é descartado após transcrição (LGPD - não armazenar voz)

**Notas Técnicas**:
- Speech-to-text: mesma API de US-COP-03
- Privacy: apenas transcrição é armazenada, áudio deletado
- Custo: ~$0.006/min × 3min/questão × 30 questões × 450 mecânicos = $243

---

### US-AVA-07: Correção Automatizada via IA

**Como** sistema
**Quero** corrigir respostas automaticamente usando IA
**Para que** mecânicos recebam feedback rapidamente

**Pré-requisitos**: US-AVA-05 (respostas coletadas)

**Critérios de Aceitação**:
1. Após mecânico completar avaliação, sistema inicia correção automática
2. Para cada resposta, LLM avalia contra rubrica de 4 níveis
3. IA gera score (1-4) e justificativa breve
4. Casos de baixa confiança (confidence < 70%) são sinalizados para revisão manual
5. Tempo de correção < 5 minutos para avaliação completa de 30 questões
6. Resultados são armazenados com score + justificativa + confidence

**Notas Técnicas**:
- LLM: GPT-4 com prompt incluindo rubrica + resposta
- Output parsing: score (int 1-4) + rationale (str)
- Queue: Celery para processar correções em background

---

### US-AVA-08: Revisão Manual de Respostas Ambíguas

**Como** especialista revisor
**Quero** revisar respostas sinalizadas como ambíguas
**Para que** correção seja precisa e justa

**Pré-requisitos**: US-AVA-07 (correção automática)

**Critérios de Aceitação**:
1. Interface lista respostas que precisam revisão (confidence < 70%)
2. Revisor vê:
   - Questão original + rubrica
   - Resposta do mecânico
   - Score sugerido pela IA + justificativa
3. Revisor pode:
   - Concordar com IA (aceitar score)
   - Modificar score e adicionar justificativa
4. Após revisar todas pendentes, ciclo pode ser finalizado
5. Dashboard mostra % de respostas que precisaram revisão manual (meta: <20%)

**Notas Técnicas**:
- RBAC: apenas usuários com role "specialist" acessam interface
- Tracking: concordância IA vs. humano para melhoria contínua
- Prazo: revisão deve ocorrer em até 48h após avaliação completada

---

### US-AVA-09: Classificação de Mecânico por Níveis

**Como** sistema
**Quero** classificar mecânico em níveis baseado em performance
**Para que** gestores tenham visibilidade de competências

**Pré-requisitos**: US-AVA-07 ou US-AVA-08 (correção completa)

**Critérios de Aceitação**:
1. Sistema agrega scores de todas as questões
2. Classificação segue thresholds:
   - Fase 2: 0-69% = Iniciante, 70-84% = Adequado, 85-100% = Experiente
   - Fase 3: 0-59% = Sem Qualificação, 60-84% = Qualificado, 85-100% = Especialista
3. Resultado é armazenado com: mechanic_id, cycle_id, classification, score_percentage
4. Dashboard é atualizado automaticamente com nova classificação
5. Mecânico recebe notificação com resultado (após 48h da conclusão)

**Notas Técnicas**:
- Agregação: média ponderada de scores (peso pode ser por área técnica)
- Versionamento: histórico de classificações preservado para tracking de evolução
- Delay de 48h: permite revisão manual de casos ambíguos antes de divulgar

---

## Epic 4: Dashboard e Visibilidade de Competências (Secondary Product - Part 2)

**Objetivo**: Dashboards para gestores com visão agregada, drill-down individual, identificação de gaps e exportação de dados.

**Valor de Negócio**: Transforma dados de avaliação em insights acionáveis para gestão.

**Prioridade**: ALTA | **Fase**: Mês 3 | **Total Stories**: 7

---

### US-DASH-01: Dashboard Agregado de Competências

**Como** gestor
**Quero** visualizar distribuição de mecânicos por nível
**Para que** eu tenha visão geral de competências da equipe

**Pré-requisitos**: Epic 3 completo (avaliações realizadas)

**Critérios de Aceitação**:
1. Dashboard mostra gráficos:
   - Pizza chart: % de mecânicos por nível (Iniciante/Adequado/Experiente)
   - Bar chart: distribuição por concessionária
   - Line chart: evolução ao longo dos últimos 4 ciclos
2. Filtros: por concessionária, por área técnica, por período
3. KPIs destacados:
   - Total de mecânicos avaliados
   - Taxa de conclusão de avaliações (% que completaram no prazo)
   - Nível médio da equipe (score médio geral)
4. Atualização automática diária (não tempo real)

**Notas Técnicas**:
- Frontend: React + Chart.js ou D3.js
- Backend: agregações SQL pré-computadas (materialized views)
- Caching: Redis com TTL de 6 horas

---

### US-DASH-02: Drill-down Individual de Competências

**Como** gestor
**Quero** ver perfil detalhado de competências de cada mecânico
**Para que** eu possa planejar desenvolvimento individual

**Pré-requisitos**: US-DASH-01 (dashboard agregado)

**Critérios de Aceitação**:
1. Gestor clica em mecânico na lista → abre perfil individual
2. Perfil mostra:
   - Classificação atual (Iniciante/Adequado/Experiente)
   - Score por área técnica (radar chart)
   - Histórico de classificações (últimos 4 ciclos)
   - Pontos fortes e áreas para melhorar
3. Comparação com média da concessionária
4. Sugestões de materiais de estudo (baseado em gaps)
5. Botão para exportar perfil em PDF

**Notas Técnicas**:
- Radar chart: biblioteca como Recharts
- Comparação: percentil em relação à equipe
- PDF generation: biblioteca como PDFKit ou ReportLab

---

### US-DASH-03: Identificação Automática de Gaps Críticos

**Como** gestor
**Quero** que sistema identifique gaps de conhecimento críticos
**Para que** eu priorize capacitações de alto impacto

**Pré-requisitos**: US-DASH-01 (dados agregados)

**Critérios de Aceitação**:
1. Dashboard destaca gaps críticos:
   - Áreas com >50% dos mecânicos abaixo de "Adequado"
   - Áreas com piora de performance vs. ciclo anterior
2. Cada gap mostra:
   - Nome da área técnica
   - % de mecânicos afetados
   - Sugestão de ação (ex: "Treinamento em Sistemas Elétricos")
3. Ranking de gaps por criticidade (mais afetados primeiro)
4. Exportação de lista de mecânicos por gap para planejar turmas de capacitação

**Notas Técnicas**:
- Regra de criticidade: >50% abaixo de adequado OU queda >10pp vs. ciclo anterior
- Algoritmo: análise de distribuição + comparação temporal
- Alertas: notificação automática para gestores quando novo gap crítico detectado

---

### US-DASH-04: Comparação Entre Concessionárias

**Como** gestor regional
**Quero** comparar performance entre concessionárias
**Para que** eu identifique best practices e outliers

**Pré-requisitos**: US-DASH-01 (dados agregados)

**Critérios de Aceitação**:
1. Dashboard mostra ranking de concessionárias por:
   - Score médio geral
   - % de mecânicos "Experientes"
   - Taxa de conclusão de avaliações no prazo
2. Gráfico de dispersão: score médio × taxa de conclusão
3. Drill-down por concessionária para ver detalhes
4. Filtros temporais (último ciclo, últimos 6 meses, último ano)
5. Exportação de ranking em Excel

**Notas Técnicas**:
- RBAC: apenas gestores regionais/nacionais acessam comparação entre concessionárias
- Anonimização opcional: ocultar nomes de concessionárias (mostrar apenas IDs)
- Benchmarking: percentil de cada concessionária vs. média nacional

---

### US-DASH-05: Exportação de Dados para Análise Externa

**Como** gestor
**Quero** exportar dados de competências em formatos estruturados
**Para que** eu possa analisar em ferramentas externas (Excel, BI)

**Pré-requisitos**: US-DASH-01 (dados disponíveis)

**Critérios de Aceitação**:
1. Botão "Exportar Dados" permite escolher formato:
   - CSV
   - Excel (XLSX)
   - JSON
2. Exportação inclui:
   - Lista de mecânicos com classificação atual
   - Scores por área técnica
   - Histórico de classificações (últimos 4 ciclos)
3. Filtros aplicados no dashboard são respeitados na exportação
4. Arquivo gerado em <30s para até 1000 mecânicos
5. Download direto ou envio por e-mail (para arquivos grandes)

**Notas Técnicas**:
- Excel generation: biblioteca openpyxl (Python) ou exceljs (Node.js)
- Streaming: para grandes volumes, usar streaming para evitar timeout
- Security: link de download expira em 24 horas

---

### US-DASH-06: Visualização de Tendências Temporais

**Como** gestor
**Quero** visualizar tendências de evolução de competências
**Para que** eu avalie eficácia de capacitações e identifique progressos

**Pré-requisitos**: US-DASH-01 (dados históricos)

**Critérios de Aceitação**:
1. Gráfico de linha mostra evolução ao longo do tempo:
   - Eixo X: ciclos de avaliação (Q1-2025, Q2-2025, etc.)
   - Eixo Y: score médio ou % por nível
2. Séries múltiplas: uma linha por área técnica
3. Destacar eventos importantes (ex: "Treinamento em Sistemas Elétricos - Ago/2025")
4. Tooltip ao passar mouse mostra detalhes do ponto
5. Zoom temporal: selecionar intervalo de ciclos para análise

**Notas Técnicas**:
- Charting library: Chart.js com plugin de zoom
- Annotations: biblioteca como chartjs-plugin-annotation
- Data points: agregações mensais ou trimestrais

---

### US-DASH-07: Alertas Proativos para Gestores

**Como** gestor
**Quero** receber alertas automáticos sobre eventos importantes
**Para que** eu possa agir rapidamente sem monitorar dashboard constantemente

**Pré-requisitos**: US-DASH-01 e US-DASH-03 (dashboard funcional)

**Critérios de Aceitação**:
1. Alertas via e-mail/WhatsApp para eventos:
   - Novo gap crítico detectado
   - Taxa de conclusão de avaliação <70% a 3 dias do deadline
   - Mecânico com queda abrupta de performance (>20pp vs. ciclo anterior)
2. Gestor pode configurar quais alertas deseja receber
3. Alertas incluem link direto para dashboard relevante
4. Frequência máxima: 1 alerta por tipo por dia (evitar spam)
5. Dashboard mostra histórico de alertas enviados

**Notas Técnicas**:
- Trigger: Cron job diário analisa condições de alerta
- Delivery: SendGrid (e-mail) ou Twilio (WhatsApp)
- Preferences: stored em user_settings table

---

## Epic 5: Autenticação, Permissões e Observabilidade (Infrastructure & Ops)

**Objetivo**: SSO, RBAC, observabilidade completa e compliance LGPD.

**Valor de Negócio**: Requisitos não-negociáveis para deploy em produção com cliente enterprise.

**Prioridade**: ALTA | **Fase**: Mês 1 (parcial) + Mês 2 (completo) | **Total Stories**: 8

---

### US-AUTH-01: Integração SSO com Sistema da Montadora

**Como** mecânico ou gestor
**Quero** fazer login com minhas credenciais corporativas
**Para que** eu não precise criar nova senha

**Pré-requisitos**: Nenhum (infraestrutura base)

**Critérios de Aceitação**:
1. Login via SAML 2.0 ou OAuth 2.0 (conforme DMS da montadora)
2. Após autenticação bem-sucedida, usuário é redirecionado para dashboard apropriado
3. Atributos do usuário são sincronizados: nome, CPF, role, concessionária
4. Sessão tem duração de 8 horas (renovável)
5. Logout limpa sessão local e invalida token

**Notas Técnicas**:
- SAML library: python-saml ou passport-saml (Node.js)
- Identity Provider: configurado pela montadora
- Session storage: Redis com TTL 8h
- Callback URL: https://app.carguroo.com/auth/callback

---

### US-AUTH-02: Controle de Permissões (RBAC)

**Como** administrador
**Quero** definir permissões por role
**Para que** cada usuário acesse apenas funcionalidades apropriadas

**Pré-requisitos**: US-AUTH-01 (autenticação funcional)

**Critérios de Aceitação**:
1. 3 roles principais:
   - **Admin**: acesso total (gestão de usuários, configuração, etc.)
   - **Gestor**: criar avaliações, ver dashboards, exportar dados
   - **Mecânico**: responder avaliações, usar Copiloto
2. Permissões verificadas em backend (não apenas frontend)
3. Tentativa de acesso não autorizado retorna HTTP 403
4. Admin pode alterar role de usuários via interface
5. Logs de auditoria registram mudanças de permissões

**Notas Técnicas**:
- RBAC implementation: decorator @require_role("gestor") em endpoints
- Storage: user_roles table com foreign key para users
- Middleware: verifica permissões antes de executar controller

---

### US-AUTH-03: Gestão de Usuários (CRUD)

**Como** administrador
**Quero** gerenciar usuários da plataforma
**Para que** eu controle acesso e atualize informações

**Pré-requisitos**: US-AUTH-02 (RBAC)

**Critérios de Aceitação**:
1. Interface de gestão de usuários com:
   - Listar todos os usuários (paginado)
   - Criar novo usuário (nome, CPF, role, concessionária)
   - Editar usuário existente
   - Desativar usuário (soft delete)
   - Reativar usuário desativado
2. Busca por nome ou CPF
3. Filtros por role e concessionária
4. Bulk import via CSV (para onboarding de 450 mecânicos)
5. Logs de auditoria para todas as operações

**Notas Técnicas**:
- Soft delete: campo is_active (boolean)
- Bulk import: parse CSV + validação + batch insert
- Auditoria: tabela audit_log com user_id, action, timestamp

---

### US-AUTH-04: Logs Estruturados com Trace ID

**Como** desenvolvedor/SRE
**Quero** logs estruturados com trace ID
**Para que** eu possa debugar problemas em produção

**Pré-requisitos**: Infraestrutura base

**Critérios de Aceitação**:
1. Todos os logs são estruturados em JSON com campos obrigatórios:
   - timestamp (ISO 8601)
   - level (DEBUG/INFO/WARNING/ERROR)
   - trace_id (UUID único por request)
   - message
   - context (user_id, endpoint, etc.)
2. Trace ID é propagado em headers entre serviços
3. Logs são enviados para agregador centralizado (ex: ELK, Datadog)
4. Interface permite buscar logs por trace_id
5. Retention: 90 dias em hot storage, 1 ano em cold storage

**Notas Técnicas**:
- Logging library: structlog (Python) ou winston (Node.js)
- Trace ID: gerado em middleware e injetado em todos os logs
- Aggregator: Elasticsearch + Kibana ou Datadog Logs

---

### US-AUTH-05: Métricas de Negócio e Técnicas

**Como** SRE ou gestor de produto
**Quero** visualizar métricas de negócio e técnicas
**Para que** eu monitore saúde do sistema e KPIs

**Pré-requisitos**: Infraestrutura base

**Critérios de Aceitação**:
1. Métricas de negócio expostas:
   - WAU (Weekly Active Users)
   - Total de queries do Copiloto
   - Taxa de conclusão de avaliações
   - Taxa de feedback positivo
2. Métricas técnicas:
   - Latência (p50/p95/p99) por endpoint
   - Error rate (% de requests com erro)
   - Throughput (requests/segundo)
3. Métricas em formato Prometheus (scrape endpoint /metrics)
4. Dashboards Grafana pré-configurados
5. Alertas configuráveis (ex: error rate >5% por 5min)

**Notas Técnicas**:
- Instrumentation: prometheus_client library
- Metrics endpoint: /metrics (protegido, apenas internal IPs)
- Grafana dashboards: exportados como JSON para versionamento

---

### US-AUTH-06: Alertas de Degradação de Serviço

**Como** SRE
**Quero** receber alertas automáticos quando serviço degradar
**Para que** eu possa agir rapidamente e minimizar downtime

**Pré-requisitos**: US-AUTH-05 (métricas expostas)

**Critérios de Aceitação**:
1. Alertas configurados para condições críticas:
   - Error rate >5% por 5 minutos
   - Latência p95 >10s por 5 minutos
   - Uptime <99% em janela de 1 hora
   - LLM API down (circuit breaker ativado)
2. Alertas enviados via:
   - E-mail para equipe de ops
   - Slack channel dedicado (#carguroo-alerts)
3. Alertas incluem link direto para dashboard relevante
4. Supressão de alertas duplicados (cooldown de 30min)
5. Runbook link para cada tipo de alerta

**Notas Técnicas**:
- Alerting: Prometheus Alertmanager ou Datadog Monitors
- Channels: configurados via webhook (Slack, PagerDuty, e-mail)
- Runbooks: documentados em wiki ou Notion

---

### US-AUTH-07: Compliance LGPD - Criptografia e Auditoria

**Como** DPO (Data Protection Officer)
**Quero** garantir compliance com LGPD
**Para que** empresa evite multas e proteja dados de usuários

**Pré-requisitos**: Infraestrutura base

**Critérios de Aceitação**:
1. Criptografia em trânsito: TLS 1.3 em todas as conexões (HTTPS)
2. Criptografia em repouso: AES-256 para dados sensíveis (CPF, respostas de avaliações)
3. Logs de auditoria completos:
   - Quem acessou quais dados pessoais e quando
   - Quem criou/editou/deletou usuários
4. Capacidade de anonimização: substituir dados pessoais por hashes irreversíveis
5. Capacidade de exclusão: deletar todos os dados de um usuário em <48h (direito ao esquecimento)
6. Data retention policy: dados são deletados automaticamente após 2 anos

**Notas Técnicas**:
- TLS: configurado em load balancer (ALB ou Nginx)
- Encryption at rest: campo-level encryption ou database-level (PostgreSQL)
- Anonimização: substituir CPF por hash SHA-256
- Exclusão: cascade delete + verificação manual

---

### US-AUTH-08: Health Checks e Status Page

**Como** usuário ou SRE
**Quero** verificar saúde do sistema
**Para que** eu saiba se serviço está disponível antes de tentar usar

**Pré-requisitos**: Infraestrutura base

**Critérios de Aceitação**:
1. Endpoint /health retorna status do sistema:
   - UP: todos os serviços críticos funcionando
   - DEGRADED: um serviço não-crítico com problema
   - DOWN: serviço crítico indisponível
2. Health check verifica:
   - Database connectivity (PostgreSQL)
   - Redis connectivity
   - Vector DB connectivity
   - LLM API accessibility
3. Status page pública mostra histórico de uptime (últimos 90 dias)
4. Incidentes são documentados com:
   - Timestamp início/fim
   - Duração
   - Impacto (qual funcionalidade afetada)
   - Causa raiz e resolução
5. Subscrição a notificações de incidentes via e-mail

**Notas Técnicas**:
- Health endpoint: GET /health (não autenticado)
- Response time: <100ms
- Status page: Statuspage.io (managed) ou self-hosted (cachet)
- Monitoring: Pingdom ou UptimeRobot para verificações externas

---

## Próximos Passos

Este documento de Epics serve como base para:

1. **Estimativa de Esforço**: Cada story pode ser estimada em horas/days (solo dev)
2. **Sprint Planning**: Agrupar stories em sprints de 1-2 semanas
3. **Tracking de Progresso**: Marcar stories como "Done" conforme desenvolvimento
4. **Handoff para Desenvolvimento**: Desenvolver specs técnicas detalhadas por story

**Recomendação**: Começar pelo **Epic 1** (Foundation RAG) → **Epic 2** (Copiloto MVP) → **Epic 3** (Avaliação) → **Epic 4** (Dashboard) → **Epic 5** (finalizar Observabilidade).

---

**Última Atualização**: 2025-10-10
**Próxima Revisão**: Após architecture phase (solution-architecture.md completo)
