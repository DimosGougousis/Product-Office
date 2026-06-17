#!/usr/bin/env python3
"""
YUUP Observability Dashboard — reads run traces and produces a summary report.

Usage:
  python scripts/yuup-dashboard.py                  # All runs summary
  python scripts/yuup-dashboard.py <run-id>         # Single run detail
  python scripts/yuup-dashboard.py --json           # Machine-readable JSON output
  python scripts/yuup-dashboard.py --since 7d       # Last 7 days only

Produces: markdown table to stdout (default) or JSON with --json.
Reads governance/runs/*.jsonl. Deterministic — no judgment, just aggregation.
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACES_DIR = REPO_ROOT / "governance" / "runs"


def load_all_traces(since: datetime | None = None) -> dict[str, list[dict]]:
    """Load all run traces, optionally filtered by date. Returns {run_id: [events]}."""
    runs = {}
    if not TRACES_DIR.exists():
        return runs

    for trace_file in sorted(TRACES_DIR.glob("*.jsonl")):
        run_id = trace_file.stem
        events = []
        with open(trace_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    evt = json.loads(line)
                    if since:
                        ts = evt.get("timestamp", "")
                        try:
                            evt_time = datetime.fromisoformat(ts)
                            if evt_time < since:
                                continue
                        except (ValueError, TypeError):
                            pass
                    events.append(evt)
                except json.JSONDecodeError:
                    continue
        if events:
            runs[run_id] = events
    return runs


def compute_run_stats(run_id: str, events: list[dict]) -> dict:
    """Compute aggregate stats for one run."""
    dispatches = [e for e in events if e.get("type") == "dispatch"]
    results = [e for e in events if e.get("type") == "result"]
    gates = [e for e in events if e.get("type") == "gate"]
    breaches = [e for e in events if e.get("type") == "budget_breach"]

    total_tokens = sum(r.get("tokens", 0) for r in results)
    total_latency = sum(r.get("latency_ms", 0) for r in results)

    verdicts = [r.get("verdict") for r in results]
    pass_count = verdicts.count("PASS")
    revise_count = verdicts.count("REVISE")
    reject_count = verdicts.count("REJECT")

    scores = [r.get("score") for r in results if r.get("score") is not None]
    avg_score = sum(scores) / len(scores) if scores else None

    agents_used = list(set(d.get("agent") for d in dispatches))

    # Determine final verdict
    final_verdict = "INCOMPLETE"
    if breaches:
        final_verdict = "BREACHED"
    elif results:
        if reject_count > 0:
            final_verdict = "REJECTED"
        elif revise_count > 0:
            final_verdict = "REVISED"
        elif pass_count == len(results):
            final_verdict = "PASSED"
        else:
            final_verdict = "MIXED"

    # Timeline
    timestamps = []
    for e in events:
        ts = e.get("timestamp", "")
        if ts:
            try:
                timestamps.append(datetime.fromisoformat(ts))
            except (ValueError, TypeError):
                pass
    start_time = min(timestamps).isoformat() if timestamps else "unknown"
    end_time = max(timestamps).isoformat() if timestamps else "unknown"

    return {
        "run_id": run_id,
        "dispatches": len(dispatches),
        "results": len(results),
        "gates": len(gates),
        "breaches": len(breaches),
        "total_tokens": total_tokens,
        "total_latency_ms": total_latency,
        "agents_used": agents_used,
        "pass_count": pass_count,
        "revise_count": revise_count,
        "reject_count": reject_count,
        "avg_score": round(avg_score, 1) if avg_score else None,
        "final_verdict": final_verdict,
        "start_time": start_time,
        "end_time": end_time,
    }


def format_markdown_table(stats_list: list[dict]) -> str:
    """Format stats as a markdown table."""
    lines = [
        "# YUUP Run Dashboard",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Total runs: {len(stats_list)}",
        "",
        "| Run ID | Dispatches | Verdict | Score | Tokens | Latency | Agents |",
        "|--------|-----------|---------|-------|--------|---------|--------|",
    ]

    total_dispatches = 0
    total_tokens = 0
    total_latency = 0
    pass_count = 0

    for s in stats_list:
        score_str = str(s["avg_score"]) if s["avg_score"] is not None else "—"
        agents_str = ", ".join(s["agents_used"]) if s["agents_used"] else "—"
        latency_sec = s["total_latency_ms"] / 1000 if s["total_latency_ms"] else 0
        lines.append(
            f"| {s['run_id']} | {s['dispatches']} | {s['final_verdict']} | "
            f"{score_str} | {s['total_tokens']:,} | {latency_sec:.1f}s | {agents_str} |"
        )
        total_dispatches += s["dispatches"]
        total_tokens += s["total_tokens"]
        total_latency += s["total_latency_ms"]
        if s["final_verdict"] == "PASSED":
            pass_count += 1

    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total dispatches**: {total_dispatches}")
    lines.append(f"- **Total tokens**: {total_tokens:,}")
    lines.append(f"- **Total latency**: {total_latency/1000:.1f}s")
    lines.append(f"- **Pass rate**: {pass_count}/{len(stats_list)} ({pass_count/len(stats_list)*100:.0f}%)" if stats_list else "- **Pass rate**: N/A (no runs)")

    # Agent utilization
    agent_counts = defaultdict(int)
    for s in stats_list:
        for agent in s["agents_used"]:
            agent_counts[agent] += 1
    if agent_counts:
        lines.append("")
        lines.append("## Agent Utilization")
        lines.append("")
        for agent, count in sorted(agent_counts.items(), key=lambda x: -x[1]):
            lines.append(f"- **{agent}**: {count} runs")

    return "\n".join(lines)


def main() -> int:
    since = None
    run_id_filter = None
    output_json = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--json":
            output_json = True
        elif arg == "--since":
            i += 1
            if i >= len(args):
                print("ERROR: --since requires a value (e.g., 7d, 24h)", file=sys.stderr)
                return 2
            val = args[i]
            if val.endswith("d"):
                since = datetime.now(timezone.utc) - timedelta(days=int(val[:-1]))
            elif val.endswith("h"):
                since = datetime.now(timezone.utc) - timedelta(hours=int(val[:-1]))
            else:
                print(f"ERROR: Unknown --since format: {val} (use 7d or 24h)", file=sys.stderr)
                return 2
        elif not arg.startswith("-"):
            run_id_filter = arg
        else:
            print(f"ERROR: Unknown argument: {arg}", file=sys.stderr)
            return 2
        i += 1

    runs = load_all_traces(since)

    if run_id_filter:
        if run_id_filter not in runs:
            print(f"No trace found for run: {run_id_filter}", file=sys.stderr)
            return 1
        runs = {run_id_filter: runs[run_id_filter]}

    if not runs:
        if output_json:
            print(json.dumps({"runs": []}, indent=2))
        else:
            print("# YUUP Run Dashboard\n\nNo runs found.")
        return 0

    stats_list = [compute_run_stats(rid, evts) for rid, evts in runs.items()]
    # Sort by start time descending
    stats_list.sort(key=lambda s: s["start_time"], reverse=True)

    if output_json:
        print(json.dumps({"runs": stats_list}, indent=2, default=str))
    else:
        print(format_markdown_table(stats_list))

    return 0


if __name__ == "__main__":
    sys.exit(main())
