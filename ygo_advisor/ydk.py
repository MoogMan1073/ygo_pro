"""Parse `.ydk` deck files into structured main / extra / side card-id lists.

The `.ydk` format is trivial: optional `#`-comment lines, three section
markers (`#main`, `#extra`, `!side`) and one integer card *passcode* per
line. That's all a decklist is under the hood — which is why we never need
the compressed `decks.ygoresources.com` URL encoding to read a deck.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Decklist:
    """A parsed decklist. Lists preserve copy counts (duplicates included)."""

    name: str = ""
    main: list[int] = field(default_factory=list)
    extra: list[int] = field(default_factory=list)
    side: list[int] = field(default_factory=list)

    @property
    def main_counts(self) -> Counter:
        return Counter(self.main)

    @property
    def extra_counts(self) -> Counter:
        return Counter(self.extra)

    @property
    def side_counts(self) -> Counter:
        return Counter(self.side)

    @property
    def main_size(self) -> int:
        return len(self.main)

    @property
    def all_ids(self) -> set[int]:
        return set(self.main) | set(self.extra) | set(self.side)


def parse_ydk(text: str, name: str = "") -> Decklist:
    """Parse the text of a `.ydk` file into a :class:`Decklist`."""
    section: str | None = None
    dl = Decklist(name=name)
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        if low.startswith("#main"):
            section = "main"
            continue
        if low.startswith("#extra"):
            section = "extra"
            continue
        if low.startswith("!side"):
            section = "side"
            continue
        if line.startswith("#"):  # e.g. "#created by ..."
            continue
        if not line.lstrip("-").isdigit():
            continue  # ignore stray non-numeric lines defensively
        cid = int(line)
        if section == "main":
            dl.main.append(cid)
        elif section == "extra":
            dl.extra.append(cid)
        elif section == "side":
            dl.side.append(cid)
    return dl


def load_ydk(path: str | Path) -> Decklist:
    """Load and parse a `.ydk` file from disk (filename becomes the name)."""
    p = Path(path)
    return parse_ydk(p.read_text(encoding="utf-8", errors="replace"), name=p.stem)
