# Agent Harness Iteration Workflow

## Purpose
- Define a repeatable workflow for improving agent contracts, prompts, and routing behavior using an `autoresearch`-style loop.
- Optimize the repository harness, not the underlying model.
- Keep agent changes empirical, reviewable, and reversible.

## Use When
- An agent repeatedly misses the questions it should ask.
- A role drifts across responsibility boundaries.
- The same class of request keeps producing weak or generic outputs.
- A prompt or contract change is being considered and should be tested against real repository scenarios.

## Core Principles
- Start with a baseline before editing anything.
- Change one mutable surface at a time.
- Keep the benchmark suite fixed for the duration of the run.
- Log every candidate and decide `keep` or `discard`.
- Prefer simpler contracts when scores are equal.
- Use real repository requests whenever possible before inventing synthetic prompts.

## Mutable Surfaces
- One agent contract under `docs/agents/`.
- One workflow skill under `docs/skills/`.
- One bootstrap or routing tool under `tools/multiagent/`.

## Benchmark Suite
- Use 3 to 10 canonical request scenarios for focused iteration.
- Reuse real repository requests when possible.
- Each benchmark should define:
  - target role
  - expected behavior
  - failure modes to watch
  - success criteria
- The focused starter suite for this repository lives at `tools/multiagent/benchmark_suites/core_agent_harness_suite.json`.
- The full-coverage suite for active roles lives at `tools/multiagent/benchmark_suites/all_agents_harness_suite.json`.
- The XR-specific suite lives at `tools/multiagent/benchmark_suites/xr_agent_harness_suite.json`.
- The real-request suite lives at `tools/multiagent/benchmark_suites/real_requests_harness_suite.json`.

## Workflow
1. Pick a run tag and the single target surface to improve.
2. Define the benchmark suite and explicit success criteria before editing the contract.
3. Initialize the run with `python tools/multiagent/agent_harness_entrypoint.py`.
4. Record the baseline result first with no contract change.
5. Make one bounded contract or tooling change.
6. Run the fixed benchmark suite against the changed harness.
7. Log the result in `results.tsv`.
8. Keep the change only if the score improves, or if the score holds and the contract is simpler.
9. Discard the change and revert if the score drops or boundary discipline regresses.
10. Repeat until the run reaches a clearly better stable contract.

## Output
- `run_context.json`
- `results.tsv`
- `notes.md`
- accepted contract or tooling diff
- automatic score when the suite provides signal groups and role-contract mappings

## Notes Rule
- Every candidate section in `notes.md` must record an explicit `keep` or `discard` decision.
- Do not leave a run with an ambiguous decision state.
