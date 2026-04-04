# Phase 01: Orchestrator And Team Topology

## Objective

Add an explicit Codex-native orchestrator layer and align the packaged workflow map to the target team hierarchy without changing implementation behavior yet.

## Dependencies

- Depends on: None
- Enables: Phase 02, Phase 03

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `skills/development-pipeline-orchestrator/SKILL.md` | User-facing orchestrator entrypoint that routes work to planning, engineering, and validation teams |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `skills/development-pipeline/SKILL.md` | Reposition the existing skill as the full pipeline package under an explicit orchestrator model |
| `skills/development-pipeline/references/README.md` | Replace the current phase-only map with an orchestrator-led hierarchy mapped to Codex-native roles |
| `skills/development-pipeline/references/teams.yaml` | Add an orchestrator layer and explicit planning, engineering, and validation team definitions |
| `.codex-plugin/plugin.json` | Include the new orchestrator skill in the packaged plugin if skill registration requires it |
| `.agents/plugins/marketplace.json` | Keep marketplace metadata aligned if plugin skill exposure changes |
| `README.md` | Document the orchestrator entrypoint and updated team model |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-01.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Introduce a top-level workflow contract in which the orchestrator is the single user-facing entrypoint.
- Define explicit mappings for:
  - Planning team
  - Engineering team
  - Validation team
- Preserve the existing research, design, plan, and implement flow as internal execution stages where possible.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-01: Orchestrator skill is present in packaged skill tree | Unit | `tests/test_validate_repo.py` |
| TC-02: Team config exposes orchestrator, planning, engineering, and validation roles | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] A Codex-native orchestrator entrypoint is defined in the skill tree
- [ ] The packaged workflow documentation shows an orchestrator-led hierarchy rather than only phase-local roles
- [ ] `teams.yaml` explicitly represents orchestrator, planning, engineering, and validation layers
- [ ] Plugin packaging and marketplace metadata remain valid after the new entrypoint is added
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Do not solve shared-skill execution or memory persistence in this phase; only establish the topology and routing contract.
- Keep the four-phase pipeline visible inside the orchestrated model rather than replacing it.

