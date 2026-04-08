# CI

## What Runs
On every PR to `main`:
1. **markdownlint** — style check on all `.md` files
2. **link check** — broken-link detection (lychee or markdown-link-check)
3. **validate-prd-links** — `python scripts/validate-prd-links.py product/prds/active/` enforces every PRD has a metric, AC, and SLO link

## Required Checks
`validate-docs` must pass before merge. Configured in branch protection rules.

## Future
- Eval CI: re-run `quality/evals/` on changes to `quality/evals/datasets/` or rubrics
- Python tests: when `scripts/` grows
