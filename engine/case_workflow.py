"""Local, auditable intake and bounded hypothesis runs for unsolved texts.

Source bytes, provenance, cribs, and run snapshots remain separate from
candidate predictions. No command marks a case solved or publishes it.
The JSON Schema is an authoring contract; runtime validation uses explicit
standard-library checks and an independent intake hash anchor.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from engine.reverse_engineer import Crib, infer_cipher_models
from engine.stats import column_mean_ic, friedman_period, index_of_coincidence, kasiski_factors, ngram_counts

WORKFLOW_VERSION = "1.1"
MAX_SOURCE_BYTES = 1_048_576
MAX_INFERENCE_LETTERS = 512
MAX_BASELINE_LETTERS = 8192
_REPO = Path(__file__).resolve().parents[1]
_STAGES = ("intake", "analyzed", "hypotheses", "validation")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _keys(value, required: tuple[str, ...], name: str) -> None:
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f"{name} must contain exactly: {', '.join(required)}")


def _string(value, name: str, *, empty: bool = False) -> None:
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ValueError(f"{name} must be a {'possibly empty ' if empty else 'nonempty '}string")


def _integer(value, name: str, minimum: int = 0) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{name} must be an integer at least {minimum}")


def _url(value, name: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    _string(value, name)
    if not re.fullmatch(r"https?://\S+", value):
        raise ValueError(f"{name} must be an http or https URL without whitespace")
    parsed = urlparse(value)
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        raise ValueError(f"{name} must be an http or https source URL")


def _digest(value, name: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or not _HASH.fullmatch(value):
        raise ValueError(f"{name} must be a lowercase SHA-256 hex digest")


def _timestamp(value, name: str) -> None:
    _string(value, name)
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|\+00:00)", value):
        raise ValueError(f"{name} must be an extended UTC timestamp with at most six fractional digits")
    try:
        format_string = "%Y-%m-%dT%H:%M:%S.%f%z" if "." in value else "%Y-%m-%dT%H:%M:%S%z"
        timestamp = datetime.strptime(value, format_string)
    except ValueError as exc:
        raise ValueError(f"{name} must be an ISO UTC timestamp") from exc
    if timestamp.utcoffset() is None or timestamp.utcoffset().total_seconds() != 0:
        raise ValueError(f"{name} must include UTC timezone information")


def _child(directory: Path, relative: str) -> Path:
    """Reject path traversal and symlinked input/output components."""
    path = Path(relative)
    if path.is_absolute() or not path.parts or any(part in ("..", ".") for part in path.parts):
        raise ValueError("case paths must be simple relative paths without traversal")
    current = directory
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"case path must not contain a symlink: {current}")
    if not current.resolve().is_relative_to(directory.resolve()):
        raise ValueError("case path escapes its directory")
    return current


def _atomic_write(path: Path, data: bytes, *, replace: bool = False, readonly: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if readonly:
            os.chmod(temporary, 0o444)
        if replace:
            os.replace(temporary, path)
        else:
            # Atomic publication without replacing an existing file.
            os.link(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def _read_bounded(path: Path) -> bytes:
    with path.open("rb") as handle:
        data = handle.read(MAX_SOURCE_BYTES + 1)
    if len(data) > MAX_SOURCE_BYTES:
        raise ValueError(f"text source must not exceed {MAX_SOURCE_BYTES} bytes")
    return data


def _decode(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("source must be UTF-8 text; preserve other media separately") from exc


def _validate_cribs(cribs, name: str) -> None:
    if not isinstance(cribs, list):
        raise ValueError(f"{name} must be a list")
    for index, crib in enumerate(cribs):
        label = f"{name}[{index}]"
        _keys(crib, ("offset", "plaintext", "status", "source_url", "note"), label)
        _integer(crib["offset"], label + ".offset")
        _string(crib["plaintext"], label + ".plaintext")
        if crib["status"] not in ("confirmed", "tentative"):
            raise ValueError(f"{label}.status must be confirmed or tentative")
        _url(crib["source_url"], label + ".source_url", nullable=crib["status"] == "tentative")
        _string(crib["note"], label + ".note", empty=True)


def _validate_structure(case: dict) -> None:
    _keys(case, ("schema_version", "case_id", "title", "status", "stage", "provenance", "source",
                 "language", "alphabet", "transcription", "cribs", "validation"), "case")
    if type(case["schema_version"]) is not int or case["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    if not isinstance(case["case_id"], str) or not _SLUG.fullmatch(case["case_id"]):
        raise ValueError("case_id must be a lowercase hyphenated slug")
    _string(case["title"], "title")
    if case["status"] != "unsolved" or case["stage"] not in _STAGES:
        raise ValueError("case status must remain unsolved with a supported workflow stage")
    provenance = case["provenance"]
    _keys(provenance, ("source_url", "description", "accessed_at_utc", "original_filename", "references"), "provenance")
    _url(provenance["source_url"], "provenance.source_url")
    _string(provenance["description"], "provenance.description", empty=True)
    _string(provenance["original_filename"], "provenance.original_filename")
    _timestamp(provenance["accessed_at_utc"], "provenance.accessed_at_utc")
    if not isinstance(provenance["references"], list):
        raise ValueError("provenance.references must be a list of source URLs")
    for reference in provenance["references"]:
        _url(reference, "provenance reference")
    source = case["source"]
    _keys(source, ("path", "sha256", "bytes", "encoding"), "source")
    if source["path"] != "source/ciphertext.txt" or source["encoding"] != "utf-8":
        raise ValueError("source path must be source/ciphertext.txt with utf-8 encoding")
    _digest(source["sha256"], "source.sha256")
    _integer(source["bytes"], "source.bytes", 1)
    if source["bytes"] > MAX_SOURCE_BYTES:
        raise ValueError("source byte count exceeds the intake bound")
    language = case["language"]
    _keys(language, ("status", "value", "basis"), "language")
    if language["status"] not in ("unknown", "tentative", "confirmed"):
        raise ValueError("unsupported language status")
    if language["value"] is not None:
        _string(language["value"], "language.value")
    _string(language["basis"], "language.basis", empty=True)
    alphabet = case["alphabet"]
    _keys(alphabet, ("kind", "symbols", "normalization"), "alphabet")
    if alphabet["kind"] not in ("unknown", "latin", "custom"):
        raise ValueError("alphabet kind must be unknown, latin, or custom")
    if alphabet["normalization"] not in ("none", "ascii_letters"):
        raise ValueError("alphabet normalization must be none or ascii_letters")
    if alphabet["kind"] != "latin" and alphabet["normalization"] != "none":
        raise ValueError("ASCII normalization requires an explicitly Latin alphabet")
    if not isinstance(alphabet["symbols"], list):
        raise ValueError("alphabet.symbols must be a list")
    for symbol in alphabet["symbols"]:
        _string(symbol, "alphabet symbol")
    if len(set(alphabet["symbols"])) != len(alphabet["symbols"]):
        raise ValueError("alphabet.symbols must not repeat")
    transcription = case["transcription"]
    _keys(transcription, ("uncertainty", "notes", "alternatives"), "transcription")
    if transcription["uncertainty"] not in ("unassessed", "reported", "checked"):
        raise ValueError("unsupported transcription uncertainty status")
    _string(transcription["notes"], "transcription.notes", empty=True)
    if not isinstance(transcription["alternatives"], list):
        raise ValueError("transcription.alternatives must be a list")
    for alternative in transcription["alternatives"]:
        _keys(alternative, ("location", "observed", "alternative", "basis"), "transcription alternative")
        for name, value in alternative.items():
            _string(value, f"transcription alternative {name}")
    _validate_cribs(case["cribs"], "cribs")
    validation = case["validation"]
    _keys(validation, ("known_plaintext_url", "expected_plaintext_sha256", "heldout_cribs"), "validation")
    _url(validation["known_plaintext_url"], "validation.known_plaintext_url", nullable=True)
    _digest(validation["expected_plaintext_sha256"], "validation.expected_plaintext_sha256", nullable=True)
    if validation["expected_plaintext_sha256"] is not None and validation["known_plaintext_url"] is None:
        raise ValueError("an expected plaintext hash requires a reference URL")
    _validate_cribs(validation["heldout_cribs"], "validation.heldout_cribs")


def _validated(case_directory: Path) -> tuple[Path, dict, bytes, bytes, bytes]:
    directory = Path(case_directory)
    if directory.is_symlink():
        raise ValueError("case directory must not be a symlink")
    directory = directory.resolve()
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    case_bytes = _read_bounded(_child(directory, "case.json"))
    try:
        case = json.loads(_decode(case_bytes))
    except json.JSONDecodeError as exc:
        raise ValueError("case.json is not valid JSON") from exc
    _validate_structure(case)
    source = _read_bounded(_child(directory, case["source"]["path"]))
    _decode(source)
    if _sha(source) != case["source"]["sha256"]:
        raise ValueError("source hash does not match case.json")
    if len(source) != case["source"]["bytes"]:
        raise ValueError("source byte count does not match case.json")
    intake_bytes = _read_bounded(_child(directory, "source/intake.json"))
    try:
        intake = json.loads(_decode(intake_bytes))
    except json.JSONDecodeError as exc:
        raise ValueError("source intake anchor is not valid JSON") from exc
    _keys(intake, ("case_id", "source_url", "timestamp_utc", "source_sha256", "source_bytes"), "intake anchor")
    _digest(intake["source_sha256"], "intake source_sha256")
    _integer(intake["source_bytes"], "intake source_bytes", 1)
    _timestamp(intake["timestamp_utc"], "intake timestamp_utc")
    if (intake["case_id"] != case["case_id"] or intake["source_sha256"] != _sha(source)
            or intake["source_bytes"] != len(source)):
        raise ValueError("immutable intake anchor does not match the case source")
    _url(intake["source_url"], "intake source_url")
    return directory, case, case_bytes, source, intake_bytes


def validate_case(case_directory: Path) -> dict:
    """Validate structure and preserved input hashes; never verify a solve."""
    return _validated(case_directory)[1]


def init_case(slug: str, *, ciphertext_file: Path, source_url: str, root: Path = Path("cases")) -> Path:
    """Create a new case without overwriting an existing directory."""
    if not isinstance(slug, str) or not _SLUG.fullmatch(slug):
        raise ValueError("slug must contain lowercase letters/digits separated by single hyphens")
    _url(source_url, "source_url")
    source_path = Path(ciphertext_file)
    data = _read_bounded(source_path)
    if not _decode(data).strip():
        raise ValueError("ciphertext file must contain nonempty UTF-8 text")
    root = Path(root)
    if root.is_symlink():
        raise ValueError("case root must not be a symlink")
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    directory = _child(root, slug)
    directory.mkdir(exist_ok=False)
    timestamp = _utc()
    case = {
        "schema_version": 1, "case_id": slug, "title": slug, "status": "unsolved", "stage": "intake",
        "provenance": {"source_url": source_url, "description": "", "accessed_at_utc": timestamp,
                       "original_filename": source_path.name, "references": []},
        "source": {"path": "source/ciphertext.txt", "sha256": _sha(data), "bytes": len(data), "encoding": "utf-8"},
        "language": {"status": "unknown", "value": None, "basis": ""},
        "alphabet": {"kind": "unknown", "symbols": [], "normalization": "none"},
        "transcription": {"uncertainty": "unassessed", "notes": "", "alternatives": []},
        "cribs": [],
        "validation": {"known_plaintext_url": None, "expected_plaintext_sha256": None, "heldout_cribs": []},
    }
    anchor = {"case_id": slug, "source_url": source_url, "timestamp_utc": timestamp,
              "source_sha256": _sha(data), "source_bytes": len(data)}
    try:
        _atomic_write(directory / "source/ciphertext.txt", data, readonly=True)
        _atomic_write(directory / "source/intake.json", _json_bytes(anchor), readonly=True)
        _atomic_write(directory / "case.json", _json_bytes(case))
    except Exception:
        shutil.rmtree(directory)
        raise
    return directory


def _latin_stream(text: str) -> str:
    ascii_letters = frozenset(_ALPHABET + _ALPHABET.lower())
    if any(ch.isalpha() and ch not in ascii_letters for ch in text):
        raise ValueError("A-Z model inference cannot normalize non-ASCII letters")
    return "".join(ch.upper() for ch in text if ch in ascii_letters)


def _git_sha() -> str | None:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=_REPO, capture_output=True,
                                text=True, timeout=2, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    value = result.stdout.strip()
    return value if result.returncode == 0 and re.fullmatch(r"[0-9a-f]{40,64}", value) else None


def _git_dirty() -> bool | None:
    try:
        result = subprocess.run(["git", "status", "--porcelain"], cwd=_REPO, capture_output=True,
                                text=True, timeout=2, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return bool(result.stdout) if result.returncode == 0 else None


def _runtime_versions() -> dict:
    try:
        z3_version = importlib.metadata.version("z3-solver")
    except importlib.metadata.PackageNotFoundError:
        z3_version = None
    return {"python_implementation": sys.implementation.name,
            "python_version": ".".join(str(value) for value in sys.version_info[:3]),
            "z3_solver_distribution": z3_version,
            "numpy_distribution": _distribution_version("numpy")}


def _distribution_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _code_hashes() -> dict:
    paths = sorted(set((_REPO / "engine").glob("*.py")) | set((_REPO / "engine/solvers").glob("*.py")))
    return {str(path.relative_to(_REPO)): _sha(path.read_bytes()) for path in paths if path.is_file()}


def _certificate_hash() -> str:
    rows = [f"{path.name}:{_sha(path.read_bytes())}" for path in sorted((_REPO / "engine/data").glob("*_certificate.json"))]
    return _sha("\n".join(rows).encode("utf-8"))


def _save_run(inputs: tuple, operation: str, report: dict, parameters: dict, stage: str,
              *, candidate: bytes | None = None, model_snapshot: bytes | None = None) -> Path:
    directory, case, case_bytes, source, intake_bytes = inputs
    runs = _child(directory, "runs")
    runs.mkdir(exist_ok=True)
    stamp = _utc()
    run = _child(directory, f"runs/{stamp.replace(':', '').replace('.', '-')}-{operation}-{uuid.uuid4().hex[:12]}")
    run.mkdir(exist_ok=False)
    incomplete = bool(report.get("incomplete", False))
    manifest = {
        "manifest_version": 1, "workflow_version": WORKFLOW_VERSION, "git_sha": _git_sha(),
        "git_dirty": _git_dirty(), "runtime_versions": _runtime_versions(),
        "timestamp_utc": stamp, "operation": operation, "case_id": case["case_id"],
        "source_sha256": _sha(source), "source_bytes": len(source),
        "case_snapshot_sha256": _sha(case_bytes), "intake_snapshot_sha256": _sha(intake_bytes),
        "code_sha256": _code_hashes(), "certificate_manifest_sha256": _certificate_hash(),
        "parameters": parameters, "execution_status": "incomplete" if incomplete else "completed",
        "report_sha256": _sha(_json_bytes(report)), "claimed_plaintext": None,
    }
    _atomic_write(run / "snapshot/ciphertext.txt", source, readonly=True)
    _atomic_write(run / "snapshot/case.json", case_bytes, readonly=True)
    _atomic_write(run / "snapshot/intake.json", intake_bytes, readonly=True)
    if candidate is not None:
        manifest.update({"candidate_sha256": _sha(candidate), "candidate_bytes": len(candidate),
                         "candidate_snapshot_path": "snapshot/plaintext-candidate.txt", "candidate_encoding": "utf-8"})
        _atomic_write(run / "snapshot/plaintext-candidate.txt", candidate, readonly=True)
    if model_snapshot is not None:
        manifest.update({"model_snapshot_sha256": _sha(model_snapshot),
                         "model_snapshot_path": "snapshot/router_weights.json"})
        _atomic_write(run / "snapshot/router_weights.json", model_snapshot, readonly=True)
    _atomic_write(run / "report.json", _json_bytes(report), readonly=True)
    # The manifest is published last, marking a completed artifact set.
    _atomic_write(run / "manifest.json", _json_bytes(manifest), readonly=True)
    # Updating the workflow stage does not change status or preserved source bytes.
    latest = validate_case(directory)
    latest["stage"] = stage
    _atomic_write(_child(directory, "case.json"), _json_bytes(latest), replace=True)
    return run


def analyze_case(case_directory: Path, *, max_period: int = 16) -> Path:
    """Record observed Unicode character/token statistics without a reading."""
    _integer(max_period, "max_period", 1)
    if max_period > 128:
        raise ValueError("max_period must not exceed 128")
    inputs = _validated(case_directory)
    _, case, _, source, _ = inputs
    text = _decode(source)
    tokens = text.split()
    counts = Counter(ch for ch in text if not ch.isspace())
    normalized = None
    latin_baseline = None
    if case["alphabet"]["kind"] == "latin" and case["alphabet"]["normalization"] == "ascii_letters":
        normalized = _latin_stream(text)
        sample = normalized[:MAX_BASELINE_LETTERS]
        latin_baseline = {
            "total_letters": len(normalized), "analyzed_letters": len(sample),
            "sampled": len(sample) < len(normalized), "sample_rule": "normalized stream prefix",
            "max_letters": MAX_BASELINE_LETTERS, "max_period": max_period,
            "index_of_coincidence": index_of_coincidence(sample),
            "friedman_period": friedman_period(sample),
            "kasiski": [{"period": period, "votes": votes}
                        for period, votes in kasiski_factors(sample, max_period=max_period)],
            "column_ic": [{"period": period, "mean_ic": column_mean_ic(sample, period)}
                          for period in range(1, min(max_period, len(sample)) + 1)],
            "top_ngrams": {str(n): ngram_counts(sample, n, limit=12) for n in (1, 2, 3, 4)},
            "scope": "Period clues only. Friedman assumes English coincidence constants; it is not language identification or cipher-family proof.",
        }
    report = {
        "report_version": 1, "operation": "analyze", "classification": "observations",
        "executed": True, "incomplete": False, "claimed_plaintext": None,
        "analysis": {"unicode_characters": len(text), "source_bytes": len(source), "tokens": tokens,
                     "token_count": len(tokens), "tokenization": "Unicode whitespace only; no token rewriting",
                     "character_frequencies": [{"symbol": symbol, "count": count} for symbol, count in sorted(counts.items())],
                     "normalized_latin": normalized,
                     "latin_baseline": latin_baseline,
                     "normalization": case["alphabet"]["normalization"],
                     "normalization_removed_characters": None if normalized is None else len(text) - len(normalized)},
        "scope": "Observed source statistics only. Alphabet and language remain declared assumptions; no reading is inferred.",
    }
    return _save_run(inputs, "analyze", report, {"max_source_bytes": MAX_SOURCE_BYTES,
                                               "max_period": max_period,
                                               "max_baseline_letters": MAX_BASELINE_LETTERS}, "analyzed")


def _symbolic_inference(ciphertext: str, **parameters) -> dict:
    module = importlib.import_module("engine.cipher_synthesis")
    try:
        return module.synthesize_cipher_models(ciphertext, **parameters).to_dict()
    except module.OptionalSynthesisDependencyError as exc:
        raise ImportError(str(exc)) from exc


def reverse_case(
    case_directory: Path, *, symbolic: bool = False, max_period: int = 4,
    timeout_seconds: float = 5.0, max_checks: int = 10_000,
    models: tuple[str, ...] = ("affine", "vigenere", "beaufort", "substitution"),
    layouts: tuple[str, ...] = ("identity", "reverse"), columnar_widths: tuple[int, ...] = (),
) -> Path:
    """Run bounded model inference with confirmed training cribs only."""
    _integer(max_period, "max_period", 1)
    if max_period > 128:
        raise ValueError("max_period must not exceed 128")
    _integer(max_checks, "max_checks", 1)
    if max_checks > 100_000:
        raise ValueError("max_checks must not exceed 100000")
    if (not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool)
            or not math.isfinite(timeout_seconds) or not 0 < timeout_seconds <= 60):
        raise ValueError("timeout_seconds must be positive and at most 60")
    inputs = _validated(case_directory)
    _, case, _, source, _ = inputs
    if case["alphabet"]["kind"] != "latin" or case["alphabet"]["normalization"] != "ascii_letters":
        raise ValueError("model inference requires an explicitly Latin alphabet with ascii_letters normalization")
    cipher = _latin_stream(_decode(source))
    if not cipher or len(cipher) > MAX_INFERENCE_LETTERS:
        raise ValueError(f"model inference requires 1..{MAX_INFERENCE_LETTERS} A-Z letters")
    confirmed = [crib for crib in case["cribs"] if crib["status"] == "confirmed"]
    if not confirmed:
        raise ValueError("model inference requires at least one confirmed aligned crib")
    cribs = [Crib(crib["offset"], crib["plaintext"]) for crib in confirmed]
    parameters = {"max_period": max_period, "max_inference_letters": MAX_INFERENCE_LETTERS,
                  "confirmed_cribs_only": True, "symbolic": symbolic}
    report = {"report_version": 1, "operation": "reverse", "executed": True, "incomplete": False,
              "availability": "available", "claimed_plaintext": None,
              "confirmed_crib_count": len(confirmed),
              "tentative_crib_count_excluded": len(case["cribs"]) - len(confirmed),
              "heldout_crib_count_not_fitted": len(case["validation"]["heldout_cribs"]),
              "verification_status": "unverified",
              "scope": "Compatible models are candidates. Crib fit, consensus, and reencryption do not verify unknown plaintext."}
    if symbolic:
        parameters.update({"timeout_seconds": timeout_seconds, "max_checks": max_checks,
                           "models": list(models), "layouts": list(layouts), "columnar_widths": list(columnar_widths)})
        try:
            result = _symbolic_inference(cipher, cribs=cribs, max_period=max_period,
                                         timeout_seconds=timeout_seconds, max_checks=max_checks,
                                         models=models, layouts=layouts, columnar_widths=columnar_widths)
        except ImportError as exc:
            report.update({"executed": False, "incomplete": True, "availability": "unavailable",
                           "classification": "incomplete", "result": None, "error": str(exc)})
            return _save_run(inputs, "reverse-symbolic", report, parameters, "hypotheses")
        incomplete = bool(result.get("incomplete") or result.get("timed_out")
                          or result.get("search_complete") is False)
        report["incomplete"] = incomplete
    else:
        result = infer_cipher_models(cipher, cribs=cribs, max_period=max_period).to_dict()
        incomplete = False
    report["result"] = result
    has_candidates = result.get("sat_models", 0) > 0 if symbolic else bool(result.get("hypotheses"))
    report["classification"] = "incomplete" if incomplete else ("candidates" if has_candidates else "failed")
    return _save_run(inputs, "reverse-symbolic" if symbolic else "reverse-baseline", report, parameters, "hypotheses")


def investigate_case(case_directory: Path, *, max_checks: int = 5000, max_candidates: int = 20,
                     temperament: str = "balanced", solver_profile: str = "planner") -> Path:
    """Connect bounded searches; hold validation evidence out of hypothesis fitting."""
    inputs = _validated(case_directory)
    if solver_profile not in ("planner", "council"):
        raise ValueError("solver_profile must be planner or council")
    _, case, _, source, _ = inputs
    if case["alphabet"]["kind"] != "latin" or case["alphabet"]["normalization"] != "ascii_letters":
        raise ValueError("investigation requires an explicitly Latin alphabet with ascii_letters normalization")
    cipher = _latin_stream(_decode(source))
    if not 4 <= len(cipher) <= MAX_INFERENCE_LETTERS:
        raise ValueError(f"case investigation requires 4..{MAX_INFERENCE_LETTERS} A-Z letters")
    from engine.solver_reasoning import investigate_cipher
    confirmed = [crib for crib in case["cribs"] if crib["status"] == "confirmed"]
    cribs = [Crib(crib["offset"], crib["plaintext"]) for crib in confirmed]
    # Snapshot before execution, then require report identity to match these bytes.
    WEIGHTS_PATH = _REPO / "engine/data/neural_router_v2_weights.json"
    model = None
    if WEIGHTS_PATH.is_file():
        with WEIGHTS_PATH.open("rb") as handle:
            model = handle.read(4 * 1024 * 1024 + 1)
        if len(model) > 4 * 1024 * 1024:
            raise ValueError("router artifact exceeds 4 MiB")
    if solver_profile == "council":
        from engine.persona_solvers import investigate_personas
        result = investigate_personas(cipher, cribs=cribs, max_checks=max_checks,
                                      max_candidates=max_candidates)
    else:
        result = investigate_cipher(cipher, cribs=cribs, max_checks=max_checks,
                                    max_candidates=max_candidates, temperament=temperament).to_dict()
    routing = result.get("neural_advice") or {}
    model_hash = routing.get("model_sha256")
    if model_hash is not None and (model is None or _sha(model) != model_hash):
        raise RuntimeError("router changed during investigation; retry with a stable model")
    report = {"report_version":1, "operation":"investigate", "executed":True,
              "incomplete":result.get("search_complete") is not True, "claimed_plaintext":None,
              "verification_status":"unverified", "result":result,
              "confirmed_crib_count":len(confirmed),
              "tentative_crib_count_excluded":len(case["cribs"]) - len(confirmed),
              "heldout_crib_count_not_fitted":len(case["validation"]["heldout_cribs"]),
              "scope":"Research candidates and explicit checks only; independent validation is a separate operation."}
    parameters = {"max_checks":max_checks, "max_candidates":max_candidates,
                  "temperament":temperament, "solver_profile":solver_profile,
                  "confirmed_cribs_only":True,
                  "max_inference_letters":MAX_INFERENCE_LETTERS}
    return _save_run(inputs, "investigate", report, parameters, "hypotheses",
                     model_snapshot=model if model_hash is not None else None)


def verify_case(case_directory: Path, *, candidate_file: Path) -> Path:
    """Compare a supplied candidate against declared independent references.

    Hashes cover exact UTF-8 bytes, including whitespace. Heldout cribs use
    A-Z positions only for explicitly normalized Latin cases; other cases
    use Unicode code point offsets in the unchanged candidate text.
    """
    inputs = _validated(case_directory)
    _, case, _, _, _ = inputs
    candidate = _read_bounded(Path(candidate_file))
    text = _decode(candidate)
    if not text.strip():
        raise ValueError("candidate must contain nonempty UTF-8 text")
    validation = case["validation"]
    latin = case["alphabet"]["kind"] == "latin" and case["alphabet"]["normalization"] == "ascii_letters"
    stream = _latin_stream(text) if latin else text
    confirmed = [crib for crib in validation["heldout_cribs"] if crib["status"] == "confirmed"]
    comparisons = []
    for crib in confirmed:
        expected = _latin_stream(crib["plaintext"]) if latin else crib["plaintext"]
        if not expected:
            raise ValueError("heldout crib must contain letters under the declared normalization")
        actual = stream[crib["offset"]:crib["offset"] + len(expected)]
        comparisons.append({"offset": crib["offset"], "expected": expected, "actual": actual,
                            "matched": actual == expected, "source_url": crib["source_url"]})
    expected_hash = validation["expected_plaintext_sha256"]
    hash_matches = None if expected_hash is None else _sha(candidate) == expected_hash
    if hash_matches is False or any(not entry["matched"] for entry in comparisons):
        classification = "rejected"
    elif hash_matches is True:
        classification = "reference-match"
    elif comparisons:
        classification = "crib-supported"
    else:
        classification = "unchecked"
    report = {
        "report_version": 1, "operation": "verify", "classification": classification,
        "executed": True, "incomplete": False, "claimed_plaintext": None,
        "candidate_sha256": _sha(candidate), "expected_plaintext_sha256": expected_hash,
        "exact_reference_hash_matches": hash_matches, "reference_url": validation["known_plaintext_url"],
        "heldout_comparisons": comparisons,
        "tentative_heldout_count_excluded": len(validation["heldout_cribs"]) - len(confirmed),
        "crib_coordinates": "normalized A-Z letters" if latin else "unchanged Unicode code points",
        "scope": "Comparisons against declared evidence only. Source independence, transcription, and historical attribution require human review; no solve status is assigned.",
    }
    parameters = {"max_candidate_bytes": MAX_SOURCE_BYTES, "hash_encoding": "exact UTF-8 bytes",
                  "confirmed_heldout_only": True, "fit_training_cribs": False}
    return _save_run(inputs, "verify", report, parameters, "validation", candidate=candidate)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m engine.case_workflow", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    intake = commands.add_parser("init", help="copy a new UTF-8 source and record provenance")
    intake.add_argument("slug")
    intake.add_argument("--ciphertext-file", type=Path, required=True)
    intake.add_argument("--source-url", required=True)
    intake.add_argument("--root", type=Path, default=Path("cases"))
    for name in ("validate", "analyze", "reverse", "investigate", "verify"):
        command = commands.add_parser(name)
        command.add_argument("case_directory", type=Path)
        if name == "analyze":
            command.add_argument("--max-period", type=int, default=16)
        if name == "reverse":
            command.add_argument("--symbolic", action="store_true")
            command.add_argument("--max-period", type=int, default=4)
            command.add_argument("--timeout", type=float)
            command.add_argument("--max-checks", type=int)
            command.add_argument("--model", action="append", choices=("affine", "caesar", "vigenere", "beaufort", "substitution", "quagmire-i", "quagmire-ii", "quagmire-iii"))
            command.add_argument("--layout", action="append", choices=("identity", "reverse"))
            command.add_argument("--columnar-width", action="append", type=int)
        if name == "verify":
            command.add_argument("--candidate-file", type=Path, required=True)
        if name == "investigate":
            command.add_argument("--max-checks", type=int, default=5000)
            command.add_argument("--max-candidates", type=int, default=20)
            command.add_argument("--temperament", choices=("balanced", "cautious", "curious"), default="balanced")
            command.add_argument("--solver-profile", choices=("planner", "council"), default="planner")
    args = parser.parse_args(argv)
    try:
        if args.command == "reverse" and not args.symbolic and any(
            value is not None for value in (args.timeout, args.max_checks, args.model, args.layout, args.columnar_width)
        ):
            raise ValueError("--timeout, --max-checks, --model, --layout, and --columnar-width require --symbolic")
        if args.command == "init":
            output = {"case_directory": str(init_case(args.slug, ciphertext_file=args.ciphertext_file,
                                                      source_url=args.source_url, root=args.root)), "status": "unsolved"}
        elif args.command == "validate":
            case = validate_case(args.case_directory)
            output = {"valid": True, "case_id": case["case_id"], "source_sha256": case["source"]["sha256"],
                      "scope": "Structure and input integrity only; no solution verified."}
        else:
            if args.command == "analyze":
                run = analyze_case(args.case_directory, max_period=args.max_period)
            elif args.command == "verify":
                run = verify_case(args.case_directory, candidate_file=args.candidate_file)
            elif args.command == "investigate":
                run = investigate_case(args.case_directory, max_checks=args.max_checks,
                                       max_candidates=args.max_candidates, temperament=args.temperament,
                                       solver_profile=args.solver_profile)
            else:
                run = reverse_case(args.case_directory, symbolic=args.symbolic, max_period=args.max_period,
                                   timeout_seconds=5.0 if args.timeout is None else args.timeout,
                                   max_checks=10_000 if args.max_checks is None else args.max_checks,
                                   models=tuple(args.model or ("affine", "vigenere", "beaufort", "substitution")),
                                   layouts=tuple(args.layout or ("identity", "reverse")), columnar_widths=tuple(args.columnar_width or ()))
            output = {"run_directory": str(run), "claimed_plaintext": None}
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        print(f"case workflow failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
