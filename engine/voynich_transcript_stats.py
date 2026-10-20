"""Transcription-robustness statistics for the frozen Voynich transliterations.

Family 1 of the Voynich ledger asks whether statistics survive a change of
transcription. This module computes the declared statistics on the shared
loci of ZL and IT, the two EVA-family files of the frozen corpus, and
compares the two files with controls that show what the numbers look like
when the answer is different.

Declared statistics, all over the same locus set (loci shared by ZL and IT,
whole reserved folios excluded, loci without words excluded):
- glyph (EVA character) frequencies, with one '@nnn;' as one glyph and a
  maximal run of question marks as one glyph;
- sign n-grams of orders 2, 3 and 4 inside words;
- word (token) frequencies and type counts;
- token length distribution (EVA characters per token).

Comparison metric: Spearman rank correlation over the types both files
share, per statistic. Verdict criteria, fixed in the tests before the run:
order one and two statistics must agree far above the within-file resampling
baseline only if the transcriptions really measure the same text, and a
planted relabelling of IT must be detected by a clear margin.

Reservation discipline: ten whole folios are chosen deterministically, by
sorting folio names under a seed-key hash, before any statistics are
computed. The selection function reads only folio names and locus presence,
never the text, so the reservation cannot be tuned to the statistics. These
ten folios stay out of every later Voynich family until their test role in
family 3.

Nothing here proposes a reading of the manuscript. This is a measurement of
how much two published transcriptions of the same text move with transcription
choice.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np

from engine.voynich_compare import index_loci
from engine.voynich_ivtff import DATA_DIR, load

RESERVED_SEED = 20261020
RESERVED_COUNT = 10
PLANT_SHIFT = 1
PLANT_TYPES = 10

STATS_PATH = (
    Path(DATA_DIR).resolve().parent.parent.parent
    / "docs" / "research-notes" / "voynich-transcript-stats.json"
)

_HIGH_ASCII_RE = re.compile(r"@\d{3};")
_QUESTION_RUN_RE = re.compile(r"\?{3,}")
_ORDERS = (1, 2, 3, 4)
_WORDS_KEY = "word1"


def _word_glyphs(word: str) -> str:
    """The declared glyph form of one word string from the parser."""
    work = _HIGH_ASCII_RE.sub(
        lambda match: chr(0x100 + int(match.group(0)[1:4])), word
    )
    return _QUESTION_RUN_RE.sub("?", work)


def shared_worded_keys() -> dict[str, list[tuple[str, int]]]:
    """Folio names over loci shared by ZL and IT with words in both files."""
    index_a = index_loci(load("ZL"))
    index_b = index_loci(load("IT"))
    folio_loci: dict[str, list[tuple[str, int]]] = {}
    for key in sorted(set(index_a) & set(index_b)):
        if index_a[key].words and index_b[key].words:
            folio_loci.setdefault(key[0], []).append(key)
    return folio_loci


def reserved_folios() -> list[str]:
    """Ten whole folios reserved before any statistics exist.

    Deterministic and blind to the text: folio names sorted under a
    seed-keyed digest, taking the first ten. No word or glyph reaches this
    function's inputs. The result is frozen in the ledger and the tests.
    """
    folios = sorted(shared_worded_keys())
    ordered = sorted(
        folios,
        key=lambda name: hashlib.sha256(
            f"{RESERVED_SEED}:{name}".encode()
        ).digest(),
    )
    return ordered[:RESERVED_COUNT]


def used_keys() -> list[tuple[str, int]]:
    """The shared, worded locus keys outside the reserved folios."""
    reserved = set(reserved_folios())
    keys = []
    for folio, loci in sorted(shared_worded_keys().items()):
        if folio in reserved:
            continue
        keys.extend(loci)
    return keys


def _ngrams(word: str, order: int) -> Counter:
    if order == 1:
        return Counter(word)
    return Counter(word[start:start + order] for start in range(len(word) - order + 1))


def _counts(words: list[str]) -> dict:
    """One pass over the declared statistics for one locus-side text."""
    words_counter: Counter[str] = Counter()
    length_counter: Counter[int] = Counter()
    ngram: dict[int, Counter] = {order: Counter() for order in _ORDERS}
    for word in words:
        glyphs = _word_glyphs(word)
        words_counter[word] += 1
        length_counter[len(glyphs)] += 1
        for order in _ORDERS:
            ngram[order].update(_ngrams(glyphs, order))
    return {
        "ngram": ngram,
        "words": words_counter,
        "lengths": length_counter,
        "tokens": sum(length_counter.values()),
    }


def _spearman(counts_a: Counter, counts_b: Counter) -> tuple[float, int]:
    """Rank correlation over the types both sides share, and their number."""
    shared = set(counts_a) & set(counts_b)
    if len(shared) < 2:
        return float("nan"), len(shared)
    x = np.array([counts_a[ctype] for ctype in shared], dtype=float)
    y = np.array([counts_b[ctype] for ctype in shared], dtype=float)
    return float(_spearman_from_values(x, y)), len(shared)


def _spearman_from_values(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(_average_ranks(x), _average_ranks(y))[0, 1])


def _average_ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="stable")
    ranks = np.empty(len(values), dtype=float)
    sorted_values = values[order]
    rank_start = 0
    while rank_start < len(values):
        rank_end = rank_start
        while rank_end < len(values) and sorted_values[rank_end] == sorted_values[rank_start]:
            rank_end += 1
        ranks[order[rank_start:rank_end]] = (rank_start + rank_end - 1) / 2.0 + 1
        rank_start = rank_end
    return ranks


def _relabel(word: str, mapping: dict[str, str]) -> str:
    """The planted relabelling of one word string."""
    return "".join(mapping.get(char, char) for char in word)


def _loci_texts(keys: list[tuple[str, int]], for_it: bool) -> list[list[str]]:
    """Words per shared locus for one file, parser words as parsed."""
    file = load("IT" if for_it else "ZL")
    index = index_loci(file)
    return [list(index[key].words) for key in keys if index[key].words]


def _plant_mapping() -> dict[str, str]:
    """Cyclic relabelling of the ten most frequent EVA characters of IT."""
    planted_counts: Counter[str] = Counter()
    for words in _loci_texts(used_keys(), for_it=True):
        for word in words:
            planted_counts.update(_word_glyphs(word))
    top = [char for char, _ in planted_counts.most_common(PLANT_TYPES)]
    return {
        original: top[(position + PLANT_SHIFT) % PLANT_TYPES]
        for position, original in enumerate(top)
    }


def _length_facts(counter: Counter) -> dict:
    """Token length distribution facts for one file."""
    tokens = sum(counter.values())
    longest = max(counter) if counter else 0
    shares = {
        str(length): round(counter[length] / tokens, 6)
        for length in range(1, min(longest, 12) + 1)
    }
    total_length = sum(length * count for length, count in counter.items())
    return {
        "mean_length": round(total_length / tokens, 6) if tokens else None,
        "share_length_over_12": round(
            sum(counter[length] for length in range(13, longest + 1)) / tokens, 6
        ) if tokens else None,
        "shares": shares,
    }


def transcript_stats() -> dict:
    """The family 1 measurement over the frozen corpus, with its controls."""
    keys = used_keys()
    real_a = _file_counts_generic(keys, "ZL", plant=None)
    real_b = _file_counts_generic(keys, "IT", plant=None)

    correlations = {
        _stat_key(order): _spearman(real_a["ngram"][order], real_b["ngram"][order])
        for order in _ORDERS
    }
    correlations[_WORDS_KEY] = _spearman(real_a["words"], real_b["words"])

    baseline: dict[str, dict] = {}
    for code in ("ZL", "IT"):
        half = _half_split(keys, code)
        baseline[code] = {
            _stat_key(order): _spearman(
                half["first"]["ngram"][order], half["second"]["ngram"][order]
            )
            for order in _ORDERS
        }
        baseline[code][_WORDS_KEY] = _spearman(
            half["first"]["words"], half["second"]["words"]
        )

    plant = _plant_mapping()
    planted_b = _file_counts_generic(keys, "IT", plant=plant)
    planted = {
        _stat_key(order): _spearman(real_a["ngram"][order], planted_b["ngram"][order])
        for order in _ORDERS
    }
    planted[_WORDS_KEY] = _spearman(real_a["words"], planted_b["words"])

    return {
        "reserved_folios": reserved_folios(),
        "used_loci": len(keys),
        "files": {
            code: {
                "glyphs": sum(real["ngram"][1].values()),
                "types": {
                    _stat_key(order): len(real["ngram"][order]) for order in _ORDERS
                },
                "tokens": real["tokens"],
                "word_types": len(real["words"]),
                "lengths": _length_facts(real["lengths"]),
            }
            for code, real in (("ZL", real_a), ("IT", real_b))
        },
        "shared_types": {
            _stat_key(order): correlations[_stat_key(order)][1]
            for order in _ORDERS
        } | {_WORDS_KEY: correlations[_WORDS_KEY][1]},
        "spearman": {name: value for name, (value, count) in correlations.items()},
        "controls": {
            "within_file_half_split_baseline": {
                code: {name: value for name, (value, count) in entries.items()}
                for code, entries in baseline.items()
            },
            "planted_relabel_of_it": {
                "mapping_size": len(plant),
                "spearman": {name: value for name, (value, count) in planted.items()},
            },
        },
    }


def _stat_key(order: int) -> str:
    return f"char{order}" if order == 1 else f"ngram{order}"


def _file_counts_generic(
    keys: list[tuple[str, int]], code: str, plant: dict[str, str] | None
) -> dict:
    """Aggregate declared counts for one file, optionally under the plant."""
    index = index_loci(load(code))
    total = _counts([])
    for key in keys:
        locus = index[key]
        if not locus.words:
            continue
        words = list(locus.words)
        if plant is not None:
            words = [_relabel(word, plant) for word in words]
        side = _counts(words)
        total["ngram"] = {
            order: total["ngram"][order] + side["ngram"][order] for order in _ORDERS
        }
        total["words"] += side["words"]
        total["lengths"] += side["lengths"]
        total["tokens"] += side["tokens"]
    return total


def _half_split(keys: list[tuple[str, int]], code: str) -> dict:
    """Within-file resampling baseline: alternate keys into two halves."""
    first = _file_counts_generic(keys[::2], code, plant=None)
    second = _file_counts_generic(keys[1::2], code, plant=None)
    return {"first": first, "second": second}


if __name__ == "__main__":
    report = transcript_stats()
    STATS_PATH.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print("wrote", STATS_PATH)
    print("reserved:", ", ".join(report["reserved_folios"]))
    print("used loci:", report["used_loci"])
    print("spearman:", {
        name: round(value, 4) for name, value in report["spearman"].items()
    })
    for code in ("ZL", "IT"):
        print(f"baseline {code}:", {
            name: round(value, 4) for name, value in
            report["controls"]["within_file_half_split_baseline"][code].items()
        })
    print("baseline ZL:", {
        name: round(value, 4) for name, value in
        report["controls"]["within_file_half_split_baseline"]["ZL"].items()
    })
    print("planted IT:", {
        name: round(value, 4) for name, value in
        report["controls"]["planted_relabel_of_it"]["spearman"].items()
    })
    print("token means:", {
        code: report["files"][code]["lengths"]["mean_length"] for code in ("ZL", "IT")
    })
