---
name: new-feature
description: Scaffold PRD + acceptance criteria + metric stub + SLO stub in one shot
---

# /new-feature <feature-name>

## Steps
1. Run `/new-prd <feature-name>` (creates branch + PRD folder).
2. Create `quality/acceptance-criteria/<feature-name>.md` from `quality/acceptance-criteria/_template.md`.
3. Append a stub entry to `analytics/metrics.md` under `## Proposed` with anchor `<feature-name>-metric`.
4. If user-facing, append a stub entry to `observability/slos.md` under `## Proposed`.
5. Update the new PRD's `PRD-Summary.md` frontmatter `links:` to point to all four (metric, AC, SLO, branch PR).
6. Stage all new files: `git add -A`
7. Commit: `git commit -m "feat(prd): scaffold <feature-name>"`
8. Push and open PR.
