"""
YUUP Eval Runner

Run regressions: python quality/evals/yuup/run_eval.py --objective <id>
Uses the golden set from golden-set.md. Scores against rubric.md.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EVAL_DIR = Path(__file__).resolve().parent
TRACES_DIR = REPO_ROOT / "governance" / "runs"
RESULTS_DIR = EVAL_DIR / "results"
GOLDEN_FILE = EVAL_DIR / "golden-set.md"


def parse_golden_set(path: Path) -> list[dict]:
    """Parse golden-set.md into structured eval cases with scoring rules."""
    text = path.read_text(encoding="utf-8")
    cases = []

    # Split by eval case headings (### eval-NNN: ...)
    sections = re.split(r"(?=^### eval-\d+:)", text, flags=re.MULTILINE)
    for section in sections:
        heading_match = re.match(r"^### (eval-\d+): (.+)$", section, re.MULTILINE)
        if not heading_match:
            continue

        case_id = heading_match.group(1)
        case_title = heading_match.group(2).strip()

        case = {
            "id": case_id,
            "title": case_title,
            "expected_routing": [],
            "expected_verdict": None,
            "expected_behavior": None,
            "expected_agent": None,
            "expected_constraint": None,
            "expected_critique_behavior": None,
        }

        # Extract structured fields
        routing_match = re.search(r"\*\*Expected routing\*\*:\s*([^\n]+)", section)
        if routing_match:
            agents_raw = routing_match.group(1).strip()
            # Extract backtick-wrapped agent names only: `robot`, `research`, etc.
            agents = re.findall(r'`([^`]+)`', agents_raw)
            case["expected_routing"] = agents

        verdict_match = re.search(r"\*\*Golden verdict[s]?\*\*:\s*([^\n]+)", section, re.IGNORECASE)
        if verdict_match:
            verdict_text = verdict_match.group(1).strip()
            upper = verdict_text.upper()
            if "PASS" in upper and "NOT" not in upper:
                case["expected_verdict"] = "PASS"
            elif "REJECT" in upper:
                case["expected_verdict"] = "REJECT"
            elif "BUDGET" in upper or "STOP" in upper:
                case["expected_verdict"] = "STOP"
            elif "NO FILE" in upper or "READ-ONLY" in upper:
                case["expected_verdict"] = "NO_WRITE"

        behavior_match = re.search(r"\*\*Expected behavior\*\*:\s*([^\n]+)", section)
        if behavior_match:
            case["expected_behavior"] = behavior_match.group(1).strip()

        agent_match = re.search(r"\*\*Expected routing\*\*:\s*`(\w+)`", section)
        if agent_match:
            case["expected_agent"] = agent_match.group(1)

        cases.append(case)

    return cases


def score_run(run_id: str, golden: list[dict]) -> dict:
    """Score a run trace against golden expectations."""
    trace_path = TRACES_DIR / f"{run_id}.jsonl"
    if not trace_path.exists():
        return {"run_id": run_id, "error": f"No trace found at {trace_path}"}

    with open(trace_path, encoding="utf-8") as f:
        events = [json.loads(line) for line in f if line.strip()]

    dispatches = [e for e in events if e.get("type") == "dispatch"]
    results = [e for e in events if e.get("type") == "result"]
    breaches = [e for e in events if e.get("type") == "budget_breach"]

    agents_seen = list(set(d.get("agent") for d in dispatches))
    verdicts = [r.get("verdict") for r in results]

    cases = []
    for gc in golden:
        case_result = {
            "case": gc["id"],
            "title": gc.get("title", ""),
            "passed": False,
            "details": [],
        }

        gid = gc["id"]

        # eval-001: Multi-agent sequential routing + PASS verdict
        if gid == "eval-001":
            expected = gc.get("expected_routing", [])
            routing_ok = all(a in agents_seen for a in expected) if expected else True
            case_result["details"].append(
                f"Routing: expected={expected}, seen={agents_seen} -> {'PASS' if routing_ok else 'FAIL'}"
            )
            if not routing_ok:
                case_result["passed"] = False
            else:
                all_pass = all(v == "PASS" for v in verdicts)
                case_result["details"].append(
                    f"Verdicts: {verdicts} -> {'PASS' if all_pass else 'FAIL'}"
                )
                case_result["passed"] = all_pass

        # eval-002: Budget breach detected
        elif gid == "eval-002":
            has_breach = len(breaches) > 0
            zero_dispatches = len(dispatches) == 0
            stopped_early = has_breach or zero_dispatches
            case_result["details"].append(
                f"Budget: breaches={len(breaches)}, dispatches={len(dispatches)} -> {'PASS' if stopped_early else 'FAIL'}"
            )
            case_result["passed"] = stopped_early

        # eval-003: Critique REJECT + stop
        elif gid == "eval-003":
            has_reject = "REJECT" in verdicts
            case_result["details"].append(
                f"Reject verdict: {verdicts} -> {'PASS' if has_reject else 'FAIL'}"
            )
            case_result["passed"] = has_reject

        # eval-004: Read-only agent, no writes
        elif gid == "eval-004":
            expected_agent = gc.get("expected_agent", "research")
            agent_used = expected_agent in agents_seen
            agent_wrote = False
            for r in results:
                if r.get("agent") == expected_agent:
                    files = r.get("files_touched", [])
                    # files_touched might be a string representation from CLI
                    if isinstance(files, str):
                        try:
                            files = json.loads(files)
                        except (json.JSONDecodeError, TypeError):
                            files = [files] if files else []
                    if files and len(files) > 0:
                        agent_wrote = True
                        case_result["details"].append(
                            f"{expected_agent} touched files: {files}"
                        )
            no_write = not agent_wrote
            case_result["details"].append(
                f"Agent: seen={agents_seen}, writes={agent_wrote} -> {'PASS' if no_write else 'FAIL'}"
            )
            case_result["passed"] = agent_used and no_write

        # eval-005: Critique dispatched and uses ACs
        elif gid == "eval-005":
            critique_dispatched = "critique" in agents_seen
            critique_pass = any(
                r.get("agent") == "critique" and r.get("verdict") == "PASS"
                for r in results
            )
            case_result["details"].append(
                f"Critique: dispatched={critique_dispatched}, pass={critique_pass} -> "
                f"{'PASS' if critique_pass else 'FAIL'}"
            )
            case_result["passed"] = critique_dispatched and critique_pass

        else:
            case_result["details"].append("No scoring rule defined")
            case_result["passed"] = False

        cases.append(case_result)

    overall_pass = all(c["passed"] for c in cases)
    return {
        "run_id": run_id,
        "cases": cases,
        "overall": "PASS" if overall_pass else "FAIL",
        "passed_count": sum(1 for c in cases if c["passed"]),
        "total_count": len(cases),
    }


def generate_trend_report() -> str:
    """Generate a historical trend report from past eval results."""
    if not RESULTS_DIR.exists():
        return "No historical eval results found."

    results_files = sorted(RESULTS_DIR.glob("eval-*.json"), reverse=True)
    if not results_files:
        return "No historical eval results found."

    lines = ["# YUUP Eval Trend Report\n"]
    lines.append(f"Last updated: {datetime.now(timezone.utc).isoformat()}\n")
    lines.append("| Timestamp | Run ID | Result | Passed |\n")
    lines.append("|-----------|--------|--------|--------|\n")

    pass_count = 0
    for rf in results_files[:20]:
        data = json.loads(rf.read_text(encoding="utf-8"))
        ts = data.get("timestamp", "unknown")
        run_id = data.get("run_id", "unknown")
        overall = data.get("overall", "UNKNOWN")
        passed = data.get("passed_count", 0)
        total = data.get("total_count", 0)
        if overall == "PASS":
            pass_count += 1
        lines.append(f"| {ts} | {run_id} | {overall} | {passed}/{total} |\n")

    lines.append(
        f"\n**Historical pass rate**: {pass_count}/{len(results_files)} "
        f"({pass_count / len(results_files) * 100:.0f}%)\n"
    )
    return "".join(lines)

def main() -> int:
    args = sys.argv[1:]

    if "--report" in args:
        print(generate_trend_report())
        return 0

    run_ids = []
    score_all = "--all" in args

    for arg in args:
        if not arg.startswith("-"):
            run_ids.append(arg)

    if score_all:
        if not TRACES_DIR.exists():
            print("No run traces found.", file=sys.stderr)
            return 1
        run_ids = [f.stem for f in sorted(TRACES_DIR.glob("*.jsonl"))]
        if not run_ids:
            print("No run traces found.", file=sys.stderr)
            return 1

    if not run_ids:
        print("Usage: python run_eval.py <run-id> [--all] [--report]", file=sys.stderr)
        return 2

    golden = parse_golden_set(GOLDEN_FILE)
    if not golden:
        print(f"ERROR: No golden cases parsed from {GOLDEN_FILE}", file=sys.stderr)
        return 1

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    exit_code = 0

    for run_id in run_ids:
        scored = score_run(run_id, golden)

        if "error" in scored:
            print(f"ERROR: {scored['error']}", file=sys.stderr)
            exit_code = 1
            continue

        # Write result
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_path = RESULTS_DIR / f"eval-{timestamp}-{run_id}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(scored, f, indent=2, default=str)

        # Print summary
        print(f"\n{'=' * 60}")
        print(f"Eval Results — {run_id}")
        print(f"{'=' * 60}")
        for case in scored["cases"]:
            status = "PASS" if case["passed"] else "FAIL"
            print(f"  {status} — {case['case']}: {case['title']}")
            for detail in case.get("details", []):
                print(f"         {detail}")
        print(
            f"\n  Overall: {scored['overall']} "
            f"({scored['passed_count']}/{scored['total_count']})"
        )
        print(f"  Results saved: {output_path}")

        if scored["overall"] != "PASS":
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
