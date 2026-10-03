"""German letter-frequency and quadgram fitness, fit on one public-domain excerpt.

The sample is the opening of Grimm, "Der Froschkönig oder der eiserne Heinrich"
(Project Gutenberg eBook #77905). It is not the Truppenschlüssel ciphertext and
not a proposed plaintext. Umlauts are folded into A–Z (ä→ae, ö→oe, ü→ue, ß→ss)
before counts are taken, so the model is a 26-letter Latin scorer, not a full
German orthography model.

Unigram rates are the smoothed letter counts of that excerpt. Quadgram scores
are the same backoff log-likelihood as engine.language.LanguageModel, fit on
the folded excerpt rather than on English. A higher score means the letters
look more like that fairy-tale sample. It is not a decipherment.
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

from engine.alphabet import to_ints
from engine.language import LanguageModel

_DATA = Path(__file__).resolve().parent / "data" / "german_excerpt.txt"

# Logged failed outputs for Funkspruch Nr. 86 (FBOIQ), 3 July 1941.
# Copied from docs/logs/attempt-2026-10-02.md. These are score dumps from an
# English Caesar, Vigenère, and substitution search. They are not plaintext.
TRUPPENSCHLUESSEL_NR86 = "FBOIQPMWRLVNREKEXXMBRWMAMRUIHEHCSHERBUZIIMLOUQ"
FAILED_NR86_APPROACHES = (
    ("caesar", "BXKEMLISNHRJNAGATTIXNSIWINQEDADYODANXQVEEIHKQM"),
    ("vigenere", "AIVILWTWMSCNMLRESETBMDTAHYBICLOCNOLRWBGIDTSOPX"),
    ("substitution", "QNPRDJOFTUGHTACALLONTFOXOTERSASKYSATNEIRROUPED"),
)

_FOLD = str.maketrans(
    {
        "Ä": "AE",
        "Ö": "OE",
        "Ü": "UE",
        "ä": "AE",
        "ö": "OE",
        "ü": "UE",
        "ß": "SS",
    }
)


def load_training_prose(path: Path | None = None) -> str:
    """Return the excerpt, skipping leading '#' attribution lines."""
    raw = (path or _DATA).read_text(encoding="utf-8")
    lines = [line for line in raw.splitlines() if not line.startswith("#")]
    return "\n".join(lines).strip()


def german_letters(text: str) -> str:
    """Fold German spelling into an A–Z stream. Non-letters are dropped."""
    folded = text.translate(_FOLD)
    return "".join(ch for ch in folded.upper() if "A" <= ch <= "Z")


class GermanModel:
    """Unigram rates and quadgram log-likelihood from one German excerpt."""

    def __init__(self, prose: str, alpha: float = 0.5) -> None:
        letters = german_letters(prose)
        if len(letters) < 80:
            raise ValueError("German sample is too short to fit a letter model")
        self.training_letters = letters
        observed = [0] * 26
        for ch in letters:
            observed[ord(ch) - 65] += 1
        total = sum(observed)
        self.unigram = tuple((observed[i] + alpha) / (total + 26 * alpha) for i in range(26))
        self.log_unigram = tuple(math.log(p) for p in self.unigram)
        self.quadgrams = LanguageModel(letters)
        self.sample_letters = len(letters)

    def unigram_score(self, seq: list[int]) -> float:
        """Sum of log unigram probabilities. Higher is more like the excerpt."""
        total = 0.0
        logp = self.log_unigram
        for idx in seq:
            total += logp[idx]
        return total

    def chi_square(self, seq: list[int]) -> float:
        """Pearson chi-square against the excerpt unigrams. Lower is closer."""
        n = len(seq)
        if n == 0:
            return 0.0
        observed = [0] * 26
        for idx in seq:
            observed[idx] += 1
        score = 0.0
        for i in range(26):
            expected = self.unigram[i] * n
            diff = observed[i] - expected
            score += (diff * diff) / expected
        return score

    def quadgram_score(self, seq: list[int]) -> float:
        """Sum of backoff quadgram log-probabilities. Higher is better."""
        n = len(seq)
        if n < 4:
            return self.unigram_score(seq)
        return self.quadgrams.score(seq)

    def mean_quadgram(self, seq: list[int]) -> float:
        """Per-step quadgram log-probability, so different lengths can be compared."""
        n = len(seq)
        if n < 4:
            if n == 0:
                return 0.0
            return self.unigram_score(seq) / n
        return self.quadgram_score(seq) / (n - 3)

    def score_text(self, text: str) -> float:
        return self.quadgram_score(to_ints(german_letters(text)))


def score_failed_nr86(model: GermanModel | None = None) -> list[dict[str, float | str | int]]:
    """Score the logged Nr. 86 failures. Does not propose a German reading."""
    fitted = model or get_german_model()
    rows: list[dict[str, float | str | int]] = []
    streams = (("ciphertext", TRUPPENSCHLUESSEL_NR86),) + FAILED_NR86_APPROACHES
    for name, text in streams:
        seq = to_ints(german_letters(text))
        rows.append(
            {
                "name": name,
                "letters": len(seq),
                "quadgram": fitted.quadgram_score(seq),
                "mean_quadgram": fitted.mean_quadgram(seq),
                "unigram": fitted.unigram_score(seq),
                "chi_square": fitted.chi_square(seq),
            }
        )
    return rows


@lru_cache(maxsize=1)
def get_german_model() -> GermanModel:
    return GermanModel(load_training_prose())
