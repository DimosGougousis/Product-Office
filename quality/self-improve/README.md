# Self-Improve Bridge

This folder is a **pointer**, not a fork. The Nine-Organ PM Framework — 7 skills, 7 rubrics, 7 golden datasets (32 examples each = 224), 7 generators, 70 tests, 159 total passing — lives at:

```
C:\Users\dimos\SelfImproveSkill\
```

## Available Skills (deployed at `~/.claude/commands/`)
| Skill | Layer | Purpose |
|---|---|---|
| `/office-hours` | Gstack | Falsifiable requirements interview |
| `/plan-ceo-review` | Gstack | 4-dimension scoring → MODE assignment |
| `/plan-eng-review` | Gstack | Architecture lock + DOT diagrams |
| `/gsd-plan` | GSD | Phase-isolated planning + Nyquist gate |
| `/gsd-execute` | GSD | Subagent orchestration with TDD |
| `/gsd-review` | GSD | Requirement → test coverage map |
| `/pm-status` | Cross | Read-only dashboard |

## Run a baseline eval
```bash
cd C:\Users\dimos\SelfImproveSkill
python run_eval.py --skill office-hours --version v1
```

## Optimize a skill
```bash
python run_optimize.py --skill office-hours --target 0.90
```

## Deploy
```bash
python run_deploy.py --skill office-hours
```
(Re-installs to `~/.claude/commands/`.)

## Why a Bridge, Not a Copy
Single source of truth. The Product Office repo focuses on **artifacts** (PRDs, ACs, plans, reports). The SelfImproveSkill repo owns the **skills + eval infrastructure**. They compose: skills write artifacts here; this repo's CI validates the artifacts.

## Optional: Symlink Rubrics
On Windows (PowerShell as admin):
```powershell
New-Item -ItemType SymbolicLink -Path "C:\Users\dimos\Product Office\quality\self-improve\rubrics" -Target "C:\Users\dimos\SelfImproveSkill\evals\rubrics"
```
This way, editing a rubric in either location updates both.
