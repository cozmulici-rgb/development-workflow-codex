# Claude to Codex Integration Notes

## Goal

Integrate the `development-pipeline` feature from the upstream Claude plugin into this repository as a Codex plugin.

## Upstream feature inventory

The Claude implementation is split across:

- `claude/agents/development-pipeline/`: phase leads, research sub-agents, reviewers, tester, and `teams.yaml`
- `claude/commands/development-pipeline/`: phase entrypoints for research, design, plan, and implement
- `claude/expertise/development-pipeline/`: persistent per-agent memory files
- `claude/skills/shared/`: reusable prompt fragments used by the teams config
- `claude/hooks/domain-lock.sh`: write-boundary enforcement for agent tool calls

## Codex mapping

Codex already had a distilled local skill at [`skills/development-pipeline/SKILL.md`](/Users/vcozmulici/workspace/ai/development-workflow-codex/skills/development-pipeline/SKILL.md). That structure maps well to the core Claude feature:

- Claude agent prompts become Codex reference files under [`skills/development-pipeline/references`](/Users/vcozmulici/workspace/ai/development-workflow-codex/skills/development-pipeline/references)
- Claude plugin metadata becomes [`.codex-plugin/plugin.json`](/Users/vcozmulici/workspace/ai/development-workflow-codex/.codex-plugin/plugin.json)
- Claude agent discoverability maps to [`skills/development-pipeline/agents/openai.yaml`](/Users/vcozmulici/workspace/ai/development-workflow-codex/skills/development-pipeline/agents/openai.yaml)

## What was integrated

- Added a Codex plugin manifest to make the repository installable as a plugin
- Replaced the older Codex reference set with the current upstream Claude `development-pipeline` files under `skills/`
- Added repository documentation describing the upstream source and the migration boundary

## Gaps and decisions

- Claude slash commands are not first-class Codex plugin primitives here, so they were not copied directly
- `teams.yaml` is Claude runtime configuration; Codex currently uses the skill and agent metadata instead
- `domain-lock.sh` depends on Claude hook semantics and JSON tool payloads; it needs a Codex-specific design before adoption
- Claude expertise files represent persistent agent memory; Codex has different memory primitives, so this was left out

## Recommended follow-up

1. Add a sync script that diffs the upstream Claude prompts against the Codex `references/` tree.
2. Decide whether to expose phase-specific helper skills such as `development-pipeline-research` and `development-pipeline-plan`.
3. If strict write-domain enforcement matters, implement a Codex-native guard as a script or documented workflow instead of copying the Claude hook unchanged.
