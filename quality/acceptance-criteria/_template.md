---
feature: <feature-name>
prd: product/prds/active/<feature-name>/PRD-Summary.md
owner: <pm>
status: draft
---

# Acceptance Criteria — <Feature Name>

> One Gherkin scenario per requirement. Edge cases included. Each scenario must map to a test in `engineering/` after `/gsd-execute`.

## Feature: <name>

### Scenario: Happy path
```gherkin
Given <precondition>
And <another precondition>
When <user action>
Then <observable outcome>
And <secondary outcome>
```

### Scenario: Invalid input
```gherkin
Given <precondition>
When <user provides invalid input>
Then <system rejects with clear message>
And <state is unchanged>
```

### Scenario: Permission denied
```gherkin
Given <user without permission>
When <attempts action>
Then <403 / clear error>
And <audit log entry created>
```

### Scenario: Empty state
```gherkin
Given <no data>
When <user views feature>
Then <empty-state UI shown>
And <CTA to create first item visible>
```

## Coverage Map (filled by `/gsd-review`)
| Scenario | Test File | Status |
|---|---|---|
| Happy path | tests/<feature>_test.py::test_happy | TBD |
| Invalid input | | |
| Permission denied | | |
| Empty state | | |
