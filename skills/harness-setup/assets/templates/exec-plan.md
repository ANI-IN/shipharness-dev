# Exec plan: <feature id> <short title>

<!-- A living plan for one feature, kept in docs/exec-plans/active/ and moved to
docs/exec-plans/completed/ when the feature passes (A1: plans "with progress and decision logs that
are checked into the repository"). Section names follow A7's ExecPlan; the wording is ours. Write it
so a new session with no memory can restart from this file alone (A7). Update it as you work, not at
the end. -->

## Purpose

<What a user can do after this change that they could not do before, and how to see it working.>

## Progress

- [ ] (<YYYY-MM-DD HH:MM>) <step>
- [ ] (<YYYY-MM-DD HH:MM>) <step>

## Surprises & Discoveries

- <Something that behaved differently than expected, with the evidence (command and output).>

## Decision Log

- Decision: <what was decided>
  Rationale: <why, and which alternative was rejected>
  Date: <YYYY-MM-DD>

## Outcomes & Retrospective

<Filled in when the feature passes: what was delivered, what is left, what to do differently.>

## Validation

Commands that prove the feature works, with the result you expect from each:

```
<test command for this feature>      expected: all pass
./init.sh                            expected: init: ok
<manual check, for example a curl>   expected: <status and body>
```
