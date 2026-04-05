#!/usr/bin/env python3
"""Record optional local workflow session logs for maintainers."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = Path(tempfile.gettempdir()) / "codex-workflow-session-recordings"


def ensure_output_dir(path: Path, *, allow_in_repo: bool = False) -> Path:
    resolved = path.resolve()
    if not allow_in_repo and (resolved == ROOT or ROOT in resolved.parents):
        raise ValueError("Session recorder output must stay outside the repository unless explicitly allowed")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def make_payload(args: argparse.Namespace) -> dict[str, object]:
    created_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    return {
        "version": 1,
        "contractual": False,
        "created_at": created_at,
        "label": args.label,
        "feature": args.feature,
        "notes": args.note,
        "prompts": args.prompt or [],
        "tool_actions": args.tool_action or [],
        "outputs": args.output or [],
    }


def record_session(args: argparse.Namespace) -> Path:
    output_dir = ensure_output_dir(
        Path(args.output_dir).resolve() if args.output_dir else DEFAULT_OUTPUT_DIR,
        allow_in_repo=args.allow_inside_repo,
    )
    payload = make_payload(args)
    label = args.label or "workflow-session"
    safe_label = "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in label).strip("-")
    filename = f"{safe_label or 'workflow-session'}-{payload['created_at'].replace(':', '').replace('+00:00', 'Z')}.json"
    destination = output_dir / filename
    destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="workflow-session", help="Short label for the recording")
    parser.add_argument("--feature", help="Optional feature or workstream name")
    parser.add_argument("--output-dir", help="Directory for local recorder output; defaults to a temp-based diagnostics directory")
    parser.add_argument("--allow-inside-repo", action="store_true", default=False)
    parser.add_argument("--note", action="append", default=[], help="Optional maintainer notes")
    parser.add_argument("--prompt", action="append", default=[], help="Prompt text to record")
    parser.add_argument("--tool-action", action="append", default=[], help="Tool action summary to record")
    parser.add_argument("--output", action="append", default=[], help="Assistant or tool output summary to record")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        path = record_session(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Recorded optional workflow session: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
