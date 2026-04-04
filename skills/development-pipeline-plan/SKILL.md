---
name: development-pipeline-plan
description: Convert an approved development-pipeline design into a phased implementation plan using the plan reference and vertical slices anchored to structure-outline.md.
---

# Development Pipeline Plan

## Use this skill when
Use this skill after the design artifacts are approved and implementation phases need to be defined without writing code yet.

## Workflow
1. Load `../development-pipeline/references/plan.md`.
2. Treat `structure-outline.md` as the authoritative phase map.
3. Produce vertical implementation slices with clear acceptance criteria, dependencies, and review gates.
4. Stop after the phased plan is ready for approval.

## Boundaries
- Do not collapse the plan into horizontal layer work.
- Do not start implementation during planning.
- Keep every phase independently reviewable and testable.
