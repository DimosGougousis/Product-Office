# Contributing to Product Office

This repo is the team's "Team OS" — strategy, PRDs, processes, all version-controlled. Contribute the same way engineers contribute code.

## First-Time Setup

1. **Install VS Code Insiders** — https://code.visualstudio.com/insiders/
2. **Clone the repo:**
   ```bash
   git clone https://github.com/DimosGougousis/Product-Office.git
   cd Product-Office
   ```
3. **Open the workspace:**
   ```bash
   code-insiders Product-Office.code-workspace
   ```
4. **Accept the recommended extensions** when prompted (Claude Code, GitHub PR, markdownlint, mermaid, python).
5. **Verify Claude Code** can read the repo: open the panel and ask *"What's in the agent registry?"* — it should list all 11 agents from `CLAUDE.md`.

## How to Contribute

### Branch
Use the conventions in `delivery/github/branch-strategy.md`:
- `feature/<area>-<short-name>` for new PRDs and features
- `docs/<topic>` for pure docs
- `fix/<short-name>` for bug fixes

### Draft
Use slash commands instead of writing from scratch:
- `/new-prd <name>` — scaffolds a PRD from the template
- `/new-feature <name>` — scaffolds PRD + AC + metric + SLO stubs together
- `/office-hours` — runs the discovery interview before any new initiative
- `/pm-status` — read-only dashboard, callable any time

### PR
- Use the template (auto-loaded from `.github/pull_request_template.md`)
- Fill in **all** the linked items (PRD, AC, metric, SLO, issue)
- Tag a reviewer per `team/directory.md`
- CI must be green — `validate-docs` runs markdownlint + link check + PRD link validator

### Review
- Spec compliance first, then code/doc quality
- Push back with reasoning when feedback is wrong — review is a conversation, not a checklist
- Use GitHub suggested changes for small edits

### Merge
- Squash and merge to `main`
- Use Conventional Commits in the PR title: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`

## PRD-Specific Rules

Every PRD must:
- Start as a **Lean One-Pager** (`product/prds/_template/01-lean-onepager.md`)
- Only graduate to a **Shape Up Pitch** after `/plan-ceo-review` returns positive MODE
- Link to a metric in `analytics/metrics.md`
- Link to an AC file in `quality/acceptance-criteria/<feature>.md`
- Link to an SLO in `observability/slos.md` (or mark `slo: N/A — internal`)

The `verify-prd` skill (and CI) enforces these. Don't try to bypass — fix the links instead.

## Agent Etiquette

- Route requests to the right agent — see the registry in `CLAUDE.md`
- For cascading actions across Jira/Slack/Drive, route to `integration-orchestrator`, not directly to each integration
- Approval gates in `governance/directives/approval-gates.md` are mandatory — any agent action that costs >$1, is destructive, or sends external comms requires explicit user approval

## Getting Help

- **Onboarding:** `team/onboarding.md`
- **Writing style:** `.claude/skills/writing-guide.md`
- **MCP setup:** `docs/MCP-SETUP.md`
- **Governance:** `governance/framework.md`
- **Ask in Slack:** `#prd-reviews` (see `team/directory.md`)
