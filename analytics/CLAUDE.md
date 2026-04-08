# Analytics Folder

Source of truth for metrics, queries, and data playbooks.

## Doc Index
- `metrics.md` — North-star metric + guardrail metrics + per-feature metric definitions
- `schemas/` — Table definitions (column names, types, join keys)
- `queries/` — Verified SQL snippets, named by metric
- `playbooks/` — Funnel, cohort, retention, AARRR walkthroughs
- `reports/` — Output of `dashboard-reporting` agent (weekly/monthly/quarterly)

## Instructions for Claude
- **ALWAYS** read `schemas/` before writing SQL — never guess column names or join keys.
- Prefer existing snippets in `queries/` over writing new SQL. Add new queries here once verified against the live warehouse.
- When asked to compute a metric, check `metrics.md` for the canonical definition first.
- Route data-pull requests requiring live execution to a Snowflake/Postgres MCP (see `docs/MCP-SETUP.md`). Without one, return the SQL only with a note that it needs human execution.
- Reports go in `reports/YYYY-MM-DD-<name>.md`.
