---
description: Show recent CrewAI code-ops run history, errors, and agent health
agent: gentle-orchestrator
subtask: true
---

Show the recent CrewAI code-ops run history with error and health details.

TASK:
1. If `$ARGUMENTS` contains a run_id, run:
   `cd /home/frankil_aldair/code/code_ops && uv run code-ops --status --detail "<run_id>"`
2. Otherwise run:
   `cd /home/frankil_aldair/code/code_ops && uv run code-ops --status`
3. Show the output.
4. For any run with errors > 0, read the log file to get more details:
   `cat /home/frankil_aldair/code/code_ops/output/logs/<run_id>.jsonl`
5. Summarize in plain text: which runs succeeded, which failed, what triggered the failure (cycle, timeout, guardrail, error), and what the agent was doing when it failed.
