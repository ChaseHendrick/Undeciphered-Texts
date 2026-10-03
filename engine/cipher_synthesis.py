"""Exact bounded cipher model fitting with optional Z3 SMT constraints.

A layout permutes original plaintext positions before the letter cipher.
Cribs and consensus remain in original plaintext coordinates. A satisfying
model supplies example parameters, not a recovered key. A letter is forced
only if a second solver query forbids every different value. Unknown and
exhausted checks never become evidence of unsatisfiability or uniqueness.

Official solver API: https://z3prover.github.io/api/html/classz3py_1_1_solver.html
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any, Callable

from engine.alphabet import ALPHABET
from engine.reverse_engineer import Crib


SOURCE_URL = "https://z3prover.github.io/api/html/classz3py_1_1_solver.html"
MAX_LETTERS = 512
MAX_PERIOD = 128
MAX_INSTANCES = 1024
MAX_CHECKS = 100000
MODELS = (
    "affine", "caesar", "vigenere", "beaufort", "substitution",
    "quagmire-i", "quagmire-ii", "quagmire-iii",
)
DEFAULT_MODELS = ("affine", "vigenere", "beaufort", "substitution")
_REPEATING = frozenset(("vigenere", "beaufort", "quagmire-i", "quagmire-ii", "quagmire-iii"))
_ASCII = frozenset(ALPHABET + ALPHABET.lower())
SCOPE = (
    "Exact implications only within the specified cipher families, periods, "
    "alphabet permutations, layouts and supplied cribs. Example parameters "
    "are not established keys. No unsolved plaintext or unknown-script reading is claimed."
)


class OptionalSynthesisDependencyError(RuntimeError):
    """The optional SMT engine has not been installed in the active Python."""


def _load_z3() -> Any:
    try:
        import z3
    except ImportError as exc:
        raise OptionalSynthesisDependencyError(
            "Symbolic synthesis requires optional z3-solver. "
            "Install requirements-synthesis.txt in the active Python environment."
        ) from exc
    return z3


@dataclass(frozen=True)
class SynthesizedModel:
    family: str
    period: int | None
    layout: str
    status: str
    reason: str
    example_parameters: dict | None
    parameters_are_example: bool
    forced_plaintext: str
    forced_positions: tuple[int, ...]
    consensus_complete: bool
    unknown_queries: int


@dataclass(frozen=True)
class CipherSynthesisReport:
    ciphertext_length: int
    known_positions: int
    models: tuple[SynthesizedModel, ...]
    consensus_plaintext: str
    consensus_positions: tuple[int, ...]
    consensus_basis: str
    search_complete: bool
    sat_models: int
    unsat_models: int
    unknown_models: int
    unresolved_consensus_queries: int
    solver_checks: int
    elapsed_seconds: float
    bounds: dict
    claimed_plaintext: None = None
    scope: str = SCOPE
    source_url: str = SOURCE_URL

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class _Budget:
    started: float
    timeout_seconds: float
    max_checks: int
    checks: int = 0

    def exhaustion_reason(self) -> str:
        if self.checks >= self.max_checks:
            return "check_limit"
        if monotonic() - self.started >= self.timeout_seconds:
            return "wallclock_timeout"
        return ""

    def check(self, solver: Any) -> tuple[str, str]:
        reason = self.exhaustion_reason()
        if reason:
            return "unknown", reason
        remaining = self.timeout_seconds - (monotonic() - self.started)
        if remaining <= 0:
            return "unknown", "wallclock_timeout"
        solver.set(timeout=max(1, int(remaining * 1000)))
        self.checks += 1
        status = str(solver.check())
        return status, solver.reason_unknown() if status == "unknown" else ""


def _check_solver(solver: Any, budget: _Budget) -> tuple[str, str]:
    return budget.check(solver)


def _integer(value: int, name: str, minimum: int, maximum: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be in {minimum}..{maximum}")


def _letters(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("ciphertext and crib plaintext must be strings")
    if any(ch.isalpha() and ch not in _ASCII for ch in value):
        raise ValueError("symbolic synthesis accepts only A-Z letters")
    letters = "".join(ch.upper() for ch in value if ch in _ASCII)
    if not 1 <= len(letters) <= MAX_LETTERS:
        raise ValueError(f"letter streams must contain 1..{MAX_LETTERS} A-Z letters")
    return letters


def _sequence(value: Any, name: str) -> tuple:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a finite sequence")
    return tuple(value)


def _crib_positions(cribs: Sequence[Crib], length: int) -> dict[int, int]:
    rows = _sequence(cribs, "cribs")
    if not 1 <= len(rows) <= MAX_LETTERS:
        raise ValueError(f"supply 1..{MAX_LETTERS} aligned cribs")
    known: dict[int, int] = {}
    for crib in rows:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain Crib objects")
        _integer(crib.offset, "crib offset", 0, length - 1)
        text = _letters(crib.plaintext)
        if crib.offset + len(text) > length:
            raise ValueError("crib extends beyond the plaintext letter stream")
        for index, letter in enumerate(text, start=crib.offset):
            value = ord(letter) - 65
            if index in known and known[index] != value:
                raise ValueError("overlapping cribs disagree")
            known[index] = value
    return known


def _layouts(length: int, names: Sequence[str], widths: Sequence[int]) -> tuple[tuple[str, tuple[int, ...]], ...]:
    layouts = []
    for name in dict.fromkeys(_sequence(names, "layouts")):
        if name not in ("identity", "reverse"):
            raise ValueError("layouts must be identity or reverse; use columnar_widths for columns")
        order = tuple(range(length))
        layouts.append((name, order if name == "identity" else order[::-1]))
    for width in dict.fromkeys(_sequence(widths, "columnar_widths")):
        _integer(width, "columnar width", 2, 128)
        order = tuple(index for column in range(width) for index in range(column, length, width))
        layouts.append((f"columnar:{width}", order))
    if not layouts:
        raise ValueError("at least one layout is required")
    return tuple(layouts)


@dataclass
class _Instance:
    solver: Any
    plaintext: list[Any]
    read_parameters: Callable[[Any], dict]


class _ConstructionBudgetExpired(RuntimeError):
    pass


def _build_instance(z3: Any, cipher: str, known: dict[int, int], family: str,
                    period: int | None, order: tuple[int, ...], budget: _Budget) -> _Instance:
    solver = z3.Solver()
    solver.set(random_seed=0)
    plain = []
    encoded = [ord(letter) - 65 for letter in cipher]

    def construction_checkpoint(index: int) -> None:
        if index % 16 == 0:
            reason = budget.exhaustion_reason()
            if reason:
                raise _ConstructionBudgetExpired(reason + " during model construction")

    def number(model: Any, expression: Any) -> int:
        return model.eval(expression, model_completion=True).as_long()

    def permutation(name: str) -> tuple[Any, list[Any]]:
        array = z3.Array(name, z3.IntSort(), z3.IntSort())
        values = [z3.Select(array, index) for index in range(26)]
        solver.add([z3.And(value >= 0, value < 26) for value in values])
        solver.add(z3.Distinct(values))
        return array, values

    if family in ("affine", "caesar"):
        solver = z3.Solver()
        solver.set(random_seed=0)
        a, b = z3.Ints("multiplier offset")
        choices = (1,) if family == "caesar" else (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
        solver.add(z3.Or([a == value for value in choices]), b >= 0, b < 26)
        # Known plaintext makes each branch a constant modular shift constraint.
        # Plaintext expressions use the corresponding constant modular inverse.
        derived = [None] * len(cipher)
        for index, source in enumerate(order):
            construction_checkpoint(index)
            expression = (pow(choices[-1], -1, 26) * (encoded[index] - b)) % 26
            for value in reversed(choices[:-1]):
                expression = z3.If(a == value, (pow(value, -1, 26) * (encoded[index] - b)) % 26, expression)
            derived[source] = expression
            if source in known:
                solver.add(z3.Or([z3.And(a == value, b == (encoded[index] - value * known[source]) % 26)
                                  for value in choices]))
        return _Instance(solver, derived, lambda model: {"multiplier": number(model, a), "offset": number(model, b)})

    if family == "substitution":
        solver = z3.Solver()
        solver.set(random_seed=0)
        decrypt, values = permutation("decrypt")
        derived = [None] * len(cipher)
        for index, source in enumerate(order):
            construction_checkpoint(index)
            derived[source] = z3.Select(decrypt, encoded[index])
            if source in known:
                solver.add(derived[source] == known[source])
        return _Instance(solver, derived, lambda model: {
            "decrypt_alphabet": "".join(ALPHABET[number(model, value)] for value in values),
            "key_direction": "ciphertext A-Z to plaintext",
        })

    solver = z3.Solver()
    solver.set(random_seed=0)
    key = [z3.Int(f"shift_{index}") for index in range(period)]
    solver.add([z3.And(value >= 0, value < 26) for value in key])
    if family in ("vigenere", "beaufort"):
        derived = [None] * len(cipher)
        for index, source in enumerate(order):
            construction_checkpoint(index)
            shift = key[index % period]
            derived[source] = (encoded[index] - shift if family == "vigenere" else shift - encoded[index]) % 26
            if source in known:
                required = encoded[index] - known[source] if family == "vigenere" else encoded[index] + known[source]
                solver.add(shift == required % 26)
        return _Instance(solver, derived, lambda model: {"key": "".join(ALPHABET[number(model, value)] for value in key)})

    # Ranks map A-Z letter values to indices in an unknown keyed alphabet.
    rank, ranks = permutation("alphabet_rank")
    # Rotating an alphabet does not change the model class: its phase can
    # compensate in I/II, and rank differences are rotation invariant in III.
    solver.add(ranks[0] == 0)
    derived = [None] * len(cipher)

    def inverse_rank(target: Any) -> Any:
        expression = z3.IntVal(25)
        for letter in reversed(range(25)):
            expression = z3.If(ranks[letter] == target, letter, expression)
        return expression

    for index, source in enumerate(order):
        construction_checkpoint(index)
        shift = key[index % period]
        if family == "quagmire-ii":
            derived[source] = (ranks[encoded[index]] - shift) % 26
            if source in known:
                solver.add(ranks[encoded[index]] == (known[source] + shift) % 26)
        else:
            cipher_rank = encoded[index] if family == "quagmire-i" else ranks[encoded[index]]
            derived[source] = inverse_rank((cipher_rank - shift) % 26)
            if source in known:
                solver.add(cipher_rank == (ranks[known[source]] + shift) % 26)
    plain = derived

    def quagmire_parameters(model: Any) -> dict:
        alphabet = [""] * 26
        for letter, value in zip(ALPHABET, ranks):
            alphabet[number(model, value)] = letter
        mixed = "".join(alphabet)
        plain_alphabet = ALPHABET if family == "quagmire-ii" else mixed
        cipher_alphabet = ALPHABET if family == "quagmire-i" else mixed
        shifts = [number(model, value) for value in key]
        # Under=A loses no row settings because the indicator can be adjusted.
        under_index = plain_alphabet.index("A")
        indicator = "".join(cipher_alphabet[(shift + under_index) % 26] for shift in shifts)
        return {"plaintext_alphabet": plain_alphabet, "ciphertext_alphabet": cipher_alphabet,
                "indicator": indicator, "indicator_under": "A", "effective_shifts": shifts}

    return _Instance(solver, plain, quagmire_parameters)


def _unknown(family: str, period: int | None, layout: str, reason: str,
             known_text: str, known: dict[int, int]) -> SynthesizedModel:
    return SynthesizedModel(family, period, layout, "unknown", reason, None, False,
                            known_text, tuple(sorted(known)), False, len(known_text) - len(known))


def synthesize_cipher_models(
    ciphertext: str,
    *,
    cribs: Sequence[Crib],
    models: Sequence[str] = DEFAULT_MODELS,
    max_period: int = 4,
    layouts: Sequence[str] = ("identity", "reverse"),
    columnar_widths: Sequence[int] = (),
    timeout_seconds: float = 5.0,
    max_checks: int = 10000,
) -> CipherSynthesisReport:
    """Fit finite model classes and prove their conditional plaintext consensus.

    All timeouts share a single monotonic deadline. Solver checks receive
    only the remaining milliseconds. Model construction is bounded by input
    and instance caps. Optional Z3 is imported only when this function runs.
    """
    started = monotonic()
    _integer(max_period, "max_period", 1, MAX_PERIOD)
    _integer(max_checks, "max_checks", 1, MAX_CHECKS)
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
        raise TypeError("timeout_seconds must be a number")
    if not math.isfinite(timeout_seconds) or not 0 < timeout_seconds <= 60:
        raise ValueError("timeout_seconds must be finite and in (0, 60]")
    cipher = _letters(ciphertext)
    known = _crib_positions(cribs, len(cipher))
    families = tuple(dict.fromkeys(_sequence(models, "models")))
    if not families or any(family not in MODELS for family in families):
        raise ValueError("models must contain supported cipher family names")
    layout_orders = _layouts(len(cipher), layouts, columnar_widths)
    period_bound = min(max_period, len(cipher))
    specifications = [(family, period, layout, order) for family in families
                      for period in (range(1, period_bound + 1) if family in _REPEATING else (None,))
                      for layout, order in layout_orders]
    if len(specifications) > MAX_INSTANCES:
        raise ValueError(f"requested model classes exceed the {MAX_INSTANCES} instance limit")
    known_text = "".join(ALPHABET[known[index]] if index in known else "?" for index in range(len(cipher)))
    z3 = _load_z3()
    budget = _Budget(started, float(timeout_seconds), max_checks)
    results = []
    for family, period, layout, order in specifications:
        reason = budget.exhaustion_reason()
        if reason:
            results.append(_unknown(family, period, layout, reason, known_text, known))
            continue
        try:
            instance = _build_instance(z3, cipher, known, family, period, order, budget)
        except _ConstructionBudgetExpired as exc:
            results.append(_unknown(family, period, layout, str(exc), known_text, known))
            continue
        status, reason = _check_solver(instance.solver, budget)
        if status == "unknown":
            results.append(_unknown(family, period, layout, reason, known_text, known))
            continue
        if status == "unsat":
            results.append(SynthesizedModel(family, period, layout, status, "", None, False,
                                            "?" * len(cipher), (), True, 0))
            continue
        if status != "sat":
            raise RuntimeError(f"unexpected SMT status: {status}")
        example = instance.solver.model()
        parameters = instance.read_parameters(example)
        forced = list(known_text)
        pending = [index for index in range(len(cipher)) if index not in known]
        unknown_queries = 0
        unknown_reasons = []
        for pending_index, index in enumerate(pending):
            reason = budget.exhaustion_reason()
            if reason:
                unknown_queries += len(pending) - pending_index
                unknown_reasons.append(reason)
                break
            value = example.eval(instance.plaintext[index], model_completion=True).as_long()
            instance.solver.push()
            try:
                instance.solver.add(instance.plaintext[index] != value)
                alternative, query_reason = _check_solver(instance.solver, budget)
            finally:
                instance.solver.pop()
            if alternative == "unsat":
                forced[index] = ALPHABET[value]
            elif alternative == "unknown":
                unknown_queries += 1
                unknown_reasons.append(query_reason or "solver returned unknown")
            elif alternative != "sat":
                raise RuntimeError(f"unexpected SMT status: {alternative}")
        results.append(SynthesizedModel(
            family, period, layout, "sat", "; ".join(dict.fromkeys(unknown_reasons)), parameters, True,
            "".join(forced), tuple(index for index, letter in enumerate(forced) if letter != "?"),
            unknown_queries == 0, unknown_queries,
        ))
    sat = [row for row in results if row.status == "sat"]
    unknown = sum(row.status == "unknown" for row in results)
    complete = not unknown and all(row.consensus_complete for row in sat)
    consensus = list(known_text)
    basis = "supplied cribs only; model or consensus checks remain unresolved"
    if complete and sat:
        for index in range(len(cipher)):
            choices = {row.forced_plaintext[index] for row in sat}
            if len(choices) == 1 and "?" not in choices:
                consensus[index] = choices.pop()
        basis = "forced in every satisfiable class within the reported model and layout bounds"
    elif complete:
        basis = "supplied cribs only; all tested model classes are unsatisfiable"
    return CipherSynthesisReport(
        ciphertext_length=len(cipher), known_positions=len(known), models=tuple(results),
        consensus_plaintext="".join(consensus),
        consensus_positions=tuple(index for index, letter in enumerate(consensus) if letter != "?"),
        consensus_basis=basis, search_complete=complete, sat_models=len(sat),
        unsat_models=sum(row.status == "unsat" for row in results), unknown_models=unknown,
        unresolved_consensus_queries=sum(row.unknown_queries for row in results),
        solver_checks=budget.checks, elapsed_seconds=monotonic() - started,
        bounds={"families": list(families), "max_period": max_period, "tested_period_bound": period_bound,
                "layouts": [name for name, _order in layout_orders], "timeout_seconds": float(timeout_seconds),
                "max_checks": max_checks, "model_classes": len(specifications), "max_letters": MAX_LETTERS,
                "alphabet_size": 26, "composition_order": "layout first, then letter cipher"},
    )


__all__ = [
    "CipherSynthesisReport", "DEFAULT_MODELS", "MODELS", "OptionalSynthesisDependencyError",
    "SynthesizedModel", "synthesize_cipher_models",
]
