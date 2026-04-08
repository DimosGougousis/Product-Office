---
name: run-eval
description: Execute an eval and append results to the run history
---

# Run Eval

## Procedure
1. **For Product Office evals** (in `quality/evals/`):
   ```bash
   python scripts/run_eval.py --eval <feature> --version <vN>
   ```
2. **For Nine-Organ PM-framework evals** (deferred to `SelfImproveSkill`):
   ```bash
   cd C:\Users\dimos\SelfImproveSkill
   python run_eval.py --skill <office-hours|plan-ceo-review|...> --version v1
   ```
3. **Append result** to `quality/evals/results/YYYY-MM-DD-<feature>-<version>.md`:
   ```markdown
   ---
   eval: <feature>
   version: <vN>
   date: YYYY-MM-DD
   pass_rate: NN%
   threshold: 90%
   status: pass | fail
   ---

   ## Results
   | Criterion | Pass | Fail | Notes |
   |---|---|---|---|

   ## Failures
   - Example <id>: <what failed>
   ```
4. **If failed:** open an issue tagged `eval-regression` and link to the failing examples. Block the related PR until fixed.
