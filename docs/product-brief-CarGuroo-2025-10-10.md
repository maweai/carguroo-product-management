# Product Brief: CarGuroo

**Date:** 2025-10-10
**Author:** Allan
**Status:** Draft for PM Review

---

## Executive Summary

O CarGuroo é uma plataforma SaaS de IA generativa que transforma a experiência do pós-venda automotivo B2B, com foco inicial em duas soluções integradas para grandes montadoras e concessionárias: **Copiloto do Mecânico** (assistente IA para execução de serviços) e **Avaliação** (sistema de mapeamento e capacitação de conhecimento baseado em IA).

**Status de Parceria**: O CarGuroo já possui uma **parceria confirmada com uma montadora brasileira** para desenvolvimento e implementação do MVP. A parceria inclui acesso a dados reais, ambiente de produção e possibilidade de testes de campo com mecânicos e gestores.

**Escopo Inicial Confirmado**:
- **450 mecânicos** distribuídos em **30 concessionárias** por todo Brasil
- Foco inicial: **Concessionárias proprietárias** da montadora (modelo próprio, não delegadas)
- Abordagem: Co-criação com dados reais, validação contínua e iteração baseada em feedback de campo

A proposta de valor central é reduzir custos operacionais e aumentar a qualidade do pós-venda através de diagnósticos precisos em tempo real, redução de retrabalhos e visibilidade de competências dos mecânicos em escala através de um **sistema de avaliação contínua baseado em metodologias científicas modernas**.

O sistema de Avaliação acompanha o mecânico **durante todo o ciclo profissional**: desde a contratação (avaliação de entrada), passando por qualificação contínua (Iniciante → Adequado → Experiente), até especialização por área técnica (Elétrica, Mecânica, Sistemas de Tração, etc.).

**Impacto esperado**: 30% de redução no tempo médio de reparo, 90% de aumento na taxa de resolução na primeira tentativa, 25% de redução em custos de retrabalho e eliminação significativa de chamados de help desk.

---

## Problem Statement

### O Contexto do Pós-Venda Automotivo Atual

O pós-venda automotivo brasileiro enfrenta **desafios estruturais críticos** que geram custos operacionais elevados e experiências insatisfatórias:

**1. Diagnósticos Imprecisos e Demorados**
- Mecânicos gastam tempo excessivo tentando identificar problemas complexos em veículos
- Falta de acesso rápido e contextualizado a informações técnicas atualizadas
- **Impacto**: Carros ficam mais tempo na oficina, gerando insatisfação do cliente e perda de produtividade

**2. Consultas Manuais Ineficientes**
- Mecânicos perdem tempo consultando manuais técnicos extensos para cada modelo de veículo
- Informações dispersas entre múltiplas fontes (manuais, histórico de help desk, treinamentos)
- **Impacto**: Processo lento, propenso a erros e que aumenta o tempo de imobilização do veículo

**3. Retrabalhos Frequentes por Falhas de Diagnóstico**
- Falhas na identificação correta do problema levam a reparos incorretos
- Veículos retornam à oficina com o problema não resolvido
- **Impacto quantificado**: Alta taxa de retorno (problema não resolvido na primeira visita)

**4. Sobrecarga e Custos Elevados de Help Desk**
- Atendimento de help desk gera custo significativo (atendimento humano)
- Comunicação assíncrona leva vários dias para conclusão
- **Impacto**: Custo operacional elevado + tempo de resolução estendido

**5. Invisibilidade de Competências em Escala**
- Milhares de mecânicos distribuídos por todo o Brasil sem visibilidade de competências pela alta gestão
- Impossibilidade de mapear gaps de conhecimento e direcionar capacitação de forma assertiva
- Alocação ineficiente de mecânicos para serviços específicos
- **Impacto**: Qualidade inconsistente, desperdício de talento e treinamentos genéricos ineficazes

**6. Processos Fragmentados e Baixa Visibilidade**
- Jornada do pós-venda fragmentada entre múltiplos sistemas e pontos de contato
- Falta de visibilidade end-to-end do diagnóstico até a devolução do veículo
- **Impacto**: Perda de clientes após o período de garantia por falta de relacionamento e confiança

### Por Que Resolver Isso Agora É Urgente

- **Competitividade**: Pós-venda de qualidade é diferencial competitivo crítico para fidelização de marca
- **Custos Crescentes**: Pressão por eficiência operacional e redução de custos em toda cadeia automotiva
- **Tecnologia Disponível**: IA generativa e RAG moderno tornam viável soluções antes impossíveis
- **Escala do Problema**: Impacta milhares de mecânicos, centenas de concessionárias e milhões de proprietários

---

## Proposed Solution

### Visão da Solução

O **CarGuroo** é uma plataforma SaaS de IA que atua como copiloto inteligente para mecânicos e gestores, unificando o pós-venda em uma experiência proativa, eficiente e confiável. A solução inicial foca em **duas capacidades integradas**:

### 1. **Copiloto do Mecânico** (Assistente Inteligente para Execução de Serviços)

**O que é**: Sistema conversacional baseado em IA generativa que atua como assistente inteligente do mecânico durante toda execução do serviço.

**Como funciona**:
- Interface conversacional (áudio, texto e vídeo) integrada aos sistemas da concessionária
- Busca inteligente em base de conhecimento unificada e processada por RAG moderno:
  - Manuais técnicos de todos os modelos
  - Histórico completo de help desk (problemas/soluções anteriores)
  - Conteúdos de treinamentos técnicos atualizados
  - Descrição contextualizada de imagens de documentos
  - Transcrição e contextualização de vídeos e áudios técnicos
- Diagnósticos precisos em tempo real com sugestões de próximos passos
- Persistência em bancos de dados vetoriais com embeddings modernos

**Benefícios Mensuráveis**:
- ✅ Redução de 30% no tempo médio de reparo
- ✅ Aumento de 90% na taxa de resolução na primeira tentativa
- ✅ Diminuição de 25% nos custos com retrabalhos
- ✅ Eliminação massiva de chamados de help desk
- ✅ Integração nativa com sistemas existentes da montadora/concessionária

**Exemplo de uso**: Mecânico recebe veículo com problema de sistema híbrido. Via interface conversacional, descreve sintomas em áudio/texto. O Copiloto analisa histórico do modelo, casos similares resolvidos e manual técnico, fornecendo diagnóstico preciso e roteiro passo-a-passo de verificações e reparos.

### 2. **Avaliação** (Sistema de Avaliação Contínua baseado em IA e Metodologias Científicas)

**O que é**: Sistema abrangente de avaliação de competências técnicas que acompanha o mecânico durante todo seu ciclo profissional, desde a contratação até especialização avançada, baseado em IA generativa e metodologias científicas de avaliação de competências.

**Modelo de Avaliação em 3 Fases**:

#### **Fase 1: Avaliação de Entrada (Contratação)**
- **Objetivo**: Estabelecer baseline de conhecimento técnico do candidato
- **Escopo**: Conhecimentos gerais de mecânica automotiva (fundamentos)
- **Formato**: Avaliação estruturada com questões situacionais + práticas
- **Classificação**: Aprovado/Reprovado + Nível de entrada estimado
- **Duração**: 60-90 minutos
- **Uso**: Decisão de contratação + plano de onboarding personalizado

#### **Fase 2: Qualificação Contínua (Durante o Ciclo Profissional)**
- **Objetivo**: Mapear evolução de competências gerais em mecânica
- **Escopo**: Conhecimentos gerais aplicados (diagnóstico, reparo, manutenção preventiva)
- **Classificação em 3 Níveis**:
  - **Iniciante**: Conhecimento básico, requer supervisão frequente
  - **Adequado**: Autonomia em tarefas comuns, supervisão ocasional
  - **Experiente**: Autonomia completa, capaz de orientar outros
- **Frequência**: Avaliações trimestrais (4x/ano)
- **Formato**: Questões situacionais geradas por IA + histórico de performance no Copiloto
- **Progressão**: Iniciante → Adequado (6-12 meses) → Experiente (18-36 meses)

#### **Fase 3: Especialização por Área Técnica**
- **Objetivo**: Mapear proficiência em áreas técnicas específicas
- **Áreas de Especialização**:
  1. **Elétrica e Eletrônica** (sistemas elétricos, sensores, ECU)
  2. **Mecânica de Motor** (combustão, lubrificação, arrefecimento)
  3. **Sistemas de Tração** (transmissão, diferencial, tração 4x4)
  4. **Sistemas de Freios** (ABS, freios regenerativos, assistência)
  5. **Suspensão e Direção** (geometria, amortecedores, direção elétrica)
  6. **Sistemas Híbridos/Elétricos** (baterias, inversores, motores elétricos)
  7. **Diagnóstico Avançado** (OBD, análise de dados, troubleshooting complexo)
- **Classificação por Especialidade**:
  - **Sem Qualificação**: Não apto para trabalhar nessa área
  - **Qualificado**: Executa serviços básicos com supervisão
  - **Especialista**: Autonomia completa, referência técnica
- **Frequência**: Avaliações semestrais por área (2x/ano)
- **Certificação**: Mecânicos podem obter certificados por especialidade

**Como Funciona (Operação)**:

1. **Geração de Avaliações por IA**:
   - Gestores definem escopo (fase, nível, área técnica)
   - IA gera questões situacionais contextualizadas a partir de:
     - Manuais técnicos da montadora
     - Casos reais do histórico de help desk
     - Procedimentos e padrões de qualidade
   - Questões adaptadas ao nível (evita frustração ou tédio)

2. **Execução de Avaliações**:
   - Mecânico responde via interface conversacional (texto/áudio)
   - Perguntas situacionais: "Você recebe um veículo com sintoma X. Quais suas próximas ações?"
   - Sistema aceita respostas em linguagem natural
   - IA avalia correção e completude da resposta

3. **Correção Automatizada com Validação Humana**:
   - IA realiza correção automática com rubrica detalhada
   - Casos ambíguos são sinalizados para revisão manual
   - Feedback detalhado para o mecânico (o que acertou, o que pode melhorar)

4. **Classificação e Pontuação**:
   - Sistema agrega performance em múltiplas dimensões
   - Considera também: histórico de uso do Copiloto, taxa de resolução, retrabalho
   - Classificação baseada em thresholds calibrados (ver seção Metodologias)

5. **Dashboard de Competências**:
   - Visão agregada: distribuição por nível (Iniciante/Adequado/Experiente)
   - Drill-down individual: perfil de competências de cada mecânico
   - Identificação de gaps críticos e recomendações de capacitação
   - Tracking de evolução ao longo do tempo

**Tratamento do Legado (450 Mecânicos Existentes)**:

- **Desafio**: 450 mecânicos já contratados, sem baseline de avaliação formal
- **Abordagem**:
  1. **Avaliação Inicial Acelerada** (primeiros 3 meses):
     - Todos os 450 mecânicos passam por avaliação de Fase 2 (Qualificação Geral)
     - Estabelece baseline para comparação futura
     - Priorização: começar por concessionárias proprietárias
  2. **Classificação Inicial Estimada**:
     - Usar heurísticas: tempo de casa, histórico de performance (se disponível)
     - Validar com avaliação formal nos primeiros 90 dias
  3. **Ciclo Normal a Partir do 4º Mês**:
     - Mecânicos entram no ciclo regular de avaliações trimestrais/semestrais

**Benefícios Mensuráveis**:
- ✅ 100% de visibilidade de competências de 450 mecânicos em 3 meses
- ✅ Alocação otimizada baseada em competências reais (não apenas senioridade)
- ✅ Identificação objetiva de candidatos para promoção
- ✅ Redução de 50% em custos de treinamento genérico (foco em gaps reais)
- ✅ Aumento de 30% em eficácia de capacitação (treinamento direcionado)
- ✅ Retenção de talentos via plano de desenvolvimento claro e mensurável

**Exemplo de uso - Fase 2 (Qualificação)**:
Mecânico João é avaliado trimestralmente. No Q1, é classificado como "Iniciante" (60% de acerto). Recebe feedback específico e treinamento focado. No Q2, melhora para "Adequado" (78% de acerto). Dashboard mostra sua progressão. Gestor reconhece evolução e aumenta autonomia de João em serviços.

**Exemplo de uso - Fase 3 (Especialização)**:
Mecânico Maria é "Experiente" em geral, mas quer se especializar em Sistemas Híbridos/Elétricos. Faz avaliação específica dessa área. IA gera questões sobre baterias de alta voltagem, inversores, diagnóstico de sistemas híbridos. Maria obtém 85% e é classificada como "Especialista" em Híbridos. Passa a ser referência técnica e alocada prioritariamente para esses veículos.

### Arquitetura de Integração

- **Sistema integrado** aos sistemas de gestão da montadora (SSO, dados de usuários, bases de conhecimento)
- **Processamento avançado de documentos**: OCR com descrição contextualizada de imagens, transcrição de vídeos/áudios, tudo indexado em bancos vetoriais
- **RAG moderno**: Embeddings modernos para recuperação semântica precisa
- **Multi-modal**: Suporte a áudio, texto, imagens e vídeo tanto para input quanto output

### O Que Torna Esta Solução Diferente

1. **Foco em B2B para grandes montadoras**: Não é ferramenta genérica, mas solução especializada no contexto automotivo
2. **Integração profunda**: Conecta-se nativamente aos sistemas existentes (não é overlay)
3. **IA contextualizada**: Treinada especificamente com conhecimento técnico automotivo da montadora
4. **Visão integrada**: Une assistência operacional (Copiloto) + gestão estratégica (Avaliação)
5. **Impacto mensurável**: Foco em métricas de negócio claras (tempo, custo, qualidade, NPS)
6. **Base científica rigorosa**: Sistema de avaliação fundamentado em metodologias científicas reconhecidas internacionalmente

---

## Metodologias Científicas de Avaliação de Competências

O sistema de Avaliação do CarGuroo é fundamentado em **metodologias científicas modernas** de avaliação de competências profissionais, garantindo rigor, validade e confiabilidade nas classificações.

### Frameworks Teóricos Adotados

#### 1. **Taxonomia de Bloom Revisada** (Anderson & Krathwohl, 2001)

**O que é**: Framework hierárquico de níveis cognitivos para avaliar profundidade de conhecimento.

**6 Níveis Cognitivos (do básico ao avançado)**:
1. **Lembrar**: Recordar fatos, conceitos, procedimentos
2. **Entender**: Explicar ideias ou conceitos com palavras próprias
3. **Aplicar**: Usar conhecimento em situações novas
4. **Analisar**: Decompor informação e identificar relações
5. **Avaliar**: Fazer julgamentos baseados em critérios
6. **Criar**: Combinar elementos para formar algo novo

**Aplicação no CarGuroo**:
- **Fase 1 (Entrada)**: Avalia níveis 1-3 (Lembrar, Entender, Aplicar)
  - Ex: "Descreva o ciclo de 4 tempos de um motor a combustão" (Entender)
- **Fase 2 (Qualificação)**:
  - **Iniciante**: Predominância níveis 1-2
  - **Adequado**: Predominância níveis 3-4 (Aplicar, Analisar)
  - **Experiente**: Predominância níveis 4-6 (Analisar, Avaliar, Criar)
- **Fase 3 (Especialização)**: Avalia níveis 4-6 em profundidade
  - Ex: "Dados estes sintomas complexos, qual estratégia de diagnóstico você seguiria e por quê?" (Criar + Avaliar)

**Referência**: Anderson, L. W., & Krathwohl, D. R. (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. Longman.

---

#### 2. **Competency-Based Assessment (CBA)**

**O que é**: Abordagem que avalia capacidade demonstrada de realizar tarefas específicas, não apenas conhecimento teórico.

**Princípios**:
- Avaliação baseada em **performance** (o que o profissional sabe fazer)
- **Critérios claros** e públicos de proficiência
- **Evidências múltiplas** (não uma única prova)
- **Feedback formativo** (não apenas somativo)

**Aplicação no CarGuroo**:
- **Competências Definidas**: Cada área técnica tem rubrica detalhada
  - Ex: Competência "Diagnóstico de Sistema Elétrico" tem 10 sub-competências
- **Avaliação Multimodal**:
  - Questões situacionais (conhecimento aplicado)
  - Histórico de uso do Copiloto (performance real)
  - Taxa de resolução e retrabalho (outcomes)
- **Rubricas de Pontuação**:
  - Cada questão tem rubrica de 4 níveis (Inadequado/Parcial/Adequado/Excelente)
  - Scoring holístico + analítico
- **Feedback Formativo**:
  - Mecânico recebe feedback detalhado pós-avaliação
  - Recomendações personalizadas de desenvolvimento

**Referência**: Gonczi, A. (1994). "Competency based assessment in the professions in Australia". *Assessment in Education: Principles, Policy & Practice*, 1(1), 27-44.

---

#### 3. **Item Response Theory (IRT)** - Teoria de Resposta ao Item

**O que é**: Modelo estatístico moderno que avalia proficiência do indivíduo e dificuldade de cada questão independentemente.

**Vantagens sobre avaliação clássica**:
- **Adaptive Testing**: Questões ajustadas ao nível do avaliado em tempo real
- **Comparabilidade**: Proficiências comparáveis mesmo em provas diferentes
- **Precisão**: Estima proficiência verdadeira com erro padrão
- **Detecção de Chute**: Identifica padrões inconsistentes

**Aplicação no CarGuroo**:
- **Banco de Itens Calibrados**:
  - Cada questão tem parâmetros estimados: dificuldade, discriminação, chute
  - Calibração inicial com amostra de 100+ mecânicos
- **Avaliação Adaptativa** (Fase Futura):
  - Sistema ajusta dificuldade com base em respostas anteriores
  - Reduz tempo de prova mantendo precisão
- **Equating de Provas**:
  - Diferentes ciclos de avaliação são comparáveis
  - Permite tracking longitudinal confiável

**Referência**: Embretson, S. E., & Reise, S. P. (2000). *Item response theory for psychologists*. Lawrence Erlbaum Associates.

---

#### 4. **Modelo de Kirkpatrick** (Avaliação de Treinamento)

**O que é**: Framework de 4 níveis para avaliar eficácia de programas de treinamento.

**4 Níveis**:
1. **Reação**: Satisfação do participante com o treinamento
2. **Aprendizado**: Aquisição de conhecimentos/habilidades
3. **Comportamento**: Aplicação no trabalho (transfer)
4. **Resultados**: Impacto nos KPIs de negócio

**Aplicação no CarGuroo**:
- **Nível 1 (Reação)**: NPS pós-avaliação
- **Nível 2 (Aprendizado)**: Melhoria em score de avaliação (pre-post training)
- **Nível 3 (Comportamento)**: Aumento de uso do Copiloto, redução de chamados help desk
- **Nível 4 (Resultados)**: Redução de tempo de reparo, diminuição de retrabalho

**Uso**: Medir ROI de investimentos em capacitação direcionada baseada em gaps identificados.

**Referência**: Kirkpatrick, D. L., & Kirkpatrick, J. D. (2006). *Evaluating training programs: The four levels*. Berrett-Koehler Publishers.

---

#### 5. **Rubrics and Criterion-Referenced Scoring**

**O que é**: Sistema de pontuação baseado em critérios objetivos pré-definidos, não em comparação com outros (norm-referenced).

**Componentes de uma Rubrica**:
- **Dimensões**: Aspectos a serem avaliados
- **Níveis**: Graus de proficiência (ex: 1-4)
- **Descritores**: Descrição clara do desempenho em cada nível

**Exemplo de Rubrica para Questão Situacional**:

**Dimensão: Diagnóstico de Problema Elétrico**

| Nível | Descritor |
|-------|-----------|
| **1 - Inadequado** | Não identifica possíveis causas ou sugere ações irrelevantes |
| **2 - Parcial** | Identifica 1-2 causas possíveis, mas abordagem desorganizada |
| **3 - Adequado** | Identifica principais causas e propõe sequência lógica de verificações |
| **4 - Excelente** | Diagnóstico sistemático, considera múltiplas hipóteses, prioriza por probabilidade |

**Aplicação no CarGuroo**:
- **Rubricas por Competência**: Cada área técnica tem rubrica específica
- **Correção por IA**: LLM avalia resposta contra rubrica
- **Validação Humana**: Especialistas revisam amostra (10-20%) para calibração
- **Transparência**: Mecânicos têm acesso às rubricas antes da avaliação

**Referência**: Brookhart, S. M. (2013). *How to create and use rubrics for formative assessment and grading*. ASCD.

---

### Framework de Classificação e Thresholds

**Definição de Níveis Baseada em Evidências**:

#### **Fase 2: Qualificação Geral**

| Nível | Score Range | Critérios |
|-------|-------------|-----------|
| **Iniciante** | 0-69% | - Conhecimento básico<br>- Requer supervisão frequente<br>- Aplica procedimentos com apoio<br>- Níveis cognitivos 1-2 (Bloom) |
| **Adequado** | 70-84% | - Autonomia em tarefas comuns<br>- Supervisão ocasional<br>- Aplica e analisa consistentemente<br>- Níveis cognitivos 3-4 (Bloom) |
| **Experiente** | 85-100% | - Autonomia completa<br>- Capaz de orientar outros<br>- Resolve problemas complexos<br>- Níveis cognitivos 4-6 (Bloom) |

**Calibração de Thresholds**:
- Thresholds iniciais baseados em literatura (padrão Angoff modificado)
- Ajuste após primeiros 3 meses com dados reais
- Validação com especialistas (critério externo)

#### **Fase 3: Especialização por Área**

| Nível | Score Range | Critérios |
|-------|-------------|-----------|
| **Sem Qualificação** | 0-59% | Não deve trabalhar nessa área sem treinamento |
| **Qualificado** | 60-84% | Executa serviços básicos com supervisão ocasional |
| **Especialista** | 85-100% | Autonomia completa, referência técnica para outros |

---

### Garantia de Validade e Confiabilidade

**1. Validade de Conteúdo**:
- Questões desenvolvidas com base em análise de tarefas (job task analysis)
- Revisão por painel de especialistas (mecânicos seniores + engenheiros)
- Alinhamento com manuais técnicos oficiais

**2. Validade de Construto**:
- Correlação entre scores de avaliação e performance real (uso Copiloto, taxa resolução)
- Análise fatorial confirmatória (dimensionalidade das competências)

**3. Confiabilidade**:
- **Consistência Interna**: Alfa de Cronbach > 0.80
- **Inter-rater Reliability**: Kappa > 0.75 (concordância entre IA e especialistas)
- **Test-retest Reliability**: Correlação > 0.85 (avaliações separadas por 2 semanas)

**4. Fairness e Bias Mitigation**:
- Análise de DIF (Differential Item Functioning) por concessionária/região
- Revisão de viés linguístico/cultural
- Monitoramento de taxas de aprovação por grupo demográfico

---

### Material de Avaliação: Estrutura e Geração

**Banco de Itens Estruturado**:

```
Banco de Itens
│
├── Fase 1: Entrada
│   ├── Fundamentos de Mecânica (30 itens)
│   ├── Segurança e Procedimentos (20 itens)
│   └── Diagnóstico Básico (25 itens)
│
├── Fase 2: Qualificação Geral
│   ├── Nível Iniciante (50 itens)
│   ├── Nível Adequado (75 itens)
│   └── Nível Experiente (100 itens)
│
└── Fase 3: Especialização
    ├── Elétrica e Eletrônica (60 itens)
    ├── Mecânica de Motor (60 itens)
    ├── Sistemas de Tração (50 itens)
    ├── Sistemas de Freios (50 itens)
    ├── Suspensão e Direção (50 itens)
    ├── Sistemas Híbridos/Elétricos (60 itens)
    └── Diagnóstico Avançado (70 itens)
```

**Processo de Geração de Itens**:

1. **Curadoria Humana + IA**:
   - Especialistas definem competências e cenários
   - IA gera primeira versão de questões situacionais
   - Especialistas revisam, refinam e calibram

2. **Formato de Questões**:
   - **Questões Situacionais**: "Você recebe um veículo com [sintomas]. Descreva seu processo de diagnóstico."
   - **Questões de Análise**: "Analise estes códigos de erro. Qual a causa raiz mais provável?"
   - **Questões de Decisão**: "Dados estes dados, qual ação você recomendaria e por quê?"

3. **Metadata de Cada Item**:
   - ID único
   - Área técnica e sub-competência
   - Nível cognitivo (Bloom)
   - Dificuldade estimada (IRT)
   - Rubrica de correção
   - Tempo médio de resposta

4. **Pilotagem e Calibração**:
   - Novos itens são pilotados com amostra (n=50)
   - Parâmetros IRT são estimados
   - Itens problemáticos são revisados ou descartados

**Exemplo de Item com Metadata Completa**:

```yaml
item_id: "ELET-DIAG-043"
area: "Elétrica e Eletrônica"
subcompetencia: "Diagnóstico de Falhas em Sistema de Ignição"
nivel_cognitivo: "Analisar" # Bloom nível 4
dificuldade_irt: 1.2 # escala logit
discriminacao_irt: 1.8
fase: "Fase 3 - Especialização"
nivel_target: "Especialista"

questao: |
  Um veículo apresenta dificuldade de partida intermitente, principalmente em dias frios.
  O scanner não mostra códigos de erro. O cliente relata que às vezes o motor "engasga"
  antes de dar partida. A bateria está em boas condições (testada).

  Descreva sua estratégia de diagnóstico, incluindo:
  1. Hipóteses iniciais (ranqueadas por probabilidade)
  2. Sequência de verificações que você realizaria
  3. Justificativa técnica para cada verificação

rubrica:
  inadequado: "Não formula hipóteses claras ou sugere verificações aleatórias"
  parcial: "Formula 1-2 hipóteses mas falta sistematização na abordagem"
  adequado: "Hipóteses coerentes, sequência lógica, mas falta profundidade técnica"
  excelente: "Diagnóstico diferencial completo, abordagem sistemática, justificativas técnicas sólidas"

tempo_medio: 8 # minutos
```

---

### Referências Científicas Completas

1. **Anderson, L. W., & Krathwohl, D. R.** (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. New York: Longman.

2. **Embretson, S. E., & Reise, S. P.** (2000). *Item response theory for psychologists*. Mahwah, NJ: Lawrence Erlbaum Associates.

3. **Gonczi, A.** (1994). Competency based assessment in the professions in Australia. *Assessment in Education: Principles, Policy & Practice*, 1(1), 27-44.

4. **Kirkpatrick, D. L., & Kirkpatrick, J. D.** (2006). *Evaluating training programs: The four levels* (3rd ed.). San Francisco: Berrett-Koehler Publishers.

5. **Brookhart, S. M.** (2013). *How to create and use rubrics for formative assessment and grading*. Alexandria, VA: ASCD.

6. **Mislevy, R. J., Almond, R. G., & Lukas, J. F.** (2003). A brief introduction to evidence-centered design. *ETS Research Report Series*, 2003(1), i-29.

7. **Schuwirth, L. W., & Van der Vleuten, C. P.** (2011). Programmatic assessment: From assessment of learning to assessment for learning. *Medical Teacher*, 33(6), 478-485.

8. **Messick, S.** (1995). Validity of psychological assessment: Validation of inferences from persons' responses and performances as scientific inquiry into score meaning. *American Psychologist*, 50(9), 741.

---

## Target Users

### Primary User Segment

**Mecânicos de Concessionárias Autorizadas**

**Perfil Demográfico/Profissional**:
- Profissionais técnicos trabalhando em rede de concessionárias autorizadas no Brasil
- Níveis variados: mecânicos júnior (aprendizes), plenos (experientes), seniores (especialistas)
- Distribuídos geograficamente por todo território nacional
- Milhares de profissionais por grande montadora

**Comportamento Atual**:
- Consultam manuais técnicos físicos ou PDFs extensos durante diagnósticos
- Acionam help desk via telefone/e-mail quando encontram problemas complexos
- Aguardam dias por respostas assíncronas do suporte técnico
- Dependem de conhecimento tácito e experiência pessoal
- Realizam diagnósticos por tentativa e erro em casos complexos

**Dores Específicas**:
- 😣 Frustração com tempo gasto buscando informações em manuais extensos
- 😣 Pressão por reduzir tempo de reparo (KPI de produtividade)
- 😣 Insegurança ao lidar com modelos novos ou sistemas complexos
- 😣 Retrabalho quando diagnóstico inicial está incorreto
- 😣 Demora no suporte de help desk impacta sua produtividade

**Objetivos/Metas**:
- 🎯 Diagnosticar problemas rapidamente e com precisão
- 🎯 Executar reparos corretos na primeira tentativa
- 🎯 Reduzir tempo de imobilização do veículo
- 🎯 Aumentar produtividade pessoal (mais carros atendidos)
- 🎯 Desenvolver conhecimento técnico continuamente

**Motivação para Adoção**:
- ✅ Resposta imediata às dúvidas técnicas (vs. dias de espera)
- ✅ Redução de estresse e aumento de confiança no diagnóstico
- ✅ Reconhecimento profissional via sistema de classificação
- ✅ Interface simples e familiar (conversacional, como WhatsApp)

### Secondary User Segment

**Gestores de Pós-Venda e Alta Gestão de Montadoras**

**Perfil Demográfico/Profissional**:
- Gerentes de pós-venda de concessionárias
- Diretores regionais e nacionais de pós-venda de montadoras
- Responsáveis por qualidade, treinamento e eficiência operacional
- Gestores de centenas a milhares de mecânicos distribuídos

**Comportamento Atual**:
- Monitoram métricas de eficiência (tempo de reparo, taxa de retorno, NPS)
- Planejam treinamentos genéricos sem visibilidade de gaps reais
- Lidam com custos elevados de help desk e retrabalho
- Alocam mecânicos sem conhecimento preciso de competências individuais
- Recebem reclamações de clientes sobre qualidade inconsistente

**Dores Específicas**:
- 😣 Falta de visibilidade de competências dos mecânicos em escala
- 😣 Impossibilidade de medir eficácia de treinamentos
- 😣 Custos operacionais elevados (help desk, retrabalho)
- 😣 Qualidade inconsistente do pós-venda impacta NPS e fidelização
- 😣 Dificuldade em demonstrar ROI de investimentos em capacitação

**Objetivos/Metas**:
- 🎯 Reduzir custos operacionais de pós-venda
- 🎯 Aumentar qualidade e consistência do atendimento
- 🎯 Ter visibilidade completa de competências da equipe
- 🎯 Direcionar treinamentos de forma assertiva e mensurável
- 🎯 Melhorar NPS e fidelização de clientes pós-garantia

**Motivação para Adoção**:
- ✅ Dashboard de competências em tempo real
- ✅ ROI mensurável (redução de custos + aumento de qualidade)
- ✅ Capacidade de responder rapidamente a problemas (ex: anomalias em lote de peças)
- ✅ Vantagem competitiva via qualidade superior de pós-venda

---

## Goals and Success Metrics

### Business Objectives

**Para Montadoras e Concessionárias (Cliente B2B)**:

1. **Reduzir custos operacionais de pós-venda em 20-30% no primeiro ano**
   - Redução de chamados de help desk em 70%
   - Diminuição de custos de retrabalho em 25%
   - Otimização de tempo de mecânicos (30% mais rápido)

2. **Aumentar qualidade e fidelização de clientes finais**
   - Elevar NPS de pós-venda em 15+ pontos
   - Reduzir taxa de retorno (problema não resolvido) em 50%
   - Aumentar taxa de retorno de clientes pós-garantia em 20%

3. **Ganhar visibilidade estratégica de competências**
   - 100% dos mecânicos mapeados por competência em 6 meses
   - Reduzir gaps de conhecimento críticos em 40% em 12 meses
   - Aumentar eficácia de treinamentos (ROI mensurável)

4. **Diferenciar marca via experiência de pós-venda**
   - Posicionar como referência em qualidade de pós-venda
   - Criar vantagem competitiva sustentável
   - Aumentar valor de marca (brand equity)

**Para o CarGuroo (Produto)**:

1. **Validar produto com cliente piloto (montadora brasileira - 450 mecânicos) em 6 meses**
2. **Atingir 70%+ de adoção ativa no cliente piloto em 9 meses**
3. **Expandir para 2-3 montadoras adicionais baseado em case de sucesso em 18-24 meses**
4. **Atingir 2.000+ mecânicos ativos na plataforma em 24 meses**
5. **Alcançar NRR (Net Revenue Retention) >120% após consolidação do piloto**

### User Success Metrics

**Para Mecânicos (Usuário Primário)**:

1. **Eficiência no Diagnóstico**
   - Tempo médio de diagnóstico reduzido em 30%
   - Taxa de resolução na primeira tentativa aumentada para 90%
   - Redução de 70% no uso de help desk tradicional

2. **Adoção e Engajamento**
   - 80% dos mecânicos usam Copiloto semanalmente
   - Média de 15+ interações por mecânico/semana
   - NPS de mecânicos >50

3. **Desenvolvimento Profissional**
   - 70% dos mecânicos completam ciclos de avaliação no prazo
   - Progressão mensurável em classificação de senioridade (Junior → Pleno → Sênior)
   - Satisfação com sistema de capacitação >4.5/5

**Para Gestores (Usuário Secundário)**:

1. **Visibilidade e Controle**
   - 100% de visibilidade de competências da equipe
   - Tempo de resposta a anomalias críticas <24h
   - Dashboards acessados >3x por semana

2. **Impacto em Treinamento**
   - ROI de treinamentos mensurável e >200%
   - Redução de 50% em custos de treinamento genérico
   - Aumento de 40% em eficácia de capacitação

### Key Performance Indicators (KPIs)

**KPIs de Produto (North Star)**:

1. **Mecânicos Ativos Semanais (WAU) - Cliente Piloto**
   - Baseline (Mês 0): 0
   - Meta Mês 3: 200+ (45% dos 450)
   - Meta Mês 6: 315+ (70% dos 450)
   - Meta Mês 12: 360+ (80% dos 450)

2. **Interações Copiloto por Mecânico Ativo/Semana**
   - Meta Mês 3: 5+ interações (early adopters)
   - Meta Mês 6: 10+ interações
   - Meta Mês 12: 15+ interações (uso consolidado)

3. **Taxa de Resolução na Primeira Tentativa**
   - Baseline: ~50% (estado atual do cliente piloto)
   - Meta Mês 6: 70% (melhoria de 20pp)
   - Meta Mês 12: 90% (melhoria de 40pp)

4. **Cobertura de Avaliação (450 Mecânicos)**
   - Meta Mês 3: 100% avaliados (baseline estabelecido)
   - Meta Mês 6: 2º ciclo completo (tracking de evolução)
   - Meta Mês 12: 4 ciclos completos (tendência clara de desenvolvimento)

**KPIs de Impacto de Negócio (Cliente B2B)**:

1. **Redução de Tempo Médio de Reparo**
   - Meta: -30% vs. baseline

2. **Redução de Custos de Retrabalho**
   - Meta: -25% vs. baseline

3. **Redução de Chamados de Help Desk**
   - Meta: -70% vs. baseline

4. **NPS de Pós-Venda do Cliente Final**
   - Meta: +15 pontos vs. baseline

5. **Cobertura de Mapeamento de Competências**
   - Meta: 100% dos mecânicos mapeados em 6 meses

**KPIs de Eficiência de Produto**:

1. **Tempo Médio de Resposta do Copiloto**
   - Meta: <3 segundos (95th percentile)

2. **Acurácia de Diagnóstico Sugerido**
   - Meta: >85% de diagnósticos confirmados como corretos

3. **Taxa de Conclusão de Avaliações**
   - Meta: >70% dos mecânicos completam no prazo

---

## Strategic Alignment and Financial Impact

### Financial Impact

**Modelo de Receita: SaaS B2B por Mecânico Ativo**

- **Pricing**: R$ 150-300/mecânico/mês (volume-based pricing)
- **Cliente Piloto Confirmado**: Montadora brasileira com 450 mecânicos em 30 concessionárias
- **ARR Projetado Cliente Piloto**: R$ 810K - 1.6M/ano (450 mecânicos × R$ 150-300/mês × 12 meses)
- **Target Expansão**: 2-3 montadoras adicionais em 18-24 meses → 2.000+ mecânicos totais
- **ARR Projetado Ano 3**: R$ 3.6-7.2M (2.000 mecânicos × R$ 150-300/mês × 12 meses)
- **Margem Bruta Esperada**: 70-80% (modelo SaaS típico após escala)

**ROI para o Cliente Piloto (Montadora com 450 Mecânicos)**:

Assumindo custos atuais totais da montadora:

**Custos Atuais Estimados (Anual para 450 Mecânicos)**:
- Help desk: R$ 2.7M/ano (equipe de atendimento + infraestrutura + gestão)
- Retrabalho: R$ 1.8M/ano (estimativa conservadora baseada em taxa de retorno)
- Ineficiência (tempo perdido): R$ 3.6M/ano (30% do tempo × custo de mecânico × 450 profissionais)
- **Total**: ~R$ 8.1M/ano

**Investimento no CarGuroo**:
- R$ 150/mecânico/mês × 450 mecânicos × 12 meses = **R$ 810K/ano**
- (Ou R$ 1.6M/ano no cenário de R$ 300/mecânico/mês)

**Economia Esperada**:
- Help desk: -70% = R$ 1.89M
- Retrabalho: -25% = R$ 450K
- Eficiência: -30% de tempo = R$ 1.08M
- **Total Economia**: R$ 3.42M/ano

**ROI (Cenário Conservador - R$ 150/mec/mês)**:
- **(R$ 3.42M - R$ 810K) / R$ 810K = 322% no primeiro ano**
- **Payback: ~3 meses**

**ROI (Cenário Premium - R$ 300/mec/mês)**:
- **(R$ 3.42M - R$ 1.6M) / R$ 1.6M = 113% no primeiro ano**
- **Payback: ~6 meses**

**Valor Intangível Adicional**:
- Aumento de NPS e fidelização pós-garantia
- Fortalecimento de marca (qualidade de pós-venda)
- Vantagem competitiva sustentável

### Company Objectives Alignment

**Alinhamento com Objetivos Estratégicos de Montadoras**:

1. **Redução de Custos Operacionais**
   - Pressão contínua por eficiência em toda cadeia automotiva
   - CarGuroo reduz custos de forma mensurável e sustentável

2. **Qualidade e Satisfação do Cliente**
   - NPS de pós-venda é métrica crítica para fidelização
   - Qualidade consistente fortalece valor de marca

3. **Transformação Digital**
   - Montadoras buscam digitalização de operações
   - IA generativa é prioridade estratégica em várias organizações

4. **Capacitação e Retenção de Talentos**
   - Dificuldade em reter mecânicos qualificados
   - Sistema de desenvolvimento profissional melhora engajamento

5. **Diferenciação Competitiva**
   - Mercado automotivo altamente competitivo
   - Experiência superior de pós-venda é diferencial sustentável

### Strategic Initiatives

**Iniciativas Estratégicas que o CarGuroo Viabiliza**:

1. **Centro de Excelência em Pós-Venda**
   - Criar padrão de excelência em qualidade de serviço
   - Benchmark interno e externo de performance

2. **Academia Digital de Capacitação**
   - Programa contínuo de desenvolvimento técnico
   - Certificação por competências (vs. tempo de casa)

3. **Programa de Customer Success Pós-Venda**
   - Engajamento proativo com clientes pós-garantia
   - Redução de churn para oficinas não autorizadas

4. **Data-Driven Service Optimization**
   - Decisões baseadas em dados reais de diagnósticos
   - Identificação de problemas sistêmicos em peças/modelos

---

## MVP Scope

### Core Features (Must Have)

**Copiloto do Mecânico (MVP)**:

1. **Interface Conversacional Básica**
   - ✅ Chat via WhatsApp Business API ou Web App
   - ✅ Suporte a texto e áudio (input)
   - ✅ Respostas em texto formatado (output)
   - ❌ Vídeo fica para v2

2. **RAG sobre Base de Conhecimento**
   - ✅ Ingestão de manuais técnicos (PDF)
   - ✅ Histórico de help desk (se disponível)
   - ✅ Busca semântica via embeddings
   - ✅ Citação de fontes nas respostas
   - ❌ Processamento de vídeos/áudios fica para v2

3. **Diagnóstico Assistido**
   - ✅ Fluxo guiado de perguntas (sintomas → diagnóstico)
   - ✅ Sugestões de próximos passos
   - ✅ Histórico de interações por veículo/OS
   - ❌ Análise de imagens (fotos de peças) fica para v2

4. **Integração Básica**
   - ✅ SSO com sistema da concessionária
   - ✅ Cadastro de mecânicos
   - ✅ Associação com OS (ordem de serviço)
   - ❌ Integração bidirecional completa fica para v2

**Avaliação de Mecânico (MVP)**:

1. **Criação de Ciclos de Avaliação**
   - ✅ Interface de gestão (web)
   - ✅ Geração de perguntas via IA (baseadas em tópicos)
   - ✅ Definição de período e público-alvo

2. **Execução de Avaliações**
   - ✅ Mecânico responde via chat (texto/áudio)
   - ✅ Correção automatizada via IA
   - ✅ Classificação em níveis (Inadequado/Junior/Pleno/Sênior)

3. **Dashboard de Competências**
   - ✅ Visão agregada: % por nível de conhecimento
   - ✅ Drill-down: competências individuais por mecânico
   - ✅ Identificação de gaps críticos
   - ❌ Recomendações automáticas de treinamento fica para v2

**Infraestrutura e Admin (MVP)**:

1. **Gestão de Usuários**
   - ✅ Cadastro de montadora/concessionária
   - ✅ Cadastro de gestores e mecânicos
   - ✅ Permissões básicas (admin, gestor, mecânico)

2. **Processamento de Conhecimento**
   - ✅ Upload de manuais técnicos (PDF)
   - ✅ Processamento batch (chunking + embedding)
   - ✅ Indexação em vector database

3. **Observabilidade**
   - ✅ Logs de interações
   - ✅ Métricas básicas (uso, latência)
   - ❌ Analytics avançado fica para v2

### Out of Scope for MVP

**Funcionalidades Importantes mas NÃO Críticas para Validação Inicial**:

1. **Copiloto do Motorista** (cliente final)
   - Toda interface para proprietários de veículos
   - Decisão estratégica: foco total em B2B primeiro

2. **Multimodalidade Completa**
   - Análise de imagens (fotos de peças danificadas)
   - Análise de vídeos de demonstração de problemas
   - Transcrição de áudios longos

3. **Integrações Profundas**
   - Sincronização bidirecional com DMS (Dealer Management System)
   - Leitura de dados de telemetria de veículos
   - Integração com sistemas de estoque

4. **Features Avançadas de Avaliação**
   - Recomendação automática de trilhas de capacitação
   - Gamificação (badges, rankings)
   - Avaliação adaptativa (questões ajustadas em tempo real)

5. **Analytics e Inteligência de Negócio**
   - Dashboards executivos avançados
   - Predição de problemas recorrentes
   - Benchmarking entre concessionárias

6. **Mobile Apps Nativos**
   - MVP usa web responsivo + WhatsApp
   - Apps nativos iOS/Android ficam para v2

### MVP Success Criteria

**Critérios Objetivos para Declarar MVP Bem-Sucedido**:

**Adoção**:
- ✅ 60%+ dos mecânicos piloto usam Copiloto semanalmente
- ✅ Média de 8+ interações por mecânico/semana
- ✅ 70%+ completam ciclo de avaliação no prazo

**Impacto Mensurável** (vs. baseline pré-MVP):
- ✅ 20%+ de redução em tempo médio de diagnóstico
- ✅ 15%+ de aumento em taxa de resolução na primeira tentativa
- ✅ 50%+ de redução em chamados de help desk

**Satisfação**:
- ✅ NPS de mecânicos >40
- ✅ NPS de gestores >50
- ✅ <10% de churn de usuários ativos mensais

**Viabilidade Técnica**:
- ✅ Latência p95 <5 segundos
- ✅ Acurácia de respostas >75% (validada por especialistas)
- ✅ Uptime >99%

**Validação de Negócio**:
- ✅ Cliente piloto renova para fase 2
- ✅ ROI demonstrado >200%
- ✅ 2+ leads qualificados gerados por referência

---

## Post-MVP Vision

### Phase 2 Features (6-12 meses pós-MVP)

**Expansão de Copiloto do Mecânico**:

1. **Multimodalidade Completa**
   - Análise de imagens: fotos de peças, códigos de erro no painel
   - Processamento de vídeos: demonstrações de problemas
   - Output em áudio (respostas faladas)

2. **Integração Profunda com DMS**
   - Sincronização bidirecional com sistema de OS
   - Criação automática de diagnósticos no DMS
   - Acesso a histórico completo do veículo

3. **Assistente Proativo**
   - Sugestões automáticas baseadas em padrões
   - Alertas de recalls ou anomalias conhecidas
   - Checklist inteligente pré-serviço

**Expansão de Avaliação**:

1. **Trilhas de Capacitação Personalizadas**
   - Recomendação automática de treinamentos baseada em gaps
   - Conteúdo gerado por IA (microlearning)
   - Avaliação contínua (não apenas cíclica)

2. **Alocação Inteligente de Serviços**
   - Sugestão automática de mecânico ideal para cada OS
   - Balanceamento de carga considerando competências
   - Priorização de desenvolvimento (mecânicos promissores)

**Infraestrutura e Escala**:

1. **Analytics Avançado**
   - Dashboards executivos (C-level)
   - Predição de problemas recorrentes
   - Benchmarking inter-concessionárias

2. **Mobile Apps Nativos**
   - iOS e Android
   - Modo offline (sincronização posterior)

### Long-term Vision (1-2 anos)

**Copiloto do Motorista (Expansão B2C)**:

- Interface para proprietários de veículos
- Diagnóstico pré-agendamento
- Concierge de pós-venda end-to-end
- Integração com aplicativos da montadora

**Ecossistema Integrado**:

- Conectar motoristas ↔ concessionárias ↔ montadoras
- Visibilidade completa da jornada de pós-venda
- Comunicação proativa e personalizada
- Marketplace de serviços adicionais

**Expansão de Valor**:

- **Locadoras**: Gestão de frota especializada
- **Seguradoras**: Avaliação de sinistros mais precisa
- **Oficinas Multimarcas**: Versão adaptada
- **Peças e Acessórios**: Cross-sell inteligente

**Inteligência de Produto**:

- Feedback loop: problemas recorrentes → montadora
- Dados agregados para melhoria de produtos
- Identificação de oportunidades de inovação

### Expansion Opportunities

**Expansão Geográfica**:
- Brasil (foco inicial)
- América Latina (Argentina, México, Chile)
- Europa e EUA (adaptação regulatória)

**Expansão Vertical**:
- Caminhões e veículos pesados
- Equipamentos agrícolas (tratores, colheitadeiras)
- Equipamentos de construção

**Expansão Horizontal**:
- Outras indústrias com rede de assistência técnica:
  - Eletrodomésticos
  - Eletrônicos (smartphones, notebooks)
  - Equipamentos industriais

---

## Technical Considerations

### Platform Requirements

**Frontend**:
- **Web App (Gestores)**: SPA responsivo, compatível com Chrome, Edge, Safari
- **Interface Conversacional (Mecânicos)**:
  - Opção 1 (MVP): WhatsApp Business API
  - Opção 2 (Alternativa): Web chat embeddable
  - Futuro: Apps nativos iOS/Android

**Acessibilidade**:
- WCAG 2.1 Level AA (interface web)
- Suporte a leitores de tela (importante para gestores)

**Performance**:
- Latência p95 <5s para respostas do Copiloto
- Suporte a 1.000+ usuários simultâneos (escala inicial)
- Disponibilidade 99.5% (SLA MVP)

### Technology Preferences

**Backend/API**:
- **Linguagem**: Python (ecossistema IA/ML robusto)
- **Framework**: FastAPI (performance + async + validação)
- **LLM**: OpenAI GPT-4 ou Claude (Anthropic) via API
  - Avaliação futura de modelos open-source (custo)

**Processamento de Documentos & RAG**:
- **Vector Database**: Pinecone, Weaviate ou Qdrant
- **Embeddings**: OpenAI text-embedding-ada-002 ou equivalente
- **Chunking/Processing**: LangChain ou LlamaIndex
- **OCR**: Azure Document Intelligence ou Google Cloud Vision

**Banco de Dados**:
- **Relacional (dados estruturados)**: PostgreSQL
- **Vetorial (embeddings)**: Conforme escolha acima
- **Cache**: Redis (sessões, rate limiting)

**Infraestrutura**:
- **Cloud**: AWS ou Google Cloud (preferência do cliente)
- **Containers**: Docker + Kubernetes (escala horizontal)
- **CI/CD**: GitHub Actions
- **Observability**: DataDog ou New Relic

**Integrações**:
- **WhatsApp**: Meta Business API (oficial)
- **SSO**: SAML 2.0 / OAuth 2.0
- **DMS**: APIs REST (custom por montadora)

### Architecture Considerations

**Arquitetura de Alto Nível**:

```
[Mecânico] → [WhatsApp/Web Chat]
                ↓
          [API Gateway]
                ↓
    [Conversational Service]
                ↓
        [LLM Orchestrator]
          /           \
   [Vector DB]    [Knowledge Base]
   (RAG Search)   (Manuais, HD, etc.)
                ↓
        [Response Builder]
                ↓
      [Integration Layer]
                ↓
   [DMS/ERP Montadora]
```

**Decisões Arquiteturais Críticas**:

1. **Stateless API**
   - Escalabilidade horizontal
   - Sessões em Redis

2. **Processamento Assíncrono**
   - Upload/processamento de documentos via fila (Celery/RabbitMQ)
   - Não bloqueia requests

3. **Rate Limiting por Tenant**
   - Evitar abuso de API LLM
   - Controle de custos

4. **Multi-tenancy**
   - Isolamento de dados por montadora
   - Schema compartilhado com tenant_id

5. **Observabilidade como Requisito**
   - Logs estruturados
   - Distributed tracing (cada request tem trace_id)
   - Métricas de negócio + técnicas

---

## Constraints and Assumptions

### Constraints

**Orçamento e Recursos**:
- Orçamento de desenvolvimento MVP: [A DEFINIR COM STAKEHOLDERS]
- Time técnico: [A DEFINIR]
- Prazo de lançamento MVP: 4-6 meses

**Tecnológicos**:
- Dependência de APIs de terceiros (OpenAI, WhatsApp)
- Custos de LLM podem variar significativamente com volume
- Qualidade da IA depende da qualidade dos manuais técnicos fornecidos

**Regulatórios e Compliance**:
- LGPD: Dados de mecânicos e interações são dados pessoais
- Dados de proprietários de veículos (se incluídos): cuidado extra
- Compliance com políticas de dados da montadora

**Dependências Externas**:
- Acesso às bases de conhecimento da montadora (manuais, help desk)
- Integração com sistemas legados (DMS)
- Aprovação de montadora para homologação/piloto

### Key Assumptions

**Fatos Confirmados (Não São Mais Assumições)**:
- ✅ **CONFIRMADO**: Montadora brasileira já comprometida (450 mecânicos, 30 concessionárias)
- ✅ **CONFIRMADO**: Acesso a dados reais e ambiente de produção garantido
- ✅ **CONFIRMADO**: Gestores da montadora apoiam ativamente (top-down confirmado)
- ✅ **CONFIRMADO**: Legado de 450 mecânicos sem baseline formal de avaliação

**Sobre o Problema (A Validar com Cliente Piloto)**:
- ⚠️ Mecânicos realmente sofrem com acesso lento a informações (validar em campo)
- ⚠️ Gestores realmente não têm visibilidade de competências (confirmar escala do problema)
- ⚠️ ROI de 200-300%+ é suficiente para justificar adoção (validar com CFO)

**Sobre a Solução (A Validar em POC/Piloto)**:
- ⚠️ IA generativa atual é capaz de fornecer respostas técnicas precisas no contexto automotivo específico
- ⚠️ Interface conversacional é adequada para mecânicos (vs. dashboard tradicional) - testar em piloto restrito
- ⚠️ Classificação automatizada de conhecimento é confiável o suficiente (validar inter-rater reliability com especialistas)

**Sobre o Mercado (Parcialmente Validado)**:
- ✅ **CONFIRMADO**: Pelo menos 1 montadora está disposta a adotar solução SaaS externa
- ⚠️ Processo de venda B2B com outras montadoras levará 6-12 meses (ainda a validar)
- ⚠️ Piloto bem-sucedido levará a expansão para outras montadoras (hipótese a testar)

**Sobre Adoção (A Validar em Campo)**:
- ⚠️ Mecânicos têm smartphones ou acesso a computador nas 30 concessionárias (auditoria necessária)
- ⚠️ Mecânicos terão tempo durante serviço para interagir com Copiloto (validar workflow real)
- ⚠️ Resistência cultural pode ser superada com treinamento e benefícios claros (testar em piloto)

**Sobre Dados (A Auditar)**:
- ⚠️ Montadora parceira tem manuais técnicos digitalizados e acessíveis (confirmar formato e qualidade)
- ⚠️ Histórico de help desk está acessível e suficientemente estruturado (auditoria de dados necessária)
- ⚠️ Qualidade dos dados é suficiente para treinar RAG com acurácia >75% (POC técnico necessário)

**Sobre Integrações (Crítico - A Confirmar com TI)**:
- ⚠️ **CRÍTICO**: DMS da montadora permitirá integração (confirmar APIs disponíveis com TI)
- ⚠️ SSO é viável com sistemas da montadora (confirmar protocolos suportados)
- ⚠️ Não há restrições de compliance/segurança que impeçam solução cloud (confirmar com InfoSec)

**Sobre Pricing (A Validar)**:
- ⚠️ Pricing de R$ 150-300/mês por mecânico é aceitável (negociar com procurement)
- ⚠️ Estrutura de volume-based pricing faz sentido para cliente (validar preferência)

---

## Risks and Open Questions

### Key Risks

**Riscos de Adoção (ALTO IMPACTO)**:

1. **Resistência Cultural de Mecânicos**
   - **Risco**: Mecânicos seniores podem rejeitar "ser avaliados por IA"
   - **Mitigação**:
     - Posicionar como ferramenta de auxílio, não fiscalização
     - Envolver sindicatos/representantes desde início
     - Demonstrar benefícios claros (menos estresse, mais eficiência)
   - **Probabilidade**: Média-Alta

2. **Baixa Qualidade de Bases de Conhecimento**
   - **Risco**: Manuais desatualizados ou histórico de help desk incompleto
   - **Mitigação**:
     - Assessment prévio da qualidade dos dados
     - Processo de curadoria e enriquecimento
     - Feedback loop para melhorar continuamente
   - **Probabilidade**: Média

3. **Ciclo de Venda B2B Mais Longo que Esperado**
   - **Risco**: Montadoras podem levar 12-18 meses para decisão
   - **Mitigação**:
     - Pipeline robusto (5+ prospects para fechar 2)
     - POCs curtos e focados em quick wins
     - Champions internos na montadora
   - **Probabilidade**: Alta

**Riscos Técnicos (MÉDIO IMPACTO)**:

4. **Acurácia Insuficiente da IA**
   - **Risco**: Diagnósticos incorretos podem gerar desconfiança
   - **Mitigação**:
     - Human-in-the-loop: sugestões, não decisões finais
     - Feedback explícito ("foi útil?")
     - Melhoria contínua via fine-tuning
   - **Probabilidade**: Média

5. **Custos de LLM Acima do Esperado**
   - **Risco**: Volume alto pode tornar unidade economics insustentável
   - **Mitigação**:
     - Caching agressivo de respostas similares
     - Modelos menores para tarefas simples
     - Avaliação de modelos open-source
   - **Probabilidade**: Média

6. **Integrações Complexas com Sistemas Legados**
   - **Risco**: DMS antigos sem APIs, integração manual
   - **Mitigação**:
     - MVP sem integração bidirecional (apenas SSO)
     - Fase 2: integrações customizadas
     - Parceria com consultoria de integração
   - **Probabilidade**: Alta

**Riscos de Negócio (BAIXO-MÉDIO IMPACTO)**:

7. **Competição de Grandes Players**
   - **Risco**: Salesforce, Microsoft podem entrar nesse espaço
   - **Mitigação**:
     - Velocidade: ser primeiro e profundo
     - Especialização: conhecimento automotivo específico
     - Relacionamento: proximidade com montadoras
   - **Probabilidade**: Média (horizonte 18-24 meses)

8. **Dependência de Poucos Clientes Iniciais**
   - **Risco**: Churn de cliente piloto seria devastador
   - **Mitigação**:
     - Customer success dedicado
     - Co-criação (cliente como parceiro)
     - Contrato com fases (reduz risco de cancelamento abrupto)
   - **Probabilidade**: Média

### Open Questions

**Produto**:
- ❓ Qual a melhor interface para mecânicos: WhatsApp ou app dedicado?
- ❓ Como balancear automação vs. human-in-the-loop em diagnósticos críticos?
- ❓ Sistema de avaliação deve ser anônimo ou identificado?

**Go-to-Market**:
- ❓ Qual montadora abordar primeiro? (critério: abertura a inovação vs. tamanho)
- ❓ Modelo de pricing: por mecânico ativo ou por concessionária?
- ❓ Piloto gratuito ou pago desde início?

**Técnico**:
- ❓ LLM proprietário (OpenAI/Anthropic) ou open-source (Llama 3)?
- ❓ Hospedar em cloud pública ou exigência de on-premise?
- ❓ Dados de treinamento: usar apenas manuais ou incluir interações reais?

**Estratégia**:
- ❓ Quando expandir para Copiloto do Motorista (B2C)?
- ❓ Parceria estratégica com montadora ou manter independência?
- ❓ Foco em breadth (mais montadoras) ou depth (mais features para atual)?

### Areas Needing Further Research

**Pesquisa de Mercado**:
1. **Entrevistas em profundidade com mecânicos**
   - Validar dores e workflow atual
   - Testar protótipo de interface conversacional
   - Entender resistências e motivadores

2. **Análise de concorrência**
   - Mapeamento de soluções existentes (ServiceMax, UpKeep, etc.)
   - Diferenciação clara do CarGuroo
   - Análise de pricing de mercado

3. **Quantificação de ROI**
   - Dados reais de custos de help desk
   - Benchmarks de taxa de retorno
   - Business case com CFOs de concessionárias

**Pesquisa Técnica**:
1. **Benchmark de LLMs**
   - Acurácia em diagnósticos técnicos
   - Custo vs. performance
   - Latência em produção

2. **Arquitetura de RAG**
   - Chunking strategies para manuais técnicos
   - Embedding models (qualidade vs. custo)
   - Hybrid search (vetorial + keyword)

3. **Viabilidade de Integrações**
   - Auditoria de APIs de DMS principais
   - Esforço de integração estimado
   - Alternativas se API não disponível

**Compliance e Legal**:
1. **LGPD e Privacidade**
   - DPO review do fluxo de dados
   - DPIA (Data Protection Impact Assessment)
   - Políticas de retenção de dados

2. **Propriedade Intelectual**
   - Quem detém IP dos diagnósticos gerados?
   - Licenciamento de manuais técnicos
   - Uso de dados para melhorias do produto

---

## Appendices

### A. Research Summary

**Documentos Analisados**:
- Apresentação institucional CarGuroo (CARGURUOO_PT_BR.pdf)
- Discussões com stakeholders (Allan)
- Contexto de mercado pós-venda automotivo brasileiro

**Principais Insights**:

1. **Problema é Real e Quantificável**
   - Diagnósticos imprecisos levam a 50%+ de retorno
   - Help desk custa R$ 6K+/mês por concessionária
   - Tempo médio de reparo 30% acima do ideal

2. **Solução é Tecnicamente Viável**
   - IA generativa atual (GPT-4, Claude) capaz de diagnósticos técnicos
   - RAG sobre manuais técnicos é caso de uso validado
   - WhatsApp Business API viabiliza adoção rápida

3. **Mercado é Atrativo**
   - Dezenas de montadoras no Brasil
   - Milhares de mecânicos por montadora
   - Pós-venda representa 40-50% da receita de concessionárias

4. **ROI é Comprovável**
   - Economia mensurável em help desk, retrabalho e eficiência
   - Payback <6 meses
   - Benefícios intangíveis em NPS e fidelização

### B. Stakeholder Input

**Allan (Founder/Product Lead)**:
- Visão clara de produto e mercado
- Experiência em IA e integração de sistemas
- **Parceria estabelecida com montadora brasileira** (acesso a 450 mecânicos, 30 concessionárias)

**Montadora Parceira (Cliente Piloto) - CONFIRMADO**:
- **Escopo**: 450 mecânicos distribuídos em 30 concessionárias
- **Foco Inicial**: Concessionárias proprietárias (modelo próprio)
- **Comprometimento**: Acesso a dados reais, ambiente de produção, testes de campo
- **Tipo de Parceria**: Co-criação MVP com validação contínua
- **Desafio Específico**: 450 mecânicos já contratados sem baseline de avaliação formal

**Stakeholders do Cliente Piloto a Envolver**:
- Diretor de Pós-Venda (sponsor do projeto)
- Gerentes de concessionárias proprietárias (validação operacional)
- Mecânicos seniores (validação de solução e UX, co-criação de rubricas)
- CTO ou Head de TI (viabilidade de integração com DMS)
- Head de RH/Treinamento (processo de avaliação e desenvolvimento)
- CFO (validação de ROI e business case)

**Próximos Passos Críticos**:
1. **Workshop de Alinhamento** com stakeholders da montadora (definir prioridades e cronograma)
2. **Job Task Analysis** com mecânicos seniores (mapear competências por área técnica)
3. **Auditoria de Dados** (qualidade de manuais técnicos e histórico de help desk)
4. **Proof of Concept Técnico** (RAG sobre amostra de manuais, teste de correção por IA)
5. **Piloto Restrito** (1 concessionária, ~15 mecânicos) antes de rollout completo

### C. References

**Tecnologia**:
- OpenAI GPT-4 Technical Report
- LangChain Documentation (RAG patterns)
- WhatsApp Business Platform API Docs

**Mercado Automotivo**:
- FENABRAVE: Estatísticas de pós-venda no Brasil
- JD Power: Customer Satisfaction Index (CSI) - Service

**Produto e Estratégia**:
- "Crossing the Chasm" - Geoffrey Moore (adoção B2B)
- "The Mom Test" - Rob Fitzpatrick (customer discovery)

---

_This Product Brief serves as the foundational input for Product Requirements Document (PRD) creation._

_Next Steps: Handoff to Product Manager for PRD development using the `workflow prd` command._
