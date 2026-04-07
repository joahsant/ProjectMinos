# Evidence Bundles

## Purpose
- Keep raw evidence in one place without turning the repository into an undocumented file dump.
- Group evidence by bundle so logs, decompilation output, SDK metadata, and captured UI remain traceable.

## Rules
- `artifacts/` holds raw evidence only. It is not the final source of project truth.
- Every active or reusable evidence bundle should be registered in `registry.json`.
- Every registered bundle should be reflected by at least one authority doc under `docs/`.
- Prefer bundle-level registration over file-by-file registration.
- Generated bulk files remain ignored by git unless explicitly unignored.

## Current Bundle Families
- `analysis/` static analysis, APK inspection, decompilation, and plugin reverse engineering
- `emulator/` emulator launch logs and UI dumps
- `sdk/` SDK manager logs and repository metadata

## Maintenance
- Use `python tools/multiagent/evidence_pipeline.py lint` to verify bundle registration, doc linkage, and drift-sensitive doc alignment.
- Use `python tools/multiagent/evidence_pipeline.py summary` to print the current tracked bundle inventory.
- Use `python tools/multiagent/evidence_pipeline.py scaffold ...` to append a new bundle entry without editing `registry.json` manually.
