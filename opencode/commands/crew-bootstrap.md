---
description: Bootstrap or update the current project for CrewAI code_ops
agent: gentle-orchestrator
subtask: true
---

Bootstrap or update a project for the CrewAI code-ops flow.

PROJECT:
- If `$ARGUMENTS` starts with a filesystem path, use that path as PROJECT.
- Otherwise run `git rev-parse --show-toplevel 2>/dev/null || pwd` and use the result.
- Recognize optional flag `--no-codegraph`; pass it through unchanged.

TASK:
1. Run:
   `cd /home/frankil_aldair/code/code_ops && uv run code-ops-bootstrap "<PROJECT>" <optional --no-codegraph>`
2. Show the bootstrap JSON result.
3. State that the project is ready for `/crew investigate`, `/crew review`, `/crew test`, `/crew debug`, or `/crew implement`.
4. If the command fails, show the error and the smallest corrective action. Do not edit the target project manually.
