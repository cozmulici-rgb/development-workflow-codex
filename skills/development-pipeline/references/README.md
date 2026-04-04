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
- Engineering owns implementation execution.
- Validation remains an explicit team concern for reviews and testing, even where the current implementation loop still drives those steps.

This phase establishes the topology and routing contract only. It does not yet change the underlying implementation behavior.

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

Validation team
  Review and test outputs around each implementation phase
```

---

## Topology Notes

- `teams.yaml` is the packaged source-of-truth for the orchestrator-led hierarchy and stage ownership map.
- The current Codex plugin exposes the orchestrator and phase entrypoints as skills rather than slash commands.
- Boundary enforcement in Codex remains policy-driven through `scripts/generate_boundary_policy.py` and `scripts/write_boundary_guard.py`.
- Claude-specific runtime mechanics such as automatic shared-skill injection or persistent expertise loading are still reference concepts, not active Codex runtime features.

---

## Team To Stage Mapping

| Team | Scope | Primary references |
|------|-------|--------------------|
| Orchestrator | Single user-facing routing and synthesized handoff state | `../development-pipeline-orchestrator/SKILL.md`, `teams.yaml` |
| Planning | Research, design, and plan stages with their approval gates | `research-lead.md`, `design.md`, `plan.md` |
| Engineering | Implement approved phases and produce candidate changes | `implement-lead.md`, `implement-coder.md` |
| Validation | Review and test implementation output | `reviewer-*.md`, `tester.md` |

---

## Phase Reference

| Internal phase | Owning team | Lead reference | Outputs | Human gate |
|----------------|-------------|----------------|---------|------------|
| Research | Planning | `research-lead` | `docs/research/<feature>.md` | Approve research doc |
| Design | Planning | `design` | `discussion.md`, design artifacts, `structure-outline.md` | Approve discussion, then design artifacts |
| Plan | Planning | `plan` | `docs/plan/<feature>/` | Approve plan |
| Implement | Engineering with validation review loop | `implement-lead` | code, tests, review/test results | Review implementation output |

---

## Entry Points

- `development-pipeline-orchestrator`: single packaged entrypoint for the orchestrator-led workflow
- `development-pipeline`: full packaged reference bundle
- `development-pipeline-research`: phase entrypoint for research work
- `development-pipeline-design`: phase entrypoint for design work
- `development-pipeline-plan`: phase entrypoint for planning work
- `development-pipeline-implement`: phase entrypoint for implementation work
