<!-- REPLACE: TeamTrack's API conventions (`R3`, the API conventions rule): list and error envelopes and status codes. The `R3` check asserts exactly these envelopes; keep them only if your API follows them. -->
# API conventions (R3)

Status: in force for every endpoint. Verified by the R3 check.

## R3 API conventions

### Lists

- List endpoints return `{"items": [...], "next_cursor": "..." | null}`.
- They accept `cursor` and `limit` (1 to 100, default 20).
- Use the helpers in `app/api/pagination.py`: keyset pagination by ascending id, an opaque cursor,
  `next_cursor` null on the last page.
- Do not use offset pagination. The reason is in [cursor-pagination.md](cursor-pagination.md).

In code, `list_projects` in `app/api/projects.py` shows the pieces: `page_params` for the query
parameters, `decode_cursor` for the incoming cursor, and `to_page` for the response.

### Errors

- Errors return `{"error": {"code": "...", "message": "..."}}`.
- Raise the errors in `app/services/errors.py` (`NotFound`, `Forbidden`, `Conflict`, `Invalid`,
  `BadRequest`); the handlers in `app/api/errors.py` produce the envelope.
- Validation errors come back as 422 validation_error.

### Status codes

| Request | Status |
|---|---|
| create | 201 |
| delete | 204 |
| anything else | 200 |

The check: a schema-based fuzzer (Schemathesis) plus assertions on the list and error envelopes.

## Related rules

- Another org's resource is 404 not_found and a viewer's write is 403 forbidden:
  [SECURITY.md](../SECURITY.md).
- The same `Idempotency-Key` with a different body returns 409 idempotency_conflict:
  [RELIABILITY.md](../RELIABILITY.md).
