from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


@dataclass(slots=True, frozen=True)
class BenchmarkResult:
    benchmark_id: str
    role: str
    score: float
    weight: float
    matched_signals: tuple[str, ...]
    missing_signal_groups: tuple[tuple[str, ...], ...]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["matched_signals"] = list(self.matched_signals)
        payload["missing_signal_groups"] = [list(group) for group in self.missing_signal_groups]
        return payload


@dataclass(slots=True, frozen=True)
class RoleResult:
    role: str
    contract_path: str
    score: float
    weight: float
    benchmark_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["benchmark_ids"] = list(self.benchmark_ids)
        return payload


@dataclass(slots=True, frozen=True)
class ScoreSummary:
    suite_name: str
    suite_version: str
    overall_score: float
    passing_score: float
    status: str
    benchmark_results: tuple[BenchmarkResult, ...]
    role_results: tuple[RoleResult, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "suite_name": self.suite_name,
            "suite_version": self.suite_version,
            "overall_score": self.overall_score,
            "passing_score": self.passing_score,
            "status": self.status,
            "benchmark_results": [item.to_dict() for item in self.benchmark_results],
            "role_results": [item.to_dict() for item in self.role_results],
        }


class AgentHarnessScorer:
    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = repo_root or Path.cwd()

    def score_suite(self, suite_path: Path) -> ScoreSummary:
        payload = json.loads(suite_path.read_text(encoding="utf-8"))
        role_contracts: dict[str, str] = payload.get("role_contracts", {})
        shared_contract_paths: tuple[str, ...] = tuple(payload.get("shared_contract_paths", ("AGENTS.md",)))
        role_weights: dict[str, float] = {
            role: float(weight) for role, weight in payload.get("role_weights", {}).items()
        }
        passing_score = float(payload.get("passing_score", 75.0))
        benchmark_results: list[BenchmarkResult] = []
        role_to_weighted_scores: dict[str, list[tuple[float, float]]] = {}
        role_to_benchmarks: dict[str, list[str]] = {}

        contract_cache: dict[str, str] = {}
        for role, contract_rel_path in role_contracts.items():
            contract_cache[role] = self._load_combined_text(shared_contract_paths + (contract_rel_path,))

        for benchmark in payload.get("benchmarks", []):
            role = benchmark["target_role"]
            benchmark_weight = float(benchmark.get("weight", role_weights.get(role, 1.0)))
            source_paths = benchmark.get("contract_paths")
            if source_paths:
                contract_text = self._load_combined_text(tuple(source_paths))
            else:
                contract_text = contract_cache[role]
            signal_groups = benchmark.get("signal_groups", [])
            matched_signals: list[str] = []
            missing_groups: list[tuple[str, ...]] = []
            matched_groups = 0
            for raw_group in signal_groups:
                group = tuple(_normalize(signal) for signal in raw_group)
                match = next((signal for signal in group if signal in contract_text), None)
                if match:
                    matched_groups += 1
                    matched_signals.append(match)
                    continue
                missing_groups.append(group)
            score = 100.0 if not signal_groups else round((matched_groups / len(signal_groups)) * 100.0, 1)
            benchmark_results.append(
                BenchmarkResult(
                    benchmark_id=benchmark["id"],
                    role=role,
                    score=score,
                    weight=benchmark_weight,
                    matched_signals=tuple(matched_signals),
                    missing_signal_groups=tuple(missing_groups),
                )
            )
            role_to_weighted_scores.setdefault(role, []).append((score, benchmark_weight))
            role_to_benchmarks.setdefault(role, []).append(benchmark["id"])

        role_results = tuple(
            RoleResult(
                role=role,
                contract_path=role_contracts[role],
                score=self._weighted_average(scores),
                weight=role_weights.get(role, 1.0),
                benchmark_ids=tuple(role_to_benchmarks[role]),
            )
            for role, scores in role_to_weighted_scores.items()
        )
        overall_score = self._weighted_average(
            [(result.score, result.weight) for result in benchmark_results]
        )
        status = "keep" if overall_score >= passing_score else "needs-work"
        return ScoreSummary(
            suite_name=payload["suite_name"],
            suite_version=str(payload.get("version", "0")),
            overall_score=overall_score,
            passing_score=passing_score,
            status=status,
            benchmark_results=tuple(benchmark_results),
            role_results=role_results,
        )

    def _load_combined_text(self, contract_paths: tuple[str, ...]) -> str:
        return "\n".join(
            _normalize((self.repo_root / contract_path).read_text(encoding="utf-8"))
            for contract_path in contract_paths
        )

    @staticmethod
    def _weighted_average(values: list[tuple[float, float]]) -> float:
        if not values:
            return 0.0
        total_weight = sum(weight for _, weight in values)
        if total_weight <= 0:
            return 0.0
        return round(sum(score * weight for score, weight in values) / total_weight, 1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Score agent contracts against a benchmark suite using configurable signal groups."
    )
    parser.add_argument(
        "--suite-file",
        required=True,
        help="Benchmark suite JSON with role_contracts and signal_groups.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="text",
        help="Output format.",
    )
    return parser


def _render_text(summary: ScoreSummary) -> str:
    weakest = sorted(summary.benchmark_results, key=lambda item: item.score)[:3]
    weakest_lines = [
        f"- {item.benchmark_id} ({item.role}, w={item.weight:.1f}): {item.score:.1f}"
        for item in weakest
    ]
    return "\n".join(
        [
            "Agent harness score completed.",
            f"- Suite: {summary.suite_name} v{summary.suite_version}",
            f"- Overall score: {summary.overall_score:.1f}",
            f"- Passing score: {summary.passing_score:.1f}",
            f"- Status: {summary.status}",
            "- Weakest benchmarks:",
            *weakest_lines,
        ]
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    scorer = AgentHarnessScorer()
    summary = scorer.score_suite(Path(args.suite_file))
    if args.format == "json":
        print(json.dumps(summary.to_dict(), indent=2))
        return
    print(_render_text(summary))


if __name__ == "__main__":
    main()
