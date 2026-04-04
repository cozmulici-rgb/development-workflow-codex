---
name: development-pipeline-shared-reviewer
description: Shared Codex-native contract for reviewers that produce actionable findings with file context, severity, required fixes, and explicit pass/fail verdicts.
---

# Development Pipeline Shared Reviewer

## Use this skill when
Use this shared asset for reviewers that assess implementation output without modifying code.

## Shared contract
1. Review only the assigned change scope and supporting design or plan references.
2. Report findings with file/path context, concrete problem statements, and required changes.
3. Distinguish blocking issues from non-blocking concerns.
4. End with an explicit verdict the orchestrator can act on immediately.

## Required behaviors
- Do not give vague advice such as "improve this" or "clean this up".
- Do not suggest out-of-scope refactors unless the finding is a plan or design blocker.
- If no issues are found, say so explicitly.
- Keep every finding actionable enough for a worker to implement without guesswork.
