---
name: yuup-intake
description: Front door for "a business unit wants orchestration" — gate question, 8 dimensions, emits acceptance criteria + recommended roster + dispatch graph
---

# YUUP Intake Skill — `/yuup-intake <request>`

> **Purpose:** Before a BU request reaches YUUP, this skill screens for orchestration fit, gathers the intake canvas, and emits structured acceptance criteria that Phase 1 critique will consume.

## Procedure

### 1. Gate Question — Is This Really Orchestration?
Ask **one** question first: "Does this genuinely need *multiple agents coordinating*, or can a single agent or script handle it?"

| If…                               | Then…                                                |
| --------------------------------- | ---------------------------------------------------- |
| Single agent can do it            | Route to the appropriate `/` command or skill. Stop. |
| A script can do it                | Route to `robot` with a simple task. Stop.           |
| Genuinely multi-step, multi-agent | Proceed to intake canvas.                            |

**YAGNI filter**: orchestration is expensive. Don't orchestrate what a good prompt can solve.

### 2. Intake Canvas — 8 Dimensions
Gather these dimensions, asking at most 2 follow-up questions to fill gaps:

| Dimension                                  | Questions to Answer                                                           |
| ------------------------------------------ | ----------------------------------------------------------------------------- |
| **1. Outcome & DoD**                       | What does "done" look like? What artifact or state change signals success?    |
| **2. Trigger & Cadence**                   | What kicks this off? One-time, daily, on-event? What volume?                  |
| **3. Decomposition**                       | What are the natural sub-tasks? Are they parallel or sequential?              |
| **4. Ground Truth & Data Sensitivity**     | Is there a "correct answer"? What data does it touch — public, internal, PII? |
| **5. Autonomy & Risk**                     | How much can it do unattended? What's the cost-of-wrong?                      |
| **6. Accuracy Bar & Cost-of-Wrong**        | What pass rate is acceptable? 90%? 99%? What breaks if it's wrong?            |
| **7. Existing Process & SMEs**             | Is there a current manual process? Who knows it best? Who reviews output?     |
| **8. Success Metrics, Budget & Ownership** | Who owns this? What's the budget? How do we measure success in 30/90 days?    |

### 3. Bridge to Existing Intake Skills
Reuse, don't reinvent:
- **`/office-hours`** — If this is a *product feature* idea that needs validation, route there first.
- **`pl-funnel-intake`** (Box 7 Change Readiness, Box 8 Data Readiness) — If this touches workforce transformation or data pipelines, incorporate those dimensions.
- **EU AI Act risk class** — If autonomy is high and cost-of-wrong is significant, assess risk class.

### 4. Emit Acceptance Criteria
From the canvas, derive 3-5 measurable acceptance criteria. These are what Phase 1 YUUP passes to `critique` at every review:

**Format:**
```
AC1: <measurable criterion> — measured by <metric>
AC2: <measurable criterion> — measured by <metric>
...
```

**Examples:**
- AC1: Research report covers ≥4 of 5 requested areas — measured by critique completeness score ≥80
- AC2: Architecture specifies all 6 layers with component interfaces — measured by critique correctness score ≥80
- AC3: No single dispatch exceeds 4 tool calls — measured by run trace cost field
- AC4: All findings cite ≥2 sources — measured by critique evidence score ≥70

### 5. Recommend Roster + Dispatch Graph
From the decomposition, recommend:
- **Which specialists** from `ROSTER.md` (the 4 active ones: `robot`, `research`, `process-designer`, `critique`)
- **Dispatch order** — parallel groups and sequential chains
- **Any missing specialist** — if the BU's need doesn't map to the existing roster, flag it

### 6. Output — Structured Canvas

Emit the complete intake canvas as a markdown file saved to `pipeline/active/<run-id>/intake-canvas.md`:

```markdown
# Intake Canvas — <Request Name>

## Gate Result
- **Orchestration needed?**: YES / NO
- **Reasoning**: <1 sentence>

## 8 Dimensions
| #   | Dimension                           | Finding |
| --- | ----------------------------------- | ------- |
| 1   | Outcome & DoD                       | ...     |
| 2   | Trigger & Cadence                   | ...     |
| 3   | Decomposition                       | ...     |
| 4   | Ground Truth & Data Sensitivity     | ...     |
| 5   | Autonomy & Risk                     | ...     |
| 6   | Accuracy Bar & Cost-of-Wrong        | ...     |
| 7   | Existing Process & SMEs             | ...     |
| 8   | Success Metrics, Budget & Ownership | ...     |

## Acceptance Criteria
- AC1: ... — measured by ...
- AC2: ... — measured by ...

## Recommended Roster
- Specialist: `<name>` — task: `<description>` — [parallel | sequential after <task>]
- Specialist: `<name>` — task: `<description>` — [parallel | sequential after <task>]

## Dispatch Graph
\```mermaid
graph TD
    ...
\```

## Bridge
- `/office-hours` needed: YES / NO
- `pl-funnel-intake` needed: YES / NO
- EU AI Act risk class: <class>

## Ready for YUUP
<YES / NO — if YES, the canvas is complete and YUUP can proceed to `/yuup <objective>`>
```
