# Product Office

A Product Team Operatin System repository that treats product management knowledge — strategy, PRDs, analytics, processes — as a living, version-controlled codebase. Built for collaboration with AI agents (Claude Code, MCP-enabled tooling) and human teammates via GitHub.

Repo: https://github.com/DimosGougousis/Product-Office

## What lives here
- **`governance/`** — The 3-layer Product Ownership Governance Framework constitution.
- **`agents/`** — 11 specialized PO agents (PRD creation, Jira/Slack/Drive integration, RACI, conflict resolution, dashboards, etc.).
- **`pipeline/`** — Per-initiative artifacts produced by the Nine-Organ PM Framework skills (`/office-hours` → `/gsd-review`).
- **`product/`** — PRDs (lean one-pager → Shape Up pitch), strategy, competitive intel, discovery, decisions.
- **`analytics/`**, **`engineering/`**, **`delivery/`**, **`quality/`**, **`observability/`** — domain folders for metrics, RFCs, CI/CD, ACs/evals, and SLOs.
- **`team/`**, **`operations/`** — directory, RACI, rituals, runbooks.

See `CLAUDE.md` for the full doc index and agent registry.

## Quick start

### 1. Clone
```bash
git clone https://github.com/DimosGougousis/Product-Office.git
cd Product-Office
```

### 2. Open in VS Code Insiders
```bash
code-insiders Product-Office.code-workspace
```
Insiders will prompt to install the recommended extensions (Claude Code, GitHub PR, markdownlint, mermaid, python). Accept all.

### 3. Verify Claude Code can route
Open the Claude Code panel and ask: *"What's in the agent registry?"* — it should read `CLAUDE.md` and list all 11 agents.

### 4. Try a slash command
- `/pm-status` — read-only dashboard across all initiatives
- `/office-hours` — kick off a new initiative; writes to `pipeline/active/<name>/REQUIREMENTS.md`
- `/new-prd <name>` — creates a branch + scaffolds a PRD from `product/prds/_template/`

### 5. Open a PR
Branch → draft on a feature branch → `mcp__MCP_DOCKER__create_pull_request` (or use the GitHub PR extension). CI runs `validate-docs.yml` (markdownlint + link check + PRD link validator). Tag a reviewer per `team/directory.md`. Merge to `main` once green.

## How AI agents use this repo
- **Claude Code** loads `CLAUDE.md` first (the map), then drills into nested `CLAUDE.md` files only for the folder relevant to the current task. This is "progressive loading" — saves context window.
- Slash commands in `~/.claude/commands/` (the Nine-Organ pipeline) write artifacts into `pipeline/active/<initiative>/`.
- Agents in `agents/` are routed by intent — e.g., asking Claude to "draft a PRD" routes to `prd-creation.agent.md`, which knows the 8-subfolder template and the Kanban hand-off.

## MCP setup
This repo assumes `MCP_DOCKER` is installed (provides GitHub, browser, web research, code search). For full PO agent functionality, add Slack, Google Drive, Atlassian (Jira), and a SQL MCP. See `docs/MCP-SETUP.md` for install order, env vars, and which agents depend on each.

## Contributing
See `CONTRIBUTING.md` for branch naming, PR etiquette, AC requirements, and the verify-prd checklist.

## License
Internal — not yet licensed. Add `LICENSE` before going public.
