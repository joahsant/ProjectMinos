# Periodic Agent Harness Review

## Purpose
- Re-run a fixed agent-quality evaluation flow after new models, new agent research, or a meaningful change to repository governance.
- Keep agent improvement recurring and comparable instead of episodic and memory-driven.

## Fixed Flow
1. Choose the benchmark suite size for the cycle.
2. Run the automatic cycle with `python tools/multiagent/agent_harness_cycle.py`.
3. Compare the score against the previous comparable run.
4. Refine only the weakest contracts.
5. Re-run the same suite before changing the suite size.
6. Increase the suite size only after the current suite stabilizes.

## Recommended Suite Tiers
- Focused iteration: `tools/multiagent/benchmark_suites/core_agent_harness_suite.json`
- Full-coverage baseline: `tools/multiagent/benchmark_suites/all_agents_harness_suite.json`
- XR routing and product constraints: `tools/multiagent/benchmark_suites/xr_agent_harness_suite.json`
- Real repository requests: `tools/multiagent/benchmark_suites/real_requests_harness_suite.json`
- Expanded coverage: `tools/multiagent/benchmark_suites/all_agents_harness_suite_25.json`
- Aggressive coverage: `tools/multiagent/benchmark_suites/all_agents_harness_suite_50.json`

## Outputs
- A persisted run directory under `%LOCALAPPDATA%\\CodexLead\\Project Minos\\agent_harness\\`
- Automatic score in `results.tsv`
- Automatic summary in `notes.md`
- A comparable score delta when a previous run tag is supplied
