---
name: development-pipeline
description: Internal reference bundle for maintainers or advanced workflow work on the development-pipeline package; use it to inspect or update the packaged references behind the orchestrator-led workflow.
---

# Development Pipeline

## Overview
This skill is the packaged reference bundle behind the explicit `development-pipeline-orchestrator` entrypoint. Use it for maintainer work on the workflow package itself, or when you need to inspect the full packaged reference set behind the orchestrated model. For normal workflow execution, start from `development-pipeline-orchestrator` instead.

## Typical workflow
1. Start from `references/README.md` and `references/teams.yaml` to align on the orchestrator-led hierarchy before loading stage-specific references.
2. Route planning work through `references/research-lead.md`, `references/design.md`, and `references/plan.md` in order. Preserve the research approval gate, the `discussion.md` gate, and the final design/plan approval gates.
3. Route engineering execution through `references/implement-lead.md` and `references/implement-coder.md`. Code is still written only in the implementation phase.
4. Keep reviewer and tester checks explicit in reports so validation remains a first-class concern even where current execution is still coordinated from the implementation loop.

## Reviews and testing
- For reviewer guidance, consult `references/reviewer-quality.md`, `references/reviewer-architecture.md`, `references/reviewer-security.md`, and `references/reviewer-plan-compliance.md` to validate readability, architectural boundaries, security posture, and plan fidelity before advancing phases.
- For fintech work, also consult `references/reviewer-fintech-compliance.md`, `references/reviewer-fintech-patterns.md`, and `references/research-subagent-fintech-domain.md`.
- Use `references/tester.md` for test execution steps, regression reporting, and final readiness checks.

## Upstream Source Mapping
This plugin tracks an upstream development-pipeline workflow maintained outside this package. The files in `references/` are the Codex-packaged copies adapted for this repository. `references/teams.yaml` is carried as packaged topology context for the orchestrator, planning, engineering, and validation layers even though Codex does not consume that file directly at runtime.

## Validation
Run `~/.codex/tools/skill-validator/quick_validate.py <skill-dir-or-tree>` after editing this skill to catch frontmatter, naming, link, and metadata issues early. Use `~/.codex/skills/` to validate every installed skill tree.

## References
Load the files below exactly when their scope matches the current phase or role rather than reading everything at once:
- `references/README.md`: orchestrator-led workflow map and packaged team roles.
- `../development-pipeline-orchestrator/SKILL.md`: single user-facing entrypoint for the packaged workflow.
- `references/research-lead.md`: decomposing tickets into confirmed facts.
- `references/research-subagent-*.md`: focused research checks; include the fintech variant when the domain requires it.
- `references/design.md`: design-phase deliverables, the `discussion.md` gate, and final `structure-outline.md`.
- `references/plan.md`: phased implementation plan template and vertical-slice gating expectations.
- `references/implement-lead.md` and `references/implement-coder.md`: implement-phase orchestration and coding policies.
- `references/reviewer-*.md` plus `references/tester.md`: final QA loop.
- `references/teams.yaml`: packaged orchestrator, planning, engineering, and validation topology for source alignment.
