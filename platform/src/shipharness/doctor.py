"""`shipharness doctor`: environment checks. Never prints any part of a key."""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Callable
from typing import Literal, Protocol

import httpx
from pydantic import BaseModel

from shipharness.config import Prices, Settings, UnknownModelPrice
from shipharness.config.prices import REPO_ROOT

Status = Literal["ok", "missing", "invalid", "unreachable", "warn"]
_SYMBOL = {"ok": "+", "missing": "x", "invalid": "x", "unreachable": "!", "warn": "!"}
_FAILING = {"missing", "invalid", "unreachable"}


class DoctorCheck(BaseModel):
    name: str
    status: Status
    detail: str = ""
    next_step: str = ""


class DoctorReport(BaseModel):
    checks: list[DoctorCheck]

    @property
    def ok(self) -> bool:
        return not any(c.status in _FAILING for c in self.checks)

    def render(self) -> str:
        lines = ["shipharness doctor"]
        for check in self.checks:
            lines.append(
                f"  {_SYMBOL[check.status]} {check.status:<11} {check.name:<22} {check.detail}"
            )
            if check.next_step and check.status != "ok":
                lines.append(f"    next step: {check.next_step}")
        lines.append("  result: " + ("+ ready" if self.ok else "x not ready (fix the items above)"))
        return "\n".join(lines)


class DoctorProbes(Protocol):
    def openai(self, settings: Settings) -> None: ...
    def langsmith(self, settings: Settings) -> None: ...


class KeyRejected(Exception):
    """The service answered 401 or 403 for the configured key."""

    def __init__(self, status_code: int) -> None:
        super().__init__(f"status {status_code}")
        self.status_code = status_code


class ServiceHTTPError(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"status {status_code}")
        self.status_code = status_code


class RealProbes:
    """Cheapest authenticated call for each service; no model tokens are used."""

    def __init__(self, http: httpx.Client | None = None) -> None:
        self.http = http

    def openai(self, settings: Settings) -> None:
        from openai import OpenAI

        assert settings.openai_api_key is not None
        client = OpenAI(
            api_key=settings.openai_api_key.get_secret_value(), max_retries=0, timeout=20
        )
        client.models.list()

    def langsmith(self, settings: Settings) -> None:
        """GET /api/v1/sessions?limit=1 and check the status code directly: an invalid key gives
        HTTP 403, which the SDK surfaces only as a generic LangSmithError."""
        assert settings.langsmith_api_key is not None
        http = self.http or httpx.Client(timeout=20)
        response = http.get(
            f"{settings.langsmith_endpoint.rstrip('/')}/api/v1/sessions",
            params={"limit": 1},
            headers={"x-api-key": settings.langsmith_api_key.get_secret_value()},
        )
        if response.status_code in (401, 403):
            raise KeyRejected(response.status_code)
        if response.status_code >= 400:
            raise ServiceHTTPError(response.status_code)


_AUTH_NAMES = {
    "AuthenticationError",
    "PermissionDeniedError",
    "LangSmithAuthError",
    "LangSmithError",
    "KeyRejected",
}


def _classify(exc: BaseException, service: str) -> tuple[Status, str]:
    """Map a probe failure to a status. Uses only the class name and status code, never the
    message, because provider messages can echo part of the key."""
    name = type(exc).__name__
    status = getattr(exc, "status_code", None)
    if status in (401, 403) or name in _AUTH_NAMES:
        return (
            "invalid",
            f"{service} key invalid (rejected by {service}, {name}, status {status or 'n/a'})",
        )
    if "Connect" in name or "Timeout" in name or isinstance(exc, OSError | httpx.TransportError):
        return "unreachable", f"could not reach {service} ({name})"
    return "invalid", f"unexpected error from {service} ({name}, status {status or 'n/a'})"


def _key_check(
    name: str, present: bool, offline: bool, probe: Callable[[], None], service: str
) -> DoctorCheck:
    if not present:
        return DoctorCheck(
            name=name,
            status="missing",
            detail="not set",
            next_step=f"{name} is missing: add it to .env at the repo root",
        )
    if offline:
        return DoctorCheck(name=name, status="ok", detail="set (not verified: --offline)")
    try:
        probe()
    except Exception as exc:  # noqa: BLE001 - every failure is classified and reported
        status, detail = _classify(exc, service)
        step = (
            f"check {name} in .env (create a new key in your {service} account)"
            if status == "invalid"
            else "check your network connection and retry"
        )
        return DoctorCheck(name=name, status=status, detail=detail, next_step=step)
    return DoctorCheck(name=name, status="ok", detail=f"accepted by {service}")


def run_doctor(
    settings: Settings,
    *,
    offline: bool,
    probes: DoctorProbes | None = None,
    which: Callable[[str], str | None] = shutil.which,
) -> DoctorReport:
    probes = probes or RealProbes()
    checks: list[DoctorCheck] = []
    version = sys.version_info
    checks.append(
        DoctorCheck(
            name="python",
            status="ok" if version >= (3, 12) else "invalid",
            detail=f"{version.major}.{version.minor}.{version.micro}",
            next_step="install Python 3.12 or newer (uv python install 3.12)",
        )
    )
    for tool, required in (("git", True), ("uv", False)):
        found = which(tool)
        checks.append(
            DoctorCheck(
                name=tool,
                status="ok" if found else ("missing" if required else "warn"),
                detail=found or "not found on PATH",
                next_step=f"install {tool}",
            )
        )
    runtime = which(settings.sandbox_runtime)
    checks.append(
        DoctorCheck(
            name="container runtime",
            status="ok" if runtime else "warn",
            detail=(
                f"{settings.sandbox_runtime} at {runtime}"
                if runtime
                else f"{settings.sandbox_runtime} not found: only the UNSANDBOXED fallback can run"
            ),
            next_step="install Docker Desktop (WSL2 backend), Docker Engine, Podman, or Colima; "
            "see platform/sandbox/README.md",
        )
    )
    checks.append(
        _key_check(
            "OPENAI_API_KEY",
            settings.openai_api_key is not None,
            offline,
            lambda: probes.openai(settings),
            "OpenAI",
        )
    )
    checks.append(
        _key_check(
            "LANGSMITH_API_KEY",
            settings.langsmith_api_key is not None,
            offline,
            lambda: probes.langsmith(settings),
            "LangSmith",
        )
    )
    try:
        prices = Prices.load(settings.prices_file)
        for model in (settings.openai_model, settings.openai_eval_model):
            prices.get(model)
        checks.append(
            DoctorCheck(
                name="prices",
                status="ok",
                detail=f"{settings.openai_model}, {settings.openai_eval_model}",
            )
        )
    except (UnknownModelPrice, FileNotFoundError, ValueError) as exc:
        checks.append(
            DoctorCheck(
                name="prices",
                status="invalid",
                detail=type(exc).__name__,
                next_step=f"add the configured models to {settings.prices_file}",
            )
        )
    tracked = (
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", ".env"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )
    checks.append(
        DoctorCheck(
            name=".env not in git",
            status="invalid" if tracked else "ok",
            detail="tracked by git" if tracked else "not tracked",
            next_step="git rm --cached .env (keep the file, stop tracking it)",
        )
    )
    return DoctorReport(checks=checks)
