"""K4 periodic substitution with arbitrary alphabets: a bijection bound.

A periodic polyalphabetic cipher uses one fixed substitution per column,
position mod the period. Nothing is assumed about those alphabets, so the
bound covers Quagmire I to IV with any keyword, keyed Vigenere, Beaufort,
Porta and any other in-place periodic substitution.

Inside one column the substitution is a bijection. Two crib letters in the
same column with equal plaintext must have equal ciphertext, and the other
way round. One such contradiction blocks the period for every alphabet.

Both clues are used jointly here; an open period is only not blocked, not fitted.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

from engine.k4_gromark_obstruction import CRIB_SPANS, crib_pairs
from engine.solvers.k4_attempt import K4_CIPHERTEXT


def column_contradiction(pairs, period: int):
    """First pair of crib letters that break a column bijection, or None."""
    for a, (i, cipher_i, plain_i) in enumerate(pairs):
        for j, cipher_j, plain_j in pairs[a + 1 :]:
            if (i - j) % period == 0 and (plain_i == plain_j) != (cipher_i == cipher_j):
                return (i, plain_i, cipher_i, j, plain_j, cipher_j)
    return None


def scan_periods(ciphertext: str = K4_CIPHERTEXT, spans=CRIB_SPANS, max_period: int = 97) -> dict:
    pairs = crib_pairs(ciphertext, spans)
    blocked, open_periods, witnesses = [], [], {}
    for period in range(1, max_period + 1):
        witness = column_contradiction(pairs, period)
        if witness is None:
            open_periods.append(period)
        else:
            blocked.append(period)
            witnesses[period] = witness
    return {
        "model": "periodic substitution, arbitrary alphabet per column, in place",
        "blocked": blocked,
        "open": open_periods,
        "witnesses": witnesses,
        "solved": False,
        "claimed_plaintext": None,
    }


if __name__ == "__main__":
    report = scan_periods()
    print("blocked:", report["blocked"])
    print("open:", report["open"])
    for period, (i, p, c, j, q, d) in report["witnesses"].items():
        print(f"period {period}: pt {p}@{i}->ct {c}, pt {q}@{j}->ct {d}")
