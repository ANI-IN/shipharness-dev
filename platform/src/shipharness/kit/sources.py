"""Where each kit template comes from, and the TeamTrack example values it shows.

The kit's example values are TeamTrack's. Files the harness renders at run time (progress.md,
session-handoff.md, init.sh, the exec plan, feature_list.json) are rendered here with the harness's
own functions for TeamTrack's feature F1, so a test can compare the kit copy with a fresh rendering
and fail when the source changes. Print one rendering to recopy a template:

    uv run python -m shipharness.kit.sources progress.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from shipharness.config.prices import REPO_ROOT
from shipharness.layout import APP_DIR, DATASETS_DIR

INSTRUCTIONS = REPO_ROOT / APP_DIR / "harness" / "instructions"
FEATURES_FILE = REPO_ROOT / DATASETS_DIR / "teamtrack-features-v1.jsonl"
EXAMPLE_ID = "F1-canonical"
# TeamTrack's A/B runs leave `steps` empty (the dataset has none). The kit shows observable steps
# instead, each one shortened from a sentence of the API section of
# platform/teamtrack/docs/features/f1.md.
F1_STEPS = (
    "GET /issues lists the caller's org's issues across its projects.",
    "Filters are optional and combine with AND.",
    "Deleted issues and issues of archived projects are never listed.",
    "A project_id or assignee_id that is not in the caller's org gives 404 not_found.",
    "An invalid value gives 422 validation_error.",
    "Any role may read (admin, member, viewer). Without a token: 401.",
)

# kit template -> TeamTrack instructions file it is copied from (marker lines added, walkthrough
# marker lines left out). "subset" files keep only some of the source lines, in order.
COPIED: dict[str, str] = {
    "ARCHITECTURE.md": "ARCHITECTURE.md",
    "docs/SECURITY.md": "docs/SECURITY.md",
    "docs/RELIABILITY.md": "docs/RELIABILITY.md",
    "docs/QUALITY_SCORE.md": "docs/QUALITY_SCORE.md",
    "docs/PLANS.md": "docs/PLANS.md",
    "docs/design-docs/index.md": "docs/design-docs/index.md",
    "docs/design-docs/core-beliefs.md": "docs/design-docs/core-beliefs.md",
    "docs/design-docs/api-conventions.md": "docs/design-docs/api-conventions.md",
    "docs/design-docs/cursor-pagination.md": "docs/design-docs/cursor-pagination.md",
    "docs/product-specs/teamtrack-base.md": "docs/product-specs/teamtrack-base.md",
    "docs/product-specs/f1.md": "docs/product-specs/f1.md",
    "docs/references/alembic-llms.txt": "docs/references/alembic-llms.txt",
    "docs/references/import-linter-llms.txt": "docs/references/import-linter-llms.txt",
}
SUBSET: dict[str, str] = {"docs/product-specs/index.md": "docs/product-specs/index.md"}
# kit template -> source whose every line appears in the kit file, in order (the kit adds lines).
EXTENDED: dict[str, str] = {"AGENTS.md": "AGENTS.md"}
# kit template -> harness asset rendered for F1 (marker lines added).
RENDERED: dict[str, str] = {
    "progress.md": "progress.md",
    "session-handoff.md": "session-handoff.md",
    "init.sh": "init.sh",
    "docs/exec-plans/active/F1.md": "exec-plan.md",
}


def example_line() -> dict[str, Any]:
    for line in FEATURES_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            data = json.loads(line)
            if data.get("metadata", {}).get("example_id") == EXAMPLE_ID:
                return data
    raise LookupError(f"{EXAMPLE_ID} not in {FEATURES_FILE}")


def example_spec() -> Any:
    from shipharness.runner.models import AgentRunSpec

    inputs = example_line()["inputs"]
    return AgentRunSpec(
        run_id="kit-example",
        arm="harness",
        feature_id=inputs["feature_id"],
        checkpoint=inputs["checkpoint"],
        ticket_text=inputs["ticket_text"],
        layers=frozenset({"instructions", "state", "scope", "verify"}),
        model="kit-example",
        reasoning_effort="medium",
        workspace=Path("."),
    )


def example_description() -> str:
    return str(example_line()["metadata"]["description"])


def rendered(asset: str) -> str:
    """A harness state asset rendered for TeamTrack's F1, exactly as the harness would."""
    from shipharness.harness.state.templates import fields, render

    values = fields(example_spec(), example_description(), list(F1_STEPS))
    return render(asset, values).decode("utf-8")


def feature_document() -> dict[str, Any]:
    """feature_list.json for F1, as the harness's scope layer writes it."""
    from shipharness.harness.scope.features import build_feature
    from shipharness.harness.scope.features import render as render_features

    feature = build_feature(example_spec(), "feature", example_description(), list(F1_STEPS))
    return json.loads(render_features(feature))


def schema_document() -> dict[str, Any]:
    from shipharness.harness.scope.features import SCHEMA_ASSET

    return json.loads(SCHEMA_ASSET.read_text(encoding="utf-8"))


def session_steps() -> tuple[str, str]:
    """(getting up to speed, wrap-up) texts the harness gives the agent for F1."""
    from shipharness.harness.state.lifecycle import getting_up_to_speed, wrapup_text

    spec = example_spec()
    return getting_up_to_speed(spec), wrapup_text(spec)


def source_text(rel: str) -> str:
    """The TeamTrack instructions file `rel`, without walkthrough marker lines."""
    text = (INSTRUCTIONS / rel).read_text(encoding="utf-8")
    return "".join(ln for ln in text.splitlines(keepends=True) if "[walkthrough:" not in ln)


def main(argv: list[str]) -> int:
    names = {**RENDERED, "feature_list.json": "", "feature_list.schema.json": ""}
    if len(argv) != 1 or argv[0] not in names:
        print(f"usage: python -m shipharness.kit.sources <{'|'.join(sorted(names))}>")
        return 2
    if argv[0] == "feature_list.json":
        print(json.dumps(feature_document(), indent=2, ensure_ascii=False))
    elif argv[0] == "feature_list.schema.json":
        print(json.dumps(schema_document(), indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(rendered(RENDERED[argv[0]]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
