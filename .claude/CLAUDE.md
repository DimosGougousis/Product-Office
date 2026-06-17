# .claude Folder

Skills and slash commands **specific to this Product Office repo**. Globally-deployed skills (the Nine-Organ pipeline) live in `~/.claude/commands/` and are not duplicated here.

## Skills (`.claude/skills/`)

| Skill                          | Purpose                                                                  |
| ------------------------------ | ------------------------------------------------------------------------ |
| `writing-guide.md`             | Tone, formatting rules, "10x" examples                                   |
| `draft-prd.md`                 | Standardized PRD drafting procedure (one-pager → Shape Up)               |
| `verify-prd.md`                | Self-check: every feature → metric + AC + SLO                            |
| `ask-user-workflow.md`         | Forces AskUserQuestion before drafting                                   |
| `summarize-user-interview.md`  | Extract themes from raw interviews                                       |
| `weekly-status-report.md`      | Compose the weekly digest                                                |
| `competitive-teardown.md`      | Structured competitor analysis                                           |
| `write-acceptance-criteria.md` | Gherkin scenario authoring                                               |
| `design-eval.md`               | Design an LLM eval (dataset + rubric + threshold)                        |
| `run-eval.md`                  | Execute eval and append results                                          |
| `triage-incident.md`           | Open incident timeline + RCA                                             |
| `release-readiness-check.md`   | Pre-release gate                                                         |
| `yuup-orchestration.md`        | YUUP's operating procedure — plan, dispatch, critique, gate, synthesize  |
| `new-agent.md`                 | Scaffolding procedure for `/new-agent` — interview → generate → register |
| `agent-template.md`            | Claude Code subagent template for `/new-agent`                           |
| `yuup-intake.md`               | Screen a BU request for orchestration fit → intake canvas + acceptance criteria |

## Commands (`.claude/commands/`)

| Command               | Action                                                     |
| --------------------- | ---------------------------------------------------------- |
| `/new-prd <name>`     | Branch + scaffold PRD from template                        |
| `/new-feature <name>` | PRD + AC + metric stub + SLO stub in one shot              |
| `/weekly-report`      | Generate weekly digest                                     |
| `/review-prd <name>`  | Run verify-prd against an active PRD                       |
| `/release-check`      | Run release-readiness-check                                |
| `/incident <name>`    | Open incident timeline                                     |
| `/eval-run <name>`    | Execute eval and write results                             |
| `/yuup <objective>`   | Launch the YUUP agent orchestrator with an objective       |
| `/new-agent <name>`   | Scaffold a new YUUP subagent and register it in the roster |
| `/yuup-intake <request>` | Screen a BU request for orchestration fit → intake canvas + roster |

## Agent Runtime (`.claude/agents/`)

YUUP commands a roster of runnable subagents (Claude Code format, dispatched via the `runSubagent` tool). These are distinct from the persona specs in `agents/`.

| Agent              | Dispatch Trigger                                                   |
| ------------------ | ------------------------------------------------------------------ |
| `robot`            | Automation, scripting, MCP wiring, CI hooks, integration build     |
| `research`         | Research, competitive intel, codebase archaeology, tool comparison |
| `process-designer` | SOPs, directives, RACI, checklists, workflow design                |
| `critique`         | Review deliverables, quality gate, adversarial QA                  |
| `yuup`             | Orchestration identity — actual orchestration runs via `/yuup`     |

See `.claude/agents/ROSTER.md` for the full command registry and bridge to the existing 11 persona agents.

## Plans

`.claude/plans/` archives saved plan files from complex past tasks (one per significant initiative).
