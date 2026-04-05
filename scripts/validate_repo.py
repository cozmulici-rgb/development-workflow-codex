#!/usr/bin/env python3
"""Validate the local Codex plugin repository structure."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_MANIFEST = ROOT / ".agents" / "plugins" / "marketplace.json"
BOUNDARY_POLICY_GLOB = "docs/**/boundary*.json"
REQUIRED_ROOT_FILES = (
    ROOT / "LICENSE",
    ROOT / "README.md",
    ROOT / "AGENTS.md",
)
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"
SKILL_FRONTMATTER_RE = re.compile(
    r"\A---\n(?P<frontmatter>.*?)\n---\n",
    re.DOTALL,
)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        fail(f"Missing JSON file: {path.relative_to(ROOT)}", errors)
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}", errors)
        return {}


def parse_frontmatter(skill_file: Path, errors: list[str]) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    match = SKILL_FRONTMATTER_RE.match(text)
    if not match:
        fail(f"Missing YAML-style frontmatter in {skill_file.relative_to(ROOT)}", errors)
        return {}

    values: dict[str, str] = {}
    for line in match.group("frontmatter").splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"Malformed frontmatter line in {skill_file.relative_to(ROOT)}: {line}", errors)
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def validate_skill_tree(skills_dir: Path, errors: list[str]) -> None:
    if not skills_dir.is_dir():
        fail(f"Skills directory does not exist: {skills_dir.relative_to(ROOT)}", errors)
        return

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        fail(f"No skill definitions found under {skills_dir.relative_to(ROOT)}", errors)
        return

    for skill_file in skill_files:
        skill_dir = skill_file.parent
        frontmatter = parse_frontmatter(skill_file, errors)
        if not frontmatter:
            continue

        name = frontmatter.get("name")
        description = frontmatter.get("description")

        if not name:
            fail(f"Missing frontmatter name in {skill_file.relative_to(ROOT)}", errors)
        elif name != skill_dir.name:
            fail(
                f"Frontmatter name '{name}' does not match directory '{skill_dir.name}' in "
                f"{skill_file.relative_to(ROOT)}",
                errors,
            )

        if not description:
            fail(f"Missing frontmatter description in {skill_file.relative_to(ROOT)}", errors)


def validate_marketplace(
    plugin_manifest: dict,
    marketplace_manifest: dict,
    errors: list[str],
) -> None:
    plugin_name = plugin_manifest.get("name")
    plugins = marketplace_manifest.get("plugins")

    if not isinstance(plugins, list) or not plugins:
        fail("Marketplace manifest must contain a non-empty 'plugins' list", errors)
        return

    matched_plugin = None
    for item in plugins:
        if item.get("name") == plugin_name:
            matched_plugin = item
            break

    if matched_plugin is None:
        fail(
            f"Marketplace manifest does not expose plugin '{plugin_name}'",
            errors,
        )
        return

    source = matched_plugin.get("source", {})
    if source.get("source") != "local" or source.get("path") != ".":
        fail(
            "Marketplace plugin entry must use local source path '.' for this repo",
            errors,
        )


def validate_github_distribution(plugin_manifest: dict, errors: list[str]) -> None:
    homepage = plugin_manifest.get("homepage")
    if not isinstance(homepage, str) or not homepage.startswith("https://github.com/"):
        fail("Plugin manifest must include a GitHub homepage URL", errors)

    bugs = plugin_manifest.get("bugs")
    if not isinstance(bugs, dict):
        fail("Plugin manifest must include a 'bugs' object", errors)
    else:
        bugs_url = bugs.get("url")
        if not isinstance(bugs_url, str) or not bugs_url.startswith("https://github.com/"):
            fail("Plugin manifest must include a GitHub issues URL", errors)

    repository = plugin_manifest.get("repository")
    if not isinstance(repository, dict):
        fail("Plugin manifest must include a 'repository' object", errors)
    else:
        if repository.get("type") != "git":
            fail("Plugin manifest repository.type must be 'git'", errors)
        repository_url = repository.get("url")
        if not isinstance(repository_url, str) or not repository_url.startswith("https://github.com/"):
            fail("Plugin manifest must include a GitHub repository URL", errors)

    if not RELEASE_WORKFLOW.is_file():
        fail("Missing required file: .github/workflows/release.yml", errors)


def validate_boundary_policies(errors: list[str]) -> None:
    for policy_file in sorted(ROOT.glob(BOUNDARY_POLICY_GLOB)):
        payload = load_json(policy_file, errors)
        if not payload:
            continue
        if payload.get("version") != 1:
            fail(f"{policy_file.relative_to(ROOT)}: version must be 1", errors)
        for key in ("role", "feature", "mode"):
            value = payload.get(key)
            if not isinstance(value, str) or not value.strip():
                fail(f"{policy_file.relative_to(ROOT)}: {key} must be a non-empty string", errors)
        if payload.get("mode") not in {"enforce", "report"}:
            fail(f"{policy_file.relative_to(ROOT)}: mode must be 'enforce' or 'report'", errors)
        for key in ("allowed_write_globs", "blocked_write_globs", "allowed_touched_files"):
            value = payload.get(key, [])
            if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
                fail(f"{policy_file.relative_to(ROOT)}: {key} must be a list of non-empty strings", errors)
        for key in ("allow_new_files", "require_clean_git_start"):
            if key in payload and not isinstance(payload[key], bool):
                fail(f"{policy_file.relative_to(ROOT)}: {key} must be a boolean", errors)


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_ROOT_FILES:
        if not path.is_file():
            fail(f"Missing required file: {path.relative_to(ROOT)}", errors)

    plugin_manifest = load_json(PLUGIN_MANIFEST, errors)
    marketplace_manifest = load_json(MARKETPLACE_MANIFEST, errors)

    plugin_name = plugin_manifest.get("name")
    plugin_version = plugin_manifest.get("version")
    skills_value = plugin_manifest.get("skills")

    if not plugin_name:
        fail("Plugin manifest is missing 'name'", errors)

    if not plugin_version:
        fail("Plugin manifest is missing 'version'", errors)

    if not isinstance(skills_value, str):
        fail("Plugin manifest is missing string 'skills' path", errors)
    else:
        skills_dir = (ROOT / skills_value).resolve()
        if ROOT not in skills_dir.parents and skills_dir != ROOT:
            fail("Plugin 'skills' path resolves outside the repository", errors)
        else:
            validate_skill_tree(skills_dir, errors)

    if plugin_manifest and marketplace_manifest:
        validate_marketplace(plugin_manifest, marketplace_manifest, errors)
    if plugin_manifest:
        validate_github_distribution(plugin_manifest, errors)

    validate_boundary_policies(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed for plugin '{plugin_name}' ({plugin_version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
