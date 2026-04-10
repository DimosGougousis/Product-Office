# Test Strategy

## Layers

| Layer        | What                             | Tools                | Where                |
| ------------ | -------------------------------- | -------------------- | -------------------- |
| Unit         | Pure functions, single class     | (project-specific)   | next to source       |
| Integration  | Service + DB / external boundary | (project-specific)   | `tests/integration/` |
| End-to-end   | Full user flow                   | Playwright / Cypress | `tests/e2e/`         |
| Manual / UAT | Anything that needs a human      | checklist            | `quality/uat/`       |
| Eval         | LLM/AI feature quality           | rubric + dataset     | `quality/evals/`     |

## Pyramid

Most tests at unit layer, fewer at integration, fewest at e2e. UAT and evals are not on the pyramid — they gate releases.

## Coverage Target

- Unit: ≥80% line coverage on new code
- Integration: every external boundary touched in a PR has at least one test
- E2E: every Gherkin happy-path scenario from `quality/acceptance-criteria/`

## Mocking Rule

**Do not mock the database in integration tests.** Use a real test DB. (Reason: we got burned by mocked tests passing while real migrations failed.)

## Eval Rule

For AI/LLM features, eval pass rate ≥90% on the golden dataset is a release gate. See `quality/evals/playbook.md`.
