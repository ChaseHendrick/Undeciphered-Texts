"""Bob's scratch paper. A note is a short record, not a reading.

The pad can hold a step name, a family, a method, a key, a score, a yes or
no, and a hash. It refuses a plaintext field and any letter string long
enough to be a sentence. The hash of the pad is the only thing a report
needs to keep.
"""

from __future__ import annotations

import hashlib
import json
import re

_LONG_LETTERS = re.compile(r"[A-Za-z]{20}")
_BANNED = ("plain", "reading", "letters", "crib")


def open_pad() -> list[dict]:
    """Start an empty pad. Nothing is written to disk."""
    return []


def write_note(pad: list[dict], **fields) -> dict:
    """Append one note. A plaintext, or twenty letters in a row, is refused."""
    if not isinstance(pad, list):
        raise TypeError("a scratch pad is a list")
    if "step" not in fields or not isinstance(fields["step"], str) or not fields["step"].strip():
        raise ValueError("a scratch note needs a step")
    clean: dict = {}
    for key, value in fields.items():
        if not isinstance(key, str):
            raise TypeError("a scratch field name must be text")
        folded = key.lower()
        if any(token in folded for token in _BANNED):
            raise ValueError("scratch paper cannot hold a plaintext")
        if isinstance(value, str) and _LONG_LETTERS.search(value):
            raise ValueError("scratch paper cannot hold a letter string")
        if folded == "sha256":
            if value is not None and (
                not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value)
            ):
                raise ValueError("a scratch hash must be 64 hex characters")
        clean[key] = value
    pad.append(clean)
    return clean


def pad_digest(pad: list[dict]) -> str:
    """Stable hash of the notes. The notes themselves are not a reading."""
    if not isinstance(pad, list):
        raise TypeError("a scratch pad is a list")
    raw = json.dumps(pad, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
