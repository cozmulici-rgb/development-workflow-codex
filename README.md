# Development Pipeline Codex Plugin

This repository is a Codex plugin repo for an orchestrator-led `development-pipeline` skill set.

## What is included

- `skills/development-pipeline-orchestrator/` contains the single user-facing orchestrator entrypoint
- `skills/development-pipeline/` contains the packaged workflow bundle, role references, and `agents/openai.yaml`
- `skills/development-pipeline-research/`, `skills/development-pipeline-design/`, `skills/development-pipeline-plan/`, and `skills/development-pipeline-implement/` expose phase-specific entrypoint skills
- `.codex-plugin/plugin.json` defines the plugin manifest used by Codex
- `.agents/plugins/marketplace.json` exposes the repo as a local marketplace plugin
- `docs/claude-to-codex-integration.md` documents how the upstream Claude implementation maps into Codex

The Codex version in this repository keeps the portable parts:

- top-level orchestrator routing across planning, engineering, and validation
- four-phase workflow and human gates
- role-specific reference prompts
- reviewer and tester guidance
- a plugin manifest plus skill packaging

It includes the upstream prompt and config files for alignment. The Claude phase entrypoints are represented here as Codex extra skills instead of slash commands. Claude-only mechanics such as `teams.yaml`-driven runtime injection, expertise persistence, and the pre-tool domain-lock hook are still not replicated verbatim.

## Local install

From Codex, add this repo as a local marketplace and install `development-pipeline` from it. Start from `development-pipeline-orchestrator` when you want the full packaged workflow through a single entrypoint.

## Team model

The packaged workflow exposes this top-level routing model:

- orchestrator: `development-pipeline-orchestrator`
- planning team: research, design, and plan stages
- engineering team: implement lead plus coder
- validation team: reviewers plus tester

Phase 01 only establishes this topology. The four-phase workflow remains the underlying execution model, and validation is still coordinated through the current implementation references until a dedicated validation entrypoint is added.

## Local maintenance

- `make test` runs the standard-library `unittest` suite for the repo scripts
- `make validate` checks the plugin manifest, marketplace metadata, and skill frontmatter
- `make package` validates the repo and writes a versioned zip archive to `dist/`
- `make boundary-check POLICY=docs/plan/<feature>/boundary.phase-XX.json` verifies current Git changes against a write-boundary policy
- `make boundary-generate PLAN_DIR=docs/plan/<feature>` generates `boundary.phase-XX.json` files from phase docs

Both commands use only the Python 3 standard library.

## Next steps

If you want to evolve the plugin further, the most valuable additions are:

1. split validation into its own packaged team entrypoint and lead reference
2. harden the boundary guard further around staged-only verification and stale-policy detection
3. refine policy generation for broader real-plan conventions such as docs-only or migration-heavy phases
