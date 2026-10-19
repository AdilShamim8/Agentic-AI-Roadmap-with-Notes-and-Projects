## What changed and why

<!-- One paragraph. Link the issue this PR addresses. -->

## Evaluation

<!-- If this PR touches an agent, a prompt, or a tool: run the eval
(`python examples/run_evals.py`) and paste the diff vs baseline. -->

## Checklist

- [ ] `ruff check examples/` passes
- [ ] `mypy examples/` passes
- [ ] `pytest -v` passes (LLM tests skip without keys)
- [ ] Every new statistic has a source (see STYLING.md)
- [ ] No link in the diff is dead
