# Repository Guidelines

## Project Structure & Module Organization
This repository is currently minimal: the only tracked project file is [`LICENSE`](/Users/vcozmulici/workspace/ai/development-workflow-codex/LICENSE). There is no `src/`, `tests/`, or package manifest yet. As code is added, keep the layout predictable:

- `src/` for application code
- `tests/` for automated tests
- `docs/` for design notes and contributor-facing documentation
- `assets/` for static files such as images or sample data

Use small, focused modules and keep test files close to the feature area they validate or mirrored under `tests/`.

## Build, Test, and Development Commands
There are no build, test, or local run commands defined yet. Before adding tooling, prefer standard entry points so contributors can discover them quickly:

- `make test` or `npm test` for the main test suite
- `make lint` or `npm run lint` for style checks
- `make build` or `npm run build` for production artifacts

If you introduce a new toolchain, document the exact commands in this file and in a future `README.md`.

## Coding Style & Naming Conventions
Use consistent, idiomatic style for the language you introduce. Default expectations for this repository:

- 4 spaces for Python, 2 spaces for JavaScript/JSON/YAML
- `snake_case` for Python modules, `kebab-case` for Markdown and config filenames
- Clear, descriptive names such as `tests/test_cli.py` or `docs/release-process.md`

Adopt an automatic formatter and linter with the first major code addition and commit their config with the codebase.

## Testing Guidelines
No testing framework is configured yet. Add automated tests with the first feature change; do not rely on manual checks alone. Name tests after behavior, for example `test_handles_empty_input` or `cli.spec.ts`. Target meaningful coverage for new code and include regression tests for bug fixes.

## Commit & Pull Request Guidelines
The current Git history contains a single commit: `Initial commit`. Follow that baseline with short, imperative commit subjects, and prefer focused commits such as `Add CLI skeleton` or `Document contributor workflow`.

Pull requests should include:

- a concise summary of the change
- linked issue or task reference when applicable
- test evidence or an explanation if tests are not yet available
- screenshots only for UI or rendered-document changes

## Documentation Expectations
When adding source code or tooling, update this guide so it stays accurate. Do not describe commands, directories, or workflows that do not exist in the repository.
