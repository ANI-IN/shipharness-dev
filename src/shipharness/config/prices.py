"""Model prices from `config/prices.toml` (CONTRACTS §2)."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

# src/shipharness/config/prices.py -> repository root is three levels above the package directory.
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PRICES_FILE = REPO_ROOT / "config" / "prices.toml"

_REQUIRED = ("input", "cached_input", "cache_write", "output")


class UnknownModelPrice(KeyError):
    """Raised when a model has no entry in the prices file (no silent zero cost)."""


@dataclass(frozen=True)
class ModelPrice:
    """USD per 1M tokens."""

    input: float
    cached_input: float
    cache_write: float
    output: float


@dataclass(frozen=True)
class Prices:
    models: dict[str, ModelPrice]
    source_file: Path

    @classmethod
    def load(cls, path: Path = DEFAULT_PRICES_FILE) -> Prices:
        data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
        models: dict[str, ModelPrice] = {}
        for name, entry in data.get("models", {}).items():
            missing = [field for field in _REQUIRED if field not in entry]
            if missing:
                raise ValueError(f"prices for {name!r} missing fields: {', '.join(missing)}")
            models[name] = ModelPrice(**{field: float(entry[field]) for field in _REQUIRED})
        return cls(models=models, source_file=Path(path))

    def get(self, model: str) -> ModelPrice:
        try:
            return self.models[model]
        except KeyError:
            raise UnknownModelPrice(
                f"no price for model {model!r} in {self.source_file}; add it before running"
            ) from None
