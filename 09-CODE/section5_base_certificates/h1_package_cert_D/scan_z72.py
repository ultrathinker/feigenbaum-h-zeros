# -*- coding: utf-8 -*-
"""SCAN-ONLY: read archive tube JSONs for Z72 in census_B and report Rmax_upper.
Reads only; writes nothing to archive. Output: stdout."""
import json, glob, os
ROOT = r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive"
pat = os.path.join(ROOT, "path_to_8/point10_layer1_census_B", "cert_slice_Z72_outerbox_tube_K100_P732a*.json")
rows = []
for p in sorted(glob.glob(pat)):
    arc = int(os.path.basename(p).split("a")[-1].split(".")[0])
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        rows.append((arc, None, None, None, os.path.basename(p), f"ERR {e}"))
        continue
    rows.append((arc, d.get("Rmax_upper"), d.get("x128_lower"), d.get("N_s_tube_upper"), os.path.basename(p), ""))
rows.sort(key=lambda r: (r[0] if r[1] is None else -r[1]))
print(f"{'arc':>4} {'Rmax_upper':>12} {'x128_lower':>14} {'N_s_tube':>14}  file  err")
n_above = 0
for arc, rmax, x128, ns, fn, err in rows:
    flag = ""
    if rmax is not None and rmax > 0.5:
        n_above += 1
        flag = "  <== >0.5"
    print(f"{arc:>4} {str(rmax):>12} {str(x128):>14} {str(ns):>14}  {fn}{flag}  {err}")
print(f"\nTotal Z72 tube arcs: {len(rows)}; arcs with Rmax_upper>0.5: {n_above}")
