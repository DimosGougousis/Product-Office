# SLOs (Service Level Objectives)

> Each user-facing service gets an SLO. PRDs that touch a service must reference its SLO anchor here.

## Format
```markdown
### <service-name>
- **SLI:** what we measure (e.g., HTTP success rate over 5m windows)
- **Target:** 99.9% over 30 days
- **Error budget:** 0.1% (~43m/month)
- **Owner:** <team>
- **Dashboard:** <url>
- **Alerts:** see `alerts.md#<service>`
- **Current burn rate:** TBD
```

## Active SLOs
_None yet — add as services come online._

## Proposed
_PRDs in flight may stub their SLO impact here under `## Proposed` until the service is live._
