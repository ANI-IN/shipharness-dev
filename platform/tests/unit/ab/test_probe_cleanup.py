"""The LangSmith probe deletes everything it creates, including the experiment project."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from shipharness.layout import find_repo_root

SCRIPT = find_repo_root(Path(__file__)) / "platform" / "scripts" / "probe_langsmith.py"


def load_probe() -> Any:
    spec = importlib.util.spec_from_file_location("probe_langsmith", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeClient:
    def __init__(self, fail: set[str] | None = None) -> None:
        self.deleted: list[tuple[str, Any]] = []
        self.fail = fail or set()

    def delete_dataset(self, dataset_id: Any) -> None:
        self.deleted.append(("dataset", dataset_id))

    def delete_project(self, project_name: str) -> None:
        if project_name in self.fail:
            raise RuntimeError("nope")
        self.deleted.append(("project", project_name))


def test_cleanup_deletes_the_dataset_and_every_project() -> None:
    probe = load_probe()
    client = FakeClient()
    errors = probe.cleanup(client, "ds-1", ["shipharness-probe-abc", "shipharness-probe-exp-1"])
    assert errors == []
    assert client.deleted == [
        ("dataset", "ds-1"),
        ("project", "shipharness-probe-abc"),
        ("project", "shipharness-probe-exp-1"),
    ]


def test_cleanup_keeps_going_after_an_error() -> None:
    probe = load_probe()
    client = FakeClient(fail={"a"})
    assert probe.cleanup(client, "ds", ["a", "b"]) == ["a: RuntimeError"]
    assert ("project", "b") in client.deleted


def test_main_cleans_up_the_experiment_project() -> None:
    assert "results.experiment_name]" in SCRIPT.read_text(encoding="utf-8")
