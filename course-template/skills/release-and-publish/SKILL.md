---
name: release-and-publish
description: Build the public course repository from the private dev repository as one fresh commit from an allow-list, with leak check, secret scan, contributor check, tags and CI, then refresh the test copy. Use at the publish stop point or for a release dry run.
---

# Release and publish

Learners get a clean public repository: one commit by the owner's identity, only allow-listed files,
no private notes, graders or hidden tests, CI green. The private dev repository keeps the history.
The bar is in section 2.10 of [STRUCTURE-AND-TASTE.md](../../STRUCTURE-AND-TASTE.md); the lead's
checklist is [merge-and-verify.md](../../playbooks/merge-and-verify.md).

## When to use

- At the publish stop point (⏸), after the owner approves the release candidate.
- For a dry run at any time, to see what would ship and what leaks.

## Inputs

- The dev repository at a known commit (`--ref`), with the full suite green on it.
- The release script and its allow-list (`<RELEASE SCRIPT>`): folders and files that ship.
- The public repository name (`<PUBLIC REPO>`), the release tag (`<TAG>`), the owner identity.
- The owner's approval to push.

## Steps

1. **Allow-list, not deny-list.** The release script copies only allow-listed paths, read from git
   objects at `--ref`, so untracked and working-tree files never ship. New folders ship only when
   added to the allow-list.
2. **Dry run.** Build into a temporary folder and read its report: public files per folder, files
   expected but missing, leaks, broken references to excluded files, tags, contributors.
3. **Leak check.** Fail on any private file: engineering notes, design notes, graders, hidden tests,
   internal scripts, run stores. Reference solutions ship only if the solutions policy says so.
4. **Broken references.** No public page may link to or name an excluded file; fix the page, not the
   allow-list.
5. **Secret scan** over the built tree and over the dev repository's working tree and full history.
   Use obviously fake fixture values; never relax the scanner.
6. **Contributors.** One commit, author and committer the owner's identity; no co-author lines, no
   "generated with" lines, no AUTHORS or CODEOWNERS listing others.
7. **Tags.** Write the release tag on the single commit, annotated with content hashes and run
   settings; rebuild checkpoint tags if the course has them.
8. **Build and push** only with the owner's approval. Push the dev repository and the public
   repository; watch CI on the pushed commit of each to green; dispatch slow workflows by hand.
9. **Verify from a fresh clone**: clone, sync with the lock file, run the fast suite, follow the
   tester checklist exactly.
10. **Refresh the test copy** and its "test me first" note.

## Outputs

- The public repository with one commit and the release tag; CI green on both repositories.
- The dry-run report, the scan results, and a fresh-clone verification record.

## Checks

- Dry run exits 0: no leak, no contributor problem; broken references fixed.
- Secret scan clean on tree and history.
- `git log` in the fresh clone shows one commit by the owner identity.
- Every link in the public README resolves in the public repository.
- The release steps are reported with the budget line
  ([status-and-report-formats.md](../../playbooks/status-and-report-formats.md)).
