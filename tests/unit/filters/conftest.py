from __future__ import annotations

import os
from collections.abc import Iterator

import pytest


@pytest.fixture(autouse=True, scope="session")
def _fast_child_pytest() -> Iterator[None]:
    """Child pytest processes started through LocalSandbox inherit the environment. The dev
    environment has heavy pytest plugins (hypothesis, schemathesis, langsmith) that the trusted
    fixture repos and TeamTrack's visible tests do not use; skipping their autoload saves about
    two seconds per child run."""
    old = os.environ.get("PYTEST_DISABLE_PLUGIN_AUTOLOAD")
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    yield
    if old is None:
        os.environ.pop("PYTEST_DISABLE_PLUGIN_AUTOLOAD", None)
    else:
        os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = old
