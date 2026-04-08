# Pipeline Folder

Per-initiative artifacts produced by the **Nine-Organ PM Framework** skills (deployed at `~/.claude/commands/`).

## The Pipeline
```
idea
  └─► /office-hours        → REQUIREMENTS.md
  └─► /plan-ceo-review     → MODE.md
  └─► /plan-eng-review     → ARCHITECTURE.md (+ .dot diagrams)
  └─► /gsd-plan            → PROJECT.md, ROADMAP.md, STATE.md
  └─► /gsd-execute         → code + AGENTS.md log + STATE.md updates
  └─► /gsd-review          → VALIDATION.md (requirement → test coverage)
```
`/pm-status` is read-only and callable any time — it summarizes all `active/*/STATE.md`.

## Doc Index
- `_template/` — Empty stubs for the 8 artifact files (REQUIREMENTS, MODE, ARCHITECTURE, PROJECT, ROADMAP, STATE, AGENTS, VALIDATION)
- `active/<name>/` — One folder per in-flight initiative
- `archive/<name>/` — Completed initiatives

## Instructions for Claude
- When a user kicks off a new initiative, route to `/office-hours` first. Do not skip the interview.
- Each initiative gets its own folder under `active/`. Do not mix artifacts across initiatives.
- After `/gsd-review` produces `VALIDATION.md`, cross-check it against the corresponding `quality/acceptance-criteria/<feature>.md`. Any AC without a matching test is a release blocker.
- When complete, move the folder from `active/` to `archive/` in the same PR that closes the linked GitHub issue.
- The pipeline integrates with `agents/`: REQUIREMENTS.md often becomes the seed for `prd-creation` agent input; ROADMAP.md feeds the `workflow-automation` Kanban.
