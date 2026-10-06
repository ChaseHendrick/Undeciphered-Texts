"""Five short attacks on the cells, each with its own control. Not a reading.

1. Nulls by place. Codes and Ciphers (p. 111) allows a dummy at every third,
   fourth or fifth letter. Every phase of periods 3, 4 and 5 is dropped, and
   every one of the 14 grid columns (period 14), then the rest is solved as a
   keyed Polybius square.
2. Rare symbols as word spaces. The five symbols seen only in the last grid
   column would then be the only spaces. This is a count.
3. The row digit as filler. The column digits alone, paired, give 98 symbols
   of a 5 by 5 square. Their coincidence rate is compared with English of
   that length and with shuffles.
4. The cells read backwards, solved as a keyed square.

The solver is engine/dagapeyeff_additive.c at period 1, a plain keyed square.
Planted held-out English of each length shows its power, and shuffled cells
are the control. No letter string is stored.
"""

from __future__ import annotations

import os
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from engine.dagapeyeff_add import _cells
from engine.dagapeyeff_additive import _kernel, _tables, anneal
from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_foursquare import PLAIN, _HELD, _held, _model
from engine.dagapeyeff_swarm import challenge_pairs

_SEED = 20261007
_RESTARTS = 2
_STEPS = 300_000
_SHUFFLES = 8
_PROSE_FLOOR = -2.5
_RECOVERED = 0.9
NULL_PERIODS = (3, 4, 5, 14)
_WINDOW_STEP = 97


def drop_phase(cells: list, period: int, phase: int) -> list:
    return [cell for i, cell in enumerate(cells) if i % period != phase]


def rare_symbols(cells: list[int]) -> set[int]:
    """Symbols that occur only in the last of the 14 grid columns."""
    inside = {cell for i, cell in enumerate(cells) if i % 14 != 13}
    return {cell for i, cell in enumerate(cells) if i % 14 == 13} - inside


def column_pairs(phase: int, cells: list[int] | None = None) -> list[int]:
    """The column digit of each printed pair, paired again, as cells 0 to 24."""
    if cells is None:
        digits = ["12345".index(pair[1]) for pair in challenge_pairs()]
    else:
        digits = [cell % 5 for cell in cells]
    digits = digits[phase:]
    return [digits[k] * 5 + digits[k + 1] for k in range(0, len(digits) - 1, 2)]


def coincidence(symbols: list) -> float:
    n = len(symbols)
    return sum(c * (c - 1) for c in Counter(symbols).values()) / (n * (n - 1))


def _windows(length: int):
    for name in _HELD:
        prose = _held(name)
        for start in range(0, len(prose) - length, _WINDOW_STEP):
            yield prose[start:start + length]


def spaces_check() -> dict:
    cells = _cells()
    rare = rare_symbols(cells)
    separators = sum(cell in rare for cell in cells)
    letters = len(cells) - separators
    distinct = len({cell for cell in cells if cell not in rare})
    lengths = []
    fewest = 26
    for name in ("neural_train_austen.txt", "neural_heldout_doyle.txt", "neural_audit_wells.txt"):
        words = [word for word in (_held_words(name)) if word]
        for start in range(0, len(words) - 60, 7):
            run = []
            total = 0
            for word in words[start:]:
                if total + len(word) > letters:
                    break
                run.append(word)
                total += len(word)
            lengths.append(total / len(run))
            fewest = min(fewest, len(set("".join(run))))
    return {
        "rare_symbols": len(rare),
        "separators": separators,
        "letters": letters,
        "distinct_letters": distinct,
        "mean_word_length": round(letters / (separators + 1), 2),
        "english_runs": len(lengths),
        "english_longest_mean_word": round(max(lengths), 2),
        "english_fewest_distinct": fewest,
    }


def _held_words(name: str) -> list[str]:
    from engine.dagapeyeff_foursquare import _DATA

    text = (_DATA / name).read_text(encoding="utf-8").upper().replace("J", "I")
    return ["".join(ch for ch in word if "A" <= ch <= "Z") for word in text.split()]


def column_digit_check() -> dict:
    rng = random.Random(_SEED)
    rows = {}
    for phase in (0, 1):
        symbols = column_pairs(phase)
        english = [coincidence(window) for window in _windows(len(symbols))]
        shuffled = []
        digits = ["12345".index(pair[1]) for pair in challenge_pairs()][phase:]
        for _ in range(2000):
            mixed = list(digits)
            rng.shuffle(mixed)
            shuffled.append(coincidence([mixed[k] * 5 + mixed[k + 1] for k in range(0, len(mixed) - 1, 2)]))
        value = coincidence(symbols)
        rows[f"phase {phase}"] = {
            "symbols": len(symbols),
            "coincidence": round(value, 4),
            "english_windows": len(english),
            "english_lowest": round(min(english), 4),
            "english_at_or_below": sum(x <= value for x in english),
            "shuffles_at_or_above": sum(x >= value for x in shuffled),
            "shuffles": len(shuffled),
        }
    return rows


def _per_letter(text: str) -> float:
    return _model().score([ord(ch) - 65 for ch in text]) / (len(text) - 3)


def variants(cells: list[int]) -> dict[str, list[int]]:
    out = {}
    for period in NULL_PERIODS:
        for phase in range(period):
            out[f"nulls {period}:{phase}"] = drop_phase(cells, period, phase)
    out["reversed"] = cells[::-1]
    out["column digits 0"] = column_pairs(0, cells)
    return out


@frozen("dagapeyeff-quick")
def quick_report() -> dict:
    rng = random.Random(_SEED)
    cells = _cells()
    printed = variants(cells)
    jobs = []
    redrawn = 0
    for label in ("nulls 3:0", "nulls 4:0", "nulls 5:0", "nulls 14:0", "reversed", "column digits 0"):
        length = len(printed[label])
        prose = _held(_HELD[len(jobs) % len(_HELD)])
        while True:
            start = rng.randrange(len(prose) - length)
            text = prose[start:start + length]
            if _per_letter(text) >= _PROSE_FLOOR:
                break
            redrawn += 1
        square = list(range(25))
        rng.shuffle(square)
        where = {PLAIN[square[cell]]: cell for cell in range(25)}
        jobs.append(("planted", -1, label, [where[ch] for ch in text], text, rng.randrange(1 << 40)))
    sources = [cells]
    for _ in range(_SHUFFLES):
        mixed = list(cells)
        rng.shuffle(mixed)
        sources.append(mixed)
    for index, source in enumerate(sources):
        for label, run in variants(source).items():
            jobs.append(("cells" if index == 0 else "shuffle", index, label, run, None, rng.randrange(1 << 40)))

    _kernel()
    _tables()
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
        results = list(pool.map(lambda job: anneal(job[3], 1, "both", job[5], _RESTARTS, _STEPS), jobs))

    planted = []
    searched = {}
    best_by_source = {}
    for (kind, index, label, run, text, _), (score, letters) in zip(jobs, results):
        if kind == "planted":
            planted.append({
                "for": label,
                "letters": len(text),
                "true_per_letter": round(_per_letter(text), 4),
                "found_per_letter": round(score, 4),
                "letters_right": round(sum(chr(65 + x) == ch for x, ch in zip(letters, text)) / len(text), 4),
            })
            continue
        score = round(score, 4)
        best_by_source[index] = max(best_by_source.get(index, -99.0), score)
        row = searched.setdefault(label, {"letters": len(run), "per_letter": None, "shuffles": []})
        if kind == "shuffle":
            row["shuffles"].append(score)
        else:
            row["per_letter"] = score
    for row in searched.values():
        row["shuffles"].sort(reverse=True)
        row["shuffles_as_high"] = sum(score >= row["per_letter"] for score in row["shuffles"])
    best_label = max(searched, key=lambda label: searched[label]["per_letter"])
    shuffle_bests = sorted((best_by_source[i] for i in range(1, len(sources))), reverse=True)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "search": {"restarts": _RESTARTS, "steps": _STEPS, "variants": len(printed), "shuffles": _SHUFFLES},
        "planted": planted,
        "planted_redrawn": redrawn,
        "planted_recovered": sum(row["letters_right"] >= _RECOVERED for row in planted),
        "planted_lowest_true": min(row["true_per_letter"] for row in planted),
        "searched": searched,
        "searched_best": {"variant": best_label, "per_letter": searched[best_label]["per_letter"]},
        "shuffle_bests": shuffle_bests,
        "shuffle_bests_as_high": sum(score >= searched[best_label]["per_letter"] for score in shuffle_bests),
        "spaces": spaces_check(),
        "column_digits": column_digit_check(),
    }
