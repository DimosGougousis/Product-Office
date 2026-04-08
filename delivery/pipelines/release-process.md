# Release Process

## Versioning
Semantic versioning: `vMAJOR.MINOR.PATCH`. Tag on `main` after `/release-check` passes.

## Steps
1. Create `release/vX.Y.Z` branch from `main`
2. Run `/release-check` — fix anything red
3. Update `delivery/releases/vX.Y.Z.md` with changelog (auto-drafted by `content-documentation` agent)
4. PR `release/vX.Y.Z` → `main`, get two approvers
5. Merge, then tag: `git tag -a vX.Y.Z -m "..."` and push the tag
6. CD picks up the tag and deploys to staging → prod
7. `slack-integration` agent posts to launch channel
8. Monitor SLO burn for 24h

## Hotfix Variant
Branch from the prod tag, fix, tag `vX.Y.(Z+1)`, follow steps 6–8. Backport to `main` after.
