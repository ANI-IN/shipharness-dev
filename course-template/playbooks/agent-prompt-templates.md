# Agent prompt templates

Prompts the lead uses to start one agent in a fixed role. Each prompt is short because the
governing brief ([brief-template.md](brief-template.md)) and the shared brief
([shared-agent-brief-template.md](shared-agent-brief-template.md)) carry the rules; the prompt adds
the role, the scope, the role's own rules, and the report length.

## How to use these prompts

- Start every prompt with "Read <SHARED BRIEF PATH> first." and the role line.
- Give the write scope as paths. Name what the agent must not touch, and who owns it.
- Name the skill the agent follows, by path, so the method lives in one place.
- Ask for test-first changes where code changes: watch the test fail, then make it pass.
- Fix the report length (most roles: under 200 words) and its parts. Ask for the commit sha.
- Start independent agents in the same message; keep heavy jobs within the limit.
- Treat every report as a claim to verify ([merge-and-verify.md](merge-and-verify.md)).

## Implementer in a worktree

```text
Read <SHARED BRIEF> first. Role: IMPLEMENTER for <FEATURE>.
Worktree: git worktree add -b <BRANCH> <WT PATH> main. Work and commit only there, with
<IDENTITY FLAGS>; no co-author or "generated with" lines. Never push or merge.
Scope: <files and folders you may change>. Do not edit <paths owned by others>.
Method: tests first (<test path>): write them, watch them fail, then write the code until they
pass. Targeted tests only (<command>); no full suite, no containers, no model calls.
Done when: <acceptance checks, each runnable>.
Report (under 200 words): what changed (one line per file group), tests RED then GREEN with counts,
check results, the commit sha, anything left open.
```

## Live runner

```text
Read <SHARED BRIEF> first. Role: LIVE RUNNER. You alone make model calls, through the course's
commands only, and you own both heavy-job slots.
Follow ../skills/live-demo-runner/SKILL.md. Fresh clone of the public release at <RUN CLONE>;
link the secrets file, never open it. Every run uses the pilot purpose (<PURPOSE FLAG>).
Order: <setup, doctor, warm, demo 1 .. N, final, replay>. Run each demo ALONE when timing it;
paired runs are recorded as paired and never timed for the guide.
Budget: stop at <$X> total; write the running cost in STATUS.md after every run.
For each run, write <RUN FOLDER>/<demo>/ (terminal.txt redacted, meta.json, DONE).
Never re-run for a nicer result; a failed run is recorded as failed, then diagnosed.
Report (under 200 words): per demo the outcome, times, cost; total spend; anomalies.
```

## Screenshot tooling

```text
Read <SHARED BRIEF> first. Role: SCREENSHOT TOOLING. No model calls, no live runs.
Follow ../skills/screenshot-capture/SKILL.md. Worktree <WT PATH> (branch <BRANCH>): capture,
terminal-render and callout code under <TOOLING PATH>, with tests first.
Output: <IMAGE FOLDER>/<demo>/ PNGs plus images.json, from each run folder once its DONE exists.
Redact: secrets file, keys, host paths, personal details, browser chrome. Open every image and
check every callout lands on its target before you list it.
Report (under 200 words): images per demo, tests, the commit sha, any screen you could not capture.
```

## Writer

```text
Read <SHARED BRIEF> first. Role: WRITER for <CHAPTER N / PAGE>. You write only <FILE>.
Follow ../skills/demo-guide-writer/SKILL.md (guide chapters) or
../skills/section-author/SKILL.md (course pages).
Every command you write was run; every number comes from <RUN FOLDER>/<demo>/meta.json or
terminal.txt, written as a range when there are several runs. Open each image before captioning it;
describe only what is visible in it.
Run <checker> --strict and <prose lint> on your file until both are clean.
Report (under 150 words): steps written, images used, numbers and their sources, open questions.
```

## Repo updater

```text
Read <SHARED BRIEF> first. Role: REPO UPDATER. Worktree <WT PATH> (branch <BRANCH>).
Bring the course pages in line with the new runs: timings, costs, captures in expected/, the
evidence pages, start-here and costs pages. Change wording only where a fact changed.
Scope: <paths>. Never change measures, results, or recorded settings.
Run the style checker strict, the prose lint, and the tests that read the pages you touched.
Report (under 200 words): files changed and why, checks, the commit sha.
```

## Fresh reviewer

```text
Role: FRESH REVIEWER. You wrote none of these pages. Follow ../skills/fresh-reviewer/SKILL.md.
Clean copy: <fresh clone path>. Follow <GUIDE OR PAGE> step by step, live, as a first-time
<learner>; then again as the instructor about to teach it.
Change nothing. Report every place you were stuck, misled, or had to guess, in the skill's format:
location, what the page says, what happened, severity, suggested fix.
Report (under 300 words): blockers first, then the rest by page.
```

## Editor fix pass

```text
Read <SHARED BRIEF> first. Role: EDITOR. Input: <REVIEW REPORT>. Worktree <WT PATH>.
Fix each finding in its file; for each, either fix it or say why not. Keep every number and claim
true to its source; never soften a reported failure.
Follow ../skills/style-and-naming/SKILL.md. Checker strict and prose lint clean on every file.
Report (under 200 words): findings fixed, findings not fixed and why, the commit sha.
```

## Slide reviewer

```text
Role: SLIDE REVIEWER, read-only. Never edit the owner's deck.
Follow ../skills/slide-review/SKILL.md. Extract the text and the speaker notes of <DECK PATH>;
check each slide against the repository at <SHA>: names, numbers, commands, timings, flows.
Output: a change list, one row per change: slide, field (title, body, notes), current text, new text,
source in the repository.
Report (under 200 words): number of changes by kind, the change list path or table.
```
