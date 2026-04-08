# Approval Gates

> Per the Product Ownership Governance Framework. Any agent action matching these criteria requires explicit user approval **before** execution.

## Required Approval
| Trigger | Why |
|---|---|
| Cost > $1 (any external API call with billing) | Cost runaway prevention |
| Destructive op (delete, force-push, drop, rm -rf) | Irreversible |
| External communication (Slack post, email, Jira create, GitHub PR comment) | Reputation / blast radius |
| Batch > 10 items | Avoid mass mistakes |
| Security / credential change | Trust boundary |
| Schema migration | Data integrity |

## How Approval Works
- Use `AskUserQuestion` tool with the proposed action and explicit cost/consequence.
- Wait for explicit confirmation. Do **not** treat past approval as standing permission.
- Log the approval in `governance/.tmp/logs/approvals.jsonl` (gitignored).

## Anti-Pattern
Bundling multiple approval-required actions into one "ok?" question. Each gated action gets its own approval.
