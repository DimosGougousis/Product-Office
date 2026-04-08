---
name: new-prd
description: Create a branch and scaffold a new PRD from the lean one-pager template
---

# /new-prd <feature-name>

## Steps
1. Validate `<feature-name>` is kebab-case, no spaces, ≤40 chars.
2. Create branch: `git checkout -b feature/prd-<feature-name>`
3. Copy template: `cp -r product/prds/_template product/prds/active/<feature-name>`
4. Update frontmatter in `PRD-Summary.md` and `01-lean-onepager.md` with `name`, `owner`, `created` (today's date).
5. Invoke `.claude/skills/ask-user-workflow.md` — interview the user.
6. Invoke `.claude/skills/draft-prd.md` — fill the one-pager from interview answers.
7. Invoke `.claude/skills/verify-prd.md` — self-check.
8. Open PR via `mcp__MCP_DOCKER__create_pull_request` using `.github/pull_request_template.md`.
9. Tag reviewers from `team/directory.md` based on the feature area.
