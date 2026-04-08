---
name: design-eval
description: Design an LLM evaluation harness — dataset, rubric, pass threshold
---

# Design Eval

> For any AI/LLM feature in a PRD. Mirror the Nine-Organ pattern at `C:\Users\dimos\SelfImproveSkill\evals\`.

## Procedure
1. **Dataset:** Create `quality/evals/datasets/<feature>/` with at least 32 examples (mirrors Nine-Organ standard). Each example is a JSON file with `input`, `expected_output`, `notes`.
2. **Rubric:** Create `quality/evals/rubrics/<feature>.md` with a 10-criterion binary rubric (C1–C10). Each criterion is a yes/no check that can be scored programmatically or by an LLM judge.
3. **Pass threshold:** Define in the rubric. Default: 90% of criteria pass on 90% of examples.
4. **Generator:** If using mock outputs for development, create `scripts/generators/<feature>.py` (mirrors `C:\Users\dimos\SelfImproveSkill\src\generators\`).
5. **Wire to PRD:** Update PRD frontmatter `links.eval` to point to the rubric.

## Why 32 examples
Matches the Nine-Organ golden dataset size. Big enough for statistical signal, small enough to hand-curate.

## Reuse
For PM-framework skills, do **not** create a new eval — point to `C:\Users\dimos\SelfImproveSkill\evals\<skill>` via `quality/self-improve/`.
