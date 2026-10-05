"""The common cells look like a fair die. Not a reading.

Sorted, the 196 cell counts are 20, 17, 17, 17, 17, 16, 15, 14, 12, 12, 11,
11, 9, and then 3, 2, 1, 1, 1. The cliff after the thirteenth cell is the
largest drop between neighbors. Those 13 cells hold 188 of 196, and their
counts are no less even than a fair 13-sided die would give. The index of
coincidence of 0.0697 that looks like English is what 13 equal cells give.

Each text picks its own cliff, the k with the largest ratio between the
k-th and the next count, and is scored at that k. The core is flat when its
chi-square against a fair k-sided die is no larger than the challenge's, and
full when it holds at least 188 of 196. English windows, the solved exercise,
and 19 ways of enciphering English are scored the same way. A family that
cannot make a flat, full core is not the family of this cipher. A family
that can is only a family. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter
from pathlib import Path

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import CONTROL, challenge_pairs
from engine.neural_grade import letters_az
from engine.solvers.playfair import playfair_encrypt

_PUBLIC = Path(__file__).resolve().parent / "data" / "neural_train_public.txt"
_SQUARE = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
_SEED = 20261011
_ENGLISH_DRAWS = 20000
_DIE_DRAWS = 20000
_FAMILY_DRAWS = 2000
_LENGTH = 196
_PERIODS = range(2, 50)
_PERIOD_DRAWS = 2000


def _counts(symbols) -> list[int]:
    return sorted(Counter(symbols).values(), reverse=True)


def cliff(counts: list[int]) -> int:
    """The k after which the sorted counts drop the most, by ratio. Ties keep the first."""
    best_k = len(counts)
    best_ratio = 1.0
    for k in range(1, len(counts)):
        ratio = counts[k - 1] / counts[k]
        if ratio > best_ratio:
            best_ratio = ratio
            best_k = k
    return best_k


def core(symbols) -> dict:
    """Distinct cells, the cliff, the core mass, and its chi-square against a fair die."""
    counts = _counts(symbols)
    k = cliff(counts)
    top = counts[:k]
    mean = sum(top) / k
    chi = sum((count - mean) ** 2 / mean for count in top)
    return {"distinct": len(counts), "cliff": k, "mass": sum(top), "chi": chi}


def _match(found: dict, target: dict) -> bool:
    return found["mass"] >= target["mass"] and found["chi"] <= target["chi"] + 1e-12


def _prose() -> list[int]:
    letters = letters_az(_PUBLIC.read_text(encoding="utf-8")).replace("J", "I")
    return [_SQUARE.index(char) for char in letters]


def _window(prose: list[int], drawn: random.Random, length: int) -> list[int]:
    start = drawn.randrange(len(prose) - length)
    return prose[start : start + length]


def _vigenere(period: int):
    def make(prose, drawn):
        key = [drawn.randrange(25) for _ in range(period)]
        return [(cell + key[index % period]) % 25 for index, cell in enumerate(_window(prose, drawn, _LENGTH))]

    return make


def _running(prose, drawn):
    text = _window(prose, drawn, _LENGTH)
    key = _window(prose, drawn, _LENGTH)
    return [(cell + shift) % 25 for cell, shift in zip(text, key)]


def _autokey(prose, drawn):
    previous = drawn.randrange(25)
    out = []
    for cell in _window(prose, drawn, _LENGTH):
        out.append((cell + previous) % 25)
        previous = cell
    return out


def _torus(period: int):
    def make(prose, drawn):
        key = [(drawn.randrange(5), drawn.randrange(5)) for _ in range(period)]
        out = []
        for index, cell in enumerate(_window(prose, drawn, _LENGTH)):
            down, across = key[index % period]
            out.append(((cell // 5 + down) % 5) * 5 + (cell % 5 + across) % 5)
        return out

    return make


def _column_shift(period: int):
    def make(prose, drawn):
        key = [drawn.randrange(5) for _ in range(period)]
        return [(cell // 5) * 5 + (cell % 5 + key[index % period]) % 5 for index, cell in enumerate(_window(prose, drawn, _LENGTH))]

    return make


def _bifid(period: int):
    def make(prose, drawn):
        square = list(range(25))
        drawn.shuffle(square)
        seat = {cell: index for index, cell in enumerate(square)}
        text = _window(prose, drawn, _LENGTH)
        out = []
        for start in range(0, _LENGTH, period):
            block = text[start : start + period]
            digits = [seat[cell] // 5 for cell in block] + [seat[cell] % 5 for cell in block]
            out.extend(square[digits[2 * index] * 5 + digits[2 * index + 1]] for index in range(len(block)))
        return out

    return make


def _offset(prose, drawn):
    digits = []
    for cell in _window(prose, drawn, _LENGTH + 1):
        digits.extend((cell // 5, cell % 5))
    digits = digits[1 : 2 * _LENGTH + 1]
    return [digits[2 * index] * 5 + digits[2 * index + 1] for index in range(_LENGTH)]


def _nulls(prose, drawn):
    filler = drawn.sample(range(25), 3)
    return _window(prose, drawn, _LENGTH - 20) + [drawn.choice(filler) for _ in range(20)]


def _homophonic(prose, drawn):
    common = [_SQUARE.index(char) for char in "ETAOIN"]
    out = []
    for cell in _window(prose, drawn, _LENGTH):
        if cell in common and drawn.random() < 0.5:
            out.append(25 + common.index(cell))
        else:
            out.append(cell)
    return out


def _playfair(prose, drawn):
    keyword = "".join(drawn.choice(_SQUARE) for _ in range(12))
    text = "".join(_SQUARE[cell] for cell in _window(prose, drawn, _LENGTH - 8))
    sealed = playfair_encrypt(text, keyword)
    return [_SQUARE.index(char) for char in sealed[:_LENGTH]]


def _two_cells(prose, drawn):
    symbols = drawn.sample(range(25), 13)
    table = drawn.sample([(left, right) for left in symbols for right in symbols], 25)
    out = []
    for cell in _window(prose, drawn, _LENGTH // 2):
        out.extend(table[cell])
    return out


def _two_cells_keyed(period: int):
    def make(prose, drawn):
        table = drawn.sample([(left, right) for left in range(13) for right in range(13)], 25)
        key = [drawn.randrange(13) for _ in range(period)]
        stream = []
        for cell in _window(prose, drawn, _LENGTH // 2):
            stream.extend(table[cell])
        return [(symbol + key[index % period]) % 13 for index, symbol in enumerate(stream)]

    return make


def _reduced(prose, drawn):
    letters = list(range(25))
    drawn.shuffle(letters)
    group = {letter: index % 13 for index, letter in enumerate(letters)}
    return [group[cell] for cell in _window(prose, drawn, _LENGTH)]


def _flat_core(prose, drawn):
    cells = drawn.sample(range(25), 18)
    return [drawn.choice(cells[:13]) for _ in range(188)] + [drawn.choice(cells[13:]) for _ in range(8)]


FAMILIES = (
    ("any transposition of a Polybius", lambda prose, drawn: _window(prose, drawn, _LENGTH)),
    ("vigenere period 2", _vigenere(2)),
    ("vigenere period 3", _vigenere(3)),
    ("vigenere period 5", _vigenere(5)),
    ("vigenere period 7", _vigenere(7)),
    ("vigenere period 14", _vigenere(14)),
    ("running key", _running),
    ("plaintext autokey", _autokey),
    ("both coordinates shifted, period 2", _torus(2)),
    ("both coordinates shifted, period 7", _torus(7)),
    ("column coordinate shifted, period 5", _column_shift(5)),
    ("bifid period 7", _bifid(7)),
    ("bifid over the whole text", _bifid(_LENGTH)),
    ("digit stream off by one", _offset),
    ("twenty nulls from three cells", _nulls),
    ("six common letters split in two", _homophonic),
    ("playfair", _playfair),
    ("two cells per letter from 13", _two_cells),
    ("two cells per letter from 13, then a period-7 key", _two_cells_keyed(7)),
    ("letters merged into 13 classes", _reduced),
    ("13 equal cells and a rare tail, no language", _flat_core),
)


def _english(prose: list[int], target: dict, length: int, draws: int, seed: int) -> dict:
    drawn = random.Random(seed)
    full = flat = both = narrow = 0
    for _ in range(draws):
        found = core(_window(prose, drawn, length))
        full += found["mass"] >= target["mass"]
        flat += found["chi"] <= target["chi"] + 1e-12
        both += _match(found, target)
        narrow += found["distinct"] <= target["distinct"]
    return {"draws": draws, "as_full": full, "as_flat": flat, "both": both, "as_narrow": narrow}


def _die(target: dict) -> int:
    drawn = random.Random(_SEED)
    k, mass = target["cliff"], target["mass"]
    as_flat = 0
    for _ in range(_DIE_DRAWS):
        counts = sorted(Counter(drawn.randrange(k) for _ in range(mass)).values(), reverse=True)
        counts += [0] * (k - len(counts))
        mean = mass / k
        if sum((count - mean) ** 2 / mean for count in counts) <= target["chi"] + 1e-12:
            as_flat += 1
    return as_flat


def _periodic_ic(stream: list, period: int) -> float:
    same = pairs = 0
    for start in range(period):
        column = stream[start::period]
        same += sum(count * (count - 1) for count in Counter(column).values())
        pairs += len(column) * (len(column) - 1)
    return same / pairs


def _period_scan(cells: list[str], core_cells: set[str]) -> dict:
    """The best stride on the core alone, against shuffles that may pick their own best stride."""
    stream = [cell for cell in cells if cell in core_cells]
    scores = {period: _periodic_ic(stream, period) for period in _PERIODS}
    best = max(scores, key=lambda period: (scores[period], -period))
    drawn = random.Random(_SEED + 3)
    as_high = 0
    for _ in range(_PERIOD_DRAWS):
        shuffled = stream[:]
        drawn.shuffle(shuffled)
        if max(_periodic_ic(shuffled, period) for period in _PERIODS) >= scores[best] - 1e-12:
            as_high += 1
    return {
        "core_letters": len(stream),
        "periods": [min(_PERIODS), max(_PERIODS)],
        "best_period": best,
        "best_ic": round(scores[best], 4),
        "draws": _PERIOD_DRAWS,
        "shuffles_as_high": as_high,
    }


@frozen("core")
def core_report() -> dict:
    prose = _prose()
    target = core(challenge_pairs())
    exercise_letters = "".join(char for char in CONTROL if char.isalpha())
    exercise_cells = tuple(exercise_letters[index : index + 2] for index in range(0, len(exercise_letters), 2))
    exercise = core(exercise_cells)
    drawn = random.Random(_SEED + 1)
    families = []
    for name, make in FAMILIES:
        matched = 0
        for _ in range(_FAMILY_DRAWS):
            if _match(core(make(prose, drawn)), target):
                matched += 1
        families.append({"family": name, "draws": _FAMILY_DRAWS, "flat_full_core": matched})
    language = [row for row in families if "no language" not in row["family"]]
    counts = Counter(challenge_pairs())
    core_cells = {cell for cell, _count in counts.most_common(target["cliff"])}
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(challenge_pairs()),
        "distinct": target["distinct"],
        "cliff": target["cliff"],
        "core_mass": target["mass"],
        "core_chi": round(target["chi"], 4),
        "die_draws": _DIE_DRAWS,
        "die_as_flat": _die(target),
        "english": _english(prose, target, _LENGTH, _ENGLISH_DRAWS, _SEED + 2),
        "exercise_cells": len(exercise_cells),
        "exercise_distinct": exercise["distinct"],
        "exercise_cliff": exercise["cliff"],
        "exercise_core_mass": exercise["mass"],
        "exercise_core_chi": round(exercise["chi"], 4),
        "families": families,
        "core_period": _period_scan(list(challenge_pairs()), core_cells),
        "language_families_reaching_5_percent": [
            row["family"] for row in language if row["flat_full_core"] * 20 >= row["draws"]
        ],
        "scope": (
            "The common cells are as even as a fair die, and no family that enciphers English in this sweep makes "
            "such a core. The core has no stride a shuffle cannot match, so a key on it would not be short and "
            "periodic. That narrows the family. It is not a reading."
        ),
    }
