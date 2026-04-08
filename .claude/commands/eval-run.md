---
name: eval-run
description: Execute an eval and write results
---

# /eval-run <eval-name> [--version vN]

Invokes `.claude/skills/run-eval.md`. For Product Office evals: `python scripts/run_eval.py --eval <name> --version <vN>`. For Nine-Organ skills: defers to `C:\Users\dimos\SelfImproveSkill\run_eval.py`. Results land in `quality/evals/results/`.
