---
name: yuup-intake
description: Screen a business-unit request for orchestration fit and emit a structured intake canvas with acceptance criteria, recommended roster, and dispatch graph
---

# /yuup-intake &lt;request&gt;

## Steps
1. Load `.claude/skills/yuup-intake.md` — the full intake procedure.
2. Load `.claude/agents/ROSTER.md` — to recommend specialists.
3. **Gate question** — does this genuinely need orchestration? If no, route to the appropriate single-agent command.
4. **Gather 8 dimensions** — ask at most 2 follow-up questions; fill the rest from context.
5. **Bridge to existing skills** — check `/office-hours`, `pl-funnel-intake`, EU AI Act risk class.
6. **Emit acceptance criteria** — 3-5 measurable ACs.
7. **Recommend roster + dispatch graph** — Mermaid diagram.
8. **Save canvas** → `pipeline/active/<run-id>/intake-canvas.md`.
9. **Hand off to `/yuup`** — if the canvas is complete, tell the user to run `/yuup "<objective>"`.
