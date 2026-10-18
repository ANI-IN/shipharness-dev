# Poll questions

The class has exactly one poll: a Live Zoom Poll at the start of Section 4: Verification, at
2:55-2:57, right before `make show-4` and `make final` are launched. It picks the feature of the
final A/B. No other section has a poll, and no other poll slide is in the deck. Sections 1 to 3
launch their live run on their start slide (`make show-1` at 0:11,
`make show-2 SESSION_BUDGET=12,38` at 1:11, `make demo-3 FEATURE=version-checks` at 2:01);
Section 4 launches `make show-4` and `make final` at 2:57, right after the poll. Timing is in
[run-sheet.md](run-sheet.md); the slide is "Live Zoom Poll" in
[../slides/module1-slides.md](../slides/module1-slides.md).

In class, note the vote counts and add them to the after-class record in VERIFICATION.md.

---

## Final feature poll (start of Section 4, 2:55-2:57)

Ask it right after the Section 4 start slide and close it before the launch. The final A/B is
launched at 2:57 and runs during Section 4; the room sees its
results in the final block (3:40).

**Question.** Which feature should both arms build for the final run, with all four layers on? The
winner runs first; the runner-up runs after it.

| Option | Feature | Spec and sessions | What it stresses |
|---|---|---|---|
| A | Feature 5: Bulk close: close all finished issues of a project in one request | `platform/teamtrack/docs/features/f5.md`; one session, budget 30 | Atomic 404 for any foreign or deleted id (House rule 1: Tenant isolation), viewers get 403 (House rule 2: Roles), one audit row per request (House rule 5: Audit log) |
| B | Feature 6: Watchers: follow issues and list the ones you watch | `platform/teamtrack/docs/features/f6.md`; two sessions, budgets 20 and 30 | A session stop in the middle (as in Section 2: State and sessions), one new migration (House rule 7: Migrations), no-op writes add no audit row (House rule 5) |
| C | Feature 7: Labels: tag issues and filter lists by label | `platform/teamtrack/docs/features/f7.md`; two sessions, budgets 25 and 35 | A session stop, safe label creation per org on retries (House rule 4: Safe retries) |

The session budgets are in each feature's `platform/teamtrack/reference/fN/task.toml`.

**After the vote.** Read the session figure on the Section 3 A/B's `Cost:` line. At 2:57, in
terminal C, right after `make show-4` in terminal B:
`make final FEATURES=<winner>,<runner-up>` (for example `make final FEATURES=watchers,bulk-close`)
when that figure is at most $1.10; otherwise `make final FEATURES=<winner>` (run sheet, Section 4
cost note). The readable names are `bulk-close`, `watchers`, and `labels`. `make final` runs the
features one after another. The final has no pre-registered primary measure; every score is shown
(DESIGN §8.2).

**What to compare it with.** The runs before class had no A/B on Features 5 to 7, and the experiment
batch that would have covered them was not run because the pre-registered gate did not pass.
Tonight's final is one dot for each arm: read its hidden-test and mutant counts against the section
results on the "All results" slide, never as a verdict on its own. The course's earlier Feature 5
A/Bs (the check under load and the quiet run on 2026-10-17) are listed in
[fallbacks.md](fallbacks.md).

**The section predictions.** The prediction questions that used to open each section are gone. Their
answers from the runs before class stay on each section's "What we measured" slide and in the run
sheet's results table ([run-sheet.md](run-sheet.md#every-result-on-one-slide-and-one-console-view)).
Use them in the Q&A of each section.
