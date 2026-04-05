from __future__ import annotations

import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from tests.test_support import TempRepoTestCase, load_script_module


write_boundary_guard = load_script_module(
    "write_boundary_guard_under_test",
    "scripts/write_boundary_guard.py",
)


class WriteBoundaryGuardTests(TempRepoTestCase):
    def write_policy(self, payload: dict) -> Path:
        path = self.repo_root / "docs" / "plan" / "feature-x" / "boundary.phase-01.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def base_policy(self, **overrides: object) -> dict:
        payload = {
            "version": 1,
            "role": "implement-coder",
            "feature": "feature-x",
            "mode": "enforce",
            "allowed_write_globs": ["src/**", "tests/**", "config/**"],
            "blocked_write_globs": ["docs/**"],
            "allowed_touched_files": ["src/example.py", "tests/test_example.py"],
            "allow_new_files": True,
            "require_clean_git_start": False,
        }
        payload.update(overrides)
        return payload

    def test_collect_changes_tracks_untracked_modified_deleted_and_renamed_paths(self) -> None:
        self.write_file("src/example.py", "v1\n")
        self.write_file("src/rename_me.py", "old\n")
        self.run_git("add", "src/example.py", "src/rename_me.py")
        self.run_git("commit", "-m", "Add tracked files")
        self.write_file("src/example.py", "v2\n")
        self.write_file("tests/test_example.py", "new\n")
        self.run_git("mv", "src/rename_me.py", "src/renamed.py")
        self.remove_path("README.md")

        with self.patched_boundary_guard(write_boundary_guard):
            changes = write_boundary_guard.collect_changes()

        statuses = {(change.path, change.staged): change.status for change in changes}
        self.assertIn(("src/example.py", False), statuses)
        self.assertIn(("tests/test_example.py", False), statuses)
        self.assertIn(("src/rename_me.py", True), statuses)
        self.assertIn(("src/renamed.py", True), statuses)
        self.assertIn(("README.md", False), statuses)
        self.assertNotIn(("tests/test_example.py", True), statuses)

    def test_verify_policy_blocks_new_files_when_disabled(self) -> None:
        policy_path = self.write_policy(self.base_policy(allow_new_files=False))
        self.write_file("src/example.py", "print('ok')\n")

        with self.patched_boundary_guard(write_boundary_guard):
            policy = write_boundary_guard.load_policy(policy_path)
            ok, violations = write_boundary_guard.verify_policy(policy)

        self.assertFalse(ok)
        self.assertIn("src/example.py: new files are not allowed by policy", violations)

    def test_verify_policy_ignores_baseline_dirty_paths_for_same_policy(self) -> None:
        policy_path = self.write_policy(self.base_policy())
        self.run_git("add", str(policy_path.relative_to(self.repo_root)))
        self.run_git("commit", "-m", "Add policy")
        self.write_file("src/example.py", "baseline\n")

        with self.patched_boundary_guard(write_boundary_guard):
            start_code = write_boundary_guard.cmd_start(Namespace(policy=str(policy_path)))
            self.assertEqual(start_code, 0)
            policy = write_boundary_guard.load_policy(policy_path)
            ok, violations = write_boundary_guard.verify_policy(policy)

        self.assertTrue(ok)
        self.assertEqual(violations, [])

    def test_verify_policy_flags_further_edits_to_baseline_dirty_paths(self) -> None:
        policy_path = self.write_policy(self.base_policy())
        self.run_git("add", str(policy_path.relative_to(self.repo_root)))
        self.run_git("commit", "-m", "Add policy")
        self.write_file("docs/notes.md", "baseline\n")

        with self.patched_boundary_guard(write_boundary_guard):
            start_code = write_boundary_guard.cmd_start(Namespace(policy=str(policy_path)))
            self.assertEqual(start_code, 0)

        self.write_file("docs/notes.md", "baseline\nmore\n")

        with self.patched_boundary_guard(write_boundary_guard):
            policy = write_boundary_guard.load_policy(policy_path)
            ok, violations = write_boundary_guard.verify_policy(policy)

        self.assertFalse(ok)
        self.assertIn("docs/notes.md: matches blocked_write_globs", violations)

    def test_start_requires_clean_git_state_when_policy_demands_it(self) -> None:
        policy_path = self.write_policy(self.base_policy(require_clean_git_start=True))
        self.write_file("src/example.py", "dirty\n")

        with self.patched_boundary_guard(write_boundary_guard):
            exit_code = write_boundary_guard.cmd_start(Namespace(policy=str(policy_path)))

        self.assertEqual(exit_code, 1)

    def test_verify_policy_requires_start_for_clean_git_sessions(self) -> None:
        policy_path = self.write_policy(self.base_policy(require_clean_git_start=True))
        self.write_file("src/example.py", "dirty\n")

        with self.patched_boundary_guard(write_boundary_guard):
            policy = write_boundary_guard.load_policy(policy_path)
            ok, violations = write_boundary_guard.verify_policy(policy)

        self.assertFalse(ok)
        self.assertIn("policy requires a clean git start for this policy; run 'start' before making changes", violations)

    def test_verify_policy_rejects_stale_session_for_different_policy(self) -> None:
        first_policy_path = self.write_policy(
            self.base_policy(feature="feature-a", require_clean_git_start=True)
        )
        second_policy_path = self.repo_root / "docs" / "plan" / "feature-y" / "boundary.phase-02.json"
        second_policy_path.parent.mkdir(parents=True, exist_ok=True)
        second_policy_path.write_text(
            json.dumps(self.base_policy(feature="feature-y", require_clean_git_start=True), indent=2) + "\n",
            encoding="utf-8",
        )
        self.run_git("add", str(first_policy_path.relative_to(self.repo_root)), str(second_policy_path.relative_to(self.repo_root)))
        self.run_git("commit", "-m", "Add policies")

        with self.patched_boundary_guard(write_boundary_guard):
            start_code = write_boundary_guard.cmd_start(Namespace(policy=str(first_policy_path)))
            self.assertEqual(start_code, 0)

        self.write_file("src/example.py", "dirty\n")

        with self.patched_boundary_guard(write_boundary_guard):
            policy = write_boundary_guard.load_policy(second_policy_path)
            ok, violations = write_boundary_guard.verify_policy(policy)

        self.assertFalse(ok)
        self.assertIn("policy requires a clean git start for this policy; run 'start' before making changes", violations)

    def test_verify_policy_labels_artifact_boundary_violations(self) -> None:
        policy_path = self.write_policy(
            self.base_policy(
                allowed_write_globs=["docs/context/**"],
                blocked_write_globs=[],
                allowed_touched_files=["docs/context/example-feature/planning-context.md"],
            )
        )
        self.run_git("add", str(policy_path.relative_to(self.repo_root)))
        self.run_git("commit", "-m", "Add policy")
        self.write_file("docs/context/example-feature/unlisted.md", "artifact\n")

        with self.patched_boundary_guard(write_boundary_guard):
            policy = write_boundary_guard.load_policy(policy_path)
            ok, violations = write_boundary_guard.verify_policy(policy)

        self.assertFalse(ok)
        self.assertIn(
            "docs/context/example-feature/unlisted.md: not listed in allowed_touched_files (artifact path)",
            violations,
        )


if __name__ == "__main__":
    unittest.main()
