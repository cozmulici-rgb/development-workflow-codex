from __future__ import annotations

import contextlib
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from tests.test_support import load_script_module


generate_boundary_policy = load_script_module(
    "generate_boundary_policy_under_test",
    "scripts/generate_boundary_policy.py",
)


class GenerateBoundaryPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()
        self.plan_dir = self.root / "docs" / "plan" / "feature-x"
        self.plan_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        super().tearDown()

    def _write_phase(self, filename: str, contents: str) -> Path:
        path = self.plan_dir / filename
        path.write_text(contents, encoding="utf-8")
        return path

    @contextlib.contextmanager
    def patched_module(self):
        with patch.object(generate_boundary_policy, "ROOT", self.root):
            yield

    def test_extract_phase_paths_deduplicates_paths_across_sections(self) -> None:
        phase = self._write_phase(
            "phase-01.md",
            """# Phase 01

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `src/example.py` | Add implementation |
| `tests/test_example.py` | Add tests |

### Files to Modify
| File Path | Purpose |
|-----------|---------|
| `src/example.py` | Refine implementation |

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-01 | Unit | `tests/test_example.py` |
""",
        )

        with self.patched_module():
            paths = generate_boundary_policy.extract_phase_paths(phase)

        self.assertEqual(paths, ["src/example.py", "tests/test_example.py"])

    def test_extract_phase_paths_requires_exact_file_changes_section(self) -> None:
        phase = self._write_phase("phase-01.md", "# Phase 01\n\n## Objective\n\nMissing table.\n")

        with self.patched_module():
            with self.assertRaisesRegex(ValueError, "missing '## Exact File Changes' section"):
                generate_boundary_policy.extract_phase_paths(phase)

    def test_derive_write_globs_maps_paths_to_repo_scopes(self) -> None:
        with self.patched_module():
            globs = generate_boundary_policy.derive_write_globs(
                [
                    "skills/development-pipeline/SKILL.md",
                    ".codex-plugin/plugin.json",
                    ".agents/plugins/marketplace.json",
                    "README.md",
                    "tests/test_validate_repo.py",
                ]
            )

        self.assertEqual(
            globs,
            [
                "skills/**",
                ".codex-plugin/**",
                ".agents/**",
                "README.md",
                "tests/**",
            ],
        )

    def test_cmd_generate_writes_boundary_files_for_each_phase(self) -> None:
        self._write_phase(
            "phase-01.md",
            """# Phase 01

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `src/a.py` | Add |

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-01 | Unit | `tests/test_a.py` |
""",
        )
        self._write_phase(
            "phase-02.md",
            """# Phase 02

## Exact File Changes

### Files to Modify
| File Path | Purpose |
|-----------|---------|
| `config/a.json` | Update |
""",
        )

        with self.patched_module():
            exit_code = generate_boundary_policy.cmd_generate(
                Namespace(
                    plan_dir=str(self.plan_dir),
                    mode="report",
                    require_clean_git_start=True,
                )
            )

        self.assertEqual(exit_code, 0)
        payload = json.loads((self.plan_dir / "boundary.phase-01.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["feature"], "feature-x")
        self.assertEqual(payload["mode"], "report")
        self.assertTrue(payload["require_clean_git_start"])
        self.assertEqual(payload["allowed_touched_files"], ["src/a.py", "tests/test_a.py"])
        self.assertEqual(payload["allowed_write_globs"], ["src/**", "tests/**"])
        self.assertEqual(payload["blocked_write_globs"], [])

    def test_cmd_generate_rejects_plan_dir_outside_repo(self) -> None:
        outside_dir = Path(tempfile.mkdtemp())
        try:
            with self.patched_module():
                exit_code = generate_boundary_policy.cmd_generate(
                    Namespace(
                        plan_dir=str(outside_dir),
                        mode="enforce",
                        require_clean_git_start=False,
                    )
                )
            self.assertEqual(exit_code, 1)
        finally:
            for child in outside_dir.iterdir():
                child.unlink()
            outside_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
