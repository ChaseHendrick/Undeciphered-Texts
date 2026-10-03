"""Shannon unicity lower bound for a sign-to-sign mapping.

Given an alphabet size, a text length, and a language-model entropy you
state in bits per symbol, this estimates whether the corpus is too short
to uniquely determine a random bijection (a simple substitution key).

The named bound is Shannon's unicity distance, U = H(K) / D, from
C. E. Shannon, "Communication Theory of Secrecy Systems," Bell System
Technical Journal 28(4): 656-715, 1949:

https://www.cs.virginia.edu/~evans/greatworks/shannon1949.pdf

H(K) = log2(alphabet_size!) is the entropy of a uniformly random
bijection. D = log2(alphabet_size) - entropy is the redundancy of the
stated model, in bits per symbol. The ratio does not depend on the log
base. Shannon's own English illustration uses about 0.7 decimal digits
of redundancy per letter and finds unicity near 30 letters for simple
substitution; the same quotient is computed here in bits.

This is a bound, not a decipherment. It does not read Linear A, the
Indus script, or any other ancient writing. It does not search mappings
or assign values. "possibly determined" means only that, under the
entropy you stated, the corpus is at least as long as this unicity
distance. A shorter corpus is "underdetermined": the random-cipher
argument expects more than one key of non-negligible probability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

SHANNON_UNICITY_URL = (
    "https://www.cs.virginia.edu/~evans/greatworks/shannon1949.pdf"
)

UNDERDETERMINED = "underdetermined"
POSSIBLY_DETERMINED = "possibly determined"


def _check_alphabet(alphabet_size: int) -> None:
    if isinstance(alphabet_size, bool) or not isinstance(alphabet_size, int):
        raise TypeError("alphabet_size must be an int")
    if alphabet_size < 2:
        raise ValueError("alphabet_size must be at least 2")


def _check_length(text_length: int) -> None:
    if isinstance(text_length, bool) or not isinstance(text_length, int):
        raise TypeError("text_length must be an int")
    if text_length < 0:
        raise ValueError("text_length must be >= 0")


def _check_entropy(alphabet_size: int, entropy_bits_per_symbol: float) -> float:
    if isinstance(entropy_bits_per_symbol, bool) or not isinstance(
        entropy_bits_per_symbol, (int, float)
    ):
        raise TypeError("entropy_bits_per_symbol must be a real number")
    entropy = float(entropy_bits_per_symbol)
    if entropy < 0.0 or not math.isfinite(entropy):
        raise ValueError("entropy_bits_per_symbol must be finite and >= 0")
    capacity = math.log2(alphabet_size)
    # Allow a hair of float noise when the caller passes log2(alphabet).
    if entropy > capacity + 1e-9:
        raise ValueError(
            "entropy_bits_per_symbol exceeds log2(alphabet_size)"
        )
    if entropy > capacity:
        entropy = capacity
    return entropy


def key_entropy_bits(alphabet_size: int) -> float:
    """log2(n!) for a uniformly random bijection on n signs.

    This is H(K) in Shannon's simple-substitution example, where every
    permutation is equally likely. It is not a measured key.
    """
    _check_alphabet(alphabet_size)
    return math.lgamma(alphabet_size + 1) / math.log(2)


def redundancy_bits_per_symbol(
    alphabet_size: int, entropy_bits_per_symbol: float
) -> float:
    """D = log2(|A|) - H, the stated model's redundancy in bits per symbol."""
    _check_alphabet(alphabet_size)
    entropy = _check_entropy(alphabet_size, entropy_bits_per_symbol)
    return math.log2(alphabet_size) - entropy


def unicity_distance_symbols(
    alphabet_size: int, entropy_bits_per_symbol: float
) -> float:
    """Shannon unicity distance U = H(K) / D, in symbols.

    Returns math.inf when the stated entropy leaves no positive
    redundancy. In that case the random-cipher argument never reaches a
    unique key, which is Shannon's ideal system, not a reading.
    """
    redundancy = redundancy_bits_per_symbol(
        alphabet_size, entropy_bits_per_symbol
    )
    if redundancy <= 0.0:
        return math.inf
    return key_entropy_bits(alphabet_size) / redundancy


@dataclass(frozen=True)
class SignMappingBound:
    """A unicity-distance comparison. Not a proposed sign reading."""

    alphabet_size: int
    text_length: int
    entropy_bits_per_symbol: float
    key_entropy_bits: float
    redundancy_bits_per_symbol: float
    lower_bound_symbols: float
    verdict: str
    source_url: str = SHANNON_UNICITY_URL

    @property
    def underdetermined(self) -> bool:
        return self.verdict == UNDERDETERMINED


def estimate_sign_mapping(
    alphabet_size: int,
    text_length: int,
    entropy_bits_per_symbol: float,
) -> SignMappingBound:
    """Compare text length with Shannon's unicity distance.

    ``entropy_bits_per_symbol`` is an assumption you state. It is not
    estimated from the corpus. The lower bound is the unicity distance
    in symbols. The verdict is ``underdetermined`` when the text is
    strictly shorter than that distance, and ``possibly determined``
    when the text meets or exceeds it.

    ``possibly determined`` is not a decipherment of Linear A or Indus.
    """
    _check_alphabet(alphabet_size)
    _check_length(text_length)
    entropy = _check_entropy(alphabet_size, entropy_bits_per_symbol)
    redundancy = math.log2(alphabet_size) - entropy
    key_entropy = key_entropy_bits(alphabet_size)
    if redundancy <= 0.0:
        lower_bound = math.inf
    else:
        lower_bound = key_entropy / redundancy
    if text_length < lower_bound:
        verdict = UNDERDETERMINED
    else:
        verdict = POSSIBLY_DETERMINED
    return SignMappingBound(
        alphabet_size=alphabet_size,
        text_length=text_length,
        entropy_bits_per_symbol=entropy,
        key_entropy_bits=key_entropy,
        redundancy_bits_per_symbol=redundancy,
        lower_bound_symbols=lower_bound,
        verdict=verdict,
    )
