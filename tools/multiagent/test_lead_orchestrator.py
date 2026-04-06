from __future__ import annotations

import unittest

from lead_orchestrator import (
    AgentRole,
    Classification,
    Gate,
    LeadOrchestrator,
    ParticipationDepth,
    ReasoningEffort,
    RequestSignals,
    ReviewScope,
    TaskMode,
)


class LeadOrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.orchestrator = LeadOrchestrator()

    def test_trivial_patch_stays_narrow(self) -> None:
        report = self.orchestrator.build_intake_report(
            RequestSignals(
                request_summary="Fix a typo in a stable UI label.",
                lead_interpretation="A tiny UI copy correction with no expected behavior change.",
                explicit_trivial_patch=True,
            )
        )

        self.assertEqual(report.classification, Classification.TRIVIAL_PATCH)
        self.assertEqual(report.task_mode, TaskMode.IMPLEMENTATION)
        self.assertEqual(report.review_scope, ReviewScope.LOCALIZED_CORRECTION)
        self.assertNotIn(Gate.HUMAN_REVIEW, report.gate_sequence)
        self.assertEqual(report.recommendation.next_role, AgentRole.ENGINEER)
        self.assertEqual(report.recommendation.reasoning_effort, ReasoningEffort.LOW)
        self.assertEqual(report.recommendation.expected_depth, ParticipationDepth.LIGHT_VALIDATION)

    def test_feature_flow_activates_product_and_ux(self) -> None:
        report = self.orchestrator.build_intake_report(
            RequestSignals(
                request_summary="Add a new glasses alert with new error states.",
                lead_interpretation="The request changes user-visible flow and introduces new states that need explicit acceptance framing.",
                user_visible_behavior_change=True,
                new_states_or_errors=True,
                ux_surface_change=True,
                cross_role_dependency=True,
            )
        )

        self.assertEqual(report.classification, Classification.FEATURE_FLOW)
        self.assertEqual(report.review_scope, ReviewScope.BROAD_REVIEW)
        self.assertEqual(report.recommendation.next_role, AgentRole.PRODUCT)
        self.assertEqual(report.recommendation.reasoning_effort, ReasoningEffort.HIGH)

    def test_data_contract_change_routes_to_market_data(self) -> None:
        report = self.orchestrator.build_intake_report(
            RequestSignals(
                request_summary="Switch provider and reduce refresh interval.",
                lead_interpretation="The request changes quote semantics and freshness policy.",
                data_contract_change=True,
                freshness_or_polling_change=True,
            )
        )

        self.assertEqual(report.classification, Classification.FEATURE_FLOW)
        self.assertEqual(report.activations[3].role, AgentRole.MARKET_DATA)
        self.assertEqual(report.activations[3].depth, ParticipationDepth.DEEP_ANALYSIS)

    def test_task_mode_is_preserved_in_report(self) -> None:
        report = self.orchestrator.build_intake_report(
            RequestSignals(
                request_summary="Review whether the QA role contract is sufficient.",
                lead_interpretation="This is a governance review request without implementation.",
                task_mode=TaskMode.REVIEW,
                structural_change=True,
            )
        )

        self.assertEqual(report.task_mode, TaskMode.REVIEW)
        self.assertEqual(report.classification, Classification.STRUCTURAL_INITIATIVE)
        self.assertEqual(report.recommendation.next_role, AgentRole.DOCUMENTATION)


if __name__ == "__main__":
    unittest.main()
