# Quality Folder

Acceptance criteria, Definition of Done/Ready, test strategy, AI/LLM evaluation harness.

## Doc Index
- `acceptance-criteria/_template.md` — Gherkin Given/When/Then template
- `acceptance-criteria/<feature>.md` — One AC doc per PRD; the PRD must link here
- `definition-of-done.md` — Org-wide DoD
- `definition-of-ready.md` — Sprint readiness checklist
- `test-strategy.md` — Unit / integration / e2e / manual split
- `evals/playbook.md` — How to design and run an LLM eval
- `evals/datasets/` — Golden test sets
- `evals/rubrics/` — Scoring criteria (10-criterion binary, like the Nine-Organ rubrics)
- `evals/results/` — Date-stamped run history
- `uat/` — User acceptance testing logs
- `self-improve/README.md` — How to invoke `run_eval.py` against `C:\Users\dimos\SelfImproveSkill\` for the 7 PM-framework skills

## Instructions for Claude
- Every PRD requirement must map to at least one Gherkin scenario in `acceptance-criteria/<feature>.md`.
- For AI/LLM features, design an eval before shipping: dataset + rubric + pass threshold in `evals/`.
- The `verify-prd` skill enforces that every PRD links to an AC file before merge.
- For the Nine-Organ skills, baseline evals run from `C:\Users\dimos\SelfImproveSkill\` (159 tests). Local rubrics in `self-improve/rubrics/` are pointers/copies — don't fork them.
