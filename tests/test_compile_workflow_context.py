from __future__ import annotations

import contextlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.test_support import load_script_module


compile_workflow_context = load_script_module(
    "compile_workflow_context_under_test",
    "scripts/compile_workflow_context.py",
)


class CompileWorkflowContextTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()
        feature_dir = self.root / "docs" / "context" / "example-feature"
        feature_dir.mkdir(parents=True)
        handoff_dir = self.root / "docs" / "handoffs" / "example-feature"
        handoff_dir.mkdir(parents=True)

        (feature_dir / "context-status.md").write_text(
            "# Context Status\n",
            encoding="utf-8",
        )
        (feature_dir / "planning-context.md").write_text(
            "# Planning Context\n\n## Status\n\n| Field | Value |\n|-------|-------|\n| Status | `approved` |\n",
            encoding="utf-8",
        )
        (feature_dir / "engineering-context.md").write_text(
            "# Engineering Context\n\n## Status\n\n| Field | Value |\n|-------|-------|\n| Status | `active` |\n",
            encoding="utf-8",
        )
        (feature_dir / "validation-context.md").write_text(
            "# Validation Context\n\n## Status\n\n| Field | Value |\n|-------|-------|\n| Status | `active` |\n",
            encoding="utf-8",
        )
        (handoff_dir / "planning-to-engineering.md").write_text(
            "# Handoff\n\n## Metadata\n\n| Field | Value |\n|-------|-------|\n| Status | `ready` |\n",
            encoding="utf-8",
        )
        (handoff_dir / "engineering-to-validation.md").write_text(
            "# Handoff\n\n## Metadata\n\n| Field | Value |\n|-------|-------|\n| Status | `ready` |\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        super().tearDown()

    @contextlib.contextmanager
    def patched_module(self):
        with patch.object(compile_workflow_context, "ROOT", self.root):
            yield

    def test_compile_role_context_emits_expected_inputs_for_engineering(self) -> None:
        with self.patched_module():
            output = compile_workflow_context.compile_role_context("example-feature", "engineering")

        text = output.read_text(encoding="utf-8")
        self.assertIn("# Compiled Engineering Context: example-feature", text)
        self.assertIn("docs/context/example-feature/planning-context.md", text)
        self.assertIn("docs/context/example-feature/engineering-context.md", text)
        self.assertIn("docs/handoffs/example-feature/planning-to-engineering.md", text)
        self.assertNotIn("engineering-to-validation.md", text)

    def test_compile_role_context_rejects_draft_inputs(self) -> None:
        validation_context = self.root / "docs" / "context" / "example-feature" / "validation-context.md"
        validation_context.write_text(
            "# Validation Context\n\n## Status\n\n| Field | Value |\n|-------|-------|\n| Status | `draft` |\n",
            encoding="utf-8",
        )

        with self.patched_module():
            with self.assertRaisesRegex(ValueError, "not a trusted input"):
                compile_workflow_context.compile_role_context("example-feature", "validation")

    def test_compile_role_context_supports_explicit_output_path(self) -> None:
        output_path = self.root / "docs" / "context" / "example-feature" / "custom-output.md"

        with self.patched_module():
            result = compile_workflow_context.compile_role_context(
                "example-feature",
                "planning",
                output=output_path,
            )

        self.assertEqual(result, output_path)
        self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
