"""A keyword dictionary attack on the book's own transpositions. Not a reading.

The book's double transposition (copied from Kerckhoffs, Pelling 2017) turns
a keyword into a column order by alphabetical rank, and was printed in the
decryption direction. If the challenge used a keyword transposition, the
order comes from a word, and words can be listed.

Each candidate keyword is applied to the cells, read as 25 symbols, in six
ways: single columnar undone, single columnar done, double columnar with the
same key undone twice, done twice, and, for 14 letters, the square method
with the same key on rows and columns, both ways. Doing a transposition where
undoing was meant covers the book's reversed direction.

The screen is successive-symbol information, which no letter key can change.
The right order of a real text scores near same-length English, about 1.0;
wrong orders of the cells score near 0.6. Planted texts, under random
lexicon keywords and random variants, check that the screen puts the true
keyword first. Shuffled cells get the same keyword list as the control. The
best few candidates on the cells then get the default substitution solver.
No letter string is stored.
"""

from __future__ import annotations

import heapq
import random
from pathlib import Path

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_order import _mi
from engine.neural_grade import letters_az, load_training_prose
from engine.solvers.adfgvx import columnar_decrypt, columnar_encrypt
from engine.solvers.substitution import solve_substitution

_LEXICON = Path(__file__).resolve().parent / "data" / "tridigital_lexicon.txt"
_SEED = 20261016
_SIDE = 14
_PHRASE_WORDS = 2000
_PLANTS = 6
_NULL_DRAWS = 2
_SOLVE_TOP = 3
# Names from the book, its sources and its author. Order does not matter.
BOOK_WORDS = (
    "SCHUVALOW", "SCHUVALOF", "SCHUVALOV", "KERCKHOFFS", "NIHILIST", "NIHILISTS", "AGAPEYEFF",
    "DAGAPEYEFF", "ALEXANDER", "ALEXANDERDAGAPEYEFF", "CODESANDCIPHERS", "CRYPTOGRAPHY",
    "CRYPTOGRAM", "OXFORD", "OXFORDUNIVERSITYPRESS", "POLYBIUS", "CHALLENGE", "REUNION",
    "PLAYFAIR", "VIGENERE", "PORTA", "TRITHEMIUS", "CARTOGRAPHER", "MAUGERSBURY",
)


def _letters(cells: list[int]) -> str:
    return "".join(chr(65 + cell) for cell in cells)


def _square(text: str, keyword: str, undo: bool) -> str:
    """The same key on the columns and on the rows of the 14 by 14 square."""
    order = sorted(range(_SIDE), key=lambda i: (keyword[i], i))
    rows = [text[r * _SIDE:(r + 1) * _SIDE] for r in range(_SIDE)]
    if undo:
        rows_back = [""] * _SIDE
        for rank, index in enumerate(order):
            rows_back[index] = rows[rank]
        out = []
        for row in rows_back:
            cells = [""] * _SIDE
            for rank, index in enumerate(order):
                cells[index] = row[rank]
            out.append("".join(cells))
        return "".join(out)
    rows = ["".join(row[index] for index in order) for row in rows]
    return "".join(rows[index] for index in order)


def readings(text: str, keyword: str) -> list[tuple[str, str]]:
    found = [
        ("single-undone", columnar_decrypt(text, keyword)),
        ("single-done", columnar_encrypt(text, keyword)),
        ("double-undone", columnar_decrypt(columnar_decrypt(text, keyword), keyword)),
        ("double-done", columnar_encrypt(columnar_encrypt(text, keyword), keyword)),
    ]
    if len(keyword) == _SIDE and len(text) == _SIDE * _SIDE:
        found.append(("square-undone", _square(text, keyword, undo=True)))
        found.append(("square-done", _square(text, keyword, undo=False)))
    return found


def keywords() -> list[str]:
    words = [line.strip().upper() for line in _LEXICON.read_text(encoding="utf-8").splitlines()]
    words = [word for word in words if word.isalpha()]
    single = sorted({word for word in words if 5 <= len(word) <= 20} | set(BOOK_WORDS))
    common = [word for word in words[:_PHRASE_WORDS] if len(word) >= 2]
    by_length: dict[int, list[str]] = {}
    for word in common:
        by_length.setdefault(len(word), []).append(word)
    phrases = set()
    for first in common:
        for second in by_length.get(_SIDE - len(first), []):
            phrases.add(first + second)
    return single + sorted(phrases - set(single))


def screen(text: str, candidates: list[str], keep: int = 10) -> tuple[list[tuple[float, str, str]], int]:
    """The best few orders by successive-symbol information, and how many were scored."""
    best: list[tuple[float, str, str]] = []
    scored = 0
    for keyword in candidates:
        for name, reading in readings(text, keyword):
            item = (_mi(reading), keyword, name)
            scored += 1
            if len(best) < keep:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)
    return sorted(best, reverse=True), scored


@frozen("dagapeyeff-keywords")
def keyword_report() -> dict:
    candidates = keywords()
    drawn = random.Random(_SEED)
    prose = letters_az(load_training_prose()).replace("J", "I")
    plants = []
    for index in range(_PLANTS):
        start = 1500 + 1700 * index
        plain = prose[start:start + _SIDE * _SIDE]
        keyword = drawn.choice([word for word in candidates if len(word) in (7, 9, 14)])
        letters = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")
        shuffled = letters[:]
        drawn.shuffle(shuffled)
        substituted = plain.translate(str.maketrans("".join(letters), "".join(shuffled)))
        variant = drawn.choice([name for name, _ in readings(substituted, keyword)])
        made = {
            "single-undone": lambda t: columnar_encrypt(t, keyword),
            "single-done": lambda t: columnar_decrypt(t, keyword),
            "double-undone": lambda t: columnar_encrypt(columnar_encrypt(t, keyword), keyword),
            "double-done": lambda t: columnar_decrypt(columnar_decrypt(t, keyword), keyword),
            "square-undone": lambda t: _square(t, keyword, undo=False),
            "square-done": lambda t: _square(t, keyword, undo=True),
        }[variant](substituted)
        assert dict(readings(made, keyword))[variant] == substituted
        ranked, _count = screen(made, candidates)
        top_score, top_keyword, top_variant = ranked[0]
        plants.append({
            "keyword_length": len(keyword),
            "variant": variant,
            "true_mi": round(_mi(substituted), 4),
            "top_mi": round(top_score, 4),
            "true_ranked_first": dict(readings(made, top_keyword))[top_variant] == substituted,
        })
    cells = _letters(_cells())
    ranked, orders = screen(cells, candidates)
    best = ranked[0]
    nulls = []
    for _ in range(_NULL_DRAWS):
        shuffled = list(cells)
        drawn.shuffle(shuffled)
        nulls.append(round(screen("".join(shuffled), candidates)[0][0][0], 4))
    solved_top = []
    for score, keyword, variant in ranked[:_SOLVE_TOP]:
        reading = dict(readings(cells, keyword))[variant]
        result = solve_substitution(reading)
        solved_top.append({
            "mi": round(score, 4),
            "keyword_length": len(keyword),
            "variant": variant,
            "per_letter": round(result.score / (len(reading) - 3), 4),
            "reading_gate": bool(result.details["reading"]),
        })
    return {
        "solved": False,
        "claimed_plaintext": None,
        "keywords": len(candidates),
        "orders_scored": orders,
        "plants": plants,
        "plants_ranked_first": sum(row["true_ranked_first"] for row in plants),
        "cells_best_mi": round(best[0], 4),
        "cells_best_variant": best[2],
        "null_best_mi": nulls,
        "top_solved": solved_top,
        "scope": (
            "Keyword-ordered transpositions in both directions, screened by a score no letter key can "
            "change, with planted controls and shuffled cells. Keywords are listed by their effect, not "
            "kept as a finding. Not a reading. No letter string is stored."
        ),
    }
