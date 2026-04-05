from __future__ import annotations

import json
import unittest
from argparse import Namespace
from unittest.mock import patch

from tests.test_support import TempRepoTestCase, load_script_module


generate_boundary_policy = load_script_module(
    "generate_boundary_policy_artifact_under_test",
    "scripts/generate_boundary_policy.py",
)
write_boundary_guard = load_script_module(
    "write_boundary_guard_artifact_under_test",
    "scripts/write_boundary_guard.py",
)


class BoundaryArtifactTests(TempRepoTestCase):
    def test_policy_generation_and_guard_support_artifact_paths(self) -> None:
        plan_dir = self.repo_root / "docs" / "plan" / "feature-x"
        plan_dir.mkdir(parents=True, exist_ok=True)
        phase_path = plan_dir / "phase-05.md"
        phase_path.write_text(
            """# Phase 05

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `docs/context/example-feature/compiled-engineering-context.md` | Compiled brief |
| `docs/handoffs/example-feature/engineering-to-validation.md` | Handoff |

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-01 | Unit | `tests/test_boundary_artifacts.py` |
""",
            encoding="utf-8",
        )

        with patch.object(generate_boundary_policy, "ROOT", self.repo_root):
            policy = generate_boundary_policy.generate_policy(phase_path, "enforce", False)

        self.assertEqual(
            policy["allowed_write_globs"],
            ["docs/context/**", "docs/handoffs/**", "tests/**"],
        )

        policy_path = plan_dir / "boundary.phase-05.json"
        policy_path.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")
        self.run_git("add", str(phase_path.relative_to(self.repo_root)), str(policy_path.relative_to(self.repo_root)))
        self.run_git("commit", "-m", "Add artifact boundary plan")
        self.write_file("docs/context/example-feature/compiled-engineering-context.md", "compiled\n")
        self.write_file("docs/handoffs/example-feature/engineering-to-validation.md", "handoff\n")

        with self.patched_boundary_guard(write_boundary_guard):
            start_code = write_boundary_guard.cmd_start(Namespace(policy=str(policy_path)))
            self.assertEqual(start_code, 0)
            loaded = write_boundary_guard.load_policy(policy_path)
            ok, violations = write_boundary_guard.verify_policy(loaded)

        self.assertTrue(ok)
        self.assertEqual(violations, [])
