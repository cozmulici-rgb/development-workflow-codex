#!/usr/bin/env python3
"""Compile role-specific workflow context briefs from approved artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROLE_CHOICES = ("planning", "engineering", "validation")
STATUS_LINE_RE = re.compile(r"^\|\s*Status\s*\|\s*`?([^|`]+?)`?\s*\|$", re.MULTILINE)
FRESHNESS_LINE_RE = re.compile(r"^\|\s*Freshness\s*\|\s*`?([^|`]+?)`?\s*\|$", re.MULTILINE)
ARTIFACT_INDEX_ROW_RE = re.compile(
    r"^\|\s*`(?P<artifact>[^`]+)`\s*\|\s*[^|]*\|\s*`?(?P<status>[^|`]+?)`?\s*\|\s*(?P<freshness>[^|]+?)\s*\|",
    re.MULTILINE,
)
INVALID_FEATURE_PART_RE = re.compile(r"[\\/]")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ensure_repo_path(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if ROOT not in resolved.parents and resolved != ROOT:
        raise ValueError(f"{label} resolves outside repo: {path}")
    return resolved


def read_status_value(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = STATUS_LINE_RE.search(load_text(path))
    if not match:
        return None
    return match.group(1).strip().lower()


def read_freshness_value(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = FRESHNESS_LINE_RE.search(load_text(path))
    if not match:
        return None
    return match.group(1).strip().lower()


def validate_feature_name(feature: str) -> str:
    normalized = feature.strip()
    if not normalized:
        raise ValueError("Feature name must not be empty")
    if normalized in {".", ".."} or INVALID_FEATURE_PART_RE.search(normalized) or ".." in normalized:
        raise ValueError(
            "Feature name must be a single directory name under docs/context/<feature>"
        )
    return normalized


def feature_context_dir(feature: str) -> Path:
    return ROOT / "docs" / "context" / feature


def feature_handoff_dir(feature: str) -> Path:
    return ROOT / "docs" / "handoffs" / feature


def role_inputs(feature: str, role: str) -> list[Path]:
    docs_context = feature_context_dir(feature)
    docs_handoffs = feature_handoff_dir(feature)

    common = [
        docs_context / "context-status.md",
    ]
    if role == "planning":
        return common + [
            docs_context / "planning-context.md",
            docs_handoffs / "planning-to-engineering.md",
        ]
    if role == "engineering":
        return common + [
            docs_context / "planning-context.md",
            docs_context / "engineering-context.md",
            docs_handoffs / "planning-to-engineering.md",
        ]
    if role == "validation":
        return common + [
            docs_context / "engineering-context.md",
            docs_context / "validation-context.md",
            docs_handoffs / "engineering-to-validation.md",
        ]
    raise ValueError(f"Unsupported role: {role}")


def role_output(feature: str, role: str) -> Path:
    return feature_context_dir(feature) / f"compiled-{role}-context.md"


def read_context_status_index(path: Path) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    if not path.is_file():
        return index

    for match in ARTIFACT_INDEX_ROW_RE.finditer(load_text(path)):
        index[match.group("artifact")] = {
            "status": match.group("status").strip().lower(),
            "freshness": match.group("freshness").strip().lower(),
        }
    return index


def is_stale_freshness(freshness: str | None) -> bool:
    if freshness is None:
        return False
    normalized = freshness.strip().lower()
    return "stale" in normalized


def validate_input_state(
    path: Path,
    role: str,
    *,
    context_status_index: dict[str, dict[str, str]] | None = None,
) -> None:
    if not path.is_file():
        raise ValueError(f"Missing required artifact for {role}: {relative(path)}")

    if path.name == "context-status.md":
        return

    status = read_status_value(path)
    if status in {"draft", "superseded", "blocked"}:
        raise ValueError(
            f"{relative(path)} is not a trusted input for {role}: status is '{status}'"
        )

    freshness = read_freshness_value(path)
    if is_stale_freshness(freshness):
        raise ValueError(
            f"{relative(path)} is not a trusted input for {role}: freshness is '{freshness}'"
        )

    if context_status_index is None:
        return

    indexed = context_status_index.get(relative(path))
    if indexed is None:
        return

    if indexed["status"] in {"draft", "superseded", "blocked"}:
        raise ValueError(
            f"{relative(path)} is not a trusted input for {role}: status index is '{indexed['status']}'"
        )
    if is_stale_freshness(indexed["freshness"]):
        raise ValueError(
            f"{relative(path)} is not a trusted input for {role}: freshness index is '{indexed['freshness']}'"
        )


def render_brief(feature_name: str, role: str, inputs: list[Path]) -> str:
    lines = [
        f"# Compiled {role.capitalize()} Context: {feature_name}",
        "",
        "Derived artifact. This brief is compiled from approved workflow artifacts and does not represent hidden memory.",
        "",
        "## Role",
        "",
        f"- Target role: `{role}`",
        f"- Feature: `{feature_name}`",
        "",
        "## Trusted Inputs",
        "",
    ]
    for path in inputs:
        if path.name == "context-status.md":
            continue
        status = read_status_value(path) or "unknown"
        lines.append(f"- `{relative(path)}` (`{status}`)")

    lines.extend(
        [
            "",
            "## Source Summary",
            "",
        ]
    )

    for path in inputs:
        title = path.stem.replace("-", " ")
        lines.append(f"### {title.title()}")
        lines.append("")
        lines.append(f"Source: `{relative(path)}`")
        lines.append("")
        lines.append("```markdown")
        lines.append(load_text(path).strip())
        lines.append("```")
        lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- Use this brief as a deterministic summary of trusted artifacts.",
            "- If any source artifact changes approval state or freshness, recompile before relying on this brief.",
            "",
        ]
    )
    return "\n".join(lines)


def compile_role_context(feature: str, role: str, output: Path | None = None) -> Path:
    feature = validate_feature_name(feature)
    ensure_repo_path(feature_context_dir(feature), "Feature directory")
    inputs = role_inputs(feature, role)
    context_status_index = read_context_status_index(feature_context_dir(feature) / "context-status.md")
    for path in inputs:
        validate_input_state(path, role, context_status_index=context_status_index)

    destination = ensure_repo_path(output if output is not None else role_output(feature, role), "Output path")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_brief(feature, role, inputs), encoding="utf-8")
    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature", help="Feature name under docs/context/<feature>")
    parser.add_argument("--role", required=True, choices=ROLE_CHOICES)
    parser.add_argument("--output", help="Optional output path; defaults to docs/context/<feature>/compiled-<role>-context.md")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        output = Path(args.output).resolve() if args.output else None
        path = compile_role_context(args.feature, args.role, output)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Compiled {args.role} context: {relative(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
