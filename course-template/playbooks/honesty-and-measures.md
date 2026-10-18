# Honesty and measures

A course that measures its own approach is only worth its numbers if nobody chose them. These
rules hold for every run, every page and every slide. The skill that applies them is
[evidence-and-results](../skills/evidence-and-results/SKILL.md); section 2.7 of the
[structure guide](../STRUCTURE-AND-TASTE.md) gives the page rules.

## Pre-register before any run

Write the design down, dated, in the course's design notes, before the first run it governs:

- the question, and the primary measure that answers it (one per comparison);
- the secondary measures, labelled secondary;
- the arms and what differs between them (one thing), and the settings that are identical;
- the number of runs per arm, and the stopping rule;
- what counts as a pass, a fail, and an error that is not counted;
- the budget cap.

After the first run, the measure, the arms and the run count are fixed. A new idea becomes a new,
separately pre-registered round. Old runs are not re-judged under a new measure. Analysis thought of
after seeing the data is labelled "exploratory (post hoc)" and cannot change a classification.

## Never re-run for a nicer result

- Every run counts, including the ones that fail. Never pick, drop, or replace a run.
- Never edit captured output, a terminal capture, or a screenshot's content.
- An error run (infrastructure, not the agent) is recorded as an error with its cause; the
  pre-registered rule says whether it is replaced, decided before the run.
- Re-judging applies a fixed checker to stored output, for every run of both arms at once, only when
  the checker had a bug; the bug, the fix and the before and after counts are disclosed.
- A demo that gives a different result in class is shown and explained, not hidden. The guide and
  the instructor notes say what to say for a pass and for a fail.

## Disclosure wording

Results are counts ("3 of 3", "0 of 4"), never percentages. Use these phrases exactly:

| Situation | Write |
|---|---|
| Both arms the same | "No measurable difference" |
| One arm better | "<Arm> ahead", with both counts |
| Both arms fail | "Both fail" |
| A setting changed | "<Setting> changed from <a> to <b> on <date>, for <arm or both>, because <reason>" |
| Analysis after the data | "Exploratory (post hoc); it does not change any result" |
| Small sample | "<N> runs per arm; a larger sample could differ" in Known limitations |

State what the approach costs (time, money, tokens) next to what it gains, and list known
limitations on the front page.

## Timing rules

- Time a demo only when it runs alone. A run paired with another is recorded as
  `ran: "paired with <demo>"` and its time is not used for any page.
- Each demo runs three times against its time bar before class; give times as the range over those
  runs, with the date and the profile: "3:37 to 4:45, measured <date> with the class profile".
- Write the times the tool printed (launch to first verdict, launch to full verdict), not times
  read off a clock.
- A timing that changed after a setting change is re-measured, and the old range is removed.
