# -*- coding: utf-8 -*-
"""Arcwise Rouché transfer from H_7 to the limiting function H on |u|=7."""

from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

import flint


ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
H7_PATH = HERE / "h7_circle_certificate.json"
SLICE_PATH = HERE / "pilot_slice_summary.json"
CL34_PATH = ROOT / "w36" / "tail_codex" / "cl34_certificate.json"
ABS36_PATH = ROOT / "w36" / "audit_codex" / "absolute_margins_arb.json"
OUT_PATH = HERE / "arcwise_rouche_certificate.json"
LOG_PATH = HERE / "arcwise_rouche_certificate.log"

flint.ctx.prec = 512
A = flint.arb
T0 = time.time()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def up(x):
    return A(x).upper()


def lo(x):
    return A(x).lower()


def log(message: str) -> None:
    line = f"[{time.time()-T0:7.2f}s] {message}"
    print(line, flush=True)
    with LOG_PATH.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")
        stream.flush()
        os.fsync(stream.fileno())


with H7_PATH.open(encoding="utf-8") as stream:
    h7 = json.load(stream)
with SLICE_PATH.open(encoding="utf-8") as stream:
    slices = json.load(stream)
with CL34_PATH.open(encoding="utf-8") as stream:
    cl34 = json.load(stream)
with ABS36_PATH.open(encoding="utf-8") as stream:
    abs36 = json.load(stream)

if not h7.get("pass") or h7["main"].get("count") != 2:
    raise RuntimeError("H7 winding dependency failed")
if not slices.get("all_pass"):
    raise RuntimeError("stable-tube dependency failed")
if not cl34.get("pass"):
    raise RuntimeError("CL34 dependency failed")

# Same all-level constants as the audited wave-36 assembly.  The disk-7
# parameter satisfies |t|=7*AU0 < 4.7911, so all global bootstrap and
# infinite geometric-tail lemmas apply without alteration.
AU0 = A("0.41403799908627305889537448439555967803329915886199")
delta = A("4.669201609102990671853", A("1e-27"))
delta_lower = lo(delta)
K = A("284")
M3 = A("1834")
q2 = A("111.550905120798913")
nDT = A("22.19")
nDT2 = A("193.63")
rho_star = A("7.5e-4")
linf = A("1.10485425032")
pperp = A("2.808542")

# The w36 value already contains the certified Taylor tail.  Add the full
# CL34 stored-centre error once more to dominate every normalization/head
# component as well.
nh = up(A(abs36["nh_upper"])) + up(A(cl34["V_h_delta"]["h_error_stored_center_upper"]))
L1 = nDT + K * rho_star
L2 = nDT2 + 2 * nDT * K * rho_star + (K * rho_star) ** 2
d2 = delta_lower ** 2
d4 = delta_lower ** 4
Fstar = (1 + L1 / d2) / (1 - L2 / d4)
t_abs = up(A(7) * AU0)
s8 = up(t_abs / (delta_lower ** 8))
q3 = M3 * nh ** 3 / 6
Phi = up(q2 * s8 ** 2 + q3 * s8 ** 3)

LOG_PATH.write_text("", encoding="utf-8")
log(f"|t|<={t_abs}; s8<={s8}; Phi<={Phi}; Fstar<={up(Fstar)}; ||h||<={nh}")

rows = []
all_pass = True
for row in slices["arcs"]:
    h7_lower = lo(A(row["H7_abs_lower"]))
    ph = up(A(repr(row["ph_tube"])))
    ns = up(A(repr(row["Ns_tube"])))
    L7 = up(linf * ph + pperp * ns)
    Btail = up(up(Fstar) * L7 * Phi)
    difference = lo(h7_lower - Btail)
    ratio = lo(h7_lower / Btail)
    passed = bool(difference > 0 and ratio > 1)
    all_pass &= passed
    rows.append({
        "t1": row["t1"],
        "t2": row["t2"],
        "n_arcs": row["n_arcs"],
        "arc": row["arc"],
        "H7_abs_lower": str(h7_lower),
        "phih_tube_upper": str(ph),
        "Ns_tube_upper": str(ns),
        "L7_tube_upper": str(L7),
        "H_minus_H7_upper": str(Btail),
        "absolute_gap_lower": str(difference),
        "rouche_margin_lower": str(ratio),
        "pass": passed,
    })

worst = min(rows, key=lambda row: float(A(row["rouche_margin_lower"]).lower()))
min_gap = min(rows, key=lambda row: float(A(row["absolute_gap_lower"]).lower()))
log(
    "worst ratio: arc %s/%s t=[%s,%s], |H7|>=%s, tail<=%s, margin>=%s"
    % (
        worst["arc"], worst["n_arcs"], worst["t1"], worst["t2"],
        worst["H7_abs_lower"], worst["H_minus_H7_upper"],
        worst["rouche_margin_lower"],
    )
)
log(
    "smallest absolute gap: arc %s/%s gap>=%s"
    % (min_gap["arc"], min_gap["n_arcs"], min_gap["absolute_gap_lower"])
)

payload = {
    "status": "ARCWISE_ROUCHE_COMPLETENESS_ON_DISK_U_LT_7",
    "precision_bits": 512,
    "dependencies": {
        "H7_certificate_sha256": sha256(H7_PATH),
        "stable_slice_summary_sha256": sha256(SLICE_PATH),
        "CL34_sha256": sha256(CL34_PATH),
        "wave36_absolute_constants_sha256": sha256(ABS36_PATH),
    },
    "domain": "|u|<7",
    "boundary": "|u|=7, positively oriented",
    "H7_zero_count": h7["main"]["count"],
    "constants": {
        "t_abs_upper": str(t_abs),
        "s8_upper": str(s8),
        "Phi_upper": str(Phi),
        "Fstar_upper": str(up(Fstar)),
        "h_l1_upper": str(nh),
    },
    "arc_count": len(rows),
    "all_arcwise_rouche_pass": all_pass,
    "worst_margin": worst,
    "smallest_absolute_gap": min_gap,
    "rows": rows,
    "conclusion": (
        "H and H7 have the same number of zeros with multiplicity in |u|<7; that number is exactly 2."
        if all_pass else "No completeness conclusion."
    ),
    "pass": all_pass and h7["main"]["count"] == 2,
}
OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
log(f"OVERALL PASS={payload['pass']}; wrote {OUT_PATH}")
if not payload["pass"]:
    raise SystemExit(1)

