# -*- coding: utf-8 -*-
"""Parallel outer-box stable-tube certificate on |u|=7."""

from __future__ import annotations

import concurrent.futures as cf
import json
import os
import subprocess
import sys
import threading
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PY = sys.executable
WORKERS = int(os.environ.get("PILOT_WORKERS", "16"))
RADIUS = os.environ.get("PILOT_RADIUS", "7.0")
FAT = os.environ.get("PILOT_FAT", "0.0")
RUN_LABEL = os.environ.get("PILOT_RUN_LABEL", "P7tail_")
H7_CERT = Path(os.environ.get("PILOT_PLAN_PATH", str(HERE / "h7_circle_certificate.json")))
LOG = HERE / os.environ.get("PILOT_LOG_NAME", "pilot_slice_run.log")
SUMMARY = HERE / os.environ.get("PILOT_SUMMARY_NAME", "pilot_slice_summary.json")
LOCK = threading.Lock()
T0 = time.time()
done = 0


def load_plan():
    cert = json.loads(H7_CERT.read_text(encoding="utf-8"))
    if "main" in cert:
        if not cert.get("pass") or cert["main"].get("count") != 2:
            raise RuntimeError("H7 circle certificate is not a PASS with count 2")
        source_arcs = cert["main"]["arcs"]
    else:
        if not cert.get("pass"):
            raise RuntimeError("refined H7 plan is not PASS")
        source_arcs = cert["arcs"]
    tasks = []
    for row in source_arcs:
        t1 = Fraction(row["t1"])
        t2 = Fraction(row["t2"])
        width = t2 - t1
        if width.numerator != 1:
            raise RuntimeError(f"non-unit adaptive arc width {width}")
        n_arcs = width.denominator
        arc = t1 * n_arcs
        if arc.denominator != 1:
            raise RuntimeError(f"nonintegral arc index {arc}")
        tasks.append({
            "n_arcs": n_arcs,
            "arc": arc.numerator,
            "t1": str(t1),
            "t2": str(t2),
            "H7_abs_lower": row.get("H_abs_lower", row.get("H7_abs_lower")),
        })
    return tasks


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')} +{time.time()-T0:8.1f}s] {message}"
    with LOCK:
        print(line, flush=True)
        with LOG.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")
            stream.flush()
            os.fsync(stream.fileno())


def one(task: dict) -> dict:
    global done
    arc = task["arc"]
    n_arcs = task["n_arcs"]
    try:
        for mode, kdom in (("base", "0"), ("tube", "100")):
            output = HERE / f"cert_slice_{RUN_LABEL}outerbox_{mode}_K{kdom}_P7{n_arcs}a{arc}.json"
            if output.exists():
                continue
            env = os.environ.copy()
            env.update({
                "PILOT_RADIUS": RADIUS,
                "PILOT_FAT": FAT,
                "SLICE_OUTER_BOX": "1",
                "SLICE_RUN_LABEL": RUN_LABEL,
                "SLICE_INJECT_TAIL": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
            })
            run = subprocess.run(
                [PY, str(HERE / "pilot_slice.py"), mode, kdom, "", "P7", str(n_arcs), str(arc)],
                capture_output=True,
                text=True,
                timeout=1800,
                cwd=str(HERE),
                env=env,
            )
            if run.returncode != 0:
                raise RuntimeError(f"{mode} rc={run.returncode}: {(run.stderr or run.stdout)[-1400:]}")
        data = json.loads(
            (HERE / f"cert_slice_{RUN_LABEL}outerbox_tube_K100_P7{n_arcs}a{arc}.json").read_text(encoding="utf-8")
        )
        result = {
            "arc": arc,
            "n_arcs": n_arcs,
            "t1": task["t1"],
            "t2": task["t2"],
            "H7_abs_lower": task["H7_abs_lower"],
            "ok": True,
            "Ns_base": data["N_s_base_upper"],
            "Ns_tube": data["N_s_tube_upper"],
            "ph_base": data["phih_base_upper"],
            "ph_tube": data["phih_tube_upper"],
            "Rmax": data["Rmax_upper"],
            "x128_lower": data["x128_lower"],
            "tail_symbol_injected": data["tail_symbol_injected"],
            "CL34_full_G_h_errors_injected": data["CL34_full_G_h_errors_injected"],
            "EPS_G_FULL": data["EPS_G_FULL"],
            "EPS_H_FULL": data["EPS_H_FULL"],
            "tail_value_max": data["tail_symbol_value_max"],
            "tail_derivative_max": data["tail_symbol_derivative_max"],
        }
    except Exception as exc:
        result = {**task, "ok": False, "error": repr(exc)}
    with LOCK:
        done += 1
        elapsed = time.time() - T0
        eta = elapsed / done * (TOTAL - done)
        now_done = done
    if result["ok"]:
        log(
            f"arc {arc:03d}/{n_arcs}: Ns={result['Ns_tube']:.6e} ph={result['ph_tube']:.6e} "
            f"Rmax={result['Rmax']:.6f} [{now_done}/{TOTAL}, ETA {eta/60:.1f}m]"
        )
    else:
        log(f"arc {arc:03d}/{n_arcs}: FAIL {result['error']} [{now_done}/{TOTAL}]")
    return result


def main() -> None:
    LOG.write_text("", encoding="utf-8")
    log(f"START radius={RADIUS}, fat={FAT}, adaptive_arcs={TOTAL}, workers={WORKERS}")
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        rows = list(pool.map(one, PLAN))
    good = [row for row in rows if row["ok"]]
    bad = [row for row in rows if not row["ok"]]
    payload = {
        "status": "PILOT_DISK7_STABLE_TUBE",
        "precision_bits": 512,
        "radius": RADIUS,
        "fat": FAT,
        "adaptive_arcs": TOTAL,
        "uniform_denominators": sorted(set(task["n_arcs"] for task in PLAN)),
        "workers": WORKERS,
        "frozen_kernel": "w36/audit_codex/cert_slice_param_audit.py",
        "outer_coordinate_box": True,
        "arbitrary_tail_symbol_injected": True,
        "wall_s": time.time() - T0,
        "all_pass": (len(good) == TOTAL and not bad
                     and all(r["tail_symbol_injected"] for r in good)
                     and all(r["CL34_full_G_h_errors_injected"] for r in good)),
        "maxima": ({
            "Ns_base": max(r["Ns_base"] for r in good),
            "Ns_tube": max(r["Ns_tube"] for r in good),
            "ph_base": max(r["ph_base"] for r in good),
            "ph_tube": max(r["ph_tube"] for r in good),
            "Rmax": max(r["Rmax"] for r in good),
            "tail_value": max(r["tail_value_max"] for r in good),
            "tail_derivative": max(r["tail_derivative_max"] for r in good),
        } if good else {}),
        "failed": bad,
        "arcs": rows,
    }
    SUMMARY.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"OVERALL PASS={payload['all_pass']} good={len(good)}/{TOTAL} wall={payload['wall_s']:.1f}s")
    if not payload["all_pass"]:
        raise SystemExit(1)


PLAN = load_plan()
TOTAL = len(PLAN)


if __name__ == "__main__":
    main()
