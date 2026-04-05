# Phase 06: Optional Session Recorder

## Objective

Add optional maintainer-only session recording for debugging and transparency without turning local logs into part of the packaged workflow contract.

## Dependencies

- Depends on: Phase 01, Phase 02, Phase 03
- Enables: None

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `scripts/record_workflow_session.py` | Optional local session recorder for maintainers |
| `tests/test_record_workflow_session.py` | Test optional session recorder behavior and non-contractual mode |
| `docs/session-recorder.md` | Document optional local session-recording behavior and limitations |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `README.md` | Document the session recorder as optional maintainer tooling only |
| `AGENTS.md` | Document the recorder command if it becomes repo-supported tooling |
| `docs/codex-agent-memory-and-sessions.md` | Clarify that optional session logs remain outside the packaged contract |
| `docs/orchestrator_agents_teams.md` | Reference optional local recording as debugging aid rather than runtime requirement |
| `docs/codex-write-boundary-guard.md` | Document any interaction between boundary tooling and optional session outputs |

### Files to Delete
| File Path | Reason |
|-----------|--------|

## Boundary Policy Output

This phase document must be specific enough for `scripts/generate_boundary_policy.py` to derive `boundary.phase-06.json` automatically.
That means:
- every file path that may be touched in this phase appears in `Files to Create`, `Files to Modify`, `Files to Delete`, or `Tests to Add / Modify`
- no implementation-critical file is implied without being listed explicitly

## Interface & Contract Changes

- Add an optional local recorder that can capture prompts, tool actions, and outputs for debugging.
- Keep recorder output explicitly out of the packaged workflow contract and out of required skill behavior.
- Make the recorder safe to ignore in normal workflow execution.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-09: Session recorder can write optional local logs without becoming a required artifact | Unit | `tests/test_record_workflow_session.py` |
| TC-10: Repo validation remains green with optional recorder docs | Unit | `tests/test_validate_repo.py` |

## Acceptance Criteria for This Phase

- [ ] Optional session recording exists as maintainer tooling
- [ ] Packaged workflow docs clearly state that recorded logs are non-contractual
- [ ] Recorder behavior is covered by tests
- [ ] Relevant tests pass: `python3 -m unittest discover -s tests -t .`
- [ ] Linter passes: `python3 scripts/validate_repo.py`

## Implementation Notes

- Prefer writing optional logs outside shipped workflow directories unless the repo later formalizes a local diagnostics area.
- Do not require any packaged skill to read, write, or depend on recorder output.
