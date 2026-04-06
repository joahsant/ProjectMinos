# Request Cycle Workflow

## Purpose
- Define the repeatable operational procedure for starting, routing, reporting, persisting, and closing a request.

## Workflow
- start with `Lead / Orchestrator`
- assign request classification and task mode
- open the current gate and name the next owner
- activate only the roles required at the right depth
- persist Lead and role reports when the request crosses roles or spans multiple cycles
- keep docs aligned with accepted scope
- close the request only when final status, delivered scope, evidence, remaining risks, and next action are explicit

## Persistence
- Use `python tools/multiagent/lead_entrypoint.py` to bootstrap a persisted request state.
- Use `python tools/multiagent/role_report_entrypoint.py` to persist role reports into the active request state.
