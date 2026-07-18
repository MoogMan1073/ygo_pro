# Matchup Threat Profiles

The advisor reads the meta from `data/meta/tier_list.json`. Each deck is
reduced to **threat tags** — the abstract things it does to you — so that
tech recommendations generalize instead of being hard-coded per deck. When
the format shifts, update the snapshot (names, tiers, shares, tags) and the
flavor recommender re-scores automatically.

## Threat-tag vocabulary
| Tag | Meaning | Typical answers |
| --- | --- | --- |
| `special_summon_spam` | Special Summons many bodies fast | Maxx "C", Dimensional Barrier, Torrential, floodgates |
| `extra_deck_reliant` | Wins through Extra Deck monsters | Dimensional Barrier, Different Dimension Ground |
| `going_first_combo` | Sets up a big turn-1 board | Maxx "C", hand traps, Torrential, Dominus |
| `search_heavy` | Adds several cards from Deck | Droll & Lock Bird, Ash Blossom |
| `grave_reliant` | Uses GY effects heavily | Different Dimension Ground, Ash Blossom |
| `fusion_spam` | Fusion-centric (Branded/HERO/Predaplant) | Dimensional Barrier (Fusion), D.D. Ground |
| `spell_heavy` | Leans on key Spells | Dimensional Barrier, floodgates |
| `monster_effect_heavy` | Wins on monster effects | Songs, Daruma, Lady Labrynth |
| `board_building` | Assembles a standing board | Dominus, Daruma, Torrential |
| `going_second_power` | Punches through boards | play around it: don't over-commit |

## Current snapshot (2026-07 — curated, verify before events)
> Power/share observed from the MasterDuelMeta tier list; threat tags are
> curated abstractions. This is a starting point, not gospel — re-pull before
> a tournament with `scripts/build_meta.py` and adjust tags.

- **Branded (T1)** — fusion_spam, grave_reliant, spell_heavy, going_second_power.
  Grinds with Fusions and GY recursion. D.D. Ground and Dimensional Barrier
  (declare Fusion) are strong; expect them to grind, so protect your engine.
- **Kewl Tune (T1)** — special_summon_spam, extra_deck_reliant, going_first_combo,
  search_heavy. Combo deck that wants a long turn 1: Maxx "C" tax, Droll on the
  search chain, Dimensional Barrier / Torrential on the payoff.
- **Dracotail (T1)** — special_summon_spam, extra_deck_reliant, combo_extension.
  Extends hard; hand traps early, mass removal if it resolves a board.
- **Radiant Typhoon variants (T2–T3)** — special_summon_spam, going_first_combo.
  Interruptible early; Maxx "C" and a well-timed board breaker.
- **Vanquish Soul K9 (T3)** — monster_effect_heavy, board_building. Grind fight;
  Daruma / Songs on the key body, out-value with Lady.

## How to use this in a game
1. Identify (or ask) the opponent's deck; map it to its threat tags.
2. The advisor prioritizes your set/played interaction to hit those tags in
   the right window (see `labrynth-core.md` §3 and the chain-timing rules).
3. Post-game / pre-event, the flavor recommender tells you which shell and
   tech best cover the *whole* field, not just one matchup.
