# -*- coding: utf-8 -*-
"""run_tampers.py -- tamper battery for bridge_verify.py (project standard:
>=6 deliberate corruptions of bridge_certificate.json, each must make the
verifier exit 1; plus one clean control run that must exit 0).

Principle: lie PLAUSIBLY -- keep the corrupted certificate internally
consistent where possible, so the corruption is caught only by RECOMPUTATION
from primary sources, not by cross-field bookkeeping.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT = HERE / "bridge_certificate.json"
TMP_DIR = HERE / "tamper_tmp"
TMP_DIR.mkdir(exist_ok=True)
LOG = HERE / "TAMPER_LOG.md"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def find_new(c, label, m):
    for r in c["new_windings"]:
        if r["label"] == label and r["m"] == m:
            return r
    raise KeyError((label, m))


def find_disk(c, label):
    for b in c["bridge_table"]:
        if b["label"] == label:
            return b
    raise KeyError(label)


def t1(c):
    """M1-style: Z57@8 winding_candidate := 1 while keeping strictly_zero=true,
    pass=true and every aggregate untouched (internally 'consistent' lie;
    caught only by tuple-path recomputation)."""
    find_new(c, "Z57", 8)["winding_candidate"] = 1
    return "T1 Z57@8 winding_candidate := 1 (strictly_zero/pass/aggregates kept true)"


def t2(c):
    """The exact M2 hole of the old winding audit: max_w_upper 0.4 -> 0.999
    (still < 1, no threshold broken, everything else intact)."""
    find_new(c, "Z60", 8)["max_w_upper"] = 0.999
    return "T2 Z60@8 max_w_upper 0.4 -> 0.999 (below the |w|<1 threshold)"


def t3(c):
    """Tube minimum shrunk 1000x on a bridge row (still positive, bridged
    flags kept true) -- caught only by rescanning the 1465 arc files."""
    row = find_disk(c, "Z01")["rows"][0]
    row["tube_min_x128_lower"] = row["tube_min_x128_lower"] / 1000.0
    return "T3 Z01@L7 tube_min_x128_lower /= 1000 (still > 0, flags kept)"


def t4(c):
    """sha256 pin of the base winding certificate zeroed."""
    c["sha256_pins"]["winding_certificate.json"] = "0" * 64
    return "T4 sha256 pin winding_certificate.json := 000...0"


def t5(c):
    """Containment: P_tail claimed 6e-7 (> tube radius 5.44e-7) but the
    containment_ok flags LEFT TRUE (self-consistent lie about the source)."""
    c["containment"]["P_tail_m0_primary_upper"] = 6e-7
    return "T5 containment P_tail := 6e-7 (> tube radius) with flags kept true"


def t6(c):
    """Arc bookkeeping: Z72@L8 tube_n_arcs 64 -> 128 (a plausible number:
    as if the stage9 refinement family were counted as coverage)."""
    for r in find_disk(c, "Z72")["rows"]:
        if r["level_m"] == 8:
            r["tube_n_arcs"] = 128
    return "T6 Z72@L8 tube_n_arcs 64 -> 128"


def t7(c):
    """Requirement downgrade: Z57 required_levels [7,8] -> [7] (as if the m=8
    closure did not need its own winding level)."""
    find_disk(c, "Z57")["required_levels"] = [7]
    return "T7 Z57 required_levels [7,8] -> [7]"


def t8(c):
    """Geometry: last digit of Z60@8 centre_re nudged (caught against the RAW
    point14 certificate, not against any field of this certificate)."""
    r = find_new(c, "Z60", 8)
    r["centre_re"] = r["centre_re"][:-1] + ("2" if r["centre_re"][-1] != "2" else "3")
    return "T8 Z60@8 centre_re last digit nudged (vs raw m8_certificate.json)"


def t9(c):
    """Legacy bucket: 24 superseded census_B Z72 arcs claimed as 0 (as if the
    old contour never existed)."""
    c["legacy_z72_old_contour_arcs_nonblocking"] = 0
    return "T9 legacy_z72_old_contour_arcs 24 -> 0"


def t10(c):
    """Simulate the PRE-FIX attribution bug found by the fable review:
    (Z72, 7) coverage claimed via the PARTIAL stage9_L7 family only, with
    coverage_complete forged to true and bridged kept true."""
    for r in find_disk(c, "Z72")["rows"]:
        if r["level_m"] == 7:
            r["tube_families"] = [{
                "family": "point17_z72_geometry:Z72_stage9_L7",
                "group": "point17_z72_geometry", "n_arcs": 128,
                "contiguous_full": True, "min_x128_lower": 5.9e-3,
            }]
            r["tube_n_arcs"] = 128
            r["coverage_complete"] = True
    return "T10 Z72@L7 coverage claimed via partial stage9 family (pre-fix bug simulated)"


def t11(c):
    """Reported field: containment_margin := 1.874e-7 (the misleading two-term
    headroom), flags and P_tail left intact -- fable's missed porcha #1."""
    c["containment"]["containment_margin"] = 1.874e-7
    return "T11 containment_margin := 1.874e-7 (two-term headroom instead of real one)"


def t12(c):
    """min_abs_denominator_lower scaled by 0.985 -- fable's missed porcha #2
    (was inside the old 2e-2 tolerance; the tolerance is now 1e-3)."""
    r = find_new(c, "Z57", 8)
    r["min_abs_denominator_lower"] = r["min_abs_denominator_lower"] * 0.985
    return "T12 Z57@8 min_abs_denominator_lower *= 0.985 (inside old 2e-2 tolerance)"


def t13(c):
    """Family provenance: Z01's tube family renamed to census_B -- fable's
    missed porcha #3 (tube_groups was not verified before)."""
    for r in find_disk(c, "Z01")["rows"]:
        for fm in r["tube_families"]:
            fm["family"] = "point10_layer1_census_B:Z01"
            fm["group"] = "point10_layer1_census_B"
    return "T13 Z01 tube family attributed to census_B instead of census_A"


def t14(c):
    """kilo K1: stray list emptied (as if no unattributed files existed)."""
    c["stray_tube_labels_nonblocking"] = []
    return "T14 (kilo K1) stray_tube_labels_nonblocking := []"


def t15(c):
    """kilo K2: winding_source forged on a bridge row."""
    find_disk(c, "Z40")["rows"][0]["winding_source"] = "bridge_certificate.py (new, m=7)"
    return "T15 (kilo K2) Z40@L7 winding_source forged"


def t16(c):
    """kilo K3: new winding Z57@8 n_arcs 32 -> 64 (winding at 64 arcs would
    also be strictly zero -- caught only by replicating the adaptive rule)."""
    find_new(c, "Z57", 8)["n_arcs"] = 64
    return "T16 (kilo K3) Z57@8 n_arcs 32 -> 64"


def t17(c):
    """kilo K4: table's winding_strictly_zero := false while bridged kept true."""
    find_disk(c, "Z40")["rows"][0]["winding_strictly_zero"] = False
    return "T17 (kilo K4) Z40@L7 winding_strictly_zero := false (bridged kept true)"


TAMPERS = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17]


def run_verify(path):
    p = subprocess.run([sys.executable, str(HERE / "bridge_verify.py"), str(path)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    rows = []
    t0 = time.time()

    print("clean control...")
    rc, _ = run_verify(CERT)
    clean_ok = (rc == 0)
    print("  clean exit=%d (expect 0)" % rc)

    for fn in TAMPERS:
        c = copy.deepcopy(load())
        desc = fn(c)
        tmp = TMP_DIR / ("tampered_%s.json" % fn.__name__)
        tmp.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
        rc, out = run_verify(tmp)
        caught = (rc == 1)
        first_fail = next((ln.strip() for ln in out.splitlines() if "FAIL:" in ln), "")
        rows.append((fn.__name__.upper(), desc, caught, rc, first_fail))
        print("  %s exit=%d %s" % (fn.__name__.upper(), rc, "CAUGHT" if caught else "MISSED"))

    n_caught = sum(1 for r in rows if r[2])
    lines = [
        "# TAMPER_LOG.md -- tamper battery for bridge_certificate.json",
        "",
        "Date: %s. Clean control: exit=%d (expect 0) -> %s." % (
            time.strftime("%Y-%m-%d %H:%M"), 0 if clean_ok else 1,
            "OK" if clean_ok else "BROKEN"),
        "",
        "| # | corruption | caught | exit | first failing check |",
        "|---|---|---|---|---|",
    ]
    for name, desc, caught, rc, ff in rows:
        lines.append("| %s | %s | %s | %d | %s |" % (
            name, desc.replace("|", "/"), "CAUGHT" if caught else "**MISSED**", rc,
            ff.replace("|", "/")[:160]))
    lines += ["", "**Total: %d/%d caught. Clean control %s.** (%.0fs)" % (
        n_caught, len(rows), "OK" if clean_ok else "BROKEN", time.time() - t0)]
    LOG.write_text("\n".join(lines), encoding="utf-8")
    print("caught %d/%d; clean control %s; written TAMPER_LOG.md" % (
        n_caught, len(rows), "OK" if clean_ok else "BROKEN"))
    return 0 if (clean_ok and n_caught == len(rows)) else 1


if __name__ == "__main__":
    sys.exit(main())
