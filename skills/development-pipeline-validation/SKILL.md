---
name: development-pipeline-validation
description: Coordinate validation for an approved implementation phase by running review and test workflows against the engineer-provided handoff package.
---

# Development Pipeline Validation

## Use this skill when
Use this skill after engineering completes an implementation phase and automated gates have produced a candidate change set that needs review and test coordination.

## Workflow
1. Load `../development-pipeline/references/validation-lead.md`.
2. Accept the engineering handoff package: phase plan, changed file list or diff, relevant design and research context, and automated gate results.
3. Coordinate the reviewer and tester references named in `../development-pipeline/references/teams.yaml`.
4. Return a consolidated verdict, fix checklist when needed, and an explicit pass/fail handoff back to the orchestrator.

## Boundaries
- Do not write production code.
- Keep validation focused on review and test coordination for the current approved phase.
- Escalate plan or design contradictions rather than expanding scope during validation.
