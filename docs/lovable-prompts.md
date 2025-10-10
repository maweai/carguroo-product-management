# CarGuroo - Prompts para Lovable.dev

**Projeto**: CarGuroo MVP
**Data**: 2025-10-10
**Autor**: Allan
**Referência**: ux-specification.md

---

## Contexto Global (Incluir em Todos os Prompts)

**Stack Tecnológico**:
- React 18 + TypeScript
- Tailwind CSS (utility-first)
- React Router v6 (navegação)
- React Query (server state)
- React Hook Form + Zod (formulários + validação)
- Chart.js + react-chartjs-2 (gráficos)

**Design System**:
- Font: Inter (Google Fonts)
- Cores primárias: Blue-600 (#2563eb), Green-600 (#16a34a)
- Espaçamento: 4px base unit (Tailwind default)
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)

**Acessibilidade**:
- WCAG 2.1 Level AA compliance
- Contraste mínimo 4.5:1 para texto
- Touch targets ≥ 44x44px
- Navegação completa por teclado
- ARIA labels em todos os componentes interativos

---

## Prompt 1: Dashboard Home (Gestores)

```
Crie um Dashboard Home para gestores de pós-venda automotivo usando React + TypeScript + Tailwind CSS.

CONTEXTO:
- Plataforma SaaS B2B para gestão de competências de mecânicos
- Usuário: Maria (gestora regional, 45 anos, gerencia 90 mecânicos em 6 concessionárias)
- Goal: Identificar gaps críticos e monitorar evolução da equipe em <2 minutos

LAYOUT (Desktop 1280px):

1. TOP NAVIGATION BAR (sticky, altura 64px):
   - Logo "CarGuroo" (esquerda)
   - Menu horizontal: [Dashboard] [Avaliações] [Competências] [Copiloto] [Config]
   - User menu (direita): Avatar + "Maria" + dropdown (Perfil, Logout)
   - Background: white, border-bottom gray-200

2. BREADCRUMB (abaixo do nav):
   - "Dashboard > Visão Geral"
   - Text sm, gray-600

3. KPIS ROW (4 cards horizontais):
   - Card 1: "90 Mecânicos" (total)
   - Card 2: "94% Taxa de Conclusão" (última avaliação)
   - Card 3: "72% Score Médio" (geral)
   - Card 4: "3 Gaps Críticos" (alerta em amber-500)
   - Cada card: bg-white, rounded-lg, shadow-sm, p-6
   - Ícone + número grande + label pequeno

4. CHARTS ROW (3 cards):

   Card A - Distribuição por Nível (Pie Chart):
   - Título: "Distribuição por Nível"
   - Chart.js Pie Chart com dados:
     * Iniciante: 20 mecânicos (22%, amber-500)
     * Adequado: 55 mecânicos (61%, green-600)
     * Experiente: 10 mecânicos (11%, blue-500)
   - Legenda abaixo do gráfico

   Card B - Gaps Críticos (Bar Chart):
   - Título: "Gaps Críticos por Competência"
   - Chart.js Horizontal Bar Chart:
     * Sistemas Elétricos: 60% (amber-500)
     * Diagnóstico Avançado: 35%
     * Motor Híbrido: 25%
   - Mostrar apenas top 3 gaps

   Card C - Uso do Copiloto (Line Chart):
   - Título: "Consultas ao Copiloto (7 dias)"
   - Chart.js Line Chart com trend dos últimos 7 dias
   - Mostrar: "1,200 queries esta semana"

5. ÚLTIMOS CICLOS (card full-width):
   - Título: "Últimos Ciclos de Avaliação" + botão "Ver Todos" (direita)
   - Lista com 3 items:
     * Q2-2025 (Ativo) - 85/90 completaram - ProgressBar 94%
     * Q1-2025 (Concluído) - 90/90 completaram - Badge "Concluído"
     * Q4-2024 (Concluído) - 88/90 completaram - Badge "Concluído"

REQUISITOS:

UX:
- Dados mockados (não precisa API real)
- Skeleton loading states em todos os cards (pulse animation)
- Hover states em todos os cards (shadow-md)
- Click em "3 Gaps Críticos" navega para /competencias?filter=gaps
- Click em ciclo navega para /avaliacoes/{id}

ACESSIBILIDADE:
- Gráficos têm aria-label descritivo
- Navegação por teclado funcional (tab order lógico)
- Skip link "Pular para conteúdo principal"

RESPONSIVO:
- Mobile (<768px): Stack vertical, KPIs 2x2 grid, charts 1 coluna
- Tablet (768-1023px): KPIs 2x2, charts 2 colunas
- Desktop (1024px+): Layout completo 4 colunas

COMPONENTES:
- Crie componente reutilizável <Card> com variants
- Crie <KPICard> específico para os KPIs
- Use lucide-react para ícones
```

---

## Prompt 2: Assessment Creation Wizard - Step 1 (Configuração)

```
Crie o Step 1 de um wizard multi-step para criação de ciclo de avaliação usando React + TypeScript + Tailwind CSS.

CONTEXTO:
- Wizard com 4 steps: Configuração → Público-Alvo → Competências → Questões
- Usuário: Maria (gestora) criando avaliação trimestral Q2-2025
- Goal: Configurar informações básicas do ciclo de forma rápida e clara

LAYOUT:

1. MODAL/PAGE HEADER:
   - Título: "Criar Novo Ciclo de Avaliação"
   - Botão X (fechar) no canto direito
   - Largura: max-w-4xl (1024px), centralizado

2. WIZARD STEPPER (horizontal):
   - Step 1: "Configuração" (active, blue-600)
   - Step 2: "Público-Alvo" (pending, gray-300)
   - Step 3: "Competências" (pending, gray-300)
   - Step 4: "Questões" (pending, gray-300)
   - Mostrar números + labels
   - Linha conectando steps (progress bar parcial)

3. FORM CONTENT:

   Campo 1 - Nome do Ciclo:
   - Label: "Nome do Ciclo *" (required)
   - Input text, placeholder: "Ex: Avaliação Q2-2025"
   - Helper text: "Escolha um nome descritivo"
   - Validação: min 5 caracteres, max 100

   Campo 2 - Fase do Processo Seletivo:
   - Label: "Fase do Processo Seletivo *"
   - Select dropdown com 3 opções:
     * Fase 1: Triagem Inicial
     * Fase 2: Qualificação Técnica (selected default)
     * Fase 3: Certificação Avançada
   - Helper text: "Baseado na metodologia do PRD"

   Campo 3 - Período de Execução:
   - Label: "Período de Execução *"
   - Duas date inputs lado a lado:
     * Data Início (default: hoje)
     * Data Fim (default: +15 dias)
   - Validação: data fim > data início

   Campo 4 - Descrição (opcional):
   - Label: "Descrição (opcional)"
   - Textarea, rows={4}
   - Placeholder: "Detalhes adicionais sobre este ciclo..."
   - Max 500 caracteres, mostrar contador

4. FOOTER BUTTONS:
   - Botão "Cancelar" (secondary, esquerda)
   - Botão "Próximo: Público-Alvo →" (primary, direita)

REQUISITOS:

VALIDAÇÃO:
- React Hook Form + Zod schema
- Mensagens de erro abaixo dos campos (text-sm, text-red-600)
- Desabilitar botão "Próximo" se form inválido
- Mostrar erro em real-time após blur

UX:
- Auto-focus no primeiro campo ao montar
- Enter key avança para próximo campo (não submete)
- Salvamento automático em localStorage (draft)
- Confirmar ao fechar se houver mudanças não salvas

ACESSIBILIDADE:
- Labels com htmlFor correto
- Campos required têm aria-required="true"
- Erros têm aria-describedby apontando para mensagem
- Tab order lógico (top to bottom)

STATE MANAGEMENT:
- Use React Context para compartilhar dados entre steps
- Interface TypeScript:

  interface AssessmentCycleForm {
    step1: {
      name: string;
      phase: 'phase_1' | 'phase_2' | 'phase_3';
      startDate: Date;
      endDate: Date;
      description?: string;
    };
    step2: { ... };
    // etc
  }

COMPONENTES:
- Crie <WizardStepper> reutilizável
- Crie <FormField> wrapper para label + input + error + helper
```

---

## Prompt 3: Assessment Creation Wizard - Step 2 (Público-Alvo)

```
Crie o Step 2 do wizard de criação de avaliação (Público-Alvo) usando React + TypeScript + Tailwind CSS.

CONTEXTO:
- Continuação do wizard (Step 1 já completado)
- Maria está selecionando quais mecânicos participarão da avaliação
- Goal: Selecionar 90 mecânicos das 6 concessionárias de forma rápida

LAYOUT:

1. WIZARD STEPPER:
   - Step 1: "Configuração" (completed, green checkmark)
   - Step 2: "Público-Alvo" (active, blue-600)
   - Step 3: "Competências" (pending)
   - Step 4: "Questões" (pending)

2. SECTION TITLE:
   - "Quem será avaliado?"
   - Text-2xl, font-semibold, mb-6

3. SELEÇÃO DE CONCESSIONÁRIAS:

   Card com border:
   - Título: "Selecione Concessionárias"

   Checkbox 1 (default checked):
   - ☑ "Todas as 6 concessionárias"
   - Quando checked, mostrar badge: "90 mecânicos"

   Checkbox 2:
   - ☐ "Selecionar individualmente"
   - Quando checked, expandir lista com 6 checkboxes:
     * ABC Motors - SP (15 mecânicos)
     * XYZ Auto - RJ (18 mecânicos)
     * Gamma Veículos - BH (12 mecânicos)
     * Delta Motors - Curitiba (20 mecânicos)
     * Epsilon Auto - Porto Alegre (13 mecânicos)
     * Zeta Cars - Brasília (12 mecânicos)
   - Usar accordion/collapse animation (250ms)

4. FILTROS ADICIONAIS (Card separado):

   Título: "Filtros Adicionais (Opcional)"

   Checkbox filters:
   - [ ] Apenas mecânicos classificados como "Iniciante"
   - [ ] Apenas mecânicos sem avaliação nos últimos 3 meses
   - [ ] Apenas mecânicos de concessionárias com gaps críticos

   Quando algum checkbox marcado:
   - Atualizar contador dinamicamente (ex: "45 mecânicos atendem aos filtros")

5. PREVIEW SUMMARY (Alert box):
   - Background: blue-50, border-left blue-600 (4px)
   - Ícone: 📊
   - Texto: "90 mecânicos serão incluídos nesta avaliação"
   - Atualizar em tempo real conforme seleção muda

6. FOOTER:
   - Botão "← Voltar" (secondary, esquerda)
   - Botão "Próximo: Competências →" (primary, direita, disabled se nenhum mecânico selecionado)

REQUISITOS:

UX:
- Animação suave ao expandir/colapsar lista de concessionárias
- Destacar visualmente o contador de mecânicos (badge com pulse animation quando muda)
- Mostrar tooltip ao hover nos filtros explicando o que fazem
- Desabilitar filtros conflitantes (ex: se selecionar "apenas Iniciante", desabilitar "sem avaliação recente")

STATE:
- Calcular dinamicamente total de mecânicos baseado em seleções
- Dados mockados:

  const dealerships = [
    { id: 1, name: 'ABC Motors - SP', mechanicsCount: 15 },
    { id: 2, name: 'XYZ Auto - RJ', mechanicsCount: 18 },
    // etc
  ];

VALIDAÇÃO:
- Não permitir avançar se total de mecânicos = 0
- Mostrar warning se total < 10: "Recomendado mínimo de 10 mecânicos para resultados estatísticos válidos"

ACESSIBILIDADE:
- Checkboxes têm labels clicáveis
- Accordion tem aria-expanded
- Contador anunciado por screen reader quando muda (aria-live="polite")

COMPONENTES:
- <Accordion> para lista de concessionárias
- <Badge> para contadores
- <Alert> para summary
```

---

## Prompt 4: Assessment Creation Wizard - Step 3 (Competências)

```
Crie o Step 3 do wizard de criação de avaliação (Escopo de Competências) usando React + TypeScript + Tailwind CSS.

CONTEXTO:
- Maria está selecionando quais competências avaliar
- Competências baseadas em áreas técnicas automotivas
- Goal: Selecionar 3-5 competências para gerar questões focadas

LAYOUT:

1. WIZARD STEPPER:
   - Step 1: Completed ✓
   - Step 2: Completed ✓
   - Step 3: "Competências" (active)
   - Step 4: Pending

2. SECTION TITLE:
   - "Quais competências avaliar?"
   - Subtitle (text-sm, gray-600): "Selecione de 3 a 5 competências. As questões serão geradas baseadas nessas áreas."

3. COMPETÊNCIAS GRID (3 colunas em desktop, 1 em mobile):

   Cada competência é um card selecionável:

   Card 1 - Diagnóstico Geral:
   - Checkbox grande (top-left)
   - Ícone: 🔍 (grande, centralizado)
   - Título: "Diagnóstico Geral"
   - Descrição: "Identificação de problemas, uso de ferramentas de diagnóstico"
   - Badge: "Fundamental" (blue-100, blue-700)
   - Estado: Selecionável, hover mostra border blue-600

   Card 2 - Freios e Suspensão:
   - Ícone: 🔧
   - Título: "Freios e Suspensão"
   - Descrição: "Manutenção e reparo de sistemas de freio e suspensão"
   - Badge: "Essencial"

   Card 3 - Sistemas Elétricos:
   - Ícone: ⚡
   - Título: "Sistemas Elétricos"
   - Descrição: "Elétrica automotiva, diagnóstico de sensores, ECU"
   - Badge: "Alta Demanda" (amber-100, amber-700)

   Card 4 - Motor e Transmissão:
   - Ícone: ⚙️
   - Título: "Motor e Transmissão"
   - Descrição: "Manutenção de motor, câmbio, sistemas de combustão"

   Card 5 - Ar-Condicionado e Climatização:
   - Ícone: ❄️
   - Título: "Ar-Condicionado"
   - Descrição: "Carga de gás, diagnóstico de vazamentos"

   Card 6 - Sistemas Híbridos/Elétricos:
   - Ícone: 🔋
   - Título: "Híbridos e Elétricos"
   - Descrição: "Veículos híbridos, elétricos, baterias HV"
   - Badge: "Emergente" (green-100, green-700)

   Card 7 - Segurança e ADAS:
   - Ícone: 🛡️
   - Título: "Segurança e ADAS"
   - Descrição: "Airbags, freios ABS, sistemas avançados de assistência"

4. SELECTED COMPETENCIES SUMMARY (Sticky top):
   - Background: gray-50, rounded, p-4
   - Título: "Competências Selecionadas (3/5)"
   - Chips com X para remover:
     * "Diagnóstico Geral" [X]
     * "Freios" [X]
     * "Elétricos" [X]
   - Mostrar warning se < 3 ou > 5

5. FOOTER:
   - "← Voltar"
   - "Próximo: Gerar Questões →" (disabled se não tiver 3-5 selecionados)

REQUISITOS:

UX:
- Click no card inteiro seleciona/deseleciona (não apenas checkbox)
- Animação ao selecionar: scale(1.02) + border-2 blue-600
- Transição suave (150ms) em todas as interações
- Mostrar contador "X/5 selecionados" que atualiza em tempo real
- Desabilitar cards quando limite de 5 atingido (opacity-50 + cursor-not-allowed)

VALIDAÇÃO:
- Mínimo 3 competências
- Máximo 5 competências
- Mostrar mensagem inline:
  * Se < 3: "Selecione pelo menos 3 competências para resultados equilibrados"
  * Se > 5: "Máximo de 5 competências. Remova alguma para continuar."

STATE:
- Array de competências selecionadas
- Sincronizar com context do wizard

ACESSIBILIDADE:
- Cards têm role="checkbox" ou usam input checkbox nativo
- aria-selected no card ativo
- Anunciar quando seleção muda (aria-live)
- Tab order através dos cards

DADOS MOCK:

interface Competency {
  id: string;
  name: string;
  description: string;
  icon: string;
  badge?: { label: string; color: 'blue' | 'amber' | 'green' };
}
```

---

## Prompt 5: Assessment Creation Wizard - Step 4 (Questões)

```
Crie o Step 4 (final) do wizard de criação de avaliação (Geração de Questões) usando React + TypeScript + Tailwind CSS.

CONTEXTO:
- Maria vai gerar 30 questões automaticamente via IA baseadas nas competências selecionadas
- Precisa revisar uma amostra antes de publicar
- Goal: Gerar questões + preview + publicar em <3 minutos

LAYOUT:

1. WIZARD STEPPER:
   - Steps 1-3: Completed ✓
   - Step 4: "Questões" (active)

2. SECTION TITLE:
   - "Geração de Questões Situacionais"
   - Subtitle: "A IA gerará questões baseadas nas competências selecionadas e nos manuais técnicos indexados"

3. CONFIGURAÇÃO DE GERAÇÃO (Card):

   Input Number:
   - Label: "Número de Questões"
   - Default: 30
   - Min: 10, Max: 50
   - Helper: "Recomendado: 30 questões (30-45 min de duração)"

   Select:
   - Label: "Nível de Bloom Predominante"
   - Opções:
     * Aplicação (Recomendado para Fase 2)
     * Análise
     * Síntese
   - Helper: "Define complexidade das questões"

   Checkbox:
   - [ ] "Incluir questões multimodais (com imagens de diagnóstico)"
   - Disabled para MVP com tooltip: "Disponível em breve"

4. BOTÃO DE GERAÇÃO:
   - Button large, full-width, primary
   - "🤖 Gerar 30 Questões com IA"
   - Ao clicar, mostrar loading state com progress:

   Loading State:
   - Progress bar animado
   - Texto dinâmico:
     * "Analisando competências selecionadas... 20%"
     * "Buscando conteúdo relevante nos manuais... 40%"
     * "Gerando questões situacionais... 60%"
     * "Criando rubricas de correção... 80%"
     * "Finalizando... 100%"
   - Duration: ~15 segundos (simulado)

5. PREVIEW DE QUESTÕES (após geração):

   Alert de Sucesso:
   - "✓ 30 questões geradas com sucesso!"
   - Distribuição por competência:
     * Diagnóstico Geral: 10 questões
     * Freios: 10 questões
     * Elétricos: 10 questões

   Tabs:
   - Tab 1: "Preview (5 amostras)" (active)
   - Tab 2: "Todas as Questões (30)"

   Tab 1 - Preview Content:

   Mostrar 5 questões aleatórias:

   Questão 1 Card:
   - Header:
     * "#1 - Diagnóstico Geral"
     * Badge: "Nível: Aplicação"
   - Questão (expandível/colapsável):
     "Você recebe um veículo Modelo ABC 2023 com reclamação de 'perda de potência intermitente'.
     O cliente relata que o problema ocorre apenas em subidas e após 20 minutos de uso.
     Descreva seu processo completo de diagnóstico, incluindo ferramentas e verificações prioritárias."

   - Rubrica de Correção (expandível):
     * Nível 1 (Inadequado): Resposta genérica sem metodologia
     * Nível 2 (Parcial): Menciona verificações mas sem priorização
     * Nível 3 (Adequado): Processo estruturado com ferramentas corretas
     * Nível 4 (Excelente): Diagnóstico completo + justificativas técnicas

   - Botões:
     * "Editar Questão" (icon: ✏️)
     * "Regenerar" (icon: 🔄)
     * "Deletar" (icon: 🗑️)

   [Repetir para questões 2-5]

6. FOOTER ACTIONS:

   Card com background gray-50:
   - Checkbox:
     ☑ "Confirmo que revisei as questões e estão adequadas"

   Buttons:
   - "← Voltar" (secondary)
   - "Editar Todas as 30 Questões" (secondary, abre modal com lista completa)
   - "Publicar Ciclo e Notificar Mecânicos" (primary, large, disabled se checkbox não marcado)

7. MODAL DE CONFIRMAÇÃO (ao clicar Publicar):

   Title: "Confirmar Publicação"
   Body:
   - "Você está prestes a publicar o ciclo 'Avaliação Q2-2025' para 90 mecânicos."
   - "Ações que serão executadas:"
     * ✓ Salvar 30 questões no banco
     * ✓ Associar mecânicos ao ciclo
     * ✓ Enviar 90 notificações via WhatsApp
     * ✓ Ciclo ficará ativo de 15/Out a 30/Out
   - Warning: "Esta ação não pode ser desfeita. Questões não poderão ser editadas após publicação."

   Buttons:
   - "Cancelar"
   - "Confirmar Publicação" (danger color, pois é ação final)

8. SUCCESS STATE (após publicação):

   - Confetti animation (react-confetti)
   - Success message card:
     * Título: "🎉 Ciclo Publicado com Sucesso!"
     * Mensagem: "90 notificações foram enviadas via WhatsApp"
     * Timeline estimada:
       - Hoje: Mecânicos recebem notificação
       - 15/Out: Período de execução inicia
       - 30/Out: Prazo final
       - 02/Nov: Resultados disponíveis (após correção automática)

   - Botões:
     * "Ver Dashboard de Monitoramento" (primary)
     * "Criar Outro Ciclo" (secondary)

REQUISITOS:

UX:
- Progress bar deve ter animação suave (não jumps)
- Preview questões: mostrar 5 aleatórias mas permitir "shuffle" para ver outras
- Editar questão inline (não precisa modal, usar contentEditable)
- Ao regenerar questão, mostrar loading e fade in da nova

STATE:
- Simular API call com setTimeout (15s)
- Gerar questões mockadas randomicamente
- Salvar em Context

ACESSIBILIDADE:
- Progress bar tem aria-valuenow, aria-valuemin, aria-valuemax
- Loading state anuncia progresso para screen readers
- Modal de confirmação tem focus trap

COMPONENTES:
- <ProgressBar> animado
- <QuestionCard> expandível
- <ConfirmationModal>

DADOS MOCK:

const mockQuestions = [
  {
    id: 1,
    competency: 'Diagnóstico Geral',
    bloomLevel: 'Aplicação',
    text: '...',
    rubric: {
      level1: '...',
      level2: '...',
      level3: '...',
      level4: '...'
    }
  },
  // ... 29 mais
];
```

---

## Prompt 6: Mechanic Profile (Drill-down Individual)

```
Crie a página de perfil individual de mecânico para gestores usando React + TypeScript + Tailwind CSS + Chart.js.

CONTEXTO:
- Maria (gestora) fez drill-down de "João Silva" a partir do dashboard de competências
- Goal: Ver perfil completo, evolução e identificar gaps em <1 minuto
- Página read-only (apenas visualização, não edição)

LAYOUT:

1. BREADCRUMB:
   - "Dashboard > Competências > Mecânicos Individuais > João Silva"
   - Links clicáveis até o penúltimo nível

2. HEADER CARD (bg-white, shadow, rounded, p-6):

   Avatar + Info:
   - Avatar grande (96x96px) com iniciais "JS" ou imagem placeholder
   - Ao lado:
     * Nome: "João Silva" (text-3xl, font-bold)
     * Metadata row:
       - CPF: 123.456.789-00
       - Badge: "Pleno" (blue-100, blue-700)
       - Text: "5 anos de experiência"
     * Concessionária: "ABC Motors - São Paulo" (text-sm, gray-600, com ícone 📍)

3. TOP CARDS ROW (2 cards lado a lado):

   Card A - Classificação Atual:
   - Background gradient (green-50 to white)
   - Centro:
     * Badge grande: "ADEQUADO" (green-600, text-2xl, rounded-full)
     * Score: "72%" (text-5xl, font-bold)
     * Trend: "↑ 14% desde Q1-2025" (green-600, text-sm)
   - Footer:
     * "Ranking: 23º de 90 mecânicos" (text-xs, gray-500)

   Card B - Evolução Temporal:
   - Line Chart (Chart.js)
   - Dados:
     * Q4-2024: 58%
     * Q1-2025: 68%
     * Q2-2025: 72%
   - Linha: green-600, smooth curve
   - Pontos marcados, com tooltips mostrando detalhes
   - X-axis: Trimestres, Y-axis: 0-100%

4. PERFIL DE COMPETÊNCIAS (Card full-width):

   Título: "Perfil de Competências"

   Radar Chart (Chart.js):
   - 5 eixos (pentágono):
     * Diagnóstico Geral: 90% (green)
     * Freios e Suspensão: 85% (green)
     * Motor e Transmissão: 70% (yellow)
     * Sistemas Elétricos: 45% (red) ← Destacar como gap
     * Ar-Condicionado: 65% (yellow)

   - Área preenchida com opacity 0.2
   - Pontos nos vértices
   - Grid radial com linhas a cada 20%

   Legenda lateral (list):
   - Cada competência com:
     * Nome
     * Score (número + barra horizontal)
     * Trend icon (↑ ↓ →)
     * Badge se for gap crítico (<60%): "Gap Crítico" (red-100, red-700)

5. RECOMENDAÇÕES (Card com border-left accent):

   Border-left: blue-600, 4px
   Background: blue-50

   Ícone: 💡 (grande)
   Título: "João está progredindo bem! Foco sugerido:"

   Lista de ações:
   - • Sistemas Elétricos (45% → Meta: 70%)
     - Materiais sugeridos:
       * [Link] Curso Online: Elétrica Automotiva Avançada
       * [Link] Manual Técnico: Sistemas Elétricos Modelo XYZ
       * [Link] Vídeo Tutorial: Diagnóstico de Sensores ECU

   - • Motor e Transmissão (70% → Meta: 85%)
     - Material:
       * [Link] Workshop Presencial disponível em Nov/2025

6. TABS SECTION:

   3 Tabs horizontais:
   - Tab 1: "Histórico de Avaliações" (active)
   - Tab 2: "Interações com Copiloto"
   - Tab 3: "Metas e Planos de Desenvolvimento"

   TAB 1 CONTENT - Histórico:

   Table responsiva:
   - Colunas: Ciclo | Data | Score | Classificação | Detalhes
   - Rows:
     * Q2-2025 | 25/Out/2025 | 72% | Adequado | [Ver Respostas]
     * Q1-2025 | 28/Jan/2025 | 68% | Adequado | [Ver Respostas]
     * Q4-2024 | 15/Out/2024 | 58% | Iniciante | [Ver Respostas]

   - Sortable columns
   - Hover state em rows

   TAB 2 CONTENT - Copiloto:

   Stats row (3 mini cards):
   - Total de Consultas: 156 (último trimestre)
   - Taxa de Feedback Positivo: 92%
   - Tópicos Mais Consultados: "Diagnóstico Elétrico" (34%)

   Lista de interações recentes (últimas 5):
   - Cada item:
     * Data/hora: "23/Out/2025 14:32"
     * Preview: "Como diagnosticar sensor de torque em híbrido XYZ..."
     * OS associada: "#45782"
     * Feedback: 👍 ou 👎
     * [Ver Conversa Completa]

   TAB 3 CONTENT - Metas:

   Card vazio com CTA:
   - Ícone: 🎯
   - Texto: "Nenhum plano de desenvolvimento criado ainda"
   - Botão: "Criar Plano de Desenvolvimento" (primary)
   - (Para MVP, pode estar disabled com tooltip "Em breve")

7. FOOTER ACTIONS (Sticky bottom):

   Background: white, border-top, shadow-lg
   Buttons:
   - "⬇ Exportar Perfil (PDF)" (secondary, icon-left)
   - "📧 Enviar Feedback ao Mecânico" (secondary)
   - "✏️ Editar Informações" (primary) - Para MVP: disabled

REQUISITOS:

UX:
- Dados mockados realistas
- Skeleton loading ao entrar (fade in quando dados carregam)
- Gráficos interativos (hover mostra tooltips com detalhes)
- Click em materiais sugeridos abre em nova aba
- Smooth scroll ao navegar entre tabs

RESPONSIVO:
- Mobile: Stack vertical, radar chart 100% width, tabela vira lista de cards

ACESSIBILIDADE:
- Gráficos têm data table alternative (toggle button)
- Tabs têm role="tablist", aria-selected
- Links têm contexto descritivo

DADOS MOCK:

const mechanicProfile = {
  id: 'joao-silva',
  name: 'João Silva',
  cpf: '123.456.789-00',
  level: 'Pleno',
  experience: 5,
  dealership: 'ABC Motors - São Paulo',
  currentScore: 72,
  trend: 14,
  ranking: 23,
  totalMechanics: 90,
  competencies: [
    { name: 'Diagnóstico Geral', score: 90, trend: 'up' },
    { name: 'Freios e Suspensão', score: 85, trend: 'up' },
    { name: 'Motor', score: 70, trend: 'stable' },
    { name: 'Sistemas Elétricos', score: 45, trend: 'down', isGap: true },
    { name: 'Ar-Condicionado', score: 65, trend: 'up' }
  ],
  history: [
    { cycle: 'Q2-2025', date: '2025-10-25', score: 72, level: 'Adequado' },
    // ...
  ]
};
```

---

## Prompt 7: Admin - Knowledge Base Upload

```
Crie a interface de Admin para upload e gestão de manuais técnicos (Knowledge Base) usando React + TypeScript + Tailwind CSS.

CONTEXTO:
- Carlos (admin de TI) precisa fazer upload de novo manual técnico
- Sistema processará PDF → chunks → embeddings → Qdrant (RAG)
- Goal: Upload + validação + processamento com feedback claro de status

LAYOUT:

1. PAGE HEADER:
   - Título: "Base de Conhecimento"
   - Subtitle: "Gerencie os manuais técnicos indexados para o Copiloto"
   - Botão: "+ Upload Novo Manual" (primary, direita)

2. STATS ROW (4 KPIs):
   - Total de Documentos: 12
   - Total de Chunks Indexados: 8,450
   - Latência Média de Busca: 234ms (p95)
   - Último Upload: há 3 dias

3. DOCUMENTS TABLE:

   Toolbar acima:
   - Search input: "Buscar manuais..." (com ícone 🔍)
   - Filter dropdown: "Status: Todos" (options: Todos, Processando, Concluído, Erro)
   - Sort: "Mais Recentes"

   Table:
   - Colunas: Nome | Status | Páginas | Chunks | Processado Em | Ações

   Row 1:
   - Nome: "Manual_Tecnico_Modelo_XYZ_2023.pdf"
   - Status: Badge "Concluído" (green)
   - Páginas: 450
   - Chunks: 1,850
   - Processado: "23/Out/2025 14:32"
   - Ações:
     * Button icon: 🔍 "Testar Busca" (tooltip)
     * Button icon: ⬇️ "Download" (tooltip)
     * Button icon: 🔄 "Reprocessar"
     * Button icon: 🗑️ "Deletar" (red hover)

   Row 2 (Processando):
   - Nome: "Manual_Hibrido_ABC_2026.pdf"
   - Status: Badge "Processando" (blue) + ProgressBar 67%
   - Páginas: 320 (estimado)
   - Chunks: - (ainda processando)
   - Processado: "Processando... ETA: 2 min"
   - Ações: disabled enquanto processa

   Row 3 (Erro):
   - Nome: "Manual_Antigo_Scan.pdf"
   - Status: Badge "Erro" (red)
   - Páginas: 280
   - Chunks: -
   - Processado: "Falha em 20/Out/2025"
   - Ações:
     * 🔄 "Reprocessar"
     * ⚠️ "Ver Erro" (abre modal com log)

4. UPLOAD MODAL (ao clicar "+ Upload Novo Manual"):

   Title: "Upload de Novo Manual Técnico"

   Step 1 - File Upload:

   Dropzone area (border-dashed, bg-gray-50, hover:bg-gray-100):
   - Grande (h-64)
   - Ícone: 📄 (grande, centralizado)
   - Texto: "Arraste e solte o PDF aqui"
   - "ou"
   - Button: "Selecionar Arquivo"
   - Helper text: "Formato: PDF | Tamanho máximo: 100MB | Páginas: até 1000"

   Quando arquivo selecionado:
   - Mostrar preview:
     * Nome: "Manual_Novo.pdf"
     * Tamanho: "45.2 MB"
     * Páginas: 380 (detectado)
     * Ícone PDF + thumbnail da primeira página (se possível)

   - Button "Remover Arquivo" (link style, red)

   Step 2 - Metadata (após selecionar arquivo):

   Form fields:
   - Nome do Documento (auto-preenchido com filename, editável)
   - Categoria (select):
     * Manuais de Serviço
     * Especificações Técnicas
     * Boletins de Serviço
     * Treinamentos
   - Modelo de Veículo (text input, opcional)
     * Placeholder: "Ex: XYZ-2023, ABC Híbrido"
   - Tags (multi-select ou input com chips)
     * Sugestões: "elétrica", "freios", "motor", "híbrido", "diagnóstico"

   Step 3 - Processing Options:

   Checkbox advanced options (collapsed by default):
   - [ ] "Usar OCR avançado" (mais lento, melhor para PDFs escaneados)
   - [ ] "Chunk size customizado" (input: default 1000 tokens)
   - [ ] "Priorizar processamento" (usa mais recursos, mais rápido)

   Footer:
   - "Cancelar"
   - "Fazer Upload e Processar" (primary, large)

5. PROCESSING MODAL (após upload):

   Non-closable modal (user precisa esperar ou pode minimizar)

   Header:
   - Título: "Processando Manual_Novo.pdf"
   - Button: "Minimizar" (fecha modal mas continua background)

   Progress Section:

   Overall Progress Bar:
   - 0-100%, animado
   - Cor: blue-600

   Steps breakdown (vertical stepper):
   - [✓] Upload completo (45.2 MB em 8s)
   - [⏳] Extraindo texto... 340/380 páginas (progress bar parcial)
   - [ ] Gerando chunks...
   - [ ] Criando embeddings...
   - [ ] Indexando no Qdrant...

   Live Logs (collapsible):
   - Console-style logs:
     [14:32:05] Upload iniciado
     [14:32:13] Upload completo ✓
     [14:32:14] Iniciando extração de texto...
     [14:32:45] Página 100/380 processada
     [14:33:12] Página 200/380 processada
     ...

   ETA:
   - Grande, centralizado: "Tempo estimado: 4 minutos"
   - Atualiza em tempo real

6. SUCCESS STATE:

   Modal de sucesso:
   - Confetti animation
   - Ícone: ✅ (grande)
   - Título: "Manual Processado com Sucesso!"
   - Stats:
     * 380 páginas processadas
     * 1,620 chunks gerados
     * Indexado no Qdrant
     * Latência p95: 187ms (teste automático)

   CTA:
   - "Testar Busca Agora" (primary)
   - "Voltar à Lista" (secondary)

7. TEST SEARCH MODAL (ao clicar "Testar Busca"):

   Input:
   - "Digite uma query de teste..."
   - Placeholder: "Ex: como trocar filtro de ar"
   - Button: "Buscar" (ao lado)

   Results (após buscar):

   Top 5 Chunks:
   - Cada resultado:
     * Score de similaridade: 0.87 (barra verde)
     * Documento: "Manual_Novo.pdf"
     * Página: 142
     * Preview do texto (300 chars max)
     * Button: "Ver no PDF" (abre PDF na página correta)

   Footer:
   - Texto: "Busca retornou 5 resultados em 187ms"

REQUISITOS:

UX:
- Drag & drop files funcional
- Validação client-side:
  * Apenas PDFs
  * Max 100MB
  * Mostrar erro se não passar
- Upload com progress bar (axios onUploadProgress)
- Processing simular com WebSocket ou polling (GET /api/documents/{id}/status a cada 2s)
- Auto-refresh table quando novo documento completar

VALIDAÇÃO:
- File type: application/pdf
- File size: max 100MB
- Nome não vazio
- Categoria obrigatória

ACESSIBILIDADE:
- Dropzone tem role e aria-label
- Progress bars têm aria-valuenow
- Logs têm aria-live para screen readers

STATE:
- Use React Query para table data + auto-refetch
- Upload progress em state local
- Processing status via polling

COMPONENTES:
- <FileDropzone>
- <ProcessingProgress>
- <DocumentRow>

MOCK API:
- POST /api/documents/upload → { id, status: 'processing' }
- GET /api/documents/{id}/status → { status, progress, currentStep }
- GET /api/documents/{id}/test-search?q=... → { results: [...] }
```

---

## Prompt 8: Competências - Visão Agregada

```
Crie a página de Competências (Visão Agregada) para gestores usando React + TypeScript + Tailwind CSS + Chart.js.

CONTEXTO:
- Maria quer visão geral de competências dos 90 mecânicos
- Identificar gaps por concessionária e por área técnica
- Drill-down para listas e depois para indivíduos

LAYOUT:

1. HEADER:
   - Título: "Mapeamento de Competências"
   - Filtros (row):
     * Período: Dropdown "Q2-2025" (Q1-2025, Q4-2024, Todos)
     * Concessionárias: Multi-select "Todas" (6 checkboxes)
     * Nível: Multi-select "Todos" (Iniciante, Adequado, Experiente)
   - Button: "Exportar Relatório" (CSV) (direita)

2. OVERVIEW CARDS (4 KPIs):
   - Score Médio Geral: 72% (trend: +8% vs trimestre anterior)
   - Mecânicos Adequados: 61% (55/90)
   - Gaps Críticos Identificados: 3 áreas
   - Taxa de Evolução: 89% melhoraram

3. DISTRIBUIÇÃO POR NÍVEL (Card com Pie + List):

   Left: Pie Chart
   - Iniciante: 20 (22%, amber)
   - Adequado: 55 (61%, green)
   - Experiente: 10 (11%, blue)
   - Não Avaliado: 5 (6%, gray)

   Right: Lista com detalhes
   - Cada nível:
     * Nome
     * Contagem
     * Percentual
     * Mini bar chart
     * Link "Ver lista de mecânicos →"

4. GAPS CRÍTICOS (Card destacado, border-left red-600):

   Alert style, background red-50

   Título: "⚠️ 3 Competências com Gaps Críticos"
   Subtitle: "Mais de 60% dos mecânicos abaixo do nível adequado"

   List:
   1. Sistemas Elétricos
      - 54/90 mecânicos abaixo de adequado (60%)
      - Score médio: 52%
      - Bar chart horizontal (red-600)
      - Concessionária mais afetada: "Delta Motors (85% abaixo)"
      - Button: "Ver Detalhes →"

   2. Diagnóstico de Híbridos
      - 42/90 abaixo (47%)
      - Score: 58%
      - Bar chart (amber)
      - "XYZ Auto (72% abaixo)"

   3. Sistemas ADAS
      - 38/90 abaixo (42%)
      - Score: 61%
      - Bar chart (amber)
      - "Gamma Veículos (65% abaixo)"

5. HEATMAP POR CONCESSIONÁRIA × COMPETÊNCIA:

   Título: "Mapa de Calor: Competências por Concessionária"

   Table-style heatmap:

   Rows: 6 concessionárias
   Columns: 7 competências principais

   Células:
   - Background color baseado em score médio:
     * 0-59%: red-100
     * 60-74%: amber-100
     * 75-84%: blue-100
     * 85-100%: green-100

   - Texto: Score médio (ex: "67%")
   - Hover: Tooltip com:
     * Concessionária
     * Competência
     * Score médio
     * Nº mecânicos
     * Trend

   - Click: Drill-down para lista de mecânicos daquela célula

   Legenda:
   - Gradient bar mostrando escala de cores

6. EVOLUÇÃO TEMPORAL (Card com Line Chart):

   Título: "Evolução Trimestral das Competências"

   Multi-line chart (Chart.js):
   - X-axis: Q4-2024, Q1-2025, Q2-2025
   - Y-axis: Score médio (0-100%)
   - 5 linhas (top 5 competências):
     * Diagnóstico Geral (green, linha mais alta ~85%)
     * Freios (blue, ~78%)
     * Motor (purple, ~72%)
     * Elétricos (red, linha mais baixa ~52%, destaque)
     * Ar-Cond (orange, ~68%)

   Legenda interativa (click para hide/show linha)

7. TOP & BOTTOM PERFORMERS (2 cards lado a lado):

   Card A - Top 10 Mecânicos:
   - Título: "🏆 Top Performers"
   - Lista rankeada:
     1. Maria Santos - 94% - Experiente
     2. Carlos Silva - 92%
     3. ... (até 10)
   - Avatar + nome + score + badge nível
   - Click navega para perfil

   Card B - Necessitam Atenção:
   - Título: "⚠️ Necessitam Desenvolvimento"
   - Lista dos 10 com menor score
   - Destacar gap crítico principal de cada
   - Button: "Criar Plano de Capacitação"

8. AÇÕES RECOMENDADAS (Footer Card):

   AI-generated insights:

   Ícone: 💡
   Título: "Recomendações Baseadas em Dados"

   Lista:
   - 📚 "Priorizar treinamento em Sistemas Elétricos para Delta Motors (35 mecânicos)"
   - 🎯 "Criar workshop de Diagnóstico Híbrido (42 inscritos potenciais)"
   - 👥 "Identificar mecânicos experientes para mentoria interna (10 elegíveis)"

   Button: "Gerar Plano de Ação Completo" (opens wizard)

REQUISITOS:

UX:
- Filtros aplicam em tempo real (debounce 300ms)
- Heatmap interativo (hover + click)
- Charts responsivos (redimensionam com window)
- Exportar CSV com dados filtrados
- Smooth transitions ao aplicar filtros

INTERAÇÕES:
- Click em "Sistemas Elétricos" no gaps → Drill-down para lista de 54 mecânicos
- Click em célula do heatmap → Lista filtrada
- Click em top performer → Perfil individual

RESPONSIVO:
- Mobile: Stack vertical, heatmap scroll horizontal, charts full-width

ACESSIBILIDADE:
- Heatmap tem data table alternative
- Cores não são única forma de informação (mostrar números)
- Charts têm aria-label descritivo

DADOS MOCK:

const competenciesData = {
  overview: {
    avgScore: 72,
    trend: 8,
    adequatePercentage: 61,
    criticalGaps: 3
  },
  distribution: {
    iniciante: 20,
    adequado: 55,
    experiente: 10,
    naoAvaliado: 5
  },
  gaps: [
    {
      name: 'Sistemas Elétricos',
      belowAdequate: 54,
      avgScore: 52,
      mostAffected: { dealership: 'Delta Motors', percentage: 85 }
    }
    // ...
  ],
  heatmap: [
    { dealership: 'ABC Motors', competencies: { diagnostico: 85, freios: 78, ... } },
    // ...
  ]
};
```

---

## Prompt 9: Copiloto Insights - Analytics de Uso

```
Crie a página de Copiloto Insights para gestores monitorarem uso do assistente IA usando React + TypeScript + Tailwind CSS + Chart.js.

CONTEXTO:
- Maria quer monitorar como mecânicos estão usando o Copiloto
- Verificar queries mais comuns, feedback, performance
- Identificar oportunidades de melhoria na base de conhecimento

LAYOUT:

1. HEADER:
   - Título: "Copiloto - Analytics de Uso"
   - Filtros:
     * Período: "Últimos 7 dias" (Hoje, 7 dias, 30 dias, Custom range)
     * Concessionária: "Todas"
   - Real-time indicator: "🟢 Atualizado há 2 minutos"

2. USAGE OVERVIEW (4 KPIs animados):

   KPI 1 - Total de Queries:
   - Número grande: 1,247
   - Trend: +18% vs período anterior
   - Spark line (mini chart) mostrando últimos 7 dias

   KPI 2 - Usuários Ativos:
   - 67 mecânicos (de 90 total)
   - 74% de adoção
   - Ícone de usuários

   KPI 3 - Taxa de Feedback Positivo:
   - 92% 👍
   - 8% 👎
   - Ícone polegar

   KPI 4 - Latência Média:
   - 1.8s (p95: 3.2s)
   - Status: "Ótimo" (green badge)
   - Target: <3s

3. QUERIES OVER TIME (Card com Line Chart):

   Título: "Volume de Consultas por Dia"

   Chart.js Line Chart:
   - X-axis: Últimos 7 dias (seg, ter, qua, ...)
   - Y-axis: Número de queries
   - Linha: blue-600, smooth
   - Área abaixo: fill com gradient opacity
   - Pontos nos dias com hover tooltip:
     * Data
     * Total queries
     * Peak hour

   Toggle buttons acima do chart:
   - [ ] Mostrar por hora (muda granularidade)
   - [ ] Comparar com semana anterior (adiciona linha tracejada)

4. TOP QUERIES (Card com Table):

   Título: "Queries Mais Frequentes"
   Subtitle: "Últimos 7 dias"

   Table:
   - Colunas: # | Query | Freq | Taxa Positiva | Latência Média | Ação

   Rows:
   1. "Como diagnosticar sensor de torque" | 87x | 95% 👍 | 1.2s | [Ver Respostas]
   2. "Troca de pastilha de freio modelo XYZ" | 64x | 98% 👍 | 0.9s | [Ver]
   3. "Código de erro P0420 catalisador" | 52x | 88% 👍 | 2.1s | [Ver]
   4. "Como resetar luz de manutenção" | 48x | 92% 👍 | 0.7s | [Ver]
   5. "Sangria de freio ABS" | 41x | 89% 👍 | 1.5s | [Ver]

   - Highlight rows com baixa taxa positiva (<85%) em amber-50
   - Click em query abre modal com sample de respostas

5. QUERY CATEGORIES (Card com Pie Chart):

   Título: "Distribuição por Categoria"

   Pie Chart:
   - Diagnóstico: 35% (blue)
   - Procedimentos de Manutenção: 28% (green)
   - Especificações Técnicas: 18% (purple)
   - Troubleshooting: 12% (amber)
   - Outros: 7% (gray)

   Legend com counts absolutos

6. USAGE BY MECHANIC (Card com Bar Chart):

   Título: "Top 10 Usuários Mais Ativos"

   Horizontal Bar Chart:
   - Mecânico (y-axis)
   - Queries (x-axis)

   Bars:
   1. João Silva - 78 queries
   2. Maria Santos - 64
   3. Carlos Oliveira - 59
   ...
   10. Paulo Costa - 31

   Nota: "Média: 18 queries/mecânico"

7. FEEDBACK ANALYSIS (2 cards):

   Card A - Feedback Positivo (green border):
   - 👍 92% (1,147 de 1,247)
   - "Respostas úteis e precisas"
   - Trending up

   Card B - Feedback Negativo (red border):
   - 👎 8% (100 de 1,247)
   - Top motivos (tags auto-geradas):
     * "Resposta incompleta" (42%)
     * "Fonte não encontrada" (28%)
     * "Demora na resposta" (18%)
     * "Informação desatualizada" (12%)

   - Button: "Ver Queries Problemáticas" (abre filtered view)

8. PERFORMANCE METRICS (Card com Mixed Chart):

   Título: "Performance e Custo"

   Combined chart (Bar + Line):
   - X-axis: Últimos 7 dias
   - Y-axis (left): Latência (segundos) - Line chart (red)
   - Y-axis (right): Custo LLM ($) - Bar chart (green)

   Stats abaixo:
   - Latência p50: 1.2s
   - Latência p95: 3.2s (target: <3s) ✓
   - Latência p99: 5.8s (target: <5s) ⚠️

   - Custo total 7 dias: $142.50
   - Custo médio por query: $0.11
   - Projeção mensal: ~$610

9. KNOWLEDGE GAPS (Card com Alert style):

   Border-left: amber-600, 4px
   Background: amber-50

   Título: "⚠️ Lacunas na Base de Conhecimento"
   Subtitle: "Queries com baixa taxa de sucesso indicam conteúdo faltante"

   Lista:
   1. "Procedimentos para modelos 2024+"
      - 23 queries
      - 67% feedback negativo
      - Ação sugerida: "Adicionar manuais de 2024"
      - Button: [Fazer Upload]

   2. "Diagnóstico de sistemas ADAS"
      - 18 queries
      - 71% feedback negativo
      - Ação: "Treinamento especializado necessário"

   3. "Especificações de torque para modelo ABC"
      - 15 queries
      - 73% feedback negativo

10. RECENT CONVERSATIONS (Card com List):

    Título: "Conversas Recentes"
    Filtro: Dropdown "Todas" (Todas, Apenas positivas, Apenas negativas)

    List items (últimas 10):

    Item:
    - Avatar mecânico
    - Nome: "João Silva"
    - Preview: "Como diagnosticar sensor de torque em híbrido..."
    - Timestamp: "há 5 min"
    - Feedback: 👍
    - OS: "#45782"
    - Button: "Ver Completa →"

    Click abre modal com transcrição completa:
    - Chat bubbles (mechanic left, copiloto right)
    - Citações de fontes destacadas
    - Metadata: timestamp, latência, tokens usados

11. EXPORT & ACTIONS (Footer):

    Buttons:
    - "📊 Exportar Relatório (CSV)"
    - "📧 Agendar Relatório Semanal" (abre modal de configuração)
    - "⚙️ Configurar Alertas" (ex: alerta se taxa positiva < 85%)

REQUISITOS:

UX:
- Dados atualizam a cada 2 minutos (auto-refresh)
- Charts interativos (hover, click, zoom)
- Filtros aplicam em todos os cards simultaneamente
- Smooth transitions ao filtrar
- Click em qualquer métrica abre drill-down detalhado

REAL-TIME:
- Opcional: Usar WebSocket para live updates
- Mostrar badge "🟢 Live" quando conectado
- Fallback: Polling a cada 2 min

ACESSIBILIDADE:
- Charts têm data table alternative
- Color-blind friendly (não apenas cores para feedback)
- Screen reader announce updates (aria-live)

DADOS MOCK:

const analyticsData = {
  period: 'last_7_days',
  overview: {
    totalQueries: 1247,
    trend: 18,
    activeUsers: 67,
    totalUsers: 90,
    positiveFeedback: 92,
    avgLatency: 1.8,
    p95Latency: 3.2
  },
  timeline: [
    { date: '2025-10-17', queries: 156 },
    { date: '2025-10-18', queries: 189 },
    // ...
  ],
  topQueries: [
    {
      query: 'Como diagnosticar sensor de torque',
      frequency: 87,
      positiveFeedback: 95,
      avgLatency: 1.2
    },
    // ...
  ],
  categories: {
    diagnostico: 35,
    manutencao: 28,
    especificacoes: 18,
    troubleshooting: 12,
    outros: 7
  }
};
```

---

## Notas de Implementação

### Ordem Sugerida de Desenvolvimento:

1. **Setup inicial**: Design system (cores, componentes base)
2. **Dashboard Home**: Familiarizar com charts e layout
3. **Mechanic Profile**: Página de leitura, sem forms complexos
4. **Competências View**: Heatmap e visualizações avançadas
5. **Assessment Wizard**: Forms complexos, state management
6. **Admin Upload**: File handling, progress tracking
7. **Copiloto Insights**: Real-time, analytics avançado

### Componentes Reutilizáveis Prioritários:

1. `<Card>` - Base para todos os layouts
2. `<KPICard>` - Cards de métricas
3. `<Button>` - Variants (primary, secondary, danger, ghost)
4. `<Badge>` - Status indicators
5. `<Table>` - Com sorting, filtering
6. `<Modal>` - Dialogs e confirmações
7. `<ProgressBar>` - Loading states
8. `<Skeleton>` - Loading placeholders
9. `<Chart>` wrapper - Chart.js abstractions

### Stack Recomendada (Lovable):

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@tanstack/react-query": "^5.0.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "lucide-react": "^0.294.0",
    "date-fns": "^2.30.0",
    "tailwindcss": "^3.3.0"
  }
}
```

### Dados Mock:

Todos os prompts incluem dados mockados. Para MVP, não precisa backend real - use:
- `useState` para dados locais
- `localStorage` para persistência
- `setTimeout` para simular latência de API
- React Query pode ser usado com dados mock também
