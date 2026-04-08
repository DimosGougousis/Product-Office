---
name: ask-user-workflow
description: Forces structured user interview before drafting any PRD or strategy doc
---

# Ask-User Workflow

> **MUST run before any PRD draft.** No exceptions. Guessing strategy is a plan failure.

## Required Questions (use AskUserQuestion tool)
Ask these one at a time. Do not batch. Do not assume defaults.

1. **Primary goal** — What outcome are we trying to achieve? (1 sentence)
2. **Customer** — Who is this for? Name a specific segment, not "everyone."
3. **Success metric** — How will we know it worked? Reference `analytics/metrics.md`.
4. **Non-goals** — What is this explicitly NOT doing?
5. **Stakeholders** — Who needs to review or be informed? (cross-check `team/directory.md`)
6. **Deadline / appetite** — When does this need to land, or how much time are we willing to spend?
7. **Risks / unknowns** — What could kill this?

## After the Interview
- Write answers verbatim into the PRD's `01-Problem-Statement/` and `03-Success-Metrics/` folders.
- Then invoke `draft-prd.md` to scaffold the rest.

## Anti-Pattern
Do **not** propose a solution before completing this workflow. Discovery first, design second.
