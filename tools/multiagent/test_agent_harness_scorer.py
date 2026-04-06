from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_harness_scorer import AgentHarnessScorer


class AgentHarnessScorerTests(unittest.TestCase):
    def test_score_suite_uses_signal_groups_and_role_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs_dir = root / "docs" / "agents"
            docs_dir.mkdir(parents=True)
            (root / "AGENTS.md").write_text(
                "- baseline governance\n",
                encoding="utf-8",
            )
            (docs_dir / "product.md").write_text(
                "# Product\n- empty, loading, success, and error\n- retry\n- back-navigation\n- partial state\n",
                encoding="utf-8",
            )
            suite_path = root / "suite.json"
            suite_path.write_text(
                json.dumps(
                    {
                        "suite_name": "Test Suite",
                        "version": "1.0",
                        "passing_score": 75.0,
                        "role_contracts": {
                            "Product Strategist": "docs/agents/product.md"
                        },
                        "benchmarks": [
                            {
                                "id": "product-gap",
                                "target_role": "Product Strategist",
                                "signal_groups": [
                                    ["empty, loading, success, and error"],
                                    ["retry"],
                                    ["back-navigation"],
                                    ["partial state"],
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            summary = AgentHarnessScorer(root).score_suite(suite_path)

            self.assertEqual(summary.overall_score, 100.0)
            self.assertEqual(summary.status, "keep")
            self.assertEqual(summary.role_results[0].role, "Product Strategist")
            self.assertEqual(summary.benchmark_results[0].weight, 1.0)

    def test_score_suite_can_read_multiple_contract_paths_per_benchmark(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs_dir = root / "docs"
            agents_dir = docs_dir / "agents"
            agents_dir.mkdir(parents=True)
            (root / "AGENTS.md").write_text(
                "- Every new request must begin with Lead / Orchestrator.\n- human review\n",
                encoding="utf-8",
            )
            (agents_dir / "lead.md").write_text(
                "# Lead\n- plan-first mode\n- gate sequence\n",
                encoding="utf-8",
            )
            suite_path = root / "suite.json"
            suite_path.write_text(
                json.dumps(
                    {
                        "suite_name": "Multi Source Suite",
                        "version": "1.0",
                        "passing_score": 75.0,
                        "role_contracts": {
                            "Lead / Orchestrator": "docs/agents/lead.md",
                        },
                        "benchmarks": [
                            {
                                "id": "lead-entry",
                                "target_role": "Lead / Orchestrator",
                                "contract_paths": ["AGENTS.md", "docs/agents/lead.md"],
                                "signal_groups": [
                                    ["lead / orchestrator"],
                                    ["human review"],
                                    ["plan-first mode"],
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            summary = AgentHarnessScorer(root).score_suite(suite_path)

            self.assertEqual(summary.overall_score, 100.0)
            self.assertEqual(summary.benchmark_results[0].score, 100.0)

    def test_score_suite_uses_shared_contract_paths_and_weights(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            agents_dir = root / "docs" / "agents"
            agents_dir.mkdir(parents=True)
            (root / "AGENTS.md").write_text(
                "- global governance phrase\n",
                encoding="utf-8",
            )
            (agents_dir / "lead.md").write_text(
                "# Lead\n- scoped phrase\n",
                encoding="utf-8",
            )
            suite_path = root / "suite.json"
            suite_path.write_text(
                json.dumps(
                    {
                        "suite_name": "Weighted Suite",
                        "version": "1.0",
                        "passing_score": 75.0,
                        "shared_contract_paths": ["AGENTS.md"],
                        "role_weights": {
                            "Lead / Orchestrator": 2.0
                        },
                        "role_contracts": {
                            "Lead / Orchestrator": "docs/agents/lead.md"
                        },
                        "benchmarks": [
                            {
                                "id": "weighted-lead",
                                "target_role": "Lead / Orchestrator",
                                "signal_groups": [
                                    ["global governance phrase"],
                                    ["scoped phrase"]
                                ]
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            summary = AgentHarnessScorer(root).score_suite(suite_path)

            self.assertEqual(summary.overall_score, 100.0)
            self.assertEqual(summary.benchmark_results[0].weight, 2.0)
            self.assertEqual(summary.role_results[0].weight, 2.0)


if __name__ == "__main__":
    unittest.main()
