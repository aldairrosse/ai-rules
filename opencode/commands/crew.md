---
description: Run a CrewAI code operation on the current project and show the report in chat
agent: gentle-orchestrator
subtask: true
---

EXECUTE CrewAI agents on this project. Do NOT plan — RUN the command immediately.

CONTEXT:
- Project root: run `git rev-parse --show-toplevel 2>/dev/null || pwd` and use the returned path as PROJECT.
- Flow project: `/home/frankil_aldair/code/code_ops` (do not modify it).

VALIDATION (STOP if any fails):
1. The operation is the first word of `$ARGUMENTS` and must be one of: `investigate`, `review`, `test`, `debug`, `implement`, `verify`. If missing or invalid, show `Usage: /crew <investigate|review|test|debug|implement|verify> "<request>" [flags]` and STOP.
2. The request is the remainder of `$ARGUMENTS` (after the operation word). If empty, ask the user for the request and STOP.

TASK:
1. IMMEDIATELY run the flow (streams live logs):
    `cd /home/frankil_aldair/code/code_ops && uv run code-ops --project "<PROJECT>" --op "<op>" --input "<request>" [--targets ... | --paths ...] [flags]`
   Capture the exit code. If non-zero, print error lines and STOP.
2. Extract the run_id and exact `project_run -> ...` artifact path from stdout.
3. Read the FULL report from that exact project-scoped path. Never read global `output/latest.md`.
4. Print the COMPLETE report in chat. Do NOT summarize — show all findings, verdicts, and the contract.
5. Mention the project-scoped artifact path printed by the flow.

For `investigate`, `review`, `test`, and `debug`, do NOT edit the target project. `implement` edits only an isolated worktree and prints the manual merge command.

RESUME BEHAVIOR (investigate/review/test/debug):
- These ops share per-project memory. If the last run of the same op+scope was interrupted (status `running`/`incomplete`), re-running `code-ops` RESUMES it (same run_id, prior findings injected) instead of starting fresh.
- A new run is only started when the previous one reached a final status (`done`), or when you pass `--force` to relaunch deliberately.
- Add `--force` when the user explicitly wants to redo an investigation from scratch.
