from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any


class AgentRole(StrEnum):
    LEAD = "Lead / Orchestrator"
    PRODUCT = "Product Strategist"
    UX_UI = "UX/UI Strategist"
    MARKET_DATA = "Market Data Analyst"
    ENGINEER = "Engineer"
    QA = "QA"
    DOCUMENTATION = "Documentation / Historian"


class Classification(StrEnum):
    TRIVIAL_PATCH = "trivial patch"
    LOCALIZED_CHANGE = "localized change"
    FEATURE_FLOW = "feature flow"
    STRUCTURAL_INITIATIVE = "structural initiative"


class TaskMode(StrEnum):
    ADVISORY = "advisory"
    REVIEW = "review"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"


class ParticipationDepth(StrEnum):
    DEEP_ANALYSIS = "deep analysis"
    LIGHT_VALIDATION = "light validation"
    NO_IMPACT_CONFIRMATION = "no-impact confirmation"


class ReviewScope(StrEnum):
    LOCALIZED_CORRECTION = "localized correction"
    BROAD_REVIEW = "broad review"


class Gate(StrEnum):
    UNDERSTANDING_PLAN = "Understanding / Plan"
    HUMAN_REVIEW = "Human Review"
    OPERATIONAL_SPECIFICATION = "Operational Specification"
    IMPLEMENTATION = "Implementation"
    VALIDATION = "Validation"
    DOCUMENTARY_CONSOLIDATION = "Documentary Consolidation"


class ReasoningEffort(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    DEEP = "deep"


@dataclass(slots=True, frozen=True)
class WorkflowPolicy:
    mandatory_human_review: bool = False
    allow_trivial_patch_bypass: bool = True


@dataclass(slots=True, frozen=True)
class RequestSignals:
    request_summary: str
    lead_interpretation: str
    task_mode: TaskMode = TaskMode.IMPLEMENTATION
    explicit_trivial_patch: bool = False
    user_visible_behavior_change: bool = False
    new_states_or_errors: bool = False
    ux_surface_change: bool = False
    accessibility_impact: bool = False
    design_system_impact: bool = False
    cross_role_dependency: bool = False
    structural_change: bool = False
    ambiguous_intent: bool = False
    data_contract_change: bool = False
    freshness_or_polling_change: bool = False
    persistence_or_telemetry_change: bool = False
    local_failure_only: bool = False
    qa_structural_failure: bool = False
    approved_reports: tuple[str, ...] = ()
    open_decisions: tuple[str, ...] = ()
    unresolved_risks: tuple[str, ...] = ()
    human_overrides: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class AgentActivation:
    role: AgentRole
    depth: ParticipationDepth
    rationale: str


@dataclass(slots=True, frozen=True)
class NextStepRecommendation:
    next_role: AgentRole
    reasoning_effort: ReasoningEffort
    expected_depth: ParticipationDepth
    expected_output: str


@dataclass(slots=True, frozen=True)
class LeadReport:
    request_summary: str
    lead_interpretation: str
    classification: Classification
    task_mode: TaskMode
    review_scope: ReviewScope
    assumptions: tuple[str, ...]
    risks: tuple[str, ...]
    current_gate: Gate
    gate_sequence: tuple[Gate, ...]
    activations: tuple[AgentActivation, ...]
    recommendation: NextStepRecommendation
    approved_reports: tuple[str, ...] = ()
    open_decisions: tuple[str, ...] = ()
    unresolved_risks: tuple[str, ...] = ()
    human_overrides: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_summary": self.request_summary,
            "lead_interpretation": self.lead_interpretation,
            "classification": self.classification.value,
            "task_mode": self.task_mode.value,
            "review_scope": self.review_scope.value,
            "assumptions": list(self.assumptions),
            "risks": list(self.risks),
            "current_gate": self.current_gate.value,
            "gate_sequence": [gate.value for gate in self.gate_sequence],
            "activations": [
                {
                    "role": activation.role.value,
                    "depth": activation.depth.value,
                    "rationale": activation.rationale,
                }
                for activation in self.activations
            ],
            "recommendation": {
                "next_role": self.recommendation.next_role.value,
                "reasoning_effort": self.recommendation.reasoning_effort.value,
                "expected_depth": self.recommendation.expected_depth.value,
                "expected_output": self.recommendation.expected_output,
            },
            "approved_reports": list(self.approved_reports),
            "open_decisions": list(self.open_decisions),
            "unresolved_risks": list(self.unresolved_risks),
            "human_overrides": list(self.human_overrides),
        }

    def to_markdown(self) -> str:
        lines = [
            "# Lead Intake Report",
            "",
            "## Request Summary",
            self.request_summary,
            "",
            "## Lead Interpretation",
            self.lead_interpretation,
            "",
            "## Classification",
            f"- Current classification: `{self.classification.value}`",
            f"- Task mode: `{self.task_mode.value}`",
            f"- Review scope: `{self.review_scope.value}`",
            "",
            "## Assumptions",
        ]
        lines.extend(self._render_list(self.assumptions))
        lines.extend(["", "## Risks"])
        lines.extend(self._render_list(self.risks))
        lines.extend(
            [
                "",
                "## Gate State",
                f"- Current gate: `{self.current_gate.value}`",
                "- Planned sequence:",
            ]
        )
        lines.extend(f"  - `{gate.value}`" for gate in self.gate_sequence)
        lines.extend(["", "## Activated Roles"])
        for activation in self.activations:
            lines.append(
                f"- `{activation.role.value}` -> `{activation.depth.value}`: {activation.rationale}"
            )
        lines.extend(["", "## Shared State", "- Approved reports:"])
        lines.extend(self._render_nested_list(self.approved_reports))
        lines.extend(["- Open decisions:"])
        lines.extend(self._render_nested_list(self.open_decisions))
        lines.extend(["- Unresolved risks:"])
        lines.extend(self._render_nested_list(self.unresolved_risks))
        lines.extend(["- Human overrides:"])
        lines.extend(self._render_nested_list(self.human_overrides))
        lines.extend(
            [
                "",
                "## Recommendation",
                f"- Next role: `{self.recommendation.next_role.value}`",
                f"- Reasoning effort: `{self.recommendation.reasoning_effort.value}`",
                f"- Expected depth: `{self.recommendation.expected_depth.value}`",
                f"- Expected output: {self.recommendation.expected_output}",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _render_list(items: tuple[str, ...]) -> list[str]:
        if not items:
            return ["- None"]
        return [f"- {item}" for item in items]

    @staticmethod
    def _render_nested_list(items: tuple[str, ...]) -> list[str]:
        if not items:
            return ["  - None"]
        return [f"  - {item}" for item in items]


class LeadOrchestrator:
    def __init__(self, policy: WorkflowPolicy | None = None) -> None:
        self.policy = policy or WorkflowPolicy()

    def build_intake_report(self, request: RequestSignals) -> LeadReport:
        classification = self._classify(request)
        review_scope = self._review_scope(classification)
        assumptions = self._build_assumptions(request, classification)
        risks = self._build_risks(request, classification)
        gate_sequence = self._build_gate_sequence(request, classification)
        activations = self._build_activations(request, classification)
        recommendation = self._build_recommendation(request, classification)
        return LeadReport(
            request_summary=request.request_summary,
            lead_interpretation=request.lead_interpretation,
            classification=classification,
            task_mode=request.task_mode,
            review_scope=review_scope,
            assumptions=assumptions,
            risks=risks,
            current_gate=Gate.UNDERSTANDING_PLAN,
            gate_sequence=gate_sequence,
            activations=activations,
            recommendation=recommendation,
            approved_reports=request.approved_reports,
            open_decisions=request.open_decisions,
            unresolved_risks=request.unresolved_risks,
            human_overrides=request.human_overrides,
        )

    def _classify(self, request: RequestSignals) -> Classification:
        if self._qualifies_as_trivial_patch(request):
            return Classification.TRIVIAL_PATCH
        if request.structural_change or request.qa_structural_failure:
            return Classification.STRUCTURAL_INITIATIVE
        if any(
            (
                request.user_visible_behavior_change,
                request.new_states_or_errors,
                request.cross_role_dependency,
                request.ambiguous_intent,
                request.data_contract_change,
                request.freshness_or_polling_change,
                request.persistence_or_telemetry_change,
            )
        ):
            return Classification.FEATURE_FLOW
        return Classification.LOCALIZED_CHANGE

    def _qualifies_as_trivial_patch(self, request: RequestSignals) -> bool:
        if not (self.policy.allow_trivial_patch_bypass and request.explicit_trivial_patch):
            return False
        return not any(
            (
                request.user_visible_behavior_change,
                request.new_states_or_errors,
                request.ux_surface_change,
                request.accessibility_impact,
                request.design_system_impact,
                request.cross_role_dependency,
                request.structural_change,
                request.ambiguous_intent,
                request.data_contract_change,
                request.freshness_or_polling_change,
                request.persistence_or_telemetry_change,
                request.qa_structural_failure,
            )
        )

    @staticmethod
    def _review_scope(classification: Classification) -> ReviewScope:
        if classification in (Classification.FEATURE_FLOW, Classification.STRUCTURAL_INITIATIVE):
            return ReviewScope.BROAD_REVIEW
        return ReviewScope.LOCALIZED_CORRECTION

    def _build_assumptions(
        self, request: RequestSignals, classification: Classification
    ) -> tuple[str, ...]:
        assumptions = [
            "Lead remains the only intake authority for this request cycle.",
            "The request should stay glasses-first, glanceable, and battery-aware by default.",
            f"The request is currently being handled in `{request.task_mode.value}` mode.",
        ]
        if classification == Classification.TRIVIAL_PATCH:
            assumptions.append(
                "The change is tightly localized, reversible, and does not create product, UX, market-data, or governance impact."
            )
        else:
            assumptions.append(
                "Implementation should not reinterpret missing product, UX/UI, or market-data premises."
            )
        if request.freshness_or_polling_change:
            assumptions.append(
                "Refresh policy changes must be weighed against battery cost and source guarantees."
            )
        return tuple(assumptions)

    def _build_risks(
        self, request: RequestSignals, classification: Classification
    ) -> tuple[str, ...]:
        risks = list(request.unresolved_risks)
        if request.ambiguous_intent:
            risks.append("Competing interpretations can lead to materially different outcomes.")
        if request.cross_role_dependency:
            risks.append("Multiple roles can drift without an explicit routing narrative and next owner.")
        if request.new_states_or_errors:
            risks.append("New states or error handling can expand acceptance criteria and regression surface.")
        if request.freshness_or_polling_change:
            risks.append("Polling or freshness changes can harm battery life or exceed upstream guarantees.")
        if request.data_contract_change:
            risks.append("Data-contract changes can silently alter quote semantics or recovery behavior.")
        if classification == Classification.STRUCTURAL_INITIATIVE:
            risks.append("Structural work can trigger hidden blast radius and should not be treated as localized.")
        if not risks:
            risks.append("No material risk beyond routine execution is currently flagged.")
        return tuple(risks)

    def _build_gate_sequence(
        self, request: RequestSignals, classification: Classification
    ) -> tuple[Gate, ...]:
        gates = [Gate.UNDERSTANDING_PLAN]
        if self.policy.mandatory_human_review and classification != Classification.TRIVIAL_PATCH:
            gates.append(Gate.HUMAN_REVIEW)
        gates.extend(
            [
                Gate.OPERATIONAL_SPECIFICATION,
                Gate.IMPLEMENTATION,
                Gate.VALIDATION,
                Gate.DOCUMENTARY_CONSOLIDATION,
            ]
        )
        return tuple(gates)

    def _build_activations(
        self, request: RequestSignals, classification: Classification
    ) -> tuple[AgentActivation, ...]:
        return (
            AgentActivation(
                role=AgentRole.LEAD,
                depth=ParticipationDepth.DEEP_ANALYSIS,
                rationale="Lead owns intake, classification, gate opening, and routing for every request.",
            ),
            self._product_activation(request, classification),
            self._ux_activation(request, classification),
            self._market_data_activation(request, classification),
            self._engineer_activation(classification),
            self._qa_activation(classification),
            self._documentation_activation(classification),
        )

    def _build_recommendation(
        self, request: RequestSignals, classification: Classification
    ) -> NextStepRecommendation:
        if classification == Classification.TRIVIAL_PATCH:
            return NextStepRecommendation(
                next_role=AgentRole.ENGINEER,
                reasoning_effort=ReasoningEffort.LOW,
                expected_depth=ParticipationDepth.LIGHT_VALIDATION,
                expected_output="Localized implementation note with exact delta, constraints respected, and no scope expansion.",
            )
        if self._pure_contract_review(request):
            return NextStepRecommendation(
                next_role=AgentRole.DOCUMENTATION,
                reasoning_effort=ReasoningEffort.MEDIUM,
                expected_depth=ParticipationDepth.DEEP_ANALYSIS,
                expected_output="Governance-focused contract review, bounded wording changes, and explicit keep/discard reasoning for affected rules.",
            )
        if self._product_needs_deep_analysis(request, classification):
            return NextStepRecommendation(
                next_role=AgentRole.PRODUCT,
                reasoning_effort=self._reasoning_effort(classification, request),
                expected_depth=ParticipationDepth.DEEP_ANALYSIS,
                expected_output="Operational product premises, explicit state map, and clarified scope boundaries.",
            )
        if self._ux_needs_deep_analysis(request, classification):
            return NextStepRecommendation(
                next_role=AgentRole.UX_UI,
                reasoning_effort=self._reasoning_effort(classification, request),
                expected_depth=ParticipationDepth.DEEP_ANALYSIS,
                expected_output="Glanceability, accessibility, battery-aware flow guidance, and XR surface implications.",
            )
        if self._market_data_needs_deep_analysis(request, classification):
            return NextStepRecommendation(
                next_role=AgentRole.MARKET_DATA,
                reasoning_effort=self._reasoning_effort(classification, request),
                expected_depth=ParticipationDepth.DEEP_ANALYSIS,
                expected_output="Data-source, freshness, polling, symbol, and recovery-semantics guidance.",
            )
        return NextStepRecommendation(
            next_role=AgentRole.ENGINEER,
            reasoning_effort=self._reasoning_effort(classification, request),
            expected_depth=ParticipationDepth.DEEP_ANALYSIS
            if classification in (Classification.FEATURE_FLOW, Classification.STRUCTURAL_INITIATIVE)
            else ParticipationDepth.LIGHT_VALIDATION,
            expected_output="Implementation-ready execution path aligned with approved plan and explicit constraints.",
        )

    def _reasoning_effort(
        self, classification: Classification, request: RequestSignals
    ) -> ReasoningEffort:
        if classification == Classification.TRIVIAL_PATCH:
            return ReasoningEffort.LOW
        if classification == Classification.STRUCTURAL_INITIATIVE:
            return ReasoningEffort.DEEP
        if any(
            (
                request.ambiguous_intent,
                request.cross_role_dependency,
                request.new_states_or_errors,
                request.data_contract_change,
                request.freshness_or_polling_change,
            )
        ):
            return ReasoningEffort.HIGH
        return ReasoningEffort.MEDIUM

    def _product_activation(
        self, request: RequestSignals, classification: Classification
    ) -> AgentActivation:
        if self._product_needs_deep_analysis(request, classification):
            return AgentActivation(
                role=AgentRole.PRODUCT,
                depth=ParticipationDepth.DEEP_ANALYSIS,
                rationale="Product owns unresolved behavior, state mapping, and accepted scope before engineering starts.",
            )
        if classification == Classification.LOCALIZED_CHANGE:
            return AgentActivation(
                role=AgentRole.PRODUCT,
                depth=ParticipationDepth.LIGHT_VALIDATION,
                rationale="Product should confirm no hidden behavior drift exists in an otherwise bounded change.",
            )
        return AgentActivation(
            role=AgentRole.PRODUCT,
            depth=ParticipationDepth.NO_IMPACT_CONFIRMATION,
            rationale="No material product ambiguity is currently signaled.",
        )

    def _ux_activation(
        self, request: RequestSignals, classification: Classification
    ) -> AgentActivation:
        if self._ux_needs_deep_analysis(request, classification):
            return AgentActivation(
                role=AgentRole.UX_UI,
                depth=ParticipationDepth.DEEP_ANALYSIS,
                rationale="UX/UI owns flow clarity, glanceability, accessibility, and battery-aware rendering implications.",
            )
        if classification in (Classification.LOCALIZED_CHANGE, Classification.TRIVIAL_PATCH):
            return AgentActivation(
                role=AgentRole.UX_UI,
                depth=ParticipationDepth.LIGHT_VALIDATION,
                rationale="UX/UI should confirm the change does not create silent readability or consistency regressions.",
            )
        return AgentActivation(
            role=AgentRole.UX_UI,
            depth=ParticipationDepth.NO_IMPACT_CONFIRMATION,
            rationale="No explicit experience or interface impact is currently signaled.",
        )

    def _market_data_activation(
        self, request: RequestSignals, classification: Classification
    ) -> AgentActivation:
        if self._market_data_needs_deep_analysis(request, classification):
            return AgentActivation(
                role=AgentRole.MARKET_DATA,
                depth=ParticipationDepth.DEEP_ANALYSIS,
                rationale="Market Data owns source guarantees, polling constraints, symbol semantics, and historical-data tradeoffs.",
            )
        if request.local_failure_only:
            return AgentActivation(
                role=AgentRole.MARKET_DATA,
                depth=ParticipationDepth.LIGHT_VALIDATION,
                rationale="Market Data should confirm the issue is not actually caused by quote semantics or freshness assumptions.",
            )
        return AgentActivation(
            role=AgentRole.MARKET_DATA,
            depth=ParticipationDepth.NO_IMPACT_CONFIRMATION,
            rationale="No explicit data-contract or freshness impact is currently signaled.",
        )

    @staticmethod
    def _engineer_activation(classification: Classification) -> AgentActivation:
        if classification == Classification.TRIVIAL_PATCH:
            return AgentActivation(
                role=AgentRole.ENGINEER,
                depth=ParticipationDepth.LIGHT_VALIDATION,
                rationale="Engineer should execute the narrow fix without reopening scope.",
            )
        return AgentActivation(
            role=AgentRole.ENGINEER,
            depth=ParticipationDepth.DEEP_ANALYSIS,
            rationale="Engineer should implement against approved premises and surface technical constraints without expanding scope.",
        )

    @staticmethod
    def _qa_activation(classification: Classification) -> AgentActivation:
        if classification == Classification.TRIVIAL_PATCH:
            return AgentActivation(
                role=AgentRole.QA,
                depth=ParticipationDepth.LIGHT_VALIDATION,
                rationale="QA should confirm the local fix and watch for obvious regressions.",
            )
        if classification == Classification.LOCALIZED_CHANGE:
            return AgentActivation(
                role=AgentRole.QA,
                depth=ParticipationDepth.LIGHT_VALIDATION,
                rationale="QA should validate acceptance and targeted regression risk for the bounded change.",
            )
        return AgentActivation(
            role=AgentRole.QA,
            depth=ParticipationDepth.DEEP_ANALYSIS,
            rationale="QA should validate happy path, edge cases, regressions, and whether failures are local or structural.",
        )

    @staticmethod
    def _documentation_activation(classification: Classification) -> AgentActivation:
        if classification in (
            Classification.FEATURE_FLOW,
            Classification.STRUCTURAL_INITIATIVE,
        ):
            return AgentActivation(
                role=AgentRole.DOCUMENTATION,
                depth=ParticipationDepth.DEEP_ANALYSIS,
                rationale="Documentation / Historian must reconcile role outputs into an accurate internal truth record.",
            )
        return AgentActivation(
            role=AgentRole.DOCUMENTATION,
            depth=ParticipationDepth.LIGHT_VALIDATION,
            rationale="Documentation / Historian should capture the outcome in a concise internal record.",
        )

    @staticmethod
    def _product_needs_deep_analysis(
        request: RequestSignals, classification: Classification
    ) -> bool:
        if request.task_mode == TaskMode.REVIEW and request.structural_change:
            return any(
                (
                    request.user_visible_behavior_change,
                    request.new_states_or_errors,
                    request.ambiguous_intent,
                )
            )
        return classification in (
            Classification.FEATURE_FLOW,
            Classification.STRUCTURAL_INITIATIVE,
        ) or request.ambiguous_intent

    @staticmethod
    def _ux_needs_deep_analysis(
        request: RequestSignals, classification: Classification
    ) -> bool:
        if request.task_mode == TaskMode.REVIEW and request.structural_change:
            return any(
                (
                    request.ux_surface_change,
                    request.accessibility_impact,
                    request.design_system_impact,
                )
            )
        return any(
            (
                request.ux_surface_change,
                request.accessibility_impact,
                request.design_system_impact,
            )
        ) or (
            classification == Classification.FEATURE_FLOW and request.user_visible_behavior_change
        )

    @staticmethod
    def _market_data_needs_deep_analysis(
        request: RequestSignals, classification: Classification
    ) -> bool:
        if request.task_mode == TaskMode.REVIEW and request.structural_change:
            return any(
                (
                    request.data_contract_change,
                    request.freshness_or_polling_change,
                )
            )
        return classification == Classification.STRUCTURAL_INITIATIVE or any(
            (
                request.data_contract_change,
                request.freshness_or_polling_change,
            )
        )

    @staticmethod
    def _pure_contract_review(request: RequestSignals) -> bool:
        return (
            request.task_mode == TaskMode.REVIEW
            and request.structural_change
            and not any(
                (
                    request.user_visible_behavior_change,
                    request.new_states_or_errors,
                    request.ux_surface_change,
                    request.accessibility_impact,
                    request.design_system_impact,
                    request.data_contract_change,
                    request.freshness_or_polling_change,
                    request.persistence_or_telemetry_change,
                )
            )
        )


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_request_signals(payload: dict[str, Any]) -> RequestSignals:
    return RequestSignals(
        request_summary=payload["request_summary"],
        lead_interpretation=payload["lead_interpretation"],
        task_mode=TaskMode(payload.get("task_mode", TaskMode.IMPLEMENTATION.value)),
        explicit_trivial_patch=payload.get("explicit_trivial_patch", False),
        user_visible_behavior_change=payload.get("user_visible_behavior_change", False),
        new_states_or_errors=payload.get("new_states_or_errors", False),
        ux_surface_change=payload.get("ux_surface_change", False),
        accessibility_impact=payload.get("accessibility_impact", False),
        design_system_impact=payload.get("design_system_impact", False),
        cross_role_dependency=payload.get("cross_role_dependency", False),
        structural_change=payload.get("structural_change", False),
        ambiguous_intent=payload.get("ambiguous_intent", False),
        data_contract_change=payload.get("data_contract_change", False),
        freshness_or_polling_change=payload.get("freshness_or_polling_change", False),
        persistence_or_telemetry_change=payload.get("persistence_or_telemetry_change", False),
        local_failure_only=payload.get("local_failure_only", False),
        qa_structural_failure=payload.get("qa_structural_failure", False),
        approved_reports=tuple(payload.get("approved_reports", ())),
        open_decisions=tuple(payload.get("open_decisions", ())),
        unresolved_risks=tuple(payload.get("unresolved_risks", ())),
        human_overrides=tuple(payload.get("human_overrides", ())),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lead / Orchestrator operational engine for intake routing."
    )
    parser.add_argument("input", type=Path, help="Path to a JSON file containing RequestSignals data.")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format for the generated report.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    orchestrator = LeadOrchestrator()
    report = orchestrator.build_intake_report(_build_request_signals(_load_json(args.input)))
    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2))
        return
    print(report.to_markdown())


if __name__ == "__main__":
    main()
