"""What the D'Agapeyeff solver is allowed to treat as progress. Not a reading.

The bound is recomputed from the cells. A frequency claim needs enough
count-moves for the chi-square ball to be able to clear English, and a
clear frequency ball is still not a reading.
"""

from __future__ import annotations

from engine.dagapeyeff_edits import edit_report
from engine.dagapeyeff_bifid import bifid_report
from engine.dagapeyeff_keys import key_report
from engine.dagapeyeff_model import model_report
from engine.dagapeyeff_period4 import period4_report
from engine.dagapeyeff_regroup import regroup_report


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


def consider_regrouping() -> dict:
    report = regroup_report()
    allowed = (
        report["frequency_clears_english_worst"]
        and not report["order_still_below_english"]
        and report["down_shuffles_as_high"] * 20 < report["draws"]
        and report["control_flipped_chi"] <= report["control_printed_chi"]
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "reorder": report["reorder"],
        "regrouping_allowed": allowed,
        "learned": (
            "Regrouping 01432 clears the frequency line and the order stays under English. "
            "A shuffle of the same cells matches the downward read. "
            "The book's solved example gets worse. Refuse the regrouping."
        ),
    }


def consider_column_key() -> dict:
    report = key_report()
    allowed = report["key_reaches_english"] and report["repeats_as_high"] == 0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "column_key_allowed": allowed,
        "learned": (
            "The best of 20000 column orders of regrouping 01432 scores 1.0033. "
            "13 of 20 shuffle samples of the same size reach it. English is 1.0658. Refuse the key."
        ),
    }


def consider_language_model() -> dict:
    report = model_report()
    allowed = report["either_reaches_english"] and report["regrouped_tail"]["quad_as_high"] * 20 < report["regrouped_tail"]["draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "language_model_allowed": allowed,
        "learned": (
            "Under the frequency labeling, regrouping 01432 scores -3.6352 per quadgram "
            "and the printed cells score -3.6316. English scores -1.553. "
            "151728 of 200000 shuffles beat the regrouping. The lower chi-square did not help. Refuse it."
        ),
    }


def consider_bifid() -> dict:
    report = bifid_report()
    allowed = report["reaches_english"] and report["shuffles_as_high"] * 20 < report["draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bifid_allowed": allowed,
        "learned": (
            "The best bifid period is 174 and scores -3.4727 per quadgram. "
            "English is -1.553. 1109 of 2000 shuffles have a best period at least that high. Refuse it."
        ),
    }


def consider_period4() -> dict:
    report = period4_report()
    allowed = report["reaches_prose"] and report["quad_as_high"] * 20 < report["null_texts"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "period4_allowed": allowed,
        "learned": (
            "All 390625 period-4 shifts were scored. The friendliest counts are 3.86, "
            "and 32 of 40 shuffles do that well. The quadgram is -3.4759 against prose at -2.5185. "
            "3 of 40 shuffles match it. Refuse it."
        ),
    }
