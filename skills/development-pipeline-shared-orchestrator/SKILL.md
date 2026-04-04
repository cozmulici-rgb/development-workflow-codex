---
name: development-pipeline-shared-orchestrator
description: Shared Codex-native contract for orchestrators and team leads that delegate execution, keep reports concise, and hand off work with explicit inputs and outputs.
---

# Development Pipeline Shared Orchestrator

## Use this skill when
Use this shared asset for orchestrators and team leads that coordinate work across specialized workers without writing production changes themselves.

## Shared contract
1. Read the approved inputs for the current phase before delegating.
2. Delegate execution to the smallest responsible worker or team.
3. Keep handoff packages explicit: required inputs, expected outputs, and blocking conditions.
4. Return concise synthesized status with clear pass/fail or ready/blocked decisions.

## Required behaviors
- Do not perform production-code edits directly when a delegated worker owns that scope.
- Keep delegation boundaries explicit and phase-local.
- Escalate plan or design contradictions instead of silently inventing scope.
- Consolidate downstream findings into one actionable handoff.
