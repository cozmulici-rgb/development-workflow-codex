#!/usr/bin/env python3
"""Verify repo changes against a write-boundary policy."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / ".codex-boundary"
STATE_FILE = STATE_DIR / "session.json"


@dataclass
class Change:
    path: str
    staged: bool
    status: str


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def relative_to_root(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def load_policy(policy_path: Path) -> dict[str, Any]:
    resolved = policy_path.resolve()
    if not resolved.is_file():
        raise ValueError(f"Missing policy file: {policy_path}")
    if ROOT not in resolved.parents:
        raise ValueError(f"Policy path resolves outside repo: {policy_path}")
    try:
        policy = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {policy_path}: {exc}") from exc
    validate_policy(policy, relative_to_root(resolved))
    policy["_path"] = relative_to_root(resolved)
    return policy


def validate_policy(policy: dict[str, Any], label: str) -> None:
    required_strings = ("role", "feature", "mode")
    if policy.get("version") != 1:
        raise ValueError(f"{label}: version must be 1")
    for key in required_strings:
        if not isinstance(policy.get(key), str) or not policy[key].strip():
            raise ValueError(f"{label}: {key} must be a non-empty string")
    if policy["mode"] not in {"enforce", "report"}:
        raise ValueError(f"{label}: mode must be 'enforce' or 'report'")
    for key in ("allowed_write_globs", "blocked_write_globs", "allowed_touched_files"):
        value = policy.get(key, [])
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            raise ValueError(f"{label}: {key} must be a list of non-empty strings")
    for key in ("allow_new_files", "require_clean_git_start"):
        if key in policy and not isinstance(policy[key], bool):
            raise ValueError(f"{label}: {key} must be a boolean")


def collect_changes() -> list[Change]:
    changes: dict[tuple[str, bool], Change] = {}
    for staged, args in (
        (False, ["status", "--porcelain", "--untracked-files=all"]),
        (True, ["diff", "--cached", "--name-status"]),
    ):
        result = run_git(*args)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
        if staged:
            for raw_line in result.stdout.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                parts = line.split("\t")
                status = parts[0]
                path = parts[-1]
                changes[(path, True)] = Change(path=path, staged=True, status=status)
        else:
            for raw_line in result.stdout.splitlines():
                if not raw_line:
                    continue
                status = raw_line[:2]
                path = raw_line[3:]
                if " -> " in path:
                    path = path.split(" -> ", 1)[1]
                if status[0] != " ":
                    changes[(path, True)] = Change(path=path, staged=True, status=status[0])
                if status[1] != " ":
                    changes[(path, False)] = Change(path=path, staged=False, status=status[1])
    return sorted(changes.values(), key=lambda item: (item.path, item.staged))


def matches_any(path: str, patterns: list[str]) -> bool:
    candidate = Path(path)
    return any(candidate.match(pattern) for pattern in patterns)


def changed_paths(changes: list[Change]) -> list[str]:
    return sorted({change.path for change in changes})


def current_branch() -> str:
    result = run_git("rev-parse", "--abbrev-ref", "HEAD")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git rev-parse failed")
    return result.stdout.strip()


def working_tree_is_clean() -> bool:
    result = run_git("status", "--porcelain")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git status failed")
    return not result.stdout.strip()


def baseline_dirty_paths() -> list[str]:
    return changed_paths(collect_changes())


def load_state() -> dict[str, Any]:
    if not STATE_FILE.is_file():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_policy(policy: dict[str, Any]) -> tuple[bool, list[str]]:
    violations: list[str] = []
    changes = collect_changes()
    changed = changed_paths(changes)
    allowed_globs = policy.get("allowed_write_globs", [])
    blocked_globs = policy.get("blocked_write_globs", [])
    allowed_files = set(policy.get("allowed_touched_files", []))
    allow_new = policy.get("allow_new_files", True)

    state = load_state()
    baseline_paths = set(state.get("baseline_dirty_paths", [])) if state.get("policy_path") == policy["_path"] else set()
    effective_changed = [path for path in changed if path not in baseline_paths]

    if policy.get("require_clean_git_start") and not state and changed:
        violations.append("policy requires a clean git start; run 'start' before making changes")

    for path in effective_changed:
        if blocked_globs and matches_any(path, blocked_globs):
            violations.append(f"{path}: matches blocked_write_globs")
            continue
        if allowed_globs and not matches_any(path, allowed_globs):
            violations.append(f"{path}: outside allowed_write_globs")
            continue
        if allowed_files and path not in allowed_files:
            violations.append(f"{path}: not listed in allowed_touched_files")

    if not allow_new:
        for change in changes:
            if change.path not in effective_changed:
                continue
            if change.status == "A" or change.status == "??":
                violations.append(f"{change.path}: new files are not allowed by policy")

    return (not violations, violations)


def cmd_start(args: argparse.Namespace) -> int:
    policy = load_policy(Path(args.policy))
    dirty_paths = baseline_dirty_paths()
    if policy.get("require_clean_git_start") and dirty_paths:
        print("Cannot start guarded session: worktree is not clean")
        for path in dirty_paths:
            print(f"- {path}")
        return 1
    save_state(
        {
            "branch": current_branch(),
            "policy_path": policy["_path"],
            "baseline_dirty_paths": dirty_paths,
        }
    )
    print(f"Started boundary session for {policy['_path']}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    policy = load_policy(Path(args.policy))
    ok, violations = verify_policy(policy)
    if ok:
        changed = changed_paths(collect_changes())
        print(f"Boundary check passed for {policy['_path']}")
        if changed:
            print("Changed files:")
            for path in changed:
                print(f"- {path}")
        return 0

    print("Write boundary violation")
    print()
    print(f"Policy: {policy['_path']}")
    print(f"Role: {policy['role']}")
    print()
    for violation in violations:
        print(f"- {violation}")
    return 1


def cmd_report(args: argparse.Namespace) -> int:
    policy = load_policy(Path(args.policy))
    ok, violations = verify_policy(policy)
    changed = changed_paths(collect_changes())
    print(f"Policy: {policy['_path']}")
    print(f"Role: {policy['role']}")
    print(f"Mode: {policy['mode']}")
    print(f"Branch: {current_branch()}")
    print(f"Status: {'PASS' if ok else 'FAIL'}")
    print("Changed files:")
    if changed:
        for path in changed:
            print(f"- {path}")
    else:
        print("- none")
    if violations:
        print("Violations:")
        for violation in violations:
            print(f"- {violation}")
    return 0 if ok else 1


def cmd_stage(args: argparse.Namespace) -> int:
    policy = load_policy(Path(args.policy))
    ok, violations = verify_policy(policy)
    if not ok:
        print("Refusing to stage because policy verification failed")
        for violation in violations:
            print(f"- {violation}")
        return 1

    requested = args.files
    if not requested:
        print("No files provided to stage")
        return 1

    allowed_files = set(policy.get("allowed_touched_files", []))
    allowed_globs = policy.get("allowed_write_globs", [])
    blocked_globs = policy.get("blocked_write_globs", [])
    invalid: list[str] = []
    for path in requested:
        if blocked_globs and matches_any(path, blocked_globs):
            invalid.append(f"{path}: matches blocked_write_globs")
            continue
        if allowed_globs and not matches_any(path, allowed_globs):
            invalid.append(f"{path}: outside allowed_write_globs")
            continue
        if allowed_files and path not in allowed_files:
            invalid.append(f"{path}: not listed in allowed_touched_files")

    if invalid:
        print("Refusing to stage invalid paths")
        for violation in invalid:
            print(f"- {violation}")
        return 1

    result = run_git("add", "--", *requested)
    if result.returncode != 0:
        print(result.stderr.strip() or "git add failed")
        return result.returncode
    print("Staged files:")
    for path in requested:
        print(f"- {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, handler in (
        ("start", cmd_start),
        ("verify", cmd_verify),
        ("report", cmd_report),
    ):
        sub = subparsers.add_parser(name)
        sub.add_argument("--policy", required=True)
        sub.set_defaults(func=handler)

    stage = subparsers.add_parser("stage")
    stage.add_argument("--policy", required=True)
    stage.add_argument("files", nargs="*")
    stage.set_defaults(func=cmd_stage)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
