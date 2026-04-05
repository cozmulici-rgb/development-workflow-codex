from __future__ import annotations

import contextlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from tests.test_support import load_script_module


package_plugin = load_script_module("package_plugin_under_test", "scripts/package_plugin.py")


class PackagePluginTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()
        (self.root / ".codex-plugin").mkdir(parents=True)
        (self.root / ".agents" / "plugins").mkdir(parents=True)
        (self.root / "docs").mkdir()
        (self.root / "skills").mkdir()
        (self.root / "scripts").mkdir()
        self._write("LICENSE", "license\n")
        self._write("README.md", "readme\n")
        self._write("AGENTS.md", "agents\n")
        self._write_json(
            ".codex-plugin/plugin.json",
            {
                "name": "example-plugin",
                "version": "0.1.0",
                "skills": "skills",
            },
        )
        self._write("scripts/validate_repo.py", "print('stub validator')\n")
        self._write("scripts/compile_workflow_context.py", "print('compile')\n")
        self._write("scripts/record_workflow_session.py", "print('record')\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        super().tearDown()

    def _write(self, relative_path: str, contents: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")

    def _write_json(self, relative_path: str, payload: dict) -> None:
        self._write(relative_path, json.dumps(payload, indent=2) + "\n")

    @contextlib.contextmanager
    def patched_module(self):
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(package_plugin, "ROOT", self.root))
            stack.enter_context(patch.object(package_plugin, "DIST_DIR", self.root / "dist"))
            stack.enter_context(
                patch.object(package_plugin, "PLUGIN_MANIFEST", self.root / ".codex-plugin" / "plugin.json")
            )
            yield

    def test_main_returns_validator_exit_code_when_validation_fails(self) -> None:
        class Result:
            returncode = 3

        with self.patched_module():
            with patch.object(package_plugin.subprocess, "run", return_value=Result()) as run_mock:
                exit_code = package_plugin.main()

        self.assertEqual(exit_code, 3)
        run_mock.assert_called_once()

    def test_main_builds_archive_after_successful_validation(self) -> None:
        class Result:
            returncode = 0

        with self.patched_module():
            with patch.object(package_plugin.subprocess, "run", return_value=Result()):
                exit_code = package_plugin.main()

        archive_path = self.root / "dist" / "example-plugin-0.1.0.zip"
        self.assertEqual(exit_code, 0)
        self.assertTrue(archive_path.is_file())
        with zipfile.ZipFile(archive_path) as archive:
            names = set(archive.namelist())
        self.assertIn("example-plugin-0.1.0/scripts/compile_workflow_context.py", names)
        self.assertIn("example-plugin-0.1.0/scripts/record_workflow_session.py", names)
        self.assertIn("example-plugin-0.1.0/scripts/validate_repo.py", names)


if __name__ == "__main__":
    unittest.main()
