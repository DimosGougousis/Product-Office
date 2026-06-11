---
name: "source-command-review-prd"
description: "Run verify-prd against an active PRD and report failures"
---

# source-command-review-prd

Use this skill when the user asks to run the migrated source command `review-prd`.

## Command Template

# /review-prd <feature-name>

Runs `.Codex/skills/verify-prd.md` on `product/prds/active/<feature-name>/` and reports any missing cross-links, broken frontmatter, or banned phrases. Equivalent to `python scripts/validate-prd-links.py product/prds/active/<feature-name>/`.
