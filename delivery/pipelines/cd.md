# CD

## Stages
| Stage | Trigger | Approval | Audience |
|---|---|---|---|
| dev | merge to `main` | none | internal |
| staging | tag `staging-*` | one approver | internal + select customers |
| prod | tag `v*.*.*` | two approvers + `/release-check` green | all |

## Promotion
- Same artifact promoted across stages — never rebuild per environment.
- Config differences live in env-specific files referenced in `delivery/pipelines/environments.md`.

## Rollback
Tag-based. Re-deploy the prior `v*.*.*` tag. See `delivery/runbooks/rollback.md`.
