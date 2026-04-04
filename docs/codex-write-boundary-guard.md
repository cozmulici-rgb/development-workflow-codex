# Codex-Native Write Boundary Guard

## Goal

Replace Claude's `domain-lock.sh` hook with a Codex-native mechanism that still enforces per-role write boundaries, but does so using repository-local policy files and verifiable Git state instead of pre-tool interception.

## Why Claude's hook does not map directly

Claude's original guard relied on two assumptions that do not hold here:

- a hook could inspect tool payloads before each `Write` or `Edit` call
- agent runtime configuration could inject read/write domains into every tool invocation automatically

In Codex, the strongest repo-local control surface is not a pre-tool hook. It is:

- the prompt and skill boundary
- explicit repo-local scripts
- Git-visible changed-file verification before review, packaging, or commit

That means the replacement should optimize for deterministic detection and safe recovery, not pretend to block writes before they happen.

## Design Summary

Use a three-layer guard:

1. `policy`: a machine-readable boundary file that defines the allowed write paths for a role or phase
2. `session verification`: a repo-local script that compares current Git changes against the allowed paths
3. `workflow gate`: implementation leads run verification before review and before commit; read-only roles verify that no files changed at all

This is post-write enforcement rather than pre-write interception, but it is strict enough to stop boundary violations from being merged, reviewed as valid work, or staged into commits.

## Core Artifact

Each guarded task gets a boundary policy file. Suggested location:

- `docs/plan/<feature>/boundary.phase-XX.json` for implementation phases
- `docs/design/<feature>/boundary.json` for design
- `docs/research/<feature>.boundary.json` for research

Suggested shape:

```json
{
  "version": 1,
  "role": "implement-coder",
  "phase": "phase-02",
  "feature": "payment-failure-notification",
  "mode": "enforce",
  "allowed_write_globs": [
    "src/**",
    "tests/**",
    "config/**"
  ],
  "blocked_write_globs": [
    "docs/**",
    "skills/**",
    ".codex-plugin/**",
    ".agents/**"
  ],
  "allowed_touched_files": [
    "src/notifications/payment_failure.py",
    "tests/test_payment_failure.py"
  ],
  "allow_new_files": true,
  "require_clean_git_start": true
}
```

## Enforcement Model

### 1. Policy Resolution

The guard resolves two scopes:

- `path scope`: changed files must match `allowed_write_globs`
- `plan scope`: if `allowed_touched_files` is present, the changed files must also be a subset of that explicit file list

This dual check matters because path-only controls are too broad in implementation phases. `src/**` is safe as a general domain, but still too permissive for a single approved phase.

### 2. Session Baseline

The verifier records a baseline at task start:

- current branch
- current `git status --porcelain`
- current `git diff --name-only`

If `require_clean_git_start` is true, the task must start from a clean worktree or from a known allowlisted dirty set explicitly recorded in the session file.

Suggested session path:

- `.codex-boundary/session.json`

This file is local runtime state and should stay untracked.

### 3. Verification Pass

Before any review or commit, the lead runs a verification command that checks:

- all modified, created, renamed, and deleted files
- both staged and unstaged changes
- whether each changed path is within `allowed_write_globs`
- whether any changed path matches `blocked_write_globs`
- whether the changed set exceeds `allowed_touched_files`

For read-only roles such as reviewers and testers, the allowed write set is empty. Any changed file is a violation.

### 4. Commit Gate

The lead must use the verifier before staging and again before commit. The commit flow becomes:

1. verify changed files
2. stage only the verified file list
3. verify staged files
4. commit

This preserves the original pipeline intent from `implement-lead.md`: never use `git add -A`, and never let unrelated files leak into a phase commit.

## Script Interface

The repo now includes `scripts/write_boundary_guard.py` with this interface:

- `python3 scripts/write_boundary_guard.py start --policy <path>`
- `python3 scripts/write_boundary_guard.py verify --policy <path>`
- `python3 scripts/write_boundary_guard.py stage --policy <path> -- <files...>`
- `python3 scripts/write_boundary_guard.py report --policy <path>`

Current behavior:

- `start`: validates the policy file, captures baseline, writes session state
- `verify`: exits nonzero with a violation report if the current diff exceeds policy
- `stage`: stages only verified paths and rejects out-of-scope files
- `report`: prints a human-readable summary for reviewer or lead handoff

## Example Violation Output

```text
Write boundary violation

Policy: docs/plan/payment-failure-notification/boundary.phase-02.json
Role: implement-coder

Changed files outside allowed scope:
- docs/design/payment-failure-notification/sequence.md
  reason: matches blocked_write_globs "docs/**"

Changed files outside approved phase file list:
- src/billing/refunds.py
  reason: not listed in allowed_touched_files

Result: verification failed
```

## Workflow Integration

### Research

- Role is effectively read-only for sub-agents.
- Research lead may optionally allow `docs/research/**` writes only for the lead artifact.
- Guard should fail if a sub-agent edits repository code.

### Design

- Design skill writes only to `docs/design/<feature>/**`.
- The guard blocks edits to `docs/plan/**`, `src/**`, `tests/**`, and plugin metadata.

### Plan

- Plan skill writes only to `docs/plan/<feature>/**`.
- Guard blocks edits to design artifacts once design is approved, unless the human explicitly reopens design.

### Implement

- Implement lead remains read-only.
- Implement coder uses policy derived from the approved phase document.
- Reviewers and tester must verify zero writes.

## Policy Source of Truth

The approved phase plan should remain the human source of truth. The boundary policy should be derived from it, not authored independently.

That can happen in two ways:

1. the plan document contains a canonical "Files to create/modify" section and the guard reads it directly
2. the lead generates `boundary.phase-XX.json` from the plan as a build artifact before delegating work

Option 2 is cleaner for automation and easier to validate. The repo now includes `scripts/generate_boundary_policy.py` and `make boundary-generate PLAN_DIR=...` for this workflow.

## Why this is Codex-native

This design matches Codex's strengths:

- uses repo-local scripts instead of vendor-specific runtime hooks
- relies on Git state, which Codex can inspect consistently
- works for both single-agent and delegated workflows
- fails with explicit file-path reports that can feed directly into reviewer or lead loops

It also degrades safely: even if a worker writes outside scope, the violation is detected before the work can be accepted as a valid phase result.

## Limitations

- It does not stop the first accidental out-of-scope edit at the moment it happens.
- It depends on disciplined workflow gates; if users skip verification, the guard provides no protection.
- It is strongest when paired with explicit per-phase file lists, not just broad path globs.

These are acceptable tradeoffs because the pipeline already assumes human gates and lead-controlled commits.

## Recommended Rollout

### Phase 1

- Document the guard design
- Add `.codex-boundary/` to `.gitignore`
- Teach `implement-lead` docs to require verification before review and commit

### Phase 2

- Implement `scripts/write_boundary_guard.py`
- Add `make boundary-check POLICY=<path>`
- Add validator checks for boundary policy structure

### Phase 3

- Generate phase policy files automatically from approved plan docs
- Integrate guard reports into implementation handoff templates

## Open Decisions

- Whether policy files should be checked into Git or generated locally
- Whether design and plan phases should use explicit file allowlists or only directory-scoped globs
- Whether the verifier should reject any pre-existing unrelated dirty state or allow an explicit baseline exception list

## Recommendation

Adopt the verifier-first design. It preserves the intent of Claude's domain lock, fits Codex's real execution model, and gives the implementation phase a concrete, automatable commit gate without inventing runtime capabilities that do not exist.
