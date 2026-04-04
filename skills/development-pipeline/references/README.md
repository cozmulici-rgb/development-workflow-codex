# Development Pipeline

The packaged workflow is now organized around a Codex-native orchestrator layer:

`development-pipeline-orchestrator` → planning team / engineering team / validation team

The internal execution model remains the same four-phase pipeline:

Research → Design → Plan → Implement

Code is still written only during the implementation phase. Research, design, and planning continue to produce gated artifacts that become the approved input to the next stage.

---

## Overview

**Core principle:** keep one user-facing interface while preserving strict internal phase boundaries.

- The orchestrator is the single packaged entrypoint presented to the user.
- Planning owns research, design, and plan as ordered internal stages.
- Engineering owns implementation execution and automated gates.
- Validation owns reviewer and tester coordination after engineering hands off a completed phase package.

---

## Workflow Hierarchy

```
development-pipeline-orchestrator
  ├── Planning team
  │     ├── research-lead
  │     ├── design
  │     └── plan
  ├── Engineering team
  │     ├── implement-lead
  │     └── implement-coder
  └── Validation team
        ├── validation-lead
        ├── reviewer-quality
        ├── reviewer-architecture
        ├── reviewer-security
        ├── reviewer-plan-compliance
        ├── reviewer-fintech-compliance
        ├── reviewer-fintech-patterns
        └── tester
```

---

## Internal Phase Flow

```
Planning team
  A. Research
    research-lead
      ├── research-subagent-architecture
      ├── research-subagent-patterns
      ├── research-subagent-integrations
      ├── research-subagent-domain
      ├── research-subagent-api
      ├── research-subagent-tests
      └── research-subagent-fintech-domain (fintech only)
    Human gate: approve research document

  B. Design
    design
      ├── Step 1: discussion.md
      ├── Step 2: architecture.md, dataflow.md, sequence.md,
      │           contracts.md, testing.md, adr.md
      └── Step 3: structure-outline.md
    Human gates: approve discussion, then approve design artifacts

  C. Plan
    plan
      ├── reads structure-outline.md as the authoritative phase map
      └── produces vertical implementation slices
    Human gate: approve implementation plan

Engineering team
  D. Implement
    implement-lead
      └── implement-coder
    Output: validated handoff package for the current phase

Validation team
  validation-lead
    ├── reviewer-quality
    ├── reviewer-architecture
    ├── reviewer-security
    ├── reviewer-plan-compliance
    ├── reviewer-fintech-compliance
    ├── reviewer-fintech-patterns
    └── tester
  Output: consolidated pass/fail verdict plus fix checklist
```

---

## Topology Notes

- `teams.yaml` is the packaged source-of-truth for the orchestrator-led hierarchy and stage ownership map.
- The current Codex plugin exposes the orchestrator and phase entrypoints as skills rather than slash commands.
- Shared behavior is now packaged in Codex-native assets:
  - `../development-pipeline-shared-orchestrator/SKILL.md`
  - `../development-pipeline-shared-worker/SKILL.md`
  - `../development-pipeline-shared-reviewer/SKILL.md`
- Boundary enforcement in Codex remains policy-driven through `scripts/generate_boundary_policy.py` and `scripts/write_boundary_guard.py`.
- Claude-specific runtime mechanics such as automatic shared-skill injection or persistent expertise loading are still reference concepts, not active Codex runtime features.

---

## Team To Stage Mapping

| Team | Scope | Primary references |
|------|-------|--------------------|
| Orchestrator | Single user-facing routing and synthesized handoff state | `../development-pipeline-orchestrator/SKILL.md`, `../development-pipeline-shared-orchestrator/SKILL.md`, `teams.yaml` |
| Planning | Research, design, and plan stages with their approval gates | `../development-pipeline-shared-orchestrator/SKILL.md`, `research-lead.md`, `design.md`, `plan.md` |
| Engineering | Implement approved phases, run automated gates, and prepare handoff packages | `../development-pipeline-shared-orchestrator/SKILL.md`, `../development-pipeline-shared-worker/SKILL.md`, `implement-lead.md`, `implement-coder.md` |
| Validation | Review and test the engineering handoff package, then return a verdict | `../development-pipeline-shared-orchestrator/SKILL.md`, `../development-pipeline-shared-reviewer/SKILL.md`, `../development-pipeline-shared-worker/SKILL.md`, `validation-lead.md`, `reviewer-*.md`, `tester.md` |

---

## Phase Reference

| Internal phase | Owning team | Lead reference | Outputs | Human gate |
|----------------|-------------|----------------|---------|------------|
| Research | Planning | `research-lead` | `docs/research/<feature>.md` | Approve research doc |
| Design | Planning | `design` | `discussion.md`, design artifacts, `structure-outline.md` | Approve discussion, then design artifacts |
| Plan | Planning | `plan` | `docs/plan/<feature>/` | Approve plan |
| Implement | Engineering | `implement-lead` | code, tests, automated gate results, handoff package | Validation reviews output |
| Validate | Validation | `validation-lead` | consolidated review verdict, fix checklist, pass/fail handoff | Orchestrator decides whether to proceed |

---

## Entry Points

- `development-pipeline-orchestrator`: single packaged entrypoint for the orchestrator-led workflow
- `development-pipeline`: full packaged reference bundle
- `development-pipeline-research`: phase entrypoint for research work
- `development-pipeline-design`: phase entrypoint for design work
- `development-pipeline-plan`: phase entrypoint for planning work
- `development-pipeline-implement`: phase entrypoint for implementation work
- `development-pipeline-validation`: phase entrypoint for validation work
- `development-pipeline-shared-orchestrator`: shared lead and orchestrator contract
- `development-pipeline-shared-worker`: shared execution and tester reporting contract
- `development-pipeline-shared-reviewer`: shared actionable-review contract
