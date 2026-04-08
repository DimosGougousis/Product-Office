---
name: summarize-user-interview
description: Extract themes, quotes, and jobs-to-be-done from raw user interview transcripts
---

# Summarize User Interview

## Inputs
- Raw transcript or notes file in `product/discovery/interviews/`

## Output
A structured summary in `product/discovery/insights/<interviewee-or-theme>.md`:

```markdown
---
interviewee: <pseudonym>
date: YYYY-MM-DD
interviewer: <pm>
segment: <user-segment>
---

# Interview Summary — <Pseudonym>

## Jobs To Be Done
- When ___, I want to ___, so I can ___

## Pains (verbatim quotes)
> "..."

## Gains (verbatim quotes)
> "..."

## Workarounds Observed
-

## Surprises
-

## Implications for Roadmap
-

## Linked PRDs
-
```

## Procedure
1. Read the transcript end-to-end before extracting.
2. Pull verbatim quotes — do not paraphrase pains and gains.
3. Tag each insight with the user segment.
4. Cross-link to any active PRDs the insight informs.
