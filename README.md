# Development Pipeline Codex Plugin

This repository is a Codex plugin repo for the `development-pipeline` skill set.

## What is included

- `skills/development-pipeline/` contains the top-level Codex skill, role references, and `agents/openai.yaml`
- `skills/development-pipeline-research/`, `skills/development-pipeline-design/`, `skills/development-pipeline-plan/`, and `skills/development-pipeline-implement/` expose phase-specific entrypoint skills
- `.codex-plugin/plugin.json` defines the plugin manifest used by Codex
- `.agents/plugins/marketplace.json` exposes the repo as a local marketplace plugin
- `docs/claude-to-codex-integration.md` documents how the upstream Claude implementation maps into Codex

The Codex version in this repository keeps the portable parts:

- four-phase workflow and human gates
- role-specific reference prompts
- reviewer and tester guidance
- a plugin manifest plus skill packaging

It includes the upstream prompt and config files for alignment. The Claude phase entrypoints are represented here as Codex extra skills instead of slash commands. Claude-only mechanics such as `teams.yaml`-driven runtime injection, expertise persistence, and the pre-tool domain-lock hook are still not replicated verbatim.

## Next steps

## Local install

From Codex, add this repo as a local marketplace and install `development-pipeline` from it. 

## Local maintenance

- `make validate` checks the plugin manifest, marketplace metadata, and skill frontmatter
- `make package` validates the repo and writes a versioned zip archive to `dist/`
- `make boundary-check POLICY=docs/plan/<feature>/boundary.phase-XX.json` verifies current Git changes against a write-boundary policy
- `make boundary-generate PLAN_DIR=docs/plan/<feature>` generates `boundary.phase-XX.json` files from phase docs

Both commands use only the Python 3 standard library.

## Next steps

If you want to evolve the plugin further, the most valuable additions are:

1. expand validation to cover deeper Markdown link checks or release-policy rules
2. import or sync the upstream Claude command prompt text into the new phase-specific skills when that source is available
3. implement the verifier described in `docs/codex-write-boundary-guard.md` and wire it into the implementation workflow
