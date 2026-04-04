# Phase 03: Codex-Native Shared Behavior

## Objective

Replace reference-only architecture elements with Codex-native assets so shared behavior, routing, and role conventions are part of the executable workflow rather than just described in `teams.yaml`.

## Dependencies

- Depends on: Phase 01
- Enables: Phase 04

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `skills/development-pipeline-shared-orchestrator/SKILL.md` | Codex-native shared behavior for orchestrator and lead coordination rules |
| `skills/development-pipeline-shared-worker/SKILL.md` | Codex-native shared behavior for worker-style execution and reporting |
| `skills/development-pipeline-shared-reviewer/SKILL.md` | Codex-native shared behavior for actionable review output |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `skills/development-pipeline/references/README.md` | Replace reference-only claims about shared skills with actual packaged Codex assets |
| `skills/development-pipeline/references/teams.yaml` | Point role definitions at Codex-native shared behavior conventions rather than only descriptive labels |
| `skills/development-pipeline/references/research-lead.md` | Align lead behavior with shared orchestrator conventions |
| `skills/development-pipeline/references/design.md` | Align design lead behavior with the shared lead contract where applicable |
| `skills/development-pipeline/references/plan.md` | Align planning behavior with the shared orchestrator and worker contracts where applicable |
| `skills/development-pipeline/references/implement-lead.md` | Align engineering lead behavior with the shared orchestrator contract |
| `skills/development-pipeline/references/implement-coder.md` | Align coder behavior with the shared worker contract |
| `skills/development-pipeline/references/reviewer-quality.md` | Align reviewer output with the shared reviewer contract |
| `skills/development-pipeline/references/reviewer-architecture.md` | Align reviewer output with the shared reviewer contract |
| `skills/development-pipeline/references/reviewer-security.md` | Align reviewer output with the shared reviewer contract |
| `skills/development-pipeline/references/reviewer-plan-compliance.md` | Align reviewer output with the shared reviewer contract |
| `skills/development-pipeline/references/reviewer-fintech-compliance.md` | Align reviewer output with the shared reviewer contract |
| `skills/development-pipeline/references/reviewer-fintech-patterns.md` | Align reviewer output with the shared reviewer contract |
| `skills/development-pipeline/references/tester.md` | Align tester reporting with the worker contract while preserving read-only constraints |
| `README.md` | Document which shared Codex-native assets are authoritative |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-03.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Establish Codex-native shared behavior contracts for:
  - orchestrator and lead delegation
  - worker execution and reporting
  - reviewer issue reporting
- Reduce reliance on purely descriptive `teams.yaml` skill labels that have no packaged Codex equivalent.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-05: Shared Codex-native workflow assets exist and validate | Unit | `tests/test_validate_repo.py` |
| TC-06: Repo validation enforces any new shared-skill packaging expectations | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] Shared workflow behavior described by the docs has corresponding packaged Codex-native assets
- [ ] Role references consistently follow those shared behavior contracts
- [ ] The repo no longer depends on reference-only skill labels to explain core runtime behavior
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Keep the scope limited to shared behavior that materially affects workflow execution and review outputs.
- Do not introduce a large generic skill taxonomy beyond what the workflow actually uses.

