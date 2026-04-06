from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_harness_cycle import run_cycle


class AgentHarnessCycleTests(unittest.TestCase):
    def test_run_cycle_bootstraps_scores_and_persists_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "AGENTS.md").write_text(
                "- baseline governance\n",
                encoding="utf-8",
            )
            docs_dir = root / "docs" / "agents"
            docs_dir.mkdir(parents=True)
            (docs_dir / "qa.md").write_text(
                "# QA\n- happy path, edge cases, and regressions\n- evidence\n- narrowest believable failure locality\n- not tested, failed, and passed with caveats\n",
                encoding="utf-8",
            )
            suite_path = root / "suite.json"
            suite_path.write_text(
                json.dumps(
                    {
                        "suite_name": "Cycle Suite",
                        "version": "1.0",
                        "target_surface": "docs/agents/",
                        "passing_score": 75.0,
                        "role_contracts": {
                            "QA": "docs/agents/qa.md",
                        },
                        "benchmarks": [
                            {
                                "id": "qa-proof",
                                "target_role": "QA",
                                "success_criteria": ["records explicit evidence"],
                                "signal_groups": [
                                    ["happy path, edge cases, and regressions"],
                                    ["evidence"],
                                    ["narrowest believable failure locality"],
                                    ["not tested, failed, and passed with caveats"],
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = run_cycle(
                repo_root=root,
                run_tag="cycle-run",
                suite_file=suite_path,
                candidate="auto-score",
                hypothesis="QA should score well.",
                compare_run_tag=None,
                persist_mode="always",
            )

            self.assertEqual(result.overall_score, 100.0)
            self.assertEqual(result.status, "keep")
            results_path = Path(result.run_dir) / "results.tsv"
            self.assertIn("auto-score\t100.0\tkeep", results_path.read_text(encoding="utf-8"))
            notes_path = Path(result.run_dir) / "notes.md"
            self.assertIn("Decision recommendation: `keep`", notes_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
