# Codex Agent Memory And Sessions

Persistent per-agent memory is out of scope for this repository.

## Memory Contract

- No packaged skill in this repo automatically loads or updates a persistent expertise file.
- References copied from Claude workflows may describe expertise files as source context only, not active runtime behavior.
- Agents should rely on the current conversation, approved plan artifacts, and the repository state available in the current session.

## Session Artifact Contract

The workflow guarantees only artifacts that are explicitly written into the repo or produced by the current command flow:

- planning artifacts under `docs/research/`, `docs/design/`, and `docs/plan/`
- boundary policy files under `docs/plan/<feature>/boundary.phase-XX.json`
- implementation handoff packages described in the workflow references
- validation outputs and checklists returned in the active session

Optional local logs may exist from the surrounding Codex environment or local tooling, but they are not part of the plugin contract and must not be relied on by the packaged workflow.

## Authoring Rule

When editing packaged workflow prompts:

- do not instruct agents to read or update persistent expertise files
- do not assume a shared conversation log path exists
- do describe the exact plan, research, design, validation, and boundary artifacts the current phase can rely on

## Practical Guidance

- Treat the current conversation as the only guaranteed transient context.
- Treat repo files created by prior phases as the durable handoff mechanism.
- If a workflow needs additional state, write it into an explicit repo artifact instead of describing an implicit runtime memory system.
