---
name: release-readiness-check
description: Pre-release gate — CI green, DoD met, ACs pass, SLO budget healthy, runbook updated
---

# Release Readiness Check

## Checklist
For the release candidate at `<branch>` or tag `<vN.N.N>`:

- [ ] **CI green** — `validate-docs.yml` and any test workflow pass on the head commit
- [ ] **All linked PRDs merged** — every PRD targeted for this release is in `main`
- [ ] **Definition of Done met** — see `quality/definition-of-done.md`
- [ ] **Acceptance criteria pass** — for each PRD, `quality/acceptance-criteria/<feature>.md` scenarios have matching tests in `engineering/`, and the latest `pipeline/active/<feature>/VALIDATION.md` shows full coverage
- [ ] **Eval pass rate ≥ threshold** — for AI/LLM features, latest run in `quality/evals/results/` is green
- [ ] **SLO error budget healthy** — `observability/slos.md` shows >50% budget remaining for any service this release touches
- [ ] **Runbook updated** — `delivery/runbooks/deploy.md` reflects any new steps; `rollback.md` is current
- [ ] **Release notes drafted** — by `content-documentation` agent, saved to `delivery/releases/vN.N.N.md`
- [ ] **Stakeholders notified** — `slack-integration` agent posted to launch channel
- [ ] **On-call briefed** — current on-call from `observability/alerts.md` knows the change is going out

## Procedure
Run via `/release-check`. Any failure blocks the release. Do not bypass — if a check is genuinely N/A, mark it explicitly and have a second reviewer approve.
