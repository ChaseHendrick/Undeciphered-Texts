"""Held-out grade for the trigram letter model and a cipher-family router.

The letter model is the same network as engine.neural. It is fit only on
Jane Austen, Pride and Prejudice, chapters I-III. It is scored on a
different book: the opening of Arthur Conan Doyle, "A Scandal in Bohemia."
A German contrast comes from Grimm, "Der Wolf und die sieben jungen
Geißlein," which is not the Froschkönig excerpt used by engine.german.

The router is a small softmax network on ciphertext features. It is trained
on ciphertexts made from the Austen letters and scored on ciphertexts made
from the Doyle letters. Keys are fresh. Certificate plaintexts are not the
training or evaluation prose.

This grade does not decipher Kryptos K4, Truppenschlüssel Nr. 86, or an
unknown script. There is no engine/solver_net.py in this change; the router
lives here so a parallel solver_net edit is left alone.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path

from engine.alphabet import letters_only
from engine.ciphers import (
    caesar_encrypt,
    square_from_keyword as two_square_square,
    substitution_encrypt,
    two_square_encrypt,
    vigenere_encrypt,
)
from engine.german import german_letters
from engine.neural import NeuralLetterModel, load_training_prose
from engine.solvers import keel_sieve, lumen_braid, prism_latch
from engine.solvers.adfgvx import adfgvx_encrypt, columnar_encrypt
from engine.solvers.bifid import bifid_encrypt
from engine.solvers.bifid import square_from_keyword as bifid_square
from engine.solvers.four_square import four_square_encrypt
from engine.solvers.keyed_vigenere import keyed_vigenere_encrypt
from engine.solvers.playfair import playfair_encrypt

_DATA = Path(__file__).resolve().parent / "data"
TRAIN_PATH = _DATA / "neural_train_austen.txt"
HELD_EN_PATH = _DATA / "neural_heldout_doyle.txt"
HELD_DE_PATH = _DATA / "neural_heldout_grimm_wolf.txt"
METRICS_PATH = _DATA / "neural_grade_metrics.json"
CERTIFICATE_PATH = _DATA / "neural_grade_certificate.json"

TRAIN_URL = "https://www.gutenberg.org/ebooks/1342"
TRAIN_TEXT_URL = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
HELD_EN_URL = "https://www.gutenberg.org/ebooks/1661"
HELD_EN_TEXT_URL = "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"
HELD_DE_URL = "https://www.gutenberg.org/ebooks/77905"
HELD_DE_TEXT_URL = "https://www.gutenberg.org/cache/epub/77905/pg77905.txt"

WINDOW = 120
ROUTER_WINDOW = 180
ROUTER_TRAIN_PER_CLASS = 20
ROUTER_TEST_PER_CLASS = 12
ROUTER_EPOCHS = 60
ROUTER_HIDDEN = 32
ROUTER_SEED = 20261002
GRADE_SEED = 20261002
OVERLAP_WIDTH = 48

# Certified cipher families that have a forward map in this repository.
# beam-search and vigenère-crib are search procedures, not extra families.
FAMILIES = (
    "caesar",
    "vigenere",
    "keyed-vigenere",
    "substitution",
    "playfair",
    "bifid",
    "two-square",
    "four-square",
    "adfgvx",
    "columnar-transposition",
    "beaufort",
    "porta",
    "enigma",
    "m209",
    "keel-sieve",
    "lumen-braid",
    "prism-latch",
)


def letters_az(text: str) -> str:
    """A-Z only. Umlauts are not folded; use german_letters for German."""
    return "".join(ch for ch in letters_only(text) if "A" <= ch <= "Z")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def three_way_chance_baseline(candidates: int = 3) -> float:
    """Chance that one named score is strictly best among i.i.d. continuous scores.

    With C distinct scores, each is equally likely to be the unique maximum,
    so the probability is 1/C. For the letter grade, C is 3: real English,
    shuffled English, and German.
    """
    if candidates < 2:
        raise ValueError("chance baseline needs at least two candidates")
    return 1.0 / candidates


def router_chance_baseline(n_families: int | None = None) -> float:
    """Uniform guess among the routed families."""
    count = len(FAMILIES) if n_families is None else n_families
    if count < 2:
        raise ValueError("router baseline needs at least two families")
    return 1.0 / count


def assert_split(train_letters: str, held_letters: str, width: int = OVERLAP_WIDTH) -> None:
    """Fail if the held-out letter string was used as training text.

    Containment of the whole held-out string catches a copied test file.
    Non-overlapping windows catch a partial paste of the test text.
    """
    if len(held_letters) < width:
        raise ValueError("held-out letter string is too short to audit")
    if held_letters in train_letters:
        raise ValueError("held-out text is contained in the training text")
    for start in range(0, len(held_letters) - width + 1, width):
        window = held_letters[start : start + width]
        if window in train_letters:
            raise ValueError("a held-out window is inside the training text")


def certificate_letter_strings(min_length: int = 16) -> list[str]:
    """Plaintext or known-text fields from engine/data/*_certificate.json."""
    found: list[str] = []
    for path in sorted(_DATA.glob("*_certificate.json")):
        if path.name == CERTIFICATE_PATH.name:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for key in ("plaintext", "known_text"):
            value = payload.get(key)
            if not isinstance(value, str):
                continue
            folded = letters_az(value)
            if len(folded) >= min_length:
                found.append(folded)
    return found


def assert_certificate_plaintexts_excluded(*letter_strings: str) -> None:
    """Generation prose must not be a certificate known plaintext."""
    banned = certificate_letter_strings()
    for letters in letter_strings:
        for banned_text in banned:
            if banned_text in letters:
                raise ValueError("certificate plaintext is inside the grade prose")


def _windows(letters: str, size: int) -> list[str]:
    return [letters[i : i + size] for i in range(0, len(letters) - size + 1, size)]


def language_preference(
    train_prose: str,
    held_english: str,
    held_german: str,
    window: int = WINDOW,
    seed: int = GRADE_SEED,
) -> dict[str, float | int | str]:
    """Fit on train_prose only and score held-out English against shuffle and German.

    Raises ValueError if the held-out English letters sit inside the fitted
    training letters. That is the failure mode for training on the test text.
    """
    train_letters = letters_az(train_prose)
    english = letters_az(held_english)
    german = german_letters(held_german)
    model = NeuralLetterModel(train_prose, seed=seed)
    if model.training_letters != train_letters:
        raise ValueError("letter model trained on something other than the train prose")
    assert_split(model.training_letters, english)
    english_windows = _windows(english, window)
    german_windows = _windows(german, window)
    count = min(len(english_windows), len(german_windows))
    if count < 8:
        raise ValueError("not enough held-out windows")
    draw = random.Random(seed)
    preference = 0
    beats_shuffled = 0
    beats_german = 0
    nll_english = 0.0
    nll_shuffled = 0.0
    nll_german = 0.0
    denom = float(window - 2)
    for index in range(count):
        seq = [ord(ch) - 65 for ch in english_windows[index]]
        shuffled = seq[:]
        draw.shuffle(shuffled)
        if shuffled == seq:
            draw.shuffle(shuffled)
        german_seq = [ord(ch) - 65 for ch in german_windows[index]]
        score_english = model.score(seq)
        score_shuffled = model.score(shuffled)
        score_german = model.score(german_seq)
        nll_english += -score_english / denom
        nll_shuffled += -score_shuffled / denom
        nll_german += -score_german / denom
        if score_english > score_shuffled:
            beats_shuffled += 1
        if score_english > score_german:
            beats_german += 1
        if score_english > score_shuffled and score_english > score_german:
            preference += 1
    baseline = three_way_chance_baseline(3)
    return {
        "backend": model.backend,
        "train_events": model.train_events,
        "train_letters_sha256": sha256_text(model.training_letters),
        "heldout_english_letters_sha256": sha256_text(english),
        "heldout_german_letters_sha256": sha256_text(german),
        "window_letters": window,
        "windows": count,
        "preference_correct": preference,
        "beats_shuffled": beats_shuffled,
        "beats_german": beats_german,
        "preference_accuracy": preference / count,
        "shuffled_accuracy": beats_shuffled / count,
        "german_accuracy": beats_german / count,
        "chance_baseline": baseline,
        "shuffled_chance_baseline": 0.5,
        "german_chance_baseline": 0.5,
        "mean_log_loss_english": nll_english / count,
        "mean_log_loss_shuffled": nll_shuffled / count,
        "mean_log_loss_german": nll_german / count,
    }


def _english_unigram(letters: str) -> list[float]:
    counts = [0] * 26
    for ch in letters:
        counts[ord(ch) - 65] += 1
    total = sum(counts) + 13.0
    return [(count + 0.5) / total for count in counts]


def _index_of_coincidence(counts: list[int], n: int) -> float:
    if n < 2:
        return 0.0
    return sum(count * (count - 1) for count in counts) / (n * (n - 1))


def ciphertext_features(text: str, english: list[float]) -> list[float]:
    """Fixed features of an A-Z ciphertext. english is the training unigram."""
    letters = letters_az(text)
    n = len(letters)
    if n < 16:
        raise ValueError("ciphertext is too short to featurize")
    counts = [0] * 26
    for ch in letters:
        counts[ord(ch) - 65] += 1
    freq = [count / n for count in counts]
    ic = _index_of_coincidence(counts, n)
    entropy = -sum(p * math.log(p) for p in freq if p > 0.0)
    chi_uniform = sum((count - n / 26.0) ** 2 / (n / 26.0) for count in counts) / n
    english_norm = math.sqrt(sum(p * p for p in english))
    best_chi = 1e9
    best_shift_cos = -1.0
    for shift in range(26):
        plain = freq[shift:] + freq[:shift] if shift else freq
        chi = sum((plain[i] - english[i]) ** 2 / english[i] for i in range(26))
        if chi < best_chi:
            best_chi = chi
        dot = sum(plain[i] * english[i] for i in range(26))
        norm = math.sqrt(sum(p * p for p in plain))
        cosine = dot / (norm * english_norm + 1e-12)
        if cosine > best_shift_cos:
            best_shift_cos = cosine
    dot0 = sum(freq[i] * english[i] for i in range(26))
    freq_norm = math.sqrt(sum(p * p for p in freq))
    cos0 = dot0 / (freq_norm * english_norm + 1e-12)
    sorted_freq = sorted(freq, reverse=True)
    sorted_eng = sorted(english, reverse=True)
    sorted_dot = sum(sorted_freq[i] * sorted_eng[i] for i in range(26))
    sorted_norm = math.sqrt(sum(p * p for p in sorted_freq))
    sorted_eng_norm = math.sqrt(sum(p * p for p in sorted_eng))
    sorted_cos = sorted_dot / (sorted_norm * sorted_eng_norm + 1e-12)
    doubles = sum(1 for i in range(n - 1) if letters[i] == letters[i + 1]) / (n - 1)
    pair_total = 0
    pair_doubles = 0
    for i in range(0, n - 1, 2):
        pair_total += 1
        if letters[i] == letters[i + 1]:
            pair_doubles += 1
    adfgvx = sum(ch in "ADFGVX" for ch in letters) / n
    j_frac = counts[ord("J") - 65] / n
    q_frac = counts[ord("Q") - 65] / n
    vowels = sum(counts[ord(ch) - 65] for ch in "AEIOU") / n
    max_slice = 0.0
    best_period = 2
    best_ics: list[float] = []
    for period in range(2, 8):
        ics: list[float] = []
        for residue in range(period):
            slice_letters = letters[residue::period]
            if len(slice_letters) < 8:
                continue
            slice_counts = [0] * 26
            for ch in slice_letters:
                slice_counts[ord(ch) - 65] += 1
            ics.append(_index_of_coincidence(slice_counts, len(slice_letters)))
        if ics and (sum(ics) / len(ics)) > max_slice:
            max_slice = sum(ics) / len(ics)
            best_period = period
            best_ics = ics
    slice_var = 0.0
    if best_ics:
        mean_ic = sum(best_ics) / len(best_ics)
        slice_var = sum((value - mean_ic) ** 2 for value in best_ics) / len(best_ics)
    slice_cosines: list[float] = []
    for residue in range(best_period):
        slice_letters = letters[residue::best_period]
        if len(slice_letters) < 8:
            continue
        slice_counts = [0] * 26
        for ch in slice_letters:
            slice_counts[ord(ch) - 65] += 1
        slice_n = len(slice_letters)
        slice_freq = [count / slice_n for count in slice_counts]
        best_cos = -1.0
        for shift in range(26):
            plain = slice_freq[shift:] + slice_freq[:shift] if shift else slice_freq
            dot = sum(plain[i] * english[i] for i in range(26))
            norm = math.sqrt(sum(p * p for p in plain))
            cosine = dot / (norm * english_norm + 1e-12)
            if cosine > best_cos:
                best_cos = cosine
        slice_cosines.append(best_cos)
    mean_slice_cos = sum(slice_cosines) / len(slice_cosines) if slice_cosines else 0.0
    digraphs: dict[str, int] = {}
    for i in range(0, n - 1, 2):
        pair = letters[i : i + 2]
        digraphs[pair] = digraphs.get(pair, 0) + 1
    digraph_total = sum(digraphs.values())
    repeated = sum(value for value in digraphs.values() if value > 1)
    digraph_repeat = repeated / digraph_total if digraph_total else 0.0
    unique = sum(1 for count in counts if count > 0) / 26.0
    top = max(counts) / n
    kappas = []
    for lag in (1, 2, 3, 4, 5):
        matches = sum(1 for i in range(n - lag) if letters[i] == letters[i + lag])
        kappas.append(matches / (n - lag))
    even = [0.0] * 26
    odd = [0.0] * 26
    for index, ch in enumerate(letters):
        bucket = even if index % 2 == 0 else odd
        bucket[ord(ch) - 65] += 1.0
    even_n = sum(even) or 1.0
    odd_n = sum(odd) or 1.0
    even_odd = sum(abs(even[i] / even_n - odd[i] / odd_n) for i in range(26))

    def residue_variance(modulus: int) -> float:
        columns: list[list[float]] = []
        for residue in range(modulus):
            slice_letters = letters[residue::modulus]
            slice_counts = [0] * 26
            for ch in slice_letters:
                slice_counts[ord(ch) - 65] += 1
            denom = max(len(slice_letters), 1)
            columns.append([count / denom for count in slice_counts])
        # Variance of residue-class frequencies, averaged over the alphabet.
        total = 0.0
        for letter_index in range(26):
            values = [column[letter_index] for column in columns]
            mean = sum(values) / modulus
            total += sum((value - mean) ** 2 for value in values) / modulus
        return total / 26.0

    return [
        ic,
        entropy,
        chi_uniform,
        best_chi,
        best_shift_cos,
        cos0,
        sorted_cos,
        doubles,
        pair_doubles / pair_total,
        adfgvx,
        j_frac,
        q_frac,
        vowels,
        max_slice,
        slice_var,
        mean_slice_cos,
        digraph_repeat,
        unique,
        top,
        even_odd,
        residue_variance(3),
        residue_variance(4),
        *kappas,
    ]


def _random_word(draw: random.Random, lo: int, hi: int) -> str:
    return "".join(chr(65 + draw.randrange(26)) for _ in range(draw.randint(lo, hi)))


def _random_permutation(draw: random.Random) -> str:
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    draw.shuffle(letters)
    key = "".join(letters)
    for shift in range(26):
        rotated = "".join(chr(65 + (index + shift) % 26) for index in range(26))
        if key == rotated:
            return _random_permutation(draw)
    return key



WEIGHTS_PATH = _DATA / "neural_router_weights.json"
LOOP_STATUS_PATH = _DATA / "neural_router_loop_status.json"
LOOP_STOP_PATH = _DATA / "neural_router_loop.stop"
LOOP_PID_PATH = _DATA / "neural_router_loop.pid"

# Labels that would claim an unsolved text. They are never router classes.
_UNSOLVED_LABELS = {
    "k4",
    "kryptos-k4",
    "zodiac",
    "zodiac-340",
    "zodiac-408",
    "beale",
    "beale-2",
    "beale-cipher",
    "mccormick",
    "voynich",
    "voynich-manuscript",
    "nr-86",
    "nr86",
    "truppenschlussel",
}
_UNSOLVED_TOKENS = {"k4", "zodiac", "beale", "mccormick", "voynich", "nr86"}


def label_is_unsolved(label: str) -> bool:
    """True for K4, Zodiac, Beale, McCormick, Voynich, and Nr. 86."""
    folded = " ".join(label.strip().lower().replace("_", " ").split()).replace(" ", "-")
    if folded in _UNSOLVED_LABELS or "nr-86" in folded:
        return True
    parts = set(folded.split("-"))
    return bool(parts & _UNSOLVED_TOKENS)


def normalize_cipher_label(name: str) -> str | None:
    """Map a certificate cipher_name onto a router class, or None if refused."""
    raw = " ".join(name.strip().lower().replace("_", " ").split())
    if raw.startswith("m-209") or raw.startswith("m209"):
        label = "m209"
    else:
        label = raw.replace(" ", "-").replace("(", "").replace(")", "")
        label = "-".join(part for part in label.split("-") if part)
    if not label or label_is_unsolved(label):
        return None
    return label


def discover_solver_labels(data_dir: Path | None = None) -> list[str]:
    """Known-answer cipher labels from certificate files, in filename order.

    A certificate becomes a class when it has cipher_name, plaintext, and
    ciphertext. The plaintext is not copied into the router. Unsolved-text
    names are dropped. The same cipher_name on two files is one class.
    """
    root = data_dir or _DATA
    found: list[str] = []
    seen: set[str] = set()
    for path in sorted(root.glob("*_certificate.json")):
        if path.name == CERTIFICATE_PATH.name:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        cipher_name = payload.get("cipher_name")
        plaintext = payload.get("plaintext")
        ciphertext = payload.get("ciphertext")
        if not isinstance(cipher_name, str) or not cipher_name.strip():
            continue
        if not isinstance(plaintext, str) or not plaintext.strip():
            continue
        if not isinstance(ciphertext, str) or not ciphertext.strip():
            continue
        label = normalize_cipher_label(cipher_name)
        if label is None or label in seen:
            continue
        seen.add(label)
        found.append(label)
    return found


# Families with a fresh-key encrypt function. New certificate labels whose
# normalized name is in this set are sampled on Austen and Doyle. Other
# known-answer labels still become classes via their certificate ciphertext.
_GENERATOR_NAMES = set(FAMILIES)


def families_for_grade() -> tuple[str, ...]:
    """Grade classes: discovered labels we can encrypt, original order first.

    A later certificate joins this tuple when its label is in _GENERATOR_NAMES.
    That is how a new known-answer cipher with a registered generator becomes
    a scored class without editing a separate frozen list by hand.
    """
    discovered = discover_solver_labels()
    have = set(discovered)
    labels = [name for name in FAMILIES if name in have]
    for name in discovered:
        if name in _GENERATOR_NAMES and name not in labels:
            labels.append(name)
    return tuple(labels) if labels else tuple(FAMILIES)


def _certificate_ciphertexts(label: str, data_dir: Path | None = None) -> list[str]:
    """Ciphertext exemplars for one class. Plaintext is not returned."""
    root = data_dir or _DATA
    found: list[str] = []
    for path in sorted(root.glob("*_certificate.json")):
        if path.name == CERTIFICATE_PATH.name:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        cipher_name = payload.get("cipher_name")
        ciphertext = payload.get("ciphertext")
        if not isinstance(cipher_name, str) or not isinstance(ciphertext, str):
            continue
        if normalize_cipher_label(cipher_name) != label:
            continue
        if ciphertext.strip():
            found.append(ciphertext)
    return found


def load_router_weights(path: Path | None = None) -> dict | None:
    weights_path = path or WEIGHTS_PATH
    if not weights_path.is_file():
        return None
    return json.loads(weights_path.read_text(encoding="utf-8"))


def heldout_accuracy_not_worse(new_accuracy: float, previous: dict | None) -> bool:
    """True when there is no saved score yet, or the new score does not drop."""
    if previous is None:
        return True
    old = previous.get("heldout_accuracy")
    if not isinstance(old, (int, float)):
        return True
    return float(new_accuracy) + 1e-12 >= float(old)


def _atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def retrain_router(*, write: bool = True, weights_path: Path | None = None) -> dict[str, object]:
    """Refit from the current certificates. Write weights only if the held-out score holds.

    Calling this function is the whole update. Nothing here schedules a rerun.
    The returned choice is a family label, not a plaintext.
    """
    from engine.neural_features import feature_tables, router_features

    destination = weights_path or WEIGHTS_PATH
    train_letters = letters_az(load_training_prose(TRAIN_PATH))
    held_letters = letters_az(load_training_prose(HELD_EN_PATH))
    assert_split(train_letters, held_letters)
    assert_certificate_plaintexts_excluded(train_letters, held_letters)
    discovered = [label for label in discover_solver_labels() if not label_is_unsolved(label)]
    ordered = [name for name in FAMILIES if name in discovered]
    for name in discovered:
        if name in _GENERATOR_NAMES and name not in ordered:
            ordered.append(name)
    exemplars = [name for name in discovered if name not in _GENERATOR_NAMES]
    classes = ordered + exemplars
    if len(classes) < 2:
        raise ValueError("need at least two certified solver labels")
    english = _english_unigram(train_letters)
    tables = feature_tables(train_letters, english)
    train_x, train_y = _router_samples(
        train_letters, english, ROUTER_TRAIN_PER_CLASS, ROUTER_SEED, ordered, tables
    )
    test_x, test_y = _router_samples(
        held_letters, english, ROUTER_TEST_PER_CLASS, ROUTER_SEED + 1, ordered, tables
    )
    for label in exemplars:
        class_index = classes.index(label)
        for ciphertext in _certificate_ciphertexts(label):
            try:
                train_x.append(router_features(ciphertext, english, tables))
            except ValueError:
                continue
            train_y.append(class_index)
    predicted, weights = _fit_router_numpy(
        train_x,
        train_y,
        test_x,
        ROUTER_EPOCHS,
        ROUTER_HIDDEN,
        ROUTER_SEED,
        n_classes=len(classes),
    )
    correct = sum(1 for guess, truth in zip(predicted, test_y) if guess == truth)
    total = len(test_y)
    accuracy = correct / total if total else 0.0
    previous = load_router_weights(destination)
    previous_accuracy = None if previous is None else previous.get("heldout_accuracy")
    wrote = False
    if write and heldout_accuracy_not_worse(accuracy, previous):
        payload = {
            "families": classes,
            "heldout_correct": correct,
            "heldout_total": total,
            "heldout_accuracy": accuracy,
            "note": (
                "Family choice only. Does not emit plaintext for K4, Zodiac, "
                "Beale, McCormick, Voynich, or Nr. 86."
            ),
            **weights,
        }
        _atomic_json(destination, payload)
        wrote = True
    return {
        "wrote": wrote,
        "families": classes,
        "correct": correct,
        "total": total,
        "accuracy": accuracy,
        "previous_accuracy": previous_accuracy,
        "weights_path": str(destination),
    }


def route_ciphertext(text: str, weights_path: Path | None = None) -> str:
    """Route one ciphertext to a certified family label. Does not return plaintext."""
    import numpy as np

    from engine.neural_features import feature_tables, router_features

    payload = load_router_weights(weights_path)
    if payload is None:
        raise FileNotFoundError("router weights are not written yet")
    families = list(payload["families"])
    if not families:
        raise ValueError("router weights have no certified family")
    train_letters = letters_az(load_training_prose(TRAIN_PATH))
    english = _english_unigram(train_letters)
    tables = feature_tables(train_letters, english)
    row = np.asarray(router_features(text, english, tables), dtype=np.float64)
    mean = np.asarray(payload["mean"], dtype=np.float64)
    scale = np.asarray(payload["scale"], dtype=np.float64)
    if row.shape[0] != mean.shape[0]:
        raise ValueError("feature width does not match the saved router")
    hidden = np.tanh(((row - mean) / scale) @ np.asarray(payload["w1"]) + np.asarray(payload["b1"]))
    logits = hidden @ np.asarray(payload["w2"]) + np.asarray(payload["b2"])
    # Exemplar classes sit after the scored families. Predictions still name a class.
    index = int(np.argmax(logits))
    if index >= len(families):
        raise ValueError("router weights do not match the class list")
    label = families[index]
    if label_is_unsolved(label):
        raise ValueError("refusing an unsolved-text label")
    return label


def encrypt_family(family: str, text: str, draw: random.Random) -> str:
    """Encrypt with a fresh key. text is plaintext, not a certificate string."""
    if family == "caesar":
        return caesar_encrypt(text, draw.randint(1, 25))
    if family == "vigenere":
        return vigenere_encrypt(text, _random_word(draw, 4, 9))
    if family == "keyed-vigenere":
        return keyed_vigenere_encrypt(text, _random_word(draw, 4, 7), _random_word(draw, 5, 9))
    if family == "substitution":
        return substitution_encrypt(text, _random_permutation(draw))
    if family == "playfair":
        return playfair_encrypt(text, _random_word(draw, 4, 8))
    if family == "bifid":
        return bifid_encrypt(text, bifid_square(_random_word(draw, 4, 8)), draw.randint(5, 9))
    if family == "two-square":
        left = two_square_square(_random_word(draw, 4, 8))
        right = two_square_square(_random_word(draw, 4, 8))
        return two_square_encrypt(text, left, right)
    if family == "four-square":
        return four_square_encrypt(text, _random_word(draw, 4, 8), _random_word(draw, 4, 8))
    if family == "adfgvx":
        return adfgvx_encrypt(text, _random_word(draw, 5, 8), _random_word(draw, 6, 10))
    if family == "columnar-transposition":
        return columnar_encrypt(letters_az(text), _random_word(draw, 5, 9))
    if family == "beaufort":
        from engine.solvers.beaufort import beaufort_encrypt

        return beaufort_encrypt(text, _random_word(draw, 4, 9))
    if family == "porta":
        from engine.solvers.porta import porta_encrypt

        return porta_encrypt(text, _random_word(draw, 4, 9))
    if family == "enigma":
        from engine.solvers.enigma import enigma_encrypt

        rotors = draw.choice(
            (("I", "II", "III"), ("II", "I", "III"), ("III", "II", "I"), ("I", "III", "II"))
        )
        return enigma_encrypt(
            text,
            rotors=rotors,
            reflector="B",
            rings=_random_word(draw, 3, 3),
            positions=_random_word(draw, 3, 3),
            plugboard=[],
        )
    if family == "m209":
        from engine.solvers.m209 import (
            BOUCHAUDY_LUGS,
            BOUCHAUDY_PINS,
            WHEEL_ALPHABETS,
            m209_encrypt,
        )

        external = "".join(draw.choice(alphabet) for alphabet in WHEEL_ALPHABETS)
        return m209_encrypt(text, external, BOUCHAUDY_PINS, BOUCHAUDY_LUGS)
    if family == "keel-sieve":
        return keel_sieve.encrypt(text)
    if family == "lumen-braid":
        return lumen_braid.encrypt(text)
    if family == "prism-latch":
        return prism_latch.encrypt(text)
    raise ValueError(f"unknown cipher family {family}")


def _router_samples(
    letters: str,
    english: list[float],
    per_class: int,
    seed: int,
    families: tuple[str, ...] | list[str] | None = None,
    tables: dict | None = None,
) -> tuple[list[list[float]], list[int]]:
    from engine.neural_features import router_features

    draw = random.Random(seed)
    windows = _windows(letters, ROUTER_WINDOW)
    if len(windows) < 4:
        raise ValueError("not enough plaintext for router windows")
    names = tuple(families) if families is not None else FAMILIES
    features: list[list[float]] = []
    labels: list[int] = []
    for class_index, family in enumerate(names):
        for sample_index in range(per_class):
            window = windows[(sample_index * 5 + class_index * 2) % len(windows)]
            offset = (sample_index * 17) % 40
            rotated = window[offset:] + window[:offset]
            ciphertext = encrypt_family(family, rotated, draw)
            features.append(router_features(ciphertext, english, tables))
            labels.append(class_index)
    return features, labels


def _fit_router_numpy(
    train_x: list[list[float]],
    train_y: list[int],
    test_x: list[list[float]],
    epochs: int,
    hidden: int,
    seed: int,
    n_classes: int | None = None,
) -> tuple[list[int], dict[str, object]]:
    import numpy as np

    features = np.asarray(train_x, dtype=np.float64)
    held = np.asarray(test_x, dtype=np.float64)
    mean = features.mean(axis=0)
    scale = features.std(axis=0) + 1e-6
    train_n = (features - mean) / scale
    held_n = (held - mean) / scale
    n_samples, width = train_n.shape
    n_classes = len(FAMILIES) if n_classes is None else n_classes
    rng = np.random.default_rng(seed)
    weight_1 = rng.normal(0.0, 0.15, size=(width, hidden))
    bias_1 = np.zeros(hidden)
    weight_2 = rng.normal(0.0, 0.15, size=(hidden, n_classes))
    bias_2 = np.zeros(n_classes)
    targets = np.eye(n_classes)[np.asarray(train_y, dtype=np.int64)]
    for epoch in range(epochs):
        rate = 0.4 if epoch < epochs // 2 else 0.12
        activated = np.tanh(train_n @ weight_1 + bias_1)
        logits = activated @ weight_2 + bias_2
        shifted = logits - logits.max(axis=1, keepdims=True)
        probs = np.exp(shifted)
        probs /= probs.sum(axis=1, keepdims=True)
        grad_logits = (probs - targets) / n_samples
        grad_w2 = activated.T @ grad_logits
        grad_b2 = grad_logits.sum(axis=0)
        grad_hidden = grad_logits @ weight_2.T
        grad_pre = grad_hidden * (1.0 - activated * activated)
        weight_2 -= rate * grad_w2
        bias_2 -= rate * grad_b2
        weight_1 -= rate * (train_n.T @ grad_pre)
        bias_1 -= rate * grad_pre.sum(axis=0)
    activated = np.tanh(held_n @ weight_1 + bias_1)
    logits = activated @ weight_2 + bias_2
    predicted = [int(index) for index in logits.argmax(axis=1)]
    weights = {
        "mean": mean.tolist(),
        "scale": scale.tolist(),
        "w1": weight_1.tolist(),
        "b1": bias_1.tolist(),
        "w2": weight_2.tolist(),
        "b2": bias_2.tolist(),
        "hidden": hidden,
        "epochs": epochs,
        "width": int(width),
    }
    return predicted, weights


def _dot(row: list[float], col: list[float]) -> float:
    return sum(a * b for a, b in zip(row, col))


def _fit_router_python(
    train_x: list[list[float]],
    train_y: list[int],
    test_x: list[list[float]],
    epochs: int,
    hidden: int,
    seed: int,
    n_classes: int | None = None,
) -> list[int]:
    """Same architecture as the numpy fit, standard-library only."""
    width = len(train_x[0])
    n_samples = len(train_x)
    n_classes = len(FAMILIES) if n_classes is None else n_classes
    mean = [sum(row[j] for row in train_x) / n_samples for j in range(width)]
    var = [
        sum((row[j] - mean[j]) ** 2 for row in train_x) / n_samples for j in range(width)
    ]
    scale = [math.sqrt(value) + 1e-6 for value in var]

    def norm(rows: list[list[float]]) -> list[list[float]]:
        return [[(row[j] - mean[j]) / scale[j] for j in range(width)] for row in rows]

    train_n = norm(train_x)
    held_n = norm(test_x)
    draw = random.Random(seed)
    weight_1 = [[draw.gauss(0.0, 0.15) for _ in range(hidden)] for _ in range(width)]
    bias_1 = [0.0] * hidden
    weight_2 = [[draw.gauss(0.0, 0.15) for _ in range(n_classes)] for _ in range(hidden)]
    bias_2 = [0.0] * n_classes
    for epoch in range(epochs):
        rate = 0.4 if epoch < epochs // 2 else 0.12
        grad_w1 = [[0.0] * hidden for _ in range(width)]
        grad_b1 = [0.0] * hidden
        grad_w2 = [[0.0] * n_classes for _ in range(hidden)]
        grad_b2 = [0.0] * n_classes
        for row, label in zip(train_n, train_y):
            activated = [
                math.tanh(bias_1[h] + _dot(row, [weight_1[j][h] for j in range(width)]))
                for h in range(hidden)
            ]
            logits = [
                bias_2[k] + sum(activated[h] * weight_2[h][k] for h in range(hidden))
                for k in range(n_classes)
            ]
            peak = max(logits)
            exp_shift = [math.exp(value - peak) for value in logits]
            partition = sum(exp_shift)
            probs = [value / partition for value in exp_shift]
            grad_logits = [probs[k] / n_samples for k in range(n_classes)]
            grad_logits[label] -= 1.0 / n_samples
            for h in range(hidden):
                back = sum(grad_logits[k] * weight_2[h][k] for k in range(n_classes))
                back *= 1.0 - activated[h] * activated[h]
                grad_b1[h] += back
                for j in range(width):
                    grad_w1[j][h] += row[j] * back
                for k in range(n_classes):
                    grad_w2[h][k] += activated[h] * grad_logits[k]
            for k in range(n_classes):
                grad_b2[k] += grad_logits[k]
        for j in range(width):
            for h in range(hidden):
                weight_1[j][h] -= rate * grad_w1[j][h]
        for h in range(hidden):
            bias_1[h] -= rate * grad_b1[h]
            for k in range(n_classes):
                weight_2[h][k] -= rate * grad_w2[h][k]
        for k in range(n_classes):
            bias_2[k] -= rate * grad_b2[k]
    predicted: list[int] = []
    for row in held_n:
        activated = [
            math.tanh(bias_1[h] + sum(row[j] * weight_1[j][h] for j in range(width)))
            for h in range(hidden)
        ]
        logits = [
            bias_2[k] + sum(activated[h] * weight_2[h][k] for h in range(hidden))
            for k in range(n_classes)
        ]
        best = 0
        for k in range(1, n_classes):
            if logits[k] > logits[best]:
                best = k
        predicted.append(best)
    return predicted


def route_held_out(
    train_letters: str,
    held_letters: str,
    epochs: int = ROUTER_EPOCHS,
    hidden: int = ROUTER_HIDDEN,
    seed: int = ROUTER_SEED,
    families: tuple[str, ...] | list[str] | None = None,
) -> dict[str, object]:
    """Train on Austen-derived ciphertexts and score Doyle-derived ciphertexts."""
    from engine.neural_features import feature_tables

    assert_split(train_letters, held_letters)
    assert_certificate_plaintexts_excluded(train_letters, held_letters)
    names = tuple(families) if families is not None else families_for_grade()
    english = _english_unigram(train_letters)
    tables = feature_tables(train_letters, english)
    train_x, train_y = _router_samples(
        train_letters, english, ROUTER_TRAIN_PER_CLASS, seed, names, tables
    )
    test_x, test_y = _router_samples(
        held_letters, english, ROUTER_TEST_PER_CLASS, seed + 1, names, tables
    )
    backend = "numpy"
    try:
        predicted, _weights = _fit_router_numpy(
            train_x, train_y, test_x, epochs, hidden, seed, n_classes=len(names)
        )
    except ImportError:
        # Fewer passes: the standard-library fit only has to beat chance.
        backend = "python"
        predicted = _fit_router_python(
            train_x, train_y, test_x, min(epochs, 40), hidden, seed, n_classes=len(names)
        )
        _weights = None
    correct = sum(1 for guess, truth in zip(predicted, test_y) if guess == truth)
    total = len(test_y)
    per_family: dict[str, dict[str, int]] = {}
    for class_index, family in enumerate(names):
        truths = [i for i, label in enumerate(test_y) if label == class_index]
        hits = sum(1 for i in truths if predicted[i] == class_index)
        per_family[family] = {"correct": hits, "total": len(truths)}
    return {
        "backend": backend,
        "families": list(names),
        "train_plaintext_sha256": sha256_text(train_letters),
        "heldout_plaintext_sha256": sha256_text(held_letters),
        "train_per_class": ROUTER_TRAIN_PER_CLASS,
        "test_per_class": ROUTER_TEST_PER_CLASS,
        "correct": correct,
        "total": total,
        "accuracy": correct / total,
        "chance_baseline": router_chance_baseline(len(names)),
        "per_family": per_family,
    }


def score_shipped_solver_net(held_letters: str, window: int = ROUTER_WINDOW) -> dict[str, object]:
    """Score engine.solver_net on Doyle ciphertexts. Does not edit that module.

    Training stays whatever train_solver_net does (engine/data/english.txt plus
    certificate ciphertext exemplars). The plaintexts here are the held-out
    Doyle letters, not those certificate plaintexts. Beam-search is omitted as
    a label because that module does not synthesize a separate class for it.
    """
    from engine.solver_net import ROUTED_SOLVERS, _sample_ciphertext, train_solver_net

    assert_certificate_plaintexts_excluded(held_letters)
    net = train_solver_net()
    families = [name for name in ROUTED_SOLVERS if name != "beam-search"]
    windows = _windows(held_letters, window)
    if len(windows) < 4:
        raise ValueError("not enough held-out plaintext for the shipped router")
    draw = random.Random(ROUTER_SEED + 1)
    correct = 0
    total = 0
    per_family: dict[str, dict[str, int]] = {}
    for family in families:
        hits = 0
        count = 0
        for plain in windows:
            try:
                ciphertext = _sample_ciphertext(family, plain, draw)
            except ValueError:
                continue
            if not ciphertext:
                continue
            guess = net.route(ciphertext).solver
            count += 1
            total += 1
            if guess == family:
                hits += 1
                correct += 1
        per_family[family] = {"correct": hits, "total": count}
    if total < 8:
        raise ValueError("shipped solver net produced no held-out ciphertexts")
    chance = 1.0 / len(ROUTED_SOLVERS)
    return {
        "module": "engine.solver_net",
        "edited": False,
        "train_source": "engine/data/english.txt plus certificate ciphertext exemplars",
        "heldout_plaintext_sha256": sha256_text(held_letters),
        "output_families": list(ROUTED_SOLVERS),
        "evaluated_families": families,
        "correct": correct,
        "total": total,
        "accuracy": correct / total,
        "chance_baseline": chance,
        "per_family": per_family,
    }


def _round_metrics(payload: dict) -> dict:
    """Stable floats for the metrics JSON. Counts stay integers."""

    def walk(value):
        if isinstance(value, float):
            return float(f"{value:.6f}")
        if isinstance(value, dict):
            return {key: walk(item) for key, item in value.items()}
        if isinstance(value, list):
            return [walk(item) for item in value]
        return value

    return walk(payload)


def evaluate() -> dict:
    """Run the held-out language grade and the held-out router grade."""
    train_prose = load_training_prose(TRAIN_PATH)
    held_english = load_training_prose(HELD_EN_PATH)
    held_german = load_training_prose(HELD_DE_PATH)
    train_letters = letters_az(train_prose)
    held_letters = letters_az(held_english)
    assert_split(train_letters, held_letters)
    assert_certificate_plaintexts_excluded(train_letters, held_letters)
    language = language_preference(train_prose, held_english, held_german)
    router = route_held_out(train_letters, held_letters)
    shipped = score_shipped_solver_net(held_letters)
    if language["train_letters_sha256"] != sha256_text(train_letters):
        raise ValueError("language grade did not train on the Austen letters")
    if router["train_plaintext_sha256"] != sha256_text(train_letters):
        raise ValueError("router grade did not train on the Austen letters")
    if router["heldout_plaintext_sha256"] != sha256_text(held_letters):
        raise ValueError("router grade did not evaluate on the Doyle letters")
    return _round_metrics(
        {
            "language_scorer": {
                "model": "trigram tanh hidden softmax, engine.neural.NeuralLetterModel",
                "train_source": {
                    "author": "Jane Austen",
                    "title": "Pride and Prejudice",
                    "span": "Chapters I-III, illustration blocks removed",
                    "url": TRAIN_URL,
                    "text_url": TRAIN_TEXT_URL,
                    "file": "engine/data/neural_train_austen.txt",
                },
                "heldout_english_source": {
                    "author": "Arthur Conan Doyle",
                    "title": "The Adventures of Sherlock Holmes",
                    "span": "A Scandal in Bohemia, opening, through the paragraph ending with doubts.",
                    "url": HELD_EN_URL,
                    "text_url": HELD_EN_TEXT_URL,
                    "file": "engine/data/neural_heldout_doyle.txt",
                },
                "heldout_german_source": {
                    "author": "Jacob Grimm and Wilhelm Grimm",
                    "title": "Der Wolf und die sieben jungen Geißlein",
                    "collection": "Deutsche Märchen, Project Gutenberg eBook 77905",
                    "url": HELD_DE_URL,
                    "text_url": HELD_DE_TEXT_URL,
                    "file": "engine/data/neural_heldout_grimm_wolf.txt",
                    "note": "Not the Froschkönig excerpt in engine/data/german_excerpt.txt.",
                },
                **language,
            },
            "solver_router": {
                "model": "ciphertext features plus certified look-ahead, tanh hidden softmax in engine.neural_grade",
                "note": "Separate from engine.solver_net, which is not edited. Covers certified families that module does not route.",
                "train_ciphertexts": "generated from Austen chapters I-III, not from certificate plaintexts",
                "heldout_ciphertexts": "generated from the Doyle held-out passage, not from certificate plaintexts",
                **router,
            },
            "shipped_solver_net": shipped,
            "not_a_decipherment": (
                "Does not decipher Kryptos K4, Truppenschlüssel Nr. 86, or unknown scripts."
            ),
        }
    )


def metrics_sha256(path: Path | None = None) -> str:
    raw = (path or METRICS_PATH).read_bytes()
    return hashlib.sha256(raw).hexdigest()
