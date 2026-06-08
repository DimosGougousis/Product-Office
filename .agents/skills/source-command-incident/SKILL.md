---
name: "source-command-incident"
description: "Open an incident timeline and notify on-call"
---

# source-command-incident

Use this skill when the user asks to run the migrated source command `incident`.

## Command Template

# /incident <short-name>

Invokes `.Codex/skills/triage-incident.md`. Creates `observability/incidents/YYYY-MM-DD-<short-name>/` with `timeline.md` and `summary.md`, posts to the on-call Slack channel via the `slack-integration` agent, and stubs an RCA in `engineering/bug-investigations/`.
