---
name: new-agent
description: Scaffolding procedure for /new-agent — interview, generate, register a new YUUP subagent.
---

# New Agent — Scaffolding Skill

> Invoked by `/new-agent <name>`. Creates a new runnable subagent and registers it in YUUP's roster.

## Procedure

### 1. Validate
- `<name>` must be kebab-case, no spaces, ≤40 chars.
- Check that `.claude/agents/<name>.md` does not already exist. If it does, warn and abort.

### 2. Interview
Ask the user these questions — one at a time — using `AskUserQuestion`:

1. **Domain & Responsibilities** — what does this agent specialize in? (free text)
2. **When should YUUP dispatch it?** — what triggers this agent? What kind of objectives or sub-tasks? (free text)
3. **Tools Tier** — choose one:
   - `Full (read/write/terminal)` — can create/edit files, run commands
   - `Read + write docs` — can read files and write docs but not run code
   - `Read-only + web` — can read files and search the web but not edit
   - `Read-only` — search and read only
4. **Approval-Sensitive?** — does this agent's actions trigger approval gates (cost, destructive, external comms)? (Yes/No)
5. **Color & Emoji** — pick a color and emoji for the agent's frontmatter. Suggest defaults based on the domain.

### 3. Generate
- Copy `.claude/skills/agent-template.md`.
- Fill in the blanks from the interview answers.
- Write to `.claude/agents/<name>.md`.

### 4. Register
- Append a row to `.claude/agents/ROSTER.md` in the Active Roster table:
  ```
  | `<name>` | `<dispatch trigger>` | `<tools tier>` | `<Yes/No>` |
  ```
- Do not touch any other rows.

### 5. Report
- Confirm the file was created and the roster updated.
- Tell the user the agent is immediately available under YUUP's command — no restart, no reload needed.
- Example: `/yuup "<example objective that uses this agent>"`

## Anti-Patterns
- Skipping the interview and guessing defaults
- Creating an agent without appending to the roster (YUUP won't know it exists)
- Using the Copilot `applyTo:` format instead of the Claude Code `name`/`description` frontmatter
