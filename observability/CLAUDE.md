# Observability Folder

SLOs, monitoring, alerting, incident timelines.

## Doc Index
- `slos.md` — Service Level Objectives + error budgets per service
- `slis.md` — Service Level Indicators feeding the SLOs
- `dashboards.md` — Index of Grafana / Datadog / Looker boards (URL + owner + purpose)
- `alerts.md` — Alert routing, severity levels, on-call mapping
- `logging-standards.md` — Log levels, structured fields, PII rules
- `tracing.md` — Trace ID propagation, sampling
- `incidents/` — Per-incident timelines (cross-linked to `engineering/bug-investigations/`)

## Instructions for Claude
- When a user-facing PRD is being drafted, check `slos.md` and note any SLO impact in the PRD's `08-Legal-Compliance/` or a dedicated `slo-impact.md`.
- Incident format: `incidents/YYYY-MM-DD-<short-name>/timeline.md` + `summary.md`. Link to the RCA in `engineering/bug-investigations/`.
- Route alert questions to `agents/ai-insights.agent.md` for pattern analysis.
- A Sentry or PagerDuty MCP would automate incident creation — see `docs/MCP-SETUP.md`.
