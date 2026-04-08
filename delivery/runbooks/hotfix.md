# Hotfix Runbook

## When
- SEV1 in prod that can't wait for the normal release cycle
- Security patch
- Customer-blocking bug with no workaround

## Steps
1. Branch from the current prod tag: `git checkout -b hotfix/<short-name> vX.Y.Z`
2. Make the smallest possible fix — single concern only
3. Add a regression test
4. PR with `area:incident` + `p0` labels
5. Get one approver (instead of the usual two) — document why in PR
6. Merge, tag `vX.Y.(Z+1)`, deploy via `deploy.md`
7. **Backport to `main`** in a follow-up PR
8. Open RCA in `engineering/bug-investigations/`
