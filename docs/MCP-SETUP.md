# MCP Setup

This repo is built around **Model Context Protocol (MCP)** servers that give Claude Code (and other AI agents) the ability to take real actions — open PRs, post to Slack, run SQL, fetch competitor data.

## Already Installed: `MCP_DOCKER`

The user's primary MCP. Provides a wide range of tools out of the box. **No extra install needed for these.**

| Capability | Tools (prefix `mcp__MCP_DOCKER__`) | Used by |
|---|---|---|
| GitHub workflow | `create_pull_request`, `add_issue_comment`, `list_issues`, `get_file_contents`, `create_branch`, `merge_pull_request`, `request_copilot_review`, `list_pull_requests`, `search_code`, `search_repositories` | All PR-related slash commands; the `delivery/` workflow |
| Browser (Playwright) | `browser_navigate`, `browser_take_screenshot`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_evaluate` | `competitive-teardown` skill, `discovery/` research |
| Web research | `tavily_search`, `tavily_research`, `tavily_extract`, `perplexity_research`, `perplexity_ask`, `brave_web_search`, `brave_news_search` | `competitive-intel/`, `discovery/`, market intelligence |
| Code search | `search_code` | finding patterns across linked repos |
| Academic | `paper_search` | research-driven PRDs |
| Figma | `mcp__Figma__get_design_context`, `get_screenshot`, `get_metadata` | PRDs that reference design files |
| Docs | `fetch`, `fetch_content`, `hf_doc_fetch`, `hf_doc_search` | one-off URL fetches |

That covers GitHub end-to-end and most research needs. The Product Office is **functional today** with just `MCP_DOCKER`.

## Recommended to Add (priority order)

Each of these unlocks a specific PO agent or domain. Install in the order below for best ROI.

### 1. Slack MCP — unlocks `slack-integration` agent
- **Why:** Without it, the slack-integration agent is read-only. With it: post to channels, DM, react, slash commands.
- **Source:** Anthropic's official Slack MCP, or `https://github.com/modelcontextprotocol/servers/tree/main/src/slack`
- **Required env vars:**
  - `SLACK_BOT_TOKEN` (xoxb-...)
  - `SLACK_TEAM_ID`
  - `SLACK_CHANNEL_IDS` (comma-separated)
- **Used by:** `agents/slack-integration.agent.md`, `weekly-status-report` skill, `triage-incident` skill

### 2. Google Drive MCP — unlocks `google-drive-integration` agent
- **Why:** The PRD 8-subfolder structure is designed to mirror to Drive for non-technical stakeholder access.
- **Source:** `https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive`
- **Required env vars:**
  - `GDRIVE_OAUTH_PATH` (path to OAuth credentials JSON)
- **Used by:** `agents/google-drive-integration.agent.md`, `prd-creation` agent (for the Drive folder mirror)

### 3. Atlassian / Jira MCP — unlocks `jira-integration` agent
- **Why:** Bidirectional PRD ↔ Jira Epic/Issue sync. Without it, the integration-orchestrator's full cascade is gated.
- **Source:** Atlassian's official MCP or community implementations
- **Required env vars:**
  - `JIRA_HOST` (e.g., `your-org.atlassian.net`)
  - `JIRA_EMAIL`
  - `JIRA_API_TOKEN`
- **Used by:** `agents/jira-integration.agent.md`, `agents/integration-orchestrator.agent.md`

### 4. Snowflake or Postgres MCP — makes analytics live
- **Why:** Lets the `dashboard-reporting` agent execute queries from `analytics/queries/` against the warehouse and pull real numbers into reports.
- **Source:** Anthropic example servers in the modelcontextprotocol/servers repo
- **Required env vars:**
  - `DATABASE_URL` or platform-specific (`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, etc.)
- **Used by:** `agents/dashboard-reporting.agent.md`, `analytics/CLAUDE.md` instructions

### 5. Optional Add-Ons

| MCP | Why | When to Add |
|---|---|---|
| **Sentry MCP** | Auto-create incidents from production errors → `observability/incidents/` | When you have a Sentry account and SEV2+ velocity matters |
| **PagerDuty MCP** | Read on-call schedule, ack incidents from terminal | When on-call rotation exists |
| **Notion MCP** | Mirror published PRDs to a stakeholder-readable Notion space | If non-technical execs prefer Notion over GitHub |
| **Linear MCP** | If team uses Linear instead of Jira | Replaces Atlassian MCP in that case |
| **Confluence MCP** | Sync archived PRDs / RFCs to Confluence | If org has a Confluence-based knowledge base |

## Install Order Summary

```
1. Slack MCP             → unlocks slack-integration agent
2. Google Drive MCP      → unlocks drive agent + 8-subfolder Drive mirror
3. Atlassian/Jira MCP    → unlocks jira agent + full orchestrator cascade
4. Snowflake/Postgres    → makes analytics live
5. Sentry / PagerDuty    → closes the observability loop (optional)
```

## CI Behavior When MCPs Are Missing

The CI workflow `validate-docs.yml` does **not** depend on any MCP — it only runs markdownlint, link checks, and the PRD link validator. So colleagues who haven't installed every MCP can still clone the repo, contribute PRDs, and pass CI.

Agent-level functionality degrades gracefully: e.g., the `slack-integration` agent will report "Slack MCP not configured" instead of failing the whole pipeline.

## Verifying an MCP

After installing, restart Claude Code and verify with:
```
List all available tools matching "slack"
```
Expected: tools prefixed with `mcp__Slack__` (or whatever the server registers as).
