# -*- coding: utf-8 -*-
"""Replace only the failed Rouché arcs by four rigorous H7 subarcs."""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("disk7_h7_kernel", HERE / "h7_circle_certificate.py")
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)

h7 = json.loads((HERE / "h7_circle_certificate.json").read_text(encoding="utf-8"))
rouche = json.loads((HERE / "arcwise_rouche_certificate.json").read_text(encoding="utf-8"))
failed = {(row["t1"], row["t2"]) for row in rouche["rows"] if not row["pass"]}


def exact_subarc(t1: Fraction, t2: Fraction):
    dt = t2 - t1
    tm = (t1 + t2) / 2
    theta = kernel.TWO_PI * kernel.A(tm.numerator) / kernel.A(tm.denominator)
    chord = kernel.up(
        2 * kernel.A("7.0") * (
            kernel.PI * kernel.A(dt.numerator) / (2 * kernel.A(dt.denominator))
        ).sin()
    )
    u_mid = kernel.C(kernel.A("7.0")) * (kernel.I * kernel.C(theta)).exp()
    value, diagnostics = kernel.H7_enclosure(u_mid, chord)
    if value is None:
        raise RuntimeError(f"H7 enclosure failed on [{t1},{t2}]: {diagnostics}")
    metrics = kernel.enclosure_metrics(value)
    passed = bool(kernel.lo(metrics["lower_abs"]) > 0 and kernel.up(metrics["ratio"]) < 1)
    return {
        "t1": str(t1),
        "t2": str(t2),
        "pass": passed,
        "H_abs_lower": str(kernel.lo(metrics["lower_abs"])),
        "disk_ratio_upper": str(kernel.up(metrics["ratio"])),
        "max_w_upper": diagnostics["max_w_upper"],
    }


rows = []
replaced = 0
for row in h7["main"]["arcs"]:
    key = (row["t1"], row["t2"])
    if key not in failed:
        rows.append(row)
        continue
    left, right = Fraction(row["t1"]), Fraction(row["t2"])
    step = (right - left) / 4
    for part in range(4):
        rows.append(exact_subarc(left + part * step, left + (part + 1) * step))
    replaced += 1

rows.sort(key=lambda row: Fraction(row["t1"]))
tiles = bool(rows and Fraction(rows[0]["t1"]) == 0 and Fraction(rows[-1]["t2"]) == 1)
tiles &= all(Fraction(a["t2"]) == Fraction(b["t1"]) for a, b in zip(rows, rows[1:]))
payload = {
    "status": "TARGETED_FOUR_WAY_REFINEMENT_OF_FAILED_ROUCHE_ARCS",
    "radius": "7.0",
    "original_arc_count": len(h7["main"]["arcs"]),
    "failed_arcs_replaced": replaced,
    "refined_arc_count": len(rows),
    "tiles_full_circle_exactly": tiles,
    "all_H7_boundary_enclosures_pass": all(row["pass"] for row in rows),
    "arcs": rows,
}
payload["pass"] = (
    replaced == len(failed) == 6
    and payload["tiles_full_circle_exactly"]
    and payload["all_H7_boundary_enclosures_pass"]
)
(HERE / "h7_refined_cover.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(
    f"PASS={payload['pass']} replaced={replaced} arcs={len(rows)} "
    f"minH7={min(float(kernel.A(row['H_abs_lower']).lower()) for row in rows):.12g}"
)
if not payload["pass"]:
    raise SystemExit(1)
