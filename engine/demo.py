"""Generate known ciphertext, solve it without the key, and write DEMO.md."""

from __future__ import annotations

import time
from pathlib import Path

from engine.alphabet import letters_only
from engine.ciphers import caesar_encrypt, substitution_encrypt, vigenere_encrypt
from engine.fixtures import (
    CAESAR_PLAIN,
    CAESAR_SHIFT,
    DEMO_SEED,
    SUBSTITUTION_KEY,
    SUBSTITUTION_PLAIN,
    VIGENERE_KEY,
    VIGENERE_PLAIN,
)
from engine.solvers.caesar import solve_caesar
from engine.solvers.substitution import solve_substitution
from engine.solvers.vigenere import solve_vigenere
from engine.stats import friedman_period, index_of_coincidence, kasiski_factors, ngram_counts


def _letter_accuracy(expected: str, recovered: str) -> float:
    left = letters_only(expected)
    right = letters_only(recovered)
    if not left or len(left) != len(right):
        return 0.0
    hits = sum(a == b for a, b in zip(left, right))
    return hits / len(left)


def _block(title: str, body: str) -> str:
    return f"### {title}\n\n```\n{body.rstrip()}\n```\n"


def run_demo(out_path: str = "DEMO.md") -> int:
    started = time.perf_counter()
    sections: list[str] = []
    failures: list[str] = []

    caesar_ct = caesar_encrypt(CAESAR_PLAIN, CAESAR_SHIFT)
    t0 = time.perf_counter()
    caesar = solve_caesar(caesar_ct)
    caesar_dt = time.perf_counter() - t0
    caesar_ok = letters_only(caesar.plaintext) == letters_only(CAESAR_PLAIN)
    if not caesar_ok:
        failures.append("caesar")
    sections.append(
        "\n".join(
            [
                "## Caesar",
                "",
                f"- generated shift: {CAESAR_SHIFT}",
                f"- recovered shift: {caesar.details['shift']}",
                f"- chi-square of recovered text: {caesar.details['chi_square']}",
                f"- exact letter match: {caesar_ok}",
                f"- seconds: {caesar_dt:.3f}",
                "",
                _block("Ciphertext", caesar_ct),
                _block("Recovered plaintext", caesar.plaintext),
            ]
        )
    )

    vigenere_ct = vigenere_encrypt(VIGENERE_PLAIN, VIGENERE_KEY)
    v_letters = letters_only(vigenere_ct)
    t0 = time.perf_counter()
    vigenere = solve_vigenere(vigenere_ct)
    vigenere_dt = time.perf_counter() - t0
    vigenere_ok = letters_only(vigenere.plaintext) == letters_only(VIGENERE_PLAIN)
    if not vigenere_ok:
        failures.append("vigenere")
    kasiski = ", ".join(f"{period}:{votes}" for period, votes in kasiski_factors(v_letters)[:6])
    trigrams = " ".join(f"{g}:{c}" for g, c in ngram_counts(v_letters, 3, limit=6))
    sections.append(
        "\n".join(
            [
                "## Vigenère",
                "",
                f"- generated key: {VIGENERE_KEY}",
                f"- recovered key: {vigenere.key}",
                f"- recovered period: {vigenere.details['period']}",
                f"- index of coincidence: {vigenere.details['index_of_coincidence']}",
                f"- Friedman period estimate: {vigenere.details['friedman_period']}",
                f"- Kasiski (period:votes): {kasiski}",
                f"- ciphertext trigrams: {trigrams}",
                f"- exact letter match: {vigenere_ok}",
                f"- seconds: {vigenere_dt:.3f}",
                "",
                _block("Ciphertext", vigenere_ct),
                _block("Recovered plaintext", vigenere.plaintext),
            ]
        )
    )

    subst_ct = substitution_encrypt(SUBSTITUTION_PLAIN, SUBSTITUTION_KEY)
    t0 = time.perf_counter()
    subst = solve_substitution(subst_ct, seed=DEMO_SEED)
    subst_dt = time.perf_counter() - t0
    accuracy = _letter_accuracy(SUBSTITUTION_PLAIN, subst.plaintext)
    subst_ok = accuracy == 1.0
    if not subst_ok:
        failures.append("substitution")
    sections.append(
        "\n".join(
            [
                "## Simple substitution",
                "",
                f"- generated key (plain A-Z maps to): {SUBSTITUTION_KEY}",
                f"- recovered key: {subst.key}",
                f"- letter accuracy: {accuracy:.1%}",
                f"- exact letter match: {subst_ok}",
                f"- quadgram score: {subst.score:.2f}",
                f"- restarts: {subst.details['restarts']}",
                f"- anneal steps per restart: {subst.details['anneal_steps']}",
                f"- seed: {subst.details['seed']}",
                f"- seconds: {subst_dt:.3f}",
                "",
                _block("Ciphertext", subst_ct),
                _block("Recovered plaintext", subst.plaintext),
            ]
        )
    )

    elapsed = time.perf_counter() - started
    header = "\n".join(
        [
            "# Demo: recovered plaintexts",
            "",
            "Actual output of `python -m engine demo` from this directory.",
            "Each ciphertext was produced here from a known plaintext. The solver",
            "received only the ciphertext. Spaces and punctuation stay in place and",
            "are not used as word-length constraints.",
            "",
            f"- overall seconds: {elapsed:.3f}",
            f"- failures: {', '.join(failures) if failures else 'none'}",
            "",
            "Reference index of coincidence on the Vigenère letter stream is "
            f"{index_of_coincidence(v_letters):.5f}; Friedman estimate "
            f"{friedman_period(v_letters):.3f}.",
            "",
        ]
    )
    document = header.rstrip() + "\n\n" + "\n".join(sections) + "\n"
    path = Path(out_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent.parent / path
    path.write_text(document, encoding="utf-8")
    print(document)
    print(f"wrote {path.resolve()}")
    if failures:
        from engine.errors import append_error

        append_error(
            "python -m engine demo",
            "known-plaintext recovery failed: " + ", ".join(failures),
            "no",
        )
    return 1 if failures else 0
