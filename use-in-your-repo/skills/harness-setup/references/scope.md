# Scope checklist: what the agent may change and reach

Source ids and finding ids are listed in `docs/REFERENCES.md` in the course repository.
Assessment checks C1-C5 test the items marked with a check id.

| Done | Item | Why | Source |
|---|---|---|---|
| [ ] | (C1) feature_list.json lists every feature, each starting with `"passes": false`. | A2's features "were all initially marked as “failing” so that later coding agents would have a clear outline of what full functionality looked like." A5 labels the file "source of truth". | A2, F-a-78; A5, F-a-85 |
| [ ] | The list is JSON, not Markdown. | "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files." | A2, F-a-81 |
| [ ] | (C2) Each entry has `id`, `category`, `description`, `steps`, `passes`; shipharness adds `evidence` and `testedAt`. | A2's sample entry has category, description, steps, passes. The two extra fields are course design. | A2, F-a-82 |
| [ ] | Agents may change only `passes`, and AGENTS.md says so in strong words. | "We prompt coding agents to edit this file only by changing the status of a passes field"; "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." | A2, F-a-79, F-a-80 |
| [ ] | Decide who sets `passes`. | In A2 the agent sets it after careful testing (F-a-108). shipharness moves the decision to the harness after a gate, citing A3: "Separating the agent doing the work from the agent judging it proves to be a strong lever". | A2, F-a-108; A3, F-a-110 |
| [ ] | (C3) A JSON schema describes the file, so a script can reject a malformed edit. | Structured formats for state data. | A6, F-a-77 |
| [ ] | One feature per session. | "work on only one feature at a time"; A3: "worked well for scope management." | A2, F-a-83; A3, F-a-102 |
| [ ] | Each phase has a list of paths the agent may change; changes outside it are rejected or reverted. | A5: "File operations restricted to the project directory only"; A1: "enforce boundaries centrally, allow autonomy locally." The per-phase list is the course's application of both. | A5, F-a-86; A1, F-a-98 |
| [ ] | (C4) Layering is enforced by code (an import-linter contract or a structural test). | "These constraints are enforced mechanically via custom linters ... and structural tests." | A1, F-a-93, F-a-95 |
| [ ] | (C5) The agent runs in a container with no network. | "for each agent, a Docker container is spun up"; "Claude did not have internet access at any point during its development". | A4, F-a-88, F-a-90 |
| [ ] | Commands outside an allowlist are blocked. | "Commands not in the allowlist are blocked by the security hook." | A5, F-a-87 |

## Signs the scope part is missing

- The agent starts three features in one session and finishes none.
- A feature is marked done by editing its description to match what was built.
- The agent edits a test file in the build phase to make a failing test pass.

## Notes

- A2 calls feature-list entries "tests" in its strongly-worded instruction; it means the entries,
  not unit test files.
- File presence is all the assessment can see for C5. A Dockerfile does not prove the agent runs
  inside it.
