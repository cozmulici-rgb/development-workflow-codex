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
- Memory and session behavior follow `../../../docs/codex-agent-memory-and-sessions.md`.
- Boundary enforcement in Codex remains policy-driven through `scripts/generate_boundary_policy.py` and `scripts/write_boundary_guard.py`.
- Persistent expertise loading is not part of the packaged Codex runtime contract. Durable workflow state lives in explicit repo artifacts such as research, design, plan, `docs/context/` artifacts, `docs/handoffs/` packages, boundary, and validation outputs.
- Handoff packages are the required cross-team coordination unit whenever work moves between planning, engineering, validation, or the orchestrator.
- Artifact-memory files are the durable fact layer whenever a summary should stay useful beyond a single handoff.
- Downstream stages should trust only approved, current, non-superseded durable artifacts unless the active handoff records a human override.
- Compiled role briefs are optional derived artifacts that may be read when a compact deterministic summary is useful.

---

## Team To Stage Mapping

| Team | Scope | Primary references |
|------|-------|--------------------|
| Orchestrator | Single user-facing routing and synthesized handoff state | `../development-pipeline-orchestrator/SKILL.md`, `../development-pipeline-shared-orchestrator/SKILL.md`, `teams.yaml`, `../../../docs/handoffs/README.md` |
| Planning | Research, design, and plan stages with their approval gates | `../development-pipeline-shared-orchestrator/SKILL.md`, `research-lead.md`, `design.md`, `plan.md`, `../../../docs/context/README.md` |
| Engineering | Implement approved phases, run automated gates, and prepare handoff packages | `../development-pipeline-shared-orchestrator/SKILL.md`, `../development-pipeline-shared-worker/SKILL.md`, `implement-lead.md`, `implement-coder.md`, `../../../docs/context/README.md`, `../../../docs/handoffs/README.md` |
| Validation | Review and test the engineering handoff package, then return a verdict | `../development-pipeline-shared-orchestrator/SKILL.md`, `../development-pipeline-shared-reviewer/SKILL.md`, `../development-pipeline-shared-worker/SKILL.md`, `validation-lead.md`, `reviewer-*.md`, `tester.md`, `../../../docs/context/README.md`, `../../../docs/handoffs/README.md` |

---

## Phase Reference

| Internal phase | Owning team | Lead reference | Outputs | Human gate |
|----------------|-------------|----------------|---------|------------|
| Research | Planning | `research-lead` | `docs/research/<feature>.md` plus context-seeding facts for downstream stages | Approve research doc |
| Design | Planning | `design` | `discussion.md`, design artifacts, `structure-outline.md`, and durable design-context inputs | Approve discussion, then design artifacts |
| Plan | Planning | `plan` | `docs/plan/<feature>/`, `docs/context/<feature>/planning-context.md`, and a planning-to-engineering handoff package | Approve plan |
| Implement | Engineering | `implement-lead` | code, tests, automated gate results, `docs/context/<feature>/engineering-context.md`, engineering-to-validation handoff package | Validation reviews output |
| Validate | Validation | `validation-lead` | consolidated review verdict, fix checklist, `docs/context/<feature>/validation-context.md`, validation verdict handoff | Orchestrator decides whether to proceed |

---

## Memory And Session Contract

- Persistent per-agent memory is out of scope for this plugin.
- The current conversation and explicit repo artifacts are the only guaranteed context sources.
- Durable handoffs live in `docs/research/`, `docs/design/`, `docs/plan/`, `docs/context/`, `docs/handoffs/`, generated boundary policies, and the validation outputs described by the workflow.
- Draft, stale, or superseded durable artifacts are not valid downstream inputs unless explicitly allowed by the current handoff and human decision.
- Optional local logs may exist in the surrounding environment, but they are not required or assumed by the packaged workflow.

See `../../../docs/codex-agent-memory-and-sessions.md` for the repository-wide convention.

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
