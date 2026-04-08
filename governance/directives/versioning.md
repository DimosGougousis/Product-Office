# Versioning Directive

## Semantic Versioning for Directives and Agents
`MAJOR.MINOR.PATCH`

- **MAJOR** — breaking change to agent contract (input/output schema, removed capability)
- **MINOR** — new capability, backward-compatible
- **PATCH** — bug fix, doc clarification, prompt tweak

## Where to Version
- Each `.agent.md` file: `version:` field in frontmatter
- Each directive in `directives/`: `version:` field in frontmatter
- Each rubric in `quality/evals/rubrics/`: `version:` in filename (`<name>-v1.md`, `<name>-v2.md`)

## Backups
On every change, the prior version is auto-saved to `governance/.tmp/backups/directives/<file>-<timestamp>.md` (gitignored — git history is the durable record).

## Release Notes for Agents
When an agent gets a MINOR or MAJOR bump, add a `## Changelog` section at the bottom of the `.agent.md` file.
