---
name: competitive-teardown
description: Structured competitor analysis using web research MCPs
---

# Competitive Teardown

## Procedure
1. Copy `product/competitive-intel/_template.md` to `product/competitive-intel/<competitor>.md`.
2. Use research MCPs (already available via `MCP_DOCKER`):
   - `mcp__MCP_DOCKER__tavily_research` — deep web research
   - `mcp__MCP_DOCKER__perplexity_research` — sourced answers
   - `mcp__MCP_DOCKER__browser_navigate` + `browser_take_screenshot` — visit their site, capture pricing/feature pages
   - `mcp__MCP_DOCKER__paper_search` — academic / industry reports
3. Fill the template sections: positioning, target customer, feature surface table, pricing, strengths/weaknesses, strategic implications.
4. Set `threat_level` honestly. "Critical" means it changes our roadmap.
5. Commit on `feature/intel-<competitor>` branch and PR for review.

## Quality Bar
- Every claim has a source URL in the Sources section.
- Feature comparison table compares to **our actual** capabilities, not marketing claims.
- Strategic implications must propose a forced move or explicitly say "no action needed."
