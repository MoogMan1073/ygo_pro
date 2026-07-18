"""Access to the MasterDuelMeta *Expanded Rule Book* as local markdown.

WebFetch truncates the article (it's ~140 KB of text), so we fetch the
server-rendered HTML directly, split it into the 21 canonical sections the
user cares about, and cache each as ``rules/<ANCHOR>.md``. The anchors match
the ``[baseLink]#[rule]`` scheme (spaces -> ``-``).

At runtime you normally just call :func:`load_section` / :func:`list_sections`
against the cached files; :func:`fetch_and_split` (re)builds the cache.
"""
from __future__ import annotations

import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE_URL = "https://www.masterduelmeta.com/articles/guides/expanded-rule-book"
RULES_DIR = Path(__file__).resolve().parent.parent / "rules"
_UA = {"User-Agent": "Mozilla/5.0 (compatible; ygo_advisor/0.1)"}

# user-anchor -> ordered list of source h3 blocks, each:
#   (h3_title, start_marker_or_None, end_marker_or_None)
# start/end markers are sub-headings that carve one h3 block into two logical
# sections (used where the article merges two of the user's anchors).
ANCHOR_MAP: dict[str, list[tuple[str, str | None, str | None]]] = {
    "GETTING-STARTED":           [("Decks", None, None)],
    "THE-FIELD":                 [("The Game Field", None, None)],
    "GAME-CARDS":                [("Reading Game Cards", None, None)],
    "MONSTERS":                  [("All about Monsters!", None, None),
                                  ("Special Summoning with Card Effects", None, None),
                                  ("Tokens", None, None)],
    "SPELLS-TRAPS":              [("Magic Ruler? No, Spell Ruler!", None, None),
                                  ("Spells", None, None),
                                  ("Tricky Traps", None, None),
                                  ("Traps", None, None)],
    "PLAYING-THE-GAME":          [("The Duel", None, None), ("Phases", None, None)],
    "CHAINS":                    [("Time to build Chain Links", None, None),
                                  ("Some cards are just faster than others", None, None)],
    "SEGOC":                     [("TRIGGER WARNING", None, "PSCT")],
    "READING-RESOLVING-EFFECTS": [("TRIGGER WARNING", "PSCT", None)],
    "BATTLE-PHASE":              [("Battling", None, None)],
    "DAMAGE-STEP":               [("Battling", "Steps", None)],
    "ATK-DEF-MODIFICATION":      [("Boost!", None, None)],
    "FORGETTING":                [("Huh?", None, "Negation")],
    "NEGATIONS":                 [("Huh?", "Negation", None)],
    "IF-WHEN":                   [("Now or... then?", None, None)],
    "NOMI":                      [("No U", None, None)],
    "ADDITIONAL-NORMAL":         [("Normal Summon... then Normal Summon?", None, None)],
    "HIGHLANDER-CLAUSE":         [("This town ain't big enough for the two of us", None, None)],
    "PROHIBITION":               [("Absolutely not!", None, None)],
    "GAMETERMS":                 [("But what does it mean?", None, None)],
    "FAQ":                       [("How does this work?", None, None)],
}


# --- HTML -> ordered document items --------------------------------------
class _DocParser(HTMLParser):
    """Flatten article HTML into ordered heading/body items."""

    _HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
    _SKIP = {"script", "style", "nav", "svg", "button", "form"}
    _BREAKS = {"p", "li", "tr", "br", "div", "ul", "ol", "table", "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self) -> None:
        super().__init__()
        self.items: list[dict] = []
        self._skip = 0
        self._h_level: int | None = None
        self._h_buf: list[str] = []
        self._body: list[str] = []

    def _flush_body(self) -> None:
        text = re.sub(r"[ \t]+", " ", " ".join(self._body)).strip()
        text = re.sub(r"\n{2,}", "\n", text)
        if text:
            self.items.append({"type": "body", "text": text})
        self._body = []

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip += 1
        if tag in self._HEADINGS and self._skip == 0:
            self._flush_body()
            self._h_level = int(tag[1])
            self._h_buf = []
        elif tag in self._BREAKS and self._skip == 0:
            self._body.append("\n")

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip:
            self._skip -= 1
        if tag in self._HEADINGS and self._h_level is not None:
            text = re.sub(r"\s+", " ", "".join(self._h_buf)).strip()
            if text:
                self.items.append({"type": "heading", "level": self._h_level, "text": text})
            self._h_level = None

    def handle_data(self, data):
        if self._skip:
            return
        if self._h_level is not None:
            self._h_buf.append(data)
        else:
            self._body.append(data)


def _parse(html: str) -> list[dict]:
    p = _DocParser()
    p.feed(html)
    p._flush_body()
    return p.items


def _render(items: list[dict]) -> str:
    lines: list[str] = []
    for it in items:
        if it["type"] == "heading":
            lines.append("\n" + "#" * min(it["level"], 6) + " " + it["text"])
        else:
            lines.append(it["text"])
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def _slice_block(items: list[dict], h3_title: str, start: str | None, end: str | None) -> list[dict]:
    """Return the items of the named h3 block, optionally trimmed by markers."""
    n = len(items)
    i = 0
    while i < n:
        it = items[i]
        if it["type"] == "heading" and it["level"] == 3 and it["text"] == h3_title:
            break
        i += 1
    else:
        return []
    # collect from the h3 heading up to (but not including) the next h3
    block = [items[i]]
    j = i + 1
    while j < n and not (items[j]["type"] == "heading" and items[j]["level"] == 3):
        block.append(items[j])
        j += 1
    if start:
        for k, it in enumerate(block):
            if it["type"] == "heading" and it["text"] == start:
                block = [items[i]] + block[k:]  # keep the h3 title for context
                break
    if end:
        for k, it in enumerate(block):
            if it["type"] == "heading" and it["text"] == end:
                block = block[:k]
                break
    return block


def fetch_html(url: str = BASE_URL) -> str:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_and_split(out_dir: str | Path = RULES_DIR, url: str = BASE_URL) -> dict[str, int]:
    """(Re)build ``rules/<ANCHOR>.md`` from the live article.

    Returns a mapping of anchor -> character length written.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    items = _parse(fetch_html(url))
    written: dict[str, int] = {}
    index_lines = [
        "# Master Duel Expanded Rule Book — cached sections",
        "",
        f"Source: {url}",
        "",
        "Access any section with `[baseLink]#[ANCHOR]`.",
        "",
        "| Anchor | File |",
        "| --- | --- |",
    ]
    for anchor, blocks in ANCHOR_MAP.items():
        collected: list[dict] = []
        for (title, start, end) in blocks:
            collected += _slice_block(items, title, start, end)
        body = _render(collected) if collected else "_(section not found in source)_\n"
        header = f"# {anchor}\n\nSource: {url}#{anchor}\n\n"
        (out / f"{anchor}.md").write_text(header + body, encoding="utf-8")
        written[anchor] = len(body)
        index_lines.append(f"| `{anchor}` | [{anchor}.md]({anchor}.md) |")
    (out / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return written


# --- runtime loaders -----------------------------------------------------
def list_sections(rules_dir: str | Path = RULES_DIR) -> list[str]:
    d = Path(rules_dir)
    return sorted(p.stem for p in d.glob("*.md") if p.stem != "index")


def load_section(anchor: str, rules_dir: str | Path = RULES_DIR) -> str:
    """Load a cached section by anchor (case-insensitive, spaces->'-')."""
    key = anchor.strip().upper().replace(" ", "-")
    path = Path(rules_dir) / f"{key}.md"
    if not path.exists():
        raise KeyError(f"unknown rules section {anchor!r}; have: {list_sections(rules_dir)}")
    return path.read_text(encoding="utf-8")
