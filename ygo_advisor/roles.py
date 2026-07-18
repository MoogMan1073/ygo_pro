"""Semantic role tagging for cards.

Card *type* (monster / spell / trap) is derivable from YGOPRODeck data, but
the roles that actually drive play decisions — "is this a starter?", "does
this fetch a Welcome?", "is this a hand trap?" — are not. This module keeps
a curated passcode->roles map for the Labrynth core and common tech, and
derives coarser roles for everything else.

Roles are advisory, not exhaustive; the coaching layer reads full card text
too. But they're accurate enough to define probability groups (what counts
as an "opener") and to power the flavor recommender.
"""
from __future__ import annotations

from . import cards as _c

# --- curated roles by passcode ------------------------------------------
# Keep this focused on cards whose *function* can't be inferred from stats.
CURATED: dict[int, set[str]] = {
    # Labrynth monsters -------------------------------------------------
    81497285: {"labrynth", "labrynth_monster", "boss", "starter"},        # Lady Labrynth
    2347656:  {"labrynth", "labrynth_monster", "boss"},                    # Lovely Labrynth
    73602965: {"labrynth", "labrynth_monster", "extender", "enabler"},     # Arias the Butler
    1225009:  {"labrynth", "labrynth_monster", "starter", "searcher"},     # Arianna
    75730490: {"labrynth", "labrynth_monster", "starter", "searcher"},     # Ariane
    37629703: {"labrynth", "labrynth_monster", "searcher", "furniture"},   # Chandraglier
    74018812: {"labrynth", "labrynth_monster", "searcher", "furniture"},   # Stovie Torbie
    2511:     {"labrynth", "labrynth_monster", "extender", "furniture"},   # Cooclock
    60990740: {"labrynth", "engine", "trap_setup"},                        # Absolute King Back Jack
    # Labrynth spells/traps --------------------------------------------
    5380979:  {"labrynth", "normal_trap", "welcome", "welcome_access", "starter"},  # Welcome
    92714517: {"labrynth", "normal_trap", "welcome", "welcome_access", "starter"},  # Big Welcome
    33407125: {"labrynth", "field_spell"},                                 # Labrynth Labyrinth
    # Trap engine / consistency ----------------------------------------
    80101899: {"normal_trap", "welcome_access", "searcher", "starter"},    # Trap Trick
    22377092: {"normal_trap", "welcome_access", "consistency"},            # Trap Holic
    6351147:  {"normal_trap", "handtrap_trap", "disruption", "copy"},      # Transaction Rollback
    # Hand traps --------------------------------------------------------
    23434538: {"handtrap", "going_second", "stun"},                        # Maxx "C"
    14558127: {"handtrap", "going_second", "negate"},                      # Ash Blossom
    94145021: {"handtrap", "going_second"},                                # Droll & Lock Bird
    # Floodgate / board-breaker traps ----------------------------------
    83326048: {"normal_trap", "floodgate", "disruption"},                  # Dimensional Barrier
    31849106: {"normal_trap", "floodgate", "anti_grave"},                  # Different Dimension Ground
    53582587: {"normal_trap", "board_breaker", "mass_removal"},            # Torrential Tribute
    4931121:  {"normal_trap", "board_breaker", "hand_disruption"},         # Full Force Virus
    30748475: {"normal_trap", "removal", "targeted"},                      # Destructive Daruma Karma Cannon
    40366667: {"normal_trap", "removal", "dominus"},                       # Dominus Impulse
    58053438: {"normal_trap", "floodgate", "disruption"},                  # Songs of the Dominators
    # Payoff / win condition -------------------------------------------
    25096909: {"normal_trap", "payoff", "wincon", "needs_extra_deck"},     # Simultaneous Equation Cannons
    # Fiendsmith engine -------------------------------------------------
    60764609: {"engine", "fiendsmith", "extender", "searcher"},            # Fiendsmith Engraver
    28803166: {"engine", "fiendsmith", "extender"},                        # Lacrima the Crimson Tears
    97651498: {"engine", "fiendsmith", "extender"},                        # Fabled Lurrie
    98567237: {"engine", "fiendsmith", "searcher", "spell"},               # Fiendsmith's Tract
    99989863: {"engine", "fiendsmith", "normal_trap"},                     # Fiendsmith in Paradise
    # Fydraulis engine --------------------------------------------------
    70088809: {"engine", "nonengine_tuner", "going_second", "synchro_enabler"},  # Fydraulis Harmonia
}

# Tags that make a card count as an "opener" for a Labrynth turn.
STARTER_TAGS = {"starter", "welcome_access", "searcher"}


def derive(card: dict) -> set[str]:
    """Roles inferable directly from card data."""
    r: set[str] = set()
    kind = _c.card_kind(card)
    r.add(kind)
    if _c.is_normal_trap(card):
        r.add("normal_trap")
    if _c.is_extra_deck(card):
        r.add("extra_deck")
        ft = card.get("frameType", "")
        if ft:
            r.add(ft)  # fusion / synchro / xyz / link
    if card.get("archetype") == "Labrynth":
        r.add("labrynth")
    if "Tuner" in card.get("type", ""):
        r.add("tuner")
    return r


def roles_for(cid: int, card: dict | None) -> set[str]:
    """Full role set for a card = curated ∪ derived."""
    r: set[str] = set(CURATED.get(int(cid), set()))
    if card:
        r |= derive(card)
    return r


def is_starter(cid: int, card: dict | None) -> bool:
    return bool(roles_for(cid, card) & STARTER_TAGS)
