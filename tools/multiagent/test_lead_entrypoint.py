from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from lead_entrypoint import LeadEntrypoint
from lead_orchestrator import RequestSignals


class LeadEntrypointTests(unittest.TestCase):
    def test_bootstrap_persists_non_trivial_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            entrypoint = LeadEntrypoint(Path(temp_dir))
            result = entrypoint.bootstrap(
                RequestSignals(
                    request_summary="Add a new projected-glasses alert with new error states",
                    lead_interpretation="Feature-flow bootstrap",
                    user_visible_behavior_change=True,
                    new_states_or_errors=True,
                    cross_role_dependency=True,
                )
            )

            self.assertTrue(result.persisted)
            self.assertEqual(result.classification, "feature flow")
            self.assertEqual(result.task_mode, "implementation")
            payload = json.loads(Path(result.intake_payload_path).read_text(encoding="utf-8"))
            self.assertEqual(payload["request_summary"], "Add a new projected-glasses alert with new error states")

    def test_bootstrap_skips_persistence_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            entrypoint = LeadEntrypoint(Path(temp_dir))
            result = entrypoint.bootstrap(
                RequestSignals(
                    request_summary="Fix a typo in a stable UI label",
                    lead_interpretation="Trivial patch bootstrap",
                    explicit_trivial_patch=True,
                ),
                persist_mode="never",
            )

            self.assertFalse(result.persisted)

    def test_role_report_persistence_writes_latest_and_timestamped_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            entrypoint = LeadEntrypoint(Path(temp_dir))
            result = entrypoint.persist_role_report(
                role="QA",
                content="# QA Report\n\n- Evidence: smoke path\n",
                persist_mode="always",
            )

            self.assertTrue(result["persisted"])
            self.assertTrue(Path(result["latest_path"]).exists())
            self.assertTrue(Path(result["report_path"]).exists())


if __name__ == "__main__":
    unittest.main()
