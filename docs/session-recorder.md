# Optional Session Recorder

`scripts/record_workflow_session.py` is a maintainer-only diagnostics tool for writing local workflow session logs.

It exists for debugging, transparency, and reproducibility during local maintenance work. It is not part of the packaged workflow contract.

## Contract Boundary

- Recorder output is optional.
- Packaged skills must not require recorder output.
- Recorder logs must not be treated as durable workflow artifacts like `docs/context/` or `docs/handoffs/`.
- Normal workflow execution should behave the same whether the recorder is used or ignored.

## Usage

```bash
python3 scripts/record_workflow_session.py \
  --label artifact-memory-phase-06 \
  --feature artifact-memory-and-handoffs \
  --prompt "Implement optional recorder" \
  --tool-action "Ran repo validation" \
  --output "Validation passed"
```

By default, the script writes JSON logs to a temp-based local diagnostics directory outside the repository.

You can also provide an explicit output directory:

```bash
python3 scripts/record_workflow_session.py \
  --output-dir /tmp/codex-session-recordings \
  --label local-debug
```

The script rejects repo-local output directories unless you pass `--allow-inside-repo`. That override exists only for debugging and tests; it does not make the output contractual.

## Output Shape

Each recording is a JSON file with fields such as:

- `contractual`: always `false`
- `created_at`
- `label`
- `feature`
- `notes`
- `prompts`
- `tool_actions`
- `outputs`

## Limitations

- The recorder does not integrate with packaged skills automatically.
- It does not replace handoff, context, plan, or validation artifacts.
- It should not be used as a required input to any phase gate.
