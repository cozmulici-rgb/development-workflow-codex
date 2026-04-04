---
name: development-pipeline-shared-worker
description: Shared Codex-native contract for execution-focused workers that read the assigned scope, act within declared boundaries, and return detailed, file-specific reports.
---

# Development Pipeline Shared Worker

## Use this skill when
Use this shared asset for workers that execute the assigned phase work or run structured validation tasks inside a bounded scope.

## Shared contract
1. Read the assigned plan, handoff package, or review scope before acting.
2. Stay inside the declared file and responsibility boundaries.
3. Follow existing repo patterns instead of inventing new conventions.
4. Return detailed output with explicit files, checks run, and unresolved blockers.

## Required behaviors
- Do not expand scope beyond the assigned phase or handoff package.
- When blocked, report the exact missing input or failing condition.
- Prefer concrete evidence over general commentary.
- Make the final report reusable by the orchestrator or lead without re-analysis.
