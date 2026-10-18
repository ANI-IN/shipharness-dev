# Merge and verify: the lead's checklist

Agents work on branches in their own worktrees and hand back reports. The lead combines the
branches, proves the combined tree works, and only then pushes. Each step below exists because
skipping it once let a broken tree out ([lessons-learned.md](lessons-learned.md)).

## Merge the branches

- [ ] Every agent has reported and its branch has the commit sha it named.
- [ ] Merge one branch at a time into main with `--no-ff`, in dependency order (tooling before the
      pages that use it).
- [ ] Resolve conflicts by reading both sides; never take one side wholesale for a file both
      changed.
- [ ] Check the commit identity on every new commit: owner identity only, no co-author or
      "generated with" lines.
- [ ] Remove each worktree after its branch is merged.

## Re-run the full suite on the combined tree

Each branch passed its own targeted tests; the combination has not been tested by anyone yet.

- [ ] Full test suite once, on the merged main.
- [ ] Style checker strict and prose lint over the whole repository, not just the changed files.
- [ ] The link check, internal and external.
- [ ] Container or slow tests once, if the phase touched them.
- [ ] Reproduce CI conditions locally (no colour, fixed terminal width) before trusting a pass.
- [ ] A failure on the combined tree goes back to the owning agent with the exact output, or is
      fixed test-first by the lead.

## Verify the agents' claims

A report is a claim. Check it against the tree before repeating it to the owner.

- [ ] The named files exist and hold the described change (`git show --stat <sha>`).
- [ ] The stated test counts match a run you made yourself.
- [ ] Every number in new pages traces to its run folder or file.
- [ ] Every image a caption describes shows what the caption says (open it).
- [ ] The report is about the current tree: its sha is the branch head, not an earlier commit.

## Scans before every push

- [ ] Secret scan over the working tree and the full history.
- [ ] Leak check of the release build: only allow-listed files, no private notes, graders or hidden
      tests ([release-and-publish](../skills/release-and-publish/SKILL.md)).
- [ ] No host paths, user names or personal details in committed files or images.
- [ ] Contributor check: one identity, no attribution lines.

## CI on both repositories

- [ ] Push the dev repository, then the public release, only at the publish stop point (⏸) or with
      the owner's standing permission.
- [ ] Watch CI to the end on the pushed commit of each repository; green there is the bar, not a
      local pass.
- [ ] Dispatch the slow workflows (full suite, containers) by hand if they do not run on push.
- [ ] A red CI run is fixed and pushed again before the report says "done".

## Refresh the test copy

- [ ] Replace the owner's test copy with a fresh clone of the public release.
- [ ] Update its "test me first" note: what changed, what to try first, known issues.
- [ ] Clone, sync, run the fast suite in the fresh copy, and follow the tester checklist once.
- [ ] Report with [status-and-report-formats.md](status-and-report-formats.md), budget line last.
