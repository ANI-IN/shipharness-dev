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

Each feature spec is also in `docs/features/` of the repository; the two copies are identical.
