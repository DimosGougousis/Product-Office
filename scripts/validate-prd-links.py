#!/usr/bin/env python3
"""
Validate that every PRD under the given path has the required cross-links:
- frontmatter.links.metrics      → exists in analytics/metrics.md
- frontmatter.links.acceptance_criteria → file exists
- frontmatter.links.slo          → exists in observability/slos.md (or marked N/A)

Usage:
  python scripts/validate-prd-links.py product/prds/active/
Exit code 0 = all pass. Non-zero = failures (printed).
"""
from __future__ import annotations
import sys
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
METRICS_FILE = REPO_ROOT / "analytics" / "metrics.md"
SLOS_FILE = REPO_ROOT / "observability" / "slos.md"


def parse_frontmatter(text: str) -> dict | None:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"  YAML parse error: {e}", file=sys.stderr)
        return None


def file_contains_anchor(file_path: Path, anchor_or_text: str) -> bool:
    if not file_path.exists():
        return False
    text = file_path.read_text(encoding="utf-8")
    if "#" in anchor_or_text:
        anchor = anchor_or_text.split("#", 1)[1]
        # Match a heading or explicit anchor
        return bool(re.search(rf"^#+\s.*{re.escape(anchor)}", text, re.MULTILINE | re.IGNORECASE))
    return anchor_or_text in text


def validate_prd(prd_summary: Path) -> list[str]:
    errors: list[str] = []
    text = prd_summary.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{prd_summary}: missing or invalid YAML frontmatter"]

    name = fm.get("name", "<unnamed>")
    links = fm.get("links") or {}

    # Templates and stubs are exempt — they live under _template/ paths.
    if "_template" in str(prd_summary):
        return []

    # Required link: metrics
    metrics = links.get("metrics")
    if not metrics:
        errors.append(f"{prd_summary} ({name}): missing links.metrics")
    elif not file_contains_anchor(REPO_ROOT / "analytics" / "metrics.md", metrics.split("/")[-1]):
        errors.append(f"{prd_summary} ({name}): metrics link '{metrics}' not found in analytics/metrics.md")

    # Required link: acceptance_criteria
    ac = links.get("acceptance_criteria")
    if not ac:
        errors.append(f"{prd_summary} ({name}): missing links.acceptance_criteria")
    elif not (REPO_ROOT / ac).exists():
        errors.append(f"{prd_summary} ({name}): AC file '{ac}' does not exist")

    # SLO link: required if not explicitly N/A
    slo = links.get("slo")
    if slo and not str(slo).lower().startswith("n/a"):
        if not file_contains_anchor(REPO_ROOT / "observability" / "slos.md", slo.split("/")[-1]):
            errors.append(f"{prd_summary} ({name}): slo link '{slo}' not found in observability/slos.md")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: validate-prd-links.py <path-to-active-prds-dir>", file=sys.stderr)
        return 2
    target = Path(argv[1])
    if not target.exists():
        print(f"Path not found: {target}", file=sys.stderr)
        return 2

    summaries = list(target.rglob("PRD-Summary.md"))
    if not summaries:
        print(f"No PRD-Summary.md files under {target} (nothing to validate)")
        return 0

    all_errors: list[str] = []
    for s in summaries:
        all_errors.extend(validate_prd(s))

    if all_errors:
        print(f"FAIL: {len(all_errors)} link issue(s):", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: {len(summaries)} PRD(s) validated, all required links present.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
