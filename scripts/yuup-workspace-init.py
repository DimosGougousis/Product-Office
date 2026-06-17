#!/usr/bin/env python3
"""
Create the blackboard workspace for a YUUP run.

Usage:
  python scripts/yuup-workspace-init.py <run-id>

Creates: pipeline/active/<run-id>/ with intake-canvas.md placeholder.
Exit 0 if run-id already exists (idempotent).
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/yuup-workspace-init.py <run-id>", file=sys.stderr)
        return 2

    run_id = sys.argv[1]
    workspace = REPO_ROOT / "pipeline" / "active" / run_id
    workspace.mkdir(parents=True, exist_ok=True)

    # Write a manifest so other tools can discover the workspace
    manifest = workspace / "manifest.json"
    if not manifest.exists():
        manifest.write_text(
            f'{{"run_id": "{run_id}", "created": "{datetime.now(timezone.utc).isoformat()}", "artifacts": []}}\n'
        )

    print(f"Workspace ready: {workspace}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
