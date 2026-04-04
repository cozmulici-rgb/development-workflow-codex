# Development Pipeline Codex Plugin

This repository is a Codex plugin repo for an orchestrator-led `development-pipeline` skill set.

## What is included

- `skills/development-pipeline-orchestrator/` contains the single user-facing orchestrator entrypoint
- `skills/development-pipeline/` contains the packaged workflow bundle, role references, and `agents/openai.yaml`
- `skills/development-pipeline-research/`, `skills/development-pipeline-design/`, `skills/development-pipeline-plan/`, and `skills/development-pipeline-implement/` expose phase-specific entrypoint skills
- `skills/development-pipeline-validation/` exposes the validation-team entrypoint
- `skills/development-pipeline-shared-orchestrator/`, `skills/development-pipeline-shared-worker/`, and `skills/development-pipeline-shared-reviewer/` package the shared runtime contracts used by leads, workers, and reviewers
- `.codex-plugin/plugin.json` defines the plugin manifest used by Codex
- `.agents/plugins/marketplace.json` exposes the repo as a local marketplace plugin
- `docs/claude-to-codex-integration.md` documents how the upstream Claude implementation maps into Codex

The Codex version in this repository keeps the portable parts:

- top-level orchestrator routing across planning, engineering, and validation
- four-phase workflow and human gates
- packaged shared behavior for orchestrators, workers, and reviewers
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
- validation team: validation lead, reviewers, and tester

Engineering now owns coding plus automated gates, then hands each completed phase to the validation team. Validation coordinates reviewers and tester through a dedicated entrypoint and returns a consolidated pass/fail verdict plus fix checklist.

The authoritative shared behavior contracts are now:

- `development-pipeline-shared-orchestrator` for orchestrators and leads
- `development-pipeline-shared-worker` for execution workers and tester-style reporting
- `development-pipeline-shared-reviewer` for actionable review output

## Memory And Sessions

Persistent per-agent memory is out of scope for this plugin. Packaged prompts should use the current conversation plus explicit repo artifacts as their context source, not hidden expertise files or implied session logs.

The workflow guarantees only explicit artifacts such as:

- research, design, and plan docs under `docs/`
- generated boundary policy files
- implementation handoff packages described by the references
- validation verdicts and fix checklists in the active session

Optional local logs may exist in the surrounding environment, but they are not part of the plugin contract. The repository-wide convention is documented in `docs/codex-agent-memory-and-sessions.md`.

## Local maintenance

- `make test` runs the standard-library `unittest` suite for the repo scripts
- `make validate` checks the plugin manifest, marketplace metadata, and skill frontmatter
- `make package` validates the repo and writes a versioned zip archive to `dist/`
- `make boundary-check POLICY=docs/plan/<feature>/boundary.phase-XX.json` verifies current Git changes against a write-boundary policy
- `make boundary-generate PLAN_DIR=docs/plan/<feature>` generates `boundary.phase-XX.json` files from phase docs

Both commands use only the Python 3 standard library.

## Next steps

If you want to evolve the plugin further, the most valuable additions are:

1. harden the boundary guard further around staged-only verification and stale-policy detection
2. simplify or remove remaining Claude-source metadata that is still carried only for reference
3. refine policy generation for broader real-plan conventions such as docs-only or migration-heavy phases
