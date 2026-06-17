#!/usr/bin/env python3
"""
Append a JSON line to a YUUP run trace.

Usage:
  python scripts/yuup-trace-append.py <run-id> <event-type> [--key=value ...]

Event types: dispatch, result, gate, budget_breach, summary

Examples:
  python scripts/yuup-trace-append.py yuup-2026-06-16-test dispatch --task=research --agent=research --objective_hash=abc123
  python scripts/yuup-trace-append.py yuup-2026-06-16-test result --task=research --agent=research --verdict=PASS --score=85 --tokens=1200 --latency_ms=5400
  python scripts/yuup-trace-append.py yuup-2026-06-16-test gate --gate=cost --action=api_call --approved=true
  python scripts/yuup-trace-append.py yuup-2026-06-16-test budget_breach --cap=max_dispatches --current=13

Deterministic: always appends exactly one valid JSON line. Exit code 0 on success.
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACES_DIR = REPO_ROOT / "governance" / "runs"

EVENT_SCHEMAS = {
    "dispatch": {"type", "run_id", "task", "agent", "objective_hash", "timestamp"},
    "result": {"type", "run_id", "task", "agent", "verdict", "score", "tokens", "latency_ms", "timestamp"},
    "gate": {"type", "run_id", "gate", "action", "approved", "timestamp"},
    "budget_breach": {"type", "run_id", "cap", "current", "timestamp"},
    "summary": {"type", "run_id", "total_dispatches", "total_tokens", "wall_clock_ms", "final_verdict", "timestamp"},
}


def parse_kv(args: list[str]) -> dict:
    """Parse --key=value pairs into a dict. Values are auto-typed."""
    result = {}
    for arg in args:
        if arg.startswith("--"):
            kv = arg[2:]
            if "=" not in kv:
                result[kv] = True
                continue
            key, _, value = kv.partition("=")
            result[key] = _coerce_value(value)
    return result


def _coerce_value(value: str):
    """Auto-coerce strings to int, float, or bool."""
    if value in ("true", "True"):
        return True
    if value in ("false", "False"):
        return False
    for caster in (int, float):
        try:
            return caster(value)
        except (ValueError, TypeError):
            continue
    return value


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python scripts/yuup-trace-append.py <run-id> <event-type> [--key=value ...]", file=sys.stderr)
        return 2

    run_id = sys.argv[1]
    event_type = sys.argv[2]

    if event_type not in EVENT_SCHEMAS:
        print(f"Unknown event type: {event_type}. Valid: {', '.join(EVENT_SCHEMAS)}", file=sys.stderr)
        return 2

    kv = parse_kv(sys.argv[3:])

    # Build the event record
    record: dict = {
        "type": event_type,
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    record.update(kv)

    # Validate required keys present
    schema = EVENT_SCHEMAS[event_type]
    missing = schema - set(record.keys())
    if missing:
        print(f"Missing required keys for '{event_type}': {sorted(missing)}", file=sys.stderr)
        print(f"Schema requires: {sorted(schema)}", file=sys.stderr)
        return 2

    # Write
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    trace_file = TRACES_DIR / f"{run_id}.jsonl"
    with open(trace_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")

    print(f"Appended {event_type} event to {trace_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
