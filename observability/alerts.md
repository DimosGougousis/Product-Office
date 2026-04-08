# Alerts

| Alert | Severity | Trigger | Routes To | Runbook |
|---|---|---|---|---|
| _example_ | SEV1 | error_rate > 5% for 5m | #oncall | `delivery/runbooks/rollback.md` |

## On-Call Rotation
See PagerDuty (or whichever schedule tool is configured). Document the URL here once set up.

## Severity Definitions
- **SEV1** — customer-visible outage, data loss, security event. Page immediately.
- **SEV2** — degraded experience, workaround exists. Same-day fix.
- **SEV3** — internal-only or cosmetic. Next sprint.
