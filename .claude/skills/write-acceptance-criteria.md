---
name: write-acceptance-criteria
description: Author Gherkin acceptance criteria for a PRD requirement
---

# Write Acceptance Criteria

## Format (Gherkin)
```gherkin
Feature: <feature name>

  Scenario: <happy path or edge case>
    Given <precondition>
    And <another precondition>
    When <action>
    Then <observable outcome>
    And <secondary outcome>
```

## Procedure
1. Read the PRD at `product/prds/active/<feature>/`.
2. For each requirement in the PRD, write at least one happy-path scenario and one edge-case scenario.
3. Save to `quality/acceptance-criteria/<feature>.md`.
4. Update the PRD frontmatter `links.acceptance_criteria` to point here.
5. After implementation, `/gsd-review` cross-checks each scenario against an actual test in `engineering/`. Any AC without a corresponding test is a release blocker.

## Quality Bar
- Each scenario is **observable from outside the system** — no implementation details.
- One scenario = one assertion of value, not a script.
- Edge cases include: invalid input, permission denied, network failure, empty state.
