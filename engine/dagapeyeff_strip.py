"""Remove the five symbols that never leave the last column. Not a reading.

If those eight cells were only filler, the other 188 would get closer to
prose. The comparison is same-length prose, a shuffle of what remains, and
other ways of deleting eight cells. No letter string is stored.
"""

from __future__ import annotations

import random
from collections import Counter

from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_private import private_columns
from engine.dagapeyeff_swarm import challenge_pairs
from engine.stats import successive_information

_SEED = 20261004
_KEPT_DRAWS = 10000
_DROP_DRAWS = 10000
_BUNDLE_DRAWS = 5000


def _without(pairs: list[str], banned: set[str]) -> list[str]:
    return [symbol for symbol in pairs if symbol not in banned]


def _bundle(counts: Counter[str], drawn: random.Random) -> set[str] | None:
    symbols = list(counts)
    drawn.shuffle(symbols)
    chosen = []
    mass = 0
    for symbol in symbols:
        if mass + counts[symbol] > 8:
            continue
        chosen.append(symbol)
        mass += counts[symbol]
        if mass == 8:
            return set(chosen)
    return None


def strip_report() -> dict:
    pairs = list(challenge_pairs())
    banned = {symbol for symbol, _column, _count in private_columns(pairs)}
    kept = _without(pairs, banned)
    observed = successive_information(kept)
    full = successive_information(pairs)
    english = successive_information(_prose("english.txt", len(kept)))
    german = successive_information(_prose("german_excerpt.txt", len(kept)))
    drawn = random.Random(_SEED)
    kept_as_high = 0
    for _ in range(_KEPT_DRAWS):
        shuffled = kept[:]
        drawn.shuffle(shuffled)
        if successive_information(shuffled) >= observed - 1e-15:
            kept_as_high += 1
    indexes = list(range(len(pairs)))
    drop_as_high = 0
    for _ in range(_DROP_DRAWS):
        gone = set(drawn.sample(indexes, 8))
        trial = [symbol for index, symbol in enumerate(pairs) if index not in gone]
        if successive_information(trial) >= observed - 1e-15:
            drop_as_high += 1
    counts = Counter(pairs)
    bundle_as_high = 0
    bundles = 0
    guard = 0
    while bundles < _BUNDLE_DRAWS and guard < _BUNDLE_DRAWS * 4:
        guard += 1
        chosen = _bundle(counts, drawn)
        if chosen is None:
            continue
        bundles += 1
        if successive_information(_without(pairs, chosen)) >= observed - 1e-15:
            bundle_as_high += 1
    if bundles != _BUNDLE_DRAWS:
        raise RuntimeError(f"only found {bundles} symbol bundles of mass 8")
    return {
        "solved": False,
        "claimed_plaintext": None,
        "removed": tuple(sorted(banned)),
        "kept": len(kept),
        "full_mi": round(full, 4),
        "kept_mi": round(observed, 4),
        "english_mi": round(english, 4),
        "german_mi": round(german, 4),
        "kept_as_high": kept_as_high,
        "kept_draws": _KEPT_DRAWS,
        "drop_as_high": drop_as_high,
        "drop_draws": _DROP_DRAWS,
        "bundle_as_high": bundle_as_high,
        "bundle_draws": bundles,
        "trials": _KEPT_DRAWS + _DROP_DRAWS + bundles,
        "scope": (
            "Taking the private symbols out is not a reading unless what remains "
            "beats same-length prose and beats deleting eight other cells. "
            "No letter string is stored."
        ),
    }
