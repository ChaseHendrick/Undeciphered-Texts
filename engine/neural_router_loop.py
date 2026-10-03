"""Keep fitting the cipher-family router until you stop it.

Start it from the repository root:

    python -m engine.neural_router_loop

One pass, then exit:

    python -m engine.neural_router_loop --once

This module does not register cron, a timer, or any wake outside the process.
Stop a running loop by creating engine/data/neural_router_loop.stop or by
ending the process. Each pass reads the certificate files currently on disk,
adds any new known-answer cipher_name as a class, and writes weights only
when the held-out score does not drop. The router records a family label. It
does not emit plaintext for K4, Zodiac, Beale, McCormick, Voynich, or Nr. 86.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from engine.neural_grade import (
    LOOP_PID_PATH,
    LOOP_STATUS_PATH,
    LOOP_STOP_PATH,
    retrain_router,
)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _write_status(payload: dict) -> None:
    LOOP_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = LOOP_STATUS_PATH.with_suffix(LOOP_STATUS_PATH.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(LOOP_STATUS_PATH)


def run_loop(*, once: bool, pause_seconds: float) -> None:
    """Fit, sleep, repeat. `pause_seconds` is only the gap inside this process."""
    if pause_seconds < 0:
        raise ValueError("pause must be non-negative")
    own_pid = os.getpid()
    if not once and LOOP_PID_PATH.is_file():
        try:
            existing = int(LOOP_PID_PATH.read_text(encoding="utf-8").strip() or "0")
        except ValueError:
            existing = 0
        if existing != own_pid and _pid_alive(existing):
            print(f"neural router loop already running as pid {existing}")
            return
    if not once:
        LOOP_PID_PATH.write_text(f"{own_pid}\n", encoding="utf-8")
    try:
        while True:
            if LOOP_STOP_PATH.is_file():
                print(f"stop file {LOOP_STOP_PATH} is present; leaving the loop")
                break
            started = time.time()
            try:
                report = retrain_router(write=True)
                status = {
                    "ok": True,
                    "pid": own_pid,
                    "wrote": report["wrote"],
                    "accuracy": report["accuracy"],
                    "correct": report["correct"],
                    "total": report["total"],
                    "previous_accuracy": report["previous_accuracy"],
                    "families": report["families"],
                    "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                }
                print(
                    f"held-out {report['correct']}/{report['total']} "
                    f"wrote={report['wrote']} classes={len(report['families'])}"
                )
            except Exception as exc:  # keep the process up across a bad certificate
                status = {
                    "ok": False,
                    "pid": own_pid,
                    "error": str(exc),
                    "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                }
                print(f"router pass failed: {exc}")
            _write_status(status)
            if once:
                break
            elapsed = time.time() - started
            time.sleep(pause_seconds)
            del elapsed
    finally:
        if not once and LOOP_PID_PATH.is_file():
            try:
                recorded = int(LOOP_PID_PATH.read_text(encoding="utf-8").strip() or "0")
            except ValueError:
                recorded = 0
            if recorded == own_pid:
                LOOP_PID_PATH.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fit the cipher router until stopped.")
    parser.add_argument("--once", action="store_true", help="run a single pass and exit")
    parser.add_argument(
        "--sleep",
        type=float,
        default=20.0,
        help="seconds to wait between passes inside this process (default 20)",
    )
    args = parser.parse_args()
    run_loop(once=args.once, pause_seconds=args.sleep)


if __name__ == "__main__":
    main()
