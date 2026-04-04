---
name: development-pipeline
description: Package the full development-pipeline workflow beneath an explicit orchestrator model, preserving the gated research, design, plan, and implement phases as internal execution stages.
---

# Development Pipeline

## Overview
This skill is the packaged workflow bundle behind the explicit `development-pipeline-orchestrator` entrypoint. Use it when you need the full reference set for the orchestrated model: planning routes through research, design, and plan; engineering routes through implement; validation remains a visible team concern around review and test gates.

## Typical workflow
1. Start from `references/README.md` and `references/teams.yaml` to align on the orchestrator-led hierarchy before loading stage-specific references.
2. Route planning work through `references/research-lead.md`, `references/design.md`, and `references/plan.md` in order. Preserve the research approval gate, the `discussion.md` gate, and the final design/plan approval gates.
3. Route engineering execution through `references/implement-lead.md` and `references/implement-coder.md`. Code is still written only in the implementation phase.
4. Keep reviewer and tester checks explicit in reports so validation remains a first-class concern even where current execution is still coordinated from the implementation loop.

## Reviews and testing
- For reviewer guidance, consult `references/reviewer-quality.md`, `references/reviewer-architecture.md`, `references/reviewer-security.md`, and `references/reviewer-plan-compliance.md` to validate readability, architectural boundaries, security posture, and plan fidelity before advancing phases.
- For fintech work, also consult `references/reviewer-fintech-compliance.md`, `references/reviewer-fintech-patterns.md`, and `references/research-subagent-fintech-domain.md`.
- Use `references/tester.md` for test execution steps, regression reporting, and final readiness checks.

## Claude Source Mapping
This plugin intentionally tracks the current upstream Claude workflow from `../../mysites/ai-toolbox-experiments/claude/agents/development-pipeline/`. The files in `references/` are the Codex-packaged copies of that workflow. `references/teams.yaml` is carried as packaged topology context for the orchestrator, planning, engineering, and validation layers even though Codex does not consume Claude `teams.yaml` directly at runtime.

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
