"""What the D'Agapeyeff solver is allowed to treat as progress. Not a reading.

The bound is recomputed from the cells. A frequency claim needs enough
count-moves for the chi-square ball to be able to clear English, and a
clear frequency ball is still not a reading.
"""

from __future__ import annotations

from engine.dagapeyeff_edits import edit_report


def consider_frequency_claim(count_moves: int, chi_hi: float) -> dict:
    bound = edit_report()
    required = bound["moves_required"]
    line = bound["english_line"]
    enough_moves = count_moves >= required
    clears = chi_hi < line
    return {
        "solved": False,
        "claimed_plaintext": None,
        "moves_required": required,
        "english_line": line,
        "frequency_claim_allowed": enough_moves and clears,
        "learned": (
            "At least three count-moves are required before a frequency ball can clear English. "
            "Clearing it is not a reading."
        ),
    }
