# Phase 01: Example Foundation Slice

## Objective

Create the core service and its initial tests as a small end-to-end implementation slice.

## Dependencies

- Depends on: None
- Enables: Phase 02

## Exact File Changes

### Files to Create
| File Path | Purpose |
|-----------|---------|
| `src/example/service.py` | Core example service |
| `tests/test_example_service.py` | Initial service tests |

### Files to Modify
| File Path | What Changes |
|-----------|-------------|
| `config/example.json` | Register example service |

### Files to Delete
| File Path | Reason |
|-----------|--------|
| `src/example/old_service.py` | Replaced by service.py |

## Interface & Contract Changes

None.

## Tests to Add / Modify

| Test Case | Type | File to Create/Modify |
|-----------|------|----------------------|
| TC-01: Example service happy path | Unit | `tests/test_example_service.py` |

## Acceptance Criteria for This Phase

- [ ] Example service can be imported
- [ ] Relevant tests pass: `pytest tests/test_example_service.py`
