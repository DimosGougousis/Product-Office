# PRD Lifecycle Directive

## Stages
1. **Discovery** — `/office-hours` interview → `pipeline/active/<name>/REQUIREMENTS.md`
2. **Triage** — `/plan-ceo-review` → `MODE.md` (Scope Expansion / Selective / Hold / Reject)
3. **Stage 1: Lean One-Pager** — `prd-creation` agent scaffolds `product/prds/active/<name>/01-lean-onepager.md`
4. **Architecture** — `/plan-eng-review` → `ARCHITECTURE.md` (only if MODE accepted)
5. **Stage 2: Shape Up Pitch** — graduate to `02-shape-up-pitch.md` after architecture lock
6. **Planning** — `/gsd-plan` → `PROJECT.md`, `ROADMAP.md`, `STATE.md`
7. **Kanban** — `workflow-automation` agent populates board from ROADMAP
8. **Execution** — `/gsd-execute` writes code + tests
9. **Validation** — `/gsd-review` → `VALIDATION.md` (requirement → test coverage)
10. **Release** — `/release-check` skill, then ship
11. **Archive** — move `pipeline/active/<name>/` and `product/prds/active/<name>/` to `archive/`

## Status Transitions (PRD frontmatter)
`draft → review → approved → in-progress → shipped | killed`

## Required Cross-Links Before Merge
- Metric in `analytics/metrics.md`
- AC in `quality/acceptance-criteria/<name>.md`
- SLO in `observability/slos.md` (or marked N/A)
- Tracking PR/issue
