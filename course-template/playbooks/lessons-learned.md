# Lessons learned

Failures an earlier course build hit, each with how it showed up, why, and the fix to apply from
the start. Read this before planning a phase; the [merge-and-verify](merge-and-verify.md)
checklist and the skills already include each fix.

## Real-screen overflow at display scaling

**What happened.** The web console passed every layout test at 1920 by 1080, then cut off columns on
the presenter's laptop. The laptop ran at 150% display scaling: the browser had 1280 CSS pixels.
**Fix.** No layout tied to a screen size. Test a sweep of widths (320 to 2560 CSS px), two heights,
pixel ratios 1.25, 1.5 and 2, and browser zoom; then a person looks at the screenshots. See
[ui-layout-check](../skills/ui-layout-check/SKILL.md).

## Stale stylesheet

**What happened.** A layout fix was merged and tested, yet the owner's browser still showed the
broken layout: it served the old stylesheet from its cache.
**Fix.** Version every static asset URL with a content hash (`style.css?v=<hash>`) and send
`Cache-Control: no-cache` for it; a test asserts both. Tell testers to reload with a hard refresh.

## Tests that fail only on the combined branch

**What happened.** Each agent's branch passed its tests; main failed after the merge, because two
branches changed the same fixture or page from different sides.
**Fix.** Re-run the full suite once on the merged tree before any push, and send failures back with
the exact output.

## A moved folder falls out of the checks

**What happened.** A folder was renamed; the style checker and the prose lint kept a fixed list of
folders, so the moved pages were silently no longer checked.
**Fix.** Checkers find folders by pattern (`section-*`) or by config, never by a fixed list, and a
test asserts every Markdown file in the repository is covered.

## A redaction breaks the graders

**What happened.** Host paths were redacted to `~/...` in captured output; a grader parsed the same
files and expected absolute paths, so graded runs began failing.
**Fix.** Redact only the copies made for pages and images. Keep raw captures where tools read them,
out of the public tree, and test the grader against a redacted sample.

## Fake keys trip the secret scanner

**What happened.** Test fixtures held realistic fake keys; the secret scan flagged them and blocked
the release, and someone was tempted to weaken the scanner.
**Fix.** Use obviously fake values that match no real key format (`test-key-not-real`), or an
allow-list entry for the exact fixture path with a reason. Never relax the scanner's patterns.

## A wording change breaks a parser

**What happened.** A plain-language rewrite changed a heading and a log line; a script that parsed
that heading, and a test that matched the log line, broke.
**Fix.** Before changing a fixed string, search the code and tests for it. Strings that tools parse
are listed in the shared brief's conventions and changed only with their parser and test.

## Captions that describe a cut-off part

**What happened.** A caption described a table row that the crop had cut off; the writer had
captioned from the run log, not from the image.
**Fix.** Open every image before captioning it and describe only what is visible. A reviewer
checks each caption against its image ([demo-guide-writer](../skills/demo-guide-writer/SKILL.md)).

## Demo results that differ from expectations

**What happened.** A live demo meant to show one arm failing passed both arms in a run, and the
script had nothing to say.
**Fix.** Pilot every demo three times early; write the instructor note for both outcomes; report
the real result plainly ([honesty-and-measures.md](honesty-and-measures.md)). Never re-run for the
expected result.

## Agents hand back stale reports

**What happened.** An agent's report described an earlier commit, or listed tests from before a
later change; the lead repeated it to the owner.
**Fix.** Ask for the commit sha in every report; the lead checks the sha is the branch head and
re-runs the stated checks before reporting
([merge-and-verify.md](merge-and-verify.md)).
