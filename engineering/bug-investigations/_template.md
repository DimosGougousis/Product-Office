---
incident: INC-NNN
date: YYYY-MM-DD
severity: SEV1 | SEV2 | SEV3
duration: <minutes>
owner: <ic>
---

# RCA — <Short Title>

## Summary
One paragraph: what broke, who saw it, how it was fixed.

## Timeline (UTC)
| Time | Event |
|---|---|
| HH:MM | Detected by <alert/user> |
| HH:MM | Acknowledged by <person> |
| HH:MM | Mitigation applied |
| HH:MM | Resolved |

## Root Cause
The actual underlying cause — not the symptom. Use 5 Whys.

## Contributing Factors
- 

## Fix
What was changed (commit / PR link).

## Prevention
- [ ] Test added: <link>
- [ ] Alert added / tuned: <link>
- [ ] Runbook updated: <link>
- [ ] SLO impact recorded in `observability/slos.md`

## Linked
- Incident timeline: `observability/incidents/YYYY-MM-DD-<name>/`
- PRD (if regression): `product/prds/active/<feature>/`
