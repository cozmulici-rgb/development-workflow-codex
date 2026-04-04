---
name: development-pipeline-orchestrator
description: Use the Codex-native orchestrator entrypoint to route work across the development pipeline's planning, engineering, and validation teams while preserving the gated four-phase workflow.
---

# Development Pipeline Orchestrator

## Use this skill when
Use this skill as the single user-facing entrypoint for the packaged workflow when a task needs to be routed through planning, engineering, and validation concerns.

## Workflow
1. Load `../development-pipeline/references/README.md` for the orchestrator-led workflow map.
2. Load `../development-pipeline/references/teams.yaml` for the packaged team topology.
3. Route planning work to the research, design, and plan stages without skipping their human gates.
4. Route engineering execution through `../development-pipeline-implement/SKILL.md`.
5. Keep validation visible as its own team concern in reports and handoffs, even where the current implementation loop still coordinates reviews from engineering references.

## Boundaries
- Keep the orchestrator as the single interface presented to the user.
- Preserve the existing four-phase pipeline as the internal execution model.
- Do not change implementation ownership beyond the packaged references for the current phase.
