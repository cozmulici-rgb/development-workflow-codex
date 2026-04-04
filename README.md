# Development Pipeline for Codex

`development-pipeline` is a Codex plugin that brings a structured delivery workflow to Codex. It is designed for teams that want clear phase boundaries, explicit handoffs, and repeatable engineering discipline instead of an informal prompt-to-code loop.

The plugin provides an orchestrator-led flow across research, design, planning, implementation, and validation, with human approval points between phases.

## Overview

Use this plugin when you want Codex to:

- turn a feature request into research, design, planning, and implementation artifacts
- keep code changes aligned to an approved phase plan
- separate planning, engineering, and validation responsibilities
- produce structured handoffs that are easier to review and validate

It is best suited to larger or higher-discipline work where consistency and reviewability matter.

## Included Skills

The plugin ships the following Codex skills:

- `development-pipeline-orchestrator`: the main user-facing entrypoint
- `development-pipeline`: the packaged workflow bundle and shared references
- `development-pipeline-research`: research-stage entrypoint
- `development-pipeline-design`: design-stage entrypoint
- `development-pipeline-plan`: planning-stage entrypoint
- `development-pipeline-implement`: engineering-stage entrypoint
- `development-pipeline-validation`: validation-stage entrypoint
- `development-pipeline-shared-orchestrator`: shared contract for orchestrators and leads
- `development-pipeline-shared-worker`: shared contract for execution workers
- `development-pipeline-shared-reviewer`: shared contract for reviewers

Supporting repository assets include:

- `.codex-plugin/plugin.json`: Codex plugin manifest
- `.agents/plugins/marketplace.json`: local marketplace metadata
- `docs/`: workflow references and contributor documentation
- `scripts/`: repo-local validation, packaging, and write-boundary tooling

## Workflow Model

The workflow is organized around three top-level responsibilities:

- Planning: research, design, and plan creation
- Engineering: implementation against an approved phase plan
- Validation: review and testing after engineering completes a phase

For most users, the correct starting point is `development-pipeline-orchestrator`. That skill acts as the primary entrypoint and routes work to the appropriate stage.

## Installation

Install this repository as a local Codex plugin, then enable `development-pipeline` in your Codex environment.

The repository already includes the required plugin metadata:

- `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`

If your Codex setup uses a local marketplace, point it at this repository and install the plugin from that local source.

## Recommended Usage

For most work, start with the orchestrator skill and describe the desired outcome:

```text
Use the development-pipeline-orchestrator skill to take this feature through research, design, planning, implementation, and validation.
```

You can also invoke stage-specific skills directly when you already know which phase you need:

- `development-pipeline-research` for discovery and requirements clarification
- `development-pipeline-design` for technical design and implementation approach
- `development-pipeline-plan` for explicit phase plans and file-level scope
- `development-pipeline-implement` when a phase plan is approved and coding can begin
- `development-pipeline-validation` for post-implementation review and test coordination

## Runtime Assumptions

This plugin is Codex-native. It does not assume hidden runtime features that the repository does not ship.

Specifically:

- it does not depend on persistent per-agent expertise files
- it does not assume guaranteed session-log paths
- it does not implement provider-specific pre-write hook enforcement

The workflow relies on explicit repository artifacts and current conversation context. The authoritative description of these assumptions lives in `docs/codex-agent-memory-and-sessions.md`.

## Write-Boundary Tooling

The repository includes optional write-boundary tooling for implementation phases:

- `make boundary-generate PLAN_DIR=docs/plan/<feature>` generates boundary policy files from phase plans
- `make boundary-check POLICY=docs/plan/<feature>/boundary.phase-XX.json` verifies current Git changes against a boundary policy

Direct script entrypoints are also available:

- `python3 scripts/generate_boundary_policy.py <plan-dir>`
- `python3 scripts/write_boundary_guard.py start --policy <path>`
- `python3 scripts/write_boundary_guard.py verify --policy <path>`
- `python3 scripts/write_boundary_guard.py report --policy <path>`
- `python3 scripts/write_boundary_guard.py stage --policy <path> -- <files...>`

More detail is documented in `docs/codex-write-boundary-guard.md`.

## Maintainer Commands

If you are developing or maintaining this plugin:

- `make validate` checks plugin metadata, marketplace wiring, and skill frontmatter
- `make test` runs the repository test suite
- `make package` validates the repo and builds a zip archive in `dist/`

The maintenance scripts use the Python 3 standard library only.

## Repository Layout

- `skills/`: packaged Codex skills
- `.codex-plugin/`: plugin manifest
- `.agents/plugins/`: local plugin marketplace metadata
- `scripts/`: validation, packaging, and boundary scripts
- `docs/`: workflow and contributor documentation

## Limitations

This plugin provides workflow guidance and packaged prompts. It does not, by itself:

- guarantee that every Codex environment supports identical plugin installation flows
- provide persistent memory across sessions
- enforce pre-write filesystem hooks
- replace human approval for important design or implementation decisions

## License

This repository is licensed under MIT. See `LICENSE`.
