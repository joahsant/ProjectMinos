# Codex Governance

## Purpose
- This file is the primary execution contract for Codex in this repository.
- It defines persistent project rules, intake behavior, routing boundaries, delivery standards, and the agent-harness improvement loop.
- It does not replace feature, operations, security, or data-governance docs. Those remain the domain sources of truth they own.

## Authority Model
- Prefer authority in this order:
  1. explicit human direction
  2. `AGENTS.md`
  3. directory-local `AGENTS.md` files when they exist
  4. agent contracts under `docs/agents/`
  5. workflow skills under `docs/skills/`
  6. reference docs such as `docs/OPERATIONS.md`, `docs/FEATURES.md`, `docs/SECURITY.md`, `docs/DATA_GOVERNANCE.md`, and `docs/DECISIONS.md`
- `README.md` is the human quickstart, not the primary rule source.

## Language
- Speak to the user in Portuguese in Codex.
- Keep code, repository documentation, and operational artifacts in English unless a product file explicitly requires another language.

## Current Project Direction
- The product is an Android XR app for AI glasses.
- The initial target is a passive selected-coin quote surface projected to AI glasses through the Android XR development model currently available, with host-side selection from a curated crypto catalog.
- The product promise is passive monitoring for traders with low interruption cost.
- The glasses surface must stay glanceable, battery-aware, and readable at a short dwell time.
- The current phase still requires strong planning and documentation discipline even when implementation tasks are approved.
- Do not start project code, builds, installs, emulator runs, or environment downloads until the human explicitly approves execution.
- When asking how to develop the product, frame questions around trader interruption cost, glanceability, battery impact, and passive monitoring first.

## Mandatory Thread Entry
- Every new request in this repository must begin with `Lead / Orchestrator`.
- Do not start directly as `Engineer`, `QA`, or another role even when the user asks for implementation immediately.
- Every new feature or material feature expansion must route through the agent stack before implementation.
- The first meaningful response for a new request must make the Lead intake explicit:
  - interpretation
  - classification
  - gate state
  - activated roles and depth
  - next owner
- If the request is still in discovery or planning, stay in documentation and premise-definition mode.
- If clarification is needed, agents must ask numbered questions and include only the short suggestions needed to answer quickly.
- Prefer one consolidated batch of numbered questions over many small rounds.
- When bootstrapping from the shell, use `start-request.ps1` or `python tools/multiagent/lead_entrypoint.py`.

## Multiagent Model
- `Lead / Orchestrator` is the only intake role.
- `Product Strategist` owns product premises, user-visible states, and roadmap slicing.
- `UX/UI Strategist` owns flow clarity, glanceability, battery-aware interaction, accessibility, and design-system implications for XR and companion surfaces.
- `Market Data Analyst` owns quote-source evaluation, polling constraints, symbol semantics, freshness guarantees, and historical-data tradeoffs.
- `Engineer` implements from approved premises and reports technical deltas and deviations.
- `QA` validates happy path, edge cases, regressions, and runtime confidence.
- `Documentation / Historian` consolidates internal truth and operational memory.

## Activation Rules
- Classify every request as one of:
  - `trivial patch`
  - `localized change`
  - `feature flow`
  - `structural initiative`
- Assign every request a `task mode`:
  - `advisory`
  - `review`
  - `planning`
  - `implementation`
- Activate roles in one of three depths:
  - `deep analysis`
  - `light validation`
  - `no-impact confirmation`
- Use the narrowest valid route.
- A simple request still passes logically through the stack, but most roles may stay at light or no-impact depth.
- Use `docs/playbooks/activation_matrix.md` as the compact routing reference.

## Persistent Project Rules
- Treat `docs/FEATURES.md` as the source of truth for current product behavior.
- Treat `docs/OPERATIONS.md` as the factual state, blocker, and execution queue source.
- Treat `docs/DECISIONS.md` as the consolidated source for active decisions and still-open questions.
- Treat `docs/SECURITY.md` and `docs/DATA_GOVERNANCE.md` as the source of truth for secrets, storage, transport, retention, and external data handling.
- Treat `artifacts/` as raw evidence, not as project truth by itself.
- Prefer updating existing docs before creating new ones.
- Do not create a new `.md` unless there is a real authority gap.
- Do not silently expand scope when implementation reveals new states, pairing behavior, backend requirements, or data-policy changes.
- Do not start build, install, emulator, device, or runtime validation unless the user explicitly asks for it in the current thread.
- Do not download SDKs, IDEs, emulators, or API tools until the user explicitly approves environment setup.
- For this project, battery cost is a first-class product concern; avoid gratuitous polling, rendering, and background work.
- When revising agent contracts, routing logic, or workflow prompts, use the harness iteration loop instead of untracked prompt drift.
- Keep the repository coherent after every completed governance/tooling task; do not leave broken references to missing agent docs, playbooks, or harness files.

## Repository Memory Model
- Use a three-layer memory model:
  - raw evidence in `artifacts/`
  - synthesized project truth in `docs/`
  - maintenance rules in `AGENTS.md`, `docs/agents/`, and `docs/playbooks/`
- Evidence must be curated by bundle, not treated as a flat pile of files.
- Use `artifacts/registry.json` as the tracked registry of evidence bundles that matter to the active project state.
- A relevant evidence bundle is not complete until at least one authority doc in `docs/` reflects why it matters.
- When adding or materially changing evidence, prefer:
  1. place or update the raw evidence under `artifacts/`
  2. register or update the bundle in `artifacts/registry.json`
  3. update the affected authority docs in `docs/`
- For XR pairing work, create or update a dedicated evidence bundle for each reusable investigation pass instead of leaving ad hoc logs and dumps unregistered.
- Do not rely on conversation memory when the repository can hold the evidence and synthesis explicitly.

## Mandatory Work Order
- For every substantial task:
  - read governing docs
  - inspect the current implementation and affected files
  - update existing docs first if repository truth is missing or outdated
  - implement changes
  - run builds or validation only when explicitly requested
  - report outcome, evidence, and remaining gaps

## Required Reading Matrix
- Read `README.md` when a human-readable quickstart is useful.
- Read `docs/OPERATIONS.md` when the task touches blockers, priorities, setup posture, or roadmap state.
- Read `docs/DECISIONS.md` before inventing answers to unresolved behavior.
- Read `docs/FEATURES.md` before changing feature behavior.
- Read `artifacts/README.md` and `artifacts/registry.json` when a task depends on logs, decompilation output, SDK metadata, or emulator evidence.
- Read `docs/SECURITY.md` and `docs/DATA_GOVERNANCE.md` when touching API keys, transport, user preferences, telemetry, or persistence.
- Read `docs/skills/agent_harness_iteration.md` when improving agent contracts, prompts, or routing behavior.
- Read the relevant agent contracts in `docs/agents/` for scoped role behavior.

## Agent Harness Rule
- Use the harness when the task is about improving agent behavior itself, not product behavior.
- Start from a baseline before editing the target contract, skill, or routing tool.
- Change one mutable surface at a time.
- Keep the benchmark suite fixed for the duration of a comparative run.
- Log the candidate result and keep the change only when the score improves, or when the score holds and the contract is simpler.
- Use:
  - `python tools/multiagent/agent_harness_entrypoint.py`
  - `python tools/multiagent/agent_harness_cycle.py`
  - `python tools/multiagent/agent_harness_scorer.py`
  - `powershell -File tools/multiagent/start-agent-harness-cycle.ps1`

## Request Persistence
- Persist request state when:
  - more than one role participates
  - the request spans more than one turn or cycle
  - there are open risks, blocked decisions, or deferred work
  - the user explicitly wants traceability
- Persist the Lead intake and every participating role report under the same active request state whenever persistence is enabled.
- Runtime persistence for shell workflows lives under `%LOCALAPPDATA%\\CodexLead\\Project Minos\\`.

## Definition Of Done
- Docs and code are aligned.
- Validation has run only if it was explicitly requested.
- Known gaps and deferred work are documented.
- The final owner records final status, delivered scope, validation state, remaining risks, and next action.

## Repository Structure
- `AGENTS.md` is the primary Codex contract for this repository.
- `artifacts/` holds raw evidence bundles and their tracked registry metadata.
- Agent contracts live under `docs/agents/`.
- Workflow skills live under `docs/skills/`.
- Routing support playbooks live under `docs/playbooks/`.
- Templates live under `docs/templates/`.
- Operational state and memory live under `docs/OPERATIONS.md` and `docs/DECISIONS.md`.
- Lead bootstrap and harness utilities live under `tools/multiagent/`.
