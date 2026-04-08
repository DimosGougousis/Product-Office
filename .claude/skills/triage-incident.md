---
name: triage-incident
description: Open an incident timeline and link to RCA
---

# Triage Incident

## Procedure
1. Create folder `observability/incidents/YYYY-MM-DD-<short-name>/`
2. Drop two files inside:
   - `timeline.md` — UTC timestamps, who did what
   - `summary.md` — one-paragraph what/when/impact
3. Notify via `slack-integration` agent to the on-call channel from `observability/alerts.md`.
4. Open a corresponding RCA stub at `engineering/bug-investigations/INC-NNN-<name>.md` from the template.
5. Cross-link both ways.
6. After resolution, fill the RCA's "Prevention" section with concrete tickets/PRs and check the SLO impact in `observability/slos.md`.

## Severity
- **SEV1:** customer-visible outage, data loss, security incident — page on-call immediately
- **SEV2:** degraded experience for a subset, workaround exists — same-day fix
- **SEV3:** internal-only or cosmetic — next sprint
