# Development Pipeline Codex Plugin

This repository is a Codex plugin repo for the `development-pipeline` skill.
Its packaged references are synced to the current Claude workflow under `ai-toolbox-experiments/claude/agents/development-pipeline/`, not the older `~/.codex/skills/development-pipeline` copy.

## What is included

- `skills/development-pipeline/` contains the Codex skill, role references, and `agents/openai.yaml`
- `.codex-plugin/plugin.json` defines the plugin manifest used by Codex
- `.agents/plugins/marketplace.json` exposes the repo as a local marketplace plugin
- `docs/claude-to-codex-integration.md` documents how the upstream Claude implementation maps into Codex

## Source of truth

The pipeline concept was investigated from the upstream Claude implementation at:

- `../../mysites/ai-toolbox-experiments/claude/agents/development-pipeline/`
- `../../mysites/ai-toolbox-experiments/claude/commands/development-pipeline/`
- `../../mysites/ai-toolbox-experiments/claude/hooks/domain-lock.sh`

The Codex version in this repository keeps the portable parts:

- four-phase workflow and human gates
- role-specific reference prompts
- reviewer and tester guidance
- a plugin manifest plus skill packaging

It includes the upstream prompt and config files for alignment, but does not try to replicate Claude-only mechanics such as slash commands, `teams.yaml`-driven runtime injection, expertise persistence, or the pre-tool domain-lock hook verbatim.

## Next steps

## Local install

From Codex, add this repo as a local marketplace and install `development-pipeline` from it. After that, you can remove or ignore the home-installed `~/.codex/skills/development-pipeline` copy.

## Next steps

If you want to evolve the plugin further, the most valuable additions are:

1. add repo-local validation or packaging scripts
2. decide whether Claude command prompts should become Codex helper docs or extra skills
3. design a Codex-native replacement for write-boundary enforcement if strict domain locks are required
