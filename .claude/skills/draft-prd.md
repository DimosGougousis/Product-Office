---
name: draft-prd
description: Standardized PRD drafting procedure (lean one-pager → Shape Up graduation)
---

# Draft PRD

## Procedure
1. **Run `ask-user-workflow.md` first.** No drafting until the interview is complete.
2. **Load `writing-guide.md`** and follow the voice/format rules.
3. **Create the PRD folder:** `product/prds/active/<feature-name>/`
4. **Copy the 8-subfolder template:** `cp -r product/prds/_template/* product/prds/active/<feature-name>/`
5. **Fill `01-lean-onepager.md`** with the interview answers. Keep it ≤1 page.
6. **Populate cross-links** in the frontmatter:
   - `metrics:` — pick or create an entry in `analytics/metrics.md`
   - `acceptance_criteria:` — create `quality/acceptance-criteria/<feature>.md` from `_template.md`
   - `slo:` — if user-facing, link to `observability/slos.md`
7. **Run `verify-prd.md`** to self-check. Fix any failures before opening the PR.
8. **Hand off to `prd-creation` agent** (`agents/prd-creation.agent.md`) to generate the 5 Kanban tasks and cascade to Jira/Drive/Slack via `integration-orchestrator`.

## Stage Graduation
- A PRD only graduates from Stage 1 (lean one-pager) → Stage 2 (Shape Up pitch) **after** `/plan-ceo-review` returns a positive MODE in `pipeline/active/<feature>/MODE.md`.
- On graduation: copy `02-shape-up-pitch.md` from the template into the PRD folder, expand the breadboard/rabbit-holes/no-gos, and update `PRD-Summary.md` to check both stage boxes.

## Anti-Patterns
- Drafting before the interview
- Skipping the cross-links ("I'll add metrics later" — no, the verify-prd CI gate will reject the PR)
- Jumping to Stage 2 without CEO review
