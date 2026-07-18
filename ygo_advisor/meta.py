"""MasterDuelMeta tier-list snapshot access.

The site is API-backed (``/api/v1/...``), but the tier list is also a moving
target, so we store a dated JSON *snapshot* in ``data/meta/tier_list.json``
and read from it. Each top deck carries a set of **threat tags** — the
abstract things it does to you (special-summon spam, grave reliance, going
second power …) — which the flavor recommender matches tech cards against.

``refresh_from_web`` is a thin helper to pull the live tier list when you
want to update the snapshot; the exact API shape may drift, so it fails
soft and the snapshot remains the source of truth.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parent.parent / "data" / "meta" / "tier_list.json"


@dataclass
class MetaDeck:
    name: str
    tier: int
    power: float
    share: float          # % representation, 0 if unknown
    threats: list[str]

    @property
    def weight(self) -> float:
        """Field weight for scoring — prefer share when known, else power."""
        return self.share if self.share > 0 else self.power


@dataclass
class MetaSnapshot:
    source: str
    date: str
    format: str
    decks: list[MetaDeck]

    def top(self, n: int | None = None) -> list[MetaDeck]:
        ranked = sorted(self.decks, key=lambda d: d.weight, reverse=True)
        return ranked[:n] if n else ranked

    def threat_weights(self) -> dict[str, float]:
        """Total field weight behind each threat tag."""
        out: dict[str, float] = {}
        for d in self.decks:
            for t in d.threats:
                out[t] = out.get(t, 0.0) + d.weight
        return out


def load_snapshot(path: str | Path = SNAPSHOT) -> MetaSnapshot:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    decks = [MetaDeck(**d) for d in raw["decks"]]
    return MetaSnapshot(
        source=raw.get("source", ""),
        date=raw.get("date", ""),
        format=raw.get("format", "Master Duel"),
        decks=decks,
    )


def refresh_from_web(url: str = "https://www.masterduelmeta.com/api/v1/top-decks") -> list[dict]:
    """Best-effort pull of the live tier list. Returns raw records or [].

    Threat tags are curated (not in the API), so this is a data aid, not a
    full replacement for the snapshot.
    """
    import urllib.request

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ygo_advisor/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        return data if isinstance(data, list) else data.get("data", [])
    except Exception:
        return []
