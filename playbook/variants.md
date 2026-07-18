# Labrynth Variants ("Flavors")

Labrynth's core is fixed — the Welcome normal traps plus the Fiend cast
(Lady, Lovely, Arias, Arianna/Ariane, and the furniture: Chandraglier,
Stovie Torbie, Cooclock). What you swap format-to-format is the **non-engine
shell**: the extra normal traps, hand traps, and splashed engines chosen to
beat the current top decks. That flexibility is Labrynth's defining strength,
and picking the right flavor is a real edge.

The advisor scores these against the live meta (`ygo_advisor flavor`); the
data lives in `ygo_advisor/flavor.py` and `data/meta/tier_list.json`, both
easy to update as the format shifts.

| Flavor | Extra Deck | Identity | Best when |
| --- | --- | --- | --- |
| **Pure / Building-block** | none | Max trap density, most consistent, grind-proof | Diverse field, no single combo to snipe |
| **Cannon / "Math"** | light | Builds to Simultaneous Equation Cannons payoff | You want inevitability vs control/slow boards |
| **Fydraulis / Synchro** | full Synchro | Tuners + hand traps → Baronne/Chaos Angel; strong go-2 | Combo decks dominate; need go-second power |
| **Fiendsmith** | full Fiendsmith | LIGHT-Fiend value engine, recovery, Necroquip/Desirae | Grind + GY-value decks; want more than traps |

Sample lists live in `data/decks/`:
- `cannon-lab.ydk` — Cannon / Math
- `fydraulis-synchro-lab.ydk` — Fydraulis / Synchro
- `fiendsmith-lab.ydk` — Fiendsmith

## How the recommendation works
1. Each meta deck in the snapshot carries **threat tags** — abstractions of
   what it does to you (`special_summon_spam`, `grave_reliant`,
   `extra_deck_reliant`, `going_first_combo`, …).
2. Each tech card in the catalog is tagged with the threats it **answers**
   and the flavors that favor it.
3. The field's threat tags are weighted by each deck's representation, then
   each flavor is scored by how much of that weighted field its tech package
   addresses. Individual tech cards are ranked the same way.

The output is a ranking + a recommended flavor + the top individual tech and
a best-answer-per-threat table. It is a **heuristic** starting point: the
coaching layer explains the trade-offs (consistency vs power, going-first vs
going-second) and adjusts to your ladder/tournament context and comfort.

## Notes on the trade-offs the score doesn't fully capture
- **Consistency tax:** every splashed engine (Fiendsmith, Synchro tuners)
  costs deck slots and raises brick risk. Pure/Cannon draw their traps more
  reliably.
- **Going-first vs going-second:** Fydraulis/Synchro and hand-trap-heavy
  builds are much better on the draw; pure control prefers the play.
- **Floodgates are format-dependent and risky:** cards like Dimensional
  Barrier are backbreaking vs single-archetype combo but dead vs decks that
  play around them or grind through — weigh the field, not just the top deck.
