from __future__ import annotations

import contextlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Iterator
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_script_module(name: str, relative_path: str) -> ModuleType:
    script_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module for {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class TempRepoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name).resolve()
        self.run_git("init")
        self.run_git("config", "user.name", "Codex Test")
        self.run_git("config", "user.email", "codex@example.com")
        self.run_git("config", "commit.gpgsign", "false")
        self.run_git("config", "core.hooksPath", "/dev/null")
        self.write_file("README.md", "fixture\n")
        self.run_git("add", "README.md")
        self.run_git("commit", "-m", "Initial fixture")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        super().tearDown()

    def write_file(self, relative_path: str, contents: str) -> Path:
        path = self.repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
        return path

    def remove_path(self, relative_path: str) -> None:
        path = self.repo_root / relative_path
        if path.exists():
            path.unlink()

    def run_git(self, *args: str) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(
                f"git {' '.join(args)} failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    @contextlib.contextmanager
    def patched_boundary_guard(self, module: ModuleType) -> Iterator[None]:
        state_dir = self.repo_root / ".codex-boundary"
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(module, "ROOT", self.repo_root))
            stack.enter_context(patch.object(module, "STATE_DIR", state_dir))
            stack.enter_context(patch.object(module, "STATE_FILE", state_dir / "session.json"))
            yield
