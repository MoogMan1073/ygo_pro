"""ygo_advisor — a Yu-Gi-Oh! Master Duel play-advisor toolkit.

Built around a Labrynth trap-control shell, this package turns a `.ydk`
decklist plus live card / meta data into structured information a coach
(human or LLM) can reason over:

* `ydk`          — parse `.ydk` files into main/extra/side card-id lists
* `cards`        — YGOPRODeck-backed card database with local caching
* `roles`        — semantic role tagging (starter, boss, hand trap, tech …)
* `deck_profile` — combine the above into a rich, JSON-able deck profile
* `probability`  — exact (hypergeometric) + Monte-Carlo opening-hand math
* `flavor`       — recommend a Labrynth "flavor" + tech vs the current meta
* `meta`         — MasterDuelMeta tier-list snapshot access
* `rulebook`     — the cached Expanded Rule Book sections

Nothing here plays the game for you; it assembles the facts and the math
so the advice given in chat is grounded and correct.
"""

__version__ = "0.1.0"
