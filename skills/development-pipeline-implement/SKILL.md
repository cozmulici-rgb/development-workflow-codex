---
name: development-pipeline-implement
description: Execute an approved development-pipeline plan phase by phase on the engineering side, then hand completed work to the validation team for review and test coordination.
---

# Development Pipeline Implement

## Use this skill when
Use this skill only after the phased implementation plan is approved and code is allowed to be written.

## Workflow
1. Load `../development-pipeline/references/implement-lead.md`.
2. Use `../development-pipeline/references/implement-coder.md` for coding policy.
3. Execute one approved phase at a time, preserving plan fidelity and automated gates on the engineering side.
4. Hand the completed phase package to `../development-pipeline-validation/SKILL.md` for review and test coordination.
5. Use the validation verdict to decide whether engineering needs fixes before advancing.

## Boundaries
- Write code only for the currently approved phase.
- Do not absorb validation-team ownership back into engineering.
- Escalate any need to change the approved plan before proceeding.
