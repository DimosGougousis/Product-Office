# Product Office — Team OS

> Lean entry point for Claude Code and other AI agents. This file is the **map**, not the data. Drill into nested `CLAUDE.md` files for domain context.

## Doc Index
| Folder | Purpose |
|---|---|
| `governance/` | The constitution: framework, directives (Layer 1), execution scripts (Layer 3) |
| `agents/` | The 11 PO agents (Layer 2 orchestration) — see registry below |
| `product/` | PRDs, strategy, competitive intel, discovery, decisions |
| `pipeline/` | Nine-Organ PM Framework artifacts per initiative (REQUIREMENTS → VALIDATION) |
| `analytics/` | Schemas, queries, metrics, playbooks, reports |
| `engineering/` | RFCs, bug investigations, architecture |
| `delivery/` | GitHub workflow, CI/CD, release process, environments |
| `quality/` | Acceptance criteria, DoD/DoR, evals, UAT, self-improve harness link |
| `observability/` | SLOs, SLIs, dashboards, alerts, incidents |
| `operations/` | Rituals, RACI, runbooks |
| `team/` | Directory, onboarding, 1:1 notes (private) |
| `.claude/` | Skills and slash commands specific to this repo |
| `.github/` | PR templates, issue templates, CI workflows |
| `.vscode/` | VS Code Insiders workspace config |
| `docs/` | MCP setup, contributor guides |

## Agent Registry
All 11 agents live in `agents/`. Route by intent:

| Intent | Agent | File |
|---|---|---|
| Draft a PRD | prd-creation | `agents/prd-creation.agent.md` |
| Move tickets through Kanban | workflow-automation | `agents/workflow-automation.agent.md` |
| Sync PRD ↔ Jira | jira-integration | `agents/jira-integration.agent.md` |
| Notify team / slash commands | slack-integration | `agents/slack-integration.agent.md` |
| Attach files / Drive folders | google-drive-integration | `agents/google-drive-integration.agent.md` |
| Detect bottlenecks | ai-insights | `agents/ai-insights.agent.md` |
| Find conflicts across PRDs | conflict-resolution | `agents/conflict-resolution.agent.md` |
| Generate RACI / brief stakeholders | stakeholder-intelligence | `agents/stakeholder-intelligence.agent.md` |
| Edit / export PRD content | content-documentation | `agents/content-documentation.agent.md` |
| KPI dashboards / reports | dashboard-reporting | `agents/dashboard-reporting.agent.md` |
| Cascade actions across systems | integration-orchestrator | `agents/integration-orchestrator.agent.md` |

**Rule:** Only `integration-orchestrator` may invoke external systems in cascade. Approval gates in `governance/directives/approval-gates.md`.

## Nine-Organ Pipeline (already deployed at `~/.claude/commands/`)
`idea → /office-hours → /plan-ceo-review → /plan-eng-review → /gsd-plan → /gsd-execute → /gsd-review`. `/pm-status` is callable any time. Per-initiative artifacts land in `pipeline/active/<name>/`.

## Team Directory
Edit `team/directory.md`. Format: `Name | Role | GitHub | Slack ID | Email | Timezone`.

## Communication Map
Edit `team/directory.md` (Channels section). Format: `Channel | Purpose | Owner`.

## Progressive Loading Rules
- Read only the folder relevant to the current task. Each top-level folder has its own `CLAUDE.md` with local rules.
- For PRD work → load `product/CLAUDE.md` + the specific `product/prds/active/<name>/`.
- For analytics work → load `analytics/CLAUDE.md` + `analytics/schemas/`.
- For pipeline work → load `pipeline/CLAUDE.md` + the specific `pipeline/active/<name>/`.
- Do **not** preload `agents/` unless routing to an agent — they are large.

## Workflow
1. **Branch** — `feature/<area>-<short-name>` (e.g., `feature/prd-payment-redesign`).
2. **Draft** — Use plan mode + the relevant agent / skill.
3. **PR** — Open via GitHub MCP (`mcp__MCP_DOCKER__create_pull_request`). Use `.github/pull_request_template.md`.
4. **Review** — Tag reviewers per `team/directory.md`. CI must pass (`validate-docs.yml`).
5. **Merge** — Squash to `main`. Latest truth available to all agents.

## MCP Stack
**Primary (already installed):** `MCP_DOCKER` — provides full GitHub workflow, browser (Playwright), fetch, tavily/perplexity/brave research, paper search, code search, Figma.

See `docs/MCP-SETUP.md` for the recommended additions (Slack, Google Drive, Atlassian, Snowflake/Postgres) and install priority.

## Iron Law
Verify before claiming complete. Run the command, read the output, check the exit code. No "should work."
