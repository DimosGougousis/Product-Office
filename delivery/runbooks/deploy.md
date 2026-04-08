# Deploy Runbook

## Pre-Deploy
- [ ] `/release-check` passed
- [ ] On-call notified
- [ ] Rollback plan reviewed (`rollback.md`)
- [ ] SLO burn rate < 50% on services being deployed

## Deploy
1. Tag the release: `git tag -a vX.Y.Z -m "release notes"`
2. Push the tag: `git push origin vX.Y.Z`
3. CD pipeline picks up the tag (verify in CI dashboard)
4. Watch staging smoke tests
5. Approve prod promotion
6. Watch prod for 15 minutes — error rate, p95 latency, business metrics

## Post-Deploy
- [ ] Slack post via `slack-integration` agent
- [ ] Update `delivery/releases/vX.Y.Z.md` with deploy timestamp
- [ ] Archive related PRDs to `product/prds/archive/`
