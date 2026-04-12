# Agent Flow Visual

- Open `agent_flow_visual.html` in a browser to inspect the current multiagent flow as a node-based visual map.
- The visual is derived from `AGENTS.md`, `docs/playbooks/activation_matrix.md`, `docs/agents/`, and the orchestration scripts under `tools/multiagent/`.
- Treat the HTML file as a documentation lens over the current routing logic, not as the source of truth itself.

## Mermaid View

```mermaid
flowchart LR
    U[User Request] --> L[Lead / Orchestrator]
    L --> S[Interpretation + RequestSignals]
    S --> C[Classification]
    S --> M[Task Mode]
    C --> R[Lead Report]
    M --> R

    R --> P[Product Strategist]
    R --> X[UX/UI Strategist]
    R --> D[Market Data Analyst]
    R --> E[Engineer]

    P --> E
    X --> E
    D --> E

    E --> Q[QA]
    Q --> H[Documentation / Historian]

    R --> G[Gate Sequence]
    G --> G1[Understanding / Plan]
    G1 --> G2[Operational Specification]
    G2 --> G3[Implementation]
    G3 --> G4[Validation]
    G4 --> G5[Documentary Consolidation]

    R --> PERSIST[Runtime Persistence]
    PERSIST --> A[%LOCALAPPDATA%/CodexLead/Project Minos/active]
    PERSIST --> B[lead_entrypoint.py]
    PERSIST --> C2[role_report_entrypoint.py]
```

## Detailed Routing View

```mermaid
flowchart TD
    U["User request"] --> L["Lead / Orchestrator"]
    L --> LI["Interpretation<br/>classification<br/>gate state<br/>activated roles<br/>next owner"]
    LI --> RS["RequestSignals payload"]
    RS --> ORCH["lead_orchestrator.py"]

    ORCH --> CL{"Classification"}
    CL -->|trivial patch| EN1["Engineer<br/>light validation"]
    CL -->|localized change| EN2["Engineer<br/>deep analysis or bounded execution"]
    CL -->|feature flow| PR["Product Strategist"]
    CL -->|structural initiative| DOC1["Documentation / Historian"]

    RS --> UXCHK{"UX / visibility impact?"}
    UXCHK -->|yes| UX["UX/UI Strategist"]
    UXCHK -->|no| SK1["Skip or no-impact confirmation"]

    RS --> DATACHK{"Data / freshness impact?"}
    DATACHK -->|yes| MD["Market Data Analyst"]
    DATACHK -->|no| SK2["Skip or no-impact confirmation"]

    PR --> PR_OUT["Product premises<br/>state map<br/>scope boundaries<br/>open questions"]
    UX --> UX_OUT["Glanceability guidance<br/>readability constraints<br/>battery-aware behavior"]
    MD --> MD_OUT["Source semantics<br/>polling guidance<br/>freshness constraints"]

    PR_OUT --> EN3["Engineer"]
    UX_OUT --> EN3
    MD_OUT --> EN3
    EN1 --> QA["QA"]
    EN2 --> QA
    EN3 --> QA

    QA --> QA_OUT["Validation status<br/>failure locality<br/>caveats or evidence"]
    QA_OUT --> DOC2["Documentation / Historian"]

    DOC1 --> DOC2
    DOC2 --> DOC_OUT["Update repository truth<br/>docs alignment<br/>request closure state"]

    LI --> G["Gate sequence"]
    G --> G1["Understanding / Plan"]
    G1 --> G2["Operational Specification"]
    G2 --> G3["Implementation"]
    G3 --> G4["Validation"]
    G4 --> G5["Documentary Consolidation"]

    LI --> PERSIST["Persistence decision"]
    PERSIST --> LE["lead_entrypoint.py"]
    LE --> ACTIVE["_active_request.md<br/>_active_intake.json<br/>_request_log.jsonl"]
    QA_OUT --> RR["role_report_entrypoint.py"]
    PR_OUT --> RR
    UX_OUT --> RR
    MD_OUT --> RR
    RR --> REPORTS["role_reports/<role>.md<br/>role_reports/<role>-timestamp.md"]
```

## Agent Detail Matrix

| Agent | Recebe | Faz | Gera | Envia para |
|---|---|---|---|---|
| `Lead / Orchestrator` | pedido do usuário, contexto atual, sinais de impacto | interpreta o pedido, classifica, define `task mode`, abre gate, ativa papéis por profundidade, escolhe próximo owner | `Lead Report`, `RequestSignals`, recomendação do próximo passo, riscos e premissas | próximo agente recomendado, runtime persistence via `lead_entrypoint.py` |
| `Product Strategist` | `Lead Report`, dúvidas de comportamento, escopo indefinido | explicita premissas de produto, estados visíveis, retries, recovery, fronteira MVP vs futuro | premissas operacionais, mapa de estados, perguntas abertas | `Engineer`, `Documentation / Historian`, eventualmente volta ao `Lead` |
| `UX/UI Strategist` | impacto visual, mudança de superfície, preocupações de glanceability/acessibilidade | define clareza de fluxo, legibilidade, comportamento battery-aware, implicações de largura e atenção | guidance de UX, restrições de UI, critérios de leitura rápida | `Engineer`, `Documentation / Historian`, eventualmente volta ao `Lead` |
| `Market Data Analyst` | dúvidas de fonte, polling, semântica de cotação, freshness | avalia contratos de dados, cadência, custo/limites, semântica e tradeoffs de histórico | regras de polling, garantias de freshness, decisão de fonte e semântica | `Engineer`, `Documentation / Historian`, eventualmente volta ao `Lead` |
| `Engineer` | premissas aprovadas, constraints técnicos, rota de execução | implementa sem reabrir escopo, registra desvios técnicos, separa falhas do app de bloqueios de ambiente | delta técnico, implementação, notas de restrição | `QA`, `Documentation / Historian`, ou volta ao `Lead` se faltarem premissas |
| `QA` | implementação, critérios aceitos, contexto de falha | valida happy path, edge cases, regressões e localidade do problema | status `not tested`, `failed` ou `passed with caveats`, evidências e caveats | `Documentation / Historian`, `Lead / Orchestrator` |
| `Documentation / Historian` | outputs dos demais agentes, evidências, docs atuais | consolida a verdade do repositório, alinha docs, preserva riscos e trabalho pendente | atualização de `docs/*`, fechamento documental, memória do request | repositório como fonte de verdade, fechamento da request |

## Persistence Paths

- `lead_entrypoint.py` persiste o intake em `%LOCALAPPDATA%\CodexLead\Project Minos\active`.
- Os arquivos principais do ciclo ativo são `_active_request.md`, `_active_intake.json` e `_request_log.jsonl`.
- `role_report_entrypoint.py` persiste relatórios em `role_reports/`.
- Cada relatório de papel gera duas visões:
  - um arquivo estável `role_reports/<role>.md`
  - um arquivo histórico `role_reports/<role>-<timestamp>.md`

## Reading Notes

- Toda request entra por `Lead / Orchestrator`.
- O `Lead` classifica o pedido, define `task mode`, abre os gates e recomenda o próximo papel.
- `Product`, `UX/UI` e `Market Data` entram quando há impacto em comportamento, experiência ou semântica dos dados.
- `Engineer` implementa apenas depois das premissas estarem claras.
- `QA` e `Documentation / Historian` fecham validação e consolidação documental.
