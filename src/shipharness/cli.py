"""Command-line entry point: `shipharness <command>`."""

from __future__ import annotations

import typer

from shipharness import __version__

app = typer.Typer(
    name="shipharness",
    help="Harness engineering for coding agents.",
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"shipharness {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", callback=_version_callback, is_eager=True, help="Show the version."
    ),
) -> None:
    """Harness engineering for coding agents."""
