---
name: writing-guide
description: Tone, formatting, and quality bar for all Product Office docs
---

# Writing Guide

## Voice
- **Direct.** Lead with the answer, not the preamble.
- **Active.** "We will ship X" not "X will be shipped."
- **Specific.** Numbers, names, dates. Never "soon" or "many users."
- **Honest.** If we don't know, say so. Mark assumptions explicitly.

## Banned Phrases
- "best-in-class", "leverage", "synergize", "world-class", "delight users", "seamless", "robust" (unless quantified)
- "going forward", "in the near future", "as appropriate"
- "we believe that…" (just state it, or cite evidence)

## Format Defaults
- Bullets over paragraphs when listing 3+ things.
- Tables for any comparison or many-to-many relation.
- Code blocks for commands, file paths, JSON, SQL.
- Headings: H1 = doc title, H2 = section, H3 = subsection. Don't go deeper.
- Frontmatter on every doc with `name`, `status`, `owner`, `date`.

## Length
- Lean one-pager PRD: ≤1 page printed.
- Shape Up pitch: 2–4 pages.
- ADR / RFC: ≤3 pages of body.
- Status report: ≤1 screen.

## Quality Bar (10x examples to imitate)
- The PRD-Summary frontmatter must be parseable as YAML by the CI link validator.
- Every claim has a source (data link, interview, ticket, ADR).
- Every PRD links to a metric, an AC file, and an SLO impact (or marks "N/A — internal tool").

## Self-Check Before Saving
- [ ] Removed all banned phrases
- [ ] Frontmatter complete
- [ ] Required cross-links present
- [ ] Owner assigned
