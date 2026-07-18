"""Opening-hand evaluator.

Given a concrete hand (card names or passcodes) plus the deck and whether
you're on the play or the draw, classify each card, grade the hand, and
propose a turn-1 (or go-second) line with the key "if they have X" branches.

This is a Labrynth-aware but role-driven heuristic: it identifies the engine
starter, whether you can actually *use* it, and how much backup interaction
you have. It recommends and explains; the coaching layer refines with the
live matchup and your read. The exact odds of drawing hands like this come
from :mod:`ygo_advisor.probability`.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

from . import roles as _roles
from .cards import CardDB
from .ydk import Decklist

# --- specific passcodes we reason about by identity ----------------------
LADY = 81497285          # Lady Labrynth — Lv8 boss, needs a Welcome to hit the field
LOVELY = 2347656         # Lovely Labrynth — Lv8 boss
ARIAS = 73602965         # Arias the Butler — lets you use normal traps from hand T1
ARIANNA = 1225009        # Arianna — 1-card starter / searcher
ARIANE = 75730490        # Ariane — 1-card starter / searcher
BIG_WELCOME = 92714517   # Big Welcome — flexible (SS from hand/GY OR set a trap)
SMALL_WELCOME = 5380979  # Welcome — SS a Labrynth from hand/GY (needs a monster)
TRAP_TRICK = 80101899    # Trap Trick — fetch a normal trap from deck
BOSSES = {LADY, LOVELY}

_GRADES = [(75, "Strong"), (50, "Playable"), (25, "Weak"), (0, "Brick")]


@dataclass
class ResolvedCard:
    id: int
    name: str
    roles: list[str]


@dataclass
class HandEval:
    grade: str
    score: int
    going_first: bool
    cards: list[ResolvedCard]
    starters: list[str] = field(default_factory=list)
    interaction: list[str] = field(default_factory=list)
    handtraps: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    line: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d["cards"] = [c.__dict__ for c in self.cards]
        return d


# --- resolving a written hand into card ids ------------------------------
def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def resolve_cards(tokens: list, dl: Decklist, db: CardDB) -> list[ResolvedCard]:
    """Resolve a list of names/ids into cards, preferring cards in the deck."""
    # candidate name -> id, deck cards first so ambiguous names bind to the deck
    name_to_id: dict[str, int] = {}
    for cid in list(dict.fromkeys(dl.main + dl.extra)) + list(db.cards):
        c = db.get(cid)
        if c:
            name_to_id.setdefault(_norm(c["name"]), int(cid))
    norm_names = list(name_to_id)

    out: list[ResolvedCard] = []
    for tok in tokens:
        cid: int | None = None
        if isinstance(tok, int) or (isinstance(tok, str) and tok.strip().isdigit()):
            cid = int(tok)
        else:
            key = _norm(str(tok))
            if key in name_to_id:
                cid = name_to_id[key]
            else:  # substring, then fuzzy
                subs = [n for n in norm_names if key and key in n]
                if len(subs) == 1:
                    cid = name_to_id[subs[0]]
                elif subs:
                    cid = name_to_id[sorted(subs, key=len)[0]]
                else:
                    close = difflib.get_close_matches(key, norm_names, n=1, cutoff=0.6)
                    if close:
                        cid = name_to_id[close[0]]
        if cid is None:
            out.append(ResolvedCard(id=-1, name=f"<unresolved: {tok}>", roles=[]))
        else:
            out.append(ResolvedCard(id=cid, name=db.name(cid),
                                    roles=sorted(_roles.roles_for(cid, db.get(cid)))))
    return out


# --- evaluation ----------------------------------------------------------
def _has_role(card: ResolvedCard, *tags: str) -> bool:
    return bool(set(tags) & set(card.roles))


def evaluate_hand(hand: list[ResolvedCard], going_first: bool = True) -> HandEval:
    ids = {c.id for c in hand}
    welcome_access = [c for c in hand if _has_role(c, "welcome_access")]
    welcome_cards = [c for c in hand if _has_role(c, "welcome")]
    lab_monsters = [c for c in hand if _has_role(c, "labrynth_monster")]
    ss_targets = [c for c in hand if _has_role(c, "labrynth_monster") and c.id not in BOSSES]
    handtraps = [c for c in hand if _has_role(c, "handtrap")]
    # normal traps that provide standalone interaction (not the Welcome engine)
    interaction_traps = [
        c for c in hand
        if _has_role(c, "normal_trap")
        and not _has_role(c, "welcome")
        and _has_role(c, "disruption", "removal", "floodgate", "board_breaker",
                      "mass_removal", "hand_disruption", "targeted", "dominus", "copy")
    ]
    board_breakers = [c for c in hand if _has_role(c, "board_breaker", "mass_removal", "removal")]
    has_arias = ARIAS in ids
    has_boss = bool(ids & BOSSES)
    one_card_start = any(c.id in {ARIANNA, ARIANE} for c in hand)

    # Can we actually convert a Welcome-access card into a play?
    can_start = False
    if welcome_access:
        if any(c.id == BIG_WELCOME for c in welcome_cards):
            can_start = True  # Big Welcome can set a trap even with no monster
        if ss_targets or lab_monsters:
            can_start = True  # any Welcome + a Labrynth monster
        if has_arias:
            can_start = True  # Arias lets you use normal traps from hand T1
    if one_card_start:
        can_start = True

    reasons: list[str] = []
    risks: list[str] = []
    line: list[str] = []

    # ---- scoring --------------------------------------------------------
    score = 0
    if going_first:
        if can_start:
            score += 25
            reasons.append("Has a usable engine starter.")
        elif welcome_access and not (ss_targets or lab_monsters):
            reasons.append("Welcome-access but no Labrynth monster to convert it — awkward.")
            score -= 5
            risks.append("A lone small Welcome with no monster does little; mulligan-quality piece.")
        extra = len(interaction_traps) + len(handtraps)
        score += min(extra, 3) * 15
        if extra:
            reasons.append(f"{extra} extra interaction piece(s): "
                           + ", ".join(c.name for c in interaction_traps + handtraps))
        if handtraps:
            score += 8
        if has_arias:
            score += 10
            reasons.append("Arias enables using normal traps from hand on turn 1 (explosive).")
        if has_boss and not welcome_access:
            risks.append("Lady/Lovely are Level 8 — they need a Welcome to reach the field, "
                         "so a boss in hand with no Welcome is not yet a play.")
        if not (welcome_access or interaction_traps or handtraps):
            score -= 20
            reasons.append("No traps and no engine — very little to do turn 1.")
    else:  # going second
        outs = board_breakers + handtraps
        score += min(len(outs), 4) * 18
        if outs:
            reasons.append(f"{len(outs)} go-second out(s): " + ", ".join(c.name for c in outs))
        if can_start:
            score += 15
            reasons.append("Can rebuild your own board after breaking theirs.")
        if handtraps:
            score += 5
        if not outs:
            score -= 15
            reasons.append("No board breakers or hand traps — hard to interact on the draw.")

    score = max(0, min(100, score))
    grade = next(g for cut, g in _GRADES if score >= cut)

    # ---- recommended line ----------------------------------------------
    if going_first:
        if has_arias and welcome_access:
            line.append("Set your normal traps. With Arias you can activate a Welcome "
                        "from hand on their turn to Special Summon a Labrynth and disrupt.")
        elif any(c.id == BIG_WELCOME for c in welcome_cards):
            tgt = ss_targets[0].name if ss_targets else "a Labrynth monster (or set a Normal Trap)"
            line.append(f"Set Big Welcome + your other traps, then pass. On their turn use "
                        f"Big Welcome to Special Summon {tgt} (or set a trap if you have no target).")
        elif any(c.id == SMALL_WELCOME for c in welcome_cards) and (ss_targets or lab_monsters):
            tgt = (ss_targets or lab_monsters)[0].name
            line.append(f"Set Welcome + your other traps and pass. On their turn Welcome "
                        f"to Special Summon {tgt}.")
        elif any(c.id == TRAP_TRICK for c in welcome_access):
            line.append("Trap Trick for the best Normal Trap this matchup (usually a Welcome, "
                        "or a floodgate/removal vs a known combo deck), set the rest, pass.")
        elif one_card_start:
            line.append("Lead with your Labrynth starter (Arianna/Ariane) to search, "
                        "set your traps, and pass into a disruptive board.")
        else:
            line.append("Set what interaction you have and pass; prioritize keeping your "
                        "most flexible trap live for their key play.")
        if interaction_traps:
            line.append("Sequence removal onto the combo *enabler* (the searcher / one-card "
                        "starter), not the end-board payoff.")
        risks.append("Bait Ash/Called-by/​counter traps with a lesser threat before committing your key Welcome.")
        if handtraps:
            risks.append("Hold hand traps for the opponent's actual combo turn rather than spending them early.")
    else:
        if board_breakers:
            line.append("Let them build, then break the end board with "
                        + ", ".join(c.name for c in board_breakers) + " at the right window.")
        if handtraps:
            line.append("Use hand traps during their combo to reduce what you have to break through.")
        if can_start:
            line.append("After breaking, establish your own Labrynth board with a Welcome to close the game.")
        if not line:
            line.append("Survive their turn with what you have; look to stabilize with Lady value.")

    starters = [c.name for c in welcome_access] + [c.name for c in hand if c.id in {ARIANNA, ARIANE}]
    return HandEval(
        grade=grade, score=score, going_first=going_first, cards=hand,
        starters=sorted(set(starters)),
        interaction=[c.name for c in interaction_traps],
        handtraps=[c.name for c in handtraps],
        reasons=reasons, line=line, risks=risks,
    )


def evaluate(tokens: list, dl: Decklist, db: CardDB, going_first: bool = True) -> HandEval:
    """Convenience: resolve written cards then evaluate."""
    return evaluate_hand(resolve_cards(tokens, dl, db), going_first=going_first)
