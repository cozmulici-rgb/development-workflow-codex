from __future__ import annotations

import contextlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.test_support import REPO_ROOT, load_script_module


validate_repo = load_script_module("validate_repo_under_test", "scripts/validate_repo.py")


class ValidateRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()
        (self.root / ".codex-plugin").mkdir(parents=True)
        (self.root / ".agents" / "plugins").mkdir(parents=True)
        (self.root / "skills" / "example-skill").mkdir(parents=True)
        (self.root / "docs").mkdir()
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
        self._write_json(
            ".agents/plugins/marketplace.json",
            {
                "plugins": [
                    {
                        "name": "example-plugin",
                        "source": {"source": "local", "path": "."},
                    }
                ]
            },
        )
        self._write(
            "skills/example-skill/SKILL.md",
            "---\nname: example-skill\ndescription: Example skill\n---\n\nBody\n",
        )

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
            stack.enter_context(patch.object(validate_repo, "ROOT", self.root))
            stack.enter_context(
                patch.object(validate_repo, "PLUGIN_MANIFEST", self.root / ".codex-plugin" / "plugin.json")
            )
            stack.enter_context(
                patch.object(
                    validate_repo,
                    "MARKETPLACE_MANIFEST",
                    self.root / ".agents" / "plugins" / "marketplace.json",
                )
            )
            stack.enter_context(
                patch.object(
                    validate_repo,
                    "REQUIRED_ROOT_FILES",
                    (
                        self.root / "LICENSE",
                        self.root / "README.md",
                        self.root / "AGENTS.md",
                    ),
                )
            )
            yield

    def test_main_passes_for_valid_fixture(self) -> None:
        with self.patched_module():
            self.assertEqual(validate_repo.main(), 0)

    def test_main_reports_invalid_boundary_policy(self) -> None:
        self._write_json(
            "docs/boundary.invalid.json",
            {
                "version": 2,
                "role": "implement-coder",
                "feature": "example",
                "mode": "enforce",
                "allowed_write_globs": ["src/**"],
                "blocked_write_globs": ["docs/**"],
                "allowed_touched_files": ["src/example.py"],
            },
        )

        with self.patched_module():
            self.assertEqual(validate_repo.main(), 1)

    def test_main_rejects_skill_path_outside_repo(self) -> None:
        self._write_json(
            ".codex-plugin/plugin.json",
            {
                "name": "example-plugin",
                "version": "0.1.0",
                "skills": "../elsewhere",
            },
        )

        with self.patched_module():
            self.assertEqual(validate_repo.main(), 1)

    def test_parse_frontmatter_reports_malformed_line(self) -> None:
        skill_file = self.root / "skills" / "example-skill" / "SKILL.md"
        skill_file.write_text("---\nname example-skill\n---\n", encoding="utf-8")
        errors: list[str] = []

        with self.patched_module():
            frontmatter = validate_repo.parse_frontmatter(skill_file, errors)

        self.assertEqual(frontmatter, {})
        self.assertEqual(len(errors), 1)
        self.assertIn("Malformed frontmatter line", errors[0])

    def test_packaged_skill_tree_includes_orchestrator_entrypoint(self) -> None:
        manifest = json.loads((REPO_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        skills_dir = (REPO_ROOT / manifest["skills"]).resolve()
        orchestrator_skill = skills_dir / "development-pipeline-orchestrator" / "SKILL.md"

        self.assertTrue(orchestrator_skill.is_file())

        frontmatter_errors: list[str] = []
        frontmatter = validate_repo.parse_frontmatter(orchestrator_skill, frontmatter_errors)

        self.assertEqual(frontmatter_errors, [])
        self.assertEqual(frontmatter.get("name"), "development-pipeline-orchestrator")

    def test_team_config_exposes_orchestrator_planning_engineering_validation_roles(self) -> None:
        teams_yaml = (
            REPO_ROOT / "skills" / "development-pipeline" / "references" / "teams.yaml"
        ).read_text(encoding="utf-8")

        self.assertIn("orchestrator:\n", teams_yaml)
        self.assertIn("entrypoint: development-pipeline-orchestrator", teams_yaml)
        self.assertIn("teams:\n  planning:\n", teams_yaml)
        self.assertIn("\n  engineering:\n", teams_yaml)
        self.assertIn("\n  validation:\n", teams_yaml)
        self.assertIn("lead: research-lead", teams_yaml)
        self.assertIn("lead: implement-lead", teams_yaml)
        self.assertIn("lead: validation-lead", teams_yaml)

    def test_validation_team_binds_validation_lead_reviewers_and_tester(self) -> None:
        teams_yaml = (
            REPO_ROOT / "skills" / "development-pipeline" / "references" / "teams.yaml"
        ).read_text(encoding="utf-8")

        self.assertIn("\n  validation:\n", teams_yaml)
        self.assertIn("lead: validation-lead", teams_yaml)
        self.assertIn("- name: validation-lead", teams_yaml)
        self.assertIn("- name: reviewer-quality", teams_yaml)
        self.assertIn("- name: reviewer-architecture", teams_yaml)
        self.assertIn("- name: reviewer-security", teams_yaml)
        self.assertIn("- name: reviewer-plan-compliance", teams_yaml)
        self.assertIn("- name: tester", teams_yaml)

    def test_validation_lead_references_are_included_in_packaged_workflow_docs(self) -> None:
        workflow_readme = (
            REPO_ROOT / "skills" / "development-pipeline" / "references" / "README.md"
        ).read_text(encoding="utf-8")
        validation_skill = (
            REPO_ROOT / "skills" / "development-pipeline-validation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        validation_lead = (
            REPO_ROOT / "skills" / "development-pipeline" / "references" / "validation-lead.md"
        ).read_text(encoding="utf-8")

        self.assertIn("validation-lead", workflow_readme)
        self.assertIn("development-pipeline-validation", workflow_readme)
        self.assertIn("name: development-pipeline-validation", validation_skill)
        self.assertIn("name: validation-lead", validation_lead)
        self.assertNotIn("expertise:", validation_lead)

    def test_shared_codex_native_workflow_assets_exist_and_validate(self) -> None:
        shared_skills = {
            "development-pipeline-shared-orchestrator": "skills/development-pipeline-shared-orchestrator/SKILL.md",
            "development-pipeline-shared-worker": "skills/development-pipeline-shared-worker/SKILL.md",
            "development-pipeline-shared-reviewer": "skills/development-pipeline-shared-reviewer/SKILL.md",
        }

        for expected_name, relative_path in shared_skills.items():
            skill_file = REPO_ROOT / relative_path
            self.assertTrue(skill_file.is_file(), relative_path)

            frontmatter_errors: list[str] = []
            frontmatter = validate_repo.parse_frontmatter(skill_file, frontmatter_errors)

            self.assertEqual(frontmatter_errors, [])
            self.assertEqual(frontmatter.get("name"), expected_name)

    def test_repo_validation_inputs_reference_packaged_shared_skill_names(self) -> None:
        teams_yaml = (
            REPO_ROOT / "skills" / "development-pipeline" / "references" / "teams.yaml"
        ).read_text(encoding="utf-8")

        self.assertIn("development-pipeline-shared-orchestrator", teams_yaml)
        self.assertIn("development-pipeline-shared-worker", teams_yaml)
        self.assertIn("development-pipeline-shared-reviewer", teams_yaml)
        self.assertNotIn("skills: [actionable-reviewer]", teams_yaml)
        self.assertNotIn("skills: [verbose-worker]", teams_yaml)

    def test_memory_and_session_docs_replace_stale_expertise_runtime_claims(self) -> None:
        memory_doc = (REPO_ROOT / "docs" / "codex-agent-memory-and-sessions.md").read_text(encoding="utf-8")
        workflow_readme = (
            REPO_ROOT / "skills" / "development-pipeline" / "references" / "README.md"
        ).read_text(encoding="utf-8")

        self.assertIn("persistent per-agent memory is out of scope", memory_doc.lower())
        self.assertIn("docs/codex-agent-memory-and-sessions.md", workflow_readme)

        checked_files = [
            "skills/development-pipeline/references/research-lead.md",
            "skills/development-pipeline/references/design.md",
            "skills/development-pipeline/references/plan.md",
            "skills/development-pipeline/references/implement-lead.md",
            "skills/development-pipeline/references/implement-coder.md",
            "skills/development-pipeline/references/research-subagent-architecture.md",
            "skills/development-pipeline/references/research-subagent-patterns.md",
            "skills/development-pipeline/references/research-subagent-integrations.md",
            "skills/development-pipeline/references/research-subagent-domain.md",
            "skills/development-pipeline/references/research-subagent-api.md",
            "skills/development-pipeline/references/research-subagent-tests.md",
            "skills/development-pipeline/references/research-subagent-fintech-domain.md",
            "skills/development-pipeline/references/reviewer-quality.md",
            "skills/development-pipeline/references/reviewer-architecture.md",
            "skills/development-pipeline/references/reviewer-security.md",
            "skills/development-pipeline/references/reviewer-plan-compliance.md",
            "skills/development-pipeline/references/reviewer-fintech-compliance.md",
            "skills/development-pipeline/references/reviewer-fintech-patterns.md",
            "skills/development-pipeline/references/tester.md",
        ]

        for relative_path in checked_files:
            contents = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotIn("Read your expertise file", contents, relative_path)
            self.assertNotIn("expertise:", contents, relative_path)
            self.assertIn("docs/codex-agent-memory-and-sessions.md", contents, relative_path)

    def test_final_packaged_docs_and_guides_share_same_runtime_contract(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        workflow_readme = (
            REPO_ROOT / "skills" / "development-pipeline" / "references" / "README.md"
        ).read_text(encoding="utf-8")

        self.assertIn("docs/codex-agent-memory-and-sessions.md", readme)
        self.assertIn("docs/codex-agent-memory-and-sessions.md", agents)
        self.assertIn("docs/codex-agent-memory-and-sessions.md", workflow_readme)
        self.assertIn("Persistent per-agent memory is out of scope", readme)
        self.assertIn("Persistent per-agent memory is out of scope", workflow_readme)


if __name__ == "__main__":
    unittest.main()
