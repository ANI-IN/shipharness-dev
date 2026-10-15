# R-e Libraries, tool versions, name check

Prepared 2026-10-16 by research subagent R-e. Machine used for the measurements: Windows 11 Pro laptop, CPython 3.12.10, uv 0.13.0, pytest 9.1.1. Raw run logs are under `scratchpad\research\libs\<name>\run\`. PyPI metadata dump: `scratchpad\research\data\pypi.json`.

## Sources

| id | title | URL | access date |
|---|---|---|---|
| E1 | PyPI JSON API, one call per package listed in the tool-versions table (version, upload time of the first file, `requires_python`, classifiers, license expression) | https://pypi.org/pypi/{package}/json | 2026-10-16 |
| E2 | boltons repository, tag 26.2.0 | https://github.com/mahmoud/boltons/tree/26.2.0 | 2026-10-16 |
| E3 | boltons LICENSE (BSD-3-Clause text) | https://github.com/mahmoud/boltons/blob/26.2.0/LICENSE | 2026-10-16 |
| E4 | WTForms repository, tag 3.2.2 | https://github.com/pallets-eco/wtforms/tree/3.2.2 | 2026-10-16 |
| E5 | WTForms LICENSE.rst (BSD-3-Clause text) | https://github.com/pallets-eco/wtforms/blob/3.2.2/LICENSE.rst | 2026-10-16 |
| E6 | packaging repository, tag 26.3 (evaluated, rejected) | https://github.com/pypa/packaging/tree/26.3 | 2026-10-16 |
| E7 | npm registry: htmx.org (dist-tags, times) | https://registry.npmjs.org/htmx.org | 2026-10-16 |
| E8 | npm registry: htmx-ext-sse | https://registry.npmjs.org/htmx-ext-sse | 2026-10-16 |
| E9 | htmx SSE extension docs (htmx 2 install and attributes) | https://htmx.org/extensions/sse/ | 2026-10-16 |
| E10 | htmx 4.0.0 release announcement | https://four.htmx.org/announcements/2026-08-28-htmx-4.0.0-is-released | 2026-10-16 |
| E11 | htmx 4 changes / extension migration guide | https://four.htmx.org/whats-new-in-htmx-4 ; https://four.htmx.org/extensions/migration-guide | 2026-10-16 |
| E12 | npm registry: @marp-team/marp-cli | https://registry.npmjs.org/@marp-team/marp-cli | 2026-10-16 |
| E13 | uv latest GitHub release (API) | https://api.github.com/repos/astral-sh/uv/releases/latest | 2026-10-16 |
| E14 | Vale latest GitHub release (repo moved from errata-ai/vale to vale-cli/vale) | https://api.github.com/repos/vale-cli/vale/releases/latest | 2026-10-16 |
| E15 | mutmut 3.8.0 README (PyPI long description) | https://pypi.org/project/mutmut/3.8.0/ | 2026-10-16 |
| E16 | PyPI project "shipproof" | https://pypi.org/project/shipproof/ | 2026-10-16 |
| E17 | GitHub repo Hurshid87/shipproof | https://github.com/Hurshid87/shipproof | 2026-10-16 |
| E18 | GitHub repository search "shipproof" (31 results) | https://api.github.com/search/repositories?q=shipproof | 2026-10-16 |
| E19 | npm package "shipproof" (CalvaryBloom) | https://registry.npmjs.org/shipproof | 2026-10-16 |
| E20 | shipproof.io (social-proof widget product named ShipProof) | https://shipproof.io | 2026-10-16 |
| E21 | Propel Apps "ShipProof" supply-chain feature | https://www.propelapps.com/blog/how-secure-shipping-with-shipproof | 2026-10-16 |
| E22 | github.com/shipproof and github.com/ANI-IN/shipproof (both HTTP 404) | https://github.com/shipproof ; https://github.com/ANI-IN/shipproof | 2026-10-16 |

## Library shortlist

Module-size figures are from shallow clones of the default branch (survey) or the pinned tag (picks). "Moderate modules" counts modules in roughly the 90-650 line range.

| library | license | pure logic | pytest | suite runtime | py3.12 | moderate modules | maintained (latest release) | notes | verdict |
|---|---|---|---|---|---|---|---|---|---|
| boltons | BSD-3-Clause | yes (socketutils/gcutils/ecoutils/debugutils are environment-dependent; avoid them) | yes, plus doctests | measured 3.4 s, 672 tests | yes (classifier) | ~15 | 26.2.0, 2026-09-07 | many independent modules, each with its own test file; 76% stmt coverage leaves room for coverage-gain | PICK |
| WTForms | BSD-3-Clause | yes (only dep MarkupSafe, which has a pure-Python fallback) | yes | measured 0.9-2.3 s, 354 tests | yes (`requires_python >=3.10`, tox env py312) | 11 | 3.2.2, 2026-05-03; 3.3.0b3 tagged | dense branching in validators/fields; 98% branch coverage, so kept tests will mostly have to kill mutants rather than add coverage | PICK |
| packaging | Apache-2.0 OR BSD-2-Clause | yes | yes | measured 59-65 s (62,423 tests; 45 s in test_version.py alone) | yes | ~10 | 26.3, 2026-08-04 | pytest itself depends on packaging, so the module is imported before coverage starts (coverage reported 70% for version.py, a measurement artefact) and a mutant in version.py/specifiers.py would also alter pytest's behaviour | rejected |
| humanize | MIT | yes | yes | not measured | yes | 4 (number.py 603, time.py 704, filesize 110, i18n 210) | 4.16.0, 2026-06-30 | too few modules for 10 targets | rejected |
| marshmallow | MIT | yes | yes | not measured | yes | 3-4 (fields.py 2153 and schema.py 1253 are too large; others < 110) | 4.3.1, 2026-08-08 | module size distribution poor | rejected |
| toolz | BSD-3-Clause | yes | yes | not measured | yes | 3 (itertoolz 1062, functoolz 1141 too large) | 1.2.0, 2026-10-07 | too few moderate modules | rejected |
| cattrs | MIT | yes | yes, heavy Hypothesis use | not measured (Hypothesis-heavy suites are typically minutes) | yes | ~8 (many are thin `preconf/*` wrappers needing optional serializers) | 26.2.1, 2026-09-26 | optional C/Rust serializers for preconf modules | rejected |
| semver | BSD-3-Clause | yes | yes | not measured | yes | 2 (version.py 851) | 3.1.0, 2026-09-12 | too few modules | rejected |
| python-dateutil | Apache-2.0 / BSD dual | yes | yes | not measured | yes | few; rrule/parser/tz are > 1500 lines | 2.9.0.post0, 2024-03-01 | release cadence stalled | rejected |
| more-itertools | MIT | yes | yes | not measured | yes | 0 (more.py is several thousand lines) | 11.2.1, 2026-10-14 | single huge module | rejected |

## Picks

### Pick 1: boltons

| field | value |
|---|---|
| name | boltons |
| repo | https://github.com/mahmoud/boltons |
| license | BSD-3-Clause; file `LICENSE` at repo root ("Copyright (c) 2013, Mahmoud Hashemi"). PyPI shows the BSD classifier, no SPDX expression. |
| pinned tag | `26.2.0` (annotated tag object b14438d23fa32fcc7edc564dbdb13520ba8532eb) |
| commit SHA | `4332b35a278d694f30c99881faa61cde695c7a96` ("boltons version 26.2.0", 2026-09-07T03:42:05-07:00) |
| release date | 2026-09-07 (PyPI upload) |
| Python versions | `requires_python >=3.7`; classifiers 3.7-3.14, CPython and PyPy |
| runtime deps | none |
| test deps | `pytest>=8` (dependency group `dev`); pytest-cov added for coverage |
| test command (upstream tox) | `pytest --doctest-modules {site-packages}/boltons {repo}/tests` |
| test command (as run) | `python -I -m pytest -q -p no:cacheprovider -c src/pyproject.toml --rootdir src --doctest-modules .venv/Lib/site-packages/boltons src/tests` |
| measured runtime | wall 3.42 s and 3.43 s (pytest-reported 2.94 s / 2.96 s); first cold run 4.61 s; with `--cov` 5.87 s |
| test count | 672 collected (518 test functions in `tests/` + 154 doctests): 671 passed, 1 failed |
| coverage | 76% statements over the whole package (7319 stmts, 1731 missed), doctests included |
| known failure | `tests/test_jsonutils.py::test_reverse_iter_lines` fails on Windows only: the test joins lines with `os.linesep` (`\r\n`) and compares against an LF data file. Platform issue, not a regression. Must be recorded as a known-failing baseline test (or the dataset must run on Linux/WSL). |

Output excerpt:

```
........................................................................ [ 10%]
...
=========================== short test summary info ===========================
FAILED ..\src\tests\test_jsonutils.py::test_reverse_iter_lines - AssertionErr...
1 failed, 671 passed in 2.96s
```

Notes: most boltons functions carry doctest examples in their docstrings. That is useful context for the LLM but also means the harness must decide whether doctests are part of the baseline suite when measuring "adds coverage".

### Pick 2: WTForms

| field | value |
|---|---|
| name | WTForms (PyPI `wtforms`) |
| repo | https://github.com/pallets-eco/wtforms |
| license | BSD-3-Clause; file `LICENSE.rst` at repo root ("Copyright 2008 WTForms"). PyPI shows the BSD classifier, no SPDX expression. |
| pinned tag | `3.2.2` (annotated tag object d18aa4a14e5d1f04111a032988970aed639c02d7) |
| commit SHA | `ea57c11591556333b4f0ac494d1e5d3f250ab305` ("chore: bump to 3.2.2", 2026-05-03T07:43:42+02:00) |
| release date | 2026-05-03 (PyPI upload). 3.3.0b3 is tagged but not a stable release. |
| Python versions | `requires_python >=3.10`; tox env list py310-py314 and pypy310 (no per-version classifiers in metadata) |
| runtime deps | MarkupSafe >=1.1.1 (3.0.4 installed; ships optional C speedups with a pure-Python fallback) |
| test deps | `pytest>=7.0`, `babel>=2.8`, `email_validator>=2.0` (dependency group `dev`; installed email-validator 2.3.0, dnspython 2.9.0, idna 3.20); pytest-cov added |
| test command (upstream tox) | `pytest --tb=short -l --basetemp={envtmpdir}` |
| test command (as run) | `python -I -m pytest -q -p no:cacheprovider -c src/pyproject.toml --rootdir src src/tests` |
| measured runtime | wall 2.29 s (cold) and 0.87 s (warm); pytest-reported 1.09 s / 0.48 s; with `--cov --cov-branch` 1.90 s |
| test count | 354 collected: 353 passed, 1 failed |
| coverage | 98% with branch coverage (1642 stmts, 21 missed; 474 branches, 24 partial) |
| known failure | `tests/fields/test_date.py::test_basic` fails on Windows only: it uses the glibc-specific `%-m/%-d` strftime/strptime format, which Windows does not support. Platform issue. Record as known-failing baseline test or run on Linux/WSL. |

Output excerpt:

```
........F............................................................... [ 20%]
...
=========================== short test summary info ===========================
FAILED ..\src\tests\fields\test_date.py::test_basic - assert None == datetime...
1 failed, 353 passed in 0.48s
```

Note: `pyproject.toml` sets `filterwarnings = ["error"]`; generated tests that trigger any warning will fail under the upstream config. The `Email` validator uses `email_validator` with deliverability checks off by default, so no DNS traffic in the suite.

### Rejected after measurement: packaging 26.3

Recorded because it was the original second choice. Tag 26.3, commit `929fd4b1410ac7ef61ef3f45b2f5d7e87711a9b5`, Apache-2.0 OR BSD-2-Clause. Suite: 62,422 passed, 1 skipped, 427 deselected (property tests) in 61.3 s and 58.6 s (wall 65.2 s / 61.9 s); 147.98 s with branch coverage. `tests/test_version.py` alone: 51,523 tests, 44.6 s. Two blockers: (1) runtime is at the 60 s limit; (2) pytest 9.1.1 depends on `packaging` (`Requires: colorama, iniconfig, packaging, pluggy, pygments`), so the package is already imported when coverage starts (coverage warned "Module packaging was previously imported" and showed 70% for version.py against an upstream `fail_under = 100`), and any mutant in it changes pytest's own behaviour. Usable only if vendored under a different import name, which adds work.

## Proposed target modules

Line counts are physical lines (`wc -l`) at the pinned tag. Coverage is per-module statement coverage from the upstream suite run above.

### boltons 26.2.0 (paths relative to repo root)

| # | path | lines | upstream coverage | test file(s) | why | mutant opportunities |
|---|---|---|---|---|---|---|
| 1 | boltons/mathutils.py | 257 | 89% | tests/test_mathutils.py | `clamp`, `ceil`/`floor` with an options list (bisect), `Bits` bit-string class with int/hex/bytes conversions and slicing | swap `bisect_left` (ceil) and `bisect_right` (floor); `<` to `<=` in clamp bounds check; off-by-one in `Bits.__getitem__` slice |
| 2 | boltons/listutils.py | 350 | 74% | tests/test_listutils.py | `BarrelList` (list of lists with index translation and split-on-size) and `SplayList` | off-by-one in `_translate_index` for negative indices; change split threshold; wrong list in `pop` rebalancing |
| 3 | boltons/formatutils.py | 356 | 87% | tests/test_formatutils.py | parsing of `str.format` fields: `split_format_str`, `infer_positional_format_args`, `get_format_args`, `tokenize_format_str` | drop the escaped-brace (`{{`) branch; wrong positional counter increment; misclassify conversion `!r`/`!s` |
| 4 | boltons/queueutils.py | 223 | 85% | tests/test_queueutils.py (2 tests only) | `HeapPriorityQueue` / `SortedPriorityQueue` with add/remove/peek/pop, lazy deletion, default priority negation | remove negation in default `priority_key`; skip the `_REMOVED` entry check in `_cull`; wrong default in `pop(default=...)` |
| 5 | boltons/timeutils.py | 632 | 81% | tests/test_timeutils.py | `parse_timedelta`, `relative_time`, `decimal_relative_time`, `daterange` (step, inclusive), `USTimeZone` DST rules | `inclusive` comparison `<` vs `<=` in `daterange`; unit-boundary bisect in `decimal_relative_time`; DST start/end Sunday calculation. Avoid `LocalTZInfo` (host time zone) |
| 6 | boltons/tableutils.py | 588 | 74% | tests/test_tableutils.py | `Table` built from dicts/lists/objects via `InputType` detection; `to_text` truncation; `to_html` | wrong input-type precedence; `maxlen` truncation off-by-one; drop header row in `to_text` |
| 7 | boltons/typeutils.py | 180 | 87% | tests/test_typeutils.py | `make_sentinel` (repr, bool, pickling), safe `issubclass`, `get_all_subclasses`, `classproperty` | sentinel `__bool__` returns True; `issubclass` swallow vs re-raise TypeError; skip recursion into grandchildren |
| 8 | boltons/namedutils.py | 385 | 81% | tests/test_namedutils.py | `namedtuple`/`namedlist` code generation with field-name validation and `rename` | skip keyword check; `rename` uses wrong index; `_replace` ignores unexpected-field error |
| 9 | boltons/ioutils.py | 587 | 93% | tests/test_ioutils.py | `SpooledBytesIO`/`SpooledStringIO` rollover at `max_size`, codepoint-aware `tell`/`seek` for text, `MultiFileReader` | `>` vs `>=` on rollover; wrong `whence` handling in seek; `MultiFileReader.read(n)` boundary across files |
| 10 | boltons/jsonutils.py | 266 | 68% | tests/test_jsonutils.py | `JSONLIterator` (ignore_errors, `rel_seek`) and `reverse_iter_lines` (block reading, CRLF joining) | swallow vs raise on bad line; `rel_seek` sign error; blocksize boundary in reverse reader. Note the Windows-only baseline failure in this test file |

Alternates: boltons/pathutils.py (183, small, OS-path dependent), boltons/excutils.py (287, no test file). Avoid: socketutils, gcutils, ecoutils, debugutils, fileutils (I/O, environment, gc or timing dependent); cacheutils/setutils/dictutils/strutils/urlutils/iterutils exceed 800 lines.

### WTForms 3.2.2 (paths relative to repo root)

| # | path | lines | upstream coverage (branch) | test file(s) | why | mutant opportunities |
|---|---|---|---|---|---|---|
| 1 | src/wtforms/validators.py | 734 | 95% | tests/validators/*.py (18 files) | `Length`, `NumberRange`, `EqualTo`, `Optional`, `DataRequired`, `InputRequired`, `Regexp`, `IPAddress`, `MacAddress`, `URL`, `UUID`, `AnyOf`/`NoneOf`, `HostnameValidation`. Over 600 lines, but each validator is independent | `<` to `<=` in `Length`/`NumberRange`; `min == -1` sentinel check; IPv4 octet range `<= 255`; `Optional` stop-chain vs continue |
| 2 | src/wtforms/widgets/core.py | 569 | 100% | tests/test_widgets.py | `html_params` (boolean attrs, `class_` and `data_` key cleaning), `Select`/`Option`, `ListWidget`, `TableWidget`, `Input` subclasses | `True` attr rendered as `key="True"` instead of bare `key`; `False` attr not dropped; `clean_key` stops stripping trailing `_` |
| 3 | src/wtforms/fields/core.py | 448 | 99% | tests/fields/test_field.py, test_label.py, test_flags.py, test_filters.py, test_defaults.py | `Field.process`, `pre_validate`/`post_validate` chain, `StopValidation` handling, filters, `Flags`, `Label` | do not clear errors on `StopValidation`; filters applied before vs after coercion; default callable not called |
| 4 | src/wtforms/form.py | 330 | 99% | tests/test_form.py | `BaseForm.process` (formdata vs obj vs data vs kwargs precedence), `validate` with `extra_validators`, `populate_obj`, `FormMeta` field ordering | swap obj/kwargs precedence; `validate` returns True when one field fails; ignore `extra_validators` for a field |
| 5 | src/wtforms/fields/choices.py | 227 | 95% | tests/fields/test_select.py, test_selectmultiple.py, test_radio.py | `SelectField` choices (list, dict optgroups, callable), `validate_choice`, coercion | skip "Not a valid choice" check; selected-state comparison uses raw instead of coerced value; mishandle empty choices |
| 6 | src/wtforms/fields/list.py | 202 | 97% | tests/fields/test_list.py | `FieldList` with `min_entries`/`max_entries`, index extraction from form keys, `append_entry`/`pop_entry` | `>` vs `>=` on `max_entries`; index sort order; `last_index` off-by-one |
| 7 | src/wtforms/fields/numeric.py | 213 | 97% | tests/fields/test_integer.py, test_decimal.py, test_float.py, tests/test_locale_babel.py | `IntegerField`, `DecimalField` (places/rounding), `FloatField`, locale-aware parsing via babel | rounding mode swap; `places=None` branch; empty string coerced to 0 instead of None |
| 8 | src/wtforms/fields/datetime.py | 170 | 100% | tests/fields/test_date.py, test_datetime.py, test_time.py, test_month.py, test_week.py, test_datetimelocal.py | multiple-format parsing (first format that parses wins), joined multi-value input | stop after first format; drop `" ".join(valuelist)`; swallow vs record parse error. Note Windows-only baseline failure in test_date.py |
| 9 | src/wtforms/fields/simple.py | 173 | 100% | tests/fields/test_boolean.py, test_string.py, test_file.py, test_hidden.py, test_textarea.py | `BooleanField` false-values tuple, `StringField` empty handling, `FileField`/`MultipleFileField` | remove `""` from false values; `StringField` returns None vs "" for missing data |
| 10 | src/wtforms/csrf/session.py | 93 | 100% | tests/test_csrf.py | `SessionCSRF` token generation and validation with HMAC and `time_limit` expiry | `>` vs `>=` on expiry; skip HMAC compare; wrong time-limit default. Time-dependent: tests need the `now()` hook, not wall clock |

Alternates: src/wtforms/meta.py (132), src/wtforms/csrf/core.py (96), src/wtforms/utils.py (91).

Trade-off between the two picks: boltons modules have 68-93% upstream coverage, so generated tests can be kept on coverage gain; WTForms modules are at 95-100% branch coverage, so kept tests will mostly depend on killing the prepared mutants. This makes the two halves exercise different keep criteria.

Memorisation: both libraries are old and widely mirrored on GitHub; assume they are in model training data.

## Tool versions

"py3.12" is yes when `requires_python` admits 3.12 and, where classifiers exist, 3.12 is listed. Dates are the upload time of the first file of the latest version on PyPI (UTC date). All rows source E1 unless noted.

| package | version | release date | py3.12 | license | notes | source |
|---|---|---|---|---|---|---|
| fastapi | 0.143.2 | 2026-10-15 | yes (>=3.10; 3.10-3.14) | MIT | still 0.x; minor bumps may break | E1 |
| uvicorn | 0.54.0 | 2026-09-25 | yes (>=3.10) | BSD-3-Clause | | E1 |
| sqlalchemy | 2.1.4 | 2026-10-07 | yes (>=3.11) | MIT | 2.1 series is current; requires Python >=3.11 | E1 |
| alembic | 1.20.0 | 2026-09-11 | yes (>=3.10) | MIT | | E1 |
| jinja2 | 3.1.6 | 2025-03-05 | yes (>=3.7) | BSD-3-Clause (classifier; no SPDX field) | no release since 2025-03 | E1 |
| pydantic | 2.14.1 | 2026-10-11 | yes (>=3.10) | MIT | | E1 |
| pydantic-settings | 2.16.0 | 2026-10-14 | yes (>=3.11) | MIT | | E1 |
| structlog | 26.1.0 | 2026-06-06 | yes (>=3.10) | MIT OR Apache-2.0 | | E1 |
| httpx | 0.28.1 | 2024-12-06 | yes (>=3.8; classifiers stop at 3.12) | BSD-3-Clause | no release in ~22 months; classifiers list 3.8-3.12 only | E1 |
| schemathesis | 4.31.1 | 2026-10-14 | yes (>=3.11) | MIT | | E1 |
| import-linter | 2.15 | 2026-09-04 | yes (>=3.10) | BSD-2-Clause | | E1 |
| coverage | 7.16.2 | 2026-09-27 | yes (>=3.10) | Apache-2.0 | | E1 |
| pytest | 9.1.1 | 2026-06-19 | yes (>=3.10) | MIT | depends on `packaging` (relevant to library choice) | E1 |
| pytest-cov | 7.1.0 | 2026-03-21 | yes (>=3.9) | MIT | | E1 |
| pytest-xdist | 3.8.0 | 2025-07-01 | yes (>=3.9) | MIT | | E1 |
| mutmut | 3.8.0 | 2026-09-12 | yes (>=3.10) | BSD-3-Clause | requires `fork`; not native on Windows (see assessment) | E1, E15 |
| hypothesis | 6.170.0 | 2026-10-15 | yes (>=3.11) | MPL-2.0 | weak copyleft; fine as a dev dependency | E1 |
| playwright (Python) | 1.64.0 | 2026-10-13 | yes (>=3.10) | Apache-2.0 | browsers installed separately (`playwright install`) | E1 |
| ruff | 0.17.1 | 2026-10-15 | yes | MIT | 0.x; rule set changes between minors | E1 |
| openai | 3.31.0 | 2026-10-14 | yes (>=3.10) | Apache-2.0 | major version 3.x; check examples written against 1.x/2.x | E1 |
| langsmith | 0.14.9 | 2026-10-15 | yes (>=3.10; no classifiers) | MIT | | E1 |
| typer | 0.27.3 | 2026-10-06 | yes (>=3.10) | MIT | 0.x; built on click | E1 |
| click | 8.5.0 | 2026-08-26 | yes (>=3.10) | BSD-3-Clause | | E1 |
| rich | 15.0.0 | 2026-04-12 | yes (>=3.9) | MIT | | E1 |
| sse-starlette | 3.5.0 | 2026-09-28 | yes (>=3.10; classifiers 3.10-3.13) | BSD-3-Clause | | E1 |
| python-multipart | 0.0.32 | 2026-06-04 | yes (>=3.10) | Apache-2.0 | | E1 |
| tomli-w | 1.2.0 | 2025-01-15 | yes (>=3.9) | MIT (classifier) | only needed if the CLI writes TOML; reading uses stdlib `tomllib` | E1 |
| HTMX (`htmx.org`) | 2.0.11 (npm `latest`) | 2026-09-22 | n/a | 0BSD | htmx 4.0.0 was released 2026-08-28 under npm tag `next`; `latest` stays on 2.x, so pin `htmx.org@2.0.11` | E7, E10 |
| htmx-ext-sse | 2.2.4 | 2025-10-18 | n/a | not set in registry metadata (repo bigskysoftware/htmx-extensions) | peerDependency `htmx.org ^2.0.2`. Load core first, then `https://cdn.jsdelivr.net/npm/htmx-ext-sse@2.2.4`; enable with `hx-ext="sse"` plus `sse-connect="<url>"` on the same element, `sse-swap="<event>"` on targets, optional `sse-close="<event>"`. Replaces the htmx 1 `hx-sse` attribute | E8, E9 |
| uv | 0.13.1 | 2026-10-14 | n/a | Apache-2.0 OR MIT (GitHub reports Apache-2.0) | local machine has 0.13.0 | E13 |
| @marp-team/marp-cli | 4.5.1 | 2026-09-06 | n/a | MIT | | E12 |
| Vale | v3.24.0 | 2026-10-01 | n/a | MIT | repository moved to `vale-cli/vale` (old `errata-ai/vale` redirects) | E14 |

Python 3.12 issues: none. Every package admits 3.12. Four packages require >=3.11 (sqlalchemy 2.1, pydantic-settings, hypothesis, schemathesis); that only matters if 3.10 support were wanted.

Pending major-version breaks to watch:
- htmx 4.0.0 is out under the `next` tag. It changes extension loading (no `hx-ext`; script include plus config approval), renames events (`htmx:beforeSwap` to `htmx:before:swap`), makes attribute inheritance explicit, swaps 4xx/5xx responses by default and adds a 60 s default timeout (E10, E11). The SSE extension for htmx 4 is a different file with renamed events. Pin htmx 2.0.11 and htmx-ext-sse 2.2.4 and do not use unversioned CDN URLs.
- openai SDK is at 3.x; course code should be checked against the 3.x API.
- fastapi, typer, ruff, httpx, python-multipart, langsmith remain 0.x and may break on minor bumps; pin exact versions.

## mutmut assessment

Version 3.8.0 (2026-09-12), BSD-3-Clause, Python >=3.10.

1. Windows: not supported natively. The README states "Mutmut must be run on a system with `fork` support. This means that if you want to run on windows, you must run inside WSL." Both process-isolation modes (`fork`, `forkserver`) require `os.fork` and are POSIX-only (E15).
2. Target selection:
   - File level: `source_paths`, `only_mutate` and `do_not_mutate` glob lists.
   - Function level: mutants are named per function (`module.function__mutmut_N`); `mutmut run "my_module.my_function*"` runs a subset by glob. By default only functions that are called by the tests are mutated.
   - Line level: only exclusion, via `# pragma: no mutate`, `# pragma: no mutate block`, `# pragma: no mutate start/end`, and `do_not_mutate_patterns` regexes; `mutate_only_covered_lines = true` restricts to coverage-hit lines. There is no option to say "mutate only line N" or "apply this specific operator here".
   - Mutants are generated automatically from mutmut's operator set via libcst; individual mutants cannot be hand-written. Mutation is done through trampolines in a copied `mutants/` tree, so tests run against a rewritten copy of the source, not the original file. `mutmut apply <mutant>` can write one mutant to disk.
3. Verdict: unsuitable as the primary engine for "~4 hand-written targeted mutants on risky lines" on this Windows-based course setup. It cannot express curated mutants, cannot restrict to chosen lines except by excluding everything else, and needs WSL. Recommendation: write a small targeted mutant runner. Each mutant is a record `{id, file, line, original, replacement, rationale}` (or a unified diff); the runner applies one mutant to a temporary copy of the target module, runs the candidate test file in a subprocess with a timeout, records killed/survived/timeout/error, and restores. It runs the same on Windows and Linux and gives exact control over which lines are mutated. mutmut can still be shown as an optional comparison on Linux/WSL/CI.

## Name check

Findings for "shipproof" (checked 2026-10-16):

- PyPI: `shipproof` is taken (E16). Version 0.1.0, uploaded 2026-08-08, MIT, from GitHub user Hurshid87 (E17). Summary: "Prove a deploy actually landed. Don't take the agent's word for it." It is a CLI that verifies AI coding agents' deploy claims. Same domain as our tool (verifying coding-agent claims), same artefact type (Python CLI).
- npm: `shipproof` is taken (E19), latest 0.2.0, published 2026-07-19 by CalvaryBloom: "Zero-config release readiness checks for AI-assisted projects."
- GitHub: `github.com/shipproof` returns 404 (no user/org) (E22); `github.com/ANI-IN/shipproof` returns 404 (E22). Repository search returns 31 repositories named shipproof or similar (E18), many created between April and October 2026 in the same niche, for example `WhorideChicken/shipproof` ("Evidence-driven acceptance gate for AI-generated software changes"), `lianmt/shipproof` ("Tamper-aware acceptance contracts and deterministic evidence for AI coding agents"), `mjcole76/shipproof` ("Evidence before merge - deterministic verification for agent-written software"), `kingggg5/shipproof` (Codex/Claude plugin, 18 stars), `CalvaryBloom/shipproof`, `aryan877/shipproof`.
- Web: shipproof.io is a live product named "ShipProof" (social-proof widget for indie hackers) (E20); Propel Apps markets a "ShipProof" feature in supply-chain software (E21).

Verdict: meaningful clash. The PyPI and npm names are taken, and several projects with the same name do the same kind of thing (evidence gates for AI-written code). `pip install shipproof` would install someone else's package.

Alternatives (each returned 404 on PyPI JSON API, npm registry, `github.com/<name>` and `github.com/ANI-IN/<name>`, including the hyphenated form; GitHub repository search returned 0 repositories; a web search for the three terms returned no software matches):

| name | PyPI | npm | github.com/<name> | GitHub repo search | rationale |
|---|---|---|---|---|---|
| testvetter | free | free | free | 0 | describes vetting LLM-written tests |
| proofsieve | free | free | free | 0 | keeps the "proof" idea; a sieve that filters tests |
| keptests | free | free | free | 0 | names the output (tests that were kept) |

Checked and rejected: testsieve (2 repos), keepgate (3 repos), provegate (npm and GitHub org taken), testwarden (GitHub user taken), sievetest (CRAN package mirror), mergeproof (PyPI taken). Availability is as of 2026-10-16; register the PyPI name early if one is chosen. No trademark search was done.

## Open gaps

- Runtimes were measured on one Windows laptop only; not repeated on Linux/macOS. Both picks have exactly one Windows-only baseline failure (boltons `test_reverse_iter_lines`, WTForms `test_date.py::test_basic`); the harness needs a known-failures list or a Linux/WSL run target.
- The other shortlist candidates (humanize, marshmallow, toolz, cattrs, semver, dateutil, more-itertools) were not run; they were rejected on module-size, maintenance or dependency grounds from source inspection.
- Mutant opportunities above are one-line sketches from module structure and function names; the specific lines for the ~4 mutants per module still need to be chosen and validated (each mutant must be killed by at least one upstream or reference test, and must not be equivalent).
- Per-module upstream test runtimes were not split out for boltons and WTForms (whole suites run in under 4 s, so not expected to matter).
- htmx-ext-sse has no `license` field in npm metadata; the htmx-extensions repository license was not verified.
- HTMX 4 SSE extension details (file name and event names) were taken from a search summary of four.htmx.org, not read directly.
- No trademark or company-registry search for the alternative names.
- mutmut was not installed or run; the assessment is from its 3.8.0 README.
