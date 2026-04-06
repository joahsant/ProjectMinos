from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from lead_orchestrator import LeadOrchestrator, RequestSignals, TaskMode


def slugify(text: str, max_words: int = 8) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(words[:max_words]) or "request"


@dataclass(slots=True, frozen=True)
class BootstrapResult:
    request_summary: str
    persisted: bool
    persistence_mode: str
    request_dir: str
    lead_report_path: str
    intake_payload_path: str
    classification: str
    task_mode: str
    next_role: str
    current_gate: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LeadEntrypoint:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()
        self.orchestrator = LeadOrchestrator()
        self.runtime_root = self._runtime_root()

    def bootstrap(
        self,
        request: RequestSignals,
        *,
        persist_mode: str = "auto",
    ) -> BootstrapResult:
        report = self.orchestrator.build_intake_report(request)
        should_persist = self._should_persist(request, persist_mode)
        state_dir = self.runtime_root / "active"
        state_dir.mkdir(parents=True, exist_ok=True)
        lead_report_path = state_dir / "_active_request.md"
        intake_payload_path = state_dir / "_active_intake.json"
        log_path = self.runtime_root / "_request_log.jsonl"

        if should_persist:
            lead_report_path.write_text(report.to_markdown() + "\n", encoding="utf-8")
            intake_payload_path.write_text(
                json.dumps(self._request_payload(request), indent=2) + "\n",
                encoding="utf-8",
            )
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        {
                            "request_summary": request.request_summary,
                            "classification": report.classification.value,
                            "task_mode": report.task_mode.value,
                            "next_role": report.recommendation.next_role.value,
                        }
                    )
                    + "\n"
                )

        return BootstrapResult(
            request_summary=request.request_summary,
            persisted=should_persist,
            persistence_mode="runtime-state",
            request_dir=str(state_dir),
            lead_report_path=str(lead_report_path),
            intake_payload_path=str(intake_payload_path),
            classification=report.classification.value,
            task_mode=report.task_mode.value,
            next_role=report.recommendation.next_role.value,
            current_gate=report.current_gate.value,
        )

    def persist_role_report(
        self,
        *,
        role: str,
        content: str,
        persist_mode: str = "auto",
    ) -> dict[str, Any]:
        should_persist = persist_mode != "never"
        state_dir = self.runtime_root / "active"
        state_dir.mkdir(parents=True, exist_ok=True)
        reports_dir = state_dir / "role_reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        role_slug = slugify(role)
        latest_path = reports_dir / f"{role_slug}.md"
        timestamped_path = reports_dir / f"{role_slug}-{self._timestamp_token()}.md"

        if should_persist:
            rendered = content if content.endswith("\n") else content + "\n"
            latest_path.write_text(rendered, encoding="utf-8")
            timestamped_path.write_text(rendered, encoding="utf-8")

        return {
            "role": role,
            "persisted": should_persist,
            "report_path": str(timestamped_path),
            "latest_path": str(latest_path),
        }

    def _runtime_root(self) -> Path:
        base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        return base / "CodexLead" / self.root.name

    @staticmethod
    def _timestamp_token() -> str:
        return str(time.time_ns())

    @staticmethod
    def _should_persist(request: RequestSignals, persist_mode: str) -> bool:
        if persist_mode == "always":
            return True
        if persist_mode == "never":
            return False
        return any(
            (
                request.cross_role_dependency,
                request.new_states_or_errors,
                request.open_decisions,
                request.unresolved_risks,
                request.human_overrides,
                request.structural_change,
                request.ambiguous_intent,
                request.data_contract_change,
                request.freshness_or_polling_change,
                request.persistence_or_telemetry_change,
                not request.explicit_trivial_patch,
            )
        )

    @staticmethod
    def _request_payload(request: RequestSignals) -> dict[str, Any]:
        return {
            "request_summary": request.request_summary,
            "lead_interpretation": request.lead_interpretation,
            "task_mode": request.task_mode.value,
            "explicit_trivial_patch": request.explicit_trivial_patch,
            "user_visible_behavior_change": request.user_visible_behavior_change,
            "new_states_or_errors": request.new_states_or_errors,
            "ux_surface_change": request.ux_surface_change,
            "accessibility_impact": request.accessibility_impact,
            "design_system_impact": request.design_system_impact,
            "cross_role_dependency": request.cross_role_dependency,
            "structural_change": request.structural_change,
            "ambiguous_intent": request.ambiguous_intent,
            "data_contract_change": request.data_contract_change,
            "freshness_or_polling_change": request.freshness_or_polling_change,
            "persistence_or_telemetry_change": request.persistence_or_telemetry_change,
            "approved_reports": list(request.approved_reports),
            "open_decisions": list(request.open_decisions),
            "unresolved_risks": list(request.unresolved_risks),
            "human_overrides": list(request.human_overrides),
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lead bootstrap entrypoint for starting request cycles in Project Minos."
    )
    parser.add_argument("request_summary", help="Raw request summary to send through Lead intake.")
    parser.add_argument(
        "--lead-interpretation",
        help="Optional explicit Lead interpretation. Defaults to a direct operational reading of the request.",
    )
    parser.add_argument(
        "--task-mode",
        choices=tuple(mode.value for mode in TaskMode),
        default=TaskMode.IMPLEMENTATION.value,
        help="Request handling mode distinct from change classification.",
    )
    parser.add_argument(
        "--persist",
        choices=("auto", "always", "never"),
        default="auto",
        help="Whether to persist active request state to the runtime directory.",
    )
    parser.add_argument("--explicit-trivial-patch", action="store_true")
    parser.add_argument("--user-visible-behavior-change", action="store_true")
    parser.add_argument("--new-states-or-errors", action="store_true")
    parser.add_argument("--ux-surface-change", action="store_true")
    parser.add_argument("--accessibility-impact", action="store_true")
    parser.add_argument("--design-system-impact", action="store_true")
    parser.add_argument("--cross-role-dependency", action="store_true")
    parser.add_argument("--structural-change", action="store_true")
    parser.add_argument("--ambiguous-intent", action="store_true")
    parser.add_argument("--data-contract-change", action="store_true")
    parser.add_argument("--freshness-or-polling-change", action="store_true")
    parser.add_argument("--persistence-or-telemetry-change", action="store_true")
    parser.add_argument("--approved-report", action="append", default=[])
    parser.add_argument("--open-decision", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--human-override", action="append", default=[])
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="text",
        help="Output format for the bootstrap result.",
    )
    return parser


def _build_request_from_args(args: argparse.Namespace) -> RequestSignals:
    interpretation = (
        args.lead_interpretation
        or f"Initial Lead intake for the request: {args.request_summary}"
    )
    return RequestSignals(
        request_summary=args.request_summary,
        lead_interpretation=interpretation,
        task_mode=TaskMode(args.task_mode),
        explicit_trivial_patch=args.explicit_trivial_patch,
        user_visible_behavior_change=args.user_visible_behavior_change,
        new_states_or_errors=args.new_states_or_errors,
        ux_surface_change=args.ux_surface_change,
        accessibility_impact=args.accessibility_impact,
        design_system_impact=args.design_system_impact,
        cross_role_dependency=args.cross_role_dependency,
        structural_change=args.structural_change,
        ambiguous_intent=args.ambiguous_intent,
        data_contract_change=args.data_contract_change,
        freshness_or_polling_change=args.freshness_or_polling_change,
        persistence_or_telemetry_change=args.persistence_or_telemetry_change,
        approved_reports=tuple(args.approved_report),
        open_decisions=tuple(args.open_decision),
        unresolved_risks=tuple(args.risk),
        human_overrides=tuple(args.human_override),
    )


def _render_result(result: BootstrapResult) -> str:
    return "\n".join(
        [
            "Lead bootstrap completed.",
            f"- Request summary: {result.request_summary}",
            f"- Classification: {result.classification}",
            f"- Task mode: {result.task_mode}",
            f"- Current gate: {result.current_gate}",
            f"- Next role: {result.next_role}",
            f"- Persisted: {'yes' if result.persisted else 'no'}",
            f"- Persistence mode: {result.persistence_mode}",
            f"- Request directory: {result.request_dir}",
            f"- Lead report: {result.lead_report_path}",
            f"- Intake payload: {result.intake_payload_path}",
        ]
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    entrypoint = LeadEntrypoint()
    result = entrypoint.bootstrap(
        _build_request_from_args(args),
        persist_mode=args.persist,
    )
    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
        return
    print(_render_result(result))


if __name__ == "__main__":
    main()
