"""Homophonic substitution attack by simulated annealing at a fixed temperature.

Method, fetched 2026-10-02, from Nils Kopal, "Cryptanalysis of Homophonic
Substitution Ciphers Using Simulated Annealing with Fixed Temperature",
Proceedings of the 2nd International Conference on Historical Cryptology
(HistoCrypt 2019), Linkoping University Electronic Press, pages 107-116:

  https://ep.liu.se/ecp/158/012/ecp19158012.pdf

Section 5.2 keeps a key that maps each ciphertext homophone to a plaintext
letter. The key is longer than the set of observed homophones (about 1.3
times that set) so spare slots can hold letters that are not in the active
map. The start key is drawn at random with the English unigram distribution,
so E is more common in the key than X. Search swaps two key entries. The
fitness is a sum of natural-log n-gram scores. Kopal sums log pentagrams.
This small version sums the quadgram log-likelihood already fitted in
engine.language, which is the same kind of score on a shorter model.

Section 5.3 accepts a swap with a simulated-annealing test whose temperature
does not cool:

  if new_score > current_score: accept
  degradation = current_score - new_score
  acceptance_probability = exp(-degradation / fixed_temperature)
  accept if acceptance_probability > 0.0085 and a uniform draw falls below it
  otherwise reject

Kopal reports a user-chosen scale of 500000 on pentagram sums and a
user-chosen temperature of 15000. Both numbers are parameters, not part of
the ciphertext. On unscaled quadgram sums the temperature used here is 2.0,
which is the same acceptance rule on this fixture.

If 500 proposals pass with no new global best, the last three key letters are
replaced with fresh draws. That is section 5.2 step 9. Kopal counts a stall
of 100 tries on a full pair sweep; this sampler counts proposals.

After annealing, a hill climb writes each homophone to the single plaintext
letter that most raises the quadgram sum, and repeats until no letter change
helps. One homophone changing its plaintext letter is the edit Kopal's spare
slots and manual correction both apply.

The unit-test ciphertext is constructed, not historical. E is given two
homophones and every other letter that occurs is given one. Homophones are
taken in turn so the ciphertext is fixed. The search is not given that table.

This is a known-cipher demonstration on that fixture. It does not solve army
message Nr. 86, Kryptos K4, or an unknown script.
"""

from __future__ import annotations

import math
import random

from engine.alphabet import letters_only
from engine.language import UNIGRAM, get_model
from engine.result import SolveResult

PAPER_URL = "https://ep.liu.se/ecp/158/012/ecp19158012.pdf"
PAPER_YEAR = 2019
PAPER_TITLE = (
    "Cryptanalysis of Homophonic Substitution Ciphers "
    "Using Simulated Annealing with Fixed Temperature"
)
FIXED_TEMPERATURE = 2.0
ACCEPT_FLOOR = 0.0085
STALL_LIMIT = 500
DEFAULT_STEPS = 20000
DEFAULT_SEED = 3

# Constructed fixture. Not a historical ciphertext and not printed in the paper.
FIXTURE_SENTENCE = (
    "A baker on Pine Street rolled dough before dawn and set the loaves near the open window so the crust would dry. "
    "She kept a tally of rye and wheat and marked the board when the oven was hot enough. "
    "The early customers wanted rolls with butter and a cup of tea. "
    "A quiet dog slept by the door until the bell rang and the street filled with carts. "
    "After noon the same baker wrapped two extra loaves and walked them to the school on the hill. "
    "Children waited by the gate and traded stories about the river. "
    "The baker smiled, counted the coins, and turned back before the rain reached Pine Street."
)
DOUBLED_LETTERS = "E"

_SCOPE = (
    "Constructed homophonic substitution fixture only; "
    "not a solution of army message Nr. 86, Kryptos K4, or an unknown script."
)


def fixture_plaintext() -> str:
    """A-Z letters of the constructed sentence."""
    return letters_only(FIXTURE_SENTENCE)


def homophone_table(plaintext: str, doubled: str = DOUBLED_LETTERS) -> dict[str, list[str]]:
    """Two-digit homophones. Letters in `doubled` that occur get two codes.

    Codes are assigned in alphabet order so the table does not depend on
    a random draw. Letters that do not occur are omitted.
    """
    present = sorted(set(letters_only(plaintext)))
    if not present:
        raise ValueError("plaintext must contain a letter")
    extra = set(letters_only(doubled))
    table: dict[str, list[str]] = {}
    cursor = 0
    for letter in present:
        count = 2 if letter in extra else 1
        table[letter] = [f"{cursor + offset:02d}" for offset in range(count)]
        cursor += count
    return table


def flatten_mapping(table: dict[str, list[str]]) -> dict[str, str]:
    """Map each homophone code back to its plaintext letter."""
    mapping: dict[str, str] = {}
    for letter, codes in table.items():
        for code in codes:
            mapping[code] = letter
    return mapping


def homophonic_encrypt(plaintext: str, table: dict[str, list[str]] | None = None) -> str:
    """Round-robin homophones, space-separated two-digit codes.

    Round-robin is only how this fixture is built. The paper attacks a
    ciphertext; it does not define this encipherment.
    """
    letters = letters_only(plaintext)
    if not letters:
        raise ValueError("plaintext must contain a letter")
    if table is None:
        table = homophone_table(letters)
    cursors = {letter: 0 for letter in table}
    tokens: list[str] = []
    for letter in letters:
        codes = table.get(letter)
        if not codes:
            raise ValueError(f"no homophone for {letter}")
        tokens.append(codes[cursors[letter] % len(codes)])
        cursors[letter] += 1
    return " ".join(tokens)


def homophonic_decrypt(ciphertext: str, mapping: dict[str, str]) -> str:
    """Apply a homophone-to-letter map. Unknown codes raise."""
    tokens = _tokens(ciphertext)
    letters: list[str] = []
    for token in tokens:
        letter = mapping.get(token)
        if letter is None or len(letter) != 1 or not letter.isalpha():
            raise ValueError(f"no plaintext letter for homophone {token}")
        letters.append(letter.upper())
    return "".join(letters)


def accepts_swap(
    new_score: float,
    current_score: float,
    draw: float,
    temperature: float = FIXED_TEMPERATURE,
    floor: float = ACCEPT_FLOOR,
) -> bool:
    """Section 5.3 fixed-temperature test. `draw` is uniform on [0, 1)."""
    if temperature <= 0:
        raise ValueError("fixed temperature must be positive")
    if new_score > current_score:
        return True
    degradation = current_score - new_score
    probability = math.exp(-degradation / temperature)
    return probability > floor and draw < probability


def solve_homophonic_fixed_temperature(
    ciphertext: str,
    seed: int = DEFAULT_SEED,
    steps: int = DEFAULT_STEPS,
    temperature: float = FIXED_TEMPERATURE,
) -> SolveResult:
    """Recover plaintext letters with the fixed-temperature homophonic search.

    `seed` makes the English-weighted start key and the swap draws repeatable.
    The default seed and step count recover the constructed fixture.
    """
    tokens = _tokens(ciphertext)
    symbols = sorted(set(tokens))
    if len(tokens) < 40:
        raise ValueError("ciphertext is too short for this homophonic search (need at least 40 symbols)")
    if temperature <= 0:
        raise ValueError("fixed temperature must be positive")
    index = {symbol: position for position, symbol in enumerate(symbols)}
    ids = [index[token] for token in tokens]
    n_symbols = len(symbols)
    model = get_model()
    logp = model.logp
    positions = _positions(ids, n_symbols)
    rng = random.Random(seed)
    tail = max(3, math.ceil(n_symbols * 0.3))
    key = [_sample_unigram(rng) for _ in range(n_symbols + tail)]
    plain = [key[symbol] for symbol in ids]
    current = _score(plain, logp)
    best = current
    best_key = key[:]
    stale = 0
    key_length = n_symbols + tail
    for _ in range(steps):
        left = rng.randrange(n_symbols)
        right = rng.randrange(key_length)
        if left == right or key[left] == key[right]:
            continue
        old_left = key[left]
        old_right = key[right]
        trial = _assign(plain, current, positions, logp, left, old_right)
        key[left] = old_right
        if right < n_symbols:
            trial = _assign(plain, trial, positions, logp, right, old_left)
            key[right] = old_left
        else:
            key[right] = old_left
        if accepts_swap(trial, current, rng.random(), temperature):
            current = trial
            if current > best:
                best = current
                best_key = key[:]
                stale = 0
            else:
                stale += 1
        else:
            if right < n_symbols:
                trial = _assign(plain, trial, positions, logp, right, old_right)
                key[right] = old_right
            else:
                key[right] = old_right
            current = _assign(plain, trial, positions, logp, left, old_left)
            key[left] = old_left
            stale += 1
        if stale >= STALL_LIMIT:
            for offset in range(1, 4):
                key[-offset] = _sample_unigram(rng)
            stale = 0
    key = best_key[:]
    plain = [key[symbol] for symbol in ids]
    current = _score(plain, logp)
    _hill_climb(plain, key, current, positions, logp, n_symbols)
    current = _score(plain, logp)
    recovered = "".join(chr(65 + letter) for letter in plain)
    mapping = {symbol: chr(65 + key[index[symbol]]) for symbol in symbols}
    return SolveResult(
        method="homophonic_fixed_temperature",
        plaintext=recovered,
        key=" ".join(f"{symbol}={mapping[symbol]}" for symbol in symbols),
        score=current,
        details={
            "source_url": PAPER_URL,
            "year": PAPER_YEAR,
            "temperature": temperature,
            "accept_floor": ACCEPT_FLOOR,
            "seed": seed,
            "steps": steps,
            "symbols": n_symbols,
            "scope": _SCOPE,
            "fitness": "quadgram_log_likelihood",
        },
    )


def _tokens(ciphertext: str) -> list[str]:
    tokens = ciphertext.split()
    if not tokens:
        raise ValueError("ciphertext must contain homophone tokens")
    return tokens


def _positions(ids: list[int], n_symbols: int) -> list[list[int]]:
    found = [[] for _ in range(n_symbols)]
    for position, symbol in enumerate(ids):
        found[symbol].append(position)
    return found


def _sample_unigram(rng: random.Random) -> int:
    draw = rng.random()
    acc = 0.0
    for index, weight in enumerate(UNIGRAM):
        acc += weight
        if draw <= acc:
            return index
    return 25


def _quad(a: int, b: int, c: int, d: int) -> int:
    return ((a * 26 + b) * 26 + c) * 26 + d


def _score(plain: list[int], logp: list[float]) -> float:
    total = 0.0
    for index in range(3, len(plain)):
        total += logp[_quad(plain[index - 3], plain[index - 2], plain[index - 1], plain[index])]
    return total


def _assign(
    plain: list[int],
    score: float,
    positions: list[list[int]],
    logp: list[float],
    symbol: int,
    letter: int,
) -> float:
    starts: set[int] = set()
    limit = len(plain) - 3
    for position in positions[symbol]:
        for start in range(max(0, position - 3), min(position + 1, limit)):
            starts.add(start)
    for start in starts:
        score -= logp[_quad(plain[start], plain[start + 1], plain[start + 2], plain[start + 3])]
    for position in positions[symbol]:
        plain[position] = letter
    for start in starts:
        score += logp[_quad(plain[start], plain[start + 1], plain[start + 2], plain[start + 3])]
    return score


def _hill_climb(
    plain: list[int],
    key: list[int],
    score: float,
    positions: list[list[int]],
    logp: list[float],
    n_symbols: int,
) -> float:
    changed = True
    passes = 0
    while changed and passes < 30:
        changed = False
        passes += 1
        for symbol in range(n_symbols):
            base = key[symbol]
            best_letter = base
            best_score = score
            for letter in range(26):
                if letter == base:
                    continue
                trial = _assign(plain, score, positions, logp, symbol, letter)
                if trial > best_score + 1e-9:
                    best_score = trial
                    best_letter = letter
                _assign(plain, trial, positions, logp, symbol, base)
            if best_letter != base:
                score = _assign(plain, score, positions, logp, symbol, best_letter)
                key[symbol] = best_letter
                changed = True
    return score
