---
name: incident
description: Open an incident timeline and notify on-call
---

# /incident <short-name>

Invokes `.claude/skills/triage-incident.md`. Creates `observability/incidents/YYYY-MM-DD-<short-name>/` with `timeline.md` and `summary.md`, posts to the on-call Slack channel via the `slack-integration` agent, and stubs an RCA in `engineering/bug-investigations/`.
