# Agents Folder

The 11 PO agents (Layer 2 of the governance framework). Each is a self-contained markdown directive.

## Routing Rules
- **Always** load only the specific agent file you need — they are large.
- For multi-system actions (e.g., "create PRD and notify Slack and open Jira Epic"), route to `integration-orchestrator.agent.md` — it's the only agent permitted to cascade.
- For read-only queries about state, prefer `dashboard-reporting` or `ai-insights` over hitting integrations.

## Approval Gates
Per `governance/directives/approval-gates.md`, any agent action that:
- Costs >$1
- Is destructive (delete, overwrite, force-push)
- Sends external comms (Slack post, email, Jira create)
- Operates on >10 items in batch
- Touches security/credentials

…requires explicit user approval before execution.

## Files
| Agent | Owner Domain |
|---|---|
| `prd-creation.agent.md` | `product/prds/` |
| `workflow-automation.agent.md` | `operations/kanban.json` |
| `jira-integration.agent.md` | Jira (external) |
| `slack-integration.agent.md` | Slack (external) |
| `google-drive-integration.agent.md` | Google Drive (external) |
| `ai-insights.agent.md` | `analytics/`, Kanban history |
| `conflict-resolution.agent.md` | `product/decisions/conflicts/` |
| `stakeholder-intelligence.agent.md` | `team/directory.md` |
| `content-documentation.agent.md` | `product/prds/`, `delivery/releases/` |
| `dashboard-reporting.agent.md` | `analytics/reports/` |
| `integration-orchestrator.agent.md` | All of the above |
