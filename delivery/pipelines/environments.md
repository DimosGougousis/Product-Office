# Environments

| Env | URL | Owner | Data | Notes |
|---|---|---|---|---|
| dev | TBD | platform | synthetic | auto-deploy on `main` |
| staging | TBD | platform | anonymized prod | manual promote |
| prod | TBD | platform | live customer data | tagged release only |

## Secrets
Stored in environment-specific secret managers — never in repo. See `governance/directives/approval-gates.md` for credential change approval.
