"""Command line: python -m engine analyze|solve|demo."""

from __future__ import annotations

import argparse
import sys

from engine.alphabet import letters_only
from engine.solvers import SOLVERS
from engine.stats import (
    column_mean_ic,
    friedman_period,
    index_of_coincidence,
    kasiski_factors,
    ngram_counts,
)


def _read_text(value: str | None) -> str:
    if value is not None:
        return value
    return sys.stdin.read()


def _cmd_analyze(text: str, max_period: int) -> int:
    letters = letters_only(text)
    if not letters:
        print("no letters in input", file=sys.stderr)
        return 2
    ic = index_of_coincidence(letters)
    print(f"letters: {len(letters)}")
    print(f"index_of_coincidence: {ic:.5f}")
    print(f"english_ic: 0.06670  random_ic: {1/26:.5f}")
    print(f"friedman_period: {friedman_period(letters):.3f}")
    print("kasiski:")
    factors = kasiski_factors(letters, max_period=max_period)
    if not factors:
        print("  (no repeated n-grams)")
    for period, votes in factors[:10]:
        col = column_mean_ic(letters, period)
        print(f"  period {period:2d}  votes {votes:4d}  column_ic {col:.5f}")
    for n in (1, 2, 3, 4):
        top = ngram_counts(letters, n, limit=8)
        rendered = " ".join(f"{gram}:{count}" for gram, count in top)
        print(f"{n}-grams: {rendered}")
    return 0


def _cmd_solve(method: str, text: str, args: argparse.Namespace) -> int:
    solver = SOLVERS[method]
    if method == "vigenere":
        result = solver(text, max_period=args.max_period)
    elif method == "substitution":
        result = solver(text, restarts=args.restarts, steps=args.steps, seed=args.seed)
    else:
        result = solver(text)
    print(result.summary())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m engine",
        description="Recover classical ciphers with IC, Kasiski, n-grams, and search.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="IC, Friedman, Kasiski, and n-gram counts")
    analyze.add_argument("text", nargs="?", help="ciphertext; omit to read stdin")
    analyze.add_argument("--max-period", type=int, default=16)

    solve = sub.add_parser("solve", help="recover plaintext")
    solve.add_argument("method", choices=sorted(SOLVERS))
    solve.add_argument("text", nargs="?", help="ciphertext; omit to read stdin")
    solve.add_argument("--max-period", type=int, default=12)
    solve.add_argument("--restarts", type=int, default=10)
    solve.add_argument("--steps", type=int, default=4000)
    solve.add_argument("--seed", type=int, default=20261002)

    demo = sub.add_parser("demo", help="encrypt known text, solve it, write DEMO.md")
    demo.add_argument("--out", default="DEMO.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "demo":
        from engine.demo import run_demo

        return run_demo(args.out)
    text = _read_text(args.text)
    if args.command == "analyze":
        return _cmd_analyze(text, args.max_period)
    return _cmd_solve(args.method, text, args)
