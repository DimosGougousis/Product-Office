---
name: <feature-name>
stage: lean-onepager
status: draft
owner: <pm>
created: YYYY-MM-DD
links:
  metrics: analytics/metrics.md#<metric-anchor>
  acceptance_criteria: quality/acceptance-criteria/<feature>.md
  slo: observability/slos.md#<service>
  jira: <epic-key>
  pr: <pr-url>
---

# <Feature Name> — Lean One-Pager

## Problem
What hurts? Whose pain is it? How do we know it's real?

## Customer
Specific segment. Not "everyone." Reference discovery interviews if available.

## Solution Sketch
Two or three sentences. No screens, no spec — just the shape.

## Success Metric
One number. Defined in `analytics/metrics.md`. Threshold + horizon (e.g., "+15% activation in 30 days").

## Risks / Unknowns
Top 3, ranked. What would kill this?

## Next Step
- [ ] Run `/plan-ceo-review` to decide whether to graduate to Stage 2 (Shape Up Pitch)
- [ ] If green, copy to `02-shape-up-pitch.md` and expand
