"""Published Sudoku answers and bounded general puzzle behavior."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from engine.puzzles import find_anagrams, find_words, main, solve_sudoku


PUBLISHED_GRID = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
PUBLISHED_SOLUTION = "417369825632158947958724316825437169791586432346912758289643571573291684164875293"
EASY_GRID = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
EASY_SOLUTION = "483921657967345821251876493548132976729564138136798245372689514814253769695417382"


class SudokuTest(unittest.TestCase):
    def assert_valid_completion(self, solution, original):
        self.assertEqual(len(solution), 81)
        for index, digit in enumerate(original):
            if digit in "123456789":
                self.assertEqual(solution[index], digit)
        units = [solution[row * 9:row * 9 + 9] for row in range(9)]
        units += [solution[column::9] for column in range(9)]
        units += ["".join(solution[(row + dr) * 9 + column + dc] for dr in range(3) for dc in range(3))
                  for row in (0, 3, 6) for column in (0, 3, 6)]
        self.assertTrue(all(set(unit) == set("123456789") for unit in units))

    def test_norvig_published_grid_solution_and_certificate(self):
        result = solve_sudoku(PUBLISHED_GRID, max_nodes=10000)
        self.assertEqual(result.status, "solved")
        self.assertEqual(result.solution, PUBLISHED_SOLUTION)
        self.assertEqual(result.uniqueness, "unique")
        self.assertTrue(result.search_complete)
        self.assert_valid_completion(result.solution, PUBLISHED_GRID)
        certificate = json.loads((Path(__file__).parents[1] / "engine/data/puzzle_certificate.json").read_text())
        vector = certificate["vectors"][0]
        self.assertEqual(vector["grid"], PUBLISHED_GRID)
        self.assertEqual(vector["solution"], PUBLISHED_SOLUTION)
        self.assertEqual(vector["sha256"], hashlib.sha256(result.solution.encode("ascii")).hexdigest())
        self.assertNotIn("ciphertext", vector)

    def test_propagation_only_and_already_completed_grid(self):
        for grid in (EASY_GRID, EASY_SOLUTION):
            result = solve_sudoku(grid, max_nodes=1)
            self.assertEqual(result.status, "solved")
            self.assertEqual(result.solution, EASY_SOLUTION)
            self.assertEqual(result.nodes, 1)

    def test_budget_exhaustion_never_claims_solved_or_unique(self):
        for maximum in (0, 1):
            result = solve_sudoku(PUBLISHED_GRID, max_nodes=maximum)
            self.assertEqual(result.status, "incomplete")
            self.assertEqual(result.uniqueness, "unknown")
            self.assertIsNone(result.solution)
            self.assertFalse(result.search_complete)
            self.assertTrue(result.exhausted)
            self.assertLessEqual(result.nodes, maximum)
        result = solve_sudoku(PUBLISHED_GRID, max_nodes=26)
        self.assertEqual(result.solutions, (PUBLISHED_SOLUTION,))
        self.assertEqual(result.status, "incomplete")
        self.assertEqual(result.uniqueness, "unknown")
        self.assertIsNone(result.solution)

    def test_two_valid_completions_prove_nonuniqueness(self):
        grid = "".join("." if digit in "12" else digit for digit in EASY_SOLUTION)
        result = solve_sudoku(grid, max_nodes=100)
        self.assertEqual(result.status, "multiple")
        self.assertEqual(result.uniqueness, "multiple")
        self.assertEqual(len(result.solutions), 2)
        self.assertFalse(result.search_complete)
        self.assertFalse(result.exhausted)
        self.assertNotEqual(*result.solutions)
        self.assertIsNone(result.solution)
        for solution in result.solutions:
            self.assert_valid_completion(solution, grid)

    def test_contradictory_and_unsatisfiable_clues(self):
        for grid in ("11" + "." * 79, "5" + EASY_GRID[1:]):
            result = solve_sudoku(grid, max_nodes=100)
            self.assertEqual(result.status, "unsatisfiable")
            self.assertEqual(result.uniqueness, "none")
            self.assertTrue(result.search_complete)
            self.assertIsNone(result.solution)

    def test_strict_grid_and_budget_validation(self):
        for grid in ("." * 80, "." * 82, "x" + "." * 80, "\u0661" + "." * 80):
            with self.subTest(grid=grid), self.assertRaises(ValueError):
                solve_sudoku(grid)
        with self.assertRaises(TypeError):
            solve_sudoku(None)
        for maximum in (-1, True, 1000001):
            with self.assertRaises((ValueError, TypeError)):
                solve_sudoku(EASY_GRID, max_nodes=maximum)
        formatted = "\n".join(EASY_GRID[index:index + 9] for index in range(0, 81, 9))
        self.assertEqual(solve_sudoku(formatted).solution, EASY_SOLUTION)


class WordSearchTest(unittest.TestCase):
    def test_eight_directions_rectangles_and_all_occurrences(self):
        rows = ("ABC", "DEF", "GHI")
        words = ("ABC", "CBA", "ADG", "GDA", "AEI", "IEA", "CEG", "GEC", "A", "MISSING")
        result = find_words(rows, words)
        self.assertTrue(result.search_complete)
        self.assertEqual(len(result.matches), 9)
        self.assertEqual({match.direction for match in result.matches if match.word != "A"},
                         {(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)})
        self.assertEqual(result.unmatched_words, ("MISSING",))
        result = find_words(("ABABA", "XXXXX"), ("ABA", "ABA"))
        self.assertEqual(len(result.matches), 4)
        self.assertEqual(len({match.cells for match in result.matches}), 4)

    def test_word_search_budget_retains_only_observed_matches(self):
        result = find_words(("AB", "CD"), ("AB", "CD"), max_checks=1)
        self.assertEqual(result.status, "incomplete")
        self.assertFalse(result.search_complete)
        self.assertLessEqual(result.checks, 1)
        self.assertIsNone(result.unmatched_words)

    def test_grid_word_and_dimension_validation(self):
        for rows in ((), ("AB", "C"), ("A1",), ("\u03b1",), ("",), "ABC"):
            with self.subTest(rows=rows), self.assertRaises((ValueError, TypeError)):
                find_words(rows, ("A",))
        for words in (("",), ("TWO WORDS",), ("\u03b1",), "ABC"):
            with self.assertRaises((ValueError, TypeError)):
                find_words(("ABC",), words)


class AnagramTest(unittest.TestCase):
    def test_supplied_lexicon_exact_letters_duplicates_and_phrase_entries(self):
        result = find_anagrams("Listen", ("silent", "enlist", "listen", "LISTEN", "tinsel", "inlets", "stone"))
        self.assertEqual(result.matches, ("silent", "enlist", "listen", "tinsel", "inlets"))
        self.assertTrue(result.search_complete)
        self.assertEqual(find_anagrams("Dormitory", ("dirty room", "dormitory", "dirty rooms")).matches,
                         ("dirty room", "dormitory"))

    def test_lexicon_scan_is_bounded_and_has_no_default_dictionary(self):
        result = find_anagrams("abc", ("cab", "bca", "abc"), max_entries=1)
        self.assertEqual(result.matches, ("cab",))
        self.assertEqual(result.entries_checked, 1)
        self.assertFalse(result.search_complete)
        self.assertEqual(result.status, "incomplete")
        with self.assertRaises(TypeError):
            find_anagrams("abc")
        for text in ("", "123", "\u03b1\u03b2"):
            with self.assertRaises(ValueError):
                find_anagrams(text, ("abc",))

    def test_standalone_commands_return_structured_results(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            grid = root / "grid.txt"; grid.write_text("ABC\nDEF\n", encoding="utf-8")
            lexicon = root / "lexicon.txt"; lexicon.write_text("silent\nenlist\nstone\n", encoding="utf-8")
            for arguments, status in ((["sudoku", EASY_GRID, "--max-nodes", "1"], "solved"),
                                      (["word-search", "--grid-file", str(grid), "--words", "ABC", "FED"], "complete"),
                                      (["anagram", "listen", "--lexicon", str(lexicon)], "complete")):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(main(arguments), 0)
                self.assertEqual(json.loads(output.getvalue())["status"], status)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(["sudoku", "BAD"]), 2)


if __name__ == "__main__":
    unittest.main()
