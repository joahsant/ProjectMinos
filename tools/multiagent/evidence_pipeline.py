from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "artifacts" / "registry.json"
ARTIFACT_ROOT = REPO_ROOT / "artifacts"
DEFAULT_COVERAGE_ROOTS = [
    ARTIFACT_ROOT / "analysis",
    ARTIFACT_ROOT / "emulator",
    ARTIFACT_ROOT / "sdk",
]
DECISIONS_PATH = REPO_ROOT / "docs" / "DECISIONS.md"
FEATURES_PATH = REPO_ROOT / "docs" / "FEATURES.md"
PRD_PATH = REPO_ROOT / "docs" / "PRD.md"

DRIFT_RULES = [
    {
        "decision": "DEC-004 MVP Data Strategy",
        "feature_needles": [
            "The MVP refreshes the quote from the network every 60 seconds.",
            "The MVP is online-only.",
            "The MVP uses Binance public market data as the source of truth.",
        ],
    },
    {
        "decision": "DEC-005 Asset Scope",
        "feature_needles": [
            "The MVP shows the current Bitcoin quote.",
        ],
    },
    {
        "decision": "DEC-007A Interaction Scope",
        "feature_needles": [
            "The MVP is passive read-only on glasses (no gestures).",
        ],
    },
    {
        "decision": "DEC-007B Loading And Retry",
        "feature_needles": [
            "The MVP starts in loading and retries every 5 seconds until the first successful quote arrives.",
        ],
    },
    {
        "decision": "DEC-007C Refresh Failure Behavior",
        "feature_needles": [
            "After the first successful load, failed refreshes clear the visible quote and replace it with the standard loading indicator.",
            "A fresh quote is shown again only after connectivity is re-established and a new successful response arrives.",
        ],
    },
    {
        "decision": "DEC-011 Binance Endpoint Contract",
        "feature_needles": [
            "The MVP uses the Binance single-symbol 24hr ticker response as the canonical market snapshot contract.",
        ],
    },
    {
        "decision": "DEC-013 Implementation Shape",
        "feature_needles": [
            "The current canonical host presentation is the glasses-focused UI, not the earlier baseline comparison layout.",
        ],
    },
    {
        "decision": "DEC-013A Market Value Presentation",
        "feature_needles": [
            "The MVP presents market values using human-readable grouped currency formatting instead of raw exchange strings.",
        ],
    },
]

PRD_DECISION_RULES = [
    {
        "prd_needles": [
            "Asset: `BTC/USDT`",
            "Market data source: Binance public market data",
            "Canonical endpoint: `GET /api/v3/ticker/24hr` for `BTCUSDT`",
        ],
        "decision_needles": [
            "## DEC-005 Asset Scope",
            "The canonical MVP quote pair is BTC/USDT for display and data semantics.",
            "## DEC-011 Binance Endpoint Contract",
            "The canonical MVP endpoint is `GET /api/v3/ticker/24hr` for `BTCUSDT` using the single-symbol path.",
        ],
    },
    {
        "prd_needles": [
            "Refresh cadence after first success: every 60 seconds",
            "Startup behavior: loading state, retry every 5 seconds until first successful quote",
        ],
        "decision_needles": [
            "## DEC-004 MVP Data Strategy",
            "The first MVP quote refresh cadence is 60 seconds.",
            "## DEC-007B Loading And Retry",
            "While the first quote has not loaded yet, the app retries every 5 seconds.",
        ],
    },
    {
        "prd_needles": [
            "Interaction model: passive read-only on glasses",
        ],
        "decision_needles": [
            "## DEC-007A Interaction Scope",
            "MVP is passive read-only.",
        ],
    },
    {
        "prd_needles": [
            "The quote area shows the standard loading indicator while recovery is in progress.",
        ],
        "decision_needles": [
            "## DEC-007C Refresh Failure Behavior",
            "The quote area switches to the standard loading indicator until connectivity is re-established and a fresh value is available.",
        ],
    },
    {
        "prd_needles": [
            "Current development model: Android XR projected experience from a phone-hosted Android app",
        ],
        "decision_needles": [
            "## DEC-003 Platform Direction",
            "The current development assumption is a phone-hosted Android app surface projected to AI glasses during preview-phase tooling.",
        ],
    },
]


@dataclass(frozen=True)
class Bundle:
    bundle_id: str
    kind: str
    status: str
    summary: str
    paths: tuple[Path, ...]
    owner_docs: tuple[Path, ...]


def load_registry_payload() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def load_registry() -> list[Bundle]:
    payload = load_registry_payload()
    bundles: list[Bundle] = []
    for entry in payload.get("bundles", []):
        bundles.append(
            Bundle(
                bundle_id=entry["id"],
                kind=entry["kind"],
                status=entry["status"],
                summary=entry["summary"],
                paths=tuple(REPO_ROOT / path for path in entry["paths"]),
                owner_docs=tuple(REPO_ROOT / path for path in entry["owner_docs"]),
            )
        )
    return bundles


def path_display(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def to_repo_relative(path_value: str) -> str:
    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate.relative_to(REPO_ROOT).as_posix()
    return candidate.as_posix()


def bundle_markers(bundle: Bundle) -> list[str]:
    markers = [bundle.bundle_id]
    markers.extend(path_display(path) for path in bundle.paths)
    return markers


def path_is_covered(target: Path, registered_paths: Iterable[Path]) -> bool:
    for candidate in registered_paths:
        if candidate == target:
            return True
        if candidate.is_dir() and target.is_relative_to(candidate):
            return True
        if target.is_dir() and candidate.is_relative_to(target):
            return True
    return False


def lint_evidence() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not REGISTRY_PATH.exists():
        errors.append("registry missing")
        return errors, warnings

    bundles = load_registry()

    seen_ids: set[str] = set()
    seen_paths: dict[Path, str] = {}

    for bundle in bundles:
        if bundle.bundle_id in seen_ids:
            errors.append(f"duplicate bundle id: {bundle.bundle_id}")
        seen_ids.add(bundle.bundle_id)

        if not bundle.summary.strip():
            errors.append(f"{bundle.bundle_id}: summary is empty")

        if not bundle.paths:
            errors.append(f"{bundle.bundle_id}: no registered paths")

        if not bundle.owner_docs:
            errors.append(f"{bundle.bundle_id}: no owner docs")

        for path in bundle.paths:
            if not path.exists():
                errors.append(f"{bundle.bundle_id}: missing path {path_display(path)}")
                continue
            if not path.is_relative_to(ARTIFACT_ROOT):
                errors.append(f"{bundle.bundle_id}: path outside artifacts {path_display(path)}")
            prior = seen_paths.get(path)
            if prior and prior != bundle.bundle_id:
                warnings.append(
                    f"{bundle.bundle_id}: path {path_display(path)} already registered by {prior}"
                )
            else:
                seen_paths[path] = bundle.bundle_id

        for owner_doc in bundle.owner_docs:
            if not owner_doc.exists():
                errors.append(
                    f"{bundle.bundle_id}: missing owner doc {path_display(owner_doc)}"
                )
                continue
            owner_text = owner_doc.read_text(encoding="utf-8")
            if not any(marker in owner_text for marker in bundle_markers(bundle)):
                errors.append(
                    f"{bundle.bundle_id}: owner docs do not reference bundle id or path "
                    f"({path_display(owner_doc)})"
                )

    registered_paths = [path for bundle in bundles for path in bundle.paths]
    for coverage_root in DEFAULT_COVERAGE_ROOTS:
        if not coverage_root.exists():
            continue
        for child in coverage_root.iterdir():
            if not path_is_covered(child, registered_paths):
                warnings.append(
                    f"uncovered artifact child: {path_display(child)}"
                )

    return errors, warnings


def lint_decision_feature_drift() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    decisions_text = DECISIONS_PATH.read_text(encoding="utf-8")
    features_text = FEATURES_PATH.read_text(encoding="utf-8")

    for rule in DRIFT_RULES:
        decision = rule["decision"]
        if decision not in decisions_text:
            warnings.append(f"drift rule references missing decision heading: {decision}")
            continue
        for needle in rule["feature_needles"]:
            if needle not in features_text:
                errors.append(
                    f"decision/features drift: {decision} expects FEATURES.md to contain "
                    f"'{needle}'"
                )

    if "baseline comparison layout" in features_text and "glasses-focused UI" not in features_text:
        errors.append(
            "decision/features drift: FEATURES.md still implies baseline comparison layout "
            "without affirming glasses-focused UI as canonical"
        )

    return errors, warnings


def lint_prd_decision_drift() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    prd_text = PRD_PATH.read_text(encoding="utf-8")
    decisions_text = DECISIONS_PATH.read_text(encoding="utf-8")

    for rule in PRD_DECISION_RULES:
        prd_matches = [needle for needle in rule["prd_needles"] if needle in prd_text]
        if not prd_matches:
            continue
        for needle in rule["decision_needles"]:
            if needle not in decisions_text:
                errors.append(
                    f"prd/decisions drift: PRD expects DECISIONS.md to contain '{needle}'"
                )

    if "Google AI glasses" in prd_text and "## DEC-003 Platform Direction" not in decisions_text:
        warnings.append(
            "prd/decisions drift: PRD references Google AI glasses but DEC-003 is missing"
        )

    return errors, warnings


def print_findings(errors: list[str], warnings: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"ERROR {error}")
    if warnings:
        for warning in warnings:
            print(f"WARN  {warning}")
    if not errors and not warnings:
        print("OK evidence registry and doc linkage look consistent")
    elif not errors:
        print("OK with warnings")

    return 1 if errors else 0


def lint() -> int:
    errors, warnings = lint_evidence()
    drift_errors, drift_warnings = lint_decision_feature_drift()
    prd_errors, prd_warnings = lint_prd_decision_drift()
    errors.extend(drift_errors)
    errors.extend(prd_errors)
    warnings.extend(drift_warnings)
    warnings.extend(prd_warnings)

    if not errors and not warnings:
        print(
            "OK evidence registry, doc linkage, decision/features drift, and PRD/decisions drift checks look consistent"
        )
        return 0

    return print_findings(errors, warnings)


def summary() -> int:
    bundles = load_registry()
    for bundle in bundles:
        print(f"{bundle.bundle_id} [{bundle.kind}/{bundle.status}]")
        print(f"  summary: {bundle.summary}")
        print(f"  paths: {', '.join(path_display(path) for path in bundle.paths)}")
        print(f"  owner_docs: {', '.join(path_display(doc) for doc in bundle.owner_docs)}")
    return 0


def scaffold(args: argparse.Namespace) -> int:
    if not REGISTRY_PATH.exists():
        print("ERROR registry missing")
        return 1

    payload = load_registry_payload()
    bundles = payload.setdefault("bundles", [])
    if any(entry["id"] == args.id for entry in bundles):
        print(f"ERROR bundle id already exists: {args.id}")
        return 1

    relative_paths = [to_repo_relative(path_value) for path_value in args.path]
    relative_owner_docs = [to_repo_relative(path_value) for path_value in args.owner_doc]

    if args.mkdir:
        for rel_path in relative_paths:
            target = REPO_ROOT / rel_path
            if target.suffix:
                target.parent.mkdir(parents=True, exist_ok=True)
            else:
                target.mkdir(parents=True, exist_ok=True)

    entry = {
        "id": args.id,
        "kind": args.kind,
        "status": args.status,
        "summary": args.summary,
        "paths": relative_paths,
        "owner_docs": relative_owner_docs,
    }
    bundles.append(entry)
    payload["bundles"] = sorted(bundles, key=lambda item: item["id"])
    REGISTRY_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Added bundle {args.id}")
    print(f"  paths: {', '.join(relative_paths)}")
    print(f"  owner_docs: {', '.join(relative_owner_docs)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lightweight evidence registry tools for Project Minos."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "lint",
        help="Validate evidence bundle registration, doc linkage, and decision/features drift.",
    )
    subparsers.add_parser("summary", help="Print the tracked evidence bundle inventory.")
    scaffold_parser = subparsers.add_parser(
        "scaffold",
        help="Append a new evidence bundle entry to artifacts/registry.json.",
    )
    scaffold_parser.add_argument("--id", required=True, help="Bundle id, for example EV-XR-PAIRING-2026-04.")
    scaffold_parser.add_argument("--kind", required=True, help="Bundle kind.")
    scaffold_parser.add_argument("--summary", required=True, help="Short bundle summary.")
    scaffold_parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Repo-relative or absolute bundle path. Repeat for multiple paths.",
    )
    scaffold_parser.add_argument(
        "--owner-doc",
        action="append",
        required=True,
        help="Repo-relative or absolute owner doc path. Repeat for multiple docs.",
    )
    scaffold_parser.add_argument(
        "--status",
        default="active",
        help="Bundle status. Defaults to active.",
    )
    scaffold_parser.add_argument(
        "--mkdir",
        action="store_true",
        help="Create missing directories for the provided paths before registration.",
    )
    args = parser.parse_args()

    if args.command == "lint":
        return lint()
    if args.command == "summary":
        return summary()
    if args.command == "scaffold":
        return scaffold(args)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
