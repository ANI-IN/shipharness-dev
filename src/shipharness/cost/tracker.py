"""CostTracker: token usage x prices, with run, review, batch, session, experiment caps."""

from __future__ import annotations

import json
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from shipharness.config import ModelPrice, Prices, Settings

ScopeKind = Literal["run", "review"]
CapScope = Literal["run", "review", "session", "batch", "experiment"]


class Usage(BaseModel):
    model_config = ConfigDict(frozen=True)

    input_tokens: int = 0  # total input, including cached and cache-write tokens
    cached_tokens: int = 0  # usage.input_tokens_details.cached_tokens
    cache_write_tokens: int = 0  # usage.input_tokens_details.cache_write_tokens
    output_tokens: int = 0  # includes reasoning tokens
    reasoning_tokens: int = 0  # usage.output_tokens_details.reasoning_tokens


class CapExceeded(Exception):
    def __init__(self, scope: CapScope, limit_usd: float, spent_usd: float) -> None:
        super().__init__(f"cost cap reached: {scope} ${spent_usd:.4f} of ${limit_usd:.2f}")
        self.scope = scope
        self.limit_usd = limit_usd
        self.spent_usd = spent_usd


@dataclass(frozen=True)
class Caps:
    run: float
    review: float
    session: float
    batch: float
    experiment: float

    @classmethod
    def from_settings(cls, settings: Settings, *, final: bool = False) -> Caps:
        return cls(
            run=settings.max_final_run_cost_usd if final else settings.max_run_cost_usd,
            review=settings.max_review_cost_usd,
            session=settings.max_session_cost_usd,
            batch=settings.max_batch_cost_usd,
            experiment=settings.max_experiment_total_usd,
        )


@dataclass
class CostScope:
    kind: ScopeKind
    key: str
    limit_usd: float
    spent_usd: float = 0.0


@dataclass(frozen=True)
class CostSummary:
    total_usd: float
    by_model: dict[str, float]
    by_key: dict[str, float]
    batch_total_usd: float
    session_total_usd: float
    experiment_total_usd: float
    caps: Caps
    experiment: bool = False

    def remaining(self) -> dict[str, float]:
        return {
            "batch": round(self.caps.batch - self.batch_total_usd, 6),
            "session": round(self.caps.session - self.session_total_usd, 6),
            "experiment": round(self.caps.experiment - self.experiment_total_usd, 6),
        }


def cost_of(price: ModelPrice, usage: Usage) -> float:
    uncached = max(usage.input_tokens - usage.cached_tokens - usage.cache_write_tokens, 0)
    return (
        uncached * price.input
        + usage.cached_tokens * price.cached_input
        + usage.cache_write_tokens * price.cache_write
        + usage.output_tokens * price.output
    ) / 1e6


def usage_from_openai(resp_usage: Any) -> Usage:
    """Build Usage from an OpenAI Responses `usage` object, tolerating missing fields."""

    def num(obj: Any, name: str) -> int:
        value = getattr(obj, name, 0) if obj is not None else 0
        return int(value or 0)

    input_details = getattr(resp_usage, "input_tokens_details", None)
    output_details = getattr(resp_usage, "output_tokens_details", None)
    return Usage(
        input_tokens=num(resp_usage, "input_tokens"),
        cached_tokens=num(input_details, "cached_tokens"),
        cache_write_tokens=num(input_details, "cache_write_tokens"),
        output_tokens=num(resp_usage, "output_tokens"),
        reasoning_tokens=num(output_details, "reasoning_tokens"),
    )


@dataclass
class CostTracker:
    """Records every model call in an append-only ledger and enforces caps.

    `session_id` groups class-session spend (persisted across commands); `experiment=True` marks
    pre-class experiment spend, which counts toward the experiment total instead of the session.
    The batch total covers this tracker instance (one command).
    """

    prices: Prices
    caps: Caps
    ledger_path: Path
    session_id: str
    experiment: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _batch: float = field(default=0.0, init=False)
    _session: float = field(default=0.0, init=False)
    _experiment: float = field(default=0.0, init=False)
    _by_model: dict[str, float] = field(default_factory=lambda: defaultdict(float), init=False)
    _by_key: dict[str, float] = field(default_factory=lambda: defaultdict(float), init=False)

    def __post_init__(self) -> None:
        self.ledger_path = Path(self.ledger_path)
        if self.ledger_path.exists():
            for line in self.ledger_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                if entry.get("experiment"):
                    self._experiment += entry["cost_usd"]
                elif entry.get("session") == self.session_id:
                    self._session += entry["cost_usd"]

    @property
    def batch_total_usd(self) -> float:
        return self._batch

    @property
    def session_total_usd(self) -> float:
        return self._session

    @property
    def experiment_total_usd(self) -> float:
        return self._experiment

    def scope(self, kind: ScopeKind, key: str, limit_usd: float) -> CostScope:
        return CostScope(kind=kind, key=key, limit_usd=limit_usd)

    def _active_limits(self, scope: CostScope) -> list[tuple[CapScope, float, float]]:
        limits: list[tuple[CapScope, float, float]] = [
            (scope.kind, scope.limit_usd, scope.spent_usd),
            ("batch", self.caps.batch, self._batch),
        ]
        if self.experiment:
            limits.append(("experiment", self.caps.experiment, self._experiment))
        else:
            limits.append(("session", self.caps.session, self._session))
        return limits

    def check_before_call(
        self, scope: CostScope, model: str, est_input_tokens: int, max_output_tokens: int
    ) -> None:
        """Raise CapExceeded if the worst case of the next call would cross any active cap."""
        price = self.prices.get(model)
        worst = (
            est_input_tokens * max(price.input, price.cache_write)
            + max_output_tokens * price.output
        ) / 1e6
        with self._lock:
            for name, limit, spent in self._active_limits(scope):
                if spent + worst > limit:
                    raise CapExceeded(name, limit, spent)

    def record(self, scope: CostScope, model: str, usage: Usage) -> float:
        """Record one call. Raises CapExceeded after recording if a cap is now crossed."""
        cost = round(cost_of(self.prices.get(model), usage), 9)
        entry = {
            "ts": datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "session": self.session_id,
            "experiment": self.experiment,
            "kind": scope.kind,
            "key": scope.key,
            "model": model,
            **usage.model_dump(),
            "cost_usd": cost,
        }
        with self._lock:
            self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
            with self.ledger_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")
            scope.spent_usd += cost
            self._batch += cost
            if self.experiment:
                self._experiment += cost
            else:
                self._session += cost
            self._by_model[model] += cost
            self._by_key[scope.key] += cost
            for name, limit, spent in self._active_limits(scope):
                if spent > limit:
                    raise CapExceeded(name, limit, spent)
        return cost

    def summary(self) -> CostSummary:
        with self._lock:
            return CostSummary(
                total_usd=self._batch,
                by_model=dict(self._by_model),
                by_key=dict(self._by_key),
                batch_total_usd=self._batch,
                session_total_usd=self._session,
                experiment_total_usd=self._experiment,
                caps=self.caps,
                experiment=self.experiment,
            )
