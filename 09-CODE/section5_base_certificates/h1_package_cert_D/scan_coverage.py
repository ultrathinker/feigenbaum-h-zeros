# -*- coding: utf-8 -*-
"""SCAN-ONLY over archive: verify coverage counts, min x128_lower, total K100.
Reads only. Writes nothing to archive."""
import glob, json, os
ROOT = r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive"

GROUPS = {
    "point10_layer1_census_A": os.path.join(ROOT, "path_to_8", "point10_layer1_census_A"),
    "point10_layer1_census_B": os.path.join(ROOT, "path_to_8", "point10_layer1_census_B"),
    "point14_m8_base":         os.path.join(ROOT, "path_to_8", "point14_m8_base"),
    "point17_z72_geometry":    os.path.join(ROOT, "path_to_8", "point17_z72_geometry"),
    "point3B_localize_two_roots_agent_fix1": os.path.join(ROOT, "path_to_8", "point3B_localize_two_roots_agent_fix1"),
    # atlas / pilot / completeness -- NOT among the 25 disks:
    "point2_completeness_disk7": os.path.join(ROOT, "path_to_8", "point2_completeness_disk7"),
    "point6_sector_atlas_pilot": os.path.join(ROOT, "path_to_8", "point6_sector_atlas_pilot"),
    "point11_radial_segments":   os.path.join(ROOT, "path_to_8", "point11_radial_segments"),
}

def count_tube(groupdir):
    """Count *_outerbox_tube_K100_*.json files (the working tube certificates)."""
    if not os.path.isdir(groupdir):
        return 0, []
    pat = os.path.join(groupdir, "cert_slice_*_outerbox_tube_K100_*.json")
    files = glob.glob(pat)
    return len(files), files

def count_all_k100(groupdir):
    if not os.path.isdir(groupdir):
        return 0
    # any cert_slice_*_K100_*.json (base/outerbox_base/outerbox_tube with K100)
    pat = os.path.join(groupdir, "cert_slice_*_K100_*.json")
    return len(glob.glob(pat))

def scan_x128(files):
    npos = 0; ntot = 0; xmin = None; xminfile = None
    for p in files:
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        v = d.get("x128_lower")
        if v is None:
            continue
        ntot += 1
        v = float(v)
        if v > 0:
            npos += 1
        if xmin is None or v < xmin:
            xmin = v; xminfile = os.path.basename(p)
    return npos, ntot, xmin, xminfile

print("=== tube coverage by group (outerbox_tube_K100) ===")
total_25 = 0
all_25_files = []
for name, d in GROUPS.items():
    if name.startswith("point10") or name in ("point14_m8_base","point17_z72_geometry","point3B_localize_two_roots_agent_fix1"):
        c, files = count_tube(d)
        total_25 += c
        all_25_files += files
        print(f"  {name:48s} {c:5d}  (dir exists={os.path.isdir(d)})")
print(f"  {'TOTAL 25 disks':48s} {total_25:5d}")
print()
print("=== non-25 groups (atlas/pilot/completeness) ===")
extra = 0
for name in ("point2_completeness_disk7","point6_sector_atlas_pilot","point11_radial_segments"):
    c, _ = count_tube(GROUPS[name])
    extra += c
    print(f"  {name:48s} {c:5d}")
print(f"  {'extra total':48s} {extra:5d}")
print(f"  {'25 + extra':48s} {total_25+extra:5d}  (expected total ~2426)")
print()
print("=== x128_lower over the 25-disk tube set ===")
npos, ntot, xmin, xminfile = scan_x128(all_25_files)
print(f"  parsed={ntot}  x128_lower>0={npos}  min={xmin:.6e}  at {xminfile}")
print(f"  all positive? {npos == ntot}")
print()
print("=== total K100 JSONs (all groups, all 8 dirs) ===")
grand = 0
for name, d in GROUPS.items():
    c = count_all_k100(d)
    grand += c
    print(f"  {name:48s} all_K100={c}")
print(f"  GRAND TOTAL (8 dirs) = {grand}")
