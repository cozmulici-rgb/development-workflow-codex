# Phase 01: Handoff Package Contract

## Objective

Define a portable, explicit handoff-package format that replaces any need for implicit shared session state between planning, engineering, and validation.

## Dependencies

- Depends on: None
- Enables: Phase 02, Phase 03, Phase 04, Phase 05, Phase 06

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `docs/handoffs/README.md` | Define the canonical handoff-package layout and artifact expectations |
| `docs/handoffs/example-feature/planning-to-engineering.md` | Example planning-to-engineering handoff package |
| `docs/handoffs/example-feature/engineering-to-validation.md` | Example engineering-to-validation handoff package |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `docs/codex-agent-memory-and-sessions.md` | Add the handoff-package contract as an explicit durable artifact mechanism |
| `docs/orchestrator_agents_teams.md` | Update session and coordination sections to reference handoff packages |
| `skills/development-pipeline/references/README.md` | Document handoff packages as the required cross-team coordination unit |
| `skills/development-pipeline/references/research-lead.md` | Clarify what research must emit for downstream handoff |
| `skills/development-pipeline/references/design.md` | Clarify what design artifacts and summary fields feed the handoff package |
| `skills/development-pipeline/references/plan.md` | Require an implementation-ready handoff package at plan completion |
| `skills/development-pipeline/references/implement-lead.md` | Define the engineering handoff package to validation |
| `skills/development-pipeline/references/validation-lead.md` | Consume the engineering handoff package and return a validation verdict package |
| `README.md` | Document explicit handoff packages as part of the workflow model |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-01.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Introduce `docs/handoffs/` as a first-class workflow artifact location.
- Define minimum required handoff fields such as source phase, approved inputs, changed scope, open questions, gate status, and next required action.
- Require packaged workflow references to produce or consume handoff packages instead of relying on implicit shared state.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-01: Repo validation tolerates handoff examples and docs | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] A durable handoff-package contract is documented in repo docs
- [ ] The packaged workflow references explicit handoff packages for cross-team coordination
- [ ] Example handoff artifacts exist and match the documented contract
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Keep the examples small and illustrative; they are contract references, not generated runtime outputs.
- Do not add optional session recorder behavior in this phase.
