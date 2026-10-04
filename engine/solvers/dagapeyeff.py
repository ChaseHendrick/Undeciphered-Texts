"""What the D'Agapeyeff solver is allowed to treat as progress. Not a reading.

The bound is recomputed from the cells. A frequency claim needs enough
count-moves for the chi-square ball to be able to clear English, and a
clear frequency ball is still not a reading.
"""

from __future__ import annotations

from engine.dagapeyeff_edits import edit_report
from engine.dagapeyeff_angles import angle_report
from engine.dagapeyeff_autokey import autokey_report
from engine.dagapeyeff_bifid import bifid_report
from engine.dagapeyeff_bookkey import bookkey_report
from engine.dagapeyeff_keys import key_report
from engine.dagapeyeff_model import model_report
from engine.dagapeyeff_patterns import pattern_report
from engine.dagapeyeff_places import place_report
from engine.dagapeyeff_period4 import period4_report
from engine.dagapeyeff_columns import column_report
from engine.dagapeyeff_delay import delay_report
from engine.dagapeyeff_digit_routes import digit_route_report
from engine.dagapeyeff_groups import group_report
from engine.dagapeyeff_regroup import regroup_report
from engine.dagapeyeff_running import running_report
from engine.dagapeyeff_solver_swarm import solver_swarm_report
from engine.dagapeyeff_classic_swarm import classic_swarm_report
from engine.dagapeyeff_word import word_report


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


def consider_word_score() -> dict:
    report = word_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] == 0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "word_score_allowed": allowed,
        "learned": (
            "Scoring all 390625 period-4 shifts by the word model reaches -3.2713. "
            "Prose is -2.5185. 4 of 8 shuffled ciphers do as well. Refuse it."
        ),
    }


def consider_running_key() -> dict:
    report = running_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] == 0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "running_key_allowed": allowed,
        "learned": (
            "94860 alignments of five texts were tried as a running key. "
            "The best is -3.4945, worse than the period-4 word search at -3.2713. "
            "Prose is -2.5185. 1 of 8 shuffles beats it. Refuse it."
        ),
    }


def consider_patterns() -> dict:
    report = pattern_report()
    tails = (
        report["printed_null"]["as_high"] * 100 < report["printed_null"]["draws"]
        or report["down_null"]["as_high"] * 100 < report["down_null"]["draws"]
        or report["regrouped_null"]["as_high"] * 100 < report["regrouped_null"]["draws"]
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pattern_allowed": tails,
        "learned": (
            "Of 940 windows, the printed cells match a dictionary shape in 423. "
            "92932 of 100000 shuffles do that well or better. "
            "The regrouping matches 499, and 31687 of 50000 shuffles do too. Refuse it."
        ),
    }


def consider_columns() -> dict:
    report = column_report()
    allowed = report["nulls_as_high"] == 0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "column_allowed": allowed,
        "learned": (
            "A width-27 downward read matches 544 dictionary windows, and the best of 25000 column orders matches 581. "
            "The printed order matches 423. 4 of 8 shuffled grids, given the same column search, reach 581. Refuse it."
        ),
    }


def consider_autokey() -> dict:
    report = autokey_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] == 0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "autokey_allowed": allowed,
        "learned": (
            "Four autokey rules, 25 starts each. The best is plain-sub at -3.7495. "
            "Prose is -2.5185. 37 of 40 shuffles do as well or better. Refuse it."
        ),
    }


def consider_digit_routes() -> dict:
    report = digit_route_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] == 0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "digit_routes_allowed": allowed,
        "learned": (
            "46 routes of the row digits and the column digits stay on the square. "
            "The best is rail-both-4 at -3.4242. Prose is -2.5185. "
            "29 of 40 shuffles of those digits do as well. Refuse it."
        ),
    }


def consider_angles() -> dict:
    report = angle_report()
    step_ok = report["reaches_prose"] and report["shuffles_as_high"] == 0
    holes_ok = report["placements_as_crowded"] * 20 < report["placements"]
    playfair_ok = report["shuffles_as_few_identical"] * 20 < report["digraph_draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "angles_allowed": step_ok and holes_ok and playfair_ok,
        "learned": (
            "The step from cell to cell scores -3.8542, and 23 of 40 shuffles do as well. "
            "Seven unused cells put 4 in one row, and 29450 of 480700 placements do that. "
            "10 of 98 digraphs repeat a cell, and 363 of 400 shuffles have as few repeats, so it is not Playfair. "
            "Refuse all three."
        ),
    }


def consider_delay() -> dict:
    report = delay_report()
    rare = report["delay_shuffles_as_high"] * 20 < report["delay_draws"]
    allowed = report["reaches_prose"] and rare and report["progressive_shuffles_as_high"] == 0
    return {
        "solved": False,
        "claimed_plaintext": None,
        "delay_allowed": allowed,
        "learned": (
            "Rotating the row digits against the column digits, the best delay is 79 and scores -3.2652. "
            "Prose is -2.5185. 3 of 200 shuffles do as well. "
            "A progressive shift scores -3.6491, and 4 of 200 shuffles do as well. Refuse both."
        ),
    }


def consider_bookkey() -> dict:
    report = bookkey_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] * 20 < report["null_texts"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bookkey_allowed": allowed,
        "learned": (
            "The book's solved exercise, slid or repeated as a key, scores -3.389. "
            "Prose is -2.5185. 61 of 100 shuffles do as well. Refuse it."
        ),
    }


def consider_groups() -> dict:
    report = group_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] * 20 < report["null_texts"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "groups_allowed": allowed,
        "learned": (
            "160 routes keep an even group in an even place. All 160 stay on the square. "
            "The best is rail-odd-6 at -3.3582. Prose is -2.5185. "
            "33 of 40 shuffles of those groups do as well. Refuse them."
        ),
    }


def consider_places() -> dict:
    report = place_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] * 20 < report["null_texts"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "places_allowed": allowed,
        "learned": (
            "Five digit places, each paired on its own, stay on the square. "
            "Place 4 scores -3.1598 on 39 cells. Prose is -2.5185. "
            "24 of 80 shuffles do as well. The shorter score is not a better reading. Refuse them."
        ),
    }


def consider_solver_swarm() -> dict:
    report = solver_swarm_report()
    caesar_ok = (
        report["caesar_per_letter"] >= report["caesar_prose_per_letter"]
        and report["caesar_shuffles_as_high"] * 20 < report["caesar_draws"]
    )
    vigenere_ok = (
        report["vigenere_per_letter"] >= report["vigenere_prose_per_letter"]
        and report["vigenere_shuffles_as_high"] * 20 < report["vigenere_draws"]
    )
    substitution_ok = (
        report["substitution_reading"] is True
        and report["substitution_shuffles_as_high"] * 20 < report["substitution_draws"]
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "solver_swarm_allowed": caesar_ok or vigenere_ok or substitution_ok,
        "learned": (
            "Caesar scores -3.4459 per letter, prose -2.9415, and 33 of 40 shuffles do as well. "
            "Vigenere, periods through 8, picks period 3 at -3.7393, prose -2.4363, and 7 of 20 shuffles do as well. "
            "Substitution at 400 steps scores -3.0858, its own reading flag is false, and 8 of 8 shuffles do as well. "
            "Refuse the swarm."
        ),
    }


def consider_classic_swarm() -> dict:
    report = classic_swarm_report()
    prose = report["prose_per_quadgram"]
    affine_ok = (
        report["affine_per_quadgram"] >= prose
        and report["affine_shuffles_as_high"] * 20 < report["affine_draws"]
    )
    beaufort_ok = (
        report["beaufort_per_quadgram"] >= prose
        and report["beaufort_shuffles_as_high"] * 20 < report["beaufort_draws"]
    )
    porta_ok = (
        report["porta_per_quadgram"] >= prose
        and report["porta_shuffles_as_high"] * 20 < report["porta_draws"]
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "classic_swarm_allowed": affine_ok or beaufort_ok or porta_ok,
        "learned": (
            "Affine's best multiplier is 1, a Caesar, at -3.7883. 16 of 20 shuffles do as well. "
            "Beaufort period 5 scores -3.7684. A sample of 20 was widened to 80, and 8 do as well. "
            "Porta period 4 scores -3.9175, and 11 of 20 shuffles do as well. "
            "Prose is -2.5185. Refuse the swarm."
        ),
    }
