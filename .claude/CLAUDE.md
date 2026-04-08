# .claude Folder

Skills and slash commands **specific to this Product Office repo**. Globally-deployed skills (the Nine-Organ pipeline) live in `~/.claude/commands/` and are not duplicated here.

## Skills (`.claude/skills/`)
| Skill | Purpose |
|---|---|
| `writing-guide.md` | Tone, formatting rules, "10x" examples |
| `draft-prd.md` | Standardized PRD drafting procedure (one-pager → Shape Up) |
| `verify-prd.md` | Self-check: every feature → metric + AC + SLO |
| `ask-user-workflow.md` | Forces AskUserQuestion before drafting |
| `summarize-user-interview.md` | Extract themes from raw interviews |
| `weekly-status-report.md` | Compose the weekly digest |
| `competitive-teardown.md` | Structured competitor analysis |
| `write-acceptance-criteria.md` | Gherkin scenario authoring |
| `design-eval.md` | Design an LLM eval (dataset + rubric + threshold) |
| `run-eval.md` | Execute eval and append results |
| `triage-incident.md` | Open incident timeline + RCA |
| `release-readiness-check.md` | Pre-release gate |

## Commands (`.claude/commands/`)
| Command | Action |
|---|---|
| `/new-prd <name>` | Branch + scaffold PRD from template |
| `/new-feature <name>` | PRD + AC + metric stub + SLO stub in one shot |
| `/weekly-report` | Generate weekly digest |
| `/review-prd <name>` | Run verify-prd against an active PRD |
| `/release-check` | Run release-readiness-check |
| `/incident <name>` | Open incident timeline |
| `/eval-run <name>` | Execute eval and write results |

## Plans
`.claude/plans/` archives saved plan files from complex past tasks (one per significant initiative).
