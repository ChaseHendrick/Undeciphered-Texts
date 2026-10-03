"""Solver registry. One module per cipher, same result type."""

from __future__ import annotations

from collections.abc import Callable

from engine.result import SolveResult
from engine.solvers.caesar import solve_caesar
from engine.solvers.keyed_vigenere import solve_keyed_vigenere
from engine.solvers.substitution import solve_substitution
from engine.solvers.vigenere import solve_vigenere
from engine.solvers.two_square import climb_two_square, solve_two_square

Solver = Callable[..., SolveResult]

SOLVERS: dict[str, Solver] = {
    "caesar": solve_caesar,
    "vigenere": solve_vigenere,
    "substitution": solve_substitution,
}

__all__ = [
    "SOLVERS",
    "solve_caesar",
    "solve_keyed_vigenere",
    "solve_substitution",
    "solve_vigenere",
    "solve_two_square",
    "climb_two_square",
]
