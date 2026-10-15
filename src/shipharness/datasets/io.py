"""Validate dataset JSONL files and upload them to LangSmith (there is no JSONL uploader there)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from shipharness.config.prices import REPO_ROOT
from shipharness.datasets.schema import LINE_MODELS, DatasetKind

STANDARD_DATASETS: dict[DatasetKind, tuple[str, Path, int]] = {
    "features": (
        "teamtrack-features-v1",
        REPO_ROOT / "datasets" / "teamtrack-features-v1.jsonl",
        60,
    ),
    "testgen": ("testgen-targets-v1", REPO_ROOT / "datasets" / "testgen-targets-v1.jsonl", 40),
}


def _model_for(kind: str) -> type[BaseModel]:
    if kind not in LINE_MODELS:
        raise ValueError(f"unknown dataset kind {kind!r}; choose from {sorted(LINE_MODELS)}")
    return LINE_MODELS[kind]


def validate_file(path: Path, kind: DatasetKind) -> list[str]:
    """Return one message per invalid line (empty list = valid)."""
    model = _model_for(kind)
    errors: list[str] = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            model.model_validate(json.loads(line))
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: not valid JSON ({exc.msg})")
        except ValidationError as exc:
            for error in exc.errors():
                where = ".".join(str(part) for part in error["loc"])
                errors.append(f"line {number}: {where}: {error['msg']}")
    return errors


def load_lines(path: Path, kind: DatasetKind) -> list[BaseModel]:
    errors = validate_file(path, kind)
    if errors:
        raise ValueError(f"{path} has {len(errors)} invalid line(s); first: {errors[0]}")
    model = _model_for(kind)
    return [
        model.model_validate(json.loads(line))
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def build_examples(lines: list[BaseModel]) -> list[dict[str, Any]]:
    """LangSmith create_examples payloads: inputs, reference outputs, metadata, splits."""
    examples = []
    for line in lines:
        data = line.model_dump(mode="json")
        examples.append(
            {
                "inputs": data["inputs"],
                "outputs": data["outputs"],
                "metadata": data["metadata"],
                "split": data["split"],
            }
        )
    return examples


def upload(
    client: Any, dataset_name: str, examples: list[dict[str, Any]], description: str = ""
) -> int:
    """Create the dataset if needed and add the examples. Returns the number uploaded."""
    if client.has_dataset(dataset_name=dataset_name):
        dataset = client.read_dataset(dataset_name=dataset_name)
    else:
        dataset = client.create_dataset(dataset_name, description=description)
    client.create_examples(dataset_id=dataset.id, examples=examples)
    return len(examples)
