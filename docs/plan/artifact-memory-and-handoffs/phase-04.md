# Phase 04: Role-Specific Context Compilers

## Objective

Add deterministic context-compilation tooling that derives role-specific briefs from approved artifacts instead of relying on long-lived mental models.

## Dependencies

- Depends on: Phase 01, Phase 02, Phase 03
- Enables: Phase 05

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `scripts/compile_workflow_context.py` | Generate role-specific context briefs from approved workflow artifacts |
| `tests/test_compile_workflow_context.py` | Test context compilation behavior and output selection |
| `docs/context/example-feature/compiled-planning-context.md` | Example compiled planning brief |
| `docs/context/example-feature/compiled-engineering-context.md` | Example compiled engineering brief |
| `docs/context/example-feature/compiled-validation-context.md` | Example compiled validation brief |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `AGENTS.md` | Document the new script entrypoint if it becomes part of repo tooling |
| `README.md` | Document context compilation as optional deterministic tooling |
| `docs/codex-agent-memory-and-sessions.md` | Reference compiled briefs as derived artifacts, not hidden memory |
| `docs/orchestrator_agents_teams.md` | Describe compiled briefs as the replacement for role-specific mental models |
| `skills/development-pipeline/references/README.md` | Clarify when packaged workflow references should read compiled briefs |
| `skills/development-pipeline/references/research-lead.md` | Clarify what source artifacts feed the planning compiler |
| `skills/development-pipeline/references/implement-lead.md` | Clarify what source artifacts feed the engineering compiler |
| `skills/development-pipeline/references/validation-lead.md` | Clarify what source artifacts feed the validation compiler |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-04.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Add a deterministic script for producing role-specific workflow briefs.
- Define compiled briefs as derived artifacts based only on approved handoffs and context files.
- Keep compiled briefs optional unless the packaged workflow is explicitly updated to require them.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-04: Context compiler emits the correct role-specific artifact set | Unit | `tests/test_compile_workflow_context.py` |
| TC-05: Repo validation remains green after adding context compiler docs | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] A deterministic context-compiler script exists
- [ ] The compiler uses approved artifacts as inputs
- [ ] Example compiled briefs exist for each workflow role
- [ ] Repo docs explain compiled briefs as derived context, not implicit memory
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Use standard-library Python only unless the repo formally adopts new tooling.
- Keep output stable and diff-friendly so compiled briefs can be reviewed.
