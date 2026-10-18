---
name: fresh-reviewer
description: Follow a guide or page on a clean copy of the repository, live and exactly as written, first as a first-time learner and then as the instructor about to teach it, and report every place you got stuck or misled. Use before a release candidate or after a big rewrite.
---

# Fresh reviewer

Authors cannot see the gaps in their own pages. A reviewer that wrote none of them follows them
exactly as written, on a copy with nothing left over from the build. Lesson 10 in section 4.4 of
[STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md) asks for this before every release candidate.

## When to use

- A section, guide or setup page is finished and has not been followed by someone new.
- Before the publish stop point, on the release candidate.

## Inputs

- A fresh clone of the release candidate (not the dev repository, not a worktree).
- The page or guide to follow, and the role order: learner first, then instructor.
- Whether model calls are allowed (only if this reviewer is also the live runner for the phase).
- The findings form under "Outputs".

## Steps

1. **Clean copy.** Clone fresh, set up only as the setup pages say. Do not use anything you know
   from elsewhere; if a step needs knowledge the page does not give, that is a finding.
2. **As a learner**: do every step exactly as written, type every command, compare every output with
   what the page says you should see. Time each part against the page's stated time.
3. **As an instructor**: read it again as the person teaching it next: can you deliver each demo
   from the notes alone, explain a failed result, recover with the fallback, and stay on time?
4. **Check consistency**: commands, timings, numbers and names agree across the pages, the guide and
   the slides; every link opens and points at the right place.
5. Change nothing. Write every finding in the report format.

## Outputs

A report in the findings form below: blockers first, then the rest by page. Each finding: location, what the
page says, what happened, severity (blocker, misleading, minor), suggested fix.

```text
Fresh review: <PAGE OR GUIDE>. Copy: fresh clone of <REPOSITORY> at <SHA>. Model calls: <yes/no>.
Summary: <could a first-time engineer finish it; could an instructor teach from it>.
Findings: <B> blockers, <M> misleading, <N> minor.

| # | Severity | Location | The page says | What happened | Suggested fix |
|---|---|---|---|---|---|
| 1 | blocker | <file>, step <N> | <quote> | <exact output or behaviour> | <fix> |

As the instructor: <each demo deliverable from the notes alone? fallback clear? timing holds?>
Times: <part: page says / took>, one line each.
```

## Checks

- Every finding names a file and a line or step, so an editor can act without asking.
- Findings are about what happened, not about taste, unless they break a rule in the
  [checklist](../../STRUCTURE-AND-TASTE-CHECKLIST.md).
- The report goes to the lead, who starts an editor fix pass
  ([agent-prompt-templates.md](../../playbooks/agent-prompt-templates.md)).
