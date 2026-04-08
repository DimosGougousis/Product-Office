# Kanban Flow Directive

## Columns
1. **Backlog** — Triaged, not started
2. **Research** — Discovery / spike in progress
3. **Waiting** — Blocked on external input (review, dependency, customer)
4. **Review** — Implementation done, awaiting code/PRD review
5. **Complete** — Merged, validated

## WIP Limits
- Research: 3
- Waiting: no limit (but flagged in weekly report)
- Review: 5

## Auto-Transitions (workflow-automation agent)
- PR opened → card moves Research → Review
- PR merged + `/gsd-review` green → Review → Complete
- No activity 5 days in Research → flag in `ai-insights`
- Card in Waiting >7 days → escalate via slack-integration

## State File
`operations/kanban.json` is the source of truth. Edited only by the `workflow-automation` agent.
