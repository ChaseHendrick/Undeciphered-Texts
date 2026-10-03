"""Bounded Sudoku, eight-direction word search, and supplied-lexicon anagrams.

Sudoku combines propagation and minimum remaining values search. A single
completion proves uniqueness only after all remaining branches are ruled
out. Search exhaustion never reports a unique solution.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

SUDOKU_SOURCE_URL = "https://www.norvig.com/sudoku.html"
MAX_NODES = 1_000_000
MAX_GRID_CELLS = 10_000
MAX_WORDS = 1_000
MAX_WORD_LENGTH = 256
MAX_CHECKS = 10_000_000
MAX_LEXICON_ENTRIES = 100_000
MAX_FILE_BYTES = 2_097_152
_ASCII = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
_ALL = (1 << 9) - 1
_UNITS = tuple(
    [tuple(row * 9 + column for column in range(9)) for row in range(9)]
    + [tuple(row * 9 + column for row in range(9)) for column in range(9)]
    + [tuple((row + dr) * 9 + column + dc for dr in range(3) for dc in range(3))
       for row in (0, 3, 6) for column in (0, 3, 6)]
)
_PEERS = tuple(tuple(sorted(set().union(*(unit for unit in _UNITS if cell in unit)) - {cell}))
               for cell in range(81))
_DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def _integer(value, name: str, maximum: int, minimum: int = 0) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be in {minimum}..{maximum}")


def _sequence(value, name: str, maximum: int) -> tuple:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a finite sequence")
    if len(value) > maximum:
        raise ValueError(f"{name} must contain at most {maximum} entries")
    return tuple(value)


@dataclass(frozen=True)
class SudokuReport:
    grid: str
    status: str
    solution: str | None
    solutions: tuple[str, ...]
    uniqueness: str
    search_complete: bool
    solution_count_lower_bound: int
    nodes: int
    max_nodes: int
    exhausted: bool
    algorithm_source_url: str = SUDOKU_SOURCE_URL

    def to_dict(self) -> dict:
        return asdict(self)


def _sudoku_grid(grid: str) -> str:
    if not isinstance(grid, str):
        raise TypeError("Sudoku grid must be a string")
    if len(grid) > 4096:
        raise ValueError("formatted Sudoku grid must not exceed 4096 characters")
    if any(ch not in "1234567890.|+-" and not ch.isspace() for ch in grid):
        raise ValueError("Sudoku grid permits ASCII digits, dots, whitespace, and |+- separators")
    cells = "".join("." if ch == "0" else ch for ch in grid if ch in "1234567890.")
    if len(cells) != 81:
        raise ValueError("Sudoku grid must contain exactly 81 digits or blank cells")
    return cells


def _propagate(state: list[int]) -> bool:
    """Only remove candidates, so each fixed-point loop makes finite progress."""
    changed = True
    while changed:
        changed = False
        for cell, mask in enumerate(state):
            if mask == 0:
                return False
            if mask & (mask - 1) == 0:
                for peer in _PEERS[cell]:
                    if state[peer] & mask:
                        reduced = state[peer] & ~mask
                        if not reduced:
                            return False
                        state[peer] = reduced
                        changed = True
        for unit in _UNITS:
            for digit in range(9):
                bit = 1 << digit
                places = [cell for cell in unit if state[cell] & bit]
                if not places:
                    return False
                if len(places) == 1 and state[places[0]] != bit:
                    state[places[0]] = bit
                    changed = True
    return True


def solve_sudoku(grid: str, *, max_nodes: int = 100_000) -> SudokuReport:
    """Find up to two completions, with a strict bound on visited search nodes.

    Each root or branch visit consumes one node before propagation. Direct
    duplicate givens are a contradiction without search. Once two distinct
    completions are found, nonuniqueness is established and search stops.
    """
    _integer(max_nodes, "max_nodes", MAX_NODES)
    grid = _sudoku_grid(grid)
    for unit in _UNITS:
        givens = [grid[cell] for cell in unit if grid[cell] != "."]
        if len(givens) != len(set(givens)):
            return SudokuReport(grid, "unsatisfiable", None, (), "none", True, 0, 0, max_nodes, False)
    state = [_ALL if digit == "." else 1 << (int(digit) - 1) for digit in grid]
    solutions: list[str] = []
    nodes = 0
    exhausted = False

    def search(current: list[int]) -> bool:
        nonlocal nodes, exhausted
        if nodes >= max_nodes:
            exhausted = True
            return False
        nodes += 1
        if not _propagate(current):
            return True
        pending = [cell for cell, mask in enumerate(current) if mask & (mask - 1)]
        if not pending:
            solutions.append("".join(str(mask.bit_length()) for mask in current))
            return True
        cell = min(pending, key=lambda index: (current[index].bit_count(), index))
        for digit in range(9):
            bit = 1 << digit
            if current[cell] & bit:
                branch = current.copy()
                branch[cell] = bit
                complete = search(branch)
                if not complete or len(solutions) >= 2:
                    return False
        return True

    complete = search(state)
    if len(solutions) >= 2:
        status, uniqueness, solution = "multiple", "multiple", None
    elif not complete:
        status, uniqueness, solution = "incomplete", "unknown", None
    elif solutions:
        status, uniqueness, solution = "solved", "unique", solutions[0]
    else:
        status, uniqueness, solution = "unsatisfiable", "none", None
    return SudokuReport(grid, status, solution, tuple(solutions), uniqueness, complete,
                        len(solutions), nodes, max_nodes, exhausted)


@dataclass(frozen=True)
class WordMatch:
    word: str
    start: tuple[int, int]
    end: tuple[int, int]
    direction: tuple[int, int]
    cells: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class WordSearchReport:
    rows: tuple[str, ...]
    words: tuple[str, ...]
    matches: tuple[WordMatch, ...]
    unmatched_words: tuple[str, ...] | None
    status: str
    search_complete: bool
    checks: int
    max_checks: int
    coordinate_system: str = "zero-based row, column"

    def to_dict(self) -> dict:
        return asdict(self)


def _word(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not 1 <= len(value) <= MAX_WORD_LENGTH or any(ch not in _ASCII for ch in value):
        raise ValueError(f"{name} must contain 1..{MAX_WORD_LENGTH} ASCII letters")
    return value.upper()


def find_words(rows: Sequence[str], words: Sequence[str], *, max_checks: int = 2_000_000) -> WordSearchReport:
    """Return every observed straight path in eight directions within budget.

    Each direction attempt and each compared cell consumes one check. Single
    letter occurrences have one direction (0, 0), avoiding eight duplicates.
    """
    _integer(max_checks, "max_checks", MAX_CHECKS)
    rows = _sequence(rows, "grid rows", MAX_GRID_CELLS)
    if not rows or any(not isinstance(row, str) or not row or any(ch not in _ASCII for ch in row) for row in rows):
        raise ValueError("grid must contain nonempty rows of ASCII letters")
    if len({len(row) for row in rows}) != 1 or sum(map(len, rows)) > MAX_GRID_CELLS:
        raise ValueError(f"grid must be rectangular and contain at most {MAX_GRID_CELLS} cells")
    rows = tuple(row.upper() for row in rows)
    words = tuple(dict.fromkeys(_word(word, "search word") for word in _sequence(words, "words", MAX_WORDS)))
    if not words:
        raise ValueError("at least one search word is required")
    height, width = len(rows), len(rows[0])
    matches: list[WordMatch] = []
    checks = 0

    def consume() -> bool:
        nonlocal checks
        if checks >= max_checks:
            return False
        checks += 1
        return True

    complete = True
    for word in words:
        for row in range(height):
            for column in range(width):
                for dr, dc in ((0, 0),) if len(word) == 1 else _DIRECTIONS:
                    if not consume():
                        complete = False
                        break
                    end_row, end_column = row + dr * (len(word) - 1), column + dc * (len(word) - 1)
                    if not (0 <= end_row < height and 0 <= end_column < width):
                        continue
                    cells = []
                    matched = True
                    for index, letter in enumerate(word):
                        if not consume():
                            complete = False
                            matched = False
                            break
                        position = row + dr * index, column + dc * index
                        if rows[position[0]][position[1]] != letter:
                            matched = False
                            break
                        cells.append(position)
                    if matched:
                        matches.append(WordMatch(word, (row, column), (end_row, end_column), (dr, dc), tuple(cells)))
                    if not complete:
                        break
                if not complete:
                    break
            if not complete:
                break
        if not complete:
            break
    found = {match.word for match in matches}
    return WordSearchReport(rows, words, tuple(matches), tuple(word for word in words if word not in found) if complete else None,
                            "complete" if complete else "incomplete", complete, checks, max_checks)


@dataclass(frozen=True)
class AnagramReport:
    normalized_text: str
    matches: tuple[str, ...]
    entries_checked: int
    max_entries: int
    search_complete: bool
    status: str
    scope: str = "Exact letter counts from supplied lexicon entries only; no generated dictionary or phrase search."

    def to_dict(self) -> dict:
        return asdict(self)


def _anagram_letters(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("anagram text and lexicon entries must be strings")
    if len(value) > 1024 or any(ch not in _ASCII and not ch.isspace() and ch not in "-'" for ch in value):
        raise ValueError("anagrams accept ASCII letters, whitespace, apostrophes, and hyphens")
    letters = "".join(ch.upper() for ch in value if ch in _ASCII)
    if not 1 <= len(letters) <= MAX_WORD_LENGTH:
        raise ValueError(f"anagram input must contain 1..{MAX_WORD_LENGTH} letters")
    return letters


def find_anagrams(text: str, lexicon: Sequence[str], *, max_entries: int = MAX_LEXICON_ENTRIES) -> AnagramReport:
    """Match complete lexicon words or supplied phrase entries by letter count."""
    _integer(max_entries, "max_entries", MAX_LEXICON_ENTRIES)
    letters = _anagram_letters(text)
    lexicon = _sequence(lexicon, "lexicon", MAX_LEXICON_ENTRIES)
    target = Counter(letters)
    matches: list[str] = []
    seen = set()
    checked = 0
    for entry in lexicon[:max_entries]:
        normalized = _anagram_letters(entry)
        checked += 1
        display = " ".join(entry.split())
        key = display.casefold()
        if Counter(normalized) == target and key not in seen:
            matches.append(display)
            seen.add(key)
    complete = checked == len(lexicon)
    return AnagramReport(letters, tuple(matches), checked, max_entries, complete,
                         "complete" if complete else "incomplete")


def _read_text(path: Path) -> str:
    with path.open("rb") as handle:
        data = handle.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"puzzle input files must not exceed {MAX_FILE_BYTES} bytes")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("puzzle input files must be UTF-8") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m engine.puzzles", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    sudoku = commands.add_parser("sudoku")
    sudoku.add_argument("grid")
    sudoku.add_argument("--max-nodes", type=int, default=100_000)
    word_search = commands.add_parser("word-search")
    word_search.add_argument("--grid-file", type=Path, required=True)
    word_search.add_argument("--words", nargs="+", required=True)
    word_search.add_argument("--max-checks", type=int, default=2_000_000)
    anagram = commands.add_parser("anagram")
    anagram.add_argument("text")
    anagram.add_argument("--lexicon", type=Path, required=True)
    anagram.add_argument("--max-entries", type=int, default=MAX_LEXICON_ENTRIES)
    args = parser.parse_args(argv)
    try:
        if args.command == "sudoku":
            report = solve_sudoku(args.grid, max_nodes=args.max_nodes)
        elif args.command == "word-search":
            rows = tuple("".join(line.split()) for line in _read_text(args.grid_file).splitlines() if line.strip())
            report = find_words(rows, args.words, max_checks=args.max_checks)
        else:
            lexicon = tuple(line.strip() for line in _read_text(args.lexicon).splitlines() if line.strip())
            report = find_anagrams(args.text, lexicon, max_entries=args.max_entries)
        print(json.dumps(report.to_dict(), ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"puzzle solver failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
