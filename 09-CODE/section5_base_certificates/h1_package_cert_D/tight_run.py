# -*- coding: utf-8 -*-
"""Orchestrator for item C: recompute the SIX worst Z72 tube arcs with the
TIGHT tube l1 budget R_S = 3.566e-7 (actual exit r_s) instead of the frozen
conservative tube_radius 5.44e-7. Drives tight_arcs/tight_pilot.py.

Per arc, runs the validated 3-subprocess sequence (base -> outerbox_base ->
tube), exactly like census_B_run.py's one_arc_task but with the tight pilot.
base and outerbox_base do NOT depend on R_S (no tube budget in K_DOM=0 mode),
so they reproduce the archive byte-for-byte; only the tube step tightens.

Budget: 4 parallel workers, each spawned at Windows IDLE priority class
(inherited + explicitly set via ctypes). Output JSONs land in tight_arcs/.
Progress -> ../progress.log (flushed).
"""
from __future__ import annotations
import ctypes
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
TIGHT_DIR = HERE / "tight_arcs"
PILOT = TIGHT_DIR / "tight_pilot.py"
PROGRESS = HERE / "progress.log"
T0 = time.time()

# Z72 disk geometry (from point10_layer1_census_B/census_B_run.py DISKS entry).
DISK = {"label": "Z72", "re": "4.79165", "im": "7.177607", "rho": "0.1", "n_arcs": 32}

# The six Z72 arcs with Rmax_upper > 0.5 (scan_z72.py over census_B archive).
ARCS = [6, 13, 8, 12, 14, 11]
CONSERVATIVE_RMAX = {
    6: 0.884996133213671, 13: 0.7143768149736405, 8: 0.6402520439773116,
    12: 0.5365224978508042, 14: 0.5197376009868044, 11: 0.5082233538322567,
}
WORKERS = 4

# --- Windows idle priority (no psutil available) ---
_PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
_PROCESS_SET_INFORMATION = 0x0200
_IDLE_PRIORITY_CLASS = 0x40
kernel32 = ctypes.windll.kernel32
kernel32.OpenProcess.restype = ctypes.c_void_p
kernel32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
kernel32.SetPriorityClass.restype = ctypes.c_int
kernel32.CloseHandle.argtypes = [ctypes.c_void_p]


def _idle(pid: int) -> None:
    h = kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION | _PROCESS_SET_INFORMATION, False, pid)
    if h:
        kernel32.SetPriorityClass(h, _IDLE_PRIORITY_CLASS)
        kernel32.CloseHandle(h)


def log(msg: str) -> None:
    line = "[%s +%8.1fs] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), time.time() - T0, msg)
    print(line, flush=True)
    with PROGRESS.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_kernel(mode, k_dom, arc, env_extra, timeout=1800):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PILOT_CENTER_RE"] = DISK["re"]
    env["PILOT_CENTER_IM"] = DISK["im"]
    env["PILOT_RADIUS"] = DISK["rho"]
    env["PILOT_FAT"] = "0"
    env["SLICE_RUN_LABEL"] = DISK["label"] + "_"
    env.update(env_extra)
    argv = [sys.executable, str(PILOT), mode, str(k_dom), "none", "P7",
            str(DISK["n_arcs"]), str(arc)]
    t0 = time.time()
    # CREATE_NEW_PROCESS_GROUP not needed; we set idle right after spawn.
    proc = subprocess.Popen(argv, cwd=str(TIGHT_DIR), env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    _idle(proc.pid)
    try:
        out, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, _ = proc.communicate()
        return None, time.time() - t0, "TIMEOUT", out
    rc = proc.returncode
    dt = time.time() - t0
    return rc, dt, ("OK" if rc == 0 else "RC=%d" % rc), out


def tube_path(arc):
    return TIGHT_DIR / ("cert_slice_%s_outerbox_tube_K100_P7%da%d.json" % (DISK["label"], DISK["n_arcs"], arc))


def base_path(arc):
    return TIGHT_DIR / ("cert_slice_%s_base_K0_P7%da%d.json" % (DISK["label"], DISK["n_arcs"], arc))


def ob_base_path(arc):
    return TIGHT_DIR / ("cert_slice_%s_outerbox_base_K0_P7%da%d.json" % (DISK["label"], DISK["n_arcs"], arc))


def one_arc(arc):
    t_a = time.time()
    # 1. base
    if not base_path(arc).exists():
        rc, dt, st, out = run_kernel("base", 0, arc, {})
        if rc != 0:
            return {"arc": arc, "ok": False, "stage": "base", "st": st, "dt": dt, "out": out[-1200:]}
    b = json.load(base_path(arc).open(encoding="utf-8"))
    if not (float(b.get("Rmax_upper", 2)) < 1.0):
        return {"arc": arc, "ok": False, "stage": "base_admissibility", "st": "Rmax>=1", "dt": time.time()-t_a}
    # 2. outerbox_base
    if not ob_base_path(arc).exists():
        rc, dt, st, out = run_kernel("base", 0, arc, {"SLICE_OUTER_BOX": "1", "SLICE_INJECT_TAIL": "1"})
        if rc != 0:
            return {"arc": arc, "ok": False, "stage": "outerbox_base", "st": st, "dt": dt, "out": out[-1200:]}
    ob = json.load(ob_base_path(arc).open(encoding="utf-8"))
    if not (float(ob.get("Rmax_upper", 2)) < 1.0):
        return {"arc": arc, "ok": False, "stage": "outerbox_base_admissibility", "st": "Rmax>=1", "dt": time.time()-t_a}
    # 3. tube (TIGHT R_S)
    rc, dt, st, out = run_kernel("tube", 100, arc, {"SLICE_OUTER_BOX": "1", "SLICE_INJECT_TAIL": "1"})
    if rc != 0:
        return {"arc": arc, "ok": False, "stage": "tube", "st": st, "dt": dt, "out": out[-2000:]}
    t = json.load(tube_path(arc).open(encoding="utf-8"))
    return {"arc": arc, "ok": True, "tube": t, "base": b, "ob_base": ob, "dt": time.time()-t_a,
            "stage": "tube", "conservative_Rmax": CONSERVATIVE_RMAX[arc]}


def main():
    TIGHT_DIR.mkdir(parents=True, exist_ok=True)
    log("=== tight_run.py START: Z72 tight R_S=3.566e-7, %d arcs, workers=%d, idle priority ===" % (len(ARCS), WORKERS))
    log("arcs (sorted by conservative Rmax desc): %s" % ARCS)
    results = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(one_arc, a): a for a in ARCS}
        done = 0
        for fut in as_completed(futs):
            a = futs[fut]
            try:
                r = fut.result()
            except Exception as e:
                r = {"arc": a, "ok": False, "stage": "exception", "st": str(e), "dt": 0.0}
            results[a] = r
            done += 1
            eta = (time.time() - T0) / done * (len(ARCS) - done)
            if r["ok"]:
                t = r["tube"]
                old = r["conservative_Rmax"]
                new = t["Rmax_upper"]
                log("  arc %2d TUBE OK dt=%.1fs [%d/%d] ETA %.0fs | r_s=%.4e  Rmax %.6f -> %.6f  x128_lower=%.4e  pass(<1)=%s" % (
                    a, r["dt"], done, len(ARCS), eta, t["r_s"], old, new, t["x128_lower"], new < 1.0))
            else:
                log("  arc %2d FAIL stage=%s st=%s [%d/%d] | tail: %s" % (a, r["stage"], r.get("st"), done, len(ARCS), r.get("out", "")[-400:]))
    log("=== tight_run.py DONE, wall=%.1fs ===" % (time.time() - T0))

    # Summary table
    log("--- SUMMARY (tight R_S=3.566e-7) ---")
    log("  arc | conservative Rmax | tight Rmax | tube_excess_cons(=Rmax-0.40) | scaled=excess*0.6555 | headroom")
    ratio = 3.5659822966266e-7 / 5.44e-7
    for a in sorted(results, key=lambda x: -CONSERVATIVE_RMAX[x]):
        r = results[a]
        if not r["ok"]:
            log("  arc %2d FAILED (%s/%s)" % (a, r["stage"], r.get("st")))
            continue
        old = CONSERVATIVE_RMAX[a]
        new = r["tube"]["Rmax_upper"]
        excess_old = old - 0.40
        linear_pred = 0.40 + excess_old * ratio
        log("  %2d  | %.6f          | %.6f   | %.6f                  | %.6f             | new-pred=%+.4e" % (
            a, old, new, excess_old, linear_pred, new - linear_pred))

    # Write machine-readable summary
    summ = {"r_s_tight": 3.566e-7, "r_s_conservative": 5.44e-7, "ratio": ratio,
            "disk": DISK, "arcs": {}}
    for a in results:
        r = results[a]
        if r["ok"]:
            t = r["tube"]
            summ["arcs"][str(a)] = {
                "Rmax_conservative": CONSERVATIVE_RMAX[a],
                "Rmax_tight": t["Rmax_upper"],
                "x128_lower": t["x128_lower"],
                "r_s_in_json": t["r_s"],
                "N_s_tube_upper": t["N_s_tube_upper"],
                "phih_tube_upper": t["phih_tube_upper"],
                "kappa_D": t["kappa_D"],
                "tube_json": tube_path(a).name,
            }
        else:
            summ["arcs"][str(a)] = {"failed": True, "stage": r["stage"], "st": r.get("st")}
    (HERE / "tight_arcs_summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=2), encoding="utf-8")
    log("summary -> tight_arcs_summary.json")


if __name__ == "__main__":
    main()
