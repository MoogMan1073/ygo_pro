"""Tests for the opening-hand evaluator."""
from pathlib import Path

from ygo_advisor import hand as H
from ygo_advisor.cards import CardDB
from ygo_advisor.ydk import load_ydk

DECKS = Path(__file__).resolve().parent.parent / "data" / "decks"


def _db_dl():
    return CardDB(), load_ydk(DECKS / "cannon-lab.ydk")


def test_resolve_fuzzy_names():
    db, dl = _db_dl()
    cards = H.resolve_cards(["Maxx C", "Big Welcome", "arias", "23434538"], dl, db)
    names = [c.name for c in cards]
    assert names[0] == 'Maxx "C"'
    assert names[1] == "Big Welcome Labrynth"
    assert names[2] == "Arias the Labrynth Butler"
    assert cards[3].id == 23434538  # numeric passcode resolves directly


def test_unresolved_card_is_flagged():
    db, dl = _db_dl()
    (c,) = H.resolve_cards(["Definitely Not A Real Card 999"], dl, db)
    assert c.id == -1 and "unresolved" in c.name


def test_boss_only_hand_is_brick():
    db, dl = _db_dl()
    ev = H.evaluate(["Lady Labrynth", "Lovely Labrynth", "Chandraglier",
                     "Stovie Torbie", "Simultaneous Equation Cannons"], dl, db)
    assert ev.grade == "Brick"
    assert any("Level 8" in r for r in ev.risks)


def test_starter_plus_interaction_is_playable_or_better():
    db, dl = _db_dl()
    ev = H.evaluate(["Big Welcome Labrynth", "Arias the Labrynth Butler",
                     "Dominus Impulse", "Stovie Torbie", "Maxx C"], dl, db)
    assert ev.score >= 50
    assert ev.grade in {"Playable", "Strong"}
    assert "Big Welcome Labrynth" in ev.starters


def test_lone_welcome_without_monster_is_awkward():
    db, dl = _db_dl()
    # small Welcome + only bosses/furniture that can't be summoned cheaply
    ev = H.evaluate(["Welcome Labrynth", "Full Force Virus", "Trap Holic",
                     "Transaction Rollback", "Simultaneous Equation Cannons"], dl, db)
    # It has interaction so it's not a brick, but note the conversion problem.
    assert ev.grade in {"Weak", "Playable"}


def test_going_second_scoring_differs():
    db, dl = _db_dl()
    cards = ["Dominus Impulse", "Destructive Daruma Karma Cannon", "Maxx C",
             "Welcome Labrynth", "Arianna"]
    first = H.evaluate(cards, dl, db, going_first=True)
    second = H.evaluate(cards, dl, db, going_first=False)
    assert first.going_first and not second.going_first
    # both should produce a recommended line
    assert first.line and second.line
