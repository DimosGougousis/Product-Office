# Definition of Done

A change is "done" only when **all** of the following are true:

## Code
- [ ] Implements the linked PRD requirements
- [ ] Has unit tests covering happy path + at least one edge case
- [ ] Has integration test if it crosses a service boundary
- [ ] Passes all CI checks (`validate-docs.yml` + any test workflow)
- [ ] Code-reviewed by at least one other person
- [ ] No new lint warnings
- [ ] No TODO/FIXME without a linked issue

## Acceptance Criteria
- [ ] Every Gherkin scenario in `quality/acceptance-criteria/<feature>.md` has a passing test
- [ ] `/gsd-review` produced `VALIDATION.md` with full coverage

## Documentation
- [ ] PRD updated to `status: shipped`
- [ ] User-facing changelog entry in `delivery/releases/`
- [ ] Runbook updated if operational behavior changed
- [ ] Architecture diagram updated if system topology changed

## Observability
- [ ] Logs at appropriate level with required structured fields
- [ ] New metric instrumented if PRD defined one
- [ ] SLO impact recorded in `observability/slos.md`
- [ ] Alert added or tuned if user-facing failure mode is new

## Release
- [ ] Release notes drafted
- [ ] Stakeholders notified
- [ ] On-call briefed
- [ ] Rollback plan documented
