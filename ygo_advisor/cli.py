"""Command-line entry point: `python -m ygo_advisor <command>`.

Commands
--------
  deck <file.ydk> [--second]   Profile a deck + opening-hand probabilities
  flavor                       Recommend a Labrynth flavor vs the meta snapshot
  rules <ANCHOR>               Print a cached Expanded Rule Book section
  rules-list                   List cached rule sections
  build-cards <file.ydk ...>   Fetch + cache card data for the given decks
  build-rules                  (Re)build the rules cache from the live article
"""
from __future__ import annotations

import argparse
import sys

from . import flavor as _flavor
from . import probability as prob
from . import rulebook
from .cards import CardDB
from .deck_profile import build_profile
from .ydk import load_ydk


def _cmd_deck(args) -> int:
    db = CardDB()
    dl = load_ydk(args.file)
    missing = [c for c in dl.all_ids if c not in db]
    if missing:
        print(f"[note] {len(missing)} card(s) not in cache; run: "
              f"python -m ygo_advisor build-cards {args.file}", file=sys.stderr)
    hand = 6 if args.second else 5
    p = build_profile(dl, db, hand_size=hand)
    print(f"# {p.name}  ({p.main_size} main / {len(dl.extra)} extra)")
    print(f"  breakdown: {p.counts}")
    print(f"  going {'second (6 cards)' if args.second else 'first (5 cards)'}\n")
    print("## Main deck")
    for e in p.entries:
        roles = ",".join(r for r in e.roles if r not in {"monster", "spell", "trap", "extra"})
        print(f"  {e.copies}x {e.name:<42} [{e.kind}] {roles}")
    print("\n## Opening-hand probabilities (exact, hypergeometric)")
    for label, val in p.openers.items():
        print(f"  {prob.pct(val):>7}  {label}")
    return 0


def _cmd_flavor(args) -> int:
    rec = _flavor.recommend()
    print(f"# Flavor recommendation vs meta {rec['meta_date']}\n")
    print("## Field (top decks by weight)")
    for name, tier, w in rec["field"][:8]:
        print(f"  T{tier}  {name:<26} weight {w}")
    print("\n## Threat weights (what the field does to you)")
    for t, w in list(rec["threat_weights"].items())[:10]:
        print(f"  {w:6.2f}  {t}")
    print("\n## Flavor ranking (field coverage)")
    for f in rec["flavor_ranking"]:
        print(f"  {f['coverage']:6.2f}  {f['name']}")
        print(f"          answers: {', '.join(f['covered_threats'])}")
    rf = rec["recommended_flavor"]
    print(f"\n>> Recommended: {rf['name']}")
    print(f"   best when: {rf['best_when']}")
    print("\n## Top individual tech vs this field")
    for name, score, note in rec["top_tech"]:
        print(f"  {score:6.2f}  {name:<34} {note}")
    return 0


def _cmd_rules(args) -> int:
    try:
        print(rulebook.load_section(args.anchor))
    except KeyError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


def _cmd_rules_list(args) -> int:
    for s in rulebook.list_sections():
        print(s)
    return 0


def _cmd_build_cards(args) -> int:
    db = CardDB()
    ids: set[int] = set()
    for f in args.files:
        ids |= load_ydk(f).all_ids
    fetched = db.fetch(sorted(ids))
    db.save()
    print(f"cached {len(db.cards)} cards total ({len(fetched)} newly fetched)")
    return 0


def _cmd_build_rules(args) -> int:
    written = rulebook.fetch_and_split()
    for anchor, n in written.items():
        print(f"  {n:6d} chars  {anchor}")
    print(f"wrote {len(written)} sections to {rulebook.RULES_DIR}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ygo_advisor")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("deck"); d.add_argument("file"); d.add_argument("--second", action="store_true")
    d.set_defaults(func=_cmd_deck)
    f = sub.add_parser("flavor"); f.set_defaults(func=_cmd_flavor)
    r = sub.add_parser("rules"); r.add_argument("anchor"); r.set_defaults(func=_cmd_rules)
    rl = sub.add_parser("rules-list"); rl.set_defaults(func=_cmd_rules_list)
    bc = sub.add_parser("build-cards"); bc.add_argument("files", nargs="+"); bc.set_defaults(func=_cmd_build_cards)
    br = sub.add_parser("build-rules"); br.set_defaults(func=_cmd_build_rules)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
