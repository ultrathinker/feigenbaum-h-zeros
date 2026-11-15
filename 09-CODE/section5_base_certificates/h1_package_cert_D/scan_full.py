# -*- coding: utf-8 -*-
"""SCAN-ONLY: full-archive scan of cert_slice_*_K100*.json; per-disk Rmax/x128;
locate the worst x128_lower disk. Reads only."""
import glob, json, os, re
ROOT = r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive"

# ALL K100 JSONs anywhere in the archive
allpat = os.path.join(ROOT, "**", "cert_slice_*_K100*.json")
allfiles = glob.glob(allpat, recursive=True)
print(f"FULL-ARCHIVE cert_slice_*_K100*.json count = {len(allfiles)}")

# the 25-disk tube set
GROUPS_25 = ["point10_layer1_census_A","point10_layer1_census_B","point14_m8_base",
             "point17_z72_geometry","point3B_localize_two_roots_agent_fix1"]
def is_25(p):
    return any(g in p for g in GROUPS_25) and "_outerbox_tube_K100_" in os.path.basename(p)
files25 = [p for p in allfiles if is_25(p)]
print(f"25-disk outerbox_tube_K100 subset = {len(files25)}")

# NEG controls among the 25-disk groups (label NEG_*)
neg = [p for p in files25 if re.search(r"_NEG_[A-Za-z0-9]+_outerbox_tube_K100_", os.path.basename(p))]
print(f"  of which NEG_* control arcs = {len(neg)}")
working25 = [p for p in files25 if p not in set(neg)]
print(f"  working (non-NEG) 25-disk arcs = {len(working25)}")

# x128_lower stats over ALL 25-disk arcs
def load_x128(files):
    xs = []
    for p in files:
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        v = d.get("x128_lower")
        if v is None:
            continue
        xs.append((float(v), p))
    return xs

xs_all = load_x128(files25)
xs_all.sort()
print(f"\nx128_lower over 25-disk arcs (incl NEG): n={len(xs_all)}  all>0={all(v>0 for v,_ in xs_all)}")
print(f"  min = {xs_all[0][0]:.6e}  at {os.path.basename(xs_all[0][1])}")
print(f"     full path group: {[g for g in GROUPS_25 if g in xs_all[0][1]]}")
# is the min a NEG control?
mnbase = os.path.basename(xs_all[0][1])
print(f"     is NEG? {'YES' if '_NEG_' in mnbase else 'no'}")
print(f"  10th smallest: {xs_all[9][0]:.6e}  at {os.path.basename(xs_all[9][1])}")

# Rmax over working 25-disk arcs
def load_rmax(files):
    rs = []
    for p in files:
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        v = d.get("Rmax_upper")
        if v is None:
            continue
        rs.append((float(v), p))
    return rs
rs_work = load_rmax(working25)
rs_work.sort(reverse=True)
print(f"\nRmax_upper over WORKING 25-disk arcs: n={len(rs_work)}")
print("  top 6 worst working:")
for v, p in rs_work[:6]:
    print(f"    {v:.6f}  {os.path.basename(p)}")
print(f"  max working Rmax = {rs_work[0][0]:.6f}  at {os.path.basename(rs_work[0][1])}")
# NEG worst
rs_neg = load_rmax(neg)
rs_neg.sort(reverse=True)
print(f"\nRmax_upper over NEG control arcs: n={len(rs_neg)}")
for v, p in rs_neg[:3]:
    print(f"    {v:.6f}  {os.path.basename(p)}")
print(f"  max NEG Rmax = {rs_neg[0][0] if rs_neg else 'n/a'}")
