# Non-Engine & Tech Catalog

The tech cards the flavor recommender chooses between, with what each answers
and which flavor favors it. The machine-readable source of truth is the
`TECH` list in `ygo_advisor/flavor.py`; this file is the human reference and
the place to reason about *why* a card is in or out.

Add a card by giving it: an id, a category, the threat tags it **answers**,
and the flavors it belongs to. The recommender does the rest.

## Hand traps
| Card | Answers | Flavors | Note |
| --- | --- | --- | --- |
| Maxx "C" | special_summon_spam, going_first_combo, combo_extension | all | Universal tax; format-defining vs combo. |
| Ash Blossom | grave_reliant, going_first_combo, search_heavy | Fydraulis | Doubles as a Lv3 Tuner for the Synchro line. |
| Droll & Lock Bird | search_heavy, going_first_combo | Fydraulis | Shuts off multi-search turns. |

## Normal traps (also the Labrynth engine payload)
| Card | Answers | Flavors | Note |
| --- | --- | --- | --- |
| Dimensional Barrier | extra_deck_reliant, special_summon_spam, monster_effect_heavy | Fydraulis | Declares a summon/monster type; brutal vs single-archetype combo, dead vs varied boards. |
| Different Dimension Ground | grave_reliant, fusion_spam | Fiendsmith | Banishes GY-effect monsters instead of GY'ing — hoses graveyard decks. |
| Songs of the Dominators | special_summon_spam, monster_effect_heavy | Fydraulis, Pure | Flexible floodgate/removal. |
| Torrential Tribute | special_summon_spam, going_first_combo | Fiendsmith, Pure | Mass removal punishing wide boards. |
| Dominus Impulse | going_first_combo, board_building | Pure, Cannon, Fydraulis | Chainable disruption/removal. |
| Full Force Virus | going_first_combo, combo_extension | Cannon, Pure | Hand disruption vs setup hands. |
| Destructive Daruma Karma Cannon | board_building, monster_effect_heavy | Pure, Cannon, Fiendsmith | Flips/locks a problem monster. |

## Payoffs / engines
| Card | Role | Flavors | Note |
| --- | --- | --- | --- |
| Simultaneous Equation Cannons | payoff / closer | Cannon | Trap-based mass removal; needs a light Extra Deck as fuel. |
| Fydraulis Harmonia | go-second engine | Fydraulis | Non-engine tuner enabling go-second Synchro breaks. |
| Fiendsmith package | value engine | Fiendsmith | Shares Fiend type with Lab; recovery + Necroquip/Desirae disruption. |

## Selection principles
- **Density vs power:** each non-trap engine card lowers your trap density and
  raises brick risk. Only splash an engine that meaningfully improves a bad
  matchup or your go-second game.
- **Floodgates are high-variance:** enormous vs the deck they hit, dead vs the
  rest. Weight them by the *combined* share of the decks they punish.
- **Redundancy of answers:** prefer tech that answers multiple top threats
  (Maxx "C", Torrential) over narrow silver bullets unless one deck dominates.
- **Copy counts matter for consistency:** use the probability engine to check
  "how often do I open this tech" before committing multiple slots.
