# Phase 04: Memory, Session Conventions, And Final Reconciliation

## Objective

Resolve the remaining architecture gaps around persistent memory and session artifacts, then reconcile all packaged docs and workflow references so they describe one coherent Codex-native operating model.

## Dependencies

- Depends on: Phase 02
- Depends on: Phase 03
- Enables: None

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `docs/codex-agent-memory-and-sessions.md` | Codex-native convention for agent memory, session artifacts, and handoff traces |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `skills/development-pipeline/references/README.md` | Replace unsupported session and expertise claims with the final Codex-native conventions |
| `skills/development-pipeline/references/research-lead.md` | Reconcile boot sequence and memory expectations with the final Codex-native approach |
| `skills/development-pipeline/references/design.md` | Reconcile boot sequence and memory expectations with the final Codex-native approach |
| `skills/development-pipeline/references/plan.md` | Reconcile boot sequence and memory expectations with the final Codex-native approach |
| `skills/development-pipeline/references/implement-lead.md` | Reconcile boot sequence and memory expectations with the final Codex-native approach |
| `skills/development-pipeline/references/implement-coder.md` | Reconcile boot sequence and memory expectations with the final Codex-native approach |
| `skills/development-pipeline/references/research-subagent-architecture.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/research-subagent-patterns.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/research-subagent-integrations.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/research-subagent-domain.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/research-subagent-api.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/research-subagent-tests.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/research-subagent-fintech-domain.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/reviewer-quality.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/reviewer-architecture.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/reviewer-security.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/reviewer-plan-compliance.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/reviewer-fintech-compliance.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/reviewer-fintech-patterns.md` | Remove or replace unsupported expertise assumptions if needed |
| `skills/development-pipeline/references/tester.md` | Remove or replace unsupported expertise assumptions if needed |
| `README.md` | Document the final memory and session model |
| `AGENTS.md` | Keep contributor guidance aligned with the final workflow and artifact set |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-04.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Define whether persistent memory is:
  - implemented in Codex-native form, or
  - explicitly out of scope for this plugin
- Define which session artifacts are guaranteed:
  - handoff documents
  - validation outputs
  - optional local logs
- Ensure every role prompt and doc uses the same final contract.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-07: Validation catches stale references to unsupported expertise/session behavior where required | Unit | `tests/test_validate_repo.py` |
| TC-08: Final packaged docs and skill tree remain internally consistent | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] The workflow has a documented Codex-native memory and session convention or an explicit non-support statement
- [ ] Unsupported expertise/session claims are removed or reconciled across shipped references
- [ ] Top-level docs, packaged references, and contributor guidance describe the same workflow
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Prefer simplifying unsupported behavior over inventing complex runtime mechanics that the plugin cannot actually provide.
- Treat documentation consistency as part of the runtime contract, not a cleanup afterthought.
