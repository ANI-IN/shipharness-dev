# Status and report formats

Every report goes in chat, not into a report file, unless the owner asks for a file. Every report
carries the budget line. Write facts with their source; never "should work" without having run it.

## Five-line status

Use it whenever the owner asks "where are we", and at each stage end during a long phase.

```text
Done: <what finished since the last status, with commit shas>
Running: <agents and jobs now running, with what each waits on>
Next: <what starts when the running work ends>
Blocked: <what waits on the owner, or "nothing">
Budget: <the budget line>
```

## Phase line

One line when a phase or stage ends, so the owner can follow without reading reports:

```text
Phase <N> <name>: done | partly done | failed. <one-sentence result>. Next: <phase>. <budget line>
```

## Final report

One report at the end of the phase, in the order the governing brief names
([brief-template.md](brief-template.md)). Without other instructions:

1. Changes per area, one or two lines each, with the commit or tag.
2. Live results and timings: per demo, the runs, outcome, times as ranges, cost.
3. Bugs fixed, each with its test.
4. Checks: style strict, prose lint, link check, fast suite, full suite, release dry run,
   contributor check, secret scan, with their results.
5. Repository and CI status: both repositories, the pushed shas, CI result per workflow.
6. Not done, and why.
7. Decisions for you.
8. For afterwards.
9. The budget line.

## Budget line

Always the same fields, so two reports can be compared:

```text
Budget: build <$spent> spent / <$left> left of <$cap>; pilot <N> runs, <$cost>; traces <N> (<where>).
```

Spend comes from the tool's own cost records, not from estimates. Say "no model calls" when there
were none.

## Decisions for you

Only what needs the owner: a stop point (⏸) or a choice the rules do not settle. One numbered line
each: the question, the options, your recommendation, and what happens if there is no answer.

```text
1. <question>? Options: A <...>, B <...>. Recommend A because <reason>. Without an answer: <default>.
```

## For afterwards

Things worth doing later that are outside this phase: follow-up fixes, ideas, debt. One line each,
with where the detail is. Keep it apart from "Decisions for you" so neither hides the other.
