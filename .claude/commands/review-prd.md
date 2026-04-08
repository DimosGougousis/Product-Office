---
name: review-prd
description: Run verify-prd against an active PRD and report failures
---

# /review-prd <feature-name>

Runs `.claude/skills/verify-prd.md` on `product/prds/active/<feature-name>/` and reports any missing cross-links, broken frontmatter, or banned phrases. Equivalent to `python scripts/validate-prd-links.py product/prds/active/<feature-name>/`.
