"""Command line for cipher analysis, bounded search, and demonstrations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from engine.alphabet import letters_only
from engine.cipher_synthesis import OptionalSynthesisDependencyError
from engine.solvers import SOLVERS
from engine.solvers.keyed_vigenere import solve_keyed_vigenere
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
    if method == "keyed-vigenere":
        if not args.key or args.alphabet is None:
            print("keyed-vigenere requires --key and --alphabet", file=sys.stderr)
            return 2
        result = solve_keyed_vigenere(
            text,
            key=args.key,
            alphabet_keyword=args.alphabet,
            index_letter=args.index,
        )
        print(result.summary())
        return 0
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
        description="Analyze ciphers and run bounded classical searches or constraint models.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("tools", help="list connected tools, modes, and required parameters as JSON")
    invoke = sub.add_parser("run", help="invoke a connected tool with explicit JSON parameters")
    invoke.add_argument("tool")
    invoke.add_argument("text", nargs="?", help="input text, hex, or integer; omit to read stdin")
    invoke.add_argument("--params", default="{}", help="JSON object of the selected tool's parameters")
    route = sub.add_parser("route", help="rank trained cipher families with the calibrated neural ensemble")
    route.add_argument("text", nargs="?", help="A-Z ciphertext; omit to read stdin")
    investigate = sub.add_parser("investigate", help="record bounded hypotheses, evidence, and a research plan")
    investigate.add_argument("text", nargs="?")
    investigate.add_argument("--crib", action="append", default=[], metavar="OFFSET:TEXT")
    investigate.add_argument("--max-checks", type=int, default=5000)
    investigate.add_argument("--max-candidates", type=int, default=20)
    investigate.add_argument("--lexicon", type=Path, help="UTF-8 word list for numeric Morse inference")
    investigate.add_argument("--temperament", choices=("balanced", "cautious", "curious"), default="balanced")
    train = sub.add_parser("train-router", help="run one bounded local residual-router training pass")
    train.add_argument("--epochs", type=int, default=200)
    train.add_argument("--samples", type=int, default=128, help="training samples per generated family")
    train.add_argument("--expanded-families", action="store_true", help="also evaluate Condi, Progressive Key and Redefence classes")
    train.add_argument("--hidden", type=int, default=64, help="residual layer width, 2..256")
    train.add_argument("--ensemble-size", type=int, default=3, help="independent seeded members, 1..5")
    train.add_argument("--warm-start", action="store_true",
                       help="start from the compatible incumbent with unchanged families, hidden width, ensemble size and training tables")
    train.add_argument("--learning-rate", type=float, default=.01,
                       help="maximum cosine-schedule rate, finite and in (0,0.1] (default:0.01)")
    train.add_argument("--distillation-strength", type=float, default=0.0,
                       help="optional frozen-incumbent teacher KL weight; requires --warm-start (default:0)")
    train.add_argument("--distillation-temperature", type=float, default=2.0,
                       help="teacher/student softening temperature (default:2)")
    train.add_argument("--feature-version", default=None,
                       help="cipher statistics version; default is the current feature set")
    train.add_argument("--dry-run", action="store_true", help="evaluate without writing artifacts")

    analyze = sub.add_parser("analyze", help="IC, Friedman, Kasiski, and n-gram counts")
    analyze.add_argument("text", nargs="?", help="ciphertext; omit to read stdin")
    analyze.add_argument("--max-period", type=int, default=16)

    solve = sub.add_parser("solve", help="recover plaintext")
    solve.add_argument("method", choices=sorted([*SOLVERS, "keyed-vigenere"]))
    solve.add_argument("text", nargs="?", help="ciphertext; omit to read stdin")
    solve.add_argument("--max-period", type=int, default=12)
    solve.add_argument("--restarts", type=int, default=10)
    solve.add_argument("--steps", type=int, default=4000)
    solve.add_argument("--seed", type=int, default=20261002)
    solve.add_argument("--key", help="repeating key for keyed-vigenere")
    solve.add_argument(
        "--alphabet",
        help="alphabet keyword for keyed-vigenere (keyword, then remaining A-Z)",
    )
    solve.add_argument(
        "--index",
        help="index letter for keyed-vigenere (default: first letter of the mixed alphabet)",
    )

    reverse = sub.add_parser("reverse-engineer", help="fit bounded cipher hypotheses to aligned cribs")
    reverse.add_argument("text", nargs="?", help="ciphertext; omit to read stdin")
    reverse.add_argument("--crib", action="append", required=True, metavar="OFFSET:TEXT",
                         help="zero-based offset in the A-Z stream and known plaintext; repeat for multiple cribs")
    reverse.add_argument("--max-period", type=int, default=None,
                         help="maximum repeating period (default: 16 baseline, 4 symbolic)")
    reverse.add_argument("--symbolic", action="store_true",
                         help="use optional Z3 for exact constraints and plaintext consensus")
    reverse.add_argument("--model", action="append",
                         choices=("affine", "caesar", "substitution", "vigenere", "beaufort",
                                  "quagmire-i", "quagmire-ii", "quagmire-iii"),
                         help="symbolic cipher family; repeat to select several")
    reverse.add_argument("--layout", action="append", choices=("identity", "reverse"),
                         help="symbolic layout before letter encryption; default: both")
    reverse.add_argument("--columnar-width", action="append", type=int,
                         help="also test row-fill, column-takeoff layouts at this width")
    reverse.add_argument("--timeout-seconds", type=float, default=None,
                         help="total symbolic wall time, at most 60 seconds (default: 5)")
    reverse.add_argument("--max-checks", type=int, default=None,
                         help="maximum symbolic satisfiability checks (default: 10000)")

    pattern = sub.add_parser("word-pattern", help="bounded substitution search with a supplied word list")
    pattern.add_argument("text", nargs="?", help="word-separated ciphertext; omit to read stdin")
    pattern.add_argument("--lexicon", required=True, help="UTF-8 file of whitespace-separated A-Z words")
    pattern.add_argument("--max-nodes", type=int, default=10000)
    pattern.add_argument("--max-candidates", type=int, default=20)

    demo = sub.add_parser("demo", help="encrypt known text, solve it, write DEMO.md")
    demo.add_argument("--out", default="DEMO.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "demo":
        from engine.demo import run_demo

        return run_demo(args.out)
    if args.command == "tools":
        from engine.tool_registry import list_tools
        print(json.dumps(list_tools(), indent=2))
        return 0
    if args.command == "train-router":
        try:
            from engine.neural_router_v2 import train_router
            teacher_options = {}
            if args.distillation_strength != 0.0 or args.distillation_temperature != 2.0:
                teacher_options = {"distillation_strength": args.distillation_strength,
                                   "distillation_temperature": args.distillation_temperature}
            print(json.dumps(train_router(epochs=args.epochs, train_per_class=args.samples,
                                          write=not args.dry_run, expanded_families=args.expanded_families,
                                          hidden=args.hidden, ensemble_size=args.ensemble_size,
                                          warm_start=args.warm_start, learning_rate=args.learning_rate,
                                          feature_version=args.feature_version,
                                          **teacher_options), indent=2))
            return 0
        except (ValueError, TypeError, ImportError, OSError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
    if args.command in {"run", "route", "investigate"}:
        try:
            text = args.text if args.text is not None else sys.stdin.read(8193)
            if len(text) > 8192:
                raise ValueError("input exceeds8192 characters")
            if args.command == "investigate":
                from engine.solver_reasoning import investigate_cipher
                from engine.reverse_engineer import Crib
                cribs = []
                for value in args.crib:
                    offset, separator, plaintext = value.partition(":")
                    if not separator:
                        raise ValueError("crib must be OFFSET:TEXT")
                    cribs.append(Crib(int(offset), plaintext))
                lexicon = None
                if args.lexicon is not None:
                    with args.lexicon.open(encoding="utf-8") as handle:
                        lexicon_text = handle.read(1_048_577)
                    if len(lexicon_text) > 1_048_576:
                        raise ValueError("lexicon exceeds 1 MiB")
                    lexicon = lexicon_text.split()
                output = investigate_cipher(text, cribs=cribs, lexicon=lexicon,
                    max_checks=args.max_checks, max_candidates=args.max_candidates,
                    temperament=args.temperament).to_dict()
            elif args.command == "route":
                from engine.neural_router_v2 import route_probabilities
                output = route_probabilities(text)
            else:
                from engine.tool_registry import TOOLS, run_tool
                if len(args.params) > 65536:
                    raise ValueError("parameter JSON exceeds64 KiB")
                params = json.loads(args.params)
                if args.tool in TOOLS and TOOLS[args.tool].encoding == "integer":
                    text = int(text)
                output = run_tool(args.tool, text, params=params)
            print(json.dumps(output, indent=2, allow_nan=False))
            return 0
        except (ValueError, TypeError, ImportError, OSError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
    text = _read_text(args.text)
    if args.command == "word-pattern":
        from engine.solvers.word_pattern import solve_word_pattern

        try:
            words = Path(args.lexicon).read_text(encoding="utf-8").split()
            result = solve_word_pattern(text, words, max_nodes=args.max_nodes,
                                        max_candidates=args.max_candidates)
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps({"method": result.method, "plaintext": result.plaintext,
                          "key": result.key, "details": result.details}, indent=2))
        return 0
    if args.command == "reverse-engineer":
        from engine.reverse_engineer import Crib, infer_cipher_models

        try:
            cribs = []
            for value in args.crib:
                offset, separator, plaintext = value.partition(":")
                if not separator:
                    raise ValueError("--crib must be OFFSET:TEXT")
                cribs.append(Crib(int(offset), plaintext))
            if args.symbolic:
                from engine.cipher_synthesis import synthesize_cipher_models

                report = synthesize_cipher_models(
                    text, cribs=cribs,
                    models=tuple(args.model or ("affine", "vigenere", "beaufort", "substitution")),
                    max_period=4 if args.max_period is None else args.max_period,
                    layouts=tuple(args.layout or ("identity", "reverse")),
                    columnar_widths=tuple(args.columnar_width or ()),
                    timeout_seconds=5.0 if args.timeout_seconds is None else args.timeout_seconds,
                    max_checks=10000 if args.max_checks is None else args.max_checks,
                )
            else:
                if args.model or args.layout or args.columnar_width or args.timeout_seconds is not None or args.max_checks is not None:
                    raise ValueError("--model, --layout, --columnar-width, --timeout-seconds, and --max-checks require --symbolic")
                report = infer_cipher_models(text, cribs=cribs,
                                            max_period=16 if args.max_period is None else args.max_period)
        except (ValueError, TypeError, ImportError, OptionalSynthesisDependencyError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(report.to_dict(), indent=2))
        return 0
    if args.command == "analyze":
        return _cmd_analyze(text, args.max_period)
    try:
        return _cmd_solve(args.method, text, args)
    except (ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
