# ygo_advisor — a Labrynth play-advisor for Yu-Gi-Oh! Master Duel

A toolkit that helps you make the best calls in a Master Duel game. You share
your decklist (`.ydk`) and your opening hand / board (screenshot or text) in
chat; the advisor reasons over grounded data — your exact card list, live
card text, the current meta, the full rulebook — and gives probability- and
game-theory-informed advice on the play to make.

It is built **Labrynth-first**, because Labrynth is a flexible trap/non-engine
control shell you re-tune every format. A headline feature is recommending
which **flavor** of Labrynth (and which tech cards) best beats the current
meta.

> **The chat is the interface.** This repo is the knowledge base + math tools
> + playbook that make that conversation expert-level and *correct*. The
> deterministic tools do the counting; the coaching layer does the flexible,
> meta-aware reasoning and explains the play.

---

## What's here

```
ygo_advisor/          the Python package
  ydk.py              parse .ydk -> main/extra/side card ids
  cards.py            YGOPRODeck card data + local cache (data/cards_cache.json)
  roles.py            semantic role tagging (starter, boss, hand trap, tech, ...)
  deck_profile.py     deck + cards + roles -> profile with opening-hand odds
  probability.py      exact (hypergeometric) + Monte-Carlo hand math
  flavor.py           recommend a Labrynth flavor + tech vs the meta
  meta.py             MasterDuelMeta tier-list snapshot access
  rulebook.py         fetch + split the Expanded Rule Book into rules/*.md
  cli.py              `python -m ygo_advisor ...`
data/
  decks/              three sample Labrynth flavors (.ydk)
  cards_cache.json    cached card data (committed; no network needed to use)
  meta/tier_list.json curated meta snapshot with threat tags
rules/                21 cached Expanded Rule Book sections (built)
playbook/             the coaching knowledge layer (markdown)
tests/                probability + parser tests
scripts/build_meta.py refresh helper for the meta snapshot
```

## Quick start

No dependencies — Python 3.10+ standard library only.

```bash
# Profile a deck + exact opening-hand probabilities (going first)
python -m ygo_advisor deck data/decks/cannon-lab.ydk
python -m ygo_advisor deck data/decks/fydraulis-synchro-lab.ydk --second   # going second

# Which flavor of Labrynth should I bring vs the current meta?
python -m ygo_advisor flavor

# Look up a rules section (the [baseLink]#[rule] anchors)
python -m ygo_advisor rules SEGOC
python -m ygo_advisor rules IF-WHEN
python -m ygo_advisor rules-list

# (Re)build the caches from the web
python -m ygo_advisor build-cards data/decks/*.ydk
python -m ygo_advisor build-rules
```

Example — the profiler prints exact, verified odds:

```
## Opening-hand probabilities (exact, hypergeometric)
    74.2%  open >=1 Welcome-access (9 copies)
    93.5%  open >=1 Labrynth monster (16 copies)
    68.2%  open Welcome-access + Labrynth monster (9+16)
```

## The probability engine

Opening-hand questions are exact **hypergeometric** calculations (drawing
without replacement), not estimates. AND-conditions across disjoint card
groups are computed exactly; awkward OR/"any two of these" conditions fall
back to a Monte-Carlo sampler. The two agree to <1% in tests. Master Duel
seat math is built in: going first you see 5 cards, going second 6 (`--second`).

## The flavor recommender

Labrynth's core is fixed; the non-engine shell changes per format. The
recommender:
1. reduces each meta deck to **threat tags** (what it does to you),
2. weights those tags by the deck's representation,
3. scores each flavor / tech card by how much of the weighted field it answers.

Output: a ranked list of flavors, the best individual tech, and a best-answer-
per-threat table. It's a heuristic starting point that the coaching layer
explains and adjusts. Data lives in `flavor.py` + `data/meta/tier_list.json`,
both easy to update. See `playbook/variants.md` and `playbook/nonengine-catalog.md`.

## The rules reference

The MasterDuelMeta *Expanded Rule Book* (competitive-depth: chains, SEGOC,
PSCT, missing timing, damage step, "forgetting", negations, …) is cached
locally as 21 sections keyed to the `[baseLink]#[rule]` anchors. It fills the
gap the beginner Structure Deck rulebook can't — and for a trap deck that
operates entirely on the opponent's turn, chain/SEGOC/timing rulings decide
games.

## Data sources
- **Cards:** YGOPRODeck API (`db.ygoprodeck.com/api/v7`), cached locally.
- **Meta + rules:** MasterDuelMeta, which is API-backed (`/api/v1/...`); the
  server-rendered rulebook page is parsed for the full article.
- **Decklists:** plain `.ydk` (a list of passcodes). The compressed
  `decks.ygoresources.com` URL codec is *not* needed — `.ydk` is read directly.

## Status & roadmap
- **Now (MVP):** deck pipeline, probability engine, flavor recommender, rules
  cache, coaching playbook — all runnable and tested.
- **Next:** richer per-deck matchup profiles; an opening-hand *evaluator*
  that classifies a concrete hand and proposes the line; live meta refresh.
- **Later:** wrap the same engine as a standalone Claude-API chatbot / small
  web UI (the tools become function-calls) for use outside this chat.

## Tests
```bash
python -m pytest          # if pytest is installed
```
The suite verifies the hypergeometric math against Monte-Carlo, the `.ydk`
parser, sample-deck legality, and role tagging.

---
*Not affiliated with Konami. Card data © their respective owners; retrieved
via public APIs for personal analysis.*
