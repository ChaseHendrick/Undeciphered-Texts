"""How far the cells are from a published score and from English. Not a reading.

Tim Marland's sa_trans_k7 figure of 49.23 and his two-square score of -692 are
his published numbers, not a measurement made here. -692 is a different scale
and is not converted. Lower chi-square is closer to the English counts.
No letter string is stored.
"""

from __future__ import annotations

from engine.dagapeyeff_more import group_reorders
from engine.dagapeyeff_swarm import best_chi_square, challenge_pairs, english_calibration
from engine.dagapeyeff_yardstick import yardstick_report

# Findings, D'Agapeyeff Research, Tim Marland, 2026. Not recomputed here.
_PUBLISHED_CHI = 49.23


def record_report() -> dict:
    pairs = challenge_pairs()
    chi = round(best_chi_square(pairs), 2)
    english = english_calibration()
    groups = group_reorders()
    yard = yardstick_report()
    legal = groups["best_legal_chi"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "our_chi": chi,
        "published_chi": _PUBLISHED_CHI,
        "ahead_of_published_chi": round(_PUBLISHED_CHI - chi, 2),
        "english_worst_chi": english["chi_max"],
        "english_median_chi": english["chi_median"],
        "above_worst_english": round(chi - english["chi_max"], 2),
        "above_median_english": round(chi - english["chi_median"], 2),
        "flatter_than_challenge": english["flatter_than_challenge"],
        "legal_reorder": groups["best_reorder"],
        "legal_reorder_chi": legal,
        "legal_reorder_above_median": round(legal - english["chi_median"], 2),
        "cipher_mi": yard["cipher_mi"],
        "english_mi": yard["english_mi"],
        "order_gap": round(yard["english_mi"] - yard["cipher_mi"], 4),
        "order_gap_closed": 0,
        "scope": (
            "Beating a published chi-square is not a reading when the cells themselves "
            "already beat it. The order gap is unclosed because a shuffle is already "
            "more predictable than the printed order. No letter string is stored."
        ),
    }
