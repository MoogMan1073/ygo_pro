"""Recommend a Labrynth *flavor* and tech package for the current meta.

Labrynth's core (the Welcome traps + the Fiend cast) is fixed; what changes
format to format is the **non-engine shell** — the normal traps, hand traps
and splashed engines you pick to beat the top decks. This module scores
tech cards against the meta's *threat tags* and ranks the well-known Lab
flavors by how much of the field their package answers.

It's a heuristic recommender: the numbers rank options, and the coaching
layer explains and adjusts. Card/threat annotations live in ``TECH`` and in
the meta snapshot, so they're easy to update as the format shifts.
"""
from __future__ import annotations

from dataclasses import dataclass

from .meta import MetaSnapshot, load_snapshot

# --- the flavors ---------------------------------------------------------
FLAVORS: dict[str, dict] = {
    "pure-control": {
        "name": "Pure / Building-block Labrynth",
        "sample_deck": None,
        "summary": "Maximum trap density, minimal Extra Deck. The most "
                   "consistent and grind-proof shell; leans on Lady + Welcome "
                   "value and a wide normal-trap suite.",
        "core_tech": ["Dominus Impulse", "Destructive Daruma Karma Cannon",
                      "Trap Trick", "Transaction Rollback"],
        "extra_deck_need": "none",
        "best_when": "Field is diverse / grindy; no single dominant combo to snipe.",
    },
    "cannon": {
        "name": "Cannon / \"Math\" Labrynth",
        "sample_deck": "cannon-lab",
        "summary": "Builds toward Simultaneous Equation Cannons for a "
                   "trap-based OTK/removal payoff. Uses a light generic Extra "
                   "Deck purely as Cannon fuel and go-second bodies.",
        "core_tech": ["Simultaneous Equation Cannons", "Trap Trick",
                      "Destructive Daruma Karma Cannon"],
        "extra_deck_need": "light (Cannon fuel + rank-ups)",
        "best_when": "You want inevitability vs control mirrors and slower boards.",
    },
    "fydraulis-synchro": {
        "name": "Fydraulis / Synchro Labrynth",
        "sample_deck": "fydraulis-synchro-lab",
        "summary": "Splashes Fydraulis Harmonia + Ash (tuners) and hand traps "
                   "into a Synchro toolbox (Baronne, Chaos Angel, Psychic End "
                   "Punisher). Strong going second and adds proactive negation.",
        "core_tech": ["Fydraulis Harmonia", "Ash Blossom & Joyous Spring",
                      "Droll & Lock Bird", "Dimensional Barrier",
                      "Songs of the Dominators"],
        "extra_deck_need": "full Synchro suite",
        "best_when": "Combo decks dominate; you need go-second power + hand traps.",
    },
    "fiendsmith": {
        "name": "Fiendsmith Labrynth",
        "sample_deck": "fiendsmith-lab",
        "summary": "Adds the LIGHT-Fiend Fiendsmith engine (shares Fiend type "
                   "with Lab) for extra-deck value, recovery and Necroquip/"
                   "Desirae disruption. Grindier and more resilient to removal.",
        "core_tech": ["Fiendsmith Engraver", "Lacrima the Crimson Tears",
                      "Different Dimension Ground", "Torrential Tribute"],
        "extra_deck_need": "full Fiendsmith package",
        "best_when": "Grind games and GY-value decks; you want more than traps.",
    },
}

# --- tech catalog: card -> what it answers + which flavors favor it -------
@dataclass
class Tech:
    name: str
    id: int
    category: str
    answers: frozenset[str]
    flavors: frozenset[str]
    note: str = ""


TECH: list[Tech] = [
    Tech("Maxx \"C\"", 23434538, "handtrap",
         frozenset({"special_summon_spam", "going_first_combo", "combo_extension"}),
         frozenset({"pure-control", "cannon", "fydraulis-synchro", "fiendsmith"}),
         "Universal tax vs any SS-heavy combo deck."),
    Tech("Ash Blossom & Joyous Spring", 14558127, "handtrap",
         frozenset({"grave_reliant", "going_first_combo", "search_heavy"}),
         frozenset({"fydraulis-synchro"}),
         "Also a Level-3 Tuner enabling the Synchro line."),
    Tech("Droll & Lock Bird", 94145021, "handtrap",
         frozenset({"search_heavy", "going_first_combo"}),
         frozenset({"fydraulis-synchro"}),
         "Shuts off decks that add multiple cards from Deck."),
    Tech("Dimensional Barrier", 83326048, "normal_trap",
         frozenset({"extra_deck_reliant", "special_summon_spam", "monster_effect_heavy"}),
         frozenset({"fydraulis-synchro"}),
         "Declares a summon/monster type; brutal vs single-archetype combo."),
    Tech("Different Dimension Ground", 31849106, "normal_trap",
         frozenset({"grave_reliant", "fusion_spam"}),
         frozenset({"fiendsmith"}),
         "Banishes GY-effect monsters; hoses graveyard decks."),
    Tech("Songs of the Dominators", 58053438, "normal_trap",
         frozenset({"special_summon_spam", "monster_effect_heavy"}),
         frozenset({"fydraulis-synchro", "pure-control"}),
         "Flexible floodgate/removal."),
    Tech("Torrential Tribute", 53582587, "normal_trap",
         frozenset({"special_summon_spam", "going_first_combo"}),
         frozenset({"fiendsmith", "pure-control"}),
         "Mass removal punishing wide boards."),
    Tech("Dominus Impulse", 40366667, "normal_trap",
         frozenset({"going_first_combo", "board_building"}),
         frozenset({"pure-control", "cannon", "fydraulis-synchro"}),
         "Chainable disruption/removal."),
    Tech("Full Force Virus", 4931121, "normal_trap",
         frozenset({"going_first_combo", "combo_extension"}),
         frozenset({"cannon", "pure-control"}),
         "Hand disruption vs setup-heavy hands."),
    Tech("Destructive Daruma Karma Cannon", 30748475, "normal_trap",
         frozenset({"board_building", "monster_effect_heavy"}),
         frozenset({"pure-control", "cannon", "fiendsmith"}),
         "Flips/locks a problem monster."),
    Tech("Simultaneous Equation Cannons", 25096909, "payoff",
         frozenset({"inevitability"}),
         frozenset({"cannon"}),
         "Trap-based mass removal / closer."),
    Tech("Fydraulis Harmonia", 70088809, "engine",
         frozenset({"going_second", "board_building"}),
         frozenset({"fydraulis-synchro"}),
         "Non-engine tuner enabling go-second Synchro breaks."),
]


@dataclass
class FlavorScore:
    key: str
    name: str
    coverage: float                 # field weight this flavor's package answers
    covered_threats: list[str]
    summary: str
    best_when: str


def _flavor_answers(key: str) -> frozenset[str]:
    ans: set[str] = set()
    for t in TECH:
        if key in t.flavors:
            ans |= t.answers
    return frozenset(ans)


def rank_tech(snap: MetaSnapshot) -> list[tuple[Tech, float]]:
    """Rank individual tech cards by how much of the field they answer."""
    tw = snap.threat_weights()
    scored = [(t, sum(tw.get(a, 0.0) for a in t.answers)) for t in TECH]
    return sorted(scored, key=lambda x: x[1], reverse=True)


def rank_flavors(snap: MetaSnapshot) -> list[FlavorScore]:
    """Rank flavors by the total field weight their tech package addresses."""
    tw = snap.threat_weights()
    out: list[FlavorScore] = []
    for key, meta in FLAVORS.items():
        answers = _flavor_answers(key)
        covered = sorted((a for a in answers if a in tw), key=lambda a: tw[a], reverse=True)
        coverage = sum(tw[a] for a in covered)
        out.append(FlavorScore(
            key=key, name=meta["name"], coverage=round(coverage, 2),
            covered_threats=covered, summary=meta["summary"], best_when=meta["best_when"],
        ))
    return sorted(out, key=lambda f: f.coverage, reverse=True)


def recommend(snap: MetaSnapshot | None = None) -> dict:
    """Full recommendation: ranked flavors, top tech, and per-threat answers."""
    snap = snap or load_snapshot()
    tw = snap.threat_weights()
    flavors = rank_flavors(snap)
    tech = rank_tech(snap)
    # best answer per major threat
    per_threat: dict[str, list[str]] = {}
    for threat in sorted(tw, key=lambda t: tw[t], reverse=True):
        answerers = [t.name for t in TECH if threat in t.answers]
        if answerers:
            per_threat[threat] = answerers
    return {
        "meta_date": snap.date,
        "field": [(d.name, d.tier, d.weight) for d in snap.top()],
        "threat_weights": dict(sorted(tw.items(), key=lambda x: x[1], reverse=True)),
        "recommended_flavor": flavors[0].__dict__ if flavors else None,
        "flavor_ranking": [f.__dict__ for f in flavors],
        "top_tech": [(t.name, round(s, 2), t.note) for t, s in tech[:8]],
        "answers_by_threat": per_threat,
    }
