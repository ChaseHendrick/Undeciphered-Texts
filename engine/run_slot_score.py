"""Run-slot score: repeat length combined with start-slot bias.

The run-slot score is original to this repository. It is not a published
decipherment method and it does not decipher an ancient script. A high score
is a statistic of the sign strings you supplied. It is not a sound, a word,
or a reading of Linear A, the Voynich manuscript, Rongorongo, the Indus
script, the Phaistos disc, or any other undeciphered writing.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Sequence


# Quoted by the unit test so the claim stays on the tool itself.
ORIGINAL_TO_THIS_REPO = (
    "The run-slot score is original to this repository."
)
NOT_A_DECIPHERMENT = (
    "This does not decipher an ancient script. "
    "A high run-slot score is not a reading."
)


@dataclass(frozen=True)
class SignRun:
    """One maximal run of the same sign inside a single span."""

    sign: str
    length: int
    start: int


@dataclass(frozen=True)
class SignRunSlot:
    """Repeat length and start-slot bias for one sign, and their product score."""

    sign: str
    occurrences: int
    run_count: int
    repeat_length: int
    peak_start_slot: int
    peak_start_count: int
    peak_share: float
    slot_count: int
    position_bias: float
    run_slot_score: float


def maximal_runs(span: Sequence[str]) -> list[SignRun]:
    """Maximal consecutive runs inside one span.

    A run stops at a different sign or at the end of the span. The next span
    does not continue it. An empty span yields nothing.
    """
    runs: list[SignRun] = []
    index = 0
    width = len(span)
    while index < width:
        sign = span[index]
        end = index + 1
        while end < width and span[end] == sign:
            end += 1
        runs.append(SignRun(sign=sign, length=end - index, start=index))
        index = end
    return runs


def position_bias(peak_share: float, slot_count: int) -> float:
    """How far the favorite start slot sits above a uniform column.

    ``slot_count`` is the widest span in the corpus, so every sign is judged
    against the same grid. Bias is 0 when that grid has fewer than two columns,
    because a single column is not a preference. Otherwise

        (peak_share - 1/slot_count) / (1 - 1/slot_count)

    clipped to [0, 1]. A sign whose runs all start in one column scores 1.
    A sign whose starts are spread evenly across the grid scores 0.
    """
    if slot_count < 2:
        return 0.0
    baseline = 1.0 / slot_count
    if peak_share <= baseline:
        return 0.0
    raw = (peak_share - baseline) / (1.0 - baseline)
    if raw > 1.0:
        return 1.0
    return raw


def run_slot_score(repeat_length: int, bias: float) -> float:
    """Combine the two measurements.

    ``repeat_length * (1 + position_bias)``. Length and bias both raise the
    score. A long run locked to one start column outranks either a long run
    with no column preference or a single sign that happens to sit in one
    column. The formula is original to this repository.
    """
    if repeat_length < 0:
        raise ValueError("repeat_length must be >= 0")
    if bias < 0.0 or bias > 1.0:
        raise ValueError("position_bias must be in [0, 1]")
    return repeat_length * (1.0 + bias)


def _rank_runs(runs: Sequence[SignRun], slot_count: int) -> list[SignRunSlot]:
    if not runs:
        return []
    by_sign: dict[str, list[SignRun]] = defaultdict(list)
    for run in runs:
        by_sign[run.sign].append(run)
    ranked: list[SignRunSlot] = []
    for sign, group in by_sign.items():
        repeat_length = max(run.length for run in group)
        occurrences = sum(run.length for run in group)
        start_counts: dict[int, int] = defaultdict(int)
        for run in group:
            start_counts[run.start] += 1
        peak_start_slot, peak_start_count = min(
            start_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
        peak_share = peak_start_count / len(group)
        bias = position_bias(peak_share, slot_count)
        ranked.append(
            SignRunSlot(
                sign=sign,
                occurrences=occurrences,
                run_count=len(group),
                repeat_length=repeat_length,
                peak_start_slot=peak_start_slot,
                peak_start_count=peak_start_count,
                peak_share=peak_share,
                slot_count=slot_count,
                position_bias=bias,
                run_slot_score=run_slot_score(repeat_length, bias),
            )
        )
    ranked.sort(
        key=lambda row: (
            -row.run_slot_score,
            -row.repeat_length,
            -row.position_bias,
            row.sign,
        )
    )
    return ranked


def rank_run_slot(spans: Iterable[Sequence[str]]) -> list[SignRunSlot]:
    """Rank signs by the run-slot score.

    Each span is one line or one word. Runs do not cross a span boundary, and
    the start slot is the index inside that span. Signs that never occur are
    omitted. This does not assign values and does not decipher an ancient script.
    """
    runs: list[SignRun] = []
    slot_count = 0
    for span in spans:
        slot_count = max(slot_count, len(span))
        runs.extend(maximal_runs(span))
    return _rank_runs(runs, slot_count)


def rank_run_slot_stream(signs: Sequence[str]) -> list[SignRunSlot]:
    """Same ranking for one flat stream, treated as a single span."""
    return rank_run_slot([signs])
