from __future__ import annotations

import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from tests.test_support import load_script_module


record_workflow_session = load_script_module(
    "record_workflow_session_under_test",
    "scripts/record_workflow_session.py",
)


class RecordWorkflowSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.repo_root = Path(tempfile.mkdtemp()).resolve() / "repo"
        self.repo_root.mkdir(parents=True)
        self.outside_dir = Path(tempfile.mkdtemp()).resolve() / "logs"

    def test_record_session_writes_non_contractual_log_outside_repo(self) -> None:
        with patch.object(record_workflow_session, "ROOT", self.repo_root):
            path = record_workflow_session.record_session(
                Namespace(
                    label="phase-06",
                    feature="artifact-memory-and-handoffs",
                    output_dir=str(self.outside_dir),
                    allow_inside_repo=False,
                    note=["maintainer debug"],
                    prompt=["Implement phase 06"],
                    tool_action=["Ran validation"],
                    output=["Validation passed"],
                )
            )

        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(payload["contractual"])
        self.assertEqual(payload["feature"], "artifact-memory-and-handoffs")
        self.assertEqual(payload["prompts"], ["Implement phase 06"])
        self.assertEqual(payload["tool_actions"], ["Ran validation"])
        self.assertEqual(payload["outputs"], ["Validation passed"])
        self.assertTrue(path.is_file())
        self.assertNotIn(self.repo_root, path.parents)

    def test_record_session_rejects_repo_local_output_without_override(self) -> None:
        inside_repo = self.repo_root / "docs" / "logs"

        with patch.object(record_workflow_session, "ROOT", self.repo_root):
            with self.assertRaisesRegex(ValueError, "outside the repository"):
                record_workflow_session.record_session(
                    Namespace(
                        label="phase-06",
                        feature=None,
                        output_dir=str(inside_repo),
                        allow_inside_repo=False,
                        note=[],
                        prompt=[],
                        tool_action=[],
                        output=[],
                    )
                )

    def test_record_session_allows_repo_local_output_when_explicitly_requested(self) -> None:
        inside_repo = self.repo_root / "tmp" / "logs"

        with patch.object(record_workflow_session, "ROOT", self.repo_root):
            path = record_workflow_session.record_session(
                Namespace(
                    label="phase-06",
                    feature=None,
                    output_dir=str(inside_repo),
                    allow_inside_repo=True,
                    note=[],
                    prompt=[],
                    tool_action=[],
                    output=[],
                )
            )

        self.assertTrue(path.is_file())
        self.assertIn(inside_repo.resolve(), path.parents)


if __name__ == "__main__":
    unittest.main()
