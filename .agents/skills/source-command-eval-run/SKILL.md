---
name: "source-command-eval-run"
description: "Execute an eval and write results"
---

# source-command-eval-run

Use this skill when the user asks to run the migrated source command `eval-run`.

## Command Template

# /eval-run <eval-name> [--version vN]

Invokes `.Codex/skills/run-eval.md`. For Product Office evals: `python scripts/run_eval.py --eval <name> --version <vN>`. For Nine-Organ skills: defers to `C:\Users\dimos\SelfImproveSkill\run_eval.py`. Results land in `quality/evals/results/`.
