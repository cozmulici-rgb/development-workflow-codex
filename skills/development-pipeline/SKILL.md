---
name: development-pipeline
description: Coordinate the four-phase agentic development pipeline (research, design, plan, implement) with strict human gates; use when the task needs structured research/design artifacts, phased planning, and gated implementation reviews tested by reviewers and a tester before writing code.
---

# Development Pipeline

## Overview
Follow the four-phase flow described in `references/README.md`: research generates factual repo findings through focused sub-agents, design freezes the solution through a gated `discussion.md` plus full design artifacts, plan converts `structure-outline.md` into vertical slices, and implement executes each approved phase with coder, reviewer, and tester gates.

## Typical workflow
1. Start with `references/research-lead.md`, then load only the matching `references/research-subagent-*.md` files needed for architecture, patterns, integrations, domain, API, testing, and optional fintech facts. Research sub-agents investigate questions, not the ticket directly.
2. After research approval, use `references/design.md` to produce `discussion.md` first, pause for human approval, then complete the full artifact set including `structure-outline.md`.
3. Use `references/plan.md` only after design approval. Treat `structure-outline.md` as the authoritative phase map and enforce vertical slices instead of horizontal layers.
4. During implementation, use `references/implement-lead.md` to coordinate `implement-coder`, reviewers, and `tester` per phase. Code is written only in this phase.

## Reviews and testing
- For reviewer guidance, consult `references/reviewer-quality.md`, `references/reviewer-architecture.md`, `references/reviewer-security.md`, and `references/reviewer-plan-compliance.md` to validate readability, architectural boundaries, security posture, and plan fidelity before advancing phases.
- For fintech work, also consult `references/reviewer-fintech-compliance.md`, `references/reviewer-fintech-patterns.md`, and `references/research-subagent-fintech-domain.md`.
- Use `references/tester.md` for test execution steps, regression reporting, and final readiness checks.

## Claude Source Mapping
This plugin intentionally tracks the current upstream Claude workflow from `../../mysites/ai-toolbox-experiments/claude/agents/development-pipeline/`. The files in `references/` are the Codex-packaged copies of that workflow. `references/teams.yaml` is included as source context for roles, models, and domain boundaries even though Codex does not consume Claude `teams.yaml` directly at runtime.

## Validation
Run `~/.codex/tools/skill-validator/quick_validate.py <skill-dir-or-tree>` after editing this skill to catch frontmatter, naming, link, and metadata issues early. Use `~/.codex/skills/` to validate every installed skill tree.

## References
Load the files below exactly when their scope matches the current phase or role rather than reading everything at once:
- `references/README.md`: full pipeline map and agent roles.
- `references/research-lead.md`: decomposing tickets into confirmed facts.
- `references/research-subagent-*.md`: focused research checks; include the fintech variant when the domain requires it.
- `references/design.md`: design-phase deliverables, the `discussion.md` gate, and final `structure-outline.md`.
- `references/plan.md`: phased implementation plan template and vertical-slice gating expectations.
- `references/implement-lead.md` and `references/implement-coder.md`: implement-phase orchestration and coding policies.
- `references/reviewer-*.md` plus `references/tester.md`: final QA loop.
- `references/teams.yaml`: upstream Claude team, skill, model, and domain configuration for source alignment.
