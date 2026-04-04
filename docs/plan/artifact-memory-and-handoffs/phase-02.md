# Phase 02: Artifact Memory Files

## Objective

Add an explicit artifact-memory layer so durable project knowledge can accumulate in repo-managed files instead of hidden expertise state.

## Dependencies

- Depends on: Phase 01
- Enables: Phase 03, Phase 04, Phase 05, Phase 06

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `docs/context/README.md` | Define artifact-memory conventions, ownership, and freshness rules |
| `docs/context/example-feature/planning-context.md` | Example durable planning context artifact |
| `docs/context/example-feature/engineering-context.md` | Example durable engineering context artifact |
| `docs/context/example-feature/validation-context.md` | Example durable validation context artifact |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `docs/codex-agent-memory-and-sessions.md` | Add the artifact-memory layer as the sanctioned durable-context mechanism |
| `docs/orchestrator_agents_teams.md` | Replace generic artifact language with concrete `docs/context/` conventions |
| `skills/development-pipeline/references/README.md` | Describe when to read and update artifact-memory files |
| `skills/development-pipeline/references/research-lead.md` | Clarify which research outputs can seed durable context |
| `skills/development-pipeline/references/design.md` | Clarify how approved design decisions should be summarized into durable context |
| `skills/development-pipeline/references/plan.md` | Clarify what planning context must be durable before implementation starts |
| `skills/development-pipeline/references/implement-lead.md` | Clarify how engineering consumes and updates approved context artifacts |
| `skills/development-pipeline/references/validation-lead.md` | Clarify how validation records durable readiness findings |
| `README.md` | Document explicit context artifacts as part of the workflow |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-02.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Introduce `docs/context/` as the durable context layer for the workflow.
- Define role-specific artifact-memory files with explicit ownership and permitted update moments.
- Keep durable context separate from ephemeral conversation state and optional local logs.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-02: Repo validation tolerates artifact-memory examples and docs | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] Artifact-memory files are defined as explicit repo artifacts rather than implicit agent memory
- [ ] The packaged workflow references `docs/context/` consistently
- [ ] Example context artifacts exist for planning, engineering, and validation
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Keep the first version simple: human-readable Markdown with predictable sections.
- Do not add automatic generation yet; that belongs in later phases.
