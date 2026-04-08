---
name: <feature-name>
stage: shape-up-pitch
status: draft
owner: <pm>
appetite: <small-batch-2-weeks | big-batch-6-weeks>
created: YYYY-MM-DD
graduated_from: 01-lean-onepager.md
links:
  metrics: analytics/metrics.md#<metric-anchor>
  acceptance_criteria: quality/acceptance-criteria/<feature>.md
  slo: observability/slos.md#<service>
  architecture: pipeline/active/<feature>/ARCHITECTURE.md
  jira: <epic-key>
  pr: <pr-url>
---

# <Feature Name> — Shape Up Pitch

## Problem
The raw pain. A specific story works better than abstractions.

## Appetite
How much time we're willing to spend. Small batch (≤2 weeks) or big batch (≤6 weeks). This is a budget, not an estimate.

## Solution
The fat-marker sketch. Use Mermaid or embedded ASCII for breadboards / fat-marker drawings. Show how the user moves through it. Avoid pixel-level design.

```mermaid
flowchart LR
  A[Entry] --> B[Key step] --> C[Outcome]
```

### Breadboard
- **Place 1:** affordances
- **Place 2:** affordances
- **Connection lines:** which affordance leads where

## Rabbit Holes
Things we explicitly want to avoid getting stuck on. Decisions made in advance to prevent scope creep.

## No-Gos
What this pitch is **not** doing. Things that sound related but are out of scope.

## Cool-Down Risks
What might still trip us up after the bet is approved?

## Bet Table Decision
- [ ] Bet accepted by CEO/Steering
- [ ] Cycle assigned: <YYYY-CN>
- [ ] Team assigned

## Next Step
- [ ] Run `/plan-eng-review` → produces `ARCHITECTURE.md`
- [ ] Run `/gsd-plan` → produces `PROJECT.md`, `ROADMAP.md`, `STATE.md`
- [ ] `prd-creation` agent populates `01–08` subfolders here
