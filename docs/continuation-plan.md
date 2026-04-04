# Continuation Plan

## Goal

Carry the current plugin work from "documented and minimally working" to "reviewable, repeatable, and production-ready" without changing the core pipeline direction again.

## Current Baseline

The repository now has:

- repo-local validation and packaging commands
- phase-specific Codex skills for research, design, plan, and implement
- a documented Codex-native write-boundary design
- a working boundary verifier and policy generator
- implementation guidance updated to use generated phase policies

## Next Workstreams

### 1. Script Test Coverage

Add automated tests for:

- `scripts/validate_repo.py`
- `scripts/write_boundary_guard.py`
- `scripts/generate_boundary_policy.py`

Focus on:

- valid and invalid policy schemas
- untracked, modified, staged, renamed, and deleted file handling
- phase-plan parsing failures when required tables or paths are missing
- baseline session behavior with dirty and clean worktrees

### 2. Guard Hardening

Strengthen `write_boundary_guard.py` for commit-gate use:

- verify staged-only mode separately from full working-tree mode
- improve rename and delete reporting
- make baseline state more explicit when switching policies or branches
- fail with clearer output when policy files are stale relative to phase plans

### 3. Policy Generation Refinement

Improve `generate_boundary_policy.py` so it can support real plan directories with less ambiguity:

- optionally read plan overview metadata from `README.md`
- support phases that intentionally touch docs or migration directories
- emit warnings when phase docs use duplicate or suspicious file paths
- add a dry-run mode for review without writing files

### 4. Packaged Workflow Alignment

Keep the packaged references aligned with the repo tooling:

- update `implement-lead.md` examples when guard commands change
- keep `plan.md` requirements in sync with what the generator actually parses
- decide whether example plan artifacts remain in `docs/plan/example-feature/` or move to fixtures

### 5. Release Readiness

Before merging or publishing:

- run `make validate`
- run `make package`
- run boundary generation and verification against at least one realistic plan example
- confirm the plugin archive contains the expected skills, docs, and scripts

## Recommended Execution Order

1. Add script tests.
2. Harden the guard around staged and rename/delete behavior.
3. Refine policy generation based on test findings.
4. Decide final location for example artifacts.
5. Rebuild the package and prepare the PR.

## Definition Of Done

This follow-up work is complete when:

- script behavior is covered by automated tests
- boundary verification is reliable enough to use as the standard phase commit gate
- policy generation works from the documented plan format without manual patching
- packaged guidance and repo behavior stay in sync
