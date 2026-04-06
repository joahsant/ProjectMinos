from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from agent_harness_entrypoint import AgentHarnessEntrypoint, BenchmarkSuite
from agent_harness_scorer import AgentHarnessScorer, ScoreSummary


@dataclass(slots=True, frozen=True)
class CycleResult:
    run_tag: str
    run_dir: str
    overall_score: float
    status: str
    candidate: str
    compared_to: str | None = None
    compared_score: float | None = None
    delta: float | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _read_latest_score(results_path: Path) -> float | None:
    if not results_path.exists():
        return None
    lines = [line.strip() for line in results_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 2:
        return None
    latest = lines[-1].split("\t")
    if len(latest) < 2:
        return None
    return float(latest[1])


def _append_result(results_path: Path, candidate: str, summary: ScoreSummary) -> None:
    with results_path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"{candidate}\t{summary.overall_score:.1f}\t{summary.status}\tdocs/agents/\t"
            "Automatic contract score using suite signal groups.\n"
        )


def _append_notes(notes_path: Path, summary: ScoreSummary, compared_to: str | None, compared_score: float | None) -> None:
    weakest = sorted(summary.benchmark_results, key=lambda item: item.score)[:3]
    strongest = sorted(summary.benchmark_results, key=lambda item: item.score, reverse=True)[:3]
    existing = notes_path.read_text(encoding="utf-8")
    decision_block = (
        "## Candidate Decision\n"
        f"- Decision: `{summary.status}`\n"
        "- Allowed values: `keep` or `discard`\n"
        f"- Reason: Automatic score summary recommends `{summary.status}` based on the current suite.\n"
    )
    if "## Candidate Decision" in existing:
        before, _, after = existing.partition("## Candidate Decision")
        _, _, remainder = after.partition("## Automatic Score Summary")
        existing = before + decision_block
        if remainder:
            existing += "\n## Automatic Score Summary" + remainder
    else:
        existing = existing.rstrip() + "\n\n" + decision_block + "\n"
    lines = [
        "",
        "## Automatic Score Summary",
        f"- Overall score: `{summary.overall_score:.1f}`",
        f"- Passing score: `{summary.passing_score:.1f}`",
        f"- Status: `{summary.status}`",
        f"- Decision recommendation: `{summary.status}`",
    ]
    if compared_to and compared_score is not None:
        delta = round(summary.overall_score - compared_score, 1)
        lines.extend(
            [
                f"- Compared run: `{compared_to}`",
                f"- Previous score: `{compared_score:.1f}`",
                f"- Delta: `{delta:+.1f}`",
            ]
        )
    lines.extend(
        [
            "",
            "### Strongest Benchmarks",
            *[f"- `{item.benchmark_id}` (`{item.role}`): `{item.score:.1f}`" for item in strongest],
            "",
            "### Weakest Benchmarks",
            *[f"- `{item.benchmark_id}` (`{item.role}`): `{item.score:.1f}`" for item in weakest],
        ]
    )
    if "## Automatic Score Summary" in existing:
        existing = existing.split("## Automatic Score Summary")[0].rstrip() + "\n"
    notes_path.write_text(existing + "\n".join(lines) + "\n", encoding="utf-8")


def run_cycle(
    *,
    repo_root: Path,
    run_tag: str,
    suite_file: Path,
    candidate: str,
    hypothesis: str | None,
    compare_run_tag: str | None,
    persist_mode: str,
) -> CycleResult:
    suite = BenchmarkSuite.from_file(suite_file)
    entrypoint = AgentHarnessEntrypoint(repo_root)
    bootstrap_result = entrypoint.bootstrap(
        run_tag=run_tag,
        target_surface=suite.target_surface,
        suite_name=suite.name,
        suite_file=str(suite_file),
        benchmark_suite=suite.benchmark_suite,
        success_criteria=suite.success_criteria,
        hypothesis=hypothesis,
        persist_mode=persist_mode,
    )
    scorer = AgentHarnessScorer(repo_root)
    score_summary = scorer.score_suite(suite_file)

    compared_score = None
    compared_to = None
    if compare_run_tag:
        compare_results = Path(entrypoint.runtime_root) / "agent_harness" / compare_run_tag / "results.tsv"
        compared_score = _read_latest_score(compare_results)
        compared_to = compare_run_tag

    if bootstrap_result.persisted:
        _append_result(Path(bootstrap_result.results_path), candidate, score_summary)
        _append_notes(Path(bootstrap_result.notes_path), score_summary, compared_to, compared_score)

    delta = None if compared_score is None else round(score_summary.overall_score - compared_score, 1)
    return CycleResult(
        run_tag=bootstrap_result.run_tag,
        run_dir=bootstrap_result.run_dir,
        overall_score=score_summary.overall_score,
        status=score_summary.status,
        candidate=candidate,
        compared_to=compared_to,
        compared_score=compared_score,
        delta=delta,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a full agent-harness cycle: bootstrap a run, score it automatically, and persist notes."
    )
    parser.add_argument("run_tag", help="Run tag for the cycle.")
    parser.add_argument("--suite-file", required=True, help="Benchmark suite JSON file.")
    parser.add_argument("--candidate", default="auto-score", help="Candidate name recorded in results.tsv.")
    parser.add_argument("--hypothesis", help="Optional hypothesis recorded in notes.")
    parser.add_argument("--compare-run-tag", help="Optional previous run tag for delta reporting.")
    parser.add_argument(
        "--persist",
        choices=("auto", "always", "never"),
        default="always",
        help="Whether to persist the run.",
    )
    parser.add_argument("--format", choices=("json", "text"), default="text", help="Output format.")
    return parser


def _render_text(result: CycleResult) -> str:
    lines = [
        "Agent harness cycle completed.",
        f"- Run tag: {result.run_tag}",
        f"- Candidate: {result.candidate}",
        f"- Overall score: {result.overall_score:.1f}",
        f"- Status: {result.status}",
        f"- Run directory: {result.run_dir}",
    ]
    if result.compared_to and result.compared_score is not None and result.delta is not None:
        lines.extend(
            [
                f"- Compared to: {result.compared_to}",
                f"- Previous score: {result.compared_score:.1f}",
                f"- Delta: {result.delta:+.1f}",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = run_cycle(
        repo_root=Path.cwd(),
        run_tag=args.run_tag,
        suite_file=Path(args.suite_file),
        candidate=args.candidate,
        hypothesis=args.hypothesis,
        compare_run_tag=args.compare_run_tag,
        persist_mode=args.persist,
    )
    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
        return
    print(_render_text(result))


if __name__ == "__main__":
    main()
