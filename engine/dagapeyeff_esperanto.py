"""Esperanto against the cells' letter counts. A key-free screen. Not a reading.

engine.dagapeyeff_screen screened 39 languages from Universal Dependencies,
which has no Esperanto treebank. Esperanto has been proposed for the challenge
(Tim Marland's project, 2026), and like Latin it uses few letters: no Q, W, X
or Y. This screen counts it the same way: the fewest single-cell errors that
turn a 196-letter window into the cells' counts, under any one-to-one key and
any order.

The texts are ten Esperanto books from Project Gutenberg, fetched into the
ignored work/ folder; only counts are stored. Several use the x-system (cx for
the hatted c), which is turned back into hatted letters first. Hats are then
removed, so the hatted c counts as C, and J is folded into I as in the book's
square.

No letter string is stored.
"""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import sorted_counts
from engine.dagapeyeff_screen import fold, screen

_WORK = Path(__file__).resolve().parents[1] / "work" / "external" / "gutenberg"
# Project Gutenberg ebook numbers: prose and drama written in or translated into Esperanto.
BOOKS = (17482, 20006, 21195, 23093, 23670, 24145, 24763, 26359, 31348, 45612)
_X_SYSTEM = {"cx": "ĉ", "gx": "ĝ", "hx": "ĥ", "jx": "ĵ", "sx": "ŝ", "ux": "ŭ",
             "Cx": "Ĉ", "Gx": "Ĝ", "Hx": "Ĥ", "Jx": "Ĵ", "Sx": "Ŝ", "Ux": "Ŭ",
             "CX": "Ĉ", "GX": "Ĝ", "HX": "Ĥ", "JX": "Ĵ", "SX": "Ŝ", "UX": "Ŭ"}


def _fetch(number: int) -> str:
    path = _WORK / f"pg{number}.txt"
    if not path.exists():
        _WORK.mkdir(parents=True, exist_ok=True)
        url = f"https://www.gutenberg.org/cache/epub/{number}/pg{number}.txt"
        with urllib.request.urlopen(url, timeout=60) as response:
            path.write_bytes(response.read())
    return path.read_text(encoding="utf-8", errors="replace")


def body(raw: str) -> str:
    """The book between Gutenberg's start and end lines, x-system turned into hats."""
    start = re.search(r"^\*\*\* ?START OF.*$", raw, re.M)
    end = re.search(r"^\*\*\* ?END OF.*$", raw, re.M)
    text = raw[start.end() if start else 0:end.start() if end else len(raw)]
    if len(re.findall(r"[cghjsu]x", text, re.I)) > len(re.findall("[ĉĝĥĵŝŭ]", text, re.I)):
        text = re.sub(r"[cghjsuCGHJSU][xX]", lambda match: _X_SYSTEM[match.group(0)], text)
    return text


def letters() -> str:
    return "".join(fold(body(_fetch(number))) for number in BOOKS)


@frozen("dagapeyeff-esperanto")
def esperanto_report() -> dict:
    target = sorted_counts(_cells())
    books = {str(number): screen(fold(body(_fetch(number))), target)["letters"] for number in BOOKS}
    row = screen(letters(), target)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "source": "Project Gutenberg Esperanto ebooks " + ", ".join(str(number) for number in BOOKS),
        "book_letters": books,
        "esperanto": row,
    }
