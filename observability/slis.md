# SLIs (Service Level Indicators)

The raw metrics that feed `slos.md`.

## Format
| Indicator | Source | Query | Owner |
|---|---|---|---|
| HTTP success rate | Prometheus | `sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` | platform |
| p95 latency | Prometheus | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` | platform |
| Job completion rate | DB | `select count(*) filter (where status='done') / count(*) from jobs where created_at > now() - interval '1 hour'` | data |

_Add rows as services come online._
