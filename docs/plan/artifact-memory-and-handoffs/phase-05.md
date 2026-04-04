# Phase 05: Boundary-Aware Artifact Enforcement

## Objective

Extend write-boundary tooling so artifact-memory, compiled context, and handoff outputs are enforceable within explicit role and phase boundaries.

## Dependencies

- Depends on: Phase 01, Phase 02, Phase 03
- Enables: Phase 06

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `tests/test_boundary_artifacts.py` | Test artifact-aware boundary policy generation and verification |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `scripts/generate_boundary_policy.py` | Derive artifact-memory and handoff paths cleanly from future plan phases |
| `scripts/write_boundary_guard.py` | Verify artifact outputs respect role and phase boundaries |
| `tests/test_generate_boundary_policy.py` | Add coverage for plans that include artifact-memory and handoff paths |
| `tests/test_write_boundary_guard.py` | Add coverage for artifact-aware enforcement scenarios |
| `docs/codex-write-boundary-guard.md` | Document boundary enforcement for artifact-memory and handoff outputs |
| `README.md` | Document artifact-aware boundary tooling at a high level |
| `AGENTS.md` | Document any new guard invocation if workflow usage changes |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-05.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Extend boundary-policy generation to include explicit artifact outputs where relevant.
- Allow enforcement to distinguish code writes from durable workflow-artifact writes.
- Keep phase-local ownership intact even when artifacts span planning, engineering, and validation directories.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-06: Policy generation includes artifact-memory and handoff files from future plan phases | Unit | `tests/test_generate_boundary_policy.py` |
| TC-07: Guard verification enforces artifact-aware write boundaries | Unit | `tests/test_write_boundary_guard.py` |
| TC-08: Artifact-specific boundary regressions are covered | Unit | `tests/test_boundary_artifacts.py` |

## Acceptance Criteria for This Phase

- [ ] Boundary policy generation supports artifact-memory and handoff outputs
- [ ] Guard verification can enforce artifact-aware write scope
- [ ] Repo docs explain artifact-aware boundary enforcement
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Keep enforcement rules declarative and derived from phase plans where possible.
- Avoid hardcoding feature-specific artifact paths into the guard.
