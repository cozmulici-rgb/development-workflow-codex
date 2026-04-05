# Repository Guidelines

## Project Structure & Module Organization
This repository packages a Codex plugin and its skill assets. Current top-level areas:

- `skills/` for packaged Codex skills and their supporting files
- `.codex-plugin/` for the plugin manifest
- `.agents/plugins/` for local marketplace metadata
- `scripts/` for repo-local validation and packaging helpers
- `docs/` for contributor-facing documentation

The packaged workflow documents its Codex-native runtime assumptions in `docs/codex-agent-memory-and-sessions.md`. Keep prompt-level claims about memory, handoffs, and session artifacts aligned with that document.

Use small, focused modules and keep validation or packaging logic in standalone scripts rather than scattering it across ad hoc shell snippets.

## Build, Test, and Development Commands
The repository now provides local Make targets for the core maintenance workflow:

- `make validate` runs `scripts/validate_repo.py` to check plugin metadata, marketplace wiring, and skill frontmatter
- `make package` runs validation and builds a zip archive in `dist/`
- `python3 -m unittest discover -s tests -t .` runs the repo-maintenance script suite
- `make boundary-check POLICY=<path>` runs `scripts/write_boundary_guard.py verify` against a boundary policy file
- `make boundary-generate PLAN_DIR=<path>` runs `scripts/generate_boundary_policy.py` to derive policy files from phase plans
- `python3 scripts/compile_workflow_context.py <feature> --role <planning|engineering|validation>` compiles a deterministic role-specific brief from approved context and handoff artifacts
- `python3 scripts/record_workflow_session.py --label <name>` records optional local maintainer diagnostics; recorder output is not part of the packaged workflow contract
- `python3 scripts/validate_repo.py` is the direct entry point when you want script output without `make`
- `python3 scripts/package_plugin.py` is the direct packaging entry point
- `python3 scripts/write_boundary_guard.py ...` is the direct write-boundary guard entry point
- `python3 scripts/generate_boundary_policy.py <plan-dir>` is the direct policy generation entry point

The boundary tooling now preserves narrower workflow-artifact scopes such as `docs/context/**` and `docs/handoffs/**` when they are explicitly listed in approved phase plans.

If a write-boundary verifier is added or updated, document its invocation here and in `README.md`.

Document any additional commands in this file and `README.md` when new tooling is introduced.

## Coding Style & Naming Conventions
Use consistent, idiomatic style for the language you introduce. Default expectations for this repository:

- 4 spaces for Python, 2 spaces for JavaScript/JSON/YAML
- `snake_case` for Python modules, `kebab-case` for Markdown and config filenames
- Clear, descriptive names such as `tests/test_cli.py` or `docs/release-process.md`

Adopt an automatic formatter and linter with the first major code addition and commit their config with the codebase.

## Testing Guidelines
Use the standard-library `unittest` suite for repo-maintenance code. Run `python3 -m unittest discover -s tests -t .` for script changes, `make validate` for plugin metadata or packaged-skill checks, and `make package` when packaging behavior changes. Do not rely on manual checks alone for script behavior.

## Commit & Pull Request Guidelines
The current Git history contains a single commit: `Initial commit`. Follow that baseline with short, imperative commit subjects, and prefer focused commits such as `Add CLI skeleton` or `Document contributor workflow`.

Pull requests should include:

- a concise summary of the change
- linked issue or task reference when applicable
- test evidence or an explanation if tests are not yet available
- screenshots only for UI or rendered-document changes

## Documentation Expectations
When adding source code or tooling, update this guide so it stays accurate. Do not describe commands, directories, or workflows that do not exist in the repository.

When editing packaged workflow references, prefer explicit repo artifacts over implied runtime state. Do not add instructions that assume persistent expertise files or guaranteed session-log paths unless the repository actually ships that behavior.
