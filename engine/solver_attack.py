"""A pentest of the classical solvers Bob can hand work to. Not a reading.

Caesar and Vigenere are searched. Beaufort and affine are known-key checks.
Substitution is searched on two training windows. A result is kept only when
the judge accepts the forward map. That map accepts a wrong key too, because
decrypting and encrypting with the same key rebuilds the ciphertext. The
substitution order flag is not treated as a recovery. No cutoff is fit to
these counts, and no plaintext is stored.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.ciphers import caesar_encrypt, substitution_encrypt, vigenere_encrypt
from engine.dagapeyeff_cache import frozen
from engine.neural_grade import letters_az, load_training_prose
from engine.solver_judge import judge_solve_result, reencryption_matches
from engine.solvers.affine import affine_encrypt, solve_affine
from engine.solvers.beaufort import beaufort_encrypt, solve_beaufort
from engine.solvers.caesar import solve_caesar
from engine.solvers.substitution import solve_substitution
from engine.solvers.vigenere import solve_vigenere

_SHIFTS = (3, 7, 11, 13, 17, 19, 23, 25)
_KEYS = ("KEY", "CODE", "QUARK", "LEMON", "NIGHT", "STONE")
_AFFINE = ((5, 8), (7, 3), (11, 14), (15, 2))
_PERMUTATION = "QWERTYUIOPASDFGHJKLZXCVBNM"
_WIDTH = 160
_SUB_WIDTH = 240


def harden_result(result, ciphertext: str) -> dict:
    """Keep a solver result only when the judge accepts it.

    The substitution order flag does not count as a recovery. That rule was
    declared before the drill counts. Withholding is not a higher score.
    """
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be text")
    judged = judge_solve_result(result, ciphertext)
    reading = bool(result.details.get("reading")) if isinstance(result.details, dict) else False
    return {
        "solved": False,
        "claimed_plaintext": None,
        "kept": bool(judged["accepted"]),
        "consistent": judged["reencryption_matches"] is True,
        "reading_flag": reading,
        "reading_flag_is_not_a_recovery": True,
        "blocks": judged["blocks"],
    }


def _window(prose: str, index: int, width: int) -> str:
    start = index * 350
    piece = prose[start : start + width]
    if len(piece) < width:
        raise RuntimeError("training prose is shorter than the solver drill")
    return piece


def _exact(result, original: str) -> bool:
    return letters_only(result.plaintext) == letters_only(original)


@frozen("solver-attack")
def solver_attack_report() -> dict:
    prose = letters_az(load_training_prose())
    caesar_exact = caesar_kept = 0
    caesar_delete_holds = caesar_insert_holds = caesar_reverse_holds = caesar_case_exact = 0
    for index, shift in enumerate(_SHIFTS):
        original = _window(prose, index, _WIDTH)
        cipher = caesar_encrypt(original, shift)
        result = solve_caesar(cipher)
        kept = harden_result(result, cipher)["kept"]
        caesar_kept += kept
        caesar_exact += kept and _exact(result, original) and result.key == str(shift)
        deleted = cipher[: len(cipher) // 2] + cipher[len(cipher) // 2 + 1 :]
        caesar_delete_holds += solve_caesar(deleted).key == str(shift)
        inserted = cipher[: len(cipher) // 2] + "X" + cipher[len(cipher) // 2 :]
        caesar_insert_holds += solve_caesar(inserted).key == str(shift)
        caesar_reverse_holds += solve_caesar(cipher[::-1]).key == str(shift)
        lowered = solve_caesar(cipher.lower())
        caesar_case_exact += _exact(lowered, original) and lowered.key == str(shift)
    vigenere_exact = vigenere_kept = vigenere_delete_holds = vigenere_case_exact = 0
    for index, key in enumerate(_KEYS):
        original = _window(prose, index + 8, _WIDTH)
        cipher = vigenere_encrypt(original, key)
        result = solve_vigenere(cipher)
        kept = harden_result(result, cipher)["kept"]
        vigenere_kept += kept
        vigenere_exact += kept and _exact(result, original) and result.key == key
        deleted = cipher[: len(cipher) // 2] + cipher[len(cipher) // 2 + 1 :]
        vigenere_delete_holds += solve_vigenere(deleted).key == key
        lowered = solve_vigenere(cipher.lower())
        vigenere_case_exact += _exact(lowered, original) and lowered.key == key
    cross_exact = 0
    for index, key in enumerate(_KEYS[:4]):
        original = _window(prose, index + 8, _WIDTH)
        cipher = vigenere_encrypt(original, key)
        cross_exact += _exact(solve_caesar(cipher), original)
    beaufort_exact = beaufort_wrong_exact = beaufort_wrong_consistent = 0
    for index, key in enumerate(_KEYS):
        original = _window(prose, index + 14, _WIDTH)
        cipher = beaufort_encrypt(original, key)
        result = solve_beaufort(cipher, key=key)
        judged = harden_result(result, cipher)
        beaufort_exact += judged["kept"] and _exact(result, original)
        wrong = solve_beaufort(cipher, key="QQQQ")
        wrong_judged = harden_result(wrong, cipher)
        beaufort_wrong_exact += _exact(wrong, original)
        beaufort_wrong_consistent += wrong_judged["consistent"]
    affine_exact = affine_wrong_exact = affine_wrong_consistent = 0
    for index, (multiplier, shift) in enumerate(_AFFINE):
        original = _window(prose, index + 20, _WIDTH)
        cipher = affine_encrypt(original, multiplier, shift)
        result = solve_affine(cipher, a=multiplier, b=shift)
        judged = harden_result(result, cipher)
        affine_exact += judged["kept"] and _exact(result, original)
        wrong = solve_affine(cipher, a=multiplier, b=(shift + 1) % 26)
        wrong_judged = harden_result(wrong, cipher)
        affine_wrong_exact += _exact(wrong, original)
        affine_wrong_consistent += wrong_judged["consistent"]
    substitution_exact = substitution_consistent = substitution_reading = substitution_reading_wrong = 0
    for index in range(2):
        original = _window(prose, index + 24, _SUB_WIDTH)
        cipher = substitution_encrypt(original, _PERMUTATION)
        result = solve_substitution(cipher)
        judged = harden_result(result, cipher)
        exact = _exact(result, original)
        substitution_exact += exact
        substitution_consistent += judged["consistent"]
        substitution_reading += judged["reading_flag"]
        substitution_reading_wrong += judged["reading_flag"] and not exact
    rejected = 0
    for probe in ("", "1234567890", "ABCD"):
        try:
            solve_caesar(probe) if probe != "ABCD" else solve_vigenere(probe)
        except ValueError:
            rejected += 1
    wikipedia = reencryption_matches("affine", "AFFINECIPHER", "a=5,b=8", "IHHWVCSWFRCP")
    return {
        "solved": False,
        "claimed_plaintext": None,
        "weights_replaced": False,
        "promoted_as_accuracy": False,
        "reading_flag_is_not_a_recovery": True,
        "reencryption_cannot_see_a_wrong_key": (
            beaufort_wrong_consistent == len(_KEYS) and affine_wrong_consistent == len(_AFFINE)
        ),
        "caesar_texts": len(_SHIFTS),
        "caesar_exact": caesar_exact,
        "caesar_kept": caesar_kept,
        "caesar_delete_holds": caesar_delete_holds,
        "caesar_insert_holds": caesar_insert_holds,
        "caesar_reverse_holds": caesar_reverse_holds,
        "caesar_case_exact": caesar_case_exact,
        "vigenere_texts": len(_KEYS),
        "vigenere_exact": vigenere_exact,
        "vigenere_kept": vigenere_kept,
        "vigenere_delete_holds": vigenere_delete_holds,
        "vigenere_case_exact": vigenere_case_exact,
        "caesar_on_vigenere_exact": cross_exact,
        "beaufort_texts": len(_KEYS),
        "beaufort_exact": beaufort_exact,
        "beaufort_wrong_key_exact": beaufort_wrong_exact,
        "beaufort_wrong_key_still_consistent": beaufort_wrong_consistent,
        "affine_texts": len(_AFFINE),
        "affine_exact": affine_exact,
        "affine_wrong_key_exact": affine_wrong_exact,
        "affine_wrong_key_still_consistent": affine_wrong_consistent,
        "affine_wikipedia_roundtrip": wikipedia is True,
        "substitution_texts": 2,
        "substitution_exact": substitution_exact,
        "substitution_consistent": substitution_consistent,
        "substitution_reading_flag": substitution_reading,
        "substitution_reading_but_wrong": substitution_reading_wrong,
        "rejected_inputs": rejected,
        "scope": (
            "Solver drills on training prose are forward checks. "
            "An order flag is not a recovery. Re-encryption cannot tell a wrong key from the true one, "
            "because the same key builds the ciphertext back. Nothing here is a historical decipherment."
        ),
    }
