# Phase 02: Validation Team Separation

## Objective

Split validation responsibilities out of the implementation lead so the workflow matches the target architecture where engineering and validation are separate team concerns.

## Dependencies

- Depends on: Phase 01
- Enables: Phase 04

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `skills/development-pipeline-validation/SKILL.md` | Team-level validation entrypoint for review and test coordination |
| `skills/development-pipeline/references/validation-lead.md` | Validation lead role prompt that coordinates reviewers and tester |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `skills/development-pipeline-implement/SKILL.md` | Narrow the engineering-side scope so it hands off to validation instead of directly owning all review orchestration |
| `skills/development-pipeline/references/implement-lead.md` | Remove direct ownership of reviewer/tester orchestration and define handoff to validation lead |
| `skills/development-pipeline/references/README.md` | Show validation as its own team instead of a sub-loop inside implementation |
| `skills/development-pipeline/references/teams.yaml` | Add validation-lead membership and bind reviewers/tester under that team |
| `README.md` | Update workflow documentation for the engineering-to-validation handoff |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-02.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Introduce a formal contract between engineering completion and validation review.
- Define validation lead inputs:
  - phase plan
  - changed file list or diff
  - relevant design and research context
  - automated gate results
- Define validation lead outputs:
  - consolidated review verdict
  - fix checklist
  - pass/fail handoff to orchestrator

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-03: Team config binds reviewer and tester roles under validation | Unit | `tests/test_validate_repo.py` |
| TC-04: Validation lead references are included in packaged workflow documentation | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] Validation has a dedicated team entrypoint and lead reference
- [ ] `implement-lead` no longer claims sole ownership of both engineering and validation coordination
- [ ] Reviewers and tester are described as validation-team members in the shipped workflow docs
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Keep automated gate execution explicit; only the ownership and reporting path should change here.
- Do not expand reviewer scope beyond what is already defined.

