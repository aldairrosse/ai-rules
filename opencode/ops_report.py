#!/usr/bin/env python3
"""opencode ops report: failures + latencies from opencode.db and opencode.log.

Usage:
  python3 ops_report.py            # last 7 days
  python3 ops_report.py --days 30  # last 30 days
  python3 ops_report.py --all      # full history
  python3 ops_report.py --smoke    # self-check, no report
"""
import argparse
import json
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict

HOMEDIR = os.path.expanduser("~")
DB = os.path.join(HOMEDIR, ".local/share/opencode/opencode.db")
LOG = os.path.join(HOMEDIR, ".local/share/opencode/log/opencode.log")
DAY_MS = 86_400_000


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else 0.0


def human(s):
    if s < 60:
        return f"{s:.1f}s"
    m, sec = divmod(int(s), 60)
    if m < 60:
        return f"{m}m{sec}s"
    h, m = divmod(m, 60)
    return f"{h}h{m}m"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=0)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    n_messages = cur.execute("SELECT count(*) FROM message").fetchone()[0]
    if a.smoke:
        assert n_messages > 0, "message table empty?"
        print(f"smoke ok: db readable, {n_messages} messages, log exists={os.path.exists(LOG)}")
        return 0

    cutoff = 0
    if not a.all and a.days > 0:
        now = cur.execute(
            "SELECT COALESCE(MAX(time_created),0) FROM message"
        ).fetchone()[0]
        cutoff = now - a.days * DAY_MS
        window = f"last {a.days}d"
    else:
        window = "full history"

    # ---- tool calls ----
    tools = Counter()
    errs = Counter()
    err_msgs = defaultdict(Counter)
    durs = defaultdict(list)
    if cutoff:
        row = cur.execute(
            "SELECT data, time_created FROM part WHERE data LIKE '%\"type\":\"tool\"%' AND time_created >= ?",
            (cutoff,),
        )
    else:
        row = cur.execute("SELECT data, 0 FROM part WHERE data LIKE '%\"type\":\"tool\"%'")
    total = 0
    for data, _ in row:
        try:
            d = json.loads(data)
        except Exception:
            continue
        st = d.get("state") or {}
        tool = d.get("tool", "?")
        tools[tool] += 1
        total += 1
        if st.get("status") == "error":
            errs[tool] += 1
            err_msgs[tool][str(st.get("error", ""))[:90]] += 1
        t = st.get("time") or {}
        if t.get("start") and t.get("end"):
            durs[tool].append((t["end"] - t["start"]) / 1000)

    print(f"=== opencode ops report ({window}) ===")
    print(f"tool calls: {total}")
    ferr = sum(errs.values())
    print(f"errors: {ferr} ({ferr / total * 100:.1f}%)" if total else "errors: n/a")
    print("\n-- tools: calls  err%   p50    p90    p99")
    for tool, n in tools.most_common(25):
        e = errs.get(tool, 0)
        x = durs.get(tool, [])
        print(
            f"{tool:38s} {n:5d}  {e / n * 100:5.1f}%  {pct(x,.5):7.1f} {pct(x,.9):8.1f} {pct(x,.99):8.1f}"
        )

    # ---- error clusters ----
    clusters = Counter()
    rows = (
        cur.execute(
            "SELECT data FROM part WHERE data LIKE '%\"status\":\"error\"%' AND time_created >= ?",
            (cutoff,),
        )
        if cutoff
        else cur.execute("SELECT data FROM part WHERE data LIKE '%\"status\":\"error\"%'")
    )
    for (data,) in rows:
        try:
            d = json.loads(data)
        except Exception:
            continue
        e = str((d.get("state") or {}).get("error", "")).lower()
        if "prevents you" in e:
            k = "permission rule blocked"
        elif "unknown_project" in e:
            k = "engram: unknown_project"
        elif "language server" in e:
            k = "serena: LSP not initialized"
        elif "not found or not indexed" in e:
            k = "codebase-memory: not indexed"
        elif "exceeded 65536" in e:
            k = "grep: ripgrep record >64KB"
        elif "oldstring" in e:
            k = "edit: oldString mismatch"
        elif "file not found" in e:
            k = "read: file not found"
        elif "cancelled" in e:
            k = "task/subagent cancelled"
        elif "rejected permission" in e:
            k = "user rejected permission"
        else:
            k = "other: " + e[:60]
        clusters[k] += 1
    print("\n-- failure clusters")
    for k, c in clusters.most_common(12):
        print(f"{c:4d}  {k}")

    # ---- turn latency: user msg -> first part of next assistant msg ----
    first_part = {}
    q = (
        "SELECT message_id, min(CAST(json_extract(data,'$.time.start') AS INTEGER), CAST(json_extract(data,'$.state.time.start') AS INTEGER)) FROM part"
        + (f" WHERE time_created >= {int(cutoff)}" if cutoff else "")
        + " GROUP BY message_id"
    )
    for mid, ts in cur.execute(q):
        if ts:
            first_part[mid] = ts
    by_session = defaultdict(list)
    for r in cur.execute(
        "SELECT id, session_id, time_created, data FROM message"
        + (f" WHERE time_created >= {int(cutoff)}" if cutoff else "")
    ):
        try:
            role = json.loads(r["data"]).get("role")
        except Exception:
            role = None
        by_session[r["session_id"]].append((r["time_created"], role, r["id"]))

    turns = []
    for ms in by_session.values():
        ms.sort()
        for i, (tc, role, _mid) in enumerate(ms):
            if role != "user":
                continue
            cands = []
            for _tc2, role2, mid2 in ms[i + 1:]:
                if role2 == "user":
                    break
                c = first_part.get(mid2)
                if c:
                    cands.append(c)
            if not cands:
                continue
            ttft = (min(cands) - tc) / 1000
            if 0 <= ttft <= 3600:
                turns.append(ttft)
    if turns:
        turns.sort()
        print(
            f"\n-- TTFT user->assistant: n={len(turns)} p50={human(pct(turns,.5))} p90={human(pct(turns,.9))} p95={human(pct(turns,.95))} p99={human(pct(turns,.99))}"
        )
        print(f"   slowest: {human(max(turns))}")

    # ---- log errors ----
    if os.path.exists(LOG):
        levels = Counter()
        log_err = Counter()
        log_warn = Counter()
        pat_l = re.compile(rb'level=(\w+) run=\S+ message=(?:"((?:[^"\\]|\\.)*)"|(\S+))')
        with open(LOG, "rb") as f:
            for line in f:
                m = pat_l.search(line)
                if not m:
                    continue
                lvl = m.group(1).decode()
                msg = m.group(2) or m.group(3)
                msg = msg.decode() if isinstance(msg, bytes) else str(msg)
                levels[lvl] += 1
                if lvl == "ERROR":
                    log_err[msg] += 1
                elif lvl == "WARN":
                    log_warn[msg] += 1
        print(f"\n-- log levels: {dict(levels)}")
        if log_err:
            print("-- top log ERRORs")
            for msg, c in log_err.most_common(6):
                print(f"{c:4d}  {msg}")
        if log_warn:
            print("-- top log WARNs")
            for msg, c in log_warn.most_common(6):
                print(f"{c:4d}  {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())