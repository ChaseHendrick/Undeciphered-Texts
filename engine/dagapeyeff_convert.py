"""The published record, as balls, and one step past it. Not a reading.

Chi-square 49.23 and index 0.0697 are rounded, so each is a center and a
radius of half a unit in the last place. The two-square score -692.13 has
no published formula, so its ball is not compared to anything here. The
letter rates are the published five-decimal figures, each with the same
rounding radius. No letter string is stored.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

from engine.dagapeyeff_balls import Ball, information_ball
from engine.dagapeyeff_order import _prose
from engine.dagapeyeff_swarm import challenge_pairs
from engine.language import UNIGRAM

_PLACE_5 = Fraction(1, 100000)
_RATE_RADIUS = _PLACE_5 / 2
_CHI_RADIUS = Fraction(1, 200)  # half of 0.01, for a figure rounded to two decimals
_IOC_RADIUS = Fraction(1, 20000)  # half of 0.0001
_PUBLISHED_CHI = Ball(Fraction("49.23"), _CHI_RADIUS)
_PUBLISHED_IOC = Ball(Fraction("0.0697"), _IOC_RADIUS)
_ENGLISH_WORST = Ball(Fraction("24.17"), _CHI_RADIUS)
_QUADGRAM_SCORE = Ball(Fraction("-692.13"), Fraction(1, 200))
_REPAIR_INDEX = 97


def _rate_balls() -> list[Ball]:
    centers = [format(rate, ".5f") for rate in UNIGRAM]
    if len(centers) != 26:
        raise RuntimeError("the published table is 26 letters")
    balls = [Ball(Fraction(center), _RATE_RADIUS) for center in centers]
    merged = []
    for index, ball in enumerate(balls):
        if index == 9:
            continue
        if index == 8:
            merged.append(ball + balls[9])
        else:
            merged.append(ball)
    total = Ball(Fraction(0), Fraction(0))
    for ball in merged:
        total += ball
    scaled = [ball / total for ball in merged]
    scaled.sort(key=lambda ball: ball.mid, reverse=True)
    for left, right in zip(scaled, scaled[1:]):
        if left.lo() <= right.hi():
            raise RuntimeError("two letter-rate balls meet, so the sort is not forced")
    return scaled


def chi_ball(symbols: list[str], rates: list[Ball]) -> Ball:
    counts = sorted(Counter(symbols).values(), reverse=True)
    counts += [0] * (len(rates) - len(counts))
    total = Fraction(len(symbols))
    score = Ball(Fraction(0), Fraction(0))
    for count, rate in zip(counts, rates):
        expected = rate.scale(total)
        gap = Ball(Fraction(count), Fraction(0)) - expected
        score += (gap * gap) / expected
    return score


def _ioc(symbols: list[str]) -> Fraction:
    count = len(symbols)
    tally = Counter(symbols)
    return Fraction(sum(seen * (seen - 1) for seen in tally.values()), count * (count - 1))


def _show(ball: Ball) -> dict:
    return {"lo": float(ball.lo()), "hi": float(ball.hi()), "rad": float(ball.rad)}


def convert_report() -> dict:
    pairs = list(challenge_pairs())
    if pairs[_REPAIR_INDEX] != "04":
        raise RuntimeError("the published repair is the cell 04")
    rates = _rate_balls()
    observed = chi_ball(pairs, rates)
    cells = "67890"
    digits = "12345"
    square = [row + column for row in cells for column in digits]
    repairs = []
    for symbol in square:
        if symbol == "04":
            continue
        trial = pairs[:]
        trial[_REPAIR_INDEX] = symbol
        repairs.append(chi_ball(trial, rates))
    tied = 0
    worse = 0
    better = 0
    for trial in repairs:
        if trial.lo() == observed.lo() and trial.hi() == observed.hi():
            tied += 1
        elif trial.lo() > observed.hi():
            worse += 1
        elif trial.hi() < observed.lo():
            better += 1
    suggested = pairs[:]
    suggested[_REPAIR_INDEX] = "75"
    suggested_chi = chi_ball(suggested, rates)
    suggested_mi = information_ball(suggested)
    english_mi = information_ball(list(_prose("english.txt", len(pairs))))
    index = _ioc(pairs)
    below_record = observed.hi() < _PUBLISHED_CHI.lo()
    above_english = observed.lo() > _ENGLISH_WORST.hi()
    repair_reaches = any(trial.hi() < _ENGLISH_WORST.lo() for trial in repairs)
    suggested_reaches = suggested_chi.hi() < _ENGLISH_WORST.lo()
    order_reaches = suggested_mi.hi() < english_mi.lo()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "published_chi": _show(_PUBLISHED_CHI),
        "published_ioc": _show(_PUBLISHED_IOC),
        "quadgram_score": _show(_QUADGRAM_SCORE),
        "quadgram_comparable": False,
        "our_chi": _show(observed),
        "english_worst": _show(_ENGLISH_WORST),
        "below_published_chi": below_record,
        "above_worst_english": above_english,
        "our_ioc": float(index),
        "ioc_inside_published": _PUBLISHED_IOC.lo() <= index <= _PUBLISHED_IOC.hi(),
        "repair_index": _REPAIR_INDEX,
        "repair_from": "04",
        "repairs": len(repairs),
        "repairs_tied": tied,
        "repairs_worse": worse,
        "repairs_better": better,
        "any_repair_reaches_english": repair_reaches,
        "suggested_repair": "75",
        "suggested_chi": _show(suggested_chi),
        "suggested_worse": suggested_chi.lo() > observed.hi(),
        "suggested_reaches_english": suggested_reaches,
        "suggested_mi": _show(suggested_mi),
        "english_mi": _show(english_mi),
        "suggested_order_still_below_english": order_reaches,
        "scope": (
            "A published chi-square can be a ball. A score with no formula cannot be compared. "
            "Changing the one anomalous cell is not a reading unless the chi ball and the order ball both clear English. "
            "No letter string is stored."
        ),
    }
