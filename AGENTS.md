# Agents Reference (mirror of CLAUDE.md for non-Claude tools)

This file mirrors the agent registry from `CLAUDE.md` so non-Claude AI tools (Cursor, Aider, Codex, etc.) can discover the same routing rules.

See `CLAUDE.md` for the canonical version. See `agents/` for the 11 agent definitions and `governance/framework.md` for the constitution.

## Quick Routing
| Intent | Agent file |
|---|---|
| PRD authoring | `agents/prd-creation.agent.md` |
| Kanban flow | `agents/workflow-automation.agent.md` |
| Jira sync | `agents/jira-integration.agent.md` |
| Slack notify | `agents/slack-integration.agent.md` |
| Drive folders | `agents/google-drive-integration.agent.md` |
| Insights | `agents/ai-insights.agent.md` |
| Conflicts | `agents/conflict-resolution.agent.md` |
| Stakeholders / RACI | `agents/stakeholder-intelligence.agent.md` |
| Content edit / export | `agents/content-documentation.agent.md` |
| KPIs / reporting | `agents/dashboard-reporting.agent.md` |
| Cross-system cascade | `agents/integration-orchestrator.agent.md` |

## Approval Gates
Per `governance/directives/approval-gates.md`: actions costing >$1, destructive, external comms, batches >10, or security changes require explicit user approval.
