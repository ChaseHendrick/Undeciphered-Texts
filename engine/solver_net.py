"""Route ciphertext to a certified solver and record why.

A small kernel classifier reads features of a Latin-letter ciphertext
(index of coincidence, digraph repeats, an ADFGVX alphabet check, even
length, and a few related counts) and picks one solver family already
certified on main. The decision is a causal link: the solver, the features
that favored it, and the certificate that link then checks.

Training uses the standard library only. Numpy is not required.

This routes known ciphers. It does not decipher Kryptos K4, army message
Nr. 86, Linear A, the Indus script, the Voynich manuscript, or rongorongo.
Unknown scripts stay unread.
"""

from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from engine.alphabet import letters_only
from engine.language import LOG_UNIGRAM, chi_square
from engine.result import SolveResult
from engine.stats import index_of_coincidence

_DATA = Path(__file__).resolve().parent / "data"
_PROSE = _DATA / "english.txt"

# Kernel width on z-scored features. Large enough that an exact certified
# exemplar wins its class, small enough that nearby synthetic samples still vote.
GAMMA = 0.40
SEED = 20261002
SAMPLES_PER_CLASS = 21

SCOPE = (
    "Routes a known Latin-letter cipher to a certified solver. "
    "Does not decipher Kryptos K4, army message Nr. 86, Linear A, "
    "the Indus script, the Voynich manuscript, or rongorongo. "
    "Unknown scripts stay unread."
)

UNREAD_SCRIPTS = {
    "k4": "Kryptos K4",
    "kryptos k4": "Kryptos K4",
    "kryptos-k4": "Kryptos K4",
    "nr. 86": "army message Nr. 86",
    "nr 86": "army message Nr. 86",
    "nr86": "army message Nr. 86",
    "army message nr. 86": "army message Nr. 86",
    "linear a": "Linear A",
    "indus": "the Indus script",
    "indus script": "the Indus script",
    "voynich": "the Voynich manuscript",
    "voynich manuscript": "the Voynich manuscript",
    "rongorongo": "rongorongo",
}

FEATURE_NAMES = (
    "index_of_coincidence",
    "adfgvx_alphabet_ratio",
    "pure_adfgvx_alphabet",
    "alphabet_coverage",
    "even_length",
    "space_ratio",
    "digit_ratio",
    "contains_j",
    "chi_square_shift0",
    "chi_square_best_shift",
    "chi_square_gap",
    "digraph_repeat_rate",
    "pair_repeat_rate",
    "double_letter_rate",
    "vowel_ratio",
    "top_letter_ratio",
    "letter_entropy",
    "column_unigram_fitness",
    "log_length",
)

_ADFGVX = set("ADFGVX")
_VOWELS = set("AEIOU")

# Solvers the feature net chooses among. Crib shares the Vigenère ciphertext
# exactly, so it is linked as a related solver rather than a second class.
# Beam search is its own class because its certificate ciphertext differs.
ROUTED_SOLVERS = (
    "caesar",
    "vigenere",
    "keyed-vigenere",
    "substitution",
    "playfair",
    "bifid",
    "adfgvx",
    "columnar",
    "two-square",
    "beam-search",
    "lumen-braid",
    "prism-latch",
)

# Every certified solver the router knows, including ones that share a family.
KNOWN_SOLVERS = ROUTED_SOLVERS[:9] + ("crib", "beam-search", "lumen-braid", "prism-latch")

RELATED_SOLVERS = {
    "vigenere": ("crib",),
    "substitution": ("beam-search",),
}

_KEYS = (
    "HARBOR",
    "CANAL",
    "PAPER",
    "NIGHT",
    "QUAY",
    "TIDE",
    "RIVER",
    "STONE",
    "LAMP",
    "BELL",
    "DAWN",
    "MIST",
    "GOLD",
    "CASTLE",
    "PRIVACY",
    "EXAMPLE",
    "CIPHER",
)
_ALPHABETS = ("KRYPTOS", "CIPHER", "PALACE", "QUARTZ", "BRIDGE")


@dataclass(frozen=True)
class SolverLink:
    """One certified solver and the certificate a routed decision checks."""

    solver: str
    family: str
    certificate_id: str
    summary: str


SOLVER_CATALOG: dict[str, SolverLink] = {
    "caesar": SolverLink(
        "caesar",
        "caesar",
        "caesar_certificate.json",
        "26-shift Caesar search by English unigram score",
    ),
    "vigenere": SolverLink(
        "vigenere",
        "vigenere",
        "vigenere_certificate.json",
        "Kasiski and column search for a standard Vigenère key",
    ),
    "keyed-vigenere": SolverLink(
        "keyed-vigenere",
        "keyed-vigenere",
        "kryptos_k1_certificate.json",
        "known-key Vigenère on a keyword-mixed alphabet",
    ),
    "substitution": SolverLink(
        "substitution",
        "substitution",
        "substitution_certificate.json",
        "monoalphabetic substitution by annealing",
    ),
    "playfair": SolverLink(
        "playfair",
        "playfair",
        "playfair_certificate.json",
        "known-key Playfair digraph decrypt",
    ),
    "bifid": SolverLink(
        "bifid",
        "bifid",
        "bifid_certificate.json",
        "known-key Bifid square and period",
    ),
    "adfgvx": SolverLink(
        "adfgvx",
        "adfgvx",
        "adfgvx_certificate.json",
        "known-key ADFGVX fractionating transposition",
    ),
    "columnar": SolverLink(
        "columnar",
        "columnar",
        "kryptos_k3_certificate.json",
        "double columnar transposition, including published K3",
    ),
    "two-square": SolverLink(
        "two-square",
        "two-square",
        "two_square_certificate.json",
        "two-square decrypt with known squares or a keyword search",
    ),
    "crib": SolverLink(
        "crib",
        "vigenere",
        "crib_certificate.json",
        "Vigenère crib drag; same ciphertext family as vigenere",
    ),
    "beam-search": SolverLink(
        "beam-search",
        "beam-search",
        "beam_search_certificate.json",
        "monoalphabetic beam search under an English bigram model",
    ),
    "lumen-braid": SolverLink(
        "lumen-braid",
        "lumen-braid",
        "lumen_braid_certificate.json",
        "repository lumen-braid cipher, certificate only",
    ),
    "prism-latch": SolverLink(
        "prism-latch",
        "prism-latch",
        "prism_latch_certificate.json",
        "repository prism-latch cipher, certificate only",
    ),
}


@dataclass
class CausalLink:
    """Why a ciphertext was sent to one solver, and which certificate is checked."""

    solver: str
    family: str
    certificate_id: str
    features: dict[str, float]
    causing_features: list[dict[str, float | str]]
    runner_up: str
    kernel_scores: dict[str, float]
    exemplar_source: str
    exemplar_distance: float
    decision: str
    related_solvers: list[str] = field(default_factory=list)
    scope: str = SCOPE
    unread: str = ""

    def summary(self) -> str:
        causes = ", ".join(str(item["name"]) for item in self.causing_features[:5])
        if self.unread:
            return f"unread: {self.unread}. {self.scope}"
        return (
            f"solver: {self.solver}\n"
            f"family: {self.family}\n"
            f"certificate: {self.certificate_id}\n"
            f"decision: {self.decision}\n"
            f"causing features: {causes}\n"
            f"exemplar: {self.exemplar_source} distance {self.exemplar_distance:.6f}\n"
            f"runner-up: {self.runner_up}\n"
            f"{self.scope}"
        )


@dataclass
class _Exemplar:
    solver: str
    raw: list[float]
    z: list[float]
    source: str
    certificate_id: str
    weight: float


def _chi_pair(letters: str) -> tuple[float, float]:
    if len(letters) < 2:
        return 0.0, 0.0
    seq = [ord(ch) - 65 for ch in letters]
    n = len(seq)
    best = None
    shift0 = None
    for shift in range(26):
        score = chi_square([(c - shift) % 26 for c in seq]) / n
        if shift == 0:
            shift0 = score
        if best is None or score < best:
            best = score
    return float(shift0), float(best)


def _column_fitness(letters: str) -> float:
    """Best per-letter English unigram after Caesar-solving short columns."""
    n = len(letters)
    if n < 8:
        return 0.0
    seq = [ord(ch) - 65 for ch in letters]
    best = -1e9
    limit = min(5, max(1, n // 4))
    for period in range(1, limit + 1):
        total = 0.0
        for offset in range(period):
            column = seq[offset::period]
            if not column:
                continue
            top = -1e9
            width = len(column)
            for shift in range(26):
                score = 0.0
                for value in column:
                    score += LOG_UNIGRAM[(value - shift) % 26]
                score /= width
                if score > top:
                    top = score
            total += top * width
        mean = total / n
        if mean > best:
            best = mean
    return best


def feature_values(text: str) -> list[float]:
    """Feature row aligned with FEATURE_NAMES."""
    letters = letters_only(text)
    n = len(letters)
    denom = max(1, len(text))
    if n == 0:
        return [0.0] * len(FEATURE_NAMES)
    counts: dict[str, int] = {}
    for ch in letters:
        counts[ch] = counts.get(ch, 0) + 1
    adfgvx_hits = sum(counts.get(ch, 0) for ch in _ADFGVX)
    ic = index_of_coincidence(letters) if n >= 2 else 0.0
    chi0, chi_best = _chi_pair(letters)
    grams = [letters[i : i + 2] for i in range(n - 1)]
    gram_counts: dict[str, int] = {}
    for gram in grams:
        gram_counts[gram] = gram_counts.get(gram, 0) + 1
    digraph_repeat = sum(v for v in gram_counts.values() if v > 1) / max(1, len(grams))
    pairs = [letters[i : i + 2] for i in range(0, n - 1, 2)]
    pair_counts: dict[str, int] = {}
    for pair in pairs:
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    pair_repeat = sum(v - 1 for v in pair_counts.values() if v > 1) / max(1, len(pairs))
    doubles = sum(1 for i in range(n - 1) if letters[i] == letters[i + 1]) / max(1, n - 1)
    vowel = sum(counts.get(ch, 0) for ch in _VOWELS) / n
    top = max(counts.values()) / n
    entropy = 0.0
    for count in counts.values():
        p = count / n
        entropy -= p * math.log(p + 1e-12)
    entropy /= math.log(26)
    pure = 1.0 if set(letters) <= _ADFGVX else 0.0
    return [
        ic,
        adfgvx_hits / n,
        pure,
        len(counts) / 26.0,
        1.0 if n % 2 == 0 else 0.0,
        sum(ch.isspace() for ch in text) / denom,
        sum(ch.isdigit() for ch in text) / denom,
        1.0 if "J" in counts else 0.0,
        chi0,
        chi_best,
        chi0 - chi_best,
        digraph_repeat,
        pair_repeat,
        doubles,
        vowel,
        top,
        entropy,
        _column_fitness(letters),
        math.log(n + 1) / 6.0,
    ]


def feature_vector(text: str) -> dict[str, float]:
    """Named ciphertext features used by the router."""
    values = feature_values(text)
    return {name: round(value, 6) for name, value in zip(FEATURE_NAMES, values)}


def _normalize_script(name: str) -> str:
    return " ".join(name.strip().lower().replace("_", " ").split())


def load_certificate(certificate_id: str) -> dict:
    path = _DATA / certificate_id
    if not path.is_file():
        raise FileNotFoundError(f"missing certificate {certificate_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def _invoke(solver: str, text: str, certificate: dict) -> SolveResult:
    """Call the existing solver with the keys stored on its certificate."""
    keys = certificate.get("keys") or {}
    if solver == "caesar":
        from engine.solvers.caesar import solve_caesar

        return solve_caesar(text)
    if solver == "vigenere":
        from engine.solvers.vigenere import solve_vigenere

        return solve_vigenere(text)
    if solver == "keyed-vigenere":
        from engine.solvers.keyed_vigenere import solve_keyed_vigenere

        return solve_keyed_vigenere(
            text,
            keys["key"],
            keys["alphabet_keyword"],
            keys.get("index_letter"),
        )
    if solver == "substitution":
        from engine.solvers.substitution import solve_substitution

        return solve_substitution(text)
    if solver == "playfair":
        from engine.solvers.playfair import solve_playfair

        return solve_playfair(text, keys["keyword"])
    if solver == "bifid":
        from engine.solvers.bifid import solve_bifid

        return solve_bifid(text, square=keys["square"], period=int(keys["period"]))
    if solver == "adfgvx":
        from engine.solvers.adfgvx import solve_adfgvx

        return solve_adfgvx(
            text,
            keys["transposition_key"],
            fractionation_keyword=keys.get("fractionation_keyword"),
            square=keys.get("square"),
        )
    if solver == "columnar":
        from engine.solvers.columnar import solve_columnar

        widths = keys.get("widths") or [21, 28]
        return solve_columnar(text, int(widths[0]), int(widths[1]))
    if solver == "two-square":
        from engine.solvers.two_square import solve_two_square

        return solve_two_square(
            text,
            left=keys.get("left_square"),
            right=keys.get("right_square"),
        )
    if solver == "crib":
        from engine.solvers.crib import search_vigenere_crib

        hits = search_vigenere_crib(text, keys["crib"])
        if not hits:
            raise ValueError("crib solver found no consistent Vigenère key")
        hit = hits[0]
        return SolveResult(
            method="crib",
            plaintext=hit.plaintext,
            key=hit.key,
            score=hit.score,
            details={"period": hit.period, "offset": hit.offset, "scope": SCOPE},
        )
    if solver == "beam-search":
        from engine.solvers.beam_search import beam_search_decipher

        found = beam_search_decipher(text)
        return SolveResult(
            method="beam-search",
            plaintext=found.plaintext,
            key=found.decrypt_key,
            score=found.score,
            details={"beam_width": found.beam_width, "scope": SCOPE},
        )
    if solver == "lumen-braid":
        from engine.solvers.lumen_braid import decrypt

        plain = decrypt(text)
        return SolveResult(
            method="lumen-braid",
            plaintext=plain,
            key="",
            score=float(len(letters_only(plain))),
            details={"scope": SCOPE},
        )
    if solver == "prism-latch":
        from engine.solvers.prism_latch import decrypt

        plain = decrypt(text)
        return SolveResult(
            method="prism-latch",
            plaintext=plain,
            key="",
            score=float(len(letters_only(plain))),
            details={"scope": SCOPE},
        )
    raise KeyError(f"no solver named {solver}")


def _sample_ciphertext(kind: str, plain: str, rng: random.Random) -> str | None:
    """Encrypt one prose window with the solver family's own encrypt function."""
    if kind == "caesar":
        from engine.ciphers import caesar_encrypt

        return caesar_encrypt(plain, rng.randint(1, 25))
    if kind == "vigenere":
        from engine.ciphers import vigenere_encrypt

        return vigenere_encrypt(plain, rng.choice(_KEYS))
    if kind == "keyed-vigenere":
        from engine.solvers.keyed_vigenere import keyed_vigenere_encrypt

        return keyed_vigenere_encrypt(plain, rng.choice(_KEYS), rng.choice(_ALPHABETS), "K")
    if kind == "substitution":
        from engine.ciphers import substitution_encrypt

        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        rng.shuffle(alphabet)
        return substitution_encrypt(plain, "".join(alphabet))
    if kind == "playfair":
        from engine.solvers.playfair import playfair_encrypt

        return playfair_encrypt(plain, rng.choice(_KEYS))
    if kind == "bifid":
        from engine.solvers.bifid import bifid_encrypt
        from engine.solvers.bifid import square_from_keyword

        return bifid_encrypt(plain, square_from_keyword(rng.choice(_KEYS)), rng.choice((5, 6, 7, 8)))
    if kind == "adfgvx":
        from engine.solvers.adfgvx import adfgvx_encrypt

        letters = "".join(ch for ch in plain.upper() if "A" <= ch <= "Z")
        take = rng.choice((10, 12, 14, 16, 20, 28))
        fragment = letters[:take]
        if len(fragment) < 8:
            return None
        return adfgvx_encrypt(
            fragment,
            rng.choice(_KEYS),
            fractionation_keyword=rng.choice(_KEYS),
        )
    if kind == "columnar":
        from engine.solvers.columnar import columnar_encrypt_right_to_left

        letters = "".join(ch for ch in plain.upper() if "A" <= ch <= "Z")
        if len(letters) < 16:
            return None
        width = rng.choice((4, 5, 6, 7, 8, 9))
        pad = (-len(letters)) % width
        return columnar_encrypt_right_to_left(letters + ("X" * pad), width)
    if kind == "two-square":
        from engine.ciphers import square_from_keyword
        from engine.ciphers import two_square_encrypt

        return two_square_encrypt(
            plain,
            square_from_keyword(rng.choice(_KEYS)),
            square_from_keyword(rng.choice(_KEYS)),
        )
    if kind == "beam-search":
        from engine.ciphers import substitution_encrypt

        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        rng.shuffle(alphabet)
        return substitution_encrypt(plain, "".join(alphabet))
    if kind == "lumen-braid":
        from engine.solvers.lumen_braid import encrypt

        return encrypt(plain)
    if kind == "prism-latch":
        from engine.solvers.prism_latch import encrypt

        return encrypt(plain)
    raise KeyError(kind)


def _windows(prose: str, rng: random.Random, count: int) -> list[str]:
    blob = " ".join(part.strip() for part in prose.split("\n\n") if part.strip())
    lengths = (26, 28, 36, 48, 64, 96, 140, 180)
    out: list[str] = []
    for index in range(count):
        length = lengths[index % len(lengths)]
        length = min(length, len(blob))
        start = rng.randint(0, len(blob) - length)
        out.append(blob[start : start + length])
    return out


def _sqdist(left: list[float], right: list[float]) -> float:
    return sum((a - b) * (a - b) for a, b in zip(left, right))


class SolverNet:
    """Trained router from ciphertext features to a certified solver."""

    def __init__(self, exemplars: list[_Exemplar], mean: list[float], std: list[float]) -> None:
        self.exemplars = exemplars
        self.mean = mean
        self.std = std
        self.centroids = self._centroids()

    def _centroids(self) -> dict[str, list[float]]:
        buckets: dict[str, list[list[float]]] = defaultdict(list)
        for exemplar in self.exemplars:
            buckets[exemplar.solver].append(exemplar.z)
        centroids: dict[str, list[float]] = {}
        width = len(FEATURE_NAMES)
        for solver, rows in buckets.items():
            centroids[solver] = [
                sum(row[i] for row in rows) / len(rows) for i in range(width)
            ]
        return centroids

    def _z(self, raw: list[float]) -> list[float]:
        return [(raw[i] - self.mean[i]) / self.std[i] for i in range(len(raw))]

    def _kernel_scores(self, zrow: list[float]) -> dict[str, float]:
        scores: dict[str, float] = {solver: 0.0 for solver in ROUTED_SOLVERS}
        for exemplar in self.exemplars:
            distance = _sqdist(zrow, exemplar.z)
            scores[exemplar.solver] += exemplar.weight * math.exp(-GAMMA * distance)
        return scores

    def _causing(
        self,
        raw: list[float],
        zrow: list[float],
        winner: str,
        runner: str,
    ) -> list[dict[str, float | str]]:
        winner_mean = self.centroids.get(winner)
        runner_mean = self.centroids.get(runner)
        ranked: list[tuple[float, dict[str, float | str]]] = []
        for index, name in enumerate(FEATURE_NAMES):
            if winner_mean is None:
                contribution = abs(zrow[index])
            elif runner_mean is None:
                contribution = abs(zrow[index] - winner_mean[index])
            else:
                # Positive when this coordinate is closer to the chosen family.
                contribution = (zrow[index] - runner_mean[index]) ** 2 - (
                    zrow[index] - winner_mean[index]
                ) ** 2
            if contribution <= 0:
                continue
            ranked.append(
                (
                    contribution,
                    {
                        "name": name,
                        "value": round(raw[index], 6),
                        "contribution": round(contribution, 6),
                    },
                )
            )
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in ranked[:6]]

    def decline(self, script: str) -> CausalLink:
        """Refuse a named unknown script. No solver is called."""
        key = _normalize_script(script)
        label = UNREAD_SCRIPTS.get(key)
        if label is None:
            for alias, title in UNREAD_SCRIPTS.items():
                if alias in key:
                    label = title
                    break
        if label is None:
            label = script.strip() or "unknown script"
        return CausalLink(
            solver="",
            family="unreadable",
            certificate_id="",
            features={},
            causing_features=[],
            runner_up="",
            kernel_scores={},
            exemplar_source="",
            exemplar_distance=0.0,
            decision="refused",
            scope=SCOPE,
            unread=label,
        )

    def route(self, text: str, *, script: str | None = None) -> CausalLink:
        """Pick a solver family and record the features that caused it."""
        if script:
            refused = self.decline(script)
            if refused.unread in UNREAD_SCRIPTS.values() or _normalize_script(script) in UNREAD_SCRIPTS:
                return refused
            if any(alias in _normalize_script(script) for alias in UNREAD_SCRIPTS):
                return refused
        if not letters_only(text):
            raise ValueError("ciphertext has no A-Z letters to route")
        raw = feature_values(text)
        zrow = self._z(raw)
        scores = self._kernel_scores(zrow)
        ordered = sorted(scores, key=lambda name: scores[name], reverse=True)
        kernel_choice = ordered[0]
        runner = ordered[1] if len(ordered) > 1 else ""
        nearest = min(self.exemplars, key=lambda exemplar: _sqdist(zrow, exemplar.z))
        distance = _sqdist(zrow, nearest.z)
        # A certified ciphertext is an exemplar. Distance 0 means these features
        # are that certificate, so the link checks that certificate.
        if nearest.certificate_id and distance <= 1e-8:
            chosen = nearest.solver
            certificate_id = nearest.certificate_id
            decision = "kernel" if kernel_choice == chosen else "certified-exemplar"
            exemplar_source = nearest.source
        else:
            chosen = kernel_choice
            certificate_id = SOLVER_CATALOG[chosen].certificate_id
            decision = "kernel"
            exemplar_source = nearest.source
        if runner == chosen and len(ordered) > 2:
            runner = ordered[2] if ordered[1] == chosen else ordered[1]
        # Runner-up should be a different solver than the choice.
        for candidate in ordered:
            if candidate != chosen:
                runner = candidate
                break
        link_meta = SOLVER_CATALOG[chosen]
        return CausalLink(
            solver=chosen,
            family=link_meta.family,
            certificate_id=certificate_id,
            features=feature_vector(text),
            causing_features=self._causing(raw, zrow, chosen, runner),
            runner_up=runner,
            kernel_scores={name: round(scores[name], 6) for name in ordered},
            exemplar_source=exemplar_source,
            exemplar_distance=distance,
            decision=decision,
            related_solvers=list(RELATED_SOLVERS.get(chosen, ())),
            scope=SCOPE,
        )

    def recover(self, text: str, link: CausalLink | None = None) -> SolveResult:
        """Run the linked solver and check the certificate it names.

        Known-key solvers are given the keys stored on that certificate.
        Search solvers (Caesar, Vigenère) are not given the key.
        """
        chosen = link if link is not None else self.route(text)
        if chosen.unread or not chosen.solver:
            raise RuntimeError(chosen.summary())
        certificate = load_certificate(chosen.certificate_id)
        result = _invoke(chosen.solver, text, certificate)
        result.details = dict(result.details)
        result.details["solver_net"] = {
            "solver": chosen.solver,
            "certificate_id": chosen.certificate_id,
            "decision": chosen.decision,
            "causing_features": [item["name"] for item in chosen.causing_features],
            "scope": SCOPE,
        }
        return result


def _certificate_exemplars() -> list[tuple[str, str, float]]:
    """Solver, certificate filename, training weight.

    Crib is omitted here because its ciphertext is the Vigenère certificate.
    Beam search keeps its own certificate. Keyed Vigenère keeps both K1 and K2.
    """
    rows = [
        ("caesar", "caesar_certificate.json", 1.0),
        ("vigenere", "vigenere_certificate.json", 1.0),
        ("keyed-vigenere", "kryptos_k1_certificate.json", 1.0),
        ("keyed-vigenere", "kryptos_k2_certificate.json", 1.0),
        ("substitution", "substitution_certificate.json", 1.0),
        ("playfair", "playfair_certificate.json", 1.0),
        ("bifid", "bifid_certificate.json", 1.0),
        ("adfgvx", "adfgvx_certificate.json", 1.0),
        ("columnar", "kryptos_k3_certificate.json", 1.0),
        ("two-square", "two_square_certificate.json", 1.0),
        ("beam-search", "beam_search_certificate.json", 1.0),
        ("lumen-braid", "lumen_braid_certificate.json", 1.0),
        ("prism-latch", "prism_latch_certificate.json", 1.0),
    ]
    return rows


def train_solver_net(seed: int = SEED, samples_per_class: int = SAMPLES_PER_CLASS) -> SolverNet:
    """Fit the router on synthetic ciphertexts plus the certified exemplars."""
    prose = _PROSE.read_text(encoding="utf-8")
    rng = random.Random(seed)
    raw_rows: list[tuple[str, list[float], str, str, float]] = []
    for solver in ROUTED_SOLVERS:
        # Beam search is the same monoalphabetic family as substitution.
        # One certified exemplar is enough; extra synthetic copies would
        # split that family in two for no ciphertext difference.
        if solver == "beam-search":
            continue
        for plain in _windows(prose, rng, samples_per_class):
            try:
                ciphertext = _sample_ciphertext(solver, plain, rng)
            except ValueError:
                continue
            if not ciphertext or len(letters_only(ciphertext)) < 8:
                continue
            raw_rows.append((solver, feature_values(ciphertext), f"synthetic:{solver}", "", 1.0))
    for solver, certificate_id, weight in _certificate_exemplars():
        certificate = load_certificate(certificate_id)
        ciphertext = certificate.get("ciphertext")
        if not ciphertext:
            continue
        raw_rows.append(
            (solver, feature_values(ciphertext), certificate_id, certificate_id, weight)
        )
    if len(raw_rows) < len(ROUTED_SOLVERS):
        raise RuntimeError("solver net training produced no exemplars")
    width = len(FEATURE_NAMES)
    mean = [0.0] * width
    for _solver, raw, _source, _cert, _weight in raw_rows:
        for index, value in enumerate(raw):
            mean[index] += value
    mean = [value / len(raw_rows) for value in mean]
    variance = [0.0] * width
    for _solver, raw, _source, _cert, _weight in raw_rows:
        for index, value in enumerate(raw):
            delta = value - mean[index]
            variance[index] += delta * delta
    std = [math.sqrt(value / len(raw_rows)) + 1e-6 for value in variance]
    exemplars: list[_Exemplar] = []
    for solver, raw, source, certificate_id, weight in raw_rows:
        zrow = [(raw[index] - mean[index]) / std[index] for index in range(width)]
        exemplars.append(
            _Exemplar(
                solver=solver,
                raw=raw,
                z=zrow,
                source=source,
                certificate_id=certificate_id,
                weight=weight,
            )
        )
    return SolverNet(exemplars, mean, std)


@lru_cache(maxsize=1)
def get_solver_net() -> SolverNet:
    """Return the process-wide trained router."""
    return train_solver_net()


def route_ciphertext(text: str, *, script: str | None = None) -> CausalLink:
    """Route one ciphertext with the shared trained net."""
    return get_solver_net().route(text, script=script)


__all__ = [
    "FEATURE_NAMES",
    "KNOWN_SOLVERS",
    "SCOPE",
    "SOLVER_CATALOG",
    "UNREAD_SCRIPTS",
    "CausalLink",
    "SolverNet",
    "feature_vector",
    "get_solver_net",
    "load_certificate",
    "route_ciphertext",
    "train_solver_net",
]
