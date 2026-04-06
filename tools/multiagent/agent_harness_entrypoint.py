from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "run"


def _unique_items(items: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return tuple(ordered)


@dataclass(slots=True, frozen=True)
class BenchmarkSuite:
    name: str
    file_path: str
    target_surface: str
    benchmark_suite: tuple[str, ...]
    success_criteria: tuple[str, ...]

    @classmethod
    def from_file(cls, path: Path) -> "BenchmarkSuite":
        payload = json.loads(path.read_text(encoding="utf-8"))
        benchmarks = payload.get("benchmarks", [])
        labels = _unique_items([item["id"] for item in benchmarks])
        criteria = _unique_items(
            [
                criterion
                for item in benchmarks
                for criterion in item.get("success_criteria", [])
            ]
        )
        return cls(
            name=payload["suite_name"],
            file_path=str(path),
            target_surface=payload["target_surface"],
            benchmark_suite=labels,
            success_criteria=criteria,
        )


@dataclass(slots=True, frozen=True)
class AgentHarnessBootstrapResult:
    run_tag: str
    persisted: bool
    run_dir: str
    context_path: str
    results_path: str
    notes_path: str
    target_surface: str
    suite_name: str | None = None
    suite_file: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentHarnessEntrypoint:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()
        self.runtime_root = self._runtime_root()

    def bootstrap(
        self,
        *,
        run_tag: str,
        target_surface: str,
        benchmark_suite: tuple[str, ...],
        success_criteria: tuple[str, ...],
        suite_name: str | None = None,
        suite_file: str | None = None,
        hypothesis: str | None = None,
        persist_mode: str = "auto",
    ) -> AgentHarnessBootstrapResult:
        should_persist = persist_mode != "never"
        normalized_tag = slugify(run_tag)
        run_dir = self.runtime_root / "agent_harness" / normalized_tag
        context_path = run_dir / "run_context.json"
        results_path = run_dir / "results.tsv"
        notes_path = run_dir / "notes.md"

        if should_persist and run_dir.exists():
            raise FileExistsError(f"Agent harness run already exists: {run_dir}")

        if should_persist:
            run_dir.mkdir(parents=True, exist_ok=False)
            context_path.write_text(
                json.dumps(
                    {
                        "run_tag": normalized_tag,
                        "target_surface": target_surface,
                        "suite_name": suite_name,
                        "suite_file": suite_file,
                        "benchmark_suite": list(benchmark_suite),
                        "success_criteria": list(success_criteria),
                        "hypothesis": hypothesis or "",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            results_path.write_text(
                "candidate\toverall_score\tstatus\tchanged_surface\tdescription\n",
                encoding="utf-8",
            )
            notes_path.write_text(
                self._notes_template(
                    run_tag=normalized_tag,
                    target_surface=target_surface,
                    suite_name=suite_name,
                    suite_file=suite_file,
                    benchmark_suite=benchmark_suite,
                    success_criteria=success_criteria,
                    hypothesis=hypothesis,
                ),
                encoding="utf-8",
            )

        return AgentHarnessBootstrapResult(
            run_tag=normalized_tag,
            persisted=should_persist,
            run_dir=str(run_dir),
            context_path=str(context_path),
            results_path=str(results_path),
            notes_path=str(notes_path),
            target_surface=target_surface,
            suite_name=suite_name,
            suite_file=suite_file,
        )

    def _runtime_root(self) -> Path:
        base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        return base / "CodexLead" / self.root.name

    @staticmethod
    def _notes_template(
        *,
        run_tag: str,
        target_surface: str,
        suite_name: str | None,
        suite_file: str | None,
        benchmark_suite: tuple[str, ...],
        success_criteria: tuple[str, ...],
        hypothesis: str | None,
    ) -> str:
        benchmarks = "\n".join(f"- {item}" for item in benchmark_suite) or "- None"
        criteria = "\n".join(f"- {item}" for item in success_criteria) or "- None"
        hypothesis_block = hypothesis or "No explicit hypothesis recorded yet."
        suite_lines = []
        if suite_name:
            suite_lines.append(f"- Suite name: `{suite_name}`")
        if suite_file:
            suite_lines.append(f"- Suite file: `{suite_file}`")
        if not suite_lines:
            suite_lines.append("- None")
        suite_block = "\n".join(suite_lines)
        return (
            f"# Agent Harness Run: {run_tag}\n\n"
            "## Target Surface\n"
            f"- `{target_surface}`\n\n"
            "## Loaded Suite\n"
            f"{suite_block}\n\n"
            "## Benchmark Suite\n"
            f"{benchmarks}\n\n"
            "## Success Criteria\n"
            f"{criteria}\n\n"
            "## Hypothesis\n"
            f"{hypothesis_block}\n\n"
            "## Run Rules\n"
            "- Record the baseline first.\n"
            "- Change one mutable surface at a time.\n"
            "- Keep the benchmark suite fixed for this run.\n"
            "- Keep the change only if the score improves, or if the score holds and the contract is simpler.\n"
            "- Discard regressions instead of accumulating prompt bloat.\n\n"
            "## Candidate Decision\n"
            "- Decision: `pending`\n"
            "- Allowed values: `keep` or `discard`\n"
            "- Reason:\n"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap an autoresearch-style agent harness iteration run."
    )
    parser.add_argument("run_tag", help="Run tag for the harness iteration, for example 'lead-clarity-apr5'.")
    parser.add_argument(
        "--target-surface",
        help="Single agent surface to improve, for example 'docs/agents/product-strategist.md'.",
    )
    parser.add_argument(
        "--suite-file",
        help="Optional benchmark suite JSON file. If provided, it can supply the target surface, benchmark labels, and success criteria.",
    )
    parser.add_argument(
        "--benchmark",
        action="append",
        default=[],
        help="Benchmark label to keep fixed for the run. Repeat the flag to add multiple benchmarks.",
    )
    parser.add_argument(
        "--criterion",
        action="append",
        default=[],
        help="Success criterion for the run. Repeat the flag to add multiple criteria.",
    )
    parser.add_argument(
        "--hypothesis",
        help="Short hypothesis about what the harness change should improve.",
    )
    parser.add_argument(
        "--persist",
        choices=("auto", "always", "never"),
        default="auto",
        help="Whether to persist the run into runtime state.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="text",
        help="Output format.",
    )
    return parser


def _render_result(result: AgentHarnessBootstrapResult) -> str:
    suite_lines = []
    if result.suite_name:
        suite_lines.append(f"- Suite name: {result.suite_name}")
    if result.suite_file:
        suite_lines.append(f"- Suite file: {result.suite_file}")
    return "\n".join(
        [
            "Agent harness bootstrap completed.",
            f"- Run tag: {result.run_tag}",
            f"- Target surface: {result.target_surface}",
            *suite_lines,
            f"- Persisted: {'yes' if result.persisted else 'no'}",
            f"- Run directory: {result.run_dir}",
            f"- Context: {result.context_path}",
            f"- Results TSV: {result.results_path}",
            f"- Notes: {result.notes_path}",
        ]
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    entrypoint = AgentHarnessEntrypoint()
    suite: BenchmarkSuite | None = None
    if args.suite_file:
        suite = BenchmarkSuite.from_file(Path(args.suite_file))
    target_surface = args.target_surface or (suite.target_surface if suite else None)
    if not target_surface:
        parser.error("--target-surface is required unless --suite-file provides one.")
    benchmark_suite = _unique_items(
        list(suite.benchmark_suite if suite else ()) + list(args.benchmark)
    )
    success_criteria = _unique_items(
        list(suite.success_criteria if suite else ()) + list(args.criterion)
    )
    result = entrypoint.bootstrap(
        run_tag=args.run_tag,
        target_surface=target_surface,
        suite_name=suite.name if suite else None,
        suite_file=suite.file_path if suite else None,
        benchmark_suite=benchmark_suite,
        success_criteria=success_criteria,
        hypothesis=args.hypothesis,
        persist_mode=args.persist,
    )
    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
        return
    print(_render_result(result))


if __name__ == "__main__":
    main()
