# -*- coding: utf-8 -*-
"""Shared progress logger for the release_h1 package.

Every notable step writes a timestamped line to release_h1/progress.log with an
immediate flush to disk (so an empty log is never confused with a hang). Long
computations call progress() with current index, total and elapsed to emit a
remaining-time estimate.
"""
import os
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROG = HERE / "progress.log"

_T0 = time.time()


def _ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(msg, flush=True):
    line = "[%s] %s" % (_ts(), msg)
    with open(PROG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        if flush:
            f.flush()
    return line


def progress(label, i, total, t0=None, flush=True):
    """Emit a remaining-time estimate for a long loop.

    label  : human-readable name of the computation
    i, total: 1-based current index and total count
    t0     : start time (time.time()); defaults to module load
    """
    t0 = t0 if t0 is not None else _T0
    elapsed = max(time.time() - t0, 1e-9)
    done = i / float(total) if total else 1.0
    remain = elapsed / done * (1.0 - done) if done < 1.0 else 0.0
    line = "[%s] %s: %d/%d (%.1f%%) elapsed=%.1fs ETA=%.1fs" % (
        _ts(), label, i, total, done * 100.0, elapsed, remain)
    with open(PROG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        if flush:
            f.flush()
    return line
