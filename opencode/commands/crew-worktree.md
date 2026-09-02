---
description: List, inspect, validate, continue, or safely discard code_ops worktrees
agent: crew-launcher
subtask: true
---

Manage code_ops worktree lifecycle without deleting reports, logs, artifacts, or memory.

Resolve PROJECT from the current git root unless the user provides a path.

Actions:
- `list`: run `cd /home/frankil_aldair/code/code_ops && uv run code-ops-worktree list --project "<PROJECT>"`.
- `inspect <WORKTREE>`: run `... code-ops-worktree inspect --project "<PROJECT>" --path "<WORKTREE>"`.
- `validate <WORKTREE> "<commands>"`: run `uv run code-ops --project "<WORKTREE>" --op verify --commands "<commands>" --mcp off --input "Validate only this worktree"`.
- `continue <WORKTREE> "<request>"`: run `uv run code-ops --project "<PROJECT>" --op implement --worktree "<WORKTREE>" --input "<request>"`.
- `discard <WORKTREE>`: first inspect it, then require explicit user intent to discard. Run `... code-ops-worktree discard --project "<PROJECT>" --path "<WORKTREE>" --delete-branch` only after confirmation.

Safety:
- Only `codeops-*` and `merge-*` sibling worktrees are eligible.
- Never delete artifacts, output, logs, or memory when discarding a worktree.
- Never discard a dirty worktree without explicit user confirmation.
