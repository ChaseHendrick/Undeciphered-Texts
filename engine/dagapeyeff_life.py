"""Searchable record of Alexander d'Agapeyeff, and a key test that uses only that record.

The JSON file is the list. search_life matches every word in a query against
the id, label, value, aliases, and source, so a later pass can ask for a
date or a rejected claim without rereading the prose note.

A name or a service number is then tried as a key. Keys dated after 1939 are
scored apart from keys he could already have used. Neither list is a reading.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

from engine.dagapeyeff_swarm import best_chi_square, challenge_pairs
from engine.language import ENGLISH_ORDER, get_model

_PATH = Path(__file__).resolve().parent / "data" / "dagapeyeff_life.json"
_ROWS = "67890"
_COLS = "12345"
_SEED = 20261004
_DRAWS = 100
_WIDTHS = (7, 14)


def load_life() -> dict:
    return json.loads(_PATH.read_text(encoding="utf-8"))


def search_life(query: str) -> list[dict]:
    """Every fact in which all of the query words occur. Empty query returns all."""
    words = [word.lower() for word in query.split() if word]
    found = []
    for fact in load_life()["facts"]:
        blob = " ".join(
            [
                fact["id"],
                fact["kind"],
                fact["label"],
                fact["value"],
                fact["source"],
                fact["confidence"],
                " ".join(fact["aliases"]),
                fact.get("letters") or "",
                fact.get("digits") or "",
                fact.get("when") or "",
            ]
        ).lower()
        if all(word in blob for word in words):
            found.append(fact)
    return found


def _keys(when: str) -> tuple[list[str], list[str]]:
    letters = []
    digits = []
    for fact in load_life()["facts"]:
        if fact["cipher_use"] != when:
            continue
        word = "".join(char for char in fact["letters"].upper() if char.isalpha())
        if len(word) >= 4:
            letters.append(word)
        number = "".join(char for char in fact["digits"] if char.isdigit())
        if number and set(number) != {"0"}:
            digits.append(number)
    return letters, digits


def _assign(pairs: tuple[str, ...]) -> str:
    """Frequency rank only. Ties break on the pair text so the string is fixed."""
    counts: dict[str, int] = {}
    for pair in pairs:
        counts[pair] = counts.get(pair, 0) + 1
    order = [letter for letter in ENGLISH_ORDER if letter != "J"]
    ranked = sorted(counts, key=lambda pair: (-counts[pair], pair))
    table = {pair: order[index] for index, pair in enumerate(ranked)}
    return "".join(table[pair] for pair in pairs)


def _perm(key: str, width: int) -> tuple[int, ...]:
    stream = (key * ((width // len(key)) + 1))[:width]
    return tuple(sorted(range(width), key=lambda index: (stream[index], index)))


def _columns(text: str, order: tuple[int, ...], undo: bool) -> str:
    width = len(order)
    rows = math.ceil(len(text) / width)
    if undo:
        placed = [""] * width
        cursor = 0
        for column in order:
            placed[column] = text[cursor:cursor + rows]
            cursor += rows
        return "".join(placed[column][row] for row in range(rows) for column in range(width))
    columns = [""] * width
    for index, letter in enumerate(text):
        columns[index % width] += letter
    return "".join(columns[column] for column in order)


def _mean_quadgram(text: str) -> float:
    model = get_model()
    seq = [ord(letter) - 65 for letter in text]
    return model.score(seq) / (len(seq) - 3)


def _running(pairs: tuple[str, ...], number: str) -> tuple[str, ...]:
    shifts = [int(digit) for digit in number]
    out = []
    for index, pair in enumerate(pairs):
        cell = (_ROWS.index(pair[0]) * 5 + _COLS.index(pair[1]) + shifts[index % len(shifts)]) % 25
        row, column = divmod(cell, 5)
        out.append(_ROWS[row] + _COLS[column])
    return tuple(out)


def search_life_keys() -> dict:
    """Score 1939 keys and later keys. Do not return a letter string."""
    pairs = challenge_pairs()
    labeled = _assign(pairs)
    printed = best_chi_square(pairs)
    drawn = random.Random(_SEED)
    columns = {}
    for when in ("1939", "later"):
        words, _numbers = _keys(when)
        scores = []
        for word in words:
            for width in _WIDTHS:
                order = _perm(word, width)
                for undo in (False, True):
                    scores.append(_mean_quadgram(_columns(labeled, order, undo)))
        best = max(scores)
        null_hits = 0
        for _ in range(_DRAWS):
            package = []
            for _word in words:
                for width in _WIDTHS:
                    order = list(range(width))
                    drawn.shuffle(order)
                    for undo in (False, True):
                        package.append(_mean_quadgram(_columns(labeled, tuple(order), undo)))
            if max(package) >= best - 1e-9:
                null_hits += 1
        columns[when] = {
            "keys": len(words),
            "trials": len(scores),
            "best_mean_quadgram": round(best, 4),
            "null_draws": _DRAWS,
            "null_as_high": null_hits,
        }
    digits = {}
    for when in ("1939", "later"):
        _words, numbers = _keys(when)
        scored = []
        for number in numbers:
            scored.append((best_chi_square(_running(pairs, number)), number))
        best_chi, best_number = min(scored)
        null = []
        for _ in range(_DRAWS):
            number = "".join(str(drawn.randrange(10)) for _ in range(5))
            null.append(best_chi_square(_running(pairs, number)))
        digits[when] = {
            "keys": len(numbers),
            "best_chi": round(best_chi, 2),
            "best_digits": best_number,
            "printed_chi": round(printed, 2),
            "null_draws": _DRAWS,
            "null_as_low": sum(1 for score in null if score <= best_chi + 1e-9),
            "null_median": round(sorted(null)[_DRAWS // 2], 2),
        }
    return {
        "claimed_plaintext": None,
        "solved": False,
        "schema": load_life()["schema"],
        "facts": len(load_life()["facts"]),
        "columns": columns,
        "running_digit": digits,
        "scope": (
            "Life words are column orders on a frequency ranking, and life numbers "
            "are a repeating shift of the 25 cells. A shift does not become plaintext. "
            "Keys from after 1939 are a control, not a candidate."
        ),
    }
