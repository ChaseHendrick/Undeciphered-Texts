"""Explicit invocation adapters for cipher helpers and bounded searches.

Only allowlisted functions run. JSON parameters are validated, native binary
inputs are hexadecimal, and typed cribs preserve each search's contract.
"""
from __future__ import annotations

import dataclasses
import importlib
import inspect
import json
import math
from dataclasses import dataclass
from collections.abc import Mapping

from engine.result import SolveResult
from engine.reverse_engineer import Crib


@dataclass(frozen=True)
class Tool:
    module: str
    function: str
    mode: str
    encoding: str = "text"
    binary_parameters: tuple[str, ...] = ()


_SUPPLIED = (
    "affine", "autokey", "beaufort", "bifid", "cadenus", "chaocipher",
    "cm_bifid", "digrafid", "enigma", "four_square", "grandpre", "gromark",
    "gronsfeld", "hill", "m209", "myszkowski", "nihilist", "nihilist_transposition",
    "phillips", "portax", "quagmire_i", "quagmire_ii", "quagmire_iii", "quagmire_iv",
    "running_key", "seriated_playfair", "slidefair", "solitaire", "straddling_checkerboard",
    "swagman", "tridigital", "trifid", "tri_square", "turning_grille", "rail_fence", "route",
    "ragbaby", "fractionated_morse", "condi", "progressive_key", "periodic_gromark",
    "morbit", "pollux", "monome_dinome", "sequence_transposition", "numbered_key", "baconian",
    "porta", "playfair", "adfgvx", "amsco", "bazeries", "nicodemus", "keyed_vigenere", "fbi_letter_shift",
    "interrupted_key", "checkerboard", "homophonic",
)
TOOLS = {name.replace("_", "-"): Tool("engine.solvers." + name, "solve_" + name, "supplied-key") for name in _SUPPLIED}
TOOLS.update({
    "baconian": Tool("engine.solvers.baconian", "solve_baconian", "supplied-extraction"),
    "caesar": Tool("engine.solvers.caesar", "solve_caesar", "score-ranked-search"),
    "vigenere": Tool("engine.solvers.vigenere", "solve_vigenere", "score-ranked-search"),
    "substitution": Tool("engine.solvers.substitution", "solve_substitution", "score-ranked-search"),
    "redefence": Tool("engine.solvers.redefence", "solve_redefence", "supplied-key-or-search"),
    "word-pattern": Tool("engine.solvers.word_pattern", "solve_word_pattern", "lexicon-constrained"),
    "progressive-inference": Tool("engine.solvers.progressive_key", "infer_progressive_key", "crib-constrained"),
    "condi-inference": Tool("engine.solvers.condi", "infer_condi", "lexicon-and-crib-constrained"),
    "interrupted-inference": Tool("engine.solvers.interrupted_key", "infer_interrupted_key", "reset-pattern-and-crib-constrained"),
    "homophonic-inference": Tool("engine.solvers.homophonic", "infer_homophonic", "row-and-crib-constrained"),
    "autokey-inference": Tool("engine.solvers.autokey_inference", "infer_autokey", "conditional-seed-ranking-and-crib-inference"),
    "enigma-start-search": Tool("engine.solvers.enigma_crib_search", "search_enigma_starts", "supplied-machine-crib-constrained-start-search"),
    "morse-constraints": Tool("engine.solvers.morse_constraints", "search_morse_constraints", "map-and-text-constrained"),
    "transposition-ensemble": Tool("engine.transposition_ensemble", "search_transposition_ensemble", "score-ranked-search"),
    "investigate": Tool("engine.solver_reasoning", "investigate_cipher", "bounded-investigation"),
    "emperor": Tool("engine.solvers.persona_court_notice", "investigate_emperor", "systematic-persona-search"),
    "inheritance": Tool("engine.solvers.persona_inheritance", "investigate_inheritance", "clue-based-persona-search"),
    "hallucinogens": Tool("engine.solvers.persona_hallucinogens", "investigate_hallucinogens", "bounded-composition-persona-search"),
    "persona-council": Tool("engine.persona_solvers", "investigate_personas", "shared-budget-persona-search"),
    "k4-models": Tool("engine.k4_models", "search_k4_models", "conditional-crib-model-compositions"),
    "pacifist": Tool("engine.solvers.pacifist", "investigate_pacifist", "conservative-exact-persona-search"),
    "cartographer": Tool("engine.solvers.persona_cartographer", "investigate_cartographer", "layout-persona-search"),
    "detective": Tool("engine.solvers.persona_detective", "investigate_detective", "unplaced-crib-persona-search"),
    "mechanic": Tool("engine.solvers.persona_mechanic", "investigate_mechanic", "algebra-and-recurrence-persona-search"),
    "normal-man": Tool("engine.solvers.persona_normal_man", "investigate_normal_man", "plain-classical-baseline"),
    "adversary": Tool("engine.solvers.persona_adversary", "investigate_adversary", "same-evidence-counterexample-search"),
    "skeptic": Tool("engine.solvers.persona_skeptic", "investigate_skeptic", "reserved-evidence-postcheck"),
    "hill-inference": Tool("engine.solvers.hill_inference", "infer_hill", "crib-constrained-matrix-search"),
    "two-square": Tool("engine.solvers.two_square", "solve_two_square", "supplied-squares-or-lexicon-search"),
    "columnar": Tool("engine.solvers.columnar", "solve_columnar", "supplied-widths"),
    "homophonic-fixed-temperature": Tool("engine.solvers.homophonic_fixed_temperature", "solve_homophonic_fixed_temperature", "score-ranked-search"),
    "chaos-search": Tool("engine.solvers.chaos_search", "solve_chaos_search", "score-ranked-search"),
    "rsa-wiener": Tool("engine.solvers.rsa_wiener", "solve_rsa_wiener", "public-parameter-attack", "integer"),
    "rsa-fermat": Tool("engine.solvers.rsa_fermat", "solve_rsa_fermat", "public-parameter-attack", "integer"),
    "rsa-common-modulus": Tool("engine.solvers.rsa_common_modulus", "solve_rsa_common_modulus", "public-parameter-attack", "integer"),
    "aes": Tool("engine.solvers.aes", "solve_aes", "supplied-key", "hex", ("key",)),
    "chacha20": Tool("engine.solvers.chacha20", "solve_chacha20", "supplied-key", "hex", ("key", "nonce")),
})


def _resolve(name):
    if not isinstance(name, str) or name not in TOOLS:
        raise ValueError("unknown tool; use the tools command to inspect supported names")
    spec = TOOLS[name]
    function = getattr(importlib.import_module(spec.module), spec.function)
    return spec, function, inspect.signature(function)


def list_tools():
    catalog = []
    for name in sorted(TOOLS):
        spec, _, signature = _resolve(name)
        parameters = list(signature.parameters.values())[1:]
        catalog.append({"name": name, "mode": spec.mode, "input_encoding": spec.encoding,
                        "required_parameters": [p.name for p in parameters if p.default is inspect.Parameter.empty],
                        "optional_parameters": {p.name: p.default for p in parameters if p.default is not inspect.Parameter.empty},
                        "binary_parameters_encoding": "hex" if spec.binary_parameters else None,
                        "output_contract": "SolveResult" if spec.function.startswith("solve_") else "tool-specific structured report; see implementation and topical documentation",
                        "output_fields": ["method", "plaintext", "key", "score", "details"] if spec.function.startswith("solve_") else None,
                        "implementation": spec.module + "." + spec.function})
    return catalog


def _validate_json(value, *, depth=0):
    if depth > 8:
        raise ValueError("parameter nesting exceeds8 levels")
    if isinstance(value, str):
        if len(value) > 8192:
            raise ValueError("parameter string exceeds8192 characters")
    elif isinstance(value, bool) or value is None:
        return
    elif isinstance(value, int):
        if value.bit_length() > 4096:
            raise ValueError("integer parameter exceeds4096 bits")
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("numeric parameters must be finite")
    elif isinstance(value, list):
        if len(value) > 1000:
            raise ValueError("parameter sequence exceeds1000 entries")
        for item in value:
            _validate_json(item, depth=depth + 1)
    elif isinstance(value, dict):
        if len(value) > 100:
            raise ValueError("parameter object exceeds100 fields")
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("parameter names must be strings")
            _validate_json(item, depth=depth + 1)
    else:
        raise TypeError("parameters must contain JSON values only")


def run_tool(name, value, *, params=None):
    """Invoke an allowlisted tool with JSON-compatible parameters and report its mode."""
    spec, function, signature = _resolve(name)
    if params is None:
        params = {}
    if not isinstance(params, Mapping):
        raise TypeError("params must be an object")
    params = dict(params)
    _validate_json(params)
    if len(json.dumps(params)) > 65536:
        raise ValueError("parameter JSON exceeds64 KiB")
    if spec.encoding == "integer":
        if not isinstance(value, int) or isinstance(value, bool) or value.bit_length() > 4096:
            raise TypeError("input must be a bounded RSA integer")
    else:
        if not isinstance(value, str) or len(value) > 8192:
            raise ValueError("input must be text of at most8192 characters")
    if spec.encoding == "hex":
        try:
            value = bytes.fromhex(value)
            for parameter in spec.binary_parameters:
                if parameter in params:
                    params[parameter] = bytes.fromhex(params[parameter])
        except (ValueError, TypeError) as exc:
            raise ValueError("binary input and key parameters must be hexadecimal strings") from exc
    for parameter, maximum in (("restarts", 20), ("steps", 50000), ("max_period", 128), ("max_steps", 10000)):
        if parameter in params and (not isinstance(params[parameter], int) or isinstance(params[parameter], bool) or not 0 <= params[parameter] <= maximum):
            raise ValueError(f"{parameter} must be an integer between0 and{maximum}")
    for parameter in ("byte_length", "plaintext_length"):
        if parameter in params and params[parameter] is not None and (not isinstance(params[parameter], int) or isinstance(params[parameter], bool) or not 1 <= params[parameter] <= 4096):
            raise ValueError(f"{parameter} must be an integer between 1 and 4096")
    if name == "chaos-search" and "max_trials" in params and (not isinstance(params["max_trials"], int) or isinstance(params["max_trials"], bool) or not 1 <= params["max_trials"] <= 50000):
        raise ValueError("max_trials must be an integer between 1 and 50000")
    if name == "two-square" and "keywords" in params and (not isinstance(params["keywords"], list) or not 1 <= len(params["keywords"]) <= 100):
        raise ValueError("keywords must be a list of at most 100 entries")
    if name == "monome-dinome" and "merge" in params and isinstance(params["merge"], list):
        params["merge"] = tuple(params["merge"])
    for crib_parameter in ("cribs", "verification_cribs"):
        if crib_parameter not in params:
            continue
        if not isinstance(params[crib_parameter], list):
            raise TypeError("cribs must be a list of offset/plaintext records")
        cribs = []
        for entry in params[crib_parameter]:
            if not isinstance(entry, dict) or set(entry) != {"offset", "plaintext"} or not isinstance(entry["offset"], int) or isinstance(entry["offset"], bool) or entry["offset"] < 0 or not isinstance(entry["plaintext"], str):
                raise ValueError("each crib requires a nonnegative integer offset and text plaintext")
            if name == "morse-constraints":
                from engine.solvers.morse_constraints import MorseCrib
                cribs.append(MorseCrib(entry["offset"], entry["plaintext"]))
            else:
                cribs.append(Crib(entry["offset"], entry["plaintext"]))
        params[crib_parameter] = cribs
    try:
        bound = signature.bind(value, **params)
    except TypeError as exc:
        raise ValueError(f"invalid parameters for{name}: {exc}") from exc
    result = function(*bound.args, **bound.kwargs)
    if hasattr(result, "to_dict"):
        report = result.to_dict()
    elif isinstance(result, SolveResult) or dataclasses.is_dataclass(result):
        report = dataclasses.asdict(result)
    elif isinstance(result, dict):
        report = result
    else:
        raise TypeError("unsupported tool result")
    return {"tool": name, "mode": spec.mode, "executed": True, "result": report,
            "scope": "The result follows the selected tool's documented limits. Invocation does not validate an unknown historical plaintext."}
