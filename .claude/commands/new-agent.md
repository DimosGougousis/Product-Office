---
name: new-agent
description: Scaffold a new YUUP subagent and register it in the roster
---

# /new-agent &lt;name&gt;

## Steps
1. Validate `<name>` is kebab-case, no spaces, ≤40 chars.
2. Check `.claude/agents/<name>.md` does not already exist. If it does, warn and abort.
3. Invoke `.claude/skills/new-agent.md` — interview the user (domain, dispatch triggers, tools tier, approval sensitivity, color/emoji).
4. Generate `.claude/agents/<name>.md` from `.claude/skills/agent-template.md` with the interview answers.
5. Append a row to `.claude/agents/ROSTER.md` in the Active Roster table.
6. Report: the agent file path + roster row — immediately available under YUUP.
