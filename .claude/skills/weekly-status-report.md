---
name: weekly-status-report
description: Compose the weekly digest from Kanban state, PRD status, and incidents
---

# Weekly Status Report

## Inputs (auto-pull)
- `operations/kanban.json` — current Kanban state
- `product/prds/active/*/PRD-Summary.md` — PRD status frontmatter
- `pipeline/active/*/STATE.md` — initiative progress
- `observability/incidents/` — anything new this week
- `analytics/reports/` — latest metric snapshot

## Output
`analytics/reports/YYYY-MM-DD-weekly.md`

```markdown
# Weekly Status — Week of YYYY-MM-DD

## Highlights
- 

## Shipped
| Item | Owner | Link |
|---|---|---|

## In Flight
| Item | Stage | Owner | Risk |
|---|---|---|---|

## Blocked
| Item | Blocker | Needed From |
|---|---|---|

## Metrics Snapshot
| Metric | This Week | Last Week | Δ |
|---|---|---|---|

## Incidents
| Severity | Title | Status | RCA |
|---|---|---|---|

## Decisions This Week
- ADR-NNN: <title>

## Next Week
- 
```

## Procedure
1. Generate via `dashboard-reporting` agent (`agents/dashboard-reporting.agent.md`).
2. Cross-check incidents against `observability/incidents/`.
3. Post via `slack-integration` agent to the team channel.
4. Commit to `analytics/reports/` on a `docs/weekly-YYYY-MM-DD` branch.
