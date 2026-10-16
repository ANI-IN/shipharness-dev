# Product specs

What TeamTrack does, from the user's side. Feature specs are added here as features are planned.

| Spec | Covers |
|---|---|
| [teamtrack-base.md](teamtrack-base.md) | the base product: orgs, users and roles, projects, members, issues, audit log |
| [f1.md](f1.md) | F1 org-wide issue search: `GET /issues` with filters and cursor pagination |
| [f2.md](f2.md) | F2 comments on issues, and the board's comments panel |
| [f3.md](f3.md) | F3 `Idempotency-Key` on issue creation |
| [f4.md](f4.md) | F4 optimistic concurrency (`ETag`, `If-Match`), issue history, the board's conflict page |
| [f5.md](f5.md) | F5 bulk close of in-progress issues in one project |
| [f6.md](f6.md) | F6 watchers: watch issues, list an issue's watchers, list what I watch |
| [f7.md](f7.md) | F7 labels: org labels, labels on issues, label filters |
| [c1.md](c1.md) | C1 control task: filter the user list by role |
| [c2.md](c2.md) | C2 control task: search projects by name |
| [c3.md](c3.md) | C3 control task: filter a project's issues by priority |
| [c4.md](c4.md) | C4 control task: store issue titles without surrounding whitespace |
| [c5.md](c5.md) | C5 control task: admins cannot change their own role |
| [c6.md](c6.md) | C6 control task: filter the audit log by action |
| [c7.md](c7.md) | C7 control task: show user details in project member lists |
| [c8.md](c8.md) | C8 control task: show the assignee on the board's issue page |

Each feature spec is also in `docs/features/` of the repository; the two copies are identical.
