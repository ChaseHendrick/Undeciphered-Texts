"""ACA Checkerboard: supplied Polybius square and row/column homophones.

Primary source: https://www.cryptogram.org/downloads/aca.info/ciphers/Checkerboard.pdf
This is the two-coordinate construction, distinct from straddling checkerboard.
"""
from __future__ import annotations

from collections.abc import Sequence
import string
from engine.result import SolveResult

SOURCE_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Checkerboard.pdf"
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
MAX_LETTERS = 4096


def _letters(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("plaintext and square must be strings")
    if len(text) > 16384:
        raise ValueError("letter input exceeds 16384 raw characters")
    if any(ch not in string.ascii_letters + string.whitespace + string.punctuation for ch in text):
        raise ValueError("letter input must use ASCII letters, spaces or punctuation, without digits")
    letters = "".join(ch.upper() for ch in text if ch in string.ascii_letters).replace("J", "I")
    if not 1 <= len(letters) <= MAX_LETTERS:
        raise ValueError("letter input must contain 1..4096 letters")
    return letters


def _labels(value: Sequence[str], name: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be a finite sequence of one or two label strings")
    if not 1 <= len(value) <= 2:
        raise ValueError(f"{name} must contain one or two five-character labels")
    if any(not isinstance(label, str) or len(label) != 5 or
           any(ch not in string.ascii_letters + string.digits for ch in label) for label in value):
        raise ValueError(f"{name} must use five ASCII letters or digits per label")
    labels = tuple(label.upper() for label in value)
    if len(set("".join(labels))) != 5 * len(labels):
        raise ValueError(f"{name} characters must be unique across that coordinate axis")
    return labels


def _board(square: str, row_labels: Sequence[str], column_labels: Sequence[str]):
    cells = _letters(square)
    if len(cells) != 25 or set(cells) != set(ALPHABET):
        raise ValueError("square must contain each of the 25 I/J-merged letters exactly once")
    rows = _labels(row_labels, "row_labels")
    columns = _labels(column_labels, "column_labels")
    return cells, rows, columns


def checkerboard_encrypt(text: str, *, square: str, row_labels: Sequence[str],
                         column_labels: Sequence[str], choices: Sequence[Sequence[int]] | None = None) -> str:
    """Encode row then column, using supplied per-letter homophone selections."""
    cells, rows, columns = _board(square, row_labels, column_labels)
    plain = _letters(text)
    if choices is None:
        selections = ((0, 0),) * len(plain)
    elif isinstance(choices, Sequence) and not isinstance(choices, (str, bytes, bytearray)):
        if len(choices) != len(plain):
            raise ValueError("choices must provide one row/column label selection per plaintext letter")
        selections = choices
    else:
        raise TypeError("choices must be a finite sequence of row/column index pairs")
    positions = {letter: divmod(index, 5) for index, letter in enumerate(cells)}
    output = []
    for letter, selection in zip(plain, selections):
        if not isinstance(selection, Sequence) or isinstance(selection, (str, bytes, bytearray)) or len(selection) != 2:
            raise ValueError("each choice must contain two label indices")
        r_choice, c_choice = selection
        if any(not isinstance(index, int) or isinstance(index, bool) for index in selection):
            raise TypeError("label choice indices must be integers")
        if not 0 <= r_choice < len(rows) or not 0 <= c_choice < len(columns):
            raise ValueError("choice exceeds the supplied label alternatives")
        row, column = positions[letter]
        output.append(rows[r_choice][row] + columns[c_choice][column])
    return "".join(output)


def checkerboard_decrypt(text: str, *, square: str, row_labels: Sequence[str],
                         column_labels: Sequence[str], terminal_period: bool = False) -> str:
    """Decode explicit coordinate pairs; grouping whitespace carries no words."""
    cells, rows, columns = _board(square, row_labels, column_labels)
    if not isinstance(text, str):
        raise TypeError("ciphertext must be a string")
    if not isinstance(terminal_period, bool):
        raise TypeError("terminal_period must be Boolean")
    if len(text) > 32768:
        raise ValueError("ciphertext exceeds 32768 raw characters")
    body = text.strip()
    if terminal_period and body.endswith("."):
        body = body[:-1]
    if any(ch not in string.ascii_letters + string.digits + string.whitespace for ch in body):
        raise ValueError("ciphertext must use ASCII coordinate characters and whitespace")
    stream = "".join(ch.upper() for ch in body if not ch.isspace())
    if not stream or len(stream) % 2 or len(stream) > 2 * MAX_LETTERS:
        raise ValueError("ciphertext must contain 1..4096 complete coordinate pairs")
    row_positions = {char: index for label in rows for index, char in enumerate(label)}
    column_positions = {char: index for label in columns for index, char in enumerate(label)}
    output = []
    for index in range(0, len(stream), 2):
        row, column = stream[index:index + 2]
        if row not in row_positions or column not in column_positions:
            raise ValueError("coordinate is absent from its row or column labels")
        output.append(cells[5 * row_positions[row] + column_positions[column]])
    return "".join(output)


def solve_checkerboard(text: str, *, square: str, row_labels: Sequence[str],
                       column_labels: Sequence[str], terminal_period: bool = False) -> SolveResult:
    plain = checkerboard_decrypt(text, square=square, row_labels=row_labels,
                                column_labels=column_labels, terminal_period=terminal_period)
    cells, rows, columns = _board(square, row_labels, column_labels)
    return SolveResult("checkerboard", plain, cells, float(len(plain)),
                       {"mode": "supplied_key", "row_labels": rows, "column_labels": columns,
                        "lost_word_spaces": True, "letter_merges": {"J": "I"},
                        "source_url": SOURCE_URL,
                        "scope": "Supplied square and coordinate labels only; no unknown-key or historical decipherment claim."})
