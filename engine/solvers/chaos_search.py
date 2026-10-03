"""Chaotic random search over a Caesar shift or a short substitution.

The search starts from a random Caesar shift. Each step mutates that shift
or replaces it with a short substitution (the same shift plus one to three
ciphertext letter overrides). A candidate is kept when its English quadgram
score beats a fixed per-letter threshold. The caller then checks that the
recovered text matches a known plaintext. The key is never an input.

Random search solved the repository Caesar certificate only: the known
fixture in engine/data/caesar_certificate.json. It did not solve army
message Nr. 86, Kryptos K4, or an unknown script.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from engine.alphabet import from_ints, letters_only, reinject, to_ints
from engine.language import get_model
from engine.result import SolveResult

# Fixed seed used by the unit test. The walk is deterministic for this value.
CHAOS_SEED = 20261002

# Quadgram log score per letter. On the Caesar certificate only shift 11
# clears this bar (about -2.01). The next best shift is about -3.77.
SCORE_THRESHOLD_PER_LETTER = -2.5

MAX_TRIALS = 4000
SHORT_SUB_MIN = 1
SHORT_SUB_MAX = 3

_SCOPE = (
    "Random search solved this known Caesar certificate example only. "
    "It did not solve army message Nr. 86, Kryptos K4, or an unknown script."
)


@dataclass(frozen=True)
class ChaosCandidate:
    """One search state: a pure shift, or that shift plus a few overrides."""

    kind: str
    shift: int
    overrides: tuple[tuple[int, int], ...]


def mutate_candidate(rng: random.Random, current: ChaosCandidate) -> ChaosCandidate:
    """Randomly mutate a Caesar shift or build a short substitution.

    A short substitution keeps the current shift and overrides at most three
    ciphertext letters. It is not a full 26-letter key search.
    """
    if rng.randrange(2) == 0:
        if rng.random() < 0.45:
            shift = rng.randrange(26)
        else:
            step = rng.choice((-4, -3, -2, -1, 1, 2, 3, 4))
            shift = (current.shift + step) % 26
        return ChaosCandidate("caesar", shift, ())

    width = rng.randint(SHORT_SUB_MIN, SHORT_SUB_MAX)
    chosen = rng.sample(range(26), width)
    overrides = tuple(sorted((cipher, rng.randrange(26)) for cipher in chosen))
    return ChaosCandidate("short_substitution", current.shift, overrides)


def _decode(seq: list[int], candidate: ChaosCandidate) -> list[int]:
    if candidate.kind == "caesar":
        shift = candidate.shift
        return [(cipher - shift) % 26 for cipher in seq]
    overrides = dict(candidate.overrides)
    shift = candidate.shift
    plain: list[int] = []
    for cipher in seq:
        if cipher in overrides:
            plain.append(overrides[cipher])
        else:
            plain.append((cipher - shift) % 26)
    return plain


def _pure_shift(seq: list[int], plain: list[int]) -> int | None:
    if not seq:
        return None
    shift = (seq[0] - plain[0]) % 26
    for cipher, letter in zip(seq, plain):
        if (cipher - letter) % 26 != shift:
            return None
    return shift


def solve_chaos_search(
    text: str,
    seed: int = CHAOS_SEED,
    threshold_per_letter: float = SCORE_THRESHOLD_PER_LETTER,
    max_trials: int = MAX_TRIALS,
) -> SolveResult:
    """Search until an English score beats the threshold.

    ``seed`` fixes the random walk. Do not pass a key. After this returns,
    compare ``plaintext`` with the known fixture. A score above the threshold
    is not a reading of an unknown script.
    """
    letters = letters_only(text)
    if len(letters) < 4:
        raise ValueError("ciphertext needs at least 4 letters")
    if max_trials < 1:
        raise ValueError("max_trials must be at least 1")

    seq = to_ints(letters)
    model = get_model()
    rng = random.Random(seed)
    current = ChaosCandidate("caesar", rng.randrange(26), ())
    caesar_mutations = 0
    short_mutations = 0

    for trial in range(1, max_trials + 1):
        current = mutate_candidate(rng, current)
        if current.kind == "caesar":
            caesar_mutations += 1
        else:
            short_mutations += 1
            if len(current.overrides) < SHORT_SUB_MIN or len(current.overrides) > SHORT_SUB_MAX:
                raise RuntimeError("short substitution width drifted outside 1..3")
        plain = _decode(seq, current)
        score = model.score(plain)
        per_letter = score / len(seq)
        if per_letter < threshold_per_letter:
            continue
        shift = _pure_shift(seq, plain)
        rendered = reinject(text, from_ints(plain))
        if shift is None:
            key = "short_substitution"
            found_kind = "short_substitution"
        else:
            key = str(shift)
            found_kind = "caesar"
        return SolveResult(
            method="chaos_search",
            plaintext=rendered,
            key=key,
            score=score,
            details={
                "seed": seed,
                "trials": trial,
                "found_kind": found_kind,
                "shift": shift,
                "score_per_letter": round(per_letter, 4),
                "threshold_per_letter": threshold_per_letter,
                "caesar_mutations": caesar_mutations,
                "short_substitution_mutations": short_mutations,
                "letters": len(seq),
                "scope": _SCOPE,
            },
        )

    raise RuntimeError(
        "chaotic random search did not beat the English score threshold "
        "on this ciphertext"
    )
