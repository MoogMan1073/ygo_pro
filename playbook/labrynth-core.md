# Labrynth Coaching Playbook — Core

This is the decision framework the advisor follows when coaching a Labrynth
game. It is deliberately deck-first: Labrynth is a reactive, imperfect-
information trap-control deck, so most decisions are about **sequencing
interaction and reading the opponent**, not executing a fixed combo.

The advisor pairs this framework with three grounded inputs:
- your **deck profile** (`ygo_advisor deck <file>.ydk`) — exact card text + roles,
- the **probability engine** — exact odds for anything countable,
- the **rules cache** (`ygo_advisor rules <ANCHOR>`) — for timing/chain rulings.

---

## 1. Turn 0 — before you see a card

- **Going first vs second matters a lot.** Going first you see 5 cards and
  want to *set up interaction*; going second you see 6 and want *board
  breakers / hand traps*. The profiler prints both (`--second`).
- Labrynth is comfortable **going first** (set traps, pass) but its worst
  matchups race it, so know the flavor's plan for the turn you lose the roll.

## 2. Opening-hand triage (the checklist)

Ask, in order:
1. **Do I have a normal-trap starter?** (Welcome / Big Welcome / Trap Trick).
   These are the engine — with any Labrynth monster or Lady/Arias they snowball.
2. **Can I actually use it turn 1?** A Welcome needs a Labrynth monster in
   hand to Special Summon, *or* Lady/Arias already giving you value. A lone
   Welcome with no monster is weaker than it looks.
3. **What am I stopping?** Count real interruptions: normal traps you can set
   + hand traps in hand. One disruption vs a combo deck is often not enough —
   look for two.
4. **Am I bricking?** No trap + no way to start = mulligan-quality (MD has no
   mulligan, so this informs risk-taking, not a redraw).

The profiler quantifies steps 1–3 with exact opening odds so "this hand type
is rare/common" is a number, not a vibe.

## 3. Hold vs flip — the central decision

Because your face-downs are hidden, every set card is both a threat and a
bluff. Default heuristics (override with a read):
- **Flip removal on the enabler, not the payoff.** Kill the card that starts
  the combo (the searcher / the one-card starter), not the end-board monster.
- **Bait first vs decks with their own interaction.** If they hold up
  Called-by / Ash, represent a trap and make them commit before you spend
  your real one.
- **Respect SEGOC and chain timing.** Many blowouts come from activating in
  the wrong window. When unsure, check `rules CHAINS`, `rules SEGOC`,
  `rules IF-WHEN` (missing timing), and `rules DAMAGE-STEP`.
- **Lady/Lovely change the math.** With a Labrynth boss up, your normal traps
  gain extra value (search / recycle / burn) — sequence to trigger those
  bonuses, and protect the boss.

## 4. Maxx "C" decisions

- **On your opponent:** activate when they are committed to a long Special-
  Summon chain and can't easily stop. Expect them to either stop early or
  push through — the value is the tax, not the cards.
- **Against you:** if they Maxx "C" you, Labrynth can often just set and pass
  (you don't need to over-extend), which punishes the activation. Play to your
  strength — you're the control deck.

## 5. Closing games

- Pure/Fiendsmith lines grind and win with Lady beats + recursion.
- Cannon lines look for **Simultaneous Equation Cannons** to wipe/close.
- Always know your clock: reactive decks lose to time and to decking-relevant
  grind, so identify the turn you shift from defense to closing.

---

### How the advisor uses this in chat
You share a hand (screenshot or text) and whether you're on the play/draw.
The advisor: identifies each card + role from the profile, runs the triage,
quotes the exact odds where relevant, cites the specific rule for any timing
question, names the recommended line, and lists the **"if they have X"**
branches. It recommends, with reasons — you make the call.
