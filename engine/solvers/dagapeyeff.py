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
from engine.bob_exercise import bob_exercise_report
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
from engine.dagapeyeff_triples import triples_report
from engine.dagapeyeff_contact import contact_report
from engine.dagapeyeff_meeting import meeting_report
from engine.dagapeyeff_sandwich import sandwich_report
from engine.dagapeyeff_outside import outside_report
from engine.dagapeyeff_modulo import modulo_report
from engine.dagapeyeff_halves import halves_report
from engine.dagapeyeff_repeat import repeat_report
from engine.dagapeyeff_held import held_report
from engine.dagapeyeff_seats import seats_report
from engine.dagapeyeff_extras import extras_report
from engine.dagapeyeff_heldsand import heldsand_report
from engine.dagapeyeff_heldwait import heldwait_report
from engine.dagapeyeff_quartet import quartet_report
from engine.dagapeyeff_squares import squares_report
from engine.dagapeyeff_twospace import twospace_report
from engine.dagapeyeff_echo import echo_report
from engine.dagapeyeff_ride import ride_report
from engine.dagapeyeff_span import span_report
from engine.dagapeyeff_successive import successive_report
from engine.dagapeyeff_counts import counts_report
from engine.dagapeyeff_tile import tile_report
from engine.dagapeyeff_blank import blank_report
from engine.bob_pair import bob_pair_report
from engine.bob_lift import bob_lift_report
from engine.bob_distill import bob_distill_report
from engine.bob_attack import bob_attack_report
from engine.bob_slim import bob_slim_report
from engine.bob_read import bob_read_report
from engine.solver_attack import solver_attack_report
from engine.bob_train import bob_train_report
from engine.solver_train import solver_train_report
from engine.dagapeyeff_anneal import anneal_swarm_report
from engine.dagapeyeff_grille import grille_report
from engine.dagapeyeff_booksquare import booksquare_report
from engine.dagapeyeff_spiral import spiral_report
from engine.solver_strong import solver_strong_report
from engine.dagapeyeff_columnar import columnar_report
from engine.dagapeyeff_columnar14 import columnar14_report
from engine.dagapeyeff_corpus import corpus_report
from engine.dagapeyeff_claims import claims_report
from engine.dagapeyeff_body import body_report
from engine.dagapeyeff_exhaustive import exhaustive_report
from engine.dagapeyeff_keywords import keyword_report
from engine.dagapeyeff_double import double_report
from engine.dagapeyeff_exhaustive10 import exhaustive10_report
from engine.dagapeyeff_foursquare import foursquare_report
from engine.dagapeyeff_additive import additive_report
from engine.dagapeyeff_quick import quick_report
from engine.dagapeyeff_homophone import homophone_report
from engine.dagapeyeff_errors import errors_report
from engine.dagapeyeff_direction import direction_report
from engine.dagapeyeff_pairmap import pairmap_report
from engine.dagapeyeff_columnar14c import columnar14c_report
from engine.dagapeyeff_monotone import monotone_report
from engine.dagapeyeff_straight import straight_report
from engine.dagapeyeff_diagonal import diagonal_report
from engine.dagapeyeff_heavy import heavy_report
from engine.dagapeyeff_spread import spread_report
from engine.dagapeyeff_residual import residual_report
from engine.dagapeyeff_sharp import sharp_report
from engine.dagapeyeff_rest import rest_report
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


def consider_heavy() -> dict:
    report = heavy_report()
    row_rate = report["row_numerator"] / report["row_denominator"]
    column_rate = report["column_numerator"] / report["column_denominator"]
    allowed = row_rate < 0.05 and column_rate < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "heavy_allowed": allowed,
        "learned": (
            f"The fullest row that still has an empty cell has {report['row_full']} entries. "
            "That chance is rarer than 1 in 37005. "
            f"The row of {report['row_open']} entries has no empty cell. "
            f"The fullest column that still has an empty cell has {report['column_full']} entries, "
            "and that chance is 76.7 percent. "
            "The two directions together do not clear 5 percent. "
            f"The solved exercise's fullest such row has {report['control_row_full']} entries, "
            "and that chance is under 1 percent. Not a reading."
        ),
    }


def consider_spread() -> dict:
    report = spread_report()
    challenge = report["either_as_uneven"] / report["draws"]
    exercise = report["control_either_as_uneven"] / report["draws"]
    allowed = exercise < 0.05 and challenge > 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "spread_allowed": allowed,
        "learned": (
            f"The solved exercise's most uneven line stays rare when a column may be the line: "
            f"{report['control_either_as_uneven']} of {report['draws']}. "
            f"The challenge's most uneven row is {report['row_line']}, "
            f"and {report['rows_as_uneven']} of {report['draws']} re-pairings have a row at least that uneven. "
            f"Its most uneven column is {report['column_line']}. "
            f"The two directions together are {report['either_as_uneven']} of {report['draws']}. "
            "The exercise clears 5 percent. The challenge does not share it. Not a reading."
        ),
    }


def consider_residual() -> dict:
    report = residual_report()
    rate = report["best_tail"] / report["draws"]
    allowed = rate < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "residual_allowed": allowed,
        "learned": (
            f"Cells that appear at most three times stay in their seats. "
            f"Seven order scores were taken on the rest. "
            f"The closest is {report['best_name']}, {report['best_tail']} of {report['draws']}. "
            "That does not clear 5 percent. "
            f"The same trigram score on the solved exercise is {report['control_trigram_high']} of {report['draws']}, "
            "so the swarm can see a real reading order. It does not see one here. Not a reading."
        ),
    }


def consider_sharp() -> dict:
    report = sharp_report()
    allowed = report["as_sharp"] / report["draws"] < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "sharp_allowed": allowed,
        "learned": (
            f"The sharpest of the 25 cells is {report['cell']}, with {report['observed']} "
            "where the digit totals expect about 3. "
            f"None of {report['draws']} re-pairings has a cell that far out. "
            f"The total mismatch is {report['chi']}, and the two move together with correlation {report['correlation']}. "
            f"The solved exercise's sharpest cell is matched by {report['control_as_sharp']} of {report['draws']}, "
            "which is not under 5 percent. This is the known pairing at its sharpest cell. Not a reading."
        ),
    }


def consider_rest() -> dict:
    report = rest_report()
    allowed = report["as_large"] / report["draws"] < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "rest_allowed": allowed,
        "learned": (
            f"After the sharpest cell is set aside, {report['rest']} remains. "
            f"None of {report['draws']} re-pairings reach it, and each may set aside its own sharpest cell. "
            f"The furthest leftover is {report['peak']}. "
            f"The solved exercise keeps {report['control_rest']}, and {report['control_as_large']} of {report['draws']} reach it. "
            "The mismatch is not one cell. Not a reading."
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


def consider_bob_exercise() -> dict:
    exercise = bob_exercise_report()
    challenge = bob_caution_report()
    allowed = exercise["exercise_uses_order"] and not challenge["challenge_uses_order"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_exercise_allowed": allowed,
        "learned": (
            f"Bob calls the solved exercise {exercise['exercise_family']}, "
            f"and {exercise['exercise_shuffles_same_family']} of {exercise['draws']} shuffles agree. "
            f"He calls the challenge {challenge['challenge_family']}, "
            f"and {challenge['challenge_shuffles_same_family']} of {challenge['draws']} shuffles agree. "
            "The exercise uses the order. The challenge call does not. Not a reading."
        ),
    }


def consider_triples() -> dict:
    report = triples_report()
    allowed = report["as_aligned"] / report["draws"] < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "triples_allowed": allowed,
        "learned": (
            f"Two runs of three identical cells start in column {report['columns'][0]}. "
            f"The cells are {report['cells'][0]} and {report['cells'][1]}. "
            f"{report['as_aligned']} of {report['draws']} shuffles put two such runs in one starting column. "
            "Not a reading."
        ),
    }


def consider_contact() -> dict:
    report = contact_report()
    allowed = report["aligned"] > 0 and report["contact"] / report["aligned"] < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "contact_allowed": allowed,
        "learned": (
            "The two runs that share a starting column each sit next to a rare cell. "
            f"The cells after them are {report['following'][0]} and {report['following'][1]}. "
            f"Of {report['draws']} shuffles, {report['aligned']} already have two runs in one starting column, "
            f"and {report['contact']} of those also sit next to rare cells. "
            "The contact is not the alignment. Not a reading."
        ),
    }


def consider_meeting() -> dict:
    report = meeting_report()
    allowed = report["as_many"] / report["draws"] < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "meeting_allowed": allowed,
        "learned": (
            f"The most common cell, {report['mode']}, repeats down column {report['vertical_column']} "
            f"in rows {report['vertical_top']}, {report['vertical_top'] + 1}, and {report['vertical_bottom']}. "
            f"That run meets the run of {report['cell']} in row {report['row']}. "
            f"A king's move counts. {report['as_many']} of {report['draws']} shuffles have such a meeting. "
            "Not a reading."
        ),
    }


def consider_sandwich() -> dict:
    report = sandwich_report()
    allowed = report["as_many"] / report["draws"] < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "sandwich_allowed": allowed,
        "learned": (
            f"The most common cell is {report['mode']}. "
            f"Twice, {report['middle']} sits between two of them, both times in a row. "
            f"{report['middle']} is also a run of three. A vertical gap would have counted. "
            f"{report['as_many']} of {report['draws']} shuffles have at least two such gaps. "
            "Not a reading."
        ),
    }


def consider_outside() -> dict:
    report = outside_report()
    allowed = report["aligned"] > 0 and report["spare"] / report["aligned"] < 0.05
    return {
        "solved": False,
        "claimed_plaintext": None,
        "outside_allowed": allowed,
        "learned": (
            "The two runs that share a starting column each have two further copies "
            "of that cell in the same row. "
            f"Of {report['draws']} shuffles, {report['aligned']} already have the alignment, "
            f"and {report['spare']} of those also have two outside copies in every such row. "
            "The extra copies are not the alignment. Not a reading."
        ),
    }


def consider_modulo() -> dict:
    report = modulo_report()
    axis = "column" if report["axis"] == "x" else "row"
    return {
        "solved": False,
        "claimed_plaintext": None,
        "modulo_allowed": report["allowed"],
        "learned": (
            f"The {report['digit']} digit matches the {axis} of the grid, modulo 5, "
            f"in {report['hits']} cells. That is the best of {report['alignments']} alignments. "
            f"{report['early_as_high']} of {report['early_draws']} shuffles reach it, and "
            f"{report['as_high']} of {report['draws']} do. "
            "The same four pairs, scored as whole tables, are ordinary: "
            f"{report['chi_as_high']} of {report['chi_draws']} shuffles match the chi-square. "
            "The solved exercise does not clear. Not a reading."
        ),
    }


def consider_halves() -> dict:
    report = halves_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "halves_allowed": report["allowed"],
        "learned": (
            f"Even positions use {report['even_support']} symbols and odd positions use "
            f"{report['odd_support']}. "
            f"{report['as_high']} of {report['draws']} shuffles have a gap at least that large. "
            "The five symbols that sit only on the odd side are the five that never leave the last column. "
            f"Leave them out and the gap is {report['residual_gap']}, "
            f"which {report['residual_as_high']} of {report['draws']} shuffles match. "
            f"A period of 7 has a gap of {report['period7_gap']}, "
            f"and {report['period7_as_high']} of {report['draws']} shuffles match. "
            f"Leave the same five out and that gap is {report['period7_residual_gap']}, "
            f"matched by {report['period7_residual_as_high']} of {report['draws']}. "
            "Not a reading."
        ),
    }


def consider_tile() -> dict:
    report = tile_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "tile_allowed": report["allowed"],
        "learned": (
            f"{report['tiles']} blocks copy a 2 by 2 of the square. "
            f"{report['as_many']} of {report['draws']} shuffles have that many. "
            "Not a reading."
        ),
    }


def consider_blank() -> dict:
    report = blank_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "blank_allowed": report["allowed"],
        "learned": (
            f"{report['empty']} cells of the square are empty. "
            f"The digit that appears once leaves {report['once_empty']} of them empty in every re-pairing. "
            f"Shuffling either digit, {report['column_as_many']} and {report['row_as_many']} "
            f"of {report['draws']} reach the total. "
            "The solved exercise does not. Not a reading."
        ),
    }


def consider_counts() -> dict:
    report = counts_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "counts_allowed": report["allowed"],
        "learned": (
            f"The counts of three, two and one sit in order on the square. "
            f"{report['favorable']} of {report['placements']} placements do that. "
            "Not a reading."
        ),
    }


def consider_successive() -> dict:
    report = successive_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "successive_allowed": report["allowed"],
        "learned": (
            f"The cells that appear once sit in successive rows. "
            f"{report['successive_choices']} of {report['choices']} row arrangements do that, given the shared column. "
            "Not a reading."
        ),
    }


def consider_span() -> dict:
    report = span_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "span_allowed": report["allowed"],
        "learned": (
            f"A parallel line reads the same forwards and backwards across the span of a spaced triple. "
            f"{report['as_many']} of {report['draws']} scrambles have such a span, using any cell and any row or column. "
            "Not a reading."
        ),
    }


def consider_ride() -> dict:
    report = ride_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "ride_allowed": report["allowed"],
        "learned": (
            f"The two lines of an echoed triple are also two seats of a spaced triple. "
            f"{report['as_many']} of {report['draws']} scrambles have such a pair of lines, using any cell. "
            "Not a reading."
        ),
    }


def consider_echo() -> dict:
    report = echo_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "echo_allowed": report["allowed"],
        "learned": (
            f"{report['echo_count']} spaced triples are each repeated in at least two seats by a parallel line. "
            f"{report['as_many']} of {report['draws']} scrambles do that, using any cell and any row or column. "
            "Not a reading."
        ),
    }


def consider_twospace() -> dict:
    report = twospace_report()
    line = report["lines"][0]
    cells = ", ".join(
        f"{item['cell']} at {item['seats'][0]}, {item['seats'][1]} and {item['seats'][2]}"
        for item in line["cells"]
    )
    return {
        "solved": False,
        "claimed_plaintext": None,
        "twospace_allowed": report["allowed"],
        "learned": (
            f"{line['axis'].capitalize()} {line['index']} holds two cells with three equally spaced seats each: {cells}. "
            f"{report['as_many']} of {report['draws']} scrambles have such a line, using any row or column and any cells. "
            "Not a reading."
        ),
    }


def consider_squares() -> dict:
    report = squares_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "squares_allowed": report["allowed"],
        "learned": (
            f"Of the cells that share one count, {report['cell']} has "
            f"{report['even']} copies on one color of the board and {report['odd']} on the other. "
            f"{report['as_split']} of {report['draws']} scrambles, allowed to pick their most uneven cell, match that split. "
            "A straight run alternates colors, so the runs do not cause it. Not a reading."
        ),
    }


def consider_quartet() -> dict:
    report = quartet_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "quartet_allowed": report["allowed"],
        "learned": (
            "Four cells share one count: "
            + ", ".join(report["cells"])
            + f". No row holds more than {report['row_most']} of them, "
            f"and no column holds more than {report['column_most']}. "
            f"Taking the more even direction, {report['as_even']} of {report['draws']} scrambles are that even. "
            "The most common cell is not spread this way, and neither are the next four cells. Not a reading."
        ),
    }


def consider_heldwait() -> dict:
    report = heldwait_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "heldwait_allowed": report["allowed"],
        "learned": (
            "The rare cells stay in their seats. "
            f"The longest wait for a new cell is {report['wait']}, and {report['as_short']} of {report['draws']} "
            "draws are that short or shorter. "
            f"Ignore the rare cells and the wait is {report['skip_wait']}, matched by "
            f"{report['skip_as_short']} of {report['draws']}. "
            "The short wait does not survive once the rare cells are left out of the count. Not a reading."
        ),
    }


def consider_heldsand() -> dict:
    report = heldsand_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "heldsand_allowed": report["allowed"],
        "learned": (
            "The rare cells stay in their seats. "
            f"{report['as_many']} of {report['draws']} draws still have the common cell on both sides "
            f"of a cell that also has a run of three. "
            f"A plain gap, with any other cell in the middle, is {report['plain_as_many']} of {report['draws']}. "
            f"{report['also_aligned']} of the {report['as_many']} also have two aligned runs. "
            "The sandwich stays under 5 percent. The plain gap does not. Not a reading."
        ),
    }


def consider_extras() -> dict:
    report = extras_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "extras_allowed": report["allowed"],
        "learned": (
            "The rare cells stay in their seats. "
            f"Of {report['aligned']} shuffles that already have two runs in one starting column, "
            f"{report['at_least_one']} have at least one further copy in the row, "
            f"and {report['at_least_two']} have two. "
            f"{report['also_touching']} of those two-copy rows are also the rows that touch a rare cell. "
            "One further copy does not clear. Two do. Not a reading."
        ),
    }


def consider_seats() -> dict:
    report = seats_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "seats_allowed": report["allowed"],
        "learned": (
            "The rare cells stay in their seats. "
            f"Of {report['aligned']} shuffles that already have two runs in one starting column, "
            f"{report['contact']} also have both runs next to a rare cell. "
            f"Of {report['vertical_runs']} shuffles that already have a vertical run of the common cell, "
            f"{report['meeting_given_vertical']} also meet a different run. "
            "The contact stays under 5 percent. The meeting does not. Not a reading."
        ),
    }


def consider_held() -> dict:
    report = held_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "held_allowed": report["allowed"],
        "learned": (
            "The five cells that appear at most three times stay in their seats. "
            f"The other {196 - report['pinned']} cells are shuffled. "
            f"Two runs still share a starting column in {report['as_aligned']} of {report['draws']} draws. "
            f"A plain count of two runs, aligned or not, is {report['as_many_runs']} of {report['draws']}. "
            "The alignment is not the rare column. Not a reading."
        ),
    }


def consider_repeat() -> dict:
    report = repeat_report()
    hit = report["hits"][0]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "repeat_allowed": report["allowed"],
        "learned": (
            f"One {hit['axis']} holds runs of lengths {hit['lengths']} of the same cell. "
            f"{report['as_high']} of {report['draws']} shuffles have at least one such line. "
            f"Of the {report['vertical_runs']} shuffles that already have a vertical run of three, "
            f"{report['vertical_and_feature']} also have the second run. "
            f"Of the {report['any_long']} shuffles with a long run in either direction, "
            f"{report['any_and_feature']} do. The raw rate is under 5 percent and the widened rates are not. "
            "Not a reading."
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


def consider_bob_pair() -> dict:
    report = bob_pair_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_pair_allowed": report["promoted"],
        "learned": (
            f"A side vote on six M-209 scores, fit on training keys, would move the 480 from "
            f"{report['held_before']} to {report['held_after']} and the older 204 from "
            f"{report['benchmark_before']} to {report['benchmark_after']}. "
            "The older bar drops, so the weights stay. Not a reading."
        ),
    }


def consider_bob_lift() -> dict:
    report = bob_lift_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_lift_allowed": report["promoted"],
        "learned": (
            f"Two of the three networks, then a sure Enigma versus M-209 vote, move the 480 from "
            f"{report['held_before']} to {report['held_after']} "
            f"({report['held_corrections']} corrections, {report['held_mistakes']} new mistakes) "
            f"and the older 204 from {report['benchmark_before']} to {report['benchmark_after']}. "
            "The weight file stays. Not a reading, and not 480 of 480."
        ),
    }


def consider_bob_distill() -> dict:
    report = bob_distill_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_distill_allowed": report["promoted"],
        "learned": (
            f"A linear student of the three networks scores {report['held_student']} of {report['held_total']} "
            f"and {report['benchmark_student']} of {report['benchmark_total']}. "
            f"The lifted ranking is {report['held_lift']} and {report['benchmark_lift']}. "
            f"A Sinkhorn mix of the three outputs scores {report['held_sinkhorn']} and {report['benchmark_sinkhorn']}. "
            "Neither beats the lift, so neither is promoted. The weight file stays. Not a reading."
        ),
    }


def consider_bob_attack() -> dict:
    report = bob_attack_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_attack_allowed": False,
        "learned": (
            f"On {report['texts']} training ciphers the lifted call is right {report['clean_correct']} times. "
            f"Deleting the middle letter flips {report['deletion_flips']}. "
            f"The withhold gate keeps {report['hardened_correct']} right calls, "
            f"withholds {report['hardened_withheld']}, and still misses {report['hardened_wrong']}. "
            f"Unencrypted English is certain on {report['plain_certain']} of {report['plain_draws']} draws. "
            "That gate is not a higher score. Not a reading."
        ),
    }


def consider_bob_slim() -> dict:
    report = bob_slim_report()
    if report["promoted"]:
        ending = "A smaller student beat the lift. The weight file still stays. Not a reading."
    else:
        ending = "None of them beat the lift. The weight file stays. Not a reading."
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_slim_allowed": report["promoted"],
        "learned": (
            f"A 20-number bias scores {report['held_bias']} of {report['held_total']} "
            f"and {report['benchmark_bias']} of {report['benchmark_total']}. "
            f"A bias fit to the lift scores {report['held_lift_bias']} and {report['benchmark_lift_bias']}. "
            f"A three-weight mix scores {report['held_mix']} and {report['benchmark_mix']}. "
            f"The lifted ranking is {report['held_lift']} and {report['benchmark_lift']}. "
            + ending
        ),
    }


def consider_bob_read() -> dict:
    report = bob_read_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_read_allowed": False,
        "learned": (
            f"On training windows the reader matches Caesar {report['caesar_matched']} of {report['caesar_texts']} "
            f"and Vigenere {report['vigenere_matched']} of {report['vigenere_texts']}. "
            f"Substitution is left alone {report['substitution_withheld']} of {report['substitution_texts']}. "
            f"Beaufort is left alone {report['beaufort_withheld']} of {report['beaufort_texts']}. "
            f"A short shifted proverb was named {report['proverb_family']} and withheld. Not a reading."
        ),
    }


def consider_solver_attack() -> dict:
    report = solver_attack_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "solver_attack_allowed": False,
        "learned": (
            f"Caesar search is exact on {report['caesar_exact']} of {report['caesar_texts']}. "
            f"Vigenere search is exact on {report['vigenere_exact']} of {report['vigenere_texts']}, "
            f"and a one-letter deletion keeps the keyword {report['vigenere_delete_holds']} times. "
            "That deletion check stays off, because it would also drop the true keywords. "
            f"Substitution is consistent on {report['substitution_consistent']} and exact on {report['substitution_exact']}. "
            "A wrong key still re-encrypts. The order flag is not a recovery. Not a reading."
        ),
    }


def consider_bob_train() -> dict:
    report = bob_train_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "bob_train_allowed": report["promoted"],
        "learned": (
            f"A warm start of {report['epochs']} epochs stays at {report['held_after']} of {report['held_total']} "
            f"and {report['benchmark_after']} of {report['benchmark_total']}. "
            f"Every checkpoint stayed at the shipped network. The lift is still {report['lift_held']} and {report['lift_benchmark']}. "
            "The file was not replaced. Not a reading."
        ),
    }


def consider_solver_train() -> dict:
    report = solver_train_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "solver_train_allowed": report["promoted"],
        "learned": (
            f"On {report['windows']} fresh windows the default substitution search is exact {report['default_exact']} times "
            f"and the longer search is exact {report['long_exact']} times. "
            "Both recover the known certificate. The default stays. Not a reading."
        ),
    }


def consider_anneal_swarm() -> dict:
    report = anneal_swarm_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "anneal_swarm_allowed": False,
        "learned": (
            f"Bob names the cells {report['reader_family']} and the reader withholds. "
            f"A longer substitution search is matched by {report['substitution_shuffles_as_high']} of {report['draws']} shuffles. "
            f"Caesar is matched by {report['caesar_shuffles_as_high']} and Vigenere by {report['vigenere_shuffles_as_high']}. "
            "The cells do not win the swarm. Not a reading."
        ),
    }


def consider_grille() -> dict:
    report = grille_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "grille_allowed": False,
        "learned": (
            f"With the letter key given, the grille search recovers {report['known_key_recovered']} of "
            f"{len(report['known_key'])} planted grilles. With both unknown it recovers {report['joint_recovered']} of "
            f"{len(report['joint'])}, so the grille class is not closed. "
            f"On the cells {report['cell_shuffles_as_high']} of {len(report['cell_shuffles_per_letter'])} shuffles score as high. "
            f"A key should stand out after about {report['unicity_letters']} letters. Not a reading."
        ),
    }


def consider_booksquare() -> dict:
    report = booksquare_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "booksquare_allowed": False,
        "learned": (
            f"The exercise's own square, under the best of {len(report['labelings'])} digit labelings, gives a chi-square "
            f"of {report['best_chi_square']}. The worst of {report['english_draws']} English draws is {report['english_chi_max']}. "
            "A transposition cannot change counts. Not a reading."
        ),
    }


def consider_spiral() -> dict:
    report = spiral_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "spiral_allowed": False,
        "learned": (
            f"The best of {report['readings']} spiral, snake and zigzag readings scores {report['best_mi']}. "
            f"{report['shuffles_as_high']} of {report['draws']} shuffles do as well, and English is {report['english_mi']}. "
            "Not a reading."
        ),
    }


def consider_solver_strong() -> dict:
    report = solver_strong_report()
    rows = {row["width"]: row for row in report["rows"]}
    return {
        "solved": False,
        "claimed_plaintext": None,
        "solver_strong_allowed": report["promoted"],
        "learned": (
            f"At 200 letters the legacy model is exact on {rows[200]['legacy_exact']} of {rows[200]['windows']} windows "
            f"and the larger model on {rows[200]['default_exact']}. The larger model is the default. "
            "A drill on training text is not a reading."
        ),
    }


def consider_columnar() -> dict:
    report = columnar_report()
    rows = {row["width"]: row for row in report["rows"]}
    powered = [width for width, row in rows.items() if row["planted_recovered"] == len(row["planted"])]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "columnar_allowed": False,
        "learned": (
            f"Planted texts come back at widths {powered}, and there the cells score between "
            f"{min(rows[w]['cells_per_letter'] for w in powered)} and {max(rows[w]['cells_per_letter'] for w in powered)} "
            f"a letter, where shuffles score, against planted English near {report['lowest_planted_true_per_letter']}. "
            "Width 14 recovered no planted text, so it stays open. Not a reading."
        ),
    }


def consider_columnar14() -> dict:
    report = columnar14_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "columnar14_allowed": False,
        "learned": (
            f"At width 14 under a new seed the cells score {report['cells_per_letter']}. "
            f"{report['plain_shuffles_as_high']} of {report['draws']} plain shuffles and "
            f"{report['kept_column_shuffles_as_high']} of {report['draws']} shuffles that keep the rare column do as well. "
            "Not a reading."
        ),
    }


def consider_corpus() -> dict:
    report = corpus_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "corpus_allowed": False,
        "learned": (
            f"Of {report['windows']} real 196-letter windows, {report['windows_as_flat']} are as flat as the cells, "
            f"{report['windows_as_narrow']} use {report['cell_distinct']} letters or fewer, and "
            f"{report['windows_all_three']} share those with a top count of {report['cell_largest']} or less. Not a reading."
        ),
    }


def consider_claims() -> dict:
    report = claims_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "claims_allowed": False,
        "learned": (
            f"{len(report['claims'])} published readings were checked. "
            f"{report['full_length_claims_with_cell_profile']} full-length readings have the cells' letter counts. "
            "A quoted claim is someone else's, not a reading here."
        ),
    }


def consider_body() -> dict:
    report = body_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "body_allowed": False,
        "learned": (
            f"The 13 common symbols score {report['cells_top13_chi']} against equal counts; "
            f"{report['uniform_as_flat_or_flatter']} of {report['uniform_draws']} uniform draws are as flat, and "
            f"{report['windows_as_flat']} of {report['windows']} real prose windows. Not a reading."
        ),
    }


def consider_exhaustive() -> dict:
    report = exhaustive_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "exhaustive_allowed": False,
        "learned": (
            f"Every order at widths 2 to 9, in {len(report['rows'])} width and family cases. In each case the "
            "cells and the regrouping beat their own shuffles by less than planted English and German beat theirs. "
            "No letter key can change this score, so the plaintext language does not matter. Not a reading."
        ),
    }


def consider_keywords() -> dict:
    report = keyword_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "keywords_allowed": False,
        "learned": (
            f"{report['keywords']} keywords gave {report['orders_scored']} keyword-ordered transpositions. Every planted "
            f"text surfaced near English; the cells' best, {report['cells_best_mi']}, is under the best of shuffled "
            f"cells, {max(report['null_best_mi'])}. Not a reading."
        ),
    }


def consider_double() -> dict:
    report = double_report()
    return {
        "solved": False,
        "claimed_plaintext": None,
        "double_allowed": False,
        "learned": (
            f"Every pair of column orders at widths 2 to 6, both passes undone or both done: in "
            f"{report['cases_cells_below_planted']} of {report['cases']} cases the cells beat their shuffles by less "
            "than planted English and German beat theirs. Not a reading."
        ),
    }


def consider_exhaustive10() -> dict:
    report = exhaustive10_report()
    powered = [row["family"] for row in report["rows"] if min(p["excess"] for p in row["planted"]) > 0]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "exhaustive10_allowed": False,
        "learned": (
            f"At width 10 planted English and German still stand out only for {powered}; for the other families a "
            "shuffle of the planted text scores as high, so nothing follows there. Where power holds, the cells do "
            "not beat their shuffles. Not a reading."
        ),
    }


def consider_foursquare() -> dict:
    report = foursquare_report()
    counts = report["counts"]
    low, high = sorted(counts["texts"]["cells"]["pairs-from-first"])
    best = max(row["per_letter"] for row in report["searched"].values())
    return {
        "solved": False,
        "claimed_plaintext": None,
        "foursquare_allowed": False,
        "learned": (
            f"Four-square fixes how many symbols each side of a pair can use before any key is chosen. The cells use "
            f"{low} and {high}, and held-out English never has fewer than {counts['keyed_fewest_larger_side']} on its "
            f"larger side, even with keyed plain squares. The search recovers {report['planted_recovered']} of "
            f"{len(report['planted'])} planted texts. The cells and the regrouping score near their shuffles, "
            f"{best} a letter at best, where planted English is {report['planted_lowest_true']} or higher. Not a reading."
        ),
    }


def consider_additive() -> dict:
    report = additive_report()
    counts = report["counts"]
    fewest = min(row["fewest_distinct"] for row in counts["rows"])
    reaching = sum(row["reaching_cells"] for row in counts["rows"])
    draws = sum(row["draws"] for row in counts["rows"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "additive_allowed": False,
        "learned": (
            f"A repeating coordinate shift on a keyed square spreads letters over more cells. The cells use "
            f"{counts['cells']['distinct']} symbols; held-out English under random squares and shift keys never uses "
            f"fewer than {fewest}, and {reaching} of {draws} draws reach the cells' counts. The joint search recovers "
            f"{report['planted_recovered']} of {len(report['planted'])} planted texts; the cells and the regrouping "
            f"reach {report['searched_best']} a letter at best, where planted English is "
            f"{report['planted_lowest_true']} or higher. Not a reading."
        ),
    }


def consider_quick() -> dict:
    report = quick_report()
    spaces = report["spaces"]
    best = report["searched_best"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "quick_allowed": False,
        "learned": (
            f"Nulls by place, the cells reversed and the column digits alone, solved as a keyed square: planted "
            f"English comes back {report['planted_recovered']} of {len(report['planted'])} times at "
            f"{report['planted_lowest_true']} a letter or better, and the cells' best is {best['per_letter']} "
            f"({best['variant']}). Rare symbols as spaces would make words {spaces['mean_word_length']} letters long. "
            "Not a reading."
        ),
    }


def consider_homophone() -> dict:
    report = homophone_report()
    rows = report["searched"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "homophone_allowed": False,
        "learned": (
            f"A many-to-one key, capped at {report['search']['letter_cap']} places a letter, recovers "
            f"{report['planted_recovered']} of {len(report['planted'])} planted homophonic texts. The cells score "
            f"{rows['cells']['per_letter']} ({rows['cells']['shuffles_as_high']} of 8 shuffles as high) and the "
            f"regrouping {rows['regrouped']['per_letter']} ({rows['regrouped']['shuffles_as_high']} of 8), against "
            f"{report['planted_lowest_true']} for planted English. Not a reading."
        ),
    }


def consider_errors() -> dict:
    report = errors_report()
    counts = report["counts"]
    eight = report["by_errors"]["8"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "errors_allowed": False,
        "learned": (
            f"No held-out English window reaches the cells' counts with fewer than {counts['best_case_fewest']} "
            f"chosen errors, and random errors reach them 0 times. With 8 digit slips planted English still scores "
            f"{eight['found_low']} a letter or better against the cells' {report['cells_per_letter']}; English falls "
            f"to the cells' level only at {report['fewest_errors_at_cells_level']} errors. Not a reading."
        ),
    }


def consider_italian() -> dict:
    import json
    from pathlib import Path

    # The frozen file is read directly: rerunning the probe would fetch the Italian text.
    path = Path(__file__).resolve().parents[1] / "data" / "swarm_cache" / "dagapeyeff-italian.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    counts = report["counts"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "italian_allowed": False,
        "learned": (
            f"Manzoni's Italian needs at least {counts['fewest_errors']} chosen errors to reach the cells' counts. "
            f"Under an Italian model planted Italian comes back {report['planted_recovered']} of 4 times, and "
            f"{report['planted_with_errors_recovered']} of 4 with 8 slips; the cells score {report['cells_per_letter']}, "
            f"with {report['shuffles_as_high']} of 8 shuffles as high. Not a reading."
        ),
    }


def consider_direction() -> dict:
    report = direction_report()
    families = report["families"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "direction_allowed": False,
        "learned": (
            f"Delays, nulls of period 2 to 14, rails and plain columns, {report['search']['transforms']} transforms "
            f"solved as a keyed square: planted English comes back {report['planted_recovered']} of "
            f"{len(report['planted'])} times. The cells' best is {families['all']['cells_best']} and "
            f"{families['all']['shuffle_bests_as_high']} of {len(families['all']['shuffle_bests'])} shuffles reach "
            "it. No old lead points anywhere. Not a reading."
        ),
    }


def _frozen_file(name: str) -> dict:
    import json
    from pathlib import Path

    # Read directly: rerunning these probes would fetch outside text.
    path = Path(__file__).resolve().parents[1] / "data" / "swarm_cache" / f"dagapeyeff-{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def consider_screen() -> dict:
    report = _frozen_file("screen")
    closest = report["closest"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "screen_allowed": False,
        "learned": (
            f"Of {len(report['languages'])} languages, {closest['treebank']} comes closest to the cells' letter "
            f"counts: {closest['fewest_errors']} errors at its closest window, {closest['median_errors']} at the "
            "median. A count fit is a reason to search, not a reading."
        ),
    }


def consider_latin() -> dict:
    report = _frozen_file("latin")
    cells = report["searched"]["cells"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "latin_allowed": False,
        "learned": (
            f"Under a Latin model planted Latin comes back {report['planted_recovered']} of 6 times, and "
            f"{report['planted_with_errors_recovered']} of 6 with 8 slips. The cells' best is {cells['best']} "
            f"({cells['best_variant']}), and {cells['shuffle_bests_as_high']} of 8 shuffles reach it. Not a reading."
        ),
    }


def consider_pairmap() -> dict:
    report = pairmap_report()
    cells = report["texts"]["cells"]
    regrouped = report["texts"]["regrouped"]
    return {
        "solved": False,
        "claimed_plaintext": None,
        "pairmap_allowed": False,
        "learned": (
            "A cipher that sends each plaintext pair to one fixed cipher pair keeps the number of different pairs. "
            f"The cells use {cells['phase 0']['different_pairs']} and {cells['phase 1']['different_pairs']}; "
            f"{cells['phase 0']['windows_as_many']} and {cells['phase 1']['windows_as_many']} of {report['windows']} "
            "prose windows use as many, so the count does not exclude such a cipher on the cells. The regrouping uses "
            f"{regrouped['phase 0']['different_pairs']} at both phases, reached by "
            f"{regrouped['phase 0']['windows_as_many']} and {regrouped['phase 1']['windows_as_many']} windows. "
            "Not a reading."
        ),
    }


def consider_columnar14c() -> dict:
    report = columnar14c_report()
    recovered = sum(done for done, _ in report["planted_recovered"].values())
    planted = sum(total for _, total in report["planted_recovered"].values())
    best = max(row["per_letter"] for row in report["searched"].values())
    weakest = min(row["found_per_letter"] for row in report["planted"])
    return {
        "solved": False,
        "claimed_plaintext": None,
        "columnar14c_allowed": False,
        "learned": (
            f"A compiled joint search of the 14-column order and the letter key recovers {recovered} of {planted} "
            "planted 196-letter texts in both directions, some with 8 wrong cells. The cells and the regrouping "
            f"score {best} a letter at best, inside their shuffles, where the weakest planted text was found at "
            f"{weakest}. Not a reading."
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
