# Rollback Runbook

## When to Rollback
- Error rate >5% sustained for 5min
- p95 latency >2x baseline for 5min
- SLO burn rate >10% of monthly budget in 1 hour
- Customer-reported data corruption

## Rollback Steps
1. **Page on-call** if not already aware (`/incident <name>`)
2. **Identify the bad version:** `git log --oneline vX.Y.Z..HEAD`
3. **Re-deploy prior tag:** trigger CD with `vX.Y.(Z-1)`
4. **Verify recovery:** error rate back to baseline, latency normal
5. **Open RCA stub:** `engineering/bug-investigations/INC-NNN-<name>.md`
6. **Notify:** `slack-integration` agent posts to launch + customers if needed
7. **Block forward deploys** until RCA complete

## What NOT to Do
- Don't roll forward with a "quick fix" unless it's a one-line config change you've tested
- Don't skip the RCA — every rollback is a learning opportunity
