# Logging Standards

## Levels
- **ERROR** — something failed that needs attention
- **WARN** — unexpected but recoverable
- **INFO** — significant business event (not per-request noise)
- **DEBUG** — development only, off in prod

## Required Structured Fields
Every log line must be JSON with at minimum:
- `timestamp` (ISO 8601 UTC)
- `level`
- `service`
- `trace_id`
- `message`

## PII Rules
- **Never log:** passwords, tokens, full credit card numbers, SSNs, full email bodies, raw auth headers
- **Hash before logging:** email addresses (use SHA-256), user IDs in some contexts
- **Redact:** anything in a `secret`, `token`, `password`, `auth` field

## Retention
- Prod: 30 days hot, 1 year cold
- Staging: 7 days
- Dev: ephemeral
