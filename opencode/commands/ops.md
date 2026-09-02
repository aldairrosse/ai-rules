---
description: Report opencode failures, tool latencies, and log errors (DB + log)
agent: general
subtask: true
---

Run the ops report for opencode itself.

Steps:
1. Run: `python3 /home/frankil_aldair/.config/opencode/ops_report.py --days 7`
   - If the user's argument in `$ARGUMENTS` matches `--all` or `--days N`, pass it through unchanged.
2. If the script fails, show the error and the smallest corrective action.
3. Present the raw report as-is in a single code block.
4. After the report, add at most three bullets: the top actionable failure cluster, the worst latency hotspot, and the one config/agent/skill change that would remove the biggest class of failures (reference the concrete rule, agent, or skill to touch).
