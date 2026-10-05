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
from engine.bob_branch import bob_branch_report
from engine.bob_caution import bob_caution_report
from engine.dagapeyeff_bookkey import bookkey_report
from engine.dagapeyeff_keys import key_report
from engine.dagapeyeff_keystream import keystream_report
from engine.dagapeyeff_large_swarm import large_swarm_report
from engine.dagapeyeff_model import model_report
from engine.dagapeyeff_patterns import pattern_report
from engine.dagapeyeff_places import place_report
from engine.dagapeyeff_period4 import period4_report
from engine.dagapeyeff_placed import placed_report
from engine.dagapeyeff_columns import column_report
from engine.dagapeyeff_column_null import column_null_report
from engine.dagapeyeff_delay import delay_report
from engine.dagapeyeff_depth3 import depth3_report
from engine.dagapeyeff_depth4 import depth4_report
from engine.dagapeyeff_digit_routes import digit_route_report
from engine.dagapeyeff_groups import group_report
from engine.dagapeyeff_regroup import regroup_report
from engine.dagapeyeff_repair import repair_report
from engine.dagapeyeff_refined import refined_report
from engine.dagapeyeff_router_swarm import router_swarm_report
from engine.dagapeyeff_running import running_report
from engine.dagapeyeff_solver_swarm import solver_swarm_report
from engine.dagapeyeff_classic_swarm import classic_swarm_report
from engine.dagapeyeff_clump import clump_report
from engine.dagapeyeff_widths import widths_report
from engine.dagapeyeff_hole import hole_report
from engine.dagapeyeff_clerical import clerical_report
from engine.dagapeyeff_intro import intro_report
from engine.dagapeyeff_block import block_report
from engine.dagapeyeff_digraph import digraph_report
from engine.dagapeyeff_trigram import trigram_report
from engine.dagapeyeff_monotone import monotone_report
from engine.dagapeyeff_straight import straight_report
from engine.dagapeyeff_diagonal import diagonal_report
from engine.dagapeyeff_word import word_report


def consider_frequency_claim(count_moves: int, chi_hi: float) -> dict:
    bound = edit_report()
    third = depth3_report()
    required = 4 if not third["clears"] else bound["moves_required"]
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
            "Every reachable three-move change was scored, 2,321,645 of them. "
            "The best chi-square is 24.8811. Its ball runs from 24.83087 to 24.931425, "
            "entirely above the English line at 24.165. Four moves are required. "
            "Clearing the line is not a reading."
        ),
    }


def consider_depth3() -> dict:
    report = depth3_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "depth3_allowed": report["clears"],
        "learned": (
            "2,321,645 three-move changes were scored. The best is 24.8811, "
            "and the ball stays above 24.165. Three moves cannot counterfeit English counts. Refuse them."
        ),
    }


def consider_depth4() -> dict:
    report = depth4_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "depth4_allowed": False,
        "learned": (
            "140 three-move states tie for the best score. Every fourth move from them was scored, "
            "52,003 states. The best chi-square is 22.4243. Its ball, 22.377631 to 22.471061, "
            "does clear 24.165. 18,760 of the states have a point score under that line. "
            "The edited positions were not kept. A matching count is not a reading. Refuse it."
        ),
    }


def consider_placed() -> dict:
    report = placed_report()
    allowed = report["reaches_prose"] and report["shuffles_as_high"] * 20 < report["draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "placed_allowed": allowed,
        "learned": (
            "70 count vectors tie for the best four-move score. "
            "Placing every one of them on the printed cells is 2,494,800 edits. "
            "The best order scores -3.4263. Prose is -2.5185. "
            "11 of 20 shuffled orders, given the same edits, do as well. Refuse it."
        ),
    }


def consider_repair() -> dict:
    report = repair_report()
    rare = report["neighbor_shuffles_as_high"] * 20 < report["neighbor_draws"]
    allowed = report["reaches_prose"] and rare
    return {
        "solved": False,
        "claimed_plaintext": None,
        "repair_allowed": allowed,
        "learned": (
            "70 best count vectors each touch 6 symbols. The union is 10 and they share one, "
            "the symbol 72, which every vector reduces. Losses come from 3 symbols. "
            "Four neighbor edits score -3.1449, and 6 of 80 shuffles do as well. "
            "Prose is -2.5185. The shared loss is not a reading. Refuse it."
        ),
    }


def consider_clump() -> dict:
    report = clump_report()
    allowed = report["every_window_shuffles_as_high"] * 20 < report["draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "clump_allowed": allowed,
        "learned": (
            "Six of the nine 72 pairs sit in the last four rows. "
            "That one window is 35 of 2000 shuffles, and it was chosen after looking. "
            "Every window of that height is 268 of 2000. Refuse the clump."
        ),
    }


def consider_widths() -> dict:
    report = widths_report()
    rare = report["re_pairings_as_flat"] * 20 < report["draws"]
    helped = report["control_width_3_chi"] <= report["control_printed_chi"]
    allowed = rare and helped
    return {
        "solved": False,
        "claimed_plaintext": None,
        "widths_allowed": allowed,
        "learned": (
            "Of 392 column widths, only 1, 3, 131, and 392 keep every pair on the square. "
            "Width 131 scores 10.63, and 1227 of 2000 random re-pairings are at least that flat. "
            "On the solved exercise, width 3 moves the score from 4.14 to 29.56 and width 131 moves it to 42.13. "
            "Refuse the widths."
        ),
    }


def consider_hole() -> dict:
    report = hole_report()
    step = report["step_numerator"] / report["step_denominator"]
    period = report["period7_as_high"] / report["period7_draws"]
    allowed = step < 0.05 and period < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "hole_allowed": allowed,
        "learned": (
            f"The occupied counts jump by {report['gap']} between {report['low_max']} and {report['high_min']}, "
            f"the unique largest gap. All {report['low_cells']} cells on the low side sit in column 14. "
            f"Five of them were already recorded. The new {report['new_cells']} cells, given those five, "
            f"sit there in {report['step_numerator']} of {report['step_denominator']} placements. "
            f"The {report['high_cells']} cells of count {report['high_min']} do not follow: "
            f"{report['high_in_named_column']} sit in that column. "
            f"The period-7 pair rate is {report['period7_as_high']} of {report['period7_draws']} shuffles. "
            "The new cells clear 5 percent. The period does not. Neither is a reading."
        ),
    }


def consider_clerical() -> dict:
    report = clerical_report()
    line_rate = report["line_as_high"] / report["line_draws"]
    allowed = line_rate < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "clerical_allowed": allowed,
        "learned": (
            f"Seven check-digit rules were fixed first. The best single rule hits "
            f"{report['first_digit_hits']} groups, and {report['first_digit_as_high']} of "
            f"{report['check_draws']} shuffles do as well. The best of the seven, "
            f"chosen again on every shuffle, is {report['family_as_high']} of {report['check_draws']}. "
            f"One symbol sits in one column {report['column_mode']} times, "
            f"and {report['column_as_high']} of {report['line_draws']} shuffles do that. "
            f"A row reaches {report['row_mode']}, and the taller of the row and the column is "
            f"{report['line_as_high']} of {report['line_draws']}. "
            "The column alone is under 5 percent. The line is not. Refuse the line."
        ),
    }


def consider_intro() -> dict:
    report = intro_report()
    rate = report["as_short"] / report["draws"]
    given_hole = report["hole_as_short"] / report["draws"]
    allowed = rate < 0.05 and given_hole < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "intro_allowed": allowed,
        "learned": (
            f"The longest wait for a new cell is {report['longest_wait']}. "
            f"{report['as_short']} of {report['draws']} shuffles wait that little or less. "
            f"Given that every cell of count at most {report['low_max']} sits in one column, "
            f"{report['hole_as_short']} of {report['draws']} still do. "
            f"The solved exercise waits {report['control_longest_wait']}, "
            f"and {report['control_as_short']} of {report['draws']} of its shuffles do as well. "
            "The wait clears 5 percent, and the exercise does too. Not a reading."
        ),
    }


def consider_block() -> dict:
    report = block_report()
    named = report["named_numerator"] / report["named_denominator"]
    union = report["union_numerator"] / report["union_denominator"]
    allowed = named < 0.05 and union < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "block_allowed": allowed,
        "learned": (
            f"The three cells that appear once sit in rows {report['rows'][0] + 1}, "
            f"{report['rows'][1] + 1}, and {report['rows'][2] + 1} of the named column, consecutively. "
            f"Given the eight low-side cells are in that column, "
            f"{report['named_numerator']} of {report['named_denominator']} seatings do that. "
            f"If the pair or the triple may be the packed class instead, "
            f"{report['union_numerator']} of {report['union_denominator']} arrangements pack some class. "
            "The named three clear 5 percent. The menu does not. Not a reading."
        ),
    }


def consider_digraph() -> dict:
    report = digraph_report()
    repeated = report["control_repeated_as_high"] / report["draws"]
    either = report["control_either_as_high"] / report["draws"]
    allowed = repeated < 0.05 and either < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "digraph_allowed": allowed,
        "learned": (
            f"The solved exercise has {report['control_repeated_digraphs']} digraphs that occur more than once. "
            f"{report['control_repeated_as_high']} of {report['draws']} shuffles have that many. "
            f"Its most common digraph occurs {report['control_peak']} times, "
            f"and {report['control_peak_as_high']} of {report['draws']} match that. "
            f"Either measure is {report['control_either_as_high']} of {report['draws']}. "
            f"The challenge has {report['repeated_digraphs']} repeated digraphs, "
            f"and {report['repeated_as_high']} of {report['draws']} shuffles do as well. "
            "The variety clears 5 percent. The two measures together do not. Not a reading."
        ),
    }


def consider_trigram() -> dict:
    report = trigram_report()
    rate = report["control_trigrams_as_high"] / report["draws"]
    corrected = report["lengths_scored"] * rate
    challenge = report["trigrams_as_high"] / report["draws"]
    allowed = rate < 0.05 and corrected < 0.05 and challenge > 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "trigram_allowed": allowed,
        "learned": (
            f"The solved exercise has {report['control_repeated_trigrams']} three-cell sequences that repeat. "
            f"{report['control_trigrams_as_high']} of {report['draws']} shuffles have that many. "
            f"Four cells in a row were scored as well. None repeat, "
            f"and {report['control_tetragrams_as_few']} of {report['draws']} shuffles also have none. "
            f"Two lengths were scored, and twice the three-cell rate is still under 5 percent. "
            f"The challenge has {report['repeated_trigrams']} repeated three-cell sequences, "
            f"and {report['trigrams_as_high']} of {report['draws']} shuffles do as well. "
            "The exercise clears the bar. The challenge does not share it. Not a reading."
        ),
    }


def consider_monotone() -> dict:
    report = monotone_report()
    rows = report["rows_with_one"] / report["draws"]
    either = report["either_with_one"] / report["draws"]
    allowed = rows < 0.05 and either < 0.05
    counts = ", ".join(str(count) for count in report["strict_row"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "monotone_allowed": allowed,
        "learned": (
            f"One row of the square has counts {counts}, and each step changes in the same direction. "
            f"{report['rows_with_one']} of {report['draws']} re-pairings have a row like that. "
            f"No column does. If a row or a column may be the line, "
            f"{report['either_with_one']} of {report['draws']} re-pairings have one. "
            "The row clears 5 percent. The two directions together do not. Not a reading."
        ),
    }


def consider_straight() -> dict:
    report = straight_report()
    either = report["either_as_long"] / report["draws"]
    allowed = either < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "straight_allowed": allowed,
        "learned": (
            f"Four successive counts in the row {report['strict_row']} differ by one. "
            f"{report['rows_as_long']} of {report['draws']} re-pairings have a straight at least that long. "
            f"Columns were scored the same way. {report['columns_as_long']} of {report['draws']} reach it, "
            f"so both directions together are {report['either_as_long']} of {report['draws']}. "
            f"The solved exercise has a straight of length {report['control_row_length']}, "
            f"and {report['control_rows_as_long']} of {report['draws']} of its re-pairings do too. "
            "The challenge clears 5 percent. The exercise does not. Not a reading."
        ),
    }


def consider_diagonal() -> dict:
    report = diagonal_report()
    either = report["either_zeros_as_many"] / report["draws"]
    allowed = either < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "diagonal_allowed": allowed,
        "learned": (
            f"The main diagonal has {report['main_zeros']} empty cells and the other diagonal has {report['anti_zeros']}. "
            f"{report['either_zeros_as_many']} of {report['draws']} re-pairings have a diagonal with at least that many. "
            f"The sum of the main diagonal is {report['main_sum']}. "
            f"If the other diagonal's sum counts as well, {report['sum_either']} of {report['draws']} match, "
            "which is not under 5 percent. "
            f"The solved exercise has {report['control_main_zeros']} and {report['control_anti_zeros']} empty cells, "
            f"and {report['control_either_zeros_as_many']} of {report['draws']} of its re-pairings do. "
            "The empty cells clear 5 percent. The sums do not. Not a reading."
        ),
    }


def consider_branch() -> dict:
    report = bob_branch_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "branch_allowed": False,
        "learned": (
            "Bob's residual branch is in use. On the cells the three shares are "
            "0.5012, 0.5271, and 0.5178. On a Caesar of known prose they are "
            "0.4566, 0.4709, and 0.4835. The shipped weights are the promoted warm start. "
            "A live branch is not a reading."
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


def consider_router_swarm() -> dict:
    report = router_swarm_report()
    column_unusual = report["column_shuffles_as_high"] * 20 < report["grid_draws"]
    family_unusual = report["shuffles_as_confident"] * 20 < report["router_draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "router_swarm_allowed": False,
        "column_unusual": column_unusual,
        "family_unusual": family_unusual,
        "learned": (
            "The router names substitution at 0.9696 and is not uncertain. "
            "40 of 40 shuffles are also named substitution, and 25 of 40 are at least as confident. "
            "The fourth column has one symbol 6 times. 6 of 200 shuffled grids match that. "
            "A repetitive column is not a reading. Refuse it."
        ),
    }


def consider_column_null() -> dict:
    report = column_null_report()
    allowed = report["reaches_prose"] and report["best_shuffles_as_high"] * 20 < report["draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "column_null_allowed": allowed,
        "learned": (
            "Dropping the best of the 14 columns leaves 182 cells at -3.3208. "
            "That column is index 5, not the repetitive fourth column. "
            "12 of 80 shuffled grids, allowed to drop their own best column, do as well. "
            "Dropping the fourth column scores -3.6511, and 77 of 80 shuffles do as well. "
            "Dropping its six repeated symbols scores -3.5794, and 58 of 80 do as well. "
            "Prose is -2.5185. The repetitive column is not filler. Refuse it."
        ),
    }


def consider_large_swarm() -> dict:
    report = large_swarm_report()
    deletion_ok = report["reaches_prose"] and report["deletion_shuffles_as_high"] * 20 < report["deletion_draws"]
    gap_ok = report["gap_shuffles_as_high"] * 20 < report["gap_draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "large_swarm_allowed": deletion_ok and gap_ok,
        "learned": (
            "Every pair of cells was dropped, 19,110 ways. The best is -3.3437. "
            "Prose is -2.5185. 21 of 40 shuffled texts, given the same 19,110 drops, do as well. "
            "Repeat gaps at periods 2 through 28 peak at a z of 0.7495. "
            "1,505 of 5,000 shuffles peak at least that high. Refuse both."
        ),
    }


def consider_refined() -> dict:
    report = refined_report()
    allowed = report["shuffles_as_high"] * 20 < report["draws"] and report["peak_count"] > 1
    return {
        "solved": False,
        "claimed_plaintext": None,
        "refined_allowed": allowed,
        "learned": (
            "The most surprising neighbor pair has a z of 3.9957 and occurs once. "
            "1,637 of 2,000 shuffles have a peak at least that high. "
            "A pair that appears once is not a pattern. Refuse it."
        ),
    }


def consider_bob() -> dict:
    report = bob_caution_report()
    allowed = report["challenge_uses_order"] and report["weights_match_shipped"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_allowed": allowed,
        "learned": (
            "Bob names the cells substitution at 0.969. 40 of 40 shuffles get the same name, "
            "so the call does not use the order. On a Caesar of known prose he names caesar, "
            "and 0 of 40 shuffles agree. The call uses the promoted weights."
        ),
    }


def consider_keystream() -> dict:
    report = keystream_report()
    allowed = report["reaches_prose"] and report["best_shuffles_as_high"] * 20 < report["draws"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "keystream_allowed": allowed,
        "learned": (
            "Using one column as the key for the rest of its row, the best is column 9 added, at -3.645. "
            "71 of 80 shuffled grids do as well. The repetitive fourth column scores -3.6947, "
            "and 21 of 80 do as well. Prose is -2.5185. It is not a key. Refuse it."
        ),
    }
