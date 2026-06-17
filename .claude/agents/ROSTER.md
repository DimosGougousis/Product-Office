# YUUP Roster — Agent Command Registry

> YUUP reads this file at dispatch time to know who it commands. Adding a row here places an agent under YUUP's command — no other wiring needed.

## Active Roster

| Agent | Dispatch Trigger | Tools Tier | Approval-Sensitive? |
|---|---|---|---|
| `robot` | Automation, scripting, MCP wiring, CI hooks, integration build | Full (read/write/terminal) | Yes — cost, destructive, external |
| `research` | Research, competitive intel, codebase archaeology, tool comparison | Read-only + web search/fetch | No (read-only) |
| `process-designer` | SOPs, directives, RACI, checklists, workflow design | Read + write docs | No (docs only) |
| `critique` | Review deliverables, quality gate, adversarial QA | Read-only | No (read-only) |
| `yuup` | Orchestration identity — actual orchestration runs via `/yuup` slash command | Full | N/A (main thread) |

## Dispatch Rules
1. **Parallel** when tasks are independent (e.g., `research` + `process-designer` on different sub-tasks).
2. **Sequential** when one task depends on another's output (e.g., `research` → `process-designer` → `critique`).
3. **Critique loop** — after any specialist delivers, route through `critique`. On `REVISE`, re-dispatch the owning specialist (max 2 rounds). On `REJECT`, surface to the user with the critique's reasoning.
4. **Approval gates** — before any action matching `governance/directives/approval-gates.md` (cost >\$1, destructive, external comms, batch >10, security, schema), STOP and AskUserQuestion. One gate per question.

## Bridge: Existing 11 Persona Agents

The `agents/*.agent.md` files are persona specs (GitHub-Copilot format) for the external "PRD Partner" app. YUUP treats them as routing guidance, not runnable subagents:

| Intent | Route to (persona) |
|---|---|
| Draft a PRD | `agents/prd-creation.agent.md` — use for PRD structure/conventions, not as dispatch target |
| Move tickets through Kanban | `agents/workflow-automation.agent.md` |
| Sync PRD ↔ Jira | `agents/jira-integration.agent.md` |
| Notify team / Slack | `agents/slack-integration.agent.md` |
| Attach files / Drive | `agents/google-drive-integration.agent.md` |
| Detect bottlenecks | `agents/ai-insights.agent.md` |
| Find conflicts across PRDs | `agents/conflict-resolution.agent.md` |
| Generate RACI / brief stakeholders | `agents/stakeholder-intelligence.agent.md` |
| Edit / export PRD content | `agents/content-documentation.agent.md` |
| KPI dashboards / reports | `agents/dashboard-reporting.agent.md` |
| Cascade actions across systems | `agents/integration-orchestrator.agent.md` — only this one may cascade |

When an objective matches a persona agent's domain, YUUP uses that agent's conventions and output format, but performs the work in the main thread or via one of its runnable specialists.

## Adding a New Agent
Run `/new-agent <name>` — the scaffolding skill interviews you, generates the agent file, and appends a row to this roster. The new agent is immediately under YUUP's command.
