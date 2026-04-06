from __future__ import annotations

import argparse
import json
from pathlib import Path

from lead_entrypoint import LeadEntrypoint


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Persist a role report into the active CodexLead request state."
    )
    parser.add_argument("role", help="Role name, for example 'QA' or 'Engineer'.")
    parser.add_argument("report_file", type=Path, help="Path to a markdown role report.")
    parser.add_argument(
        "--persist",
        choices=("auto", "always", "never"),
        default="auto",
        help="Whether to persist the report into the active request state.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="text",
        help="Output format for the persistence result.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    entrypoint = LeadEntrypoint()
    content = args.report_file.read_text(encoding="utf-8")
    result = entrypoint.persist_role_report(
        role=args.role,
        content=content,
        persist_mode=args.persist,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2))
        return
    print(
        "\n".join(
            [
                "Role report persisted.",
                f"- Role: {result['role']}",
                f"- Persisted: {'yes' if result['persisted'] else 'no'}",
                f"- Latest report path: {result['latest_path']}",
                f"- Timestamped report path: {result['report_path']}",
            ]
        )
    )


if __name__ == "__main__":
    main()
