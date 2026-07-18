"""Card database backed by the YGOPRODeck API with a local JSON cache.

We resolve card *passcodes* (the integers in a `.ydk`) to full card data:
name, type, race, attribute, ATK/DEF/level, effect text, archetype and
banlist status. Results are cached to ``data/cards_cache.json`` so normal
use never hits the network.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
DEFAULT_CACHE = Path(__file__).resolve().parent.parent / "data" / "cards_cache.json"
_UA = {"User-Agent": "ygo_advisor/0.1 (+https://github.com/MoogMan1073/ygo_pro)"}

# Fields we keep in the cache — enough to reason about a card without the bulk.
_KEEP = (
    "id", "name", "type", "frameType", "desc", "race", "attribute",
    "atk", "def", "level", "linkval", "scale", "archetype",
)


def _slim(card: dict) -> dict:
    out = {k: card[k] for k in _KEEP if k in card}
    bl = card.get("banlist_info", {})
    if bl:
        out["banlist"] = bl  # ban_tcg / ban_ocg / ban_goat
    return out


class CardDB:
    """Load/query cached card data; fetch missing cards on demand."""

    def __init__(self, cache_path: str | Path = DEFAULT_CACHE):
        self.cache_path = Path(cache_path)
        self.cards: dict[int, dict] = {}
        if self.cache_path.exists():
            raw = json.loads(self.cache_path.read_text(encoding="utf-8"))
            self.cards = {int(k): v for k, v in raw.items()}

    # -- lookup -----------------------------------------------------------
    def get(self, cid: int) -> dict | None:
        return self.cards.get(int(cid))

    def name(self, cid: int) -> str:
        c = self.get(cid)
        return c["name"] if c else f"<unknown {cid}>"

    def __contains__(self, cid: int) -> bool:
        return int(cid) in self.cards

    # -- fetching ---------------------------------------------------------
    def fetch(self, ids: list[int], sleep: float = 0.2) -> list[int]:
        """Fetch any of ``ids`` not already cached. Returns the ids fetched."""
        missing = sorted({int(i) for i in ids} - set(self.cards))
        if not missing:
            return []
        # YGOPRODeck accepts a comma-separated id list in one request.
        qs = urllib.parse.urlencode({"id": ",".join(str(i) for i in missing)})
        req = urllib.request.Request(f"{API}?{qs}", headers=_UA)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        for card in data.get("data", []):
            self.cards[int(card["id"])] = _slim(card)
        time.sleep(sleep)
        return missing

    def save(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        serial = {str(k): v for k, v in sorted(self.cards.items())}
        self.cache_path.write_text(
            json.dumps(serial, ensure_ascii=False, indent=1), encoding="utf-8"
        )


# -- category helpers (used by roles / deck_profile) ----------------------
def is_monster(card: dict) -> bool:
    return "Monster" in card.get("type", "")


def is_spell(card: dict) -> bool:
    return card.get("type", "") == "Spell Card"


def is_trap(card: dict) -> bool:
    return card.get("type", "") == "Trap Card"


def is_normal_trap(card: dict) -> bool:
    return is_trap(card) and card.get("race") == "Normal"


def is_extra_deck(card: dict) -> bool:
    ft = card.get("frameType", "")
    return ft in {"fusion", "synchro", "xyz", "link"} or any(
        t in card.get("type", "") for t in ("Fusion", "Synchro", "XYZ", "Link")
    )


def card_kind(card: dict) -> str:
    """Coarse kind label: monster / spell / trap / extra."""
    if is_extra_deck(card):
        return "extra"
    if is_monster(card):
        return "monster"
    if is_spell(card):
        return "spell"
    if is_trap(card):
        return "trap"
    return "other"
