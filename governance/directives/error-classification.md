# Error Classification Directive

Per the governance framework, every error encountered by an agent must be classified into one of three categories:

## Recoverable
- Network blip, rate limit, transient 5xx
- **Action:** Retry with exponential backoff (max 3 attempts), then escalate
- **Logging:** WARN level

## User Input Required
- Missing parameter, ambiguous request, approval gate triggered
- **Action:** Use `AskUserQuestion` to gather what's needed; do not guess
- **Logging:** INFO level

## Fatal
- Auth failure, schema violation, destructive op blocked, repeated recoverable failure
- **Action:** Stop, log full context to `governance/.tmp/logs/error_log.jsonl`, surface to user with recommended next step
- **Logging:** ERROR level

## Self-Annealing
On Fatal errors, the agent should propose an updated directive (a "lesson learned") to prevent recurrence. Save proposals as PRs against `governance/directives/`.
