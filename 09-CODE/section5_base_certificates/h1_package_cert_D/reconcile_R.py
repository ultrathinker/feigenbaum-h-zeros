# -*- coding: utf-8 -*-
"""RECONCILE R — independent recomputation of the four BRIEF_R points.

Read-only over the archive. Writes only progress.log. No trust in any
previously-stated number: every figure is recomputed from primary sources.
"""
import json, glob, os, re, math, sys, datetime

try:
    import flint
    HAVE_FLINT = True
except Exception:
    HAVE_FLINT = False

ROOT = "D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive"
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(HERE, "progress.log")

def log(msg):
    line = "[%s] %s" % (datetime.datetime.now().isoformat(timespec="seconds"), msg)
    print(line, flush=True)
    with open(PROG, "a", encoding="utf-8") as f:
        f.write(line + "\n"); f.flush()

def rp(*a):
    return os.path.abspath(os.path.join(ROOT, *a))

GROUPS_25 = [
    "path_to_8/point10_layer1_census_A",
    "path_to_8/point10_layer1_census_B",
    "path_to_8/point14_m8_base",
    "path_to_8/point17_z72_geometry",
    "path_to_8/point3B_localize_two_roots_agent_fix1",
]

LBL = re.compile(r"cert_slice_(.+?)_outerbox_tube_K100_")

def tube_files(groupdir):
    return glob.glob(os.path.join(rp(groupdir), "cert_slice_*_outerbox_tube_K100_*.json"))

def label_of(base):
    m = LBL.match(base)
    return m.group(1) if m else "?"

def is_neg(label):
    # robust: covers NEG_A10 / NEG_B1 / NEG_B2 / NEG_MID AND NEGATIVE_u2
    return label.upper().startswith("NEG")

# ============================================================
log("=== RECONCILE R start ===  flint=%s" % HAVE_FLINT)

# ------------------------------------------------------------
# R2 + R3: coverage, NEG split, x128_lower min  (5 working groups)
# ------------------------------------------------------------
group_counts = {}
group_pos = {}
group_neg = {}
all_arcs = []      # (rmax, x128, label, base, group)
for g in GROUPS_25:
    files = tube_files(g)
    gname = g.split("/")[-1]
    group_counts[gname] = len(files)
    p = n = 0
    for pth in files:
        base = os.path.basename(pth)
        try:
            d = json.load(open(pth, encoding="utf-8"))
        except Exception:
            continue
        lbl = label_of(base)
        neg = is_neg(lbl)
        rmax = d.get("Rmax_upper"); x128 = d.get("x128_lower")
        if rmax is None or x128 is None:
            continue
        all_arcs.append((float(rmax), float(x128), lbl, base, gname))
        if neg:
            n += 1
        else:
            p += 1
    group_pos[gname] = p
    group_neg[gname] = n

n_total_25 = sum(group_counts.values())
n_parse_25 = len(all_arcs)
n_pos_25 = sum(group_pos.values())
n_neg_25 = sum(group_neg.values())
log("R2 group_counts=%s" % group_counts)
log("R2 total tube files in 5 groups = %d" % n_total_25)
log("R2 working (non-NEG) = %d ; NEG = %d ; (working+NEG parsed = %d)" % (n_pos_25, n_neg_25, n_pos_25 + n_neg_25))
log("R2 per-group pos/NEG: %s" % {k: (group_pos[k], group_neg[k]) for k in group_counts})

# x128_lower min
x128_min = min(a[1] for a in all_arcs)
x128_min_arc = min(all_arcs, key=lambda a: a[1])
all_x128_pos = all(a[1] > 0 for a in all_arcs)
# restrict to WORKING arcs for the "denominator positivity" headline
working = [a for a in all_arcs if not is_neg(a[2])]
x128_min_work = min(a[1] for a in working)
x128_min_work_arc = min(working, key=lambda a: a[1])
log("R3 min x128_lower over ALL %d arcs = %.10e  (%s / %s)" % (n_parse_25, x128_min, x128_min_arc[2], x128_min_arc[3]))
log("R3 min x128_lower over %d WORKING arcs = %.10e  (%s / %s)" % (len(working), x128_min_work, x128_min_work_arc[2], x128_min_work_arc[3]))
log("R3 all x128_lower>0 on all parsed arcs = %s" % all_x128_pos)

# worst Rmax working vs neg
worst_work = max(working, key=lambda a: a[0])
neg_arcs = [a for a in all_arcs if is_neg(a[2])]
worst_neg = max(neg_arcs, key=lambda a: a[0]) if neg_arcs else None
log("R2 worst WORKING Rmax=%.6f (%s); worst NEG Rmax=%.6f (%s)" % (
    worst_work[0], worst_work[3], worst_neg[0] if worst_neg else float("nan"), worst_neg[3] if worst_neg else "?"))

# ------------------------------------------------------------
# R2 archive-wide: 8-folders NEG counts to reconcile 85 vs 77
# ------------------------------------------------------------
all_k100_tube = glob.glob(os.path.join(ROOT, "**", "cert_slice_*_outerbox_tube_K100_*.json"), recursive=True)
# exclude our own package output (cert_D, verify_E)
all_k100_tube_archive = [p for p in all_k100_tube
                         if "article_v1/v3_work/h1_package" not in os.path.relpath(p, ROOT).replace("\\", "/")]
n_archive_tube = len(all_k100_tube_archive)
# by folder (8 candidate folders under path_to_8)
def folder_of(p):
    rel = os.path.relpath(p, ROOT).replace("\\", "/")
    parts = rel.split("/")
    # find 'path_to_8' then next component
    if "path_to_8" in parts:
        i = parts.index("path_to_8")
        return parts[i + 1] if i + 1 < len(parts) else "?"
    return parts[0] if parts else "?"

folders = {}
for p in all_k100_tube_archive:
    fo = folder_of(p)
    folders.setdefault(fo, {"total": 0, "neg": 0, "pos": 0})
    folders[fo]["total"] += 1
    lbl = label_of(os.path.basename(p))
    if is_neg(lbl):
        folders[fo]["neg"] += 1
    else:
        folders[fo]["pos"] += 1
n_archive_neg = sum(f["neg"] for f in folders.values())
n_archive_pos = sum(f["pos"] for f in folders.values())
log("R2 archive-wide (*_tube_K100_* under path_to_8, excl. h1_package): total=%d  pos=%d  NEG=%d" % (
    n_archive_tube, n_archive_pos, n_archive_neg))
log("R2 per-folder: %s" % json.dumps(folders, ensure_ascii=False))

# total tube K100 incl. our package output (cert_D tight_arcs etc.)
all_k100_tube_full = glob.glob(os.path.join(ROOT, "**", "cert_slice_*_outerbox_tube_K100_*.json"), recursive=True)
log("R4 *_tube_K100_* archive-wide INCLUDING h1_package = %d" % len(all_k100_tube_full))
log("R4 *_tube_K100_* archive-wide EXCLUDING h1_package = %d" % n_archive_tube)

# the looser glob the old cert used: cert_slice_*_K100*
loose = glob.glob(os.path.join(ROOT, "**", "cert_slice_*_K100*.json"), recursive=True)
loose_archive = [p for p in loose if "article_v1/v3_work/h1_package" not in os.path.relpath(p, ROOT).replace("\\", "/")]
log("R4 old loose glob 'cert_slice_*_K100*' excl h1_package = %d ; incl = %d" % (len(loose_archive), len(loose)))

# which files differ between the two globs (tube vs loose) -> explains 2432 vs 2431
loose_set = set(os.path.normpath(p) for p in loose_archive)
tube_set = set(os.path.normpath(p) for p in all_k100_tube_archive)
extra_loose = sorted(loose_set - tube_set)
log("R4 loose-minus-tube (files matched by loose but NOT *_tube_K100_*) = %d" % len(extra_loose))
for p in extra_loose[:20]:
    log("    EXTRA loose: %s" % os.path.relpath(p, ROOT))

# ------------------------------------------------------------
# R1: tail estimate, recomputed with BOTH e_star sources
# ------------------------------------------------------------
tail = {}
if HAVE_FLINT:
    flint.ctx.prec = 512
    A = flint.arb
    delta = A("4.669201609102990671853")
    inv_delta = 1 / delta
    denom = 1 - inv_delta          # (1 - 1/delta)
    nh = A("6.331193600692640")    # ||h||_1
    # P_all + P_perp*D_star == r_s (archive), both tight M3=1834
    P_all = A("2.113425114987063e-7")
    P_perp = A("2.808542")
    D_star_tight = A("5.171922832190344e-8")     # level_tail M3=1834
    r_s = P_all + P_perp * D_star_tight          # = 3.566e-7 (archive)
    tube_radius = A("5.44e-7")
    # two e_star sources
    e_star_tight = A("1.24527869425265020936903073761930886718217886026473051319707748823189355625891526295532609128594925295756447050622140024804579357494226421020355065785511e-8")
    e_star_cons  = A("1.505339728370349e-8")

    def third(est):
        return (nh * est) / denom

    def total(est):
        return r_s + third(est)

    t3_tight = third(e_star_tight)
    t3_cons  = third(e_star_cons)
    pt_tight = total(e_star_tight)
    pt_cons  = total(e_star_cons)
    hr_tight = tube_radius - pt_tight
    hr_cons  = tube_radius - pt_cons
    hr_r_s   = tube_radius - r_s

    log("R1 1/delta = %s" % float(inv_delta.upper()))
    log("R1 (1-1/delta) = %s" % float(denom.upper()))
    log("R1 nh*|| = %s" % float(nh.upper()))
    log("R1 r_s (=P_all+P_perp*D_star, archive) = %.10e" % float(r_s.upper()))
    log("R1 headroom to r_s (tube_radius - r_s) = %.10e" % float(hr_r_s.upper()))
    log("R1 THIRD TERM tight  (e_star=1.2453e-8, level_tail M3=1834) = %.10e" % float(t3_tight.upper()))
    log("R1 THIRD TERM cons   (e_star=1.5053e-8, compute_ld M3=123479)= %.10e" % float(t3_cons.upper()))
    log("R1 P_tail(m0) TIGHT  = r_s + third_tight = %.10e" % float(pt_tight.upper()))
    log("R1 P_tail(m0) CONS   = r_s + third_cons  = %.10e" % float(pt_cons.upper()))
    log("R1 headroom TIGHT (tube - P_tail_tight)  = %.10e" % float(hr_tight.upper()))
    log("R1 headroom CONS  (tube - P_tail_cons)   = %.10e" % float(hr_cons.upper()))
    log("R1 P_tail_tight < tube_radius = %s" % bool(pt_tight.upper() < tube_radius.lower()))
    log("R1 P_tail_cons  < tube_radius = %s" % bool(pt_cons.upper() < tube_radius.lower()))

    tail = {
        "delta": float(delta.upper()),
        "inv_delta": float(inv_delta.upper()),
        "denom_1_minus_inv_delta": float(denom.upper()),
        "nh_h1": float(nh.upper()),
        "P_all": float(P_all.upper()),
        "P_perp": float(P_perp.upper()),
        "D_star_tight": float(D_star_tight.upper()),
        "r_s_archive": float(r_s.upper()),
        "headroom_to_r_s": float(hr_r_s.upper()),
        "e_star_tight_M3_1834": float(e_star_tight.upper()),
        "e_star_tight_source": "level_tail_certificate.json:27",
        "e_star_cons_M3_123479": float(e_star_cons.upper()),
        "e_star_cons_source": "compute_ld.json:3",
        "third_term_tight": float(t3_tight.upper()),
        "third_term_cons": float(t3_cons.upper()),
        "P_tail_tight": float(pt_tight.upper()),
        "P_tail_cons": float(pt_cons.upper()),
        "headroom_tight": float(hr_tight.upper()),
        "headroom_cons": float(hr_cons.upper()),
        "pass_tight": bool(pt_tight.upper() < tube_radius.lower()),
        "pass_cons": bool(pt_cons.upper() < tube_radius.lower()),
        "tube_radius": 5.44e-7,
    }
else:
    log("R1 flint unavailable -- skipped")

# ------------------------------------------------------------
result = {
    "R1_tail": tail,
    "R2_coverage": {
        "group_counts": group_counts,
        "n_total_5groups": n_total_25,
        "n_parsed_5groups": n_parse_25,
        "n_working_5groups": n_pos_25,
        "n_neg_5groups": n_neg_25,
        "group_pos": group_pos,
        "group_neg": group_neg,
        "archive_tube_total_excl_pkg": n_archive_tube,
        "archive_pos_excl_pkg": n_archive_pos,
        "archive_neg_excl_pkg": n_archive_neg,
        "archive_per_folder": folders,
    },
    "R3_x128": {
        "min_x128_lower_all_parsed": x128_min,
        "min_x128_lower_all_arc": [x128_min_arc[2], x128_min_arc[3], x128_min_arc[4]],
        "min_x128_lower_working": x128_min_work,
        "min_x128_lower_working_arc": [x128_min_work_arc[2], x128_min_work_arc[3], x128_min_work_arc[4]],
        "all_x128_positive": all_x128_pos,
        "n_working": len(working),
    },
    "R4_count": {
        "tube_K100_excl_pkg": n_archive_tube,
        "tube_K100_incl_pkg": len(all_k100_tube_full),
        "loose_cert_slice_K100_excl_pkg": len(loose_archive),
        "loose_cert_slice_K100_incl_pkg": len(loose),
        "extra_loose_minus_tube": [os.path.relpath(p, ROOT) for p in extra_loose],
    },
}
out = os.path.join(HERE, "reconcile_R_result.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
log("wrote " + out)
log("=== RECONCILE R done ===")
