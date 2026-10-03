"""Pattern-and-mood reader for a sign stream or a simple drawn sheet.

Reports visual structure only: repeat rhythm, mirror symmetry, spacing, and a
mood label computed from those measurements. It does not transliterate, decrypt,
or emit linguistic plaintext. It is not a decipherment of the Voynich manuscript,
rongorongo, or any other unsolved text.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from typing import Sequence

DISCLAIMER = (
    "Describes art and pattern only. Not a decipherment of the Voynich manuscript, "
    "rongorongo, or any unsolved text. No linguistic plaintext is produced."
)

# Mood is a function of measurements, not of any symbol inventory.
RHYTHM_DENSE = 0.75
SPACING_TIGHT = 2.5
SPACING_OPEN = 8.0
SYMMETRY_OPEN = 0.25

# Gaps in a sign stream. Every other token is a mark, never a letter reading.
STREAM_GAPS = frozenset({"", " ", ".", "_", "-"})
SHEET_MARKS = frozenset({"#", "*", "1", "X", "x"})


@dataclass(frozen=True)
class MoodReport:
    """Visual measurements and a mood label. No plaintext field exists."""

    width: int
    height: int
    mark_count: int
    repeat_rhythm: float
    symmetry: float
    spacing: float
    density: float
    mood: str
    disclaimer: str


def mood_from_measures(repeat_rhythm: float, symmetry: float, spacing: float) -> str:
    """Label mood from rhythm, symmetry, and spacing alone.

    dense/rhythmic: a short, strong repeat and tight neighbor gaps.
    open: wide gaps and weak mirror symmetry.
    mixed: anything else.
    """
    if repeat_rhythm >= RHYTHM_DENSE and spacing <= SPACING_TIGHT:
        return "dense/rhythmic"
    if spacing >= SPACING_OPEN and symmetry <= SYMMETRY_OPEN:
        return "open"
    return "mixed"


def _is_sheet_mark(cell: object) -> bool:
    if isinstance(cell, bool):
        return cell
    if isinstance(cell, (int, float)):
        return cell != 0
    if isinstance(cell, str):
        return cell in SHEET_MARKS
    return False


def make_tight_repeating_sheet(width: int = 36, height: int = 18) -> list[list[int]]:
    """Even lattice: a mark every two cells in both axes. Tight and periodic."""
    if width < 4 or height < 4:
        raise ValueError("tight sheet needs at least 4x4")
    return [
        [1 if (x % 2 == 0 and y % 2 == 0) else 0 for x in range(width)]
        for y in range(height)
    ]


def make_sparse_asymmetric_sheet(width: int = 48, height: int = 36) -> list[list[int]]:
    """A few marks, far apart, with no mirror partner. Wide and unbalanced."""
    if width < 48 or height < 36:
        raise ValueError("sparse sheet needs at least 48x36")
    grid = [[0 for _ in range(width)] for _ in range(height)]
    for x, y in ((2, 3), (20, 8), (40, 30), (15, 28)):
        grid[y][x] = 1
    return grid


def repeat_rhythm(marks: Sequence[tuple[int, int]], width: int, height: int) -> float:
    """Best fraction of marks that reappear one period to the right or below.

    Agreement of empty cells is ignored, so a mostly blank sheet is not rhythmic
    just because the background matches itself.
    """
    found = set(marks)
    if len(found) < 2 or width < 1 or height < 1:
        return 0.0
    best = 0.0
    for lag in range(1, max(1, width // 2) + 1):
        possible = 0
        paired = 0
        for x, y in found:
            if x + lag < width:
                possible += 1
                if (x + lag, y) in found:
                    paired += 1
        if possible:
            best = max(best, paired / possible)
    for lag in range(1, max(1, height // 2) + 1):
        possible = 0
        paired = 0
        for x, y in found:
            if y + lag < height:
                possible += 1
                if (x, y + lag) in found:
                    paired += 1
        if possible:
            best = max(best, paired / possible)
    return best


def token_repeat_rhythm(signs: Sequence[str]) -> float:
    """Best lag match among tokens, ignoring pairs that are both gaps."""
    n = len(signs)
    if n < 2:
        return 0.0
    best = 0.0
    for lag in range(1, n // 2 + 1):
        matches = 0
        comparable = 0
        for i in range(n - lag):
            left = signs[i]
            right = signs[i + lag]
            if left in STREAM_GAPS and right in STREAM_GAPS:
                continue
            comparable += 1
            if left == right and left not in STREAM_GAPS:
                matches += 1
        if comparable:
            best = max(best, matches / comparable)
    return best


def mirror_symmetry(marks: Sequence[tuple[int, int]], width: int, height: int) -> float:
    """Fraction of marks that also sit on the left-right or top-bottom mirror.

    The score is the stronger of the two axes. A mark on the midline counts as
    its own partner.
    """
    found = set(marks)
    count = len(found)
    if count == 0 or width < 1 or height < 1:
        return 0.0
    left_right = sum(1 for x, y in found if (width - 1 - x, y) in found) / count
    top_bottom = sum(1 for x, y in found if (x, height - 1 - y) in found) / count
    return max(left_right, top_bottom)


def mean_nearest_spacing(marks: Sequence[tuple[int, int]]) -> float:
    """Mean Euclidean distance from each mark to its nearest other mark."""
    pts = list(set(marks))
    if len(pts) < 2:
        return math.inf
    total = 0.0
    for i, (x, y) in enumerate(pts):
        nearest = min(
            math.hypot(x - x2, y - y2)
            for j, (x2, y2) in enumerate(pts)
            if j != i
        )
        total += nearest
    return total / len(pts)


def _report(
    marks: Sequence[tuple[int, int]],
    width: int,
    height: int,
    *,
    extra_rhythm: float = 0.0,
) -> MoodReport:
    found = list(set(marks))
    area = width * height
    if area <= 0:
        raise ValueError("width and height must be positive")
    rhythm = max(repeat_rhythm(found, width, height), extra_rhythm)
    symmetry = mirror_symmetry(found, width, height)
    spacing = mean_nearest_spacing(found)
    density = len(found) / area
    if not found:
        mood = "empty"
    else:
        mood = mood_from_measures(rhythm, symmetry, spacing)
    return MoodReport(
        width=width,
        height=height,
        mark_count=len(found),
        repeat_rhythm=rhythm,
        symmetry=symmetry,
        spacing=spacing,
        density=density,
        mood=mood,
        disclaimer=DISCLAIMER,
    )


def analyze_sheet(grid: Sequence[Sequence[object]]) -> MoodReport:
    """Read a drawn sheet. Nonzero cells and # * X 1 are marks. Nothing is read as text."""
    if not grid:
        raise ValueError("sheet has no rows")
    height = len(grid)
    width = len(grid[0])
    if width == 0:
        raise ValueError("sheet has no columns")
    for row in grid:
        if len(row) != width:
            raise ValueError("sheet rows must be the same width")
    marks = [
        (x, y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if _is_sheet_mark(cell)
    ]
    return _report(marks, width, height)


def analyze_sign_stream(signs: Sequence[str]) -> MoodReport:
    """Read a sign stream left to right.

    Gap tokens (space, dot, underscore, hyphen) are empty cells. Every other
    token is only a mark. The original tokens are not returned.
    """
    if not signs:
        raise ValueError("sign stream is empty")
    marks = [(i, 0) for i, token in enumerate(signs) if token not in STREAM_GAPS]
    return _report(marks, len(signs), 1, extra_rhythm=token_repeat_rhythm(signs))


def report_to_dict(report: MoodReport) -> dict:
    payload = asdict(report)
    if not math.isfinite(payload["spacing"]):
        payload["spacing"] = None
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m engine.pattern_mood",
        description=(
            "Report repeat rhythm, symmetry, spacing, and a mood label for a "
            "synthetic sheet or sign stream. Does not decipher Voynich, rongorongo, "
            "or any unsolved text, and does not emit linguistic plaintext."
        ),
    )
    parser.add_argument(
        "--tight",
        action="store_true",
        help="score the built-in tight repeating lattice",
    )
    parser.add_argument(
        "--sparse",
        action="store_true",
        help="score the built-in sparse asymmetric sheet",
    )
    parser.add_argument(
        "--signs",
        help="sign stream; spaces, dots, underscores, and hyphens are gaps",
    )
    args = parser.parse_args(argv)

    chosen = sum(bool(x) for x in (args.tight, args.sparse, args.signs is not None))
    if chosen != 1:
        parser.error("pass exactly one of --tight, --sparse, or --signs")

    if args.tight:
        report = analyze_sheet(make_tight_repeating_sheet())
    elif args.sparse:
        report = analyze_sheet(make_sparse_asymmetric_sheet())
    else:
        report = analyze_sign_stream(list(args.signs))

    print(json.dumps(report_to_dict(report), indent=2))
    print(report.disclaimer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
