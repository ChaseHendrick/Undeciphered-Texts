"""Whether the three cells that appear once form a block. Not a reading.

Those three were already named, and they already sit in column 14. The new
question is whether their rows are consecutive. The seats of all eight
low-side cells are not held fixed: every way to choose eight rows, and
every way to place the low-side cells on them, is counted. The pair and
the triple are given the same packing test. No letter string is stored.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import gcd

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

_WIDTH = 14
_NAMED = 13


def _reduced(numerator: int, denominator: int) -> tuple[int, int]:
    scale = gcd(numerator, denominator)
    return numerator // scale, denominator // scale


def _rows(pairs: list[str], symbols: set[str]) -> tuple[int, ...]:
    return tuple(index // _WIDTH for index, symbol in enumerate(pairs) if index % _WIDTH == _NAMED and symbol in symbols)


def _packing(seats: tuple[int, ...]) -> tuple[int, int]:
    """Assignments, out of 3360, in which the named three are a block, and in which any low-side class is."""
    seats_list = list(seats)
    triples = [
        (left, mid, right)
        for left, mid, right in combinations(range(len(seats_list)), 3)
        if seats_list[mid] == seats_list[left] + 1 and seats_list[right] == seats_list[mid] + 1
    ]
    pairs = [
        (left, right)
        for left, right in combinations(range(len(seats_list)), 2)
        if seats_list[right] == seats_list[left] + 1
    ]
    named = 60 * len(triples)
    pair_packed = 120 * len(pairs)
    triple_packed = named
    both_named_pair = 0
    both_pair_triple = 0
    for triple in triples:
        used = set(triple)
        for pair in pairs:
            if used.isdisjoint(pair):
                both_named_pair += 6
                both_pair_triple += 6
    both_named_triple = 0
    for index, first in enumerate(triples):
        for second in triples[index + 1:]:
            if set(first).isdisjoint(second):
                both_named_triple += 12
    all_three = 0
    for first in triples:
        first_seats = set(first)
        for second in triples:
            if first == second or not first_seats.isdisjoint(second):
                continue
            used = first_seats | set(second)
            for pair in pairs:
                if used.isdisjoint(pair):
                    all_three += 6
    union = named + pair_packed + triple_packed - both_named_pair - both_named_triple - both_pair_triple + all_three
    return named, union


@frozen("block")
def block_report() -> dict:
    pairs = list(challenge_pairs())
    counts = Counter(pairs)
    hapax = {symbol for symbol, count in counts.items() if count == 1}
    if len(hapax) != 3:
        raise ValueError("the named set is the three cells that appear once")
    rows = _rows(pairs, hapax)
    if len(rows) != 3:
        raise ValueError("the named three are expected in the named column")
    named_hit = 0
    union_hit = 0
    assignments = 0
    for subset in combinations(range(_WIDTH), 8):
        named, union = _packing(subset)
        named_hit += named
        union_hit += union
        assignments += 3360
    named_fraction = _reduced(named_hit, assignments)
    union_fraction = _reduced(union_hit, assignments)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "rows": list(rows),
        "consecutive": rows[2] - rows[0] == 2 and rows[1] == rows[0] + 1,
        "named_numerator": named_fraction[0],
        "named_denominator": named_fraction[1],
        "union_numerator": union_fraction[0],
        "union_denominator": union_fraction[1],
        "scope": (
            "Three consecutive rows are not a reading. "
            "A class chosen from a menu of three is not a rarer class. "
            "No letter string is stored."
        ),
    }
