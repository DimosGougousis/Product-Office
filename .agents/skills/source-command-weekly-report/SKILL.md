---
name: "source-command-weekly-report"
description: "Generate the weekly status report"
---

# source-command-weekly-report

Use this skill when the user asks to run the migrated source command `weekly-report`.

## Command Template

# /weekly-report

Invokes `.Codex/skills/weekly-status-report.md` and the `dashboard-reporting` agent. Output goes to `analytics/reports/YYYY-MM-DD-weekly.md` on a `docs/weekly-YYYY-MM-DD` branch.
