"""`shipharness testgen`: filtered test generation (the integrator wires `register` into cli.py)."""

from __future__ import annotations

from pathlib import Path

import typer

from shipharness.config import Settings
from shipharness.runner.model import ModelClient, OpenAIModelClient
from shipharness.sandbox import UNSANDBOXED_BANNER


class MissingKey(RuntimeError):
    pass


def load_settings() -> Settings:
    return Settings()


def make_client(settings: Settings) -> ModelClient:
    """Production OpenAI client (max_retries=0: the runner classifies and retries errors)."""
    if settings.openai_api_key is None:
        raise MissingKey("OPENAI_API_KEY is missing: add it to .env at the repo root")
    from openai import OpenAI

    from shipharness.tracing import make_tracer

    raw = OpenAI(api_key=settings.openai_api_key.get_secret_value(), max_retries=0)
    return OpenAIModelClient(make_tracer(settings, "shipharness-testgen").wrap_openai(raw))


def _cost_line(spent_usd: float, note: str) -> None:
    typer.echo(f"Cost: ${spent_usd:.6f} ({note})")


def register(app: typer.Typer) -> None:
    @app.command()
    def testgen(
        repo: Path = typer.Option(..., help="Repository with a pytest suite."),
        module: str = typer.Option(..., help="Repo-relative path of the module to test."),
        layers: str = typer.Option("none", help="none or verify."),
        max_tests: int = typer.Option(10, "--max-tests", help="Test functions to evaluate."),
        sandbox: str = typer.Option(
            "",
            help="local (UNSANDBOXED, your environment) or docker; default: docker with "
            "--image, else local.",
        ),
        image: str = typer.Option("", help="Prepared container image for this repo."),
        tests: list[str] = typer.Option(  # noqa: B008
            [], "--tests", help="Existing test paths (default: the repo's configured suite)."
        ),
        python: str = typer.Option("python", help="Python command inside the sandbox."),
        out: Path | None = typer.Option(None, help="Directory for kept tests and the report."),
        doctest_modules: bool = typer.Option(
            False,
            "--doctest-modules/--no-doctest-modules",
            help="Run the existing suite with --doctest-modules, so the module's doctests "
            "count in the baseline (filter 3 and mutant kills).",
        ),
    ) -> None:
        """Generate tests for one module and keep only those that pass all five filters."""
        from shipharness.testgen.run import TestgenOptions, run_testgen

        kind = sandbox or ("docker" if image else "local")
        if kind not in ("local", "docker"):
            typer.echo(f"x --sandbox must be local or docker, got {kind!r}")
            _cost_line(0.0, "no model calls")
            raise typer.Exit(1)
        if kind == "docker" and not image:
            typer.echo("x --sandbox docker needs --image (a prepared image for this repo)")
            _cost_line(0.0, "no model calls")
            raise typer.Exit(1)
        if not repo.is_dir():
            typer.echo(f"x repository not found: {repo}")
            _cost_line(0.0, "no model calls")
            raise typer.Exit(1)
        settings = load_settings()
        try:
            client = make_client(settings)
        except MissingKey as exc:
            typer.echo(f"x {exc}")
            _cost_line(0.0, "no model calls")
            raise typer.Exit(1) from None
        if kind == "local":
            typer.echo(f"! {UNSANDBOXED_BANNER}: generated tests run on this machine")
        options = TestgenOptions(
            repo=repo,
            module=module,
            layers=layers,
            max_tests=max_tests,
            sandbox=kind,  # type: ignore[arg-type]
            image=image or None,
            existing_tests=list(tests),
            python=python,
            out_dir=out,
            doctest_modules=doctest_modules,
        )
        result = run_testgen(options, settings, client=client)
        if result.baseline_includes_doctests:
            typer.echo("Baseline: existing suite with doctests (--doctest-modules)")
        else:
            typer.echo("Baseline: existing suite without doctests")
        evaluated = len({r.test_id for r in result.results})
        typer.echo(
            f"testgen {result.run_id}: {result.status}; kept {len(result.kept)} of "
            f"{evaluated} proposed tests"
        )
        for test_id in result.kept:
            typer.echo(f"+ {test_id}")
        for test_id, res in result.discarded.items():
            typer.echo(f"- {test_id}: filter {res.filter}: {res.reason}")
        for test_id in result.not_evaluated:
            typer.echo(f"- {test_id}: not evaluated (over --max-tests {max_tests})")
        if result.error:
            typer.echo(f"x {result.error}")
        if result.out_dir is not None and result.out_dir.exists():
            typer.echo(f"Kept tests and report: {result.out_dir}")
        _cost_line(result.cost_usd, f"testgen, model {settings.openai_model}")
        raise typer.Exit(result.exit_code)
