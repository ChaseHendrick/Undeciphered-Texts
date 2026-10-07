"""Every 196-letter window of a larger Latin library against the cells' letter counts. Not a reading.

Latin fits the cells' counts best of the languages screened
(engine.dagapeyeff_screen): its closest Thomistic window needs 4 errors. Pelling
(Cipher Mysteries, 1 May 2021) proposed matching sorted letter counts against a
large library. Under a one-to-one letter key and any transposition, a window
whose sorted counts equal the cells' would be a possible source text, so a
window that needs 0, 1 or 2 errors is a concrete lead to search.

This screen takes every window, with a stride of one letter, of six Universal
Dependencies Latin treebanks (classical, Vulgate, medieval, Dante's Latin,
charters, Thomas Aquinas) and fifteen Latin books from Project Gutenberg, all
fetched into the ignored work/ folder. Accents are removed and J is folded
into I. For the closest windows only a source and a letter offset are
stored, never the letters.

No letter string is stored.
"""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

import numpy as np

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_errors import sorted_counts
from engine.dagapeyeff_foursquare import PLAIN
from engine.dagapeyeff_screen import fold, text_of

_GUTENBERG = Path(__file__).resolve().parents[1] / "work" / "external" / "gutenberg"
_LETTERS = 196
_CHUNK = 200_000
_KEEP = 12
TREEBANKS = ("Latin-ITTB", "Latin-Perseus", "Latin-PROIEL", "Latin-UDante", "Latin-LLCT", "Latin-CIRCSE")
# Project Gutenberg ebook numbers: Virgil, Cicero, Augustine, Descartes, Caesar, Plautus, Newton,
# Vitruvius, Sallust, Apicius and Boethius, in Latin.
BOOKS = (227, 229, 231, 47001, 14970, 226, 33849, 23306, 218, 16564, 28233, 51812, 7402, 16439, 13316)


def _book(number: int) -> str:
    path = _GUTENBERG / f"pg{number}.txt"
    if not path.exists():
        _GUTENBERG.mkdir(parents=True, exist_ok=True)
        url = f"https://www.gutenberg.org/cache/epub/{number}/pg{number}.txt"
        with urllib.request.urlopen(url, timeout=60) as response:
            path.write_bytes(response.read())
    raw = path.read_text(encoding="utf-8", errors="replace")
    start = re.search(r"^\*\*\* ?START OF.*$", raw, re.M)
    end = re.search(r"^\*\*\* ?END OF.*$", raw, re.M)
    body = raw[start.end() if start else 0:end.start() if end else len(raw)]
    return fold(" ".join(paragraph for paragraph in re.split(r"\n\s*\n", body) if is_latin(paragraph)))


_LATIN_WORDS = frozenset("et in est non ad cum quod ut sed qui quae quam enim si nec atque esse ab ex de per".split())
_ENGLISH_WORDS = frozenset("the and of to is that which with was for it his be by this not are as".split())


def is_latin(paragraph: str) -> bool:
    """Gutenberg editions mix English notes into the Latin; keep paragraphs led by Latin function words."""
    words = re.findall(r"[a-z]+", paragraph.lower())
    latin = sum(word in _LATIN_WORDS for word in words)
    return latin >= 2 and latin > 2 * sum(word in _ENGLISH_WORDS for word in words)


def errors_per_window(letters: str, target: np.ndarray) -> np.ndarray:
    """Fewest single-cell errors for every window, stride one."""
    ints = np.asarray([PLAIN.index(ch) for ch in letters], dtype=np.int16)
    running = np.zeros((len(ints) + 1, 25), dtype=np.int32)
    running[1:] = np.cumsum(np.eye(25, dtype=np.int32)[ints], axis=0)
    total = len(ints) - _LETTERS + 1
    out = np.empty(total, dtype=np.int16)
    for start in range(0, total, _CHUNK):
        stop = min(total, start + _CHUNK)
        counts = running[start + _LETTERS:stop + _LETTERS] - running[start:stop]
        out[start:stop] = np.abs(-np.sort(-counts, axis=1) - target).sum(axis=1) // 2
    return out


def _row(letters: str, target: np.ndarray) -> tuple[dict, list[tuple[int, int]]]:
    errors = errors_per_window(letters, target)
    order = np.argsort(errors, kind="stable")
    best, kept = [], []
    for at in order:
        if len(best) == _KEEP:
            break
        # One window per neighbourhood: overlapping windows are not separate texts.
        if all(abs(int(at) - other) >= _LETTERS for other in kept):
            kept.append(int(at))
            best.append((int(errors[at]), int(at)))
    return {
        "letters": len(letters),
        "windows": int(len(errors)),
        "fewest_errors": int(errors.min()),
        "median_errors": float(np.median(errors)),
        "within_2": int((errors <= 2).sum()),
        "within_4": int((errors <= 4).sum()),
        "within_8": int((errors <= 8).sum()),
    }, best


@frozen("dagapeyeff-latinlib")
def latinlib_report() -> dict:
    target = sorted_counts(_cells()).astype(np.int32)
    sources = {f"UD_{name}": text_of(name) for name in TREEBANKS}
    sources.update({f"gutenberg-{number}": _book(number) for number in BOOKS})
    rows, closest = {}, []
    for name, letters in sources.items():
        rows[name], best = _row(letters, target)
        closest += [{"source": name, "offset": offset, "errors": errors} for errors, offset in best]
    closest.sort(key=lambda item: (item["errors"], item["source"], item["offset"]))
    return {
        "solved": False,
        "claimed_plaintext": None,
        "sources": rows,
        "letters": sum(row["letters"] for row in rows.values()),
        "windows": sum(row["windows"] for row in rows.values()),
        "fewest_errors": min(row["fewest_errors"] for row in rows.values()),
        "within_2": sum(row["within_2"] for row in rows.values()),
        "within_4": sum(row["within_4"] for row in rows.values()),
        "closest": closest[:_KEEP],
    }
