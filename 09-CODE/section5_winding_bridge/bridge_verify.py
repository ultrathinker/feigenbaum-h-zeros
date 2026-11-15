# -*- coding: utf-8 -*-
"""bridge_verify.py -- independent verifier for bridge_certificate.json.

SEPARATE code path from bridge_certificate.py (the same independence pair as
the audited winding package): complex arithmetic on (re,im) arb tuples (no
flint.acb operator overloading in the orbit), g/h evaluated by DIRECT forward
power accumulation (not Horner), chord via the cos-identity
rho*sqrt(2-2*cos(phi)) (not 2*rho*sin(phi/2)), u_mid from cos/sin directly,
hand-written complex division for AU0/delta^m. Adapted with provenance from
article_v1/v3_work/winding/winding_verify.py (the audited verifier).

What it verifies (exit 1 on ANY drift):
  [0] all 11 sha256 pins;
  [1] the three NEW windings (Z57@8, Z60@8, Z72@7) fully recomputed via the
      tuple path: tiling, coverage, domain, denominator, winding, uniqueness,
      strictly_zero, pass -- INCLUDING max_w_upper (closing the M2 verifier
      hole found by the orchestrator audit of the winding package);
  [2] the tube-arc scan redone from disk with its own attribution logic:
      counts (total/working/NEG), worst x128_lower + file, min r_s,
      per-(disk,level) arc counts and minima vs every bridge_table row;
  [3] containment recomputed from h1pkg_certificate.json;
  [4] the bridge verdicts (per-disk bridged flags, required levels,
      all_disks_bridged, all_pass, n_disks, n_checks) recomputed from the
      re-verified components;
  [5] geometry of the new windings re-read from point14/z72 raw certs.

Multiprocessing: winding recomputations run in a process pool (<=12 workers).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from pathlib import Path

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
CERT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else (HERE / "bridge_certificate.json")

MAX_WORKERS = 3  # three winding tasks; hard cap 12 per project directive

WINDING_CERT = ROOT / "article_v1" / "v3_work" / "winding" / "winding_certificate.json"
H1PKG_CERT = ROOT / "article_v1" / "v3_work" / "h1_package" / "cert_D" / "h1pkg_certificate.json"
M8_CERT = ROOT / "path_to_8" / "point14_m8_base" / "m8_certificate.json"
CENSUS_A = ROOT / "path_to_8" / "point10_layer1_census_A" / "census_A_certificate.json"
CENSUS_B = ROOT / "path_to_8" / "point10_layer1_census_B" / "census_B_certificate.json"
Z72_CERT = ROOT / "path_to_8" / "point17_z72_geometry" / "z72_certificate.json"
FIX1_CERT = ROOT / "path_to_8" / "point3B_localize_two_roots_agent_fix1" / "localization_certificate.json"
X4_PATH = ROOT / "w35" / "x4_walk_sonnet" / "x4_common.py"
GH_PATH = ROOT / "w33" / "t5_cert_sonnet" / "w33_gh_hiprec.json"
CL34_PATH = ROOT / "w36" / "tail_codex" / "cl34_certificate.json"
ABS36_PATH = ROOT / "w36" / "audit_codex" / "absolute_margins_arb.json"

PIN_MAP = {
    "winding_certificate.json": WINDING_CERT,
    "h1pkg_certificate.json": H1PKG_CERT,
    "m8_certificate.json": M8_CERT,
    "census_A_certificate.json": CENSUS_A,
    "census_B_certificate.json": CENSUS_B,
    "z72_certificate.json": Z72_CERT,
    "localization_certificate.json": FIX1_CERT,
    "x4_common.py": X4_PATH,
    "w33_gh_hiprec.json": GH_PATH,
    "cl34_certificate.json": CL34_PATH,
    "absolute_margins_arb.json": ABS36_PATH,
}

TUBE_GROUPS = {
    "point10_layer1_census_A": ROOT / "path_to_8" / "point10_layer1_census_A",
    "point10_layer1_census_B": ROOT / "path_to_8" / "point10_layer1_census_B",
    "point14_m8_base": ROOT / "path_to_8" / "point14_m8_base",
    "point17_z72_geometry": ROOT / "path_to_8" / "point17_z72_geometry",
    "point3B_localize_two_roots_agent_fix1": ROOT / "path_to_8" / "point3B_localize_two_roots_agent_fix1",
}
TUBE_RE = re.compile(r"cert_slice_(.+?)_outerbox_tube_K100_")

errors = []


def err(msg):
    errors.append(msg)
    print("  FAIL:", msg)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def relclose(a, b, tol):
    if a is None or b is None:
        return a is None and b is None
    a, b = float(a), float(b)
    if a == b:
        return True
    return abs(a - b) <= tol * max(abs(a), abs(b))


# ================================================================ worker: tuple-path winding recompute
def recompute_winding_tuple(spec):
    """(label, centre_re, centre_im, rho_str, m) -> dict.
    Runs in a worker process: manual-tuple / power-sum code path.
    REPLICATES the generator's deterministic adaptive arc-count selection
    (start 32, double on failure, cap 2048) so the certificate's n_arcs field
    is itself verified, not trusted (kilo review, K3)."""
    label, centre_re, centre_im, rho_str, m = spec
    import flint

    flint.ctx.prec = 512
    A = flint.arb
    sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
    import x4_common as xc

    _cl34 = json.loads(CL34_PATH.read_text(encoding="utf-8"))
    EPS_G = A(_cl34["G"]["distance_and_Taylor_tail_upper"]).upper()
    EPS_H = A(_cl34["V_h_delta"]["h_error_stored_center_upper"]).upper()

    def cmul(x, y):
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def cdiv(x, y):
        a, b = x
        c, d = y
        denom = c * c + d * d
        return ((a * c + b * d) / denom, (b * c - a * d) / denom)

    def cabs_ub(x):
        return (x[0] * x[0] + x[1] * x[1]).sqrt()

    def acb_to_pair(z):
        return (A(z.real), A(z.imag))

    # affine state: (cre, cim, are, aim, r)
    def vconst(re_, im_=0):
        return (A(re_), A(im_), A(0), A(0), A(0))

    def vadd(x, y):
        return (x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3], x[4] + y[4])

    def vaddc(x, re_, im_=0):
        return (x[0] + re_, x[1] + im_, x[2], x[3], x[4])

    def vscalec(x, sre, sim=0):
        c = cmul((x[0], x[1]), (sre, sim))
        a = cmul((x[2], x[3]), (sre, sim))
        r = x[4] * cabs_ub((sre, sim))
        return (c[0], c[1], a[0], a[1], r)

    def vmul(x, y):
        xc_, yc_ = (x[0], x[1]), (y[0], y[1])
        xa, ya = (x[2], x[3]), (y[2], y[3])
        c = cmul(xc_, yc_)
        a1 = cmul(xc_, ya)
        a2 = cmul(yc_, xa)
        a = (a1[0] + a2[0], a1[1] + a2[1])
        axu = cabs_ub(xa)
        ayu = cabs_ub(ya)
        xcu = cabs_ub(xc_)
        ycu = cabs_ub(yc_)
        r = (axu * ayu + xcu * y[4] + ycu * x[4] + axu * y[4] + ayu * x[4] + x[4] * y[4])
        return (c[0], c[1], a[0], a[1], r)

    def vabs_lb(x):
        return cabs_ub((x[0], x[1])).lower() - cabs_ub((x[2], x[3])).upper() - x[4]

    def vabs_ub(x):
        return cabs_ub((x[0], x[1])).upper() + cabs_ub((x[2], x[3])).upper() + x[4]

    G_PAIRS = [acb_to_pair(c) for c in xc.tc_g]
    H_PAIRS = [acb_to_pair(c) for c in xc.tc_h]
    AU0_PAIR = acb_to_pair(xc.AU0)
    DELTA_PAIR = acb_to_pair(xc.DELTA_pt)
    INV_R_PAIR = cdiv((A(1), A(0)), (xc.r_disc, A(0)))

    def power_sum_eval(coeffs_pairs, z):
        powers = [vconst(1, 0)]
        for _ in range(1, len(coeffs_pairs)):
            powers.append(vmul(powers[-1], z))
        acc = vconst(0, 0)
        for k, (cre, cim) in enumerate(coeffs_pairs):
            acc = vadd(acc, vscalec(powers[k], cre, cim))
        return acc

    def cpow_int(x, n):
        r = x
        for _ in range(n - 1):
            r = cmul(r, x)
        return r

    def xden_v(u_mid_pair, u_rad, m_):
        delta_m = cpow_int(DELTA_PAIR, m_)
        s_factor = cdiv(AU0_PAIR, delta_m)
        u = (u_mid_pair[0], u_mid_pair[1], A(u_rad), A(0), A(0))
        s = vscalec(u, s_factor[0], s_factor[1])
        s_abs = vabs_ub(s)
        x = vconst(0, 0)
        lev = 1 << m_
        max_w = A(0)
        for _ in range(lev):
            xx = vmul(x, x)
            xx = vaddc(xx, A(-1), A(0))
            w = vscalec(xx, INV_R_PAIR[0], INV_R_PAIR[1])
            wu = vabs_ub(w)
            if not (wu < 1):
                return None, None
            if wu > max_w:
                max_w = wu
            vg = power_sum_eval(G_PAIRS, w)
            vh = power_sum_eval(H_PAIRS, w)
            vg = (vg[0], vg[1], vg[2], vg[3], vg[4] + EPS_G)
            vh = (vh[0], vh[1], vh[2], vh[3], vh[4] + EPS_H)
            x = vadd(vg, vmul(vh, s))
            x = (x[0], x[1], x[2], x[3], x[4] + EPS_G + s_abs * EPS_H)
        return x, max_w

    def arb_from_ratio_str(s):
        s = str(s)
        if "/" in s:
            n, d = s.split("/")
            return A(int(n)) / A(int(d))
        return A(s)

    TWO_PI = 2 * A.pi()
    uc = (A(centre_re), A(centre_im))
    rho = arb_from_ratio_str(rho_str)

    def u_point(t):
        # cos/sin directly, not complex exponential
        if t in (0, 1):
            th = A(0)
        else:
            th = TWO_PI * A(t.numerator) / A(t.denominator)
        return (uc[0] + rho * th.cos(), uc[1] + rho * th.sin())

    import flint as _f
    Cx = _f.acb
    SAFETY = 1.000001
    result = None
    n_arcs = 32
    while n_arcs <= 2048:
        # tiling (exact Fractions)
        total = Fraction(0)
        for k in range(n_arcs):
            total += Fraction(k + 1, n_arcs) - Fraction(k, n_arcs)
        tiling_ok = (total == 1)

        worst_cov_margin = None
        worst_den_lower = None
        max_w_seen = A(0)
        domain_ok = True
        den_ok = True
        for k in range(n_arcs):
            t1 = Fraction(k, n_arcs)
            t2 = Fraction(k + 1, n_arcs)
            tm = (t1 + t2) / 2
            # chord via cos-identity
            dt = t2 - t1
            phi = A.pi() * A(dt.numerator) / A(dt.denominator)
            chord_ub = (rho * (2 - 2 * phi.cos()).sqrt()).upper()
            u_rad = float(chord_ub) * SAFETY
            cov_margin = A(u_rad) - chord_ub
            if worst_cov_margin is None or cov_margin < worst_cov_margin:
                worst_cov_margin = cov_margin
            um = u_point(tm)
            xa, mw = xden_v(um, u_rad, m)
            if xa is None:
                domain_ok = False
                break
            if mw > max_w_seen:
                max_w_seen = mw
            den_lo = vabs_lb(xa)
            if worst_den_lower is None or den_lo < worst_den_lower:
                worst_den_lower = den_lo
            if not (den_lo > 0):
                den_ok = False
                break

        result = {
            "label": label, "m": m, "n_arcs": n_arcs,
            "tiling_ok": tiling_ok,
            "domain_ok": domain_ok, "den_ok": den_ok,
            "coverage_ok": bool(worst_cov_margin is not None and worst_cov_margin > 0),
            "cov_margin": float(worst_cov_margin.upper()) if worst_cov_margin is not None else None,
            "min_abs_denominator_lower": float(worst_den_lower.lower()) if worst_den_lower is not None else None,
            "max_w_upper": float(max_w_seen.upper()),
        }
        if not (domain_ok and den_ok):
            n_arcs *= 2
            continue

        # endpoints (tight point evaluation) + winding sum
        needed_ts = set()
        for k in range(n_arcs):
            needed_ts.add(Fraction(k, n_arcs))
            needed_ts.add(Fraction(k + 1, n_arcs))
        endpoints = {}
        endpoint_ok = True
        for t in needed_ts:
            up = u_point(t)
            xa, _ = xden_v(up, 0.0, m)
            if xa is None:
                endpoint_ok = False
                break
            re_m = A(xa[0].mid())
            im_m = A(xa[1].mid())
            e = A(xa[0].rad()) + A(xa[1].rad()) + cabs_ub((xa[2], xa[3])).upper() + xa[4]
            endpoints[t] = Cx(A(re_m, e), A(im_m, e))
        if not endpoint_ok:
            n_arcs *= 2
            continue
        total_arg = A(0)
        for k in range(n_arcs):
            t1 = Fraction(k, n_arcs)
            t2 = Fraction(k + 1, n_arcs)
            total_arg = total_arg + (endpoints[t2] / endpoints[t1]).arg()
        wind = total_arg / TWO_PI
        cand = int(round(float(wind.mid())))
        unique = ((wind - cand).contains(0)
                  and not (wind - (cand - 1)).contains(0)
                  and not (wind - (cand + 1)).contains(0))
        result.update({
            "winding_candidate": cand,
            "winding_unique": bool(unique),
            "strictly_zero": bool(unique and cand == 0),
        })
        result["pass"] = bool(tiling_ok and result["coverage_ok"] and domain_ok and den_ok
                              and unique and cand == 0)
        return result

    result = result or {"label": label, "m": m, "n_arcs": None}
    result["pass"] = False
    return result


# ================================================================ main
def main():
    t0 = time.time()
    if not CERT_PATH.exists():
        print("certificate not found:", CERT_PATH)
        return 1
    CERT = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    print("[0] sha256 pins (%d inputs)" % len(PIN_MAP))
    for name, path in PIN_MAP.items():
        pinned = CERT.get("sha256_pins", {}).get(name)
        if pinned is None:
            err("missing pin for %s" % name)
            continue
        actual = sha256(path)
        if actual != pinned:
            err("sha256 mismatch %s: cert=%s actual=%s" % (name, pinned, actual))

    wind_cert = json.loads(WINDING_CERT.read_text(encoding="utf-8"))
    h1pkg = json.loads(H1PKG_CERT.read_text(encoding="utf-8"))
    m8c = json.loads(M8_CERT.read_text(encoding="utf-8"))
    z72c = json.loads(Z72_CERT.read_text(encoding="utf-8"))
    if not wind_cert.get("all_pass_required"):
        err("winding_certificate.json no longer claims all_pass_required")

    # ---------- [1] recompute the NEW windings via the tuple path
    print("[1] tuple-path recompute of the new windings (<=%d workers)" % MAX_WORKERS)
    new_rows = CERT.get("new_windings", [])
    if len(new_rows) != 3:
        err("expected 3 new windings in certificate, got %d" % len(new_rows))
    # geometry re-read from RAW certs, never from the certificate
    raw_geom = {
        ("Z57", 8): (str(m8c["disk_results"]["Z57"]["centre_re"]),
                     str(m8c["disk_results"]["Z57"]["centre_im"]),
                     str(m8c["disk_results"]["Z57"]["rho"])),
        ("Z60", 8): (str(m8c["disk_results"]["Z60"]["centre_re"]),
                     str(m8c["disk_results"]["Z60"]["centre_im"]),
                     str(m8c["disk_results"]["Z60"]["rho"])),
        ("Z72", 7): (str(z72c["contour"]["centre_re"]),
                     str(z72c["contour"]["centre_im"]),
                     str(z72c["contour"]["rho"])),
    }
    specs = []
    for row in new_rows:
        key = (row["label"], row["m"])
        if key not in raw_geom:
            err("unexpected new winding row %s" % (key,))
            continue
        cre, cim, rho_s = raw_geom[key]
        if str(row["centre_re"]) != cre or str(row["centre_im"]) != cim \
                or Fraction(str(row["rho"])) != Fraction(rho_s):
            err("%s@m=%d geometry drift vs raw cert: cert=(%s,%s,%s) raw=(%s,%s,%s)" % (
                row["label"], row["m"], row["centre_re"], row["centre_im"], row["rho"],
                cre, cim, rho_s))
        specs.append((row["label"], cre, cim, rho_s, row["m"]))

    with ProcessPoolExecutor(max_workers=min(MAX_WORKERS, 12)) as ex:
        recomputed = list(ex.map(recompute_winding_tuple, specs))

    for row, rec in zip(new_rows, recomputed):
        lbl = "%s@m=%d" % (row["label"], row["m"])
        for fld in ("tiling_ok", "domain_ok", "winding_candidate", "winding_unique",
                    "strictly_zero", "pass"):
            crt = row.get(fld) if fld != "domain_ok" else row.get("domain_ok")
            if bool(crt) != bool(rec.get(fld)) and fld not in ("winding_candidate",):
                err("%s %s drift: cert=%s recomputed=%s" % (lbl, fld, crt, rec.get(fld)))
        if row.get("winding_candidate") != rec.get("winding_candidate"):
            err("%s winding_candidate drift: cert=%s recomputed=%s" % (
                lbl, row.get("winding_candidate"), rec.get("winding_candidate")))
        # n_arcs verified by replicating the adaptive selection (kilo K3)
        if row.get("n_arcs") != rec.get("n_arcs"):
            err("%s n_arcs drift: cert=%s adaptive-recomputed=%s" % (
                lbl, row.get("n_arcs"), rec.get("n_arcs")))
        if not relclose(row.get("min_abs_denominator_lower"),
                        rec.get("min_abs_denominator_lower"), 1e-3):
            err("%s min_abs_denominator drift: cert=%s recomputed=%s" % (
                lbl, row.get("min_abs_denominator_lower"), rec.get("min_abs_denominator_lower")))
        # closes the M2 hole: max_w recomputed and compared
        if not relclose(row.get("max_w_upper"), rec.get("max_w_upper"), 1e-3):
            err("%s max_w_upper drift: cert=%s recomputed=%s" % (
                lbl, row.get("max_w_upper"), rec.get("max_w_upper")))
        if not rec.get("strictly_zero"):
            err("%s: independent recompute did NOT confirm strictly_zero" % lbl)
        print("    %s: recomputed wind=%s strictly_zero=%s min|x|=%.4e max_w=%.4f" % (
            lbl, rec.get("winding_candidate"), rec.get("strictly_zero"),
            rec.get("min_abs_denominator_lower") or -1, rec.get("max_w_upper") or -1))

    # ---------- [2] independent tube rescan (own attribution + per-family
    #              contour-tiling completeness + per-file level evidence)
    print("[2] tube rescan (own attribution)")
    ARC_IDX_RE = re.compile(r"a(\d+)\.json$")
    n_total = n_neg = n_working = 0
    worst_x128 = None
    worst_file = None
    min_rs = None
    fams = {}          # family_id -> {disk, level, group, idx set, min, refinement}
    strays = []
    legacy = 0
    for gname, gdir in TUBE_GROUPS.items():
        for f in sorted(gdir.glob("cert_slice_*_outerbox_tube_K100_*.json")):
            mm = TUBE_RE.search(f.name)
            if not mm:
                err("unparsable tube filename %s" % f.name)
                continue
            raw = mm.group(1)
            ru = raw.upper()
            n_total += 1
            if ru.startswith("NEG"):
                n_neg += 1
                continue
            n_working += 1
            d = json.loads(f.read_text(encoding="utf-8"))
            x128 = float(d["x128_lower"])
            if not (x128 > 0):
                err("x128_lower <= 0 in %s" % f.name)
            rs = d.get("r_s", d.get("dom_budget_each", d.get("W_tail")))
            if rs is not None:
                rs = float(rs)
                min_rs = rs if min_rs is None else min(min_rs, rs)
            if worst_x128 is None or x128 < worst_x128:
                worst_x128, worst_file = x128, f.name
            # attribution (independent re-derivation of the same policy)
            key, refinement = None, False
            if gname.endswith("census_A"):
                key = (ru, 7)
            elif gname.endswith("census_B"):
                if ru == "Z72":
                    legacy += 1
                    continue
                key = (ru, 7)
            elif gname == "point14_m8_base":
                g2 = re.match(r"^(Z\d\d)_L([78])$", ru)
                key = (g2.group(1), int(g2.group(2))) if g2 else None
            elif gname == "point17_z72_geometry":
                if ru == "Z72_SHIFTED":
                    key = ("Z72", 7)
                elif ru == "Z72_SHIFTED_L8":
                    key = ("Z72", 8)
                else:
                    g2 = re.match(r"^Z72_STAGE9_L([78])$", ru)
                    if g2:
                        key, refinement = ("Z72", int(g2.group(1))), True
            elif gname.endswith("fix1"):
                key = (ru, 7) if ru in ("D_MINUS", "D_PLUS") else None
            if key is None:
                strays.append("%s (group %s)" % (raw, gname))
                continue
            # per-file level evidence (non-refinement families)
            if not refinement and ("H%d_abs_lower" % key[1]) not in d:
                err("level evidence missing: %s attributed to L%d without H%d_abs_lower" % (
                    f.name, key[1], key[1]))
            im = ARC_IDX_RE.search(f.name)
            if im is None:
                err("no arc index in %s" % f.name)
                continue
            fam_id = "%s:%s" % (gname, raw)
            fam = fams.setdefault(fam_id, {"key": key, "idx": set(), "min": None,
                                            "refinement": refinement, "group": gname})
            fam["idx"].add(int(im.group(1)))
            fam["min"] = x128 if fam["min"] is None else min(fam["min"], x128)

    # family completeness + (disk,level) -> family map
    scan = {}   # (disk, level) -> list of (fam_id, n_arcs, contiguous_full, min)
    for fam_id, fam in fams.items():
        idx = sorted(fam["idx"])
        n = len(idx)
        contig = (idx == list(range(n)))
        if fam["refinement"]:
            if contig:
                err("refinement family %s unexpectedly tiles the full contour "
                    "(0..%d) -- attribution policy needs review" % (fam_id, n - 1))
            continue
        scan.setdefault(fam["key"], []).append((fam_id, n, contig, fam["min"]))

    recon = CERT["tube_reconciliation"]
    for fld, mine in (("n_files_total_here", n_total), ("n_working_here", n_working),
                      ("n_neg_here", n_neg)):
        if recon.get(fld) != mine:
            err("tube count drift %s: cert=%s rescanned=%s" % (fld, recon.get(fld), mine))
    if not relclose(recon.get("x128_worst_here"), worst_x128, 1e-12):
        err("worst x128 drift: cert=%s rescanned=%s" % (recon.get("x128_worst_here"), worst_x128))
    cov = h1pkg["coverage"]
    if not (n_total == cov["n_tube_files_5groups"] and n_working == cov["n_working_arcs_5groups"]
            and n_neg == cov["n_neg_controls_5groups"]):
        err("rescan does not match h1pkg accounting: %d/%d/%d vs %d/%d/%d" % (
            n_total, n_working, n_neg, cov["n_tube_files_5groups"],
            cov["n_working_arcs_5groups"], cov["n_neg_controls_5groups"]))
    if CERT.get("legacy_z72_old_contour_arcs_nonblocking") != legacy:
        err("legacy Z72 arc count drift: cert=%s rescanned=%s" % (
            CERT.get("legacy_z72_old_contour_arcs_nonblocking"), legacy))
    # stray list is a REPORTED field -- recompute and compare (kilo K1)
    if sorted(set(strays)) != CERT.get("stray_tube_labels_nonblocking"):
        err("stray list drift: cert=%s rescanned=%s" % (
            CERT.get("stray_tube_labels_nonblocking"), sorted(set(strays))))
    print("    %d files, %d working, %d NEG, %d legacy-Z72, worst=%.6e" % (
        n_total, n_working, n_neg, legacy, worst_x128))

    # ---------- [3] containment recomputed from h1pkg
    print("[3] containment")
    tail = h1pkg["tail_resolution"]
    p_tail = float(tail["P_tail_m0_primary_upper"])
    tube_radius = float(tail["tube_radius"])
    cont = CERT["containment"]
    if not relclose(cont.get("P_tail_m0_primary_upper"), p_tail, 1e-15):
        err("P_tail drift: cert=%s h1pkg=%s" % (cont.get("P_tail_m0_primary_upper"), p_tail))
    if not relclose(cont.get("tube_radius"), tube_radius, 1e-15):
        err("tube_radius drift")
    if not relclose(cont.get("min_r_s_across_scanned_arcs"), min_rs, 1e-15):
        err("min r_s drift: cert=%s rescanned=%s" % (cont.get("min_r_s_across_scanned_arcs"), min_rs))
    if not (p_tail < tube_radius and (min_rs is None or p_tail < min_rs)):
        err("containment FAILS on recompute: P_tail=%s tube=%s min_rs=%s" % (p_tail, tube_radius, min_rs))
    if not (cont.get("containment_ok") and cont.get("containment_ok_vs_min_rs")):
        err("certificate containment flags are not both true")
    # containment_margin is a REPORTED field -- recompute it (fable finding 3)
    if not relclose(cont.get("containment_margin"), tube_radius - p_tail, 1e-12):
        err("containment_margin drift: cert=%s recomputed=%s" % (
            cont.get("containment_margin"), tube_radius - p_tail))

    # ---------- [4] bridge verdicts recomputed
    print("[4] bridge verdicts")
    base_windings = {}
    strictly_map = {}
    source_map = {}
    for d in wind_cert["disks"]:
        base_windings[(d["label"], d["m"])] = bool(d.get("pass")) and bool(d.get("strictly_zero"))
        strictly_map[(d["label"], d["m"])] = bool(d.get("strictly_zero"))
        source_map[(d["label"], d["m"])] = "winding_certificate.json"
    for row, rec in zip(new_rows, recomputed):
        base_windings[(row["label"], row["m"])] = bool(rec.get("pass")) and bool(rec.get("strictly_zero"))
        strictly_map[(row["label"], row["m"])] = bool(rec.get("strictly_zero"))
        source_map[(row["label"], row["m"])] = "bridge_certificate.py (new, m=%d)" % row["m"]

    expected_disks = {d["label"] for d in wind_cert["disks"]}
    required_levels = {lbl: {7} for lbl in expected_disks}
    required_levels["Z57"] = {7, 8}
    required_levels["Z60"] = {7, 8}
    required_levels["Z72"] = {7, 8}

    cert_table = {b["label"]: b for b in CERT["bridge_table"]}
    if set(cert_table.keys()) != expected_disks:
        err("bridge_table disk set mismatch")
    all_bridged_v = True
    for lbl in sorted(expected_disks):
        b = cert_table.get(lbl)
        if b is None:
            all_bridged_v = False
            continue
        if sorted(required_levels[lbl]) != b.get("required_levels"):
            err("%s required_levels drift: cert=%s expected=%s" % (
                lbl, b.get("required_levels"), sorted(required_levels[lbl])))
        bridged_lvls = set()
        for r in b["rows"]:
            lvl = r["level_m"]
            fam_list = scan.get((lbl, lvl), [])
            n_arcs_sum = sum(n for _, n, _, _ in fam_list)
            tube_min = min((mn for _, _, _, mn in fam_list), default=None)
            coverage_v = any(contig and mn > 0 for _, _, contig, mn in fam_list)
            ok = bool(base_windings.get((lbl, lvl))) and coverage_v
            if bool(r.get("bridged")) != ok:
                err("%s@L%s bridged drift: cert=%s recomputed=%s" % (lbl, lvl, r.get("bridged"), ok))
            if bool(r.get("coverage_complete")) != coverage_v:
                err("%s@L%s coverage_complete drift: cert=%s recomputed=%s" % (
                    lbl, lvl, r.get("coverage_complete"), coverage_v))
            # reported fields recomputed, not trusted (kilo K2, K4)
            if bool(r.get("winding_strictly_zero")) != strictly_map.get((lbl, lvl), False):
                err("%s@L%s winding_strictly_zero drift: cert=%s recomputed=%s" % (
                    lbl, lvl, r.get("winding_strictly_zero"), strictly_map.get((lbl, lvl))))
            if r.get("winding_source") != source_map.get((lbl, lvl)):
                err("%s@L%s winding_source drift: cert=%s expected=%s" % (
                    lbl, lvl, r.get("winding_source"), source_map.get((lbl, lvl))))
            if ok:
                bridged_lvls.add(lvl)
            if r.get("tube_n_arcs") != n_arcs_sum:
                err("%s@L%s tube_n_arcs drift: cert=%s rescanned=%s" % (
                    lbl, lvl, r.get("tube_n_arcs"), n_arcs_sum))
            if not relclose(r.get("tube_min_x128_lower"), tube_min, 1e-12):
                err("%s@L%s tube min drift: cert=%s rescanned=%s" % (
                    lbl, lvl, r.get("tube_min_x128_lower"), tube_min))
            # per-family cross-check (fable finding 3: report fields must be
            # recomputed, not trusted)
            cert_fams = {fm["family"]: fm for fm in r.get("tube_families", [])}
            mine_fams = {fid: (n, contig, mn) for fid, n, contig, mn in fam_list}
            if set(cert_fams.keys()) != set(mine_fams.keys()):
                err("%s@L%s family set drift: cert=%s rescanned=%s" % (
                    lbl, lvl, sorted(cert_fams), sorted(mine_fams)))
            else:
                for fid, (n, contig, mn) in mine_fams.items():
                    cf = cert_fams[fid]
                    if cf.get("n_arcs") != n or bool(cf.get("contiguous_full")) != contig \
                            or not relclose(cf.get("min_x128_lower"), mn, 1e-12):
                        err("%s@L%s family %s drift: cert=(%s,%s,%s) rescanned=(%s,%s,%s)" % (
                            lbl, lvl, fid, cf.get("n_arcs"), cf.get("contiguous_full"),
                            cf.get("min_x128_lower"), n, contig, mn))
        disk_ok = required_levels[lbl].issubset(bridged_lvls)
        if bool(b.get("disk_bridged")) != disk_ok:
            err("%s disk_bridged drift: cert=%s recomputed=%s" % (lbl, b.get("disk_bridged"), disk_ok))
        all_bridged_v = all_bridged_v and disk_ok

    # refinement families: certificate must list them, with matching stats
    refn = CERT.get("refinement_families_nonblocking", {})
    mine_refn = {fid: fam for fid, fam in fams.items() if fam["refinement"]}
    if set(refn.keys()) != set(mine_refn.keys()):
        err("refinement family set drift: cert=%s rescanned=%s" % (
            sorted(refn), sorted(mine_refn)))
    else:
        for fid, fam in mine_refn.items():
            if refn[fid].get("n_arcs") != len(fam["idx"]):
                err("refinement %s n_arcs drift: cert=%s rescanned=%s" % (
                    fid, refn[fid].get("n_arcs"), len(fam["idx"])))

    if bool(CERT.get("all_disks_bridged")) != all_bridged_v:
        err("all_disks_bridged drift: cert=%s recomputed=%s" % (
            CERT.get("all_disks_bridged"), all_bridged_v))
    all_pass_v = (all_bridged_v and n_total == cov["n_tube_files_5groups"]
                  and p_tail < tube_radius
                  and all(bool(r.get("pass")) for r, rr in zip(new_rows, recomputed) if r.get("required"))
                  and all(bool(rr.get("pass")) for r, rr in zip(new_rows, recomputed) if r.get("required")))
    if bool(CERT.get("all_pass")) != all_pass_v:
        err("all_pass drift: cert=%s recomputed=%s" % (CERT.get("all_pass"), all_pass_v))
    if CERT.get("n_disks") != len(expected_disks):
        err("n_disks drift: cert=%s expected=%s" % (CERT.get("n_disks"), len(expected_disks)))
    # n_checks formula: disks + all rows + working arcs + geom checks + 4
    n_rows = sum(len(b["rows"]) for b in CERT["bridge_table"])
    n_checks_v = len(expected_disks) + n_rows + n_working + len(CERT.get("geometry_checks_new_m8", [])) + 4
    if CERT.get("n_checks") != n_checks_v:
        err("n_checks drift: cert=%s recomputed=%s" % (CERT.get("n_checks"), n_checks_v))

    # ---------- verdict
    dt = time.time() - t0
    if errors:
        print("\nVERDICT: FAIL -- %d discrepancies (%.1fs)" % (len(errors), dt))
        return 1
    print("\nVERDICT: PASS -- bridge_certificate.json independently verified: "
          "3 new windings recomputed via the tuple path (incl. max_w), tube scan "
          "redone (%d working arcs, all x128_lower>0), containment and every "
          "bridge verdict recomputed (%.1fs)" % (n_working, dt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
