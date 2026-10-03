"""Unknown-script analysis helpers: inventory, repeats, bilingual crib check.

These tools measure a transcribed sign corpus. They do not decipher Linear A,
the Voynich manuscript, Rongorongo, Indus, or any other undeciphered script.
A high-frequency sign or a crib match is a measurement against the inputs you
supplied, not a reading of an ancient language.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

DATA_DIR = Path(__file__).resolve().parent / "data"
SYNTHETIC_CORPUS_PATH = DATA_DIR / "synthetic_sign_corpus.txt"
SYNTHETIC_BILINGUAL_PATH = DATA_DIR / "synthetic_bilingual.json"


def tokenize_signs(text: str) -> list[str]:
    """Split a transcription into sign tokens.

    Whitespace and commas separate signs. Empty tokens are dropped. Lines that
    start with '#' are comments. This is for already-transcribed corpora, not
    for pixels or photographs.
    """
    signs: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        for piece in line.replace(",", " ").split():
            if piece:
                signs.append(piece)
    return signs


def load_sign_corpus(path: Path | str | None = None) -> list[str]:
    """Load a whitespace-tokenized sign corpus from disk."""
    target = Path(path) if path is not None else SYNTHETIC_CORPUS_PATH
    return tokenize_signs(target.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class SignInventory:
    """Frequency table for a sign corpus."""

    total: int
    counts: tuple[tuple[str, int], ...]
    unique: int

    def frequency(self, sign: str) -> float:
        if self.total == 0:
            return 0.0
        lookup = dict(self.counts)
        return lookup.get(sign, 0) / self.total

    def as_dict(self) -> dict[str, int]:
        return dict(self.counts)


def sign_inventory(signs: Sequence[str]) -> SignInventory:
    """Count each distinct sign and rank by frequency descending."""
    bag: Counter[str] = Counter(signs)
    ranked = tuple(sorted(bag.items(), key=lambda item: (-item[1], item[0])))
    return SignInventory(total=sum(bag.values()), counts=ranked, unique=len(bag))


@dataclass(frozen=True)
class RepeatedSequence:
    """One n-sign sequence that appears more than once."""

    sequence: tuple[str, ...]
    count: int
    positions: tuple[int, ...]

    @property
    def text(self) -> str:
        return " ".join(self.sequence)


def find_repeated_sequences(
    signs: Sequence[str],
    *,
    min_length: int = 2,
    max_length: int = 4,
    min_count: int = 2,
) -> list[RepeatedSequence]:
    """Find sign n-grams that repeat at least ``min_count`` times.

    Positions are starting indices in the flat sign stream. Results are sorted
    by count descending, then by length descending, then by text.
    """
    if min_length < 1 or max_length < min_length or min_count < 2:
        return []
    n = len(signs)
    found: list[RepeatedSequence] = []
    for size in range(min_length, max_length + 1):
        if n < size:
            continue
        positions: dict[tuple[str, ...], list[int]] = {}
        for i in range(n - size + 1):
            gram = tuple(signs[i : i + size])
            positions.setdefault(gram, []).append(i)
        for gram, pos in positions.items():
            if len(pos) >= min_count:
                found.append(
                    RepeatedSequence(
                        sequence=gram,
                        count=len(pos),
                        positions=tuple(pos),
                    )
                )
    found.sort(key=lambda item: (-item.count, -len(item.sequence), item.text))
    return found


@dataclass(frozen=True)
class CribMatch:
    """One proposed reading checked against a known word list."""

    signs: tuple[str, ...]
    reading: str
    matched: bool
    reason: str


@dataclass(frozen=True)
class CribReport:
    """Summary of a bilingual crib check."""

    matches: tuple[CribMatch, ...]
    mismatches: tuple[CribMatch, ...]
    skipped: tuple[CribMatch, ...]

    @property
    def match_count(self) -> int:
        return len(self.matches)

    @property
    def mismatch_count(self) -> int:
        return len(self.mismatches)

    @property
    def all_matched(self) -> bool:
        return self.mismatch_count == 0 and self.match_count > 0


def apply_sign_map(signs: Sequence[str], sign_to_sound: Mapping[str, str]) -> str | None:
    """Concatenate sound values for each sign. Return None if any sign is unmapped."""
    parts: list[str] = []
    for sign in signs:
        sound = sign_to_sound.get(sign)
        if sound is None:
            return None
        parts.append(sound)
    return "".join(parts)


def check_bilingual_crib(
    entries: Iterable[Sequence[str]],
    sign_to_sound: Mapping[str, str],
    known_words: Iterable[str],
    *,
    normalize: bool = True,
) -> CribReport:
    """Score a proposed sign-to-sound map against a known word list.

    Each entry is a sign sequence believed to write one word. The map turns
    that sequence into a reading. Readings that land in ``known_words`` are
    matches; complete readings that do not are mismatches; sequences with an
    unmapped sign are skipped.

    This checks consistency with the word list you supply. It does not prove
    that the map is historically correct, and it does not read Linear A or
    Voynich.
    """
    lexicon = {
        (w.casefold() if normalize else w)
        for w in known_words
        if w is not None and str(w).strip() != ""
    }
    matches: list[CribMatch] = []
    mismatches: list[CribMatch] = []
    skipped: list[CribMatch] = []
    for entry in entries:
        signs = tuple(entry)
        reading = apply_sign_map(signs, sign_to_sound)
        if reading is None:
            skipped.append(
                CribMatch(
                    signs=signs,
                    reading="",
                    matched=False,
                    reason="unmapped_sign",
                )
            )
            continue
        key = reading.casefold() if normalize else reading
        if key in lexicon:
            matches.append(
                CribMatch(signs=signs, reading=reading, matched=True, reason="in_lexicon")
            )
        else:
            mismatches.append(
                CribMatch(
                    signs=signs,
                    reading=reading,
                    matched=False,
                    reason="not_in_lexicon",
                )
            )
    return CribReport(
        matches=tuple(matches),
        mismatches=tuple(mismatches),
        skipped=tuple(skipped),
    )


def load_synthetic_bilingual(path: Path | str | None = None) -> dict:
    """Load the tiny synthetic bilingual fixture (JSON)."""
    import json

    target = Path(path) if path is not None else SYNTHETIC_BILINGUAL_PATH
    return json.loads(target.read_text(encoding="utf-8"))
