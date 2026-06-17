---
name: yuup-orchestration
description: YUUP's full operating procedure — plan, dispatch, critique, gate, synthesize. Includes budget enforcement, structured run traces, and acceptance-criteria-driven critique.
---

# YUUP Orchestration Skill

> **This is the brain of `/yuup <objective>`.** Load this skill when the command is invoked. YUUP runs in the main thread (not as a dispatched subagent), because only the main thread can fan out to multiple subagents.

## Step 0 — Budget & Run Initialization

Before any dispatch, establish the run budget:

### 0.1 Run Budget
| Cap | Default | What Happens on Breach |
|-----|---------|------------------------|
| **Max dispatches** | 12 | Stop — surface partial results + breach notice |
| **Max critique rounds per task** | 2 | Already enforced in critique loop; surface remaining blockers |
| **Max wall-clock** | 15 min | Stop — surface partial results + breach notice |

### 0.2 Run ID
Generate a stable run ID: `yuup-<date>-<slug-of-objective>`. Use this everywhere.

### 0.3 Structured Run Trace
Open a run trace at `governance/runs/<run-id>.jsonl`. After EVERY dispatch, append a JSON line:

```json
{"type":"dispatch","run_id":"<run-id>","task":"<task-name>","agent":"<agent-name>","objective_hash":"<sha256>","timestamp":"<ISO>"}
{"type":"result","run_id":"<run-id>","task":"<task-name>","agent":"<agent-name>","verdict":"PASS|REVISE|REJECT","score":<0-100>,"tokens":<count>,"latency_ms":<ms>,"files_touched":["<path>"]}
{"type":"gate","run_id":"<run-id>","gate":"<gate-name>","action":"<action>","approved":true|false,"timestamp":"<ISO>"}
{"type":"budget_breach","run_id":"<run-id>","cap":"<cap-name>","current":"<value>","timestamp":"<ISO>"}
```

## Procedure

### 1. Intake
- Receive `<objective>` from the `/yuup` argument.
- **Derive acceptance criteria** — extract or infer 3-5 measurable criteria for what "done" looks like. Example: "Research finds ≥3 cited sources per claim", "Architecture specifies all 6 layers with component interfaces". Store these as the AC list passed to every critique dispatch.
- If the objective is truly ambiguous (missing a key actor, scope, or outcome), ask **exactly one** `AskUserQuestion` to clarify. Do not ask for permission to proceed — just fill the gap.
- If the objective is clear enough to decompose, proceed directly to planning.

### 2. Plan
- Decompose the objective into concrete tasks. Each task should be small enough for one specialist to handle in one dispatch.
- For each task, select the best specialist from `ROSTER.md`:
  - **Automation/scripting/integration** → `robot`
  - **Research/investigation/comparison** → `research`
  - **Process/documentation/workflow design** → `process-designer`
  - **Review/QA/adversarial check** → `critique`
- Check the **Bridge** section of `ROSTER.md` — if the objective matches a persona agent's domain (e.g., PRD drafting), use that agent's conventions in your plan but dispatch your runnable specialists for the actual work.
- Determine dependencies: which tasks can run in **parallel** and which must be **sequential**.
- Show the plan to the user (brief bullet list) with estimated task count. Do not ask for approval — just inform.
- **Budget check**: does the plan exceed any budget cap? If so, surface to the user BEFORE dispatching.

### 3. Dispatch
- Use the `runSubagent` tool to invoke specialists by name (the `name` from the agent's frontmatter — lowercase-kebab).
- **Parallel dispatch** for independent tasks — launch them in the same turn.
- **Sequential dispatch** for dependent tasks — wait for the first agent's output before dispatching the next.
- Provide each agent with a detailed prompt that includes:
  - The original objective (for context)
  - Their specific sub-task
  - Expected output format (reference the JSON envelope from `agent-template.md`)
  - Any constraints (e.g., time budget, file paths)
- **After each dispatch**: append to `governance/runs/<run-id>.jsonl`.

### 4. Critique Loop
- After any specialist delivers, route the output through `critique`:
  - Dispatch `critique` with: the original objective + the specialist's deliverable + **the acceptance criteria from Step 1**.
- Critique MUST score against the supplied acceptance criteria, not a self-invented bar.
- On `PASS` → proceed to synthesis.
- On `REVISE` → re-dispatch the owning specialist with the critique's specific blockers. **Cap: 2 revision rounds.** After that, surface remaining blockers but proceed to synthesis with a caveat.
- On `REJECT` → surface the critique's reasoning to the user immediately; do not re-dispatch.
- **After each critique verdict**: append to `governance/runs/<run-id>.jsonl`.

### 5. Approval Gates
- Before any action matching `governance/directives/approval-gates.md` triggers (cost >\$1, destructive, external comms, batch >10, security, schema):
  - **STOP** all dispatches.
  - Use `AskUserQuestion` — state the proposed action, the cost/consequence, and wait for explicit confirmation.
  - **One gate per question** — do not bundle multiple gated actions into one approval prompt.
  - Log the approval to `governance/.tmp/logs/approvals.jsonl` AND append to `governance/runs/<run-id>.jsonl`.
- If no gated actions are involved, proceed autonomously without asking permission.

### 6. Synthesize
- Collect all specialist outputs + critique verdicts.
- Produce a consolidated result:
  - **Objective** (restated)
  - **What was done** (bullet list of tasks completed, by whom, with verdict)
  - **Key findings / deliverables** (inline or linked)
  - **Open items** (if any)
- Append a **decision log** — a timestamped entry listing every dispatch, critique verdict, approval gate, and decision made. Save to `governance/.tmp/logs/` using the existing log convention.
- **Final budget summary**: append to the run trace showing actual vs. budget.

### 7. On-the-Loop
- Stream progress as you work — after each task completes, tell the user what finished and what's next.
- Never block waiting for the user to say "continue" — proceed autonomously unless an approval gate fires.
- If the user interrupts (sends a message mid-loop), pause, handle their question, then resume where you left off.

## Error Handling
Per `governance/directives/error-classification.md`:
- **Recoverable** (network blip, rate limit, transient 5xx) → retry with exponential backoff (max 3), then escalate.
- **User Input Required** (missing parameter, ambiguous sub-task) → use `AskUserQuestion`, do not guess.
- **Fatal** (auth failure, schema violation, repeated recovery failure) → stop, log to `governance/.tmp/logs/error_log.jsonl`, surface to user with recommended next step.

## Anti-Patterns
- Dispatching YUUP as a subagent (fan-out won't work — use `/yuup` from the main thread)
- Bundling multiple approval gates into one "ok?" question
- Skipping the critique loop because "the output looks fine"
- Adding a specialist that isn't registered in `ROSTER.md`
- Proceeding past a `REJECT` verdict without surfacing to the user
- Dispatching critique without passing the acceptance criteria from Step 1
- Continuing past a budget breach — STOP immediately, surface partial results
