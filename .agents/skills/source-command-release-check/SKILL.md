---
name: "source-command-release-check"
description: "Run the release readiness checklist"
---

# source-command-release-check

Use this skill when the user asks to run the migrated source command `release-check`.

## Command Template

# /release-check [tag-or-branch]

Invokes `.Codex/skills/release-readiness-check.md`. Reports pass/fail per checklist item. Blocks if any required item fails.
