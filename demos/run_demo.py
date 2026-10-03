#!/usr/bin/env python3
"""Write DEMO.md by generating ciphertext and recovering it."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.demo import run_demo


if __name__ == "__main__":
    raise SystemExit(run_demo(str(ROOT / "DEMO.md")))
