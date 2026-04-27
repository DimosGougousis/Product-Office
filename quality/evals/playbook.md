# Eval Playbook

How to design and run an LLM evaluation in this repo. Mirrors the pattern at `C:\Users\dimos\SelfImproveSkill\`.

## When You Need an Eval

Any feature where an LLM produces output that the user sees: PRD drafts, summaries, classifications, recommendations, code suggestions.

## Steps

### 1. Define the rubric

Create `rubrics/<feature>.md` with **10 binary criteria** (C1–C10). Each criterion is a yes/no check. Examples:

- C1: Output is valid JSON
- C2: Output references at least one source
- C3: Output stays under 500 tokens
- C4: Output matches the requested tone (per `writing-guide.md`)

### 2. Build the golden dataset

Create `datasets/<feature>/` with **32 examples**. Each example is a JSON file:

```json
{
  "id": "001",
  "input": "...",
  "expected_traits": ["..."],
  "notes": "edge case: empty input"
}
```

Cover: happy paths, edge cases, adversarial inputs, multilingual if relevant.

### 3. Build a generator (optional, for mock outputs)

Place at `scripts/generators/<feature>.py`. Used during development before the real model is wired up.

### 4. Build a judge (LLM-as-judge)

Either use a programmatic judge (regex/JSON validation) or an LLM judge that scores against the rubric. See `C:\Users\dimos\SelfImproveSkill\src\judge\` for the reference implementation.

### 5. Run

```bash
python scripts/run_eval.py --eval <feature> --version v1
```

Pass threshold default: **90% of criteria pass on 90% of examples**.

### 6. Record

Append to `results/YYYY-MM-DD-<feature>-vN.md` with pass rate, failures, and notes.

### 7. Optimize

If failing, iterate on the prompt and re-run. Use `run_optimize.py` from `SelfImproveSkill` if applicable. Track each version.

## For Nine-Organ PM-Framework Skills

**Do not duplicate.** Use `C:\Users\dimos\SelfImproveSkill\` directly:

```bash
cd C:\Users\dimos\SelfImproveSkill
python run_eval.py --skill office-hours --version v1
```

Symlink rubrics into `quality/self-improve/rubrics/` if you want one-place edits.
