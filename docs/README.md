# Documentation Hub

## Purpose
- Provide the entry point for the repository documentation.
- Keep the project truth separated by authority so each document stays short and useful.

## Read Order
1. `../AGENTS.md`
2. `PRD.md`
3. `FEATURES.md`
4. `OPERATIONS.md`
5. `DECISIONS.md`
6. `SECURITY.md`
7. `DATA_GOVERNANCE.md`

## Authority Map
- `PRD.md` defines the product contract, MVP intent, and scope boundaries.
- `FEATURES.md` records current behavior as implemented or approved.
- `OPERATIONS.md` records factual project state, blockers, and execution queue items.
- `DECISIONS.md` records active decisions and open questions that still shape the repository.
- `SECURITY.md` records security posture, secrets handling, and transport expectations.
- `DATA_GOVERNANCE.md` records data retention, persistence, and external data handling rules.
- `../artifacts/registry.json` records tracked evidence bundles that should map back into the authority docs.
- `agents/` defines stable role contracts.
- `skills/` defines repeatable workflows.
- `playbooks/` provides compact routing references.
- `templates/` provides structured report scaffolds.

## Current Phase
- The repository is in documentation and initial implementation alignment mode.
- The current MVP is a top-50 crypto host catalog with a single selected-coin glasses surface for Android XR AI glasses.
- The product should stay battery-aware, glanceable, and passive first.

## When To Update
- Update `PRD.md` when the product contract or scope changes.
- Update `FEATURES.md` when current behavior changes.
- Update `OPERATIONS.md` when the factual project state changes.
- Update `DECISIONS.md` when a decision is made or an open question is introduced.
- Update `SECURITY.md` or `DATA_GOVERNANCE.md` when data handling or safety posture changes.
- Update `../artifacts/registry.json` when a new reusable evidence bundle is created or retired.

## Related
- Root overview: `../README.md`
- Governance contract: `../AGENTS.md`
- Routing playbook: `playbooks/activation_matrix.md`
- Agent flow visual: `playbooks/agent_flow_visual.md`
- Evidence pipeline: `playbooks/evidence_memory_pipeline.md`
- Harness workflow: `skills/agent_harness_iteration.md`
