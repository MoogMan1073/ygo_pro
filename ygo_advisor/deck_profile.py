"""Build a rich, JSON-able profile from a `.ydk` + the card database.

The profile is what the coaching layer reads: every card with its text and
roles, plus a breakdown (monsters / normal traps / hand traps / engine) and
a set of standard opening-hand probabilities computed exactly from the
deck's real copy counts.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field

from . import probability as prob
from . import roles as _roles
from .cards import CardDB, card_kind
from .ydk import Decklist


@dataclass
class CardEntry:
    id: int
    name: str
    copies: int
    kind: str
    roles: list[str]
    type: str = ""
    desc: str = ""


@dataclass
class DeckProfile:
    name: str
    main_size: int
    entries: list[CardEntry]
    extra_entries: list[CardEntry]
    counts: dict[str, int]          # kind -> number of cards in main
    role_counts: dict[str, int]     # role -> copies in main
    openers: dict[str, float]       # metric -> probability (going first, 5)

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    def role_copies(self, *role_tags: str) -> int:
        """Copies in the main deck carrying ANY of the given roles."""
        wanted = set(role_tags)
        return sum(
            e.copies for e in self.entries if wanted & set(e.roles)
        )


def _entries(id_list: list[int], db: CardDB) -> list[CardEntry]:
    out: list[CardEntry] = []
    for cid, copies in sorted(Counter(id_list).items()):
        card = db.get(cid)
        out.append(
            CardEntry(
                id=cid,
                name=db.name(cid),
                copies=copies,
                kind=card_kind(card) if card else "other",
                roles=sorted(_roles.roles_for(cid, card)),
                type=card.get("type", "") if card else "",
                desc=card.get("desc", "") if card else "",
            )
        )
    return out


def _role_copies(id_list: list[int], db: CardDB) -> Counter:
    rc: Counter = Counter()
    for cid in id_list:
        for role in _roles.roles_for(cid, db.get(cid)):
            rc[role] += 1
    return rc


def standard_openers(dl: Decklist, db: CardDB, hand_size: int = 5) -> dict[str, float]:
    """Exact opening-hand probabilities keyed by a human-readable label.

    Computed from the deck's real copy counts via the hypergeometric model.
    ``hand_size=5`` models going first; pass 6 for going second.
    """
    N = dl.main_size
    rc = _role_copies(dl.main, db)

    def copies_with(*tags: str) -> int:
        wanted = set(tags)
        total = 0
        for cid in set(dl.main):
            if wanted & _roles.roles_for(cid, db.get(cid)):
                total += dl.main.count(cid)
        return total

    def ids_with(*tags: str) -> set[int]:
        wanted = set(tags)
        return {cid for cid in set(dl.main)
                if wanted & _roles.roles_for(cid, db.get(cid))}

    def copies_of(ids: set[int]) -> int:
        return sum(dl.main.count(cid) for cid in ids)

    welcome_ids = ids_with("welcome_access")
    monster_ids = ids_with("labrynth_monster")
    welcome_access = copies_of(welcome_ids)
    lab_monster = copies_of(monster_ids)
    handtraps = copies_with("handtrap")
    any_trap = sum(1 for cid in dl.main if _roles.roles_for(cid, db.get(cid)) & {"trap", "normal_trap"})
    starters = copies_with(*_roles.STARTER_TAGS)

    out: dict[str, float] = {}
    if N == 0:
        return out
    out[f"open >=1 Welcome-access ({welcome_access} copies)"] = prob.at_least_one(N, welcome_access, hand_size)
    out[f"open >=1 Labrynth monster ({lab_monster} copies)"] = prob.at_least_one(N, lab_monster, hand_size)
    out[f"open >=1 hand trap ({handtraps} copies)"] = prob.at_least_one(N, handtraps, hand_size)
    out[f"open >=1 trap of any kind ({any_trap} copies)"] = prob.at_least_one(N, any_trap, hand_size)
    out[f"open >=1 starter ({starters} copies)"] = prob.at_least_one(N, starters, hand_size)
    # Combo: a Welcome-access trap AND a Labrynth monster to use it. The two
    # buckets are disjoint (traps vs monsters); fold any overlap into the
    # monster bucket so the groups stay disjoint for the exact calc.
    monster_only = copies_of(monster_ids - welcome_ids)
    out[f"open Welcome-access + Labrynth monster ({welcome_access}+{monster_only})"] = prob.all_groups_at_least(
        N, [(welcome_access, 1), (monster_only, 1)], hand_size
    )
    return out


def build_profile(dl: Decklist, db: CardDB, hand_size: int = 5) -> DeckProfile:
    entries = _entries(dl.main, db)
    extra_entries = _entries(dl.extra, db)
    counts: Counter = Counter()
    for cid in dl.main:
        card = db.get(cid)
        counts[card_kind(card) if card else "other"] += 1
    return DeckProfile(
        name=dl.name,
        main_size=dl.main_size,
        entries=entries,
        extra_entries=extra_entries,
        counts=dict(counts),
        role_counts=dict(_role_copies(dl.main, db)),
        openers=standard_openers(dl, db, hand_size),
    )
