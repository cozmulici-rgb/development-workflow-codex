#!/usr/bin/env python3
"""Generate write-boundary policies from plan phase documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PHASE_FILE_RE = re.compile(r"^phase-\d+\.md$")
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
WORKFLOW_ARTIFACT_DIRS = {"context", "handoffs", "research", "design", "plan"}


def split_sections(text: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1).strip()] = text[start:end].strip()
    return sections


def extract_paths_from_table(section_text: str) -> list[str]:
    paths: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        matches = INLINE_CODE_RE.findall(stripped)
        if matches:
            paths.append(matches[0].strip())
    return paths


def extract_phase_paths(phase_path: Path) -> list[str]:
    text = phase_path.read_text(encoding="utf-8")
    sections = split_sections(text)
    exact_changes = sections.get("Exact File Changes", "")
    if not exact_changes:
        raise ValueError(f"{phase_path.relative_to(ROOT)}: missing '## Exact File Changes' section")

    paths: list[str] = []
    subheading = None
    buffer: list[str] = []
    for line in exact_changes.splitlines():
        if line.startswith("### "):
            if subheading in {"Files to Create", "Files to Modify", "Files to Delete"}:
                paths.extend(extract_paths_from_table("\n".join(buffer)))
            subheading = line[4:].strip()
            buffer = []
            continue
        buffer.append(line)
    if subheading in {"Files to Create", "Files to Modify", "Files to Delete"}:
        paths.extend(extract_paths_from_table("\n".join(buffer)))

    tests_section = sections.get("Tests to Add / Modify", "")
    if tests_section:
        paths.extend(extract_paths_from_table(tests_section))

    normalized = []
    for path in paths:
        if path and path not in normalized:
            normalized.append(path)
    if not normalized:
        raise ValueError(f"{phase_path.relative_to(ROOT)}: no file paths found in Exact File Changes or Tests section")
    return normalized


def derive_feature_name(plan_dir: Path) -> str:
    return plan_dir.name


def derive_write_globs(paths: list[str]) -> list[str]:
    globs: list[str] = []
    for raw_path in paths:
        path = Path(raw_path)
        parts = path.parts
        if not parts:
            continue
        if len(parts) == 1:
            candidate = parts[0]
        elif parts[0] == "docs" and len(parts) > 1 and parts[1] in WORKFLOW_ARTIFACT_DIRS:
            candidate = f"docs/{parts[1]}/**"
        else:
            candidate = f"{parts[0]}/**"
        if candidate not in globs:
            globs.append(candidate)
    return globs


def generate_policy(phase_path: Path, mode: str, require_clean_git_start: bool) -> dict:
    relative_phase = phase_path.relative_to(ROOT)
    plan_dir = phase_path.parent
    allowed_touched_files = extract_phase_paths(phase_path)
    return {
        "version": 1,
        "role": "implement-coder",
        "phase": phase_path.stem,
        "feature": derive_feature_name(plan_dir),
        "mode": mode,
        "allowed_write_globs": derive_write_globs(allowed_touched_files),
        "blocked_write_globs": [],
        "allowed_touched_files": allowed_touched_files,
        "allow_new_files": True,
        "require_clean_git_start": require_clean_git_start,
        "_generated_from": relative_phase.as_posix(),
    }


def write_policy(policy_path: Path, policy: dict) -> None:
    serializable = {key: value for key, value in policy.items() if not key.startswith("_")}
    policy_path.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def iter_phase_files(plan_dir: Path) -> list[Path]:
    return sorted(path for path in plan_dir.iterdir() if path.is_file() and PHASE_FILE_RE.match(path.name))


def cmd_generate(args: argparse.Namespace) -> int:
    plan_dir = Path(args.plan_dir).resolve()
    if not plan_dir.is_dir():
        print(f"Missing plan directory: {args.plan_dir}", file=sys.stderr)
        return 1
    if ROOT not in plan_dir.parents:
        print(f"Plan directory resolves outside repo: {args.plan_dir}", file=sys.stderr)
        return 1

    phase_files = iter_phase_files(plan_dir)
    if not phase_files:
        print(f"No phase files found in {plan_dir.relative_to(ROOT)}", file=sys.stderr)
        return 1

    generated: list[Path] = []
    for phase_file in phase_files:
        policy = generate_policy(phase_file, args.mode, args.require_clean_git_start)
        policy_path = phase_file.with_name(f"boundary.{phase_file.stem}.json")
        write_policy(policy_path, policy)
        generated.append(policy_path.relative_to(ROOT))

    print(f"Generated {len(generated)} boundary policy file(s):")
    for path in generated:
        print(f"- {path.as_posix()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan_dir", help="Plan directory containing phase-XX.md files")
    parser.add_argument("--mode", choices=("enforce", "report"), default="enforce")
    parser.add_argument("--require-clean-git-start", action="store_true", default=False)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return cmd_generate(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
