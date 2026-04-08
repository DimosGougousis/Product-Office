# Tracing

## Standard
OpenTelemetry. Propagate `traceparent` header on every cross-service call.

## Sampling
- Errors: 100%
- Slow requests (>p99): 100%
- Normal traffic: 1% baseline, increase per investigation

## Trace ID in Logs
Every log line must include `trace_id`. This is what stitches logs ↔ traces ↔ alerts together during an incident.
