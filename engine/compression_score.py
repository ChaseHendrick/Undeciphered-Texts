"""Zlib compression / cross-entropy language score.

Natural-language strings are redundant: the same words and letter patterns
recur, so a general-purpose compressor such as zlib makes them shorter than
a character-by-character shuffle of the same string. ``language_score`` is
that compression ratio (raw UTF-8 bytes divided by compressed bytes). Higher
means more redundant. ``cross_entropy_bits_per_byte`` is the same fact as an
estimated bit rate. Lower means more predictable.

This tool does not decipher ancient scripts. It does not read Linear A, the
Voynich manuscript, Rongorongo, the Indus script, Phaistos, or any other
undeciphered writing system. A higher score is not a translation, not a
language identification, and not evidence that an unknown text has been
solved. Shuffling destroys order; beating a shuffle only shows that the
original string had compressible order.

Dieses Werkzeug entziffert keine antiken Schriften — nur ein Kompressionsmaß.
"""

from __future__ import annotations

import random
import zlib
from dataclasses import dataclass

# Kept as data so tests and callers can quote the limit without parsing prose.
DOES_NOT_DECIPHER = (
    "This tool does not decipher ancient scripts. "
    "A compression score is not a reading of Linear A, Voynich, "
    "Rongorongo, Indus, Phaistos, or any other undeciphered writing."
)

HONESTY_DE = "Dieses Werkzeug entziffert keine antiken Schriften — nur ein Kompressionsmaß."


def _utf8(text: str) -> bytes:
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return text.encode("utf-8")


def _check_level(level: int) -> int:
    if isinstance(level, bool) or not isinstance(level, int) or not 0 <= level <= 9:
        raise ValueError("zlib level must be an int from 0 to 9")
    return level


def compressed_size(text: str, *, level: int = 9) -> int:
    """Byte length of zlib.compress(text.encode('utf-8'), level)."""
    return len(zlib.compress(_utf8(text), _check_level(level)))


def cross_entropy_bits_per_byte(text: str, *, level: int = 9) -> float:
    """Zlib bit-rate estimate: 8 * compressed_bytes / raw_bytes.

    Lower means the string was more compressible. This is an upper bound on
    a crude coding rate, not a linguistic entropy and not a decipherment.
    Empty text has no rate.
    """
    raw = _utf8(text)
    if not raw:
        raise ValueError("cannot score an empty string")
    return (8.0 * compressed_size(text, level=level)) / len(raw)


def language_score(text: str, *, level: int = 9) -> float:
    """Compression ratio. Higher ranks as more language-like redundancy.

    ``len(raw) / len(zlib.compress(raw))``. A real English or German passage
    should outrank a shuffle of its own characters when the passage is long
    enough for LZ77 to see repeated phrases (a few hundred characters is
    usually enough; very short strings are dominated by the zlib header).

    This does not decipher ancient scripts.
    """
    raw = _utf8(text)
    if not raw:
        raise ValueError("cannot score an empty string")
    return len(raw) / compressed_size(text, level=level)


def shuffle_characters(text: str, *, seed: int) -> str:
    """Return a new string that is a permutation of ``text``'s characters.

    The seed fixes the permutation so a comparison can be repeated. The
    multiset of code points is unchanged, including spaces and non-ASCII
    letters. Byte order inside a code point is not shuffled separately.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    chars = list(text)
    random.Random(seed).shuffle(chars)
    return "".join(chars)


@dataclass(frozen=True)
class ShuffleComparison:
    """Original string versus one shuffled copy."""

    original_score: float
    shuffled_score: float
    original_cross_entropy: float
    shuffled_cross_entropy: float
    seed: int

    @property
    def original_ranks_above(self) -> bool:
        """True when the original is strictly more compressible than the shuffle."""
        return self.original_score > self.shuffled_score


def compare_to_shuffle(text: str, *, seed: int = 0, level: int = 9) -> ShuffleComparison:
    """Score ``text`` and one character-shuffle of itself.

    Ranking is by ``language_score`` (higher is more redundant). The cross
    entropy fields move the other way: a more redundant string has a lower
    bit-rate estimate. Neither number deciphers an ancient script.
    """
    shuffled = shuffle_characters(text, seed=seed)
    return ShuffleComparison(
        original_score=language_score(text, level=level),
        shuffled_score=language_score(shuffled, level=level),
        original_cross_entropy=cross_entropy_bits_per_byte(text, level=level),
        shuffled_cross_entropy=cross_entropy_bits_per_byte(shuffled, level=level),
        seed=seed,
    )
