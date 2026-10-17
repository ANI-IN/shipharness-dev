"""Readable names for the course features.

Each feature in `teamtrack-features-v1` has one command alias (`version-checks` for F4). Commands
and make targets accept the alias or the code, in any case, and normalise it to the code with
`feature_code`; the dataset, scores, and exports keep the code. Terminal and console output show
`feature_label`: the code with the plain name next to it ("F4 version checks").
"""

from __future__ import annotations

import re

FEATURE_ALIASES: dict[str, str] = {
    "F1": "org-search",
    "F2": "comments",
    "F3": "idempotent-create",
    "F4": "version-checks",
    "F5": "bulk-close",
    "F6": "watchers",
    "F7": "labels",
}
_BY_ALIAS = {alias: code for code, alias in FEATURE_ALIASES.items()}
_CODE = re.compile(r"[A-Za-z][0-9]+")


class UnknownFeature(ValueError):
    """A feature name that is neither an alias nor a code."""


def valid_feature_names() -> str:
    """'org-search (F1), comments (F2), ...': every alias with its code."""
    return ", ".join(f"{alias} ({code})" for code, alias in FEATURE_ALIASES.items())


def feature_code(name: str) -> str:
    """The code for an alias or a code, in any case: `Version-Checks` and `f4` give `F4`. A code
    the dataset lacks passes through (the task lookup reports it); anything else is refused."""
    text = name.strip()
    if text.lower() in _BY_ALIAS:
        return _BY_ALIAS[text.lower()]
    if _CODE.fullmatch(text):
        return text.upper()
    raise UnknownFeature(
        f"unknown feature {name!r}: use a name or its code: {valid_feature_names()}"
    )


def plain_name(code: str) -> str | None:
    """'version checks' for F4; None for a code without an alias (control tasks)."""
    alias = FEATURE_ALIASES.get(code)
    return alias.replace("-", " ") if alias else None


def feature_label(code: str) -> str:
    """'F4 version checks': the code with its plain name, or the code alone."""
    name = plain_name(code)
    return f"{code} {name}" if name else code
