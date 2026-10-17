"""Run profiles: named sets of setting overrides, applied identically to both arms.

`standard` keeps the settings as loaded (the default for every command). `class` is for live class
runs only (`make demo-N`, `make final`, `make show-N`): reasoning effort low for the agent arms,
2 CPUs for every arm, referee, and preview container, and the OpenAI Fast tier for the agent
arms' model calls. The reviewer keeps OPENAI_EVAL_REASONING_EFFORT and never requests a tier.
"""

from __future__ import annotations

from typing import Any

from shipharness.config.settings import Settings

PROFILES: dict[str, dict[str, Any]] = {
    "standard": {},
    "class": {
        "openai_reasoning_effort": "low",
        "openai_service_tier": "fast",
        "sandbox_cpus": 2.0,
    },
}
PROFILE_HELP = "standard (settings as loaded) or class (live class runs: low effort, Fast, 2 CPUs)."


def apply_profile(settings: Settings, profile: str) -> Settings:
    """Settings with the profile's overrides; both arms read the same values."""
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile!r}: {', '.join(PROFILES)}")
    overrides = PROFILES[profile]
    return settings.model_copy(update=overrides) if overrides else settings
