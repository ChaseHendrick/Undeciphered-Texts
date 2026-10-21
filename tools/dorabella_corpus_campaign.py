"""Frozen larger-corpus Dorabella search with short controls and shuffled nulls.

Training books are local public-domain snapshots supplied explicitly. No neural
weights are fit or changed. All references are evaluated after key search.
"""
from __future__ import annotations

import argparse
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path
import random
import re
import struct
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from engine.alphabet import letters_only
from engine.language import LanguageModel

RAW = "abcdefgdhijklmknkkfbbkmoiopjqgkgfodhrdckkcfplgkjkfsqlmohhojqcqfsqcmstpqckfslqpdbpqfdmod"
CT = RAW.upper()
KEYS = ("PHQGIUMEAYLNOFDXJKRCVSTZWB", "QWERTYUIOPASDFGHJKLZXCVBNM", "ZYXWVUTSRQPONMLKJIHGFEDCBA")
CONTROL_PROSE = (
    "THE COURIER PLACED THE PARCEL BESIDE THE GATE AND WAITED UNDER THE PORCH UNTIL THE HEAVY RAIN HAD STOPPED",
    "We crossed the narrow bridge before sunrise and carried our blankets toward the empty farmhouse by the river.",
    "The little brass clock beside the window stopped again so she borrowed a watch and walked down to the station.",
)
TARGET_SEEDS = (1103, 2207, 3301, 4409, 5501, 6607, 7703, 8807)
MAX_SEARCH_SECONDS = 180.0
MAX_TOTAL_PROPOSALS = 12_000_000


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_book(path, ebook, title):
    raw = path.read_bytes()
    if len(raw) > 3_000_000:
        raise ValueError("book snapshot exceeds 3 MB")
    text = raw.decode("utf-8-sig")
    start = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*", text)
    end = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*?\*\*\*", text)
    if start is None or end is None or end.start() <= start.end():
        raise ValueError("expected distinct Gutenberg body markers")
    body = text[start.end():end.start()]
    ascii_body = ''.join(ch for ch in body if ch.isascii())
    return ascii_body, {"ebook": ebook, "title": title,
        "url": f"https://www.gutenberg.org/ebooks/{ebook}",
        "download_url": f"https://www.gutenberg.org/cache/epub/{ebook}/pg{ebook}.txt",
        "copyright_listing": "Public domain in the USA",
        "snapshot_bytes": len(raw), "snapshot_sha256": sha(raw),
        "body_sha256": sha(body.encode("utf-8")),
        "ascii_body_sha256": sha(ascii_body.encode("ascii")),
        "non_ascii_characters_removed": len(body) - len(ascii_body),
        "body_letters": len(letters_only(ascii_body)),
        "normalization": "UTF-8-sig decode; body strictly between Gutenberg start/end markers; discard non-ASCII code points, then engine A-Z normalization. Accented letters are omitted rather than transliterated. Chapter headings remain."}


def replay(plaintext, encrypt_key):
    if len(encrypt_key) != 26 or set(encrypt_key) != set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        raise AssertionError("encryption key is not a 26-letter permutation")
    return "".join(encrypt_key[ord(ch) - 65] for ch in plaintext)


def run(args):
    from engine.solvers.substitution_parallel_tempering import solve_substitution_parallel_tempering
    bodies, snapshots = [], []
    for path, ebook, title in ((args.austen, 1342, "Pride and Prejudice"), (args.bronte, 1260, "Jane Eyre")):
        body, metadata = load_book(path, ebook, title)
        bodies.append(body)
        snapshots.append(metadata)
    training = "\n".join(bodies)
    # Fit once, before controls and target search. Do not choose model settings
    # from Dorabella candidates or feed any reference into the optimizer.
    fit_start = time.perf_counter()
    model = LanguageModel(training, alpha=0.1)
    model_sha = sha(struct.pack("<" + "d" * len(model.logp), *model.logp))
    paths = ("engine/solvers/substitution_parallel_tempering.py", "engine/language.py", "tools/dorabella_corpus_campaign.py")
    report = {"schema_version": 1, "date": "2026-10-03", "target": "Dorabella",
        "status": "not_solved", "claimed_plaintext": None, "new_verified_plaintext": False,
        "transcription": CT, "transcription_sha256": sha(CT.encode("ascii")),
        "transcription_source": "https://doi.org/10.5281/zenodo.4819086",
        "transcription_member": "dorabella-experiments/LanguageIdentification/IsDorabellaEnglish/DorabellaTranscription.txt",
        "training_sources": snapshots, "training_body_sha256": sha(training.encode("utf-8")),
        "model": {"algorithm": "existing engine conditional quadgram backoff LanguageModel", "alpha": 0.1,
            "training_letters": len(letters_only(training)), "logp_little_endian_float64_sha256": model_sha,
            "fit_seconds": time.perf_counter() - fit_start,
            "selection": "One larger English model fixed before all searches; no target-specific tuning or neural training"},
        "code_sha256": {p: sha((REPO / p).read_bytes()) for p in paths},
        "git_head_at_start": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "python": sys.version, "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "bounds": {"global_search_seconds": MAX_SEARCH_SECONDS, "global_proposal_limit": MAX_TOTAL_PROPOSALS,
            "control_proposals_per_run": 500_000, "target_proposals_per_run": 1_000_000,
            "null_proposals_per_run": 1_000_000, "target_seeds": list(TARGET_SEEDS)},
        "controls": [], "target_runs": [], "null_runs": [],
        "scope": "All candidates are conditional on English bijective monoalphabetic substitution. Forward replay checks consistency, not a historical decipherment. Nulls are two exploratory shuffles, not a significance test."}
    started = time.perf_counter()
    total = 0

    def search(name, cipher, seed, cap, destination, reference=None):
        nonlocal total
        remaining_seconds = MAX_SEARCH_SECONDS - (time.perf_counter() - started)
        remaining_work = MAX_TOTAL_PROPOSALS - total
        if remaining_seconds <= 0.05 or remaining_work <= 0:
            return False
        settings = {"seed": seed, "restarts": 4, "sweeps": 40_000,
            "max_proposals": min(cap, remaining_work), "timeout_seconds": min(30.0, remaining_seconds),
            "max_candidates": 4, "polish_passes": 8, "logp": model.logp}
        before = time.perf_counter()
        result = solve_substitution_parallel_tempering(cipher, **settings)
        plain = letters_only(result.plaintext)
        encoded = replay(plain, result.key)
        if encoded != cipher:
            raise AssertionError("independent forward replay disagrees")
        proposals = result.details["proposals"]
        total += proposals
        entry = {"name": name, "seed": seed, "input": cipher,
            "candidate_plaintext": plain, "encrypt_key_AZ_to_cipher_labels": result.key,
            "score": result.score, "score_is_correctness_probability": False,
            "elapsed_seconds": time.perf_counter() - before, "actual_proposals": proposals,
            "exact_forward_match": True, "forward_sha256": sha(encoded.encode("ascii")),
            "candidate_sha256": sha(plain.encode("ascii")), "details": result.details,
            "claimed_plaintext": None}
        if reference is not None:
            entry["reference_comparison"] = {"reference_plaintext": reference,
                "expected_sha256": sha(reference.encode("ascii")), "recovered_sha256": sha(plain.encode("ascii")),
                "matching_positions": sum(a == b for a, b in zip(plain, reference)),
                "exact_match": plain == reference, "length": len(reference),
                "key_supplied_to_search": False,
                "provenance": "Constructed independent prose, never used to fit the scoring model"}
        destination.append(entry)
        print(json.dumps({"run": name, "proposals": proposals, "seconds": entry["elapsed_seconds"],
            "control_matches": entry.get("reference_comparison", {}).get("matching_positions"),
            "stop_reason": result.details.get("stop_reason")}), flush=True)
        return True

    # All known-answer controls and two exploratory nulls precede target runs.
    for i, (prose, key) in enumerate(zip(CONTROL_PROSE, KEYS)):
        reference = letters_only(prose)[:87]
        if len(reference) != 87:
            raise AssertionError("short control must contain 87 letters")
        search(f"matched87-control-{i}", replay(reference, key), 1009 + i, 500_000, report["controls"], reference)
    for i, seed in enumerate((9011, 9029)):
        glyphs = list(CT)
        random.Random(seed).shuffle(glyphs)
        shuffled = "".join(glyphs)
        if Counter(shuffled) != Counter(CT):
            raise AssertionError("null symbol counts changed")
        search(f"same-count-shuffled-null-{i}", shuffled, 10103 + i, 1_000_000, report["null_runs"])
        if report["null_runs"]:
            report["null_runs"][-1]["shuffle_seed"] = seed
    for seed in TARGET_SEEDS:
        if not search(f"broader-corpus-target-{seed}", CT, seed, 1_000_000, report["target_runs"]):
            break
    report["actual_proposals"] = total
    report["actual_search_seconds"] = time.perf_counter() - started
    report["completed_target_runs"] = len(report["target_runs"])
    report["stopped_before_all_scheduled_target_runs"] = len(report["target_runs"]) != len(TARGET_SEEDS)
    report["independently_verified_historical_plaintext_available"] = False
    if report["target_runs"] and report["null_runs"]:
        best_target = max(r["score"] for r in report["target_runs"])
        best_null = max(r["score"] for r in report["null_runs"])
        report["exploratory_null_comparison"] = {"best_target_score": best_target, "best_null_score": best_null,
            "target_minus_best_null": best_target - best_null,
            "limitation": "Two shuffles and unequal numbers of target/null restarts do not yield a p-value or a correctness probability"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--austen", type=Path, required=True)
    parser.add_argument("--bronte", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=REPO / "docs/logs/dorabella-corpus-2026-10-03.json")
    arguments = parser.parse_args()
    result = run(arguments)
    print(json.dumps({"output": str(arguments.output), "target_runs": result["completed_target_runs"],
        "actual_proposals": result["actual_proposals"], "status": result["status"]}), flush=True)
