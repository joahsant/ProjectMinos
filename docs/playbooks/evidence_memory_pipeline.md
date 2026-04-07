# Evidence Memory Pipeline

## Purpose
- Apply a lightweight `raw evidence -> synthesized docs -> lint` workflow to this repository.
- Preserve technical findings without turning the documentation set into a sprawling wiki.

## Model
- `artifacts/` stores raw evidence bundles.
- `artifacts/registry.json` records which bundles matter and which authority docs own their synthesis.
- `docs/` stores the curated project truth.
- `AGENTS.md` and agent contracts define the maintenance rules.

## When To Use
- A task produces logs, dumps, screenshots, SDK metadata, APK samples, decompilation output, or other reusable evidence.
- A platform investigation creates findings that should outlive the current chat thread.
- A blocker or runtime failure depends on specific evidence rather than memory alone.

## Workflow
1. Save the raw evidence under the appropriate bundle family in `artifacts/`.
2. Register a new bundle in `artifacts/registry.json` or update an existing one.
3. Update the owning docs in `docs/` with the operational consequence, decision, or feature impact.
4. Run `python tools/multiagent/evidence_pipeline.py lint`.
5. Fix any missing coverage or stale references before closing the task.

## Pairing XR Investigations
- Every reusable XR pairing investigation should create or update a dedicated evidence bundle instead of dropping untracked logs into `artifacts/`.
- Prefer bundle ids that make the investigation thread obvious, for example `EV-XR-PAIRING-2026-04-06`.
- XR pairing bundles should normally point back to:
  - `docs/OPERATIONS.md` for factual blocker state
  - `docs/DECISIONS.md` when the investigation changes constraints or confirmed platform behavior
- Emulator logs, UI dumps, `dumpsys` captures, and reverse-engineering output from pairing work should be grouped under one bundle family when they belong to the same investigation pass.

## Bundle Guidance
- Prefer one bundle per investigation thread or evidence family.
- Prefer directories over long lists of files when the files belong together.
- Use top-level loose-file bundles only when there is no stable directory boundary.
- Use `python tools/multiagent/evidence_pipeline.py scaffold` for new bundles instead of hand-editing the registry.

## Scaffold Example
```powershell
python tools/multiagent/evidence_pipeline.py scaffold `
  --id EV-XR-PAIRING-2026-04-06 `
  --kind xr_pairing `
  --summary "Runtime evidence bundle for a new XR pairing investigation pass." `
  --path artifacts/emulator/logs/pairing-pass-2026-04-06 `
  --owner-doc docs/OPERATIONS.md `
  --owner-doc docs/DECISIONS.md `
  --mkdir
```

## Lint Expectations
- Every bundle id must be unique.
- Every registered path must exist.
- Every owner doc must exist.
- Every owner doc must mention the bundle id or one of its registered paths.
- Direct children under `artifacts/analysis`, `artifacts/emulator`, and `artifacts/sdk` should be covered by some registered bundle.
- `docs/FEATURES.md` must stay aligned with selected canonical decisions from `docs/DECISIONS.md`.
- `docs/PRD.md` must stay aligned with selected canonical decisions from `docs/DECISIONS.md`.
