# CarGuroo Product Requirements Document (PRD)

**Author:** Allan
**Date:** 2025-10-10
**Project Level:** Level 3 (Full Product MVP)
**Project Type:** Web Application (SaaS B2B Platform)
**Target Scale:** 450 mechanics, 30 dealerships (pilot client)

---

## Description, Context and Goals

### Description

O **CarGuroo** é uma plataforma SaaS B2B de IA generativa que transforma o pós-venda automotivo através de dois produtos integrados:

1. **Copiloto do Mecânico**: Assistente conversacional baseado em IA que auxilia mecânicos durante a execução de serviços, fornecendo diagnósticos precisos em tempo real, acesso imediato a informações técnicas e sugestões de próximos passos.

2. **Sistema de Avaliação**: Plataforma de mapeamento e capacitação de competências que acompanha mecânicos durante todo o ciclo profissional (contratação → qualificação contínua → especialização por área técnica), baseada em metodologias científicas modernas (Bloom, IRT, CBA, Kirkpatrick).

**Sinergia de Infraestrutura**: Ambos os produtos compartilham a mesma infraestrutura RAG moderna (ingestão de documentos, embeddings, busca vetorial, processamento multimodal), reduzindo significativamente duplicação de desenvolvimento e permitindo reutilização de componentes.

**Cliente Piloto Confirmado**: Montadora brasileira com 450 mecânicos distribuídos em 30 concessionárias proprietárias, com acesso garantido a dados reais e ambiente de produção para co-criação do MVP.

### Deployment Intent

**MVP para Validação com Cliente Piloto Único**

O CarGuroo será desenvolvido como MVP focado em **validação de produto e demonstração de ROI** com um único cliente piloto (montadora brasileira).

**Características do Deployment**:
- **Single-tenant**: 1 cliente piloto apenas, sem multi-tenancy
- **Deploy simplificado**: Single-instance (cloud ou on-premise conforme preferência do cliente)
- **Escalabilidade moderada**: Dimensionado para 450 usuários, não 10K+
- **Observabilidade básica**: Logs e métricas essenciais, não APM enterprise
- **Backup básico**: Snapshots simples, não disaster recovery multi-região
- **Integrações mínimas**: SSO + acesso a bases de conhecimento, sem integração bidirecional completa com DMS no MVP

**Foco**: Velocidade de validação, iteração rápida baseada em feedback de campo, e demonstração clara de impacto mensurável antes de escalar.

### Context

#### O Problema

O pós-venda automotivo brasileiro enfrenta **desafios estruturais críticos** que geram custos operacionais elevados para montadoras e concessionárias:

**Diagnósticos imprecisos e demorados**: Mecânicos perdem tempo excessivo buscando informações em manuais extensos e consultando help desk com respostas assíncronas que levam dias. Isso resulta em diagnósticos por tentativa e erro, gerando retrabalho frequente (~50% de taxa de retorno) e tempo de imobilização elevado.

**Invisibilidade de competências em escala**: Milhares de mecânicos distribuídos por todo o Brasil sem visibilidade de competências pela alta gestão. Impossibilidade de mapear gaps de conhecimento, direcionar capacitação assertivamente ou alocar profissionais de forma otimizada, resultando em qualidade inconsistente e treinamentos genéricos ineficazes.

**Impacto financeiro massivo**: Para o cliente piloto (450 mecânicos), os custos anuais estimados são ~R$ 8.1M/ano em help desk, retrabalho e ineficiência. Além disso, a experiência insatisfatória de pós-venda impacta negativamente NPS e fidelização de clientes finais, levando à perda de receita recorrente pós-garantia.

#### A Oportunidade

A convergência de **IA generativa madura** (GPT-4, Claude), **RAG moderno** e **parceria confirmada com montadora** cria uma janela única para resolver esses problemas de forma escalável. O CarGuroo une assistência operacional em tempo real (Copiloto) com gestão estratégica de competências (Avaliação), oferecendo ROI comprovável de 200-300%+ no primeiro ano com payback de 3-6 meses.

**Por que agora é urgente**: Pressão por eficiência operacional em toda cadeia automotiva, pós-venda como diferencial competitivo crítico para fidelização de marca, e tecnologia de IA finalmente viável para soluções antes impossíveis.

### Goals

**1. Validar Viabilidade de Produto**
Atingir **70%+ de adoção ativa** (315+ mecânicos usando semanalmente) no cliente piloto em **9 meses**, demonstrando que a solução resolve dores reais dos usuários e integra-se ao workflow operacional.

**Métrica de Sucesso**:
- Mês 3: 200+ mecânicos ativos semanais (45%)
- Mês 6: 315+ mecânicos ativos semanais (70%)
- Mês 9: 360+ mecânicos ativos semanais (80%)
- Média de 15+ interações por mecânico/semana

**2. Comprovar ROI Mensurável**
Reduzir **custos operacionais de pós-venda em 20-30%** no primeiro ano através de melhorias mensuráveis em eficiência, qualidade e redução de retrabalho.

**Métrica de Sucesso**:
- 70% de redução em chamados de help desk (baseline → alvo)
- 25% de diminuição em custos de retrabalho
- 30% de redução em tempo médio de reparo
- Economia total: R$ 3.4M+ vs. investimento de R$ 810K-1.6M/ano

**3. Estabelecer Visibilidade de Competências**
Mapear **100% dos 450 mecânicos** do piloto por competência em **6 meses**, fornecendo visibilidade estratégica inédita para gestão de pós-venda e direcionamento de capacitação.

**Métrica de Sucesso**:
- Mês 3: 100% avaliados (baseline estabelecido)
- Mês 6: 2º ciclo completo (tracking de evolução)
- Mês 12: 4 ciclos completos (tendência clara de desenvolvimento)
- Dashboard acessado por gestores >3x por semana

**4. Aumentar Qualidade e Satisfação**
Elevar **NPS de pós-venda em 15+ pontos** e aumentar **taxa de resolução na primeira tentativa para 90%**, fortalecendo fidelização de clientes finais e reduzindo retorno de veículos.

**Métrica de Sucesso**:
- Taxa de resolução na primeira tentativa: 50% (baseline) → 90% (alvo)
- NPS de pós-venda: baseline atual + 15 pontos
- Taxa de retorno de clientes pós-garantia: +20%

**5. Criar Case de Sucesso Replicável**
Documentar **resultados mensuráveis** e **best practices** do piloto para viabilizar expansão para **2-3 montadoras adicionais** em 18-24 meses, atingindo 2.000+ mecânicos ativos.

**Métrica de Sucesso**:
- Cliente piloto renova para fase 2 (expansão)
- 2+ leads qualificados gerados por referência
- Case study completo com ROI documentado
- Playbook de implementação padronizado

---

## Requirements

### Functional Requirements

#### Grupo A: Copiloto do Mecânico - Interface Conversacional

**FR-01: Chat Conversacional Multi-canal**
O sistema deve fornecer interface conversacional acessível via WhatsApp Business API ou Web App, permitindo que mecânicos interajam de forma natural durante a execução de serviços.

**FR-02: Input Multimodal (Texto e Áudio)**
O Copiloto deve aceitar input em formato texto (digitado) e áudio (transcrição automática via speech-to-text), facilitando uso hands-free durante trabalho operacional.

**FR-03: Output Formatado em Texto**
As respostas do Copiloto devem ser fornecidas em texto formatado (markdown básico) com estrutura clara: diagnóstico sugerido, próximos passos, citações de fontes.

**FR-04: Histórico de Interações por Veículo/OS**
O sistema deve persistir histórico completo de interações por veículo ou ordem de serviço (OS), permitindo retomada de contexto em sessões futuras.

#### Grupo B: Copiloto do Mecânico - RAG e Diagnóstico Inteligente

**FR-05: Ingestão e Processamento de Base de Conhecimento**
O sistema deve ingerir, processar e indexar manuais técnicos (PDF), histórico de help desk e conteúdos de treinamento, realizando chunking, embedding e armazenamento em vector database.

**FR-06: Busca Semântica Avançada**
O Copiloto deve realizar busca semântica via embeddings sobre a base de conhecimento, recuperando informações relevantes mesmo quando termos exatos não são usados.

**FR-07: Diagnóstico Assistido com Fluxo Guiado**
O sistema deve guiar o mecânico através de fluxo estruturado de perguntas (sintomas → verificações → diagnóstico), sugerindo próximos passos com base no contexto.

**FR-08: Citação de Fontes e Rastreabilidade**
Todas as respostas do Copiloto devem incluir citações das fontes consultadas (ex: "Manual Técnico Modelo X, pág. 42") para validação e confiança.

**FR-09: Associação com Ordem de Serviço (OS)**
O Copiloto deve permitir associação de sessão conversacional com OS do sistema da concessionária, vinculando diagnóstico a contexto de trabalho.

#### Grupo C: Sistema de Avaliação - Criação e Execução

**FR-10: Interface de Gestão de Avaliações**
Gestores devem ter acesso a interface web para criar ciclos de avaliação, definindo escopo (Fase 1/2/3, área técnica, nível-alvo), período e público-alvo (mecânicos específicos ou grupos).

**FR-11: Geração Automática de Questões via IA**
O sistema deve gerar questões situacionais contextualizadas via IA generativa, baseadas em tópicos selecionados, manuais técnicos e casos reais do histórico de help desk.

**FR-12: Execução de Avaliações via Interface Conversacional**
Mecânicos devem responder avaliações via mesma interface do Copiloto (chat texto/áudio), recebendo questões sequenciais e podendo responder em linguagem natural.

**FR-13: Correção Automatizada com IA e Validação Humana**
O sistema deve realizar correção automática de respostas usando IA com rubricas detalhadas, sinalizando casos ambíguos para revisão manual por especialistas.

**FR-14: Classificação por Níveis e Fases**
O sistema deve classificar mecânicos em níveis específicos conforme fase:
- Fase 1 (Entrada): Aprovado/Reprovado
- Fase 2 (Qualificação): Iniciante/Adequado/Experiente
- Fase 3 (Especialização): Sem Qualificação/Qualificado/Especialista

#### Grupo D: Sistema de Avaliação - Análise e Visibilidade

**FR-15: Dashboard Agregado de Competências**
Gestores devem ter acesso a dashboard com visão agregada mostrando distribuição de mecânicos por nível (Iniciante/Adequado/Experiente), por área técnica e evolução ao longo do tempo.

**FR-16: Drill-down Individual de Competências**
O dashboard deve permitir drill-down para perfil individual de cada mecânico, exibindo competências por área técnica, histórico de avaliações e recomendações de desenvolvimento.

**FR-17: Identificação de Gaps Críticos**
O sistema deve identificar e destacar gaps críticos de conhecimento (áreas com baixa proficiência ou alta concentração de mecânicos iniciantes), priorizando ações de capacitação.

**FR-18: Feedback Detalhado para Mecânicos**
Após cada avaliação, mecânicos devem receber feedback detalhado (o que acertaram, o que podem melhorar, materiais de estudo sugeridos) de forma construtiva e formativa.

#### Grupo E: Infraestrutura e Administração

**FR-19: Gestão de Usuários e Permissões**
O sistema deve permitir cadastro e gestão de usuários com três níveis de permissão: Admin (montadora), Gestor (concessionária) e Mecânico, com SSO integrado aos sistemas da concessionária.

**FR-20: Observabilidade e Métricas**
O sistema deve registrar logs de todas as interações (Copiloto e Avaliação) e calcular métricas básicas de uso (usuários ativos, interações por mecânico, latência, acurácia) para monitoramento de produto.

### Non-Functional Requirements

**NFR-01: Latência de Resposta do Copiloto**
O Copiloto deve fornecer respostas com latência p95 < 5 segundos (do input do mecânico até resposta completa), garantindo fluidez na interação durante trabalho operacional.

**NFR-02: Disponibilidade do Sistema (MVP)**
O sistema deve ter uptime de 99.5% (SLA MVP), tolerando no máximo ~3.6 horas de downtime por mês durante horário comercial (7h-19h, seg-sex).

**NFR-03: Escalabilidade para Cliente Piloto**
O sistema deve suportar 450 usuários simultâneos com até 1.000 mecânicos cadastrados (margem para expansão do piloto), sem degradação perceptível de performance.

**NFR-04: Acurácia de Diagnósticos e Correções**
- Respostas do Copiloto devem ter acurácia > 75% (validada por especialistas via amostragem)
- Correções automáticas de avaliações devem ter concordância inter-rater (IA vs. humano) > 80% (Kappa > 0.75)

**NFR-05: Segurança e Privacidade de Dados (LGPD)**
O sistema deve estar em compliance com LGPD:
- Criptografia em trânsito (TLS 1.3) e em repouso (AES-256)
- Isolamento de dados por tenant (mesmo em single-tenant MVP)
- Logs de acesso e auditoria completos
- Capacidade de anonimização e exclusão de dados (direito ao esquecimento)

**NFR-06: Compatibilidade de Interfaces**
- **Web App (Gestores)**: Compatível com Chrome, Edge, Safari (últimas 2 versões)
- **WhatsApp**: Totalmente funcional via WhatsApp Business API oficial
- **Web Chat (Alternativa)**: Responsivo para mobile (iOS Safari, Android Chrome)

**NFR-07: Acessibilidade (WCAG 2.1 Level AA)**
A interface web de gestão deve atender WCAG 2.1 Level AA, incluindo:
- Suporte a leitores de tela
- Navegação por teclado completa
- Contraste de cores adequado
- Labels e ARIA roles apropriados

**NFR-08: Observabilidade e Monitoramento**
O sistema deve fornecer observabilidade completa com:
- Logs estruturados (JSON) com trace_id por request
- Métricas de negócio: WAU, interações/mecânico, taxa de conclusão de avaliações
- Métricas técnicas: latência (p50/p95/p99), error rate, throughput
- Alertas configuráveis para degradação de serviço

**NFR-09: Custo Operacional de LLM**
O sistema deve otimizar custos de uso de LLM mantendo acurácia:
- Caching de respostas similares (hit rate > 30%)
- Uso de modelos menores para tarefas simples (classificação, validação)
- Custo médio por interação < R$ 0.50 (alvo para viabilidade econômica)

**NFR-10: Portabilidade de Deployment**
A solução deve ser containerizada (Docker) e portável para deploy em:
- Cloud pública (AWS ou Google Cloud)
- On-premise (caso exigência do cliente por compliance)
- Configuração via variáveis de ambiente (12-factor app principles)

---

## User Journeys

### Journey 1: Mecânico Usando Copiloto para Diagnóstico Complexo

**Persona**: João, mecânico pleno com 5 anos de experiência em concessionária, classificado como "Adequado" no sistema.

**Contexto**: João recebe um veículo híbrido com problema intermitente no sistema de tração. O cliente relata que o carro às vezes "perde força" ao acelerar. Scanner não mostra códigos de erro consistentes. João não é especialista em sistemas híbridos.

**Objetivo**: Diagnosticar corretamente o problema e realizar reparo na primeira tentativa, evitando retorno do cliente.

**Jornada Detalhada**:

1. **Abertura de OS e Início de Sessão**
   - João abre OS no DMS da concessionária (#OS-45782)
   - Acessa WhatsApp e envia mensagem ao Copiloto: "Oi, preciso de ajuda com OS 45782"
   - Sistema autentica João via SSO e associa sessão à OS
   - Copiloto responde: "Olá João! Vi que você abriu OS para [Modelo Híbrido XYZ, 2023]. Como posso ajudar?"

2. **Descrição do Problema**
   - João descreve via áudio (hands-free): "Cliente falou que o carro perde força de vez em quando ao acelerar. Fiz teste rápido e vi que acontece, mas scanner não tá mostrando erro fixo."
   - Sistema transcreve áudio e processa input
   - **Decisão do Sistema**: Busca semântica por "perda de potência intermitente + híbrido + sem código de erro"

3. **Diagnóstico Guiado**
   - Copiloto retorna fluxo guiado:
     - "Entendi. Vou te ajudar a investigar. Primeiras verificações:"
     - "1. Durante o teste, o motor elétrico desliga completamente ou só perde assistência?"
     - "2. O problema acontece mais em baixa ou alta velocidade?"
   - João responde: "Só perde assistência, motor a combustão continua. Acontece mais em baixa velocidade, tipo em arrancada."
   - **Decisão do Sistema**: Refina busca para "perda de assistência motor elétrico + baixa velocidade"

4. **Sugestão de Diagnóstico com Fontes**
   - Copiloto responde:
     - "Baseado nos sintomas, as causas mais prováveis são:"
     - "**1. Sensor de torque do motor elétrico com leitura intermitente** (70% de probabilidade)"
     - "**2. Baixa tensão na bateria de alta voltagem** (20%)"
     - "**3. Software da ECU híbrida desatualizado** (10%)"
     - "📘 *Fonte: Manual Técnico Modelo XYZ-2023, pág. 187 + Boletim Técnico BT-2024-03*"
     - "Próximos passos sugeridos: [lista de verificações]"
   - **Decisão de João**: Segue sugestões na ordem de probabilidade

5. **Verificações e Resolução**
   - João realiza verificações guiadas pelo Copiloto
   - Confirma leitura intermitente do sensor de torque
   - Copiloto sugere procedimento de substituição detalhado
   - João substitui sensor conforme orientação
   - Testa veículo: problema resolvido

6. **Feedback e Conclusão**
   - Copiloto pergunta: "O problema foi resolvido?"
   - João confirma: "Sim, resolveu!"
   - Sistema registra interação bem-sucedida e encerra sessão
   - João fecha OS no DMS com diagnóstico e reparo corretos

**Outcome**: João resolveu problema complexo fora de sua especialização em 90 minutos (vs. 3-4 horas ou chamado de help desk). Cliente satisfeito, sem retorno. João ganha confiança para lidar com sistemas híbridos.

---

### Journey 2: Gestora Criando Ciclo de Avaliação e Analisando Competências

**Persona**: Maria, gestora de pós-venda regional responsável por 6 concessionárias (90 mecânicos no total).

**Contexto**: É início de trimestre e Maria precisa criar o ciclo de Avaliação de Fase 2 (Qualificação Contínua) para todos os 90 mecânicos sob sua gestão. Além disso, precisa identificar gaps críticos para planejar capacitações do próximo trimestre.

**Objetivo**: Criar ciclo de avaliação trimestral, garantir conclusão por todos os mecânicos, e identificar necessidades de treinamento.

**Jornada Detalhada**:

1. **Login e Acesso ao Dashboard**
   - Maria acessa Web App via SSO corporativo
   - Dashboard mostra visão geral: 90 mecânicos, distribuição atual por nível (25 Iniciantes, 50 Adequados, 15 Experientes)
   - Vê notificação: "Ciclo Q1-2025 concluído. Criar ciclo Q2-2025?"

2. **Criação de Ciclo de Avaliação**
   - Maria clica em "Criar Novo Ciclo"
   - Wizard guiado:
     - **Fase**: Seleciona "Fase 2 - Qualificação Contínua"
     - **Público-alvo**: Seleciona "Todas as 6 concessionárias" (90 mecânicos)
     - **Período**: Define "15/Out - 30/Out/2025" (2 semanas)
     - **Escopo de Competências**: Seleciona áreas a avaliar (Diagnóstico Geral, Manutenção Preventiva, Sistemas de Freios)
   - **Decisão do Sistema**: IA gera banco de 30 questões situacionais adaptadas ao nível médio do grupo

3. **Revisão e Publicação**
   - Sistema mostra preview de 5 questões geradas
   - Maria revisa e aprova (confia na IA baseada em ciclos anteriores)
   - Clica em "Publicar e Notificar Mecânicos"
   - Sistema envia notificação via WhatsApp para os 90 mecânicos

4. **Monitoramento de Progresso**
   - Maria retorna ao dashboard após 1 semana
   - Vê progresso: 62/90 completaram (69%)
   - Identifica 3 concessionárias com taxa de conclusão baixa (<50%)
   - **Decisão de Maria**: Liga para gerentes dessas concessionárias para engajar mecânicos

5. **Análise de Resultados (Após Conclusão)**
   - Ao final do período: 85/90 completaram (94% - meta atingida)
   - Maria acessa "Dashboard de Competências"
   - Visão agregada mostra:
     - Distribuição por nível: 20 Iniciantes, 55 Adequados, 10 Experientes (melhoria vs. Q1)
     - **Gap crítico identificado**: 60% dos mecânicos tiveram baixo desempenho em "Diagnóstico de Sistemas Elétricos Modernos"

6. **Drill-down e Ação**
   - Maria faz drill-down na área "Sistemas Elétricos"
   - Vê lista de mecânicos com score <60% nessa competência (35 mecânicos)
   - **Decisão de Maria**: Planeja treinamento focado em "Sistemas Elétricos Modernos" para esse grupo
   - Exporta lista e envia para equipe de RH/Treinamento

7. **Feedback para Mecânicos**
   - Sistema já enviou feedback detalhado automático para cada mecânico
   - Maria revisa amostras de feedback (quality check)
   - Aprova e mecânicos podem acessar via WhatsApp

**Outcome**: Maria mapeou competências de 85 mecânicos em 2 semanas, identificou gap crítico específico (não genérico), e planejou capacitação assertiva. Consegue demonstrar evolução da equipe com dados concretos para diretoria.

---

### Journey 3: Mecânico Completando Avaliação e Recebendo Feedback

**Persona**: Paulo, mecânico júnior com 18 meses de experiência, classificado como "Iniciante" na última avaliação.

**Contexto**: Paulo recebe notificação de novo ciclo de Avaliação Trimestral (Fase 2). Quer melhorar sua classificação para "Adequado" e demonstrar evolução.

**Objetivo**: Completar avaliação com melhor desempenho que ciclo anterior, receber feedback construtivo e plano de desenvolvimento.

**Jornada Detalhada**:

1. **Recebimento de Notificação**
   - Paulo recebe mensagem via WhatsApp:
     - "Olá Paulo! Novo ciclo de Avaliação Q2-2025 está aberto. Prazo: até 30/Out. Você tem 30 questões situacionais. Boa sorte! 💪"
   - **Decisão de Paulo**: Decide fazer em 3 sessões (10 questões por dia)

2. **Início da Avaliação (Sessão 1)**
   - Paulo responde: "Quero começar a avaliação"
   - Sistema apresenta instruções:
     - "Você receberá questões situacionais sobre diagnóstico e reparo. Responda com seus próprios conhecimentos, como se estivesse explicando para um colega. Sem tempo limite por questão."
   - Primeira questão (texto):
     - "Você recebe um veículo com freios fazendo ruído ao frear. Cliente relata que começou há 2 dias. Descreva seu processo de diagnóstico."
   - Paulo responde via áudio (mais confortável):
     - "Primeiro eu ia verificar pastilhas, ver se tão gastas. Depois checaria disco se tem ranhura. Se tiver ruído só de um lado, pode ser problema de pinça travada."

3. **Continuação da Avaliação**
   - Paulo completa 10 questões na primeira sessão (~25 minutos)
   - Sistema salva progresso: "10/30 concluídas. Continue quando quiser!"
   - Paulo retorna nos dias seguintes e completa 20 questões restantes

4. **Correção Automática (Backend)**
   - IA avalia respostas de Paulo contra rubricas de 4 níveis
   - Para questão de freios:
     - Rubrica: "Adequado - Identifica principais causas (pastilhas, discos) e propõe sequência lógica"
     - IA classifica resposta de Paulo como "Adequado" (nível 3/4)
   - Agregação de resultados: Paulo obtém 72% de acerto geral

5. **Recebimento de Feedback**
   - 2 dias após conclusão, Paulo recebe:
     - "Parabéns Paulo! Você completou a avaliação Q2-2025. Seus resultados:"
     - "**Classificação Geral: ADEQUADO** (72% - evoluiu de 58% no Q1! 🎉)"
     - "**Pontos Fortes**: Diagnóstico de sistemas mecânicos, procedimentos de segurança"
     - "**Áreas para Melhorar**: Sistemas elétricos modernos, diagnóstico de sensores eletrônicos"
     - "**Materiais Sugeridos**: [links para vídeos e manuais sobre sistemas elétricos]"

6. **Reação e Próximos Passos**
   - **Decisão de Paulo**: Sente motivado pela progressão (Iniciante → Adequado)
   - Acessa materiais sugeridos durante horário de almoço
   - Meta pessoal: chegar a "Experiente" em 2 ciclos (6 meses)

**Outcome**: Paulo tem visibilidade clara de sua evolução, sente reconhecimento pelo crescimento, e recebe direcionamento específico para continuar se desenvolvendo. Sistema cumpre papel formativo (não apenas avaliativo).

---

**Insights dos Journeys**:
- **Integração Natural**: Copiloto e Avaliação usam mesma interface conversacional (WhatsApp)
- **Decisões em Tempo Real**: Ambos usuários (mecânico e gestor) tomam decisões informadas por dados da plataforma
- **Feedback Loop**: Sistema aprende com interações e melhora sugestões ao longo do tempo

---

## UX Design Principles

Os princípios de UX do CarGuroo orientam todas as decisões de interface e experiência do usuário, garantindo que a solução seja intuitiva, confiável e eficaz para mecânicos e gestores.

### 1. Conversação Natural, Não Complexidade Técnica

**Princípio**: A interface conversacional deve aceitar linguagem natural e contexto do usuário, sem exigir comandos específicos ou sintaxe rígida.

**Aplicação**:
- Mecânicos podem descrever problemas como falariam com um colega: "Carro tá com barulho estranho no motor"
- Sistema entende variações linguísticas e termos coloquiais do dia a dia de oficina
- Não requer treinamento extensivo para uso básico

**Anti-pattern a evitar**: Chatbots que exigem comandos específicos ou não entendem contexto ("Desculpe, não entendi. Digite 'ajuda diagnóstico'").

---

### 2. Transparência e Rastreabilidade de Fontes

**Princípio**: Toda sugestão ou resposta do Copiloto deve citar fontes específicas (manuais, boletins técnicos, casos anteriores), permitindo validação e construindo confiança.

**Aplicação**:
- Citações claras: "Fonte: Manual Técnico Modelo XYZ-2023, pág. 187"
- Links diretos para seção relevante do documento (quando possível)
- Indicação de probabilidade/confiança quando aplicável (ex: "70% de probabilidade baseado em 12 casos similares")

**Benefício**: Mecânicos podem verificar informações e gestores auditam recomendações da IA.

---

### 3. Feedback Formativo, Não Punitivo

**Princípio**: O sistema de Avaliação deve ter caráter construtivo e de desenvolvimento, não de fiscalização ou punição. Feedback deve destacar pontos fortes E áreas de melhoria, sempre com caminhos de ação.

**Aplicação**:
- Linguagem encorajadora: "Você evoluiu de 58% para 72%! 🎉"
- Feedback específico: "Pontos fortes: diagnóstico mecânico" + "Áreas para melhorar: sistemas elétricos"
- Sempre acompanhado de materiais e próximos passos

**Anti-pattern a evitar**: Classificações frias sem contexto ou feedback genérico ("Você foi reprovado").

---

### 4. Mobile-First e Hands-Free Prioritário

**Princípio**: Mecânicos trabalham com as mãos sujas e em movimento. A interface deve priorizar uso mobile e permitir interação hands-free (voz).

**Aplicação**:
- Input de áudio como cidadão de primeira classe (não feature secundária)
- Respostas concisas e escaneáveis em tela pequena
- Botões grandes e touchable (min 44x44px)
- Funciona via WhatsApp (app já instalado e familiar)

**Contexto**: Mecânico pode consultar Copiloto enquanto está embaixo do veículo apenas falando.

---

### 5. Progressão e Gamificação Sutil

**Princípio**: Mecânicos devem ter senso claro de progressão e evolução ao longo do tempo, com reconhecimento de conquistas de forma sutil (não exagerada).

**Aplicação**:
- Visualização de evolução (Iniciante → Adequado → Experiente)
- Marcos de progresso: "Você completou 10 avaliações!"
- Comparação com si mesmo (não com outros - evita competição tóxica)

**Anti-pattern a evitar**: Rankings públicos ou competição entre mecânicos (pode gerar desmotivação).

---

### 6. Contextualização Inteligente e Memória de Sessão

**Princípio**: O sistema deve lembrar contexto de interações anteriores e usar informações já disponíveis (OS, histórico do veículo) para evitar retrabalho.

**Aplicação**:
- Copiloto associa automaticamente com OS aberta: "Vi que você está trabalhando no Modelo XYZ da OS #45782"
- Retoma histórico em sessões futuras: "Na última vez você estava investigando problema de freio. Resolveu?"
- Dashboard de gestores mostra tendências (não apenas snapshot)

**Benefício**: Reduz friction e demonstra que sistema "entende" o trabalho do usuário.

---

### 7. Ações Guiadas com Clareza de Próximos Passos

**Princípio**: Para mecânicos, especialmente iniciantes, o sistema deve guiar ações com próximos passos claros, evitando paralisia por excesso de opções.

**Aplicação**:
- Fluxo guiado de diagnóstico: "Primeira verificação: [ação]. Se X, então [próxima ação]."
- Wizards para gestores criarem avaliações (passo a passo)
- CTAs claros: "Começar avaliação", "Ver resultados", "Exportar lista"

**Anti-pattern a evitar**: Dashboards complexos com 20 opções sem hierarquia clara.

---

### 8. Performance Perceptível e Feedback de Progresso

**Princípio**: Toda ação deve ter feedback imediato. Para operações longas, mostrar progresso claro.

**Aplicação**:
- Indicador "digitando..." enquanto IA processa resposta
- Barra de progresso para upload de manuais técnicos (PDF grandes)
- Confirmação imediata após ações: "Ciclo criado com sucesso!"
- Skeleton screens ao carregar dashboards (não tela branca)

**Benefício**: Mecânicos não ficam inseguros se sistema "travou" ou está processando.

---

### 9. Acessibilidade e Inclusão Digital

**Princípio**: A interface deve ser acessível para usuários com variados níveis de letramento digital e necessidades especiais.

**Aplicação**:
- WCAG 2.1 Level AA compliance (contraste, navegação por teclado, leitores de tela)
- Linguagem simples e direta (evitar jargão técnico de UX/TI)
- Tutoriais visuais e onboarding guiado para novos usuários
- Suporte a diferentes níveis de zoom (acessibilidade visual)

**Contexto**: Mecânicos têm perfis diversos (idade, escolaridade, familiaridade com tecnologia).

---

### 10. Erro Humano é Esperado, Recuperação é Fácil

**Princípio**: O sistema deve antecipar erros comuns, prevenir quando possível, e facilitar recuperação quando ocorrem.

**Aplicação**:
- Confirmação antes de ações destrutivas: "Tem certeza que deseja excluir este ciclo de avaliação?"
- Salvamento automático de progresso em avaliações (não perde resposta se app fechar)
- Mensagens de erro claras e com ação sugerida: "Não foi possível enviar. Verifique sua conexão e tente novamente."
- Undo/Redo onde aplicável

**Benefício**: Reduz frustração e aumenta confiança no sistema.

---

## Epics

O desenvolvimento do CarGuroo MVP está estruturado em **5 epics principais**, sequenciados para entregar valor incremental e permitir validação contínua com o cliente piloto.

### Epic Overview

#### Epic 1: Infraestrutura RAG e Base de Conhecimento (Foundation)

**Objetivo**: Estabelecer fundação técnica compartilhada entre Copiloto e Avaliação, com capacidade de ingerir, processar e indexar documentos técnicos em vector database para busca semântica.

**Valor de Negócio**: Sem esta infraestrutura, nenhuma das funcionalidades core (Copiloto ou Avaliação) pode funcionar. É o "motor" de IA do sistema.

**Estimativa**: 8-10 user stories | Prioridade: **CRÍTICA** | Fase: MVP 1.0

**Dependências**: Nenhuma (primeiro epic a ser desenvolvido)

**Acceptance Criteria de Epic**:
- [ ] Sistema capaz de ingerir PDFs de manuais técnicos (>1000 páginas)
- [ ] Chunking e embedding automatizados funcionando
- [ ] Vector database indexado com busca semântica <500ms (p95)
- [ ] API de busca retorna top-5 chunks relevantes com scores

---

#### Epic 2: Copiloto do Mecânico - MVP (Primary Product)

**Objetivo**: Entregar interface conversacional funcional que permite mecânicos consultarem base de conhecimento, receberem diagnósticos assistidos e registrarem histórico por OS.

**Valor de Negócio**: Produto core #1 que reduz tempo de diagnóstico e dependência de help desk. Gera valor imediato e mensurável para mecânicos.

**Estimativa**: 10-12 user stories | Prioridade: **CRÍTICA** | Fase: MVP 1.0

**Dependências**: Epic 1 (RAG infrastructure) deve estar completo

**Acceptance Criteria de Epic**:
- [ ] Mecânico pode enviar mensagem via WhatsApp e receber resposta relevante
- [ ] Sistema aceita input texto e áudio (transcrição automática)
- [ ] Respostas incluem citações de fontes (manual técnico + página)
- [ ] Histórico de interações persiste e é consultável por OS
- [ ] Latência p95 <5s do input à resposta completa

---

#### Epic 3: Sistema de Avaliação - Criação e Execução (Secondary Product - Part 1)

**Objetivo**: Permitir que gestores criem ciclos de avaliação com questões geradas por IA, mecânicos respondam via chat, e sistema realize correção automatizada com classificação por níveis.

**Valor de Negócio**: Produto core #2 que fornece visibilidade de competências em escala. Diferencial competitivo crítico do CarGuroo.

**Estimativa**: 8-10 user stories | Prioridade: **ALTA** | Fase: MVP 1.0

**Dependências**: Epic 1 (RAG para geração de questões) e Epic 2 (interface conversacional reutilizada)

**Acceptance Criteria de Epic**:
- [ ] Gestor pode criar ciclo de avaliação via wizard guiado
- [ ] IA gera 30+ questões situacionais contextualizadas
- [ ] Mecânico recebe notificação e pode responder via chat (texto/áudio)
- [ ] Correção automatizada funciona com concordância >80% vs. especialistas
- [ ] Sistema classifica mecânicos em níveis (Iniciante/Adequado/Experiente)

---

#### Epic 4: Dashboard e Visibilidade de Competências (Secondary Product - Part 2)

**Objetivo**: Fornecer dashboards para gestores com visão agregada de competências, drill-down individual, identificação de gaps críticos e exportação de dados.

**Valor de Negócio**: Transforma dados de avaliação em insights acionáveis para gestão. Demonstra ROI do sistema de avaliação para alta gestão.

**Estimativa**: 6-8 user stories | Prioridade: **ALTA** | Fase: MVP 1.0

**Dependências**: Epic 3 (precisa de dados de avaliações para visualizar)

**Acceptance Criteria de Epic**:
- [ ] Dashboard mostra distribuição de mecânicos por nível (gráficos + tabelas)
- [ ] Drill-down individual funciona (perfil completo de competências)
- [ ] Gaps críticos são identificados e destacados automaticamente
- [ ] Exportação de listas (CSV/Excel) funciona
- [ ] Dashboards carregam em <2s (skeleton screens durante load)

---

#### Epic 5: Autenticação, Permissões e Observabilidade (Infrastructure & Ops)

**Objetivo**: Implementar autenticação via SSO, controle de permissões (RBAC), observabilidade completa (logs, métricas, alertas) e compliance com LGPD.

**Valor de Negócio**: Requisitos não-negociáveis para deploy em produção com cliente enterprise. Garante segurança, auditabilidade e capacidade de operação.

**Estimativa**: 7-9 user stories | Prioridade: **ALTA** | Fase: MVP 1.0

**Dependências**: Pode ser desenvolvido em paralelo aos epics 2-4

**Acceptance Criteria de Epic**:
- [ ] SSO integrado com sistema da montadora (SAML 2.0)
- [ ] RBAC funciona: Admin, Gestor, Mecânico com permissões distintas
- [ ] Logs estruturados (JSON) com trace_id em todas as requests
- [ ] Métricas de negócio e técnicas expostas (Prometheus/compatible)
- [ ] Compliance LGPD: criptografia, auditoria, capacidade de exclusão

---

### Epic Sequencing & Phasing

**Fase 1 - Foundation (Mês 1)**:
- Epic 1: Infraestrutura RAG (completo)
- Epic 5: Autenticação e SSO (parcial - apenas login funcional)

**Fase 2 - Core Products (Mês 2)**:
- Epic 2: Copiloto MVP (completo)
- Epic 3: Avaliação - Criação e Execução (completo)
- Epic 5: Observabilidade (completo)

**Fase 3 - Analytics & Refinement (Mês 3)**:
- Epic 4: Dashboard de Competências (completo)
- Refinamentos e ajustes baseados em feedback de campo
- Preparação para rollout completo (450 mecânicos)

**Total Estimado**: 39-49 user stories distribuídas em 5 epics

_Nota: Breakdown detalhado de user stories por epic disponível em `epics.md` (próximo documento a ser gerado)._

---

## Out of Scope

As seguintes funcionalidades são **importantes mas NÃO críticas para validação inicial do MVP**. Serão consideradas para fases futuras após comprovação de valor com cliente piloto.

### Funcionalidades Explicitamente Fora do MVP

#### 1. Copiloto do Motorista (B2C)
- **Escopo**: Interface para proprietários de veículos consultarem problemas
- **Decisão**: Foco total em B2B primeiro. B2C é mercado diferente com validação própria
- **Roadmap**: Fase 2+ (após consolidação com mecânicos)

#### 2. Multimodalidade Completa
- **Análise de Imagens**: Fotos de peças danificadas, códigos de erro no painel
- **Análise de Vídeos**: Demonstrações de problemas pelo mecânico
- **Transcrição de Áudios Longos**: >5 minutos de duração
- **Decisão**: MVP foca em texto e áudio curto. Imagem/vídeo aumenta complexidade sem validar valor core
- **Roadmap**: Fase 2 (6-12 meses pós-MVP)

#### 3. Integrações Profundas com Sistemas Legados
- **Sincronização Bidirecional com DMS**: Atualização automática de OS, criação de diagnósticos
- **Telemetria de Veículos**: Leitura de dados de sensores em tempo real
- **Sistemas de Estoque**: Verificação de disponibilidade de peças
- **Decisão**: MVP usa apenas SSO + associação manual com OS. Integrações complexas geram risco de atraso
- **Roadmap**: Fase 2-3 (após validação de valor)

#### 4. Features Avançadas de Avaliação
- **Recomendação Automática de Trilhas**: IA sugere cursos específicos baseado em gaps
- **Gamificação Avançada**: Badges, rankings, leaderboards
- **Avaliação Adaptativa em Tempo Real**: Questões ajustadas dinamicamente durante avaliação (IRT completo)
- **Certificação Formal**: Emissão de certificados oficiais reconhecidos
- **Decisão**: MVP valida correção e classificação básica. Features avançadas são incrementais
- **Roadmap**: Fase 2-3

#### 5. Analytics e Inteligência de Negócio Avançada
- **Dashboards Executivos C-level**: Visões estratégicas agregadas multi-concessionária
- **Predição de Problemas Recorrentes**: ML para identificar anomalias em lotes de veículos
- **Benchmarking Entre Concessionárias**: Comparação de performance regional
- **Decisão**: MVP foca em dashboards operacionais básicos. Analytics avançado requer volume de dados
- **Roadmap**: Fase 3+ (após 6+ meses de operação)

#### 6. Mobile Apps Nativos
- **iOS e Android**: Apps nativos dedicados
- **Modo Offline**: Sincronização quando conexão retorna
- **Decisão**: MVP usa WhatsApp (já instalado) + Web responsivo. Apps nativos são overhead grande
- **Roadmap**: Fase 3+ (se demanda clara de usuários)

#### 7. Multi-tenancy e Escalabilidade Enterprise
- **Multi-tenancy Completo**: Isolamento de dados entre múltiplas montadoras
- **Deploy Multi-região**: Disaster recovery, replicação geográfica
- **Autoscaling Avançado**: Kubernetes com HPA configurado
- **Decisão**: MVP é single-tenant para 1 cliente piloto. Arquitetura enterprise adiciona complexidade desnecessária
- **Roadmap**: Fase 4+ (quando expandir para 3+ montadoras)

### Simplificações Assumidas no MVP

**Deployment**:
- Single-instance (não distribuído)
- Cloud OU on-premise (não híbrido)
- Backup básico via snapshots (não DR enterprise)

**Observabilidade**:
- Logs e métricas básicos (não APM completo tipo New Relic/DataDog)
- Alertas simples via e-mail/Slack (não PagerDuty/OpsGenie)

**Segurança**:
- Compliance LGPD básico (não certificação ISO 27001)
- Penetration testing simplificado (não audit enterprise completo)

**Processos**:
- CI/CD básico (GitHub Actions simples, não GitOps complexo)
- Rollback manual (não blue-green/canary deployments)

### Critério de Re-inclusão

Features fora de escopo podem ser reavaliadas e incluídas se:
1. Cliente piloto solicitar explicitamente como blocker para expansão
2. Descoberta de campo mostrar valor crítico não antecipado
3. Remoção de outra feature liberar capacidade de desenvolvimento

---

## Assumptions and Dependencies

### Fatos Confirmados (Não São Mais Assumições)

Estes pontos foram **validados** durante discovery e são premissas sólidas do projeto:

✅ **Parceria com Montadora Brasileira Confirmada**: 450 mecânicos em 30 concessionárias com acesso garantido a dados reais e ambiente de produção

✅ **Suporte de Alta Gestão**: Gestores da montadora apoiam ativamente o projeto (top-down support confirmado)

✅ **Legado de 450 Mecânicos Sem Baseline**: Mecânicos existentes não têm avaliação formal prévia, exigindo estabelecimento de baseline inicial

✅ **Modelo de Desenvolvimento Acelerado**: Solo developer (Allan) com BMAD + Claude Code para velocidade máxima (2-3 meses para MVP)

### Assumptions Críticas a Validar

Estas assumições **devem ser validadas** durante MVP para mitigar riscos:

#### Sobre a Solução Técnica

⚠️ **IA Generativa é Capaz de Diagnósticos Precisos**: GPT-4 ou Claude pode fornecer respostas técnicas automotivas com acurácia >75%
- **Validação**: POC técnico com amostra de manuais antes de desenvolvimento completo
- **Risco se falsa**: Core value proposition falha. Mitigação: human-in-the-loop mais forte

⚠️ **Interface Conversacional é Adequada para Mecânicos**: Mecânicos preferem chat vs. dashboards tradicionais
- **Validação**: Piloto restrito com 15-20 mecânicos early adopters
- **Risco se falsa**: Baixa adoção. Mitigação: desenvolver interface alternativa (web tradicional)

⚠️ **Correção Automatizada de Avaliações é Confiável**: IA consegue concordância >80% com especialistas humanos
- **Validação**: Teste com painel de 3-5 especialistas revisando amostra de 50 respostas
- **Risco se falsa**: Sistema de avaliação perde credibilidade. Mitigação: aumentar validação humana

#### Sobre Adoção e Uso

⚠️ **Mecânicos Têm Acesso a Smartphones/Computador**: 30 concessionárias têm infraestrutura para uso do sistema
- **Validação**: Auditoria de infraestrutura com TI da montadora (primeiras 2 semanas)
- **Risco se falsa**: Barreira física de acesso. Mitigação: fornecimento de devices ou acesso via terminais fixos

⚠️ **Mecânicos Terão Tempo Durante Serviço**: Workflow operacional permite consultar Copiloto sem impactar produtividade
- **Validação**: Observação de campo em 2-3 concessionárias piloto
- **Risco se falsa**: Baixo uso real. Mitigação: ajustar UX para ser mais rápido ou usar em momentos específicos

⚠️ **Resistência Cultural é Superável**: Mecânicos aceitam "ser avaliados por IA" se posicionamento for formativo
- **Validação**: Pesquisa qualitativa + piloto com comunicação cuidadosa
- **Risco se falsa**: Rejeição do sistema de avaliação. Mitigação: tornar avaliação opcional ou anônima

#### Sobre Dados e Integrações

⚠️ **Manuais Técnicos Estão Acessíveis e Completos**: Montadora tem manuais digitalizados em qualidade suficiente
- **Validação**: Auditoria de qualidade de dados (primeiras 2 semanas)
- **Risco se falsa**: RAG tem acurácia baixa. Mitigação: processo de curadoria e enriquecimento de documentos

⚠️ **Histórico de Help Desk é Utilizável**: Dados históricos estão estruturados o suficiente para processamento
- **Validação**: Análise exploratória dos dados existentes
- **Risco se falsa**: Perda de fonte de conhecimento valiosa. Mitigação: focar apenas em manuais técnicos no MVP

⚠️ **DMS Permite Integração via SSO**: Sistema da concessionária suporta SAML 2.0 ou OAuth 2.0
- **Validação**: Confirmar com TI da montadora (sprint 0)
- **Risco se falsa**: Login manual requerido. Mitigação: criar base de usuários separada (menos conveniente mas funcional)

#### Sobre Viabilidade de Negócio

⚠️ **Pricing de R$ 150-300/mês por Mecânico é Aceitável**: Cliente concorda com modelo de precificação
- **Validação**: Negociação com procurement e CFO
- **Risco se falsa**: Inviabilidade econômica. Mitigação: ajustar modelo (por concessionária, volume, etc.)

⚠️ **ROI Demonstrado Leva a Renovação**: Cliente renova após 6-9 meses se resultados forem positivos
- **Validação**: Tracking rigoroso de métricas de impacto desde dia 1
- **Risco se falsa**: Churn do cliente piloto. Mitigação: ajustes contínuos baseados em feedback

### Dependências Externas Críticas

Estas dependências **bloqueiam** o desenvolvimento ou deploy se não resolvidas:

🔴 **BLOCKER - Acesso a Bases de Conhecimento da Montadora**
- **O que é necessário**: Manuais técnicos, histórico de help desk, conteúdos de treinamento
- **Dono**: Diretor de Pós-Venda da montadora
- **Timeline**: Precisa estar disponível em Sprint 1 (semana 1-2)
- **Mitigação se atraso**: Usar manuais públicos genéricos para POC técnico enquanto aguarda

🔴 **BLOCKER - Aprovação de Deploy (Cloud ou On-Premise)**
- **O que é necessário**: InfoSec aprovar arquitetura e plano de compliance LGPD
- **Dono**: CISO ou Head de InfoSec da montadora
- **Timeline**: Precisa estar definido em Sprint 2 (semana 3-4)
- **Mitigação se atraso**: Preparar arquitetura flexível que suporte ambos

🟡 **CRÍTICO - APIs do DMS para SSO**
- **O que é necessário**: Documentação e credenciais de API para integração SAML/OAuth
- **Dono**: Head de TI ou equipe de integração da montadora
- **Timeline**: Precisa estar disponível em Sprint 3 (semana 5-6)
- **Mitigação se bloqueado**: Implementar login separado (menos conveniente mas funcional)

🟡 **CRÍTICO - Painel de Especialistas para Validação de Rubricas**
- **O que é necessário**: 3-5 mecânicos seniores ou engenheiros para revisar questões de avaliação e rubricas
- **Dono**: Head de RH/Treinamento da montadora
- **Timeline**: Necessário a partir de Sprint 5 (quando avalição for desenvolvida)
- **Mitigação**: Allan pode fazer validação inicial, mas credibilidade é menor

🟢 **DESEJÁVEL - Piloto Restrito em 1 Concessionária**
- **O que é necessário**: 1 concessionária voluntária com ~15 mecânicos para testes intensivos antes de rollout
- **Dono**: Gerente de concessionária indicado pela montadora
- **Timeline**: Ideal a partir de Mês 2 (quando Copiloto MVP estiver funcional)
- **Benefício**: Reduz risco de rollout completo com problemas não detectados

### Riscos Principais e Planos de Mitigação

**Risco #1 - Qualidade Insuficiente da Base de Conhecimento** (Probabilidade: Média | Impacto: Alto)
- Mitigação: Auditoria prévia + processo de curadoria + feedback loop contínuo

**Risco #2 - Resistência Cultural de Mecânicos** (Probabilidade: Média-Alta | Impacto: Alto)
- Mitigação: Posicionamento como ferramenta de auxílio + envolvimento de representantes + demonstração de benefícios claros

**Risco #3 - Integrações com DMS Legado Mais Complexas que Esperado** (Probabilidade: Alta | Impacto: Médio)
- Mitigação: MVP sem integração bidirecional (apenas SSO) + Fase 2 para integrações profundas

**Risco #4 - Timeline de 2-3 Meses é Agressiva** (Probabilidade: Média | Impacto: Médio)
- Mitigação: Ruthless priorization + BMAD/Claude Code para velocidade + possibilidade de estender para 4 meses se necessário

---

## Next Steps

### Immediate Next Actions

Dado que este é um **projeto Level 3** com complexidade técnica significativa (IA generativa, RAG, avaliação científica), a arquitetura deve ser definida **antes** de começar desenvolvimento de user stories.

### 🏗️ Architecture Phase (REQUIRED)

**Por que arquitetura primeiro?**
- RAG moderno requer decisões técnicas críticas (vector DB, chunking strategy, embedding model)
- Integração com sistemas legados da montadora (DMS, SSO) tem implicações arquiteturais
- Compliance LGPD afeta design de dados e segurança
- Solo developer precisa de arquitetura clara para velocidade máxima

**Handoff para Arquiteto (ou Allan como Tech Lead)**:

Forneça ao arquiteto os seguintes documentos:
1. **Este PRD**: `PRD-CarGuroo-2025-10-10.md` (contexto completo de produto)
2. **Product Brief**: `product-brief-CarGuroo-2025-10-10.md` (visão de negócio e metodologias científicas)
3. **Project Analysis**: `project-workflow-analysis.md` (scope e abordagem de desenvolvimento)

**Pergunte ao arquiteto para:**
- Executar workflow de arquitetura (se disponível no BMAD)
- Considerar reference architectures para:
  - RAG-based conversational AI (LangChain, LlamaIndex patterns)
  - Multi-modal LLM applications
  - SaaS B2B com compliance LGPD
- Gerar solution fragments para componentes críticos:
  - Vector database + embedding pipeline
  - LLM orchestration layer
  - WhatsApp Business API integration
  - SSO/RBAC implementation
- Criar documento: `solution-architecture.md`

**Decisões Arquiteturais Pendentes (a serem resolvidas)**:
1. Vector DB específico: Pinecone vs. Weaviate vs. Qdrant vs. pgvector
2. LLM provider final: OpenAI GPT-4 vs. Anthropic Claude vs. open-source (Llama 3)
3. Chunking strategy otimizada para manuais técnicos automotivos
4. Caching strategy para reduzir custos de LLM
5. Deployment target: AWS vs. Google Cloud vs. on-premise
6. Orchestração de filas: Celery + RabbitMQ vs. alternativas
7. Observability stack: Prometheus + Grafana vs. managed (DataDog/New Relic)

---

### 📋 Complete Project Checklist

#### Phase 0: Sprint Zero (Semana 1-2)

**Validação de Assumptions e Dependências**:
- [ ] **BLOCKER**: Confirmar acesso a manuais técnicos e histórico de help desk da montadora
- [ ] **BLOCKER**: Aprovar deployment target (cloud ou on-premise) com InfoSec
- [ ] **CRÍTICO**: Auditar qualidade dos manuais técnicos (completude, formato, atualização)
- [ ] **CRÍTICO**: Confirmar disponibilidade de APIs do DMS para SSO
- [ ] **DESEJÁVEL**: Identificar concessionária piloto voluntária para testes (~15 mecânicos)

**Alinhamento de Stakeholders**:
- [ ] Workshop de alinhamento com stakeholders da montadora (sponsor, gestores, TI, RH)
- [ ] Definir painel de especialistas (3-5 mecânicos seniores/engenheiros) para validação de rubricas
- [ ] Estabelecer cadência de comunicação (semanal/quinzenal) com cliente piloto

**Setup de Projeto**:
- [ ] Configurar repositório Git (estrutura de monorepo ou multi-repo)
- [ ] Setup de ambiente de desenvolvimento local
- [ ] Configurar CI/CD pipeline básico (GitHub Actions)
- [ ] Provisionar ambientes: dev, staging, production (ou equivalente)

---

#### Phase 1: Architecture & Design (Semana 2-3)

- [ ] **Executar workflow de arquitetura** → Output: `solution-architecture.md`
  - Definir arquitetura de alto nível (diagramas C4 model)
  - Decidir stack tecnológico final
  - Especificar padrões de integração
  - Definir estratégia de dados e LGPD compliance

- [ ] **POC Técnico de RAG** (crítico para validar viabilidade)
  - Ingerir amostra de 1 manual técnico (~200 páginas)
  - Testar 3 estratégias de chunking
  - Comparar acurácia de busca semântica
  - Validar latência end-to-end
  - Output: Relatório de POC com decisões técnicas

- [ ] **Criar database schema design**
  - Modelo relacional para usuários, avaliações, interações
  - Definir índices e otimizações
  - Planejar migrations

- [ ] **Definir API specifications** (OpenAPI/Swagger)
  - Endpoints principais do Copiloto
  - Endpoints de gestão de avaliações
  - Endpoints de dashboard e analytics

---

#### Phase 2: Detailed Planning (Semana 3-4)

- [ ] **Gerar user stories detalhadas**
  - Comando sugerido: `/bmad:bmm:workflows:generate-stories` (se disponível)
  - Input: Este PRD + solution-architecture.md
  - Output: `user-stories.md` com critérios de aceitação completos por story

- [ ] **Definir estratégia de testes**
  - Unit tests: pytest para backend, Jest para frontend
  - Integration tests: contrato de APIs, fluxos end-to-end
  - UAT criteria: como validar com mecânicos reais

- [ ] **Criar sprint plan detalhado**
  - Priorizar stories conforme sequenciamento de epics (Foundation → Copiloto → Avaliação → Dashboard)
  - Estimar esforço por story (solo dev: usar hours ou days)
  - Definir milestones de entrega para demonstrações ao cliente

---

#### Phase 3: Development Preparation (Semana 4)

- [ ] **Setup de infraestrutura base**
  - Provisionar vector database (escolha final da arquitetura)
  - Configurar PostgreSQL + Redis
  - Setup de LLM API credentials (OpenAI ou Anthropic)
  - Configurar WhatsApp Business API (sandbox para testes)

- [ ] **Implementar esqueleto arquitetural**
  - API gateway com autenticação básica
  - Estrutura de módulos (Copiloto, Avaliação, Dashboard, Infra)
  - Logging e observabilidade básica

- [ ] **Criar protótipos de UX críticos**
  - Mockups de flow conversacional do Copiloto
  - Wireframes de dashboard de competências
  - Wizard de criação de avaliação

---

#### Phase 4: Development & Iteration (Mês 2-3)

**Seguir sequenciamento de epics conforme planejado**:

**Mês 1**:
- [ ] Epic 1: Infraestrutura RAG completa e testada
- [ ] Epic 5: Autenticação e SSO funcionais

**Mês 2**:
- [ ] Epic 2: Copiloto MVP funcional end-to-end
- [ ] Epic 3: Sistema de Avaliação - Criação e Execução
- [ ] **Piloto Restrito**: Testar com 15 mecânicos early adopters
- [ ] Iterar baseado em feedback

**Mês 3**:
- [ ] Epic 4: Dashboard de Competências completo
- [ ] Epic 5: Observabilidade completa (logs, métricas, alertas)
- [ ] Refinamentos finais baseados em feedback de campo
- [ ] Preparação para rollout completo (450 mecânicos)

---

#### Phase 5: Rollout & Monitoring (Mês 3-4)

- [ ] **Treinamento de gestores**
  - Como criar ciclos de avaliação
  - Como interpretar dashboard de competências
  - Como exportar dados e relatórios

- [ ] **Comunicação com mecânicos**
  - Envio de material explicativo via WhatsApp
  - Vídeos curtos demonstrando uso do Copiloto
  - Posicionamento do sistema de avaliação como ferramenta de desenvolvimento

- [ ] **Rollout gradual**
  - Fase 1: 50 mecânicos (1 semana)
  - Fase 2: 150 mecânicos (2 semanas)
  - Fase 3: 450 mecânicos (completo)

- [ ] **Estabelecer métricas e monitoring**
  - Dashboard de KPIs (WAU, interações/mecânico, taxa de conclusão de avaliações)
  - Alertas para degradação de serviço
  - Coleta de feedback qualitativo (NPS mensal)

---

### 🎯 Success Criteria de Projeto

O MVP será considerado **bem-sucedido** se:

**Adoção**:
- ✅ 70%+ dos 450 mecânicos usam Copiloto semanalmente (315+ WAU) em 6 meses
- ✅ 70%+ completam avaliações trimestrais no prazo

**Impacto Mensurável**:
- ✅ 20%+ de redução em tempo médio de diagnóstico
- ✅ 50%+ de redução em chamados de help desk
- ✅ 15+ pontos de aumento em NPS de pós-venda

**Satisfação**:
- ✅ NPS de mecânicos >40
- ✅ NPS de gestores >50

**Viabilidade de Negócio**:
- ✅ Cliente piloto renova para fase 2 (expansão)
- ✅ ROI demonstrado >200%
- ✅ 2+ leads qualificados gerados por referência

---

### 📚 Documentos de Referência

**Já Criados**:
- ✅ Product Brief: `product-brief-CarGuroo-2025-10-10.md`
- ✅ Project Analysis: `project-workflow-analysis.md`
- ✅ Este PRD: `PRD-CarGuroo-2025-10-10.md`

**Próximos Documentos** (a serem gerados):
- [ ] `epics.md` - Breakdown detalhado de epics e user stories (próximo passo!)
- [ ] `solution-architecture.md` - Arquitetura técnica completa
- [ ] `user-stories.md` - User stories detalhadas com critérios de aceitação
- [ ] `technical-decisions.md` - Registro de decisões técnicas (ADRs)
- [ ] `ux-specification.md` - Especificação de UX/UI (opcional para UI-heavy projects)

**Para Referência Externa**:
- Metodologias científicas de avaliação (ver Product Brief - seção completa com 8 referências)
- RAG best practices (LangChain, LlamaIndex documentation)
- WhatsApp Business API documentation

---

## Document Status

- [x] Goals and context validated with Product Brief
- [x] All functional requirements reviewed (20 FRs defined)
- [x] Non-functional requirements defined (10 NFRs)
- [x] User journeys cover all major personas (3 detailed journeys)
- [x] UX principles established (10 principles)
- [x] Epic structure defined for phased delivery (5 epics, 39-49 stories)
- [x] Out of scope explicitly documented
- [x] Assumptions and dependencies captured
- [ ] Architecture phase completed (NEXT STEP)
- [ ] Detailed user stories generated
- [ ] Ready for development

_Note: See technical-decisions.md for captured technical context (to be created during architecture phase)_

---

_This PRD adapts to project level Level 3 - providing appropriate detail without overburden._
