# Phase 03: Artifact Governance And Approval States

## Objective

Add approval-state and freshness rules so downstream phases can trust artifact-memory and handoff files without reintroducing implicit state.

## Dependencies

- Depends on: Phase 01, Phase 02
- Enables: Phase 04, Phase 05, Phase 06

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `docs/context/example-feature/context-status.md` | Example index showing approval state and freshness for durable artifacts |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `docs/codex-agent-memory-and-sessions.md` | Define approval-state and freshness rules for durable artifacts |
| `docs/orchestrator_agents_teams.md` | Clarify that downstream coordination may use only approved artifacts |
| `skills/development-pipeline/references/README.md` | Document approval-state expectations across the workflow |
| `skills/development-pipeline/references/research-lead.md` | Mark research outputs as draft or approved inputs to later phases |
| `skills/development-pipeline/references/design.md` | Require design outputs and summaries to carry approval state |
| `skills/development-pipeline/references/plan.md` | Require approved plan context before engineering starts |
| `skills/development-pipeline/references/implement-lead.md` | Require engineering to reject stale or superseded context inputs |
| `skills/development-pipeline/references/validation-lead.md` | Require validation outputs to record verdict state and freshness |
| `README.md` | Document approval-state behavior at a high level |
| `tests/test_validate_repo.py` | Add checks for stale unsupported runtime wording if validation grows to cover artifact docs |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-03.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Add explicit states such as `draft`, `approved`, and `superseded` to durable workflow artifacts.
- Require downstream phases to consume only approved, non-superseded artifacts unless explicitly overridden.
- Define how freshness and replacement should be recorded when artifacts evolve.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-03: Validation checks approval-state wording for packaged workflow docs | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] Durable artifacts have defined approval and freshness semantics
- [ ] Packaged workflow references consistently describe approved versus draft inputs
- [ ] Example artifact indexes illustrate how freshness is tracked
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Prefer minimal, explicit state markers over complicated workflow engines.
- Keep approval semantics legible in plain Markdown and friendly to future validation tooling.
