# -*- coding: utf-8 -*-
"""Independent assembly and geometry audit for the disk-|u|<7 certificate."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import flint


ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
flint.ctx.prec = 512
A, C = flint.arb, flint.acb
I = C(0, 1)
PI = A.pi()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def lo(value):
    return A(value).lower()


def up(value):
    return A(value).upper()


paths = {
    "H7": HERE / "h7_circle_certificate.json",
    "refined": HERE / "h7_refined_cover.json",
    "slices": HERE / "pilot_slice_summary.json",
    "rouche": HERE / "arcwise_rouche_certificate.json",
    "CL34": ROOT / "w36" / "tail_codex" / "cl34_certificate.json",
    "absolute36": ROOT / "w36" / "audit_codex" / "absolute_margins_arb.json",
}
data = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in paths.items()}
h7, refined, slices, rouche = (data[name] for name in ("H7", "refined", "slices", "rouche"))

checks = {}
checks["H7_main_count_is_2"] = h7.get("pass") and h7["main"].get("count") == 2
checks["nested_count_is_1"] = h7["nested_control"].get("pass") and h7["nested_control"].get("count") == 1
checks["coarse_negative_control_rejects"] = not h7["negative_control"].get("pass")
checks["refined_cover_pass"] = bool(refined.get("pass"))
checks["stable_tubes_pass"] = bool(slices.get("all_pass"))
checks["rouche_pass"] = bool(rouche.get("pass"))

# Dependency hashes in the final Rouché record must point at the exact inputs
# being audited here.
deps = rouche["dependencies"]
checks["dependency_H7_hash"] = deps["H7_certificate_sha256"] == sha256(paths["H7"])
checks["dependency_slice_hash"] = deps["stable_slice_summary_sha256"] == sha256(paths["slices"])
checks["dependency_CL34_hash"] = deps["CL34_sha256"] == sha256(paths["CL34"])
checks["dependency_absolute36_hash"] = deps["wave36_absolute_constants_sha256"] == sha256(paths["absolute36"])

# Exact rational tiling and row-by-row agreement of the three certificates.
cover_rows = sorted(refined["arcs"], key=lambda row: Fraction(row["t1"]))
slice_rows = sorted(slices["arcs"], key=lambda row: Fraction(row["t1"]))
rouche_rows = sorted(rouche["rows"], key=lambda row: Fraction(row["t1"]))
checks["same_arc_count"] = len(cover_rows) == len(slice_rows) == len(rouche_rows) == 114
checks["cover_starts_and_ends_exactly"] = (
    Fraction(cover_rows[0]["t1"]) == 0 and Fraction(cover_rows[-1]["t2"]) == 1
)
checks["no_gaps_or_overlaps"] = all(
    Fraction(left["t2"]) == Fraction(right["t1"])
    for left, right in zip(cover_rows, cover_rows[1:])
)
keys_cover = [(row["t1"], row["t2"]) for row in cover_rows]
checks["same_arc_keys"] = (
    keys_cover == [(row["t1"], row["t2"]) for row in slice_rows]
    == [(row["t1"], row["t2"]) for row in rouche_rows]
)
checks["same_H7_lower_bounds"] = all(
    c["H_abs_lower"] == s["H7_abs_lower"]
    and lo(r["H7_abs_lower"]) <= lo(c["H_abs_lower"])
    for c, s, r in zip(cover_rows, slice_rows, rouche_rows)
)

# The stable kernel uses binary64 midpoint geometry plus a 1e-9 inflation.
# Prove in Arb that every exact circular arc is contained in the disk actually
# supplied to that kernel, including the binary64 centre displacement.
geometry_slacks = []
for row in slice_rows:
    n, j = row["n_arcs"], row["arc"]
    exact_theta = 2 * PI * A(2 * j + 1) / A(2 * n)
    exact_midpoint = C(7) * (I * C(exact_theta)).exp()
    float_lo = 2.0 * math.pi * j / n
    float_hi = 2.0 * math.pi * (j + 1) / n
    float_mid = 0.5 * (float_lo + float_hi)
    float_centre = C(repr(7.0 * math.cos(float_mid)), repr(7.0 * math.sin(float_mid)))
    centre_error = (exact_midpoint - float_centre).abs_upper()
    exact_chord = up(2 * A(7) * (PI / (2 * A(n))).sin())
    used_radius = A(repr(2.0 * 7.0 * math.sin((float_hi - float_lo) / 4.0) * (1.0 + 1e-9)))
    slack = lo(used_radius - centre_error - exact_chord)
    geometry_slacks.append(slack)
checks["all_exact_arcs_inside_float_disks"] = all(slack > 0 for slack in geometry_slacks)

checks["all_H7_boundary_disks_nonzero"] = all(lo(row["H_abs_lower"]) > 0 for row in cover_rows)
checks["all_stable_tail_symbols_injected"] = all(row["tail_symbol_injected"] for row in slice_rows)
checks["all_full_CL34_errors_injected"] = all(row["CL34_full_G_h_errors_injected"] for row in slice_rows)
checks["all_orbits_inside_composition_domain"] = all(A(repr(row["Rmax"])) < 1 for row in slice_rows)
checks["all_rouche_gaps_positive"] = all(lo(row["absolute_gap_lower"]) > 0 for row in rouche_rows)
checks["all_rouche_margins_above_1"] = all(lo(row["rouche_margin_lower"]) > 1 for row in rouche_rows)

worst_margin = min(lo(row["rouche_margin_lower"]) for row in rouche_rows)
smallest_gap = min(lo(row["absolute_gap_lower"]) for row in rouche_rows)
minimum_geometry_slack = min(geometry_slacks)
maximum_Rmax = max(A(repr(row["Rmax"])) for row in slice_rows)

payload = {
    "status": "INDEPENDENT_ASSEMBLY_AND_GEOMETRY_AUDIT_DISK7",
    "checks": checks,
    "arc_count": len(cover_rows),
    "certified_H_zero_count_in_open_disk": 2,
    "domain": "|u|<7",
    "worst_rouche_margin_lower": str(worst_margin),
    "smallest_absolute_gap_lower": str(smallest_gap),
    "minimum_float_geometry_slack_lower": str(minimum_geometry_slack),
    "maximum_composition_coordinate_upper": str(maximum_Rmax),
    "artifact_hashes": {name: sha256(path) for name, path in paths.items()},
    "source_hashes": {
        name: sha256(HERE / name)
        for name in (
            "h7_circle_certificate.py",
            "refine_failed_h7_arcs.py",
            "pilot_slice.py",
            "run_pilot_slices.py",
            "arcwise_rouche_certificate.py",
            "verify_disk7_certificate.py",
        )
    },
}
payload["pass"] = all(checks.values())
(HERE / "disk7_audit.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(
    f"PASS={payload['pass']} checks={sum(checks.values())}/{len(checks)} "
    f"arcs={len(cover_rows)} margin>={worst_margin} gap>={smallest_gap} "
    f"geometry_slack>={minimum_geometry_slack} Rmax<={maximum_Rmax}"
)
if not payload["pass"]:
    for name, passed in checks.items():
        if not passed:
            print("FAILED", name)
    raise SystemExit(1)
