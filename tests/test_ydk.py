"""Tests for the .ydk parser and role tagging."""
from pathlib import Path

from ygo_advisor import roles
from ygo_advisor.cards import CardDB
from ygo_advisor.ydk import load_ydk, parse_ydk

DECKS = Path(__file__).resolve().parent.parent / "data" / "decks"


def test_parse_sections():
    text = "#created by x\n#main\n111\n111\n222\n#extra\n333\n!side\n444\n"
    dl = parse_ydk(text, name="t")
    assert dl.main == [111, 111, 222]
    assert dl.extra == [333]
    assert dl.side == [444]
    assert dl.main_counts[111] == 2
    assert dl.all_ids == {111, 222, 333, 444}


def test_sample_decks_are_legal_sizes():
    for f in ("cannon-lab.ydk", "fydraulis-synchro-lab.ydk", "fiendsmith-lab.ydk"):
        dl = load_ydk(DECKS / f)
        assert 40 <= dl.main_size <= 60, f"{f} main deck out of range"
        assert len(dl.extra) <= 15, f"{f} extra deck too big"


def test_labrynth_core_roles():
    db = CardDB()
    # Big Welcome Labrynth should be a welcome-access starter.
    r = roles.roles_for(92714517, db.get(92714517))
    assert {"welcome_access", "starter"} <= r
    # Lady Labrynth is a boss.
    assert "boss" in roles.roles_for(81497285, db.get(81497285))
    # Maxx "C" is a hand trap.
    assert "handtrap" in roles.roles_for(23434538, db.get(23434538))
