# Product Folder

Houses everything customer-facing: PRDs, strategy, competitive intel, discovery research, and product decisions.

## Doc Index
- `prds/_template/` — 8-subfolder PRD template (matches google-drive-integration agent's expected structure)
- `prds/_template/01-lean-onepager.md` — Stage 1 PRD format (every PRD starts here)
- `prds/_template/02-shape-up-pitch.md` — Stage 2 PRD format (after `/plan-ceo-review` graduation)
- `prds/active/` — In-flight PRDs, one folder per feature
- `prds/archive/` — Shipped or killed
- `strategy/vision.md` — Long-range vision
- `strategy/roadmap-YYYY-QX.md` — Quarterly roadmap
- `strategy/okrs/` — Per-quarter OKRs
- `competitive-intel/` — Rival research (use `mcp__MCP_DOCKER__tavily_research` or `perplexity_research`)
- `discovery/interviews/` — User interview notes
- `discovery/insights/` — Synthesized themes
- `decisions/` — ADR-style product decision log
- `decisions/conflicts/` — Output of `conflict-resolution` agent

## Instructions for Claude
- **Every new PRD** starts as a Lean One-Pager (`_template/01-lean-onepager.md`) inside its own folder under `prds/active/<feature-name>/`.
- Only graduate to a Shape Up Pitch (`02-shape-up-pitch.md`) after `/plan-ceo-review` returns a positive MODE.
- A PRD is only mergeable to `main` if `verify-prd` skill passes: it must link to (a) a metric in `analytics/metrics.md`, (b) acceptance criteria in `quality/acceptance-criteria/<feature>.md`, (c) an SLO impact in `observability/slos.md` if user-facing.
- Route PRD authoring requests to `agents/prd-creation.agent.md`.
- Route stakeholder/RACI questions to `agents/stakeholder-intelligence.agent.md`.
- Use `competitive-intel/_template.md` for new competitor analyses.
