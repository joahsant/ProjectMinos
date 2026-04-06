from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_harness_entrypoint import AgentHarnessEntrypoint, BenchmarkSuite


class AgentHarnessEntrypointTests(unittest.TestCase):
    def test_bootstrap_persists_run_context_results_and_notes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            entrypoint = AgentHarnessEntrypoint(Path(temp_dir))
            result = entrypoint.bootstrap(
                run_tag="Lead Clarity Apr5",
                target_surface="docs/agents/lead-orchestrator.md",
                benchmark_suite=("lead-feature-flow-btc-surface", "lead-market-data-change"),
                success_criteria=("asks missing high-leverage questions", "keeps role boundaries"),
                hypothesis="Lead should ask fewer but higher-signal questions.",
            )

            self.assertTrue(result.persisted)
            self.assertTrue(Path(result.context_path).exists())
            self.assertTrue(Path(result.results_path).exists())
            self.assertTrue(Path(result.notes_path).exists())

            payload = json.loads(Path(result.context_path).read_text(encoding="utf-8"))
            self.assertEqual(payload["run_tag"], "lead-clarity-apr5")
            self.assertEqual(payload["target_surface"], "docs/agents/lead-orchestrator.md")

            header = Path(result.results_path).read_text(encoding="utf-8")
            self.assertEqual(
                header,
                "candidate\toverall_score\tstatus\tchanged_surface\tdescription\n",
            )
            notes = Path(result.notes_path).read_text(encoding="utf-8")
            self.assertIn("- Decision: `pending`", notes)
            self.assertIn("Allowed values: `keep` or `discard`", notes)

    def test_bootstrap_rejects_duplicate_run_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            entrypoint = AgentHarnessEntrypoint(Path(temp_dir))
            kwargs = {
                "run_tag": "duplicate-run",
                "target_surface": "docs/agents/product-strategist.md",
                "benchmark_suite": ("feature-flow",),
                "success_criteria": ("improves product questions",),
            }
            entrypoint.bootstrap(**kwargs)
            with self.assertRaises(FileExistsError):
                entrypoint.bootstrap(**kwargs)

    def test_bootstrap_skips_persistence_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            entrypoint = AgentHarnessEntrypoint(Path(temp_dir))
            result = entrypoint.bootstrap(
                run_tag="no-persist",
                target_surface="docs/agents/ux-ui-strategist.md",
                benchmark_suite=("ux-flow-gap",),
                success_criteria=("asks workflow questions",),
                persist_mode="never",
            )

            self.assertFalse(result.persisted)
            self.assertFalse(Path(result.run_dir).exists())

    def test_benchmark_suite_loads_labels_criteria_and_target_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite_path = Path(temp_dir) / "suite.json"
            suite_path.write_text(
                json.dumps(
                    {
                        "suite_name": "Core Suite",
                        "target_surface": "docs/agents/lead-orchestrator.md",
                        "benchmarks": [
                            {
                                "id": "lead-one",
                                "success_criteria": ["criterion-a", "criterion-b"],
                            },
                            {
                                "id": "lead-two",
                                "success_criteria": ["criterion-b", "criterion-c"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            suite = BenchmarkSuite.from_file(suite_path)

            self.assertEqual(suite.name, "Core Suite")
            self.assertEqual(suite.target_surface, "docs/agents/lead-orchestrator.md")
            self.assertEqual(suite.benchmark_suite, ("lead-one", "lead-two"))
            self.assertEqual(
                suite.success_criteria,
                ("criterion-a", "criterion-b", "criterion-c"),
            )


if __name__ == "__main__":
    unittest.main()
