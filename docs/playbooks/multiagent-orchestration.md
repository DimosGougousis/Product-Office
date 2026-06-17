# Multi-Agent Orchestration Playbook

> Reusable, repo-agnostic playbook for standing up multi-agent orchestration.
> Use this when a business unit asks "can we automate this with agents?"

## Phase A — Intake & Gate (1 hour)

1. Run the **Gate Question**: "Does this genuinely need *multiple agents coordinating*, or can a single agent or script handle it?"
   - If single agent: route to the appropriate slash command.
   - If script: dispatch `robot`.
   - If multi-agent: proceed.

2. Run `/yuup-intake <request>` — produces the intake canvas with 8 dimensions + acceptance criteria.

**Checkpoint:** Intake canvas saved. ACs defined. Gate passed.

## Phase B — Roster Design (2-4 hours)

3. Map the intake canvas decomposition to agents:
   - Research-heavy tasks → `research` (read-only)
   - Documentation/process tasks → `process-designer` (read + write docs)
   - Automation/scripting tasks → `robot` (full tools)
   - Review/QA → `critique` (read-only)

4. Design the dispatch graph:
   - Parallel tasks: same turn
   - Sequential tasks: one after another
   - Critique after every specialist deliverable

5. **Missing specialist check**: Does the roster cover all task types? If not, design a new specialist with `/new-agent <name>`.

**Checkpoint:** Roster mapped. Dispatch graph drawn.

## Phase C — Harness Checklist (1-2 hours)

6. Wire the intake ACs into the YUUP orchestration — critique scores against them, not generic criteria.

7. Set budget caps:
   - Max dispatches: 12
   - Max wall-clock: 15 min
   - Per-dispatch tool call budget: proportional to task complexity

8. Configure approval gates:
   - Review `approval-gates.md` — any task that touches cost > $1, destructive ops, external comms, batch > 10, security, or schema gets gated.

9. Create the run trace directory: `governance/runs/<run-id>.jsonl`

**Checkpoint:** ACs wired. Budget set. Gates configured. Trace ready.

## Phase D — Eval Gate (2-4 hours)

10. Build an eval golden set for this orchestration:
    - At least 3 objectives with expected routing + outcomes
    - Cover: success path, budget breach, rejection path, tool scoping path

11. Run the eval set:
    - Before first production use
    - After any agent prompt change
    - Weekly regression

12. Gate: eval pass rate ≥ 80% before production.

**Checkpoint:** Eval set created. First run passes.

## Phase E — Production & Observability (ongoing)

13. Run `/yuup "<objective>"` with the intake canvas as context.

14. Monitor via `governance/runs/<run-id>.jsonl`:
    - Per-dispatch verdicts and scores
    - Token usage and latency
    - Gate approvals
    - Budget breaches

15. Review after first 5 runs:
    - Agent accuracy (critique scores)
    - Routing accuracy (was the right agent chosen?)
    - Cost per run
    - User satisfaction

16. Iterate:
    - Prompt tweaks → re-run evals
    - New agent → re-run evals
    - New use case → new intake canvas

## Scheduling for Unattended Runs (Phase 5 — optional)

17. Wire a cron/Task Scheduler entry:
    - Fires `/yuup "<objective>"` on cadence
    - Respects budget caps (stops on breach)
    - Pushes results to Slack/email (triggers external comms gate)

18. Dry-run: let a scheduled run fire, respect budget, and notify. Review the trace.

## When NOT to Use Orchestration

- **Single well-scoped task** — one agent is enough.
- **Deterministic pipeline** — a script is more reliable and cheaper.
- **No acceptance criteria can be written** — if you can't define "done," orchestration can't produce it.
- **Cost-of-wrong is catastrophic** and autonomy is high — keep a human in the loop for every step.

## Files Created Per Orchestration

| Artifact      | Path                                          |
| ------------- | --------------------------------------------- |
| Intake canvas | `pipeline/active/<run-id>/intake-canvas.md`   |
| Run trace     | `governance/runs/<run-id>.jsonl`              |
| Decision log  | `governance/.tmp/logs/<run-id>.jsonl`         |
| Eval results  | `quality/evals/yuup/results/<timestamp>.json` |
