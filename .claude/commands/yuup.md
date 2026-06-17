---
name: yuup
description: Launch the YUUP agent orchestrator with an objective — includes budget enforcement, structured run traces, and acceptance-criteria-driven critique
---

# /yuup &lt;objective&gt;

## Steps
0. **Budget & run init** — set budget caps (max 12 dispatches, 15 min wall-clock), generate run ID, open `governance/runs/<run-id>.jsonl`.
1. Load `.claude/skills/yuup-orchestration.md` — the full operating procedure.
2. Load `.claude/agents/ROSTER.md` — the current agent roster.
3. **Intake** the `<objective>` — derive acceptance criteria (3-5 measurable criteria), ask exactly **one** clarifying question if truly ambiguous.
4. **Plan** — decompose into tasks; show the plan (bullet list) to the user. Do not ask for approval. Check budget.
5. **Dispatch** specialists via the `runSubagent` tool — parallel for independent tasks, sequential for dependent ones. Append to `governance/runs/<run-id>.jsonl` after each.
6. **Critique loop** — route every deliverable through `critique` WITH the acceptance criteria from Step 3. On `REVISE`, re-dispatch up to 2 rounds. On `REJECT`, surface to the user.
7. **Approval gates** — before any action matching `governance/directives/approval-gates.md`, STOP and `AskUserQuestion`. One gate per question. Otherwise proceed autonomously.
8. **Synthesize** — consolidated result + decision log appended to `governance/.tmp/logs/`.
9. **Close run trace** — finalize `governance/runs/<run-id>.jsonl` with budget summary.
10. **Stream progress** throughout — the user is on the loop, never blocked except at gates.
