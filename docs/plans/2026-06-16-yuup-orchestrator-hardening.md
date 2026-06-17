---
title: YUUP Agent Orchestrator — Hardening & Build Plan
status: executed (Phases 0-5 complete as of 2026-06-16)
owner: Dimos Gougousis
created: 2026-06-16
branch: fix/md056-framework-tables
---

# YUUP Agent Orchestrator — Hardening & Build Plan

## Context

You built a first cut of **YUUP**, a main-thread agent orchestrator that dispatches runnable
specialist subagents (`robot`, `research`, `process-designer`, `critique`) from
`.claude/agents/`, runs a critique loop, honors approval gates, and synthesizes a result.
A code review found the design sound but the runnable agents **won't dispatch as written**
(non-standard frontmatter, a fictional tool name, name mismatches). Separately, the *harness*
— the reliability scaffolding that lets YUUP run accurately and unattended — is thin: agents
hand off freeform prose, tools aren't scoped, there's no durable trace, no budget ceiling, and
no evals.

This plan fixes the blockers **and** layers in every recommendation from the harness
brainstorm, in phases. Each phase is independently reviewable and shippable: you approve what
it builds, why, and the value YUUP gains before we start it.

**Goal:** a multiagent orchestrator that is correct the first time, cheap to run, safe to leave
on the loop, and improvable without fear — plus a reusable intake playbook for the next time a
business unit asks for orchestration.

## Guiding principles (apply to every phase)

- **Remove judgment from the seams.** Every contract, schema, and script replaces a place
  where the orchestrator could drift. Determinism beats cleverness.
- **Least privilege.** An agent that can't do a thing can't do it wrong.
- **Evidence before claims.** The Iron Law applies to YUUP itself: no "done" without proof.
- **Orthogonal, minimal roster.** One crisp mandate per agent; add agents only on a real gap.
- **Reuse what exists.** `approval-gates.md`, `error-classification.md`, `office-hours`,
  `pl-funnel-intake`, `quality/evals/` — wire in, don't reinvent.

## Recommendation → Phase map

| Item                                            | Phase |
| ----------------------------------------------- | ----- |
| Fix: frontmatter schema (`description`/`tools`) | 0     |
| Fix: `runSubagent` → real dispatch tool         | 0     |
| Fix: kebab `name` matching dispatch id          | 0     |
| Verify subagents actually dispatch              | 0     |
| Typed handoff contracts                         | 1     |
| Least-privilege tool scoping                    | 1     |
| Acceptance-criteria-driven critique             | 1     |
| Durable structured run trace                    | 1     |
| Global budget + circuit breaker                 | 1     |
| Shared artifact workspace (blackboard)          | 2     |
| Run IDs + idempotent/resumable runs             | 2     |
| Deterministic offloading (Layer 3 scripts)      | 2     |
| Intake canvas + gate question                   | 3     |
| Acceptance criteria captured at intake          | 3     |
| Eval golden set                                 | 4     |
| Model-tier routing                              | 4     |
| Observability dashboard / run ledger            | 4     |
| Scheduled / unattended runs                     | 5     |
| Reusable orchestration playbook                 | 5     |

---

## Phase 0 — Make it actually run (Critical fixes)

**What:** Fix the three blocking bugs and prove the runtime works.
- Rewrite all six `.claude/agents/*.md` frontmatter to the real Claude Code subagent schema:
  `name` (lowercase-kebab, matching filename + roster), `description` (the dispatch trigger —
  required), `tools` (scoped — see Phase 1 for the policy), optional `model`. Keep
  `color`/`emoji`/`vibe` only if the harness tolerates extra keys; otherwise move them into
  the body.
- Replace every `runSubagent` reference with the actual dispatch tool name (`Task`/`Agent`,
  confirmed against your CC version) in `yuup-orchestration.md`, `commands/yuup.md`,
  `agent-orchestration.md`, `.claude/CLAUDE.md`.
- Align dispatch identifiers everywhere (`robot`, `research`, `process-designer`, `critique`).

**Why:** Until these are fixed, "runnable subagents" is aspirational — the agents either don't
register or can't be invoked by name.

**Value to YUUP:** It dispatches. This is the precondition for everything else.

**Files:** all `.claude/agents/*.md`, `.claude/skills/yuup-orchestration.md`,
`.claude/commands/yuup.md`, `governance/directives/agent-orchestration.md`, `.claude/CLAUDE.md`.

**Verification (do this FIRST — the whole system hinges on it):**
1. Smoke test: dispatch `robot` with a trivial task; confirm it runs as the project subagent.
2. `/yuup "research X and design a process"` → confirm `research` then `process-designer`
   dispatch, output routes through `critique`, and a synthesized result returns.
3. Confirm a read-only agent (e.g., `research`) cannot write a file.

**Review checkpoint:** You confirm the agents dispatch and read-only scoping holds.

---

## Phase 1 — Reliability harness core

**What:** The accuracy/safety backbone.
- **Typed handoff contracts.** Every agent returns a structured envelope:
  `{ status, deliverable, evidence, confidence, open_questions, cost }`. Generalize Critique's
  existing verdict/score/issues pattern to all agents; encode it in `agent-template.md` so new
  agents inherit it.
- **Least-privilege tool scoping.** Per-agent `tools` policy: `research`/`critique` = read +
  search only; `process-designer` = read + write docs; `robot` = full. Enforced in frontmatter,
  not prose.
- **Acceptance-criteria-driven critique.** YUUP captures/derives acceptance criteria for the
  objective and passes them to `critique`, which scores against *them*, not a self-invented bar.
- **Durable structured run trace.** One structured record per dispatch
  (agent, input hash, verdict, tokens, latency, files touched) written to a committed
  `governance/runs/<run-id>.jsonl` (out of gitignored `.tmp/`).
- **Global budget + circuit breaker.** YUUP step 0 sets caps: max dispatches, max tokens, max
  wall-clock. Breach → stop and surface, don't limp on.

**Why:** Today YUUP relies on orchestrator judgment at every seam and has no spend ceiling or
audit trail. These make runs parseable, bounded, and objectively gradable.

**Value to YUUP:** Deterministic handoffs (higher accuracy), enforced safety boundaries,
bounded cost (efficiency), and a trace you can debug and later build evals on.

**Files:** all `.claude/agents/*.md` (tools + contract), `agent-template.md`,
`yuup-orchestration.md` (budget, criteria pass-through, trace write), `critique.md` (score vs.
supplied criteria), new `governance/runs/` convention.

**Verification:** Run an objective; confirm (a) each agent returns the envelope, (b) a
read-only agent is tool-blocked, (c) critique cites the supplied acceptance criteria,
(d) `governance/runs/<id>.jsonl` exists with one line per dispatch, (e) a deliberately
oversized objective trips the budget breaker.

**Review checkpoint:** You review one real run's trace + envelopes end-to-end.

---

## Phase 2 — Determinism & shared state

**What:**
- **Blackboard workspace.** Each run gets `pipeline/active/<run-id>/`; agents read/write
  artifacts there and pass *references*, not giant prompt blobs.
- **Run IDs + idempotency/resume.** Stable run IDs; re-running an objective resumes from the
  last good artifact instead of redoing work.
- **Deterministic offloading.** Move mechanical steps (link-checking, markdown lint, file
  moves, frontmatter validation, log appends) into Layer 3 scripts under `scripts/`, invoked by
  agents rather than done by judgment.

**Why:** Your own framework says push complexity into deterministic code (90%/step compounds to
59% over 5 steps). Prompt-stuffing context also bloats and loses work on long runs.

**Value to YUUP:** Higher accuracy (deterministic steps don't drift), lower token cost (refs
not blobs), and resumable runs (no wasted work on interruption).

**Files:** `yuup-orchestration.md` (workspace + resume logic), `scripts/` (new Layer 3 utils),
agent files (reference the scripts), `agent-orchestration.md` (document the pattern).

**Verification:** Interrupt a run mid-flight and re-invoke; confirm it resumes from artifacts.
Confirm a deterministic step (e.g., link-check) runs via script with exit-code evidence.

**Review checkpoint:** You see a resumed run and one offloaded deterministic step.

---

## Phase 3 — Intake canvas (designing orchestration for a business unit)

**What:** A front door for "a BU wants orchestration." A `/yuup-intake` flow (skill) that:
- **Gate question first:** is this genuinely decomposable / does it need orchestration at all?
  (YAGNI filter — single agent or script may win.)
- Gathers the eight intake dimensions: outcome & DoD; trigger & cadence/volume; decomposition;
  ground truth & data sensitivity; autonomy & risk/compliance; accuracy bar & cost-of-wrong;
  existing process & SMEs; success metrics, budget, ownership.
- **Emits the acceptance criteria** Phase 1's critique consumes, plus a recommended roster and
  dispatch graph.
- Reuses, not reinvents: bridges to `/office-hours` and `pl-funnel-intake` (Box 7 change-
  readiness, Box 8 data-readiness) and the EU AI Act risk-class skills.

**Why:** The quality of an orchestration is set at intake. Without it you encode the wrong
process and discover it late.

**Value to YUUP:** Every run starts from explicit outcomes, guardrails, and acceptance criteria
— the single biggest lever on first-time accuracy.

**Files:** new `.claude/skills/yuup-intake.md`, new `.claude/commands/yuup-intake.md`, links
from `agent-orchestration.md`; reuse existing intake skills.

**Verification:** Run `/yuup-intake` on a sample BU request; confirm it produces an intake
canvas + acceptance criteria + recommended roster, and routes simple requests away from
orchestration.

**Review checkpoint:** You review one generated intake canvas.

---

## Phase 4 — Evals, model routing & observability

**What:**
- **Eval golden set.** A handful of objectives in `quality/evals/` with expected routing +
  outcomes; a runner that replays them against the current agents and flags regressions.
- **Model-tier routing.** Strong model for YUUP + `critique` (judgment-heavy); cheaper/faster
  model for mechanical specialists. Set via `model:` frontmatter + orchestration policy.
- **Observability.** A simple read-only dashboard/report over `governance/runs/*.jsonl`
  (dispatches, verdicts, tokens, latency, pass-rate) so you can see drift over time.

**Why:** Evals are what let you change agents without fear; routing is the biggest efficiency
lever; observability turns the trace into insight.

**Value to YUUP:** Safe to evolve (regression-guarded), cheaper per run, and measurable.

**Files:** `quality/evals/yuup/` (datasets + rubric + runner), agent `model:` fields,
`yuup-orchestration.md` (routing policy), new report script/skill over `governance/runs/`.

**Verification:** Edit an agent prompt, run the eval set, confirm a regression is caught.
Confirm a mechanical specialist runs on the cheaper model. Generate the run report.

**Review checkpoint:** You review the eval results table + one run report.

---

## Phase 5 — Autonomy & reusable playbook (optional / fast-follow)

**What:**
- **Scheduled / unattended runs.** Wire a cadence (scheduled-tasks/cron) so YUUP fires on a
  schedule, runs within budget + gates, and pushes you results — true human-off-keyboard,
  still on-loop via notifications.
- **Reusable orchestration playbook.** Generalize everything above into a documented,
  repo-agnostic playbook: intake canvas → roster design → harness checklist → eval gate, so the
  *next* business-unit request follows the same proven path.

**Why:** Turns YUUP from one orchestrator into a repeatable capability.

**Value to YUUP:** Unattended operation + a standard way to stand up the next orchestration.

**Files:** scheduling config, `governance/directives/agent-orchestration.md` (autonomy section),
new `docs/playbooks/multiagent-orchestration.md`.

**Verification:** A scheduled dry-run fires, respects budget/gates, and notifies. Playbook
walked against a hypothetical new request.

**Review checkpoint:** You review the playbook + one scheduled dry-run.

---

## Out of scope (for now)
- Migrating the existing 11 persona agents (`agents/*.agent.md`) into runnable subagents — they
  stay as bridge/routing references.
- Swapping the native subagent runtime for an MCP swarm (`ruflo`) — noted as a future
  escalation only; native CC subagents are the reliable core.

## Sequencing & review flow
Phases are ordered by dependency: **0 → 1 → 2** are the spine (run, then reliable, then
deterministic). **3** can start in parallel with 2. **4** needs 1's trace. **5** is optional.
You approve each phase before it starts; each ends at a concrete verification + review
checkpoint above.
