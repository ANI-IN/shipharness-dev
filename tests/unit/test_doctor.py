from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from shipharness.config import Settings
from shipharness.doctor import DoctorReport, run_doctor

from .fakes import fake_langsmith_key, fake_openai_key


class FakeAuthError(Exception):
    status_code = 401


class APIConnectionError(Exception):
    pass


class Probes:
    def __init__(self, openai_exc: Exception | None = None, langsmith_exc: Exception | None = None):
        self.openai_exc, self.langsmith_exc = openai_exc, langsmith_exc
        self.calls: list[str] = []

    def openai(self, settings: Settings) -> None:
        self.calls.append("openai")
        if self.openai_exc:
            raise self.openai_exc

    def langsmith(self, settings: Settings) -> None:
        self.calls.append("langsmith")
        if self.langsmith_exc:
            raise self.langsmith_exc


def which_all(name: str) -> str | None:
    return f"/usr/bin/{name}"


def settings_with_keys(monkeypatch: pytest.MonkeyPatch) -> Settings:
    monkeypatch.setenv("OPENAI_API_KEY", fake_openai_key())
    monkeypatch.setenv("LANGSMITH_API_KEY", fake_langsmith_key())
    return Settings(_env_file=None)


def settings_without_keys(monkeypatch: pytest.MonkeyPatch) -> Settings:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)
    return Settings(_env_file=None)


def status(report: DoctorReport, name: str) -> str:
    return next(c.status for c in report.checks if c.name == name)


def test_missing_keys_are_reported_with_next_step(monkeypatch: pytest.MonkeyPatch) -> None:
    report = run_doctor(
        settings_without_keys(monkeypatch), offline=False, probes=Probes(), which=which_all
    )
    for name in ("OPENAI_API_KEY", "LANGSMITH_API_KEY"):
        check = next(c for c in report.checks if c.name == name)
        assert check.status == "missing"
        assert "add it to .env at the repo root" in check.next_step
    assert report.ok is False


def test_valid_keys_are_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    probes = Probes()
    report = run_doctor(
        settings_with_keys(monkeypatch), offline=False, probes=probes, which=which_all
    )
    assert status(report, "OPENAI_API_KEY") == "ok"
    assert status(report, "LANGSMITH_API_KEY") == "ok"
    assert probes.calls == ["openai", "langsmith"]


def test_auth_error_is_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    report = run_doctor(
        settings_with_keys(monkeypatch),
        offline=False,
        probes=Probes(openai_exc=FakeAuthError("bad key")),
        which=which_all,
    )
    assert status(report, "OPENAI_API_KEY") == "invalid"
    assert report.ok is False


def test_connection_error_is_unreachable(monkeypatch: pytest.MonkeyPatch) -> None:
    report = run_doctor(
        settings_with_keys(monkeypatch),
        offline=False,
        probes=Probes(langsmith_exc=APIConnectionError("down")),
        which=which_all,
    )
    assert status(report, "LANGSMITH_API_KEY") == "unreachable"


def test_offline_skips_probes(monkeypatch: pytest.MonkeyPatch) -> None:
    probes = Probes()
    report = run_doctor(
        settings_with_keys(monkeypatch), offline=True, probes=probes, which=which_all
    )
    assert probes.calls == []
    check = next(c for c in report.checks if c.name == "OPENAI_API_KEY")
    assert check.status == "ok" and "not verified" in check.detail


def test_missing_docker_is_a_warning_not_a_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def which(name: str) -> str | None:
        return None if name in ("docker", "podman") else f"/usr/bin/{name}"

    report = run_doctor(
        settings_with_keys(monkeypatch), offline=False, probes=Probes(), which=which
    )
    check = next(c for c in report.checks if c.name == "container runtime")
    assert check.status == "warn"
    assert "UNSANDBOXED" in check.detail
    assert report.ok is True


def test_report_never_echoes_any_part_of_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    key = fake_openai_key()
    leaky = FakeAuthError(f"Incorrect API key provided: {key[:8]}****{key[-6:]}")
    report = run_doctor(
        settings_with_keys(monkeypatch),
        offline=False,
        probes=Probes(openai_exc=leaky),
        which=which_all,
    )
    text = report.render()
    for start in range(len(key) - 5):
        assert key[start : start + 6] not in text


def test_cli_exit_code_and_output(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from shipharness import cli

    settings_without_keys(monkeypatch)
    monkeypatch.setattr(cli, "load_settings", lambda: Settings(_env_file=None))
    result = CliRunner().invoke(cli.app, ["doctor", "--offline"])
    assert result.exit_code == 1
    assert "x missing" in result.output
    assert "OPENAI_API_KEY" in result.output
