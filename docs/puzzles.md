# General puzzle tools

`engine.puzzles` provides a standard-library Sudoku solver, rectangular word search, and anagrams drawn from a supplied lexicon. The tools return structured JSON with explicit bounds and completion status. They do not claim to solve arbitrary puzzles or historical undeciphered texts.

## Sudoku

```sh
python3 -m engine.puzzles sudoku '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......' --max-nodes 10000
```

Python callers use `solve_sudoku(grid, max_nodes=100000)`. The grid contains exactly 81 row-major cells. Digits 1 through 9 are givens; `0` or `.` are blanks. Whitespace and `|+-` display separators are accepted. Unexpected characters fail validation, rather than silently becoming blanks. Formatted input is limited to 4,096 characters.

The solver repeatedly propagates singleton candidates and digits with only one possible position in a row, column, or box. It branches on the cell with the fewest remaining candidates and tries digits in numerical order. Root and branch visits each consume one node before propagation. Propagation only removes candidates in a fixed 81-cell state. Direct duplicate givens can be rejected without search. The node budget is an integer from 0 through 1,000,000; zero records an incomplete search for a grid without a direct duplicate contradiction.

Reports distinguish these outcomes:

- `solved`: exhaustive search found exactly one completion; `uniqueness` is `unique` and `solution` contains it.
- `multiple`: two distinct valid completions establish nonuniqueness; search stops and `solution` is null. Both witnesses appear in `solutions`.
- `unsatisfiable`: a direct contradiction or exhaustive search established no completion.
- `incomplete`: the node budget was exhausted. `uniqueness` is `unknown` and `solution` is null, even if `solutions` contains a discovered completion.

`search_complete` means the search tree was exhausted. It is false when two witnesses prove nonuniqueness without exploring every branch. `exhausted` specifically identifies budget exhaustion. The reported solution count is a lower bound; the solver stores at most two witnesses.

The algorithm and two independent known-answer fixtures come from [Peter Norvig's official Sudoku article](https://www.norvig.com/sudoku.html). The first example shown there is recovered exactly, and its uniqueness search takes 101 nodes in this implementation. Norvig's `grid1` is completed through propagation in one root node. [The certificate](../engine/data/puzzle_certificate.json) records literal input grids, literal displayed answers, and SHA-256 over 81 ASCII solution digits without whitespace. Tests independently check every row, column, box, and given clue. The result supports those examples and the bounded solver contract; it is not a timing guarantee for all Sudoku grids.

## Word search

Save one grid row per line. CLI input ignores whitespace between letters and empty lines:

```sh
python3 -m engine.puzzles word-search --grid-file /path/to/grid.txt --words ORBIT SPACE NOVA --max-checks 2000000
```

Python callers use `find_words(rows, words, max_checks=2000000)` with nonempty, equal-length ASCII-letter row strings. Grid and words are compared in uppercase. Matching covers horizontal, vertical, and both diagonal orientations, including reversed directions. Every observed occurrence is returned with zero-based `(row, column)` start/end positions, direction, and path cells. Repeated supplied words are deduplicated. A one-letter occurrence is returned once with direction `(0, 0)`. A palindromic word may have distinct forward and reverse paths, which are both returned.

Limits are 10,000 grid cells, 1,000 requested words, 256 letters per word, and a check budget from 0 through 10,000,000. Each direction attempt and cell comparison consumes one check. A completed search returns all matches and `unmatched_words`. Budget exhaustion returns only observed matches, `status: incomplete`, and `unmatched_words: null`, because absence has not been established. The default budget may be insufficient for the largest allowed input.

## Supplied-lexicon anagrams

Use a UTF-8 file with one word or phrase entry per line:

```sh
python3 -m engine.puzzles anagram 'listen' --lexicon /path/to/words.txt --max-entries 100000
```

Python callers use `find_anagrams(text, lexicon, max_entries=100000)`. There is no default dictionary. An entry matches only when its complete letter counts equal the input's counts. Matching uses uppercase ASCII letters and ignores whitespace, apostrophes, and hyphens. Unexpected characters and non-ASCII letters are rejected. Returned entries retain their supplied spelling with whitespace collapsed. Case-insensitive duplicate entries are returned once. A supplied phrase such as `dirty room` can match `Dormitory`; the tool does not generate combinations of dictionary words.

Input and entries contain 1 through 256 letters and at most 1,024 total characters each. The supplied sequence has at most 100,000 entries. The scan budget is 0 through 100,000 entries. A shorter scan reports `incomplete`; no match only establishes absence if `search_complete` is true. CLI grid and lexicon files are UTF-8 and limited to 2 MiB. CLI commands return JSON and exit 0 for completed or bounded incomplete reports; invalid input exits 2. Inspect `status` and `search_complete` when automating them.

```sh
python3 -m unittest tests.test_puzzles -v
```

These helpers follow [QUALITY.md](QUALITY.md) and [TESTING.md](TESTING.md). They are standalone tools outside the language-cipher routing registry. Their certificate uses puzzle-specific fields so the neural router does not mistake Sudoku grids for natural-language ciphertext.
