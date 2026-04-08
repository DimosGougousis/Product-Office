# Branch Strategy

## Branches
- **`main`** — protected, always deployable. Squash merges only.
- **`feature/<area>-<short-name>`** — new PRDs, features, agents
- **`docs/<topic>`** — pure documentation changes
- **`fix/<short-name>`** — bug fixes
- **`hotfix/<short-name>`** — urgent prod fixes (allowed to merge faster)
- **`release/<version>`** — release candidates

## Naming Examples
- `feature/prd-payment-redesign`
- `feature/agent-stakeholder-intel-v2`
- `docs/weekly-2026-04-08`
- `fix/kanban-state-race`
- `hotfix/billing-webhook-500`

## Protection Rules (configured on GitHub)
- Require PR + 1 approving review
- Require status check `validate-docs` to pass
- Require branches up to date
- Disallow force pushes to `main`
- Disallow deletion of `main`

## Merge Strategy
**Squash and merge** for everything. Keeps `main` linear and PR titles meaningful. Use Conventional Commits in PR titles: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
