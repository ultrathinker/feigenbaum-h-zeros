# -*- coding: utf-8 -*-
"""bridge_certificate.py -- BRIDGE certificate closing kit item §5.3(v)/§8(5):
"no zeros of the denominator x_{2^m} INSIDE any of the 25 disks, for the LIMIT
slice" -- assembled STRICTLY from three certified components plus one new
computation, with every input sha256-pinned.

CONTEXT (14.08.2026, kit D:/Исследования/И-1 — Нули функции H/Исследование-1, oid:bridge14)
----------------------------------------------------------
The kit's §5.3(v) honestly stated: "обмотка знаменателя вычислена численно, а
не интервальным сертификатом". In fact the archive ALREADY contains a strict
interval winding certificate (article_v1/v3_work/winding/, wave v3, 13.08,
verified + tamper-tested): wind(x_{2^m}, Gamma)=0 for the BASE slice on all
25 contours. What was missing to upgrade §5.3(v):

  (1) LEVEL MATCH: the winding package computed Z57/Z60 at m=7 only, while
      point14_m8_base (the closing certificates for those disks) works at
      BOTH L7 and L8. This program computes the missing m=8 windings for
      Z57/Z60 (same audited machine, orbit length 2^8=256).
  (2) THE BRIDGE from the BASE slice to the LIMIT slice: winding is certified
      for x_{2^m}(u; base(u)); the article needs it for x_{2^m}(u; slice_inf(u)).
      Bridge lemma (elementary, no new computation):
        (a) x_{2^m}(u; f) != 0 for all u on the contour and ALL f in the tube
            ball of radius r_s = 5.44e-7 around the base slice -- this is the
            already-certified fact x128_lower > 0 on every working tube arc
            (h1pkg_certificate.json: 1465 arcs, min 1.1186e-3);
        (b) slice_inf(u) lies in that ball: ||slice_inf - base||_1 <= P_tail
            = 4.5693e-7 < 5.44e-7 (h1pkg tail_resolution, primary variant);
        (c) the ball is CONVEX, so f_lambda(u) = base(u) + lambda*(slice_inf(u)
            - base(u)) stays in the ball for all lambda in [0,1];
        (d) hence lambda -> wind(x_{2^m}(.; f_lambda)) is defined (never 0 on
            the contour by (a)+(c)) and continuous, therefore CONSTANT;
        (e) wind at lambda=0 is the certified 0  =>  wind at lambda=1 is 0
            =>  by the argument principle (x_{2^m}(.; slice_inf) is holomorphic
            inside the disk -- max-principle induction, article line 191) the
            denominator has NO zeros inside the disk.  QED
      This program does the MACHINE part of the bridge: it verifies that for
      every one of the 25 disks the three components exist, are sha256-pinned,
      cover the SAME contour (same centre/rho), at a MATCHING orbit level m,
      and that the containment inequality P_tail < r_s holds with margin.

WHAT THIS PROGRAM DOES NOT DO (honest scope)
--------------------------------------------
- It does not re-verify the interior holomorphy induction (article §5.3(v),
  max principle) -- that is prose mathematics already in the article.
- It does not re-verify the tube arcs' own internals (domain checks, tail
  handling) -- those are the accepted core of the H1 package (h1pkg, item D,
  verified by an independent verifier E + tamper battery F).
- It does not re-verify the winding package internals for the 25 disks already
  covered -- that package has its own independent verifier (winding_verify.py,
  PASS) and two tamper batteries (8/8 and 6/7 caught).  This program re-reads
  its RESULTS under a sha256 pin.
- The stray file cert_slice_ST_outerbox_tube_K100_P732a0.json in point14 (label
  "ST", 1 arc) is counted among the 1465 working arcs by h1pkg; it belongs to
  no disk of the 25 and is reported here as a stray (nonblocking, its
  x128_lower is checked > 0 like all others).

INPUTS (READ-ONLY, all sha256-pinned in the output JSON)
--------------------------------------------------------
- article_v1/v3_work/winding/winding_certificate.json      (base windings, 25 disks)
- article_v1/v3_work/h1_package/cert_D/h1pkg_certificate.json (tube coverage + P_tail)
- path_to_8/point14_m8_base/m8_certificate.json             (Z57/Z60 geometry, m=8)
- path_to_8/point10_layer1_census_A|B/census_*_certificate.json (geometry cross-check)
- path_to_8/point17_z72_geometry/z72_certificate.json       (Z72 geometry)
- path_to_8/point3B_localize_two_roots_agent_fix1/localization_certificate.json
- w35/x4_walk_sonnet/x4_common.py, w33/t5_cert_sonnet/w33_gh_hiprec.json,
  w36/tail_codex/cl34_certificate.json, w36/audit_codex/absolute_margins_arb.json
  (frozen g,h series + CL-34 error radii -- same inputs as the winding package)
- all cert_slice_*_outerbox_tube_K100_*.json files of the 5 groups (scanned:
  x128_lower > 0 re-read from every file; counts reconciled against h1pkg)

NEW COMPUTATION: wind(x_{2^8}, Gamma) for Z57 and Z60 (orbit length 256),
same "light single-symbol AF" machine as winding_certificate.py (copied
verbatim below with provenance comments; that machine is itself the audited
census_A convention).

OUTPUT: bridge_certificate.json (this folder only).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

import flint

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "bridge_certificate.json"

flint.ctx.prec = 512
A = flint.arb
C = flint.acb
TWO_PI = 2 * A.pi()

sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
import x4_common as xc  # noqa: E402  (READ-ONLY frozen certified input)

G = xc.tc_g
H = xc.tc_h
AU0 = xc.AU0
DELTA = xc.DELTA_pt
R_DISC = xc.r_disc
M = xc.M
if M != 100:
    raise RuntimeError("expected M=100, got %d" % M)

# ---------------------------------------------------------------- pinned paths
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

TUBE_GROUPS = {
    "point10_layer1_census_A": ROOT / "path_to_8" / "point10_layer1_census_A",
    "point10_layer1_census_B": ROOT / "path_to_8" / "point10_layer1_census_B",
    "point14_m8_base": ROOT / "path_to_8" / "point14_m8_base",
    "point17_z72_geometry": ROOT / "path_to_8" / "point17_z72_geometry",
    "point3B_localize_two_roots_agent_fix1": ROOT / "path_to_8" / "point3B_localize_two_roots_agent_fix1",
}
TUBE_RE = re.compile(r"cert_slice_(.+?)_outerbox_tube_K100_")

N_START = 32
N_CAP = 2048
SAFETY_FACTOR = A("1.000001")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def ub(x) -> float:
    if hasattr(x, "upper"):
        x = x.upper()
    return float(x)


def lb(x) -> float:
    if hasattr(x, "lower"):
        x = x.lower()
    return float(x)


def arb_from_ratio_str(s):
    s = str(s)
    if "/" in s:
        n, d = s.split("/")
        return A(int(n)) / A(int(d))
    return A(s)


# ---------------------------------------------------------------- CL-34 error radii (census_A convention)
_cl34 = json.loads(CL34_PATH.read_text(encoding="utf-8"))
EPS_G = A(_cl34["G"]["distance_and_Taylor_tail_upper"]).upper()
EPS_H = A(_cl34["V_h_delta"]["h_error_stored_center_upper"]).upper()

# ================================================================ light single-symbol AF
# (copied verbatim from article_v1/v3_work/winding/winding_certificate.py --
#  the audited machine; provenance: census_A_certificate.py H7_light convention)


class LAff:
    __slots__ = ("c", "a", "r")

    def __init__(self, c, a=C(0), r=A(0)):
        self.c = C(c)
        self.a = C(a)
        self.r = A(r)


def la_const(c):
    return LAff(c)


def la_add(x, y):
    return LAff(x.c + y.c, x.a + y.a, x.r + y.r)


def la_addc(x, c):
    return LAff(x.c + C(c), x.a, x.r)


def la_sc(x, c):
    c = C(c)
    return LAff(x.c * c, x.a * c, x.r * c.abs_upper())


def la_mul(x, y):
    ax, ay = x.a.abs_upper(), y.a.abs_upper()
    return LAff(
        x.c * y.c,
        x.c * y.a + y.c * x.a,
        ax * ay + x.c.abs_upper() * y.r + y.c.abs_upper() * x.r + ax * y.r + ay * x.r + x.r * y.r,
    )


def la_horner(coeffs, z):
    v = la_const(C(0))
    for c in reversed(coeffs):
        v = la_addc(la_mul(v, z), c)
    return v


def la_abs_ub(x):
    return x.c.abs_upper() + x.a.abs_upper() + x.r


def la_abs_lb(x):
    return x.c.abs_lower() - x.a.abs_upper() - x.r


INV_R = C(1) / C(R_DISC)


def xden_af(u_mid, u_rad, m):
    """Affine enclosure of x_{2^m}(u) for u over disk(u_mid,u_rad) -- the
    denominator-only orbit (loop stops at n=2^m)."""
    s_factor = C(AU0) / (C(DELTA) ** m)
    u = LAff(C(u_mid), C(A(u_rad)))
    s = la_sc(u, s_factor)
    s_abs = la_abs_ub(s)
    x = la_const(C(0))
    lev = 1 << m
    max_w = A(0)
    for n in range(lev):
        w = la_sc(la_addc(la_mul(x, x), -1), INV_R)
        wu = la_abs_ub(w)
        if not (wu < 1):
            return None, {"fail": "composition", "step": n, "w_upper": str(wu)}
        if wu > max_w:
            max_w = wu
        vg = la_horner(G, w)
        vh = la_horner(H, w)
        vg.r = vg.r + EPS_G
        vh.r = vh.r + EPS_H
        x = la_add(vg, la_mul(vh, s))
        x.r = x.r + EPS_G + s_abs * EPS_H
    return x, {"max_w": max_w}


def check_tiling(n_arcs):
    total_width = Fraction(0)
    for k in range(n_arcs):
        total_width += Fraction(k + 1, n_arcs) - Fraction(k, n_arcs)
    ok = (total_width == 1)
    return ok, "sum of %d arc widths = %s (must be 1)" % (n_arcs, total_width)


def arc_coverage_margin(rho, t1, t2, u_rad):
    dt = t2 - t1
    half_span = A.pi() * A(dt.numerator) / A(dt.denominator) / 2
    chord_ub = (2 * rho * half_span.sin()).upper()
    margin = u_rad - chord_ub
    return margin, chord_ub


def run_disk_winding(label, centre_re, centre_im, rho_str, m):
    """Identical algorithm to winding_certificate.py:run_disk (same PASS rule)."""
    t0 = time.time()
    uc = C(A(centre_re), A(centre_im))
    rho = arb_from_ratio_str(rho_str)

    n_arcs = N_START
    fail_reason = None
    while n_arcs <= N_CAP:
        ok_t, tiling_detail = check_tiling(n_arcs)
        if not ok_t:
            fail_reason = "tiling: " + tiling_detail
            break

        per_arc = []
        worst_cov_margin = None
        worst_den_lower = None
        max_w_seen = A(0)
        domain_ok = True
        den_ok = True

        for k in range(n_arcs):
            t1 = Fraction(k, n_arcs)
            t2 = Fraction(k + 1, n_arcs)
            tm = (t1 + t2) / 2
            theta = TWO_PI * A(tm.numerator) / A(tm.denominator)
            u_mid = uc + C(rho) * (C(0, 1) * C(theta)).exp()

            _, chord_ub = arc_coverage_margin(rho, t1, t2, 0.0)
            u_rad = float(chord_ub) * float(SAFETY_FACTOR)
            cov_margin2, _ = arc_coverage_margin(rho, t1, t2, A(u_rad))
            if worst_cov_margin is None or cov_margin2 < worst_cov_margin:
                worst_cov_margin = cov_margin2

            xa, diag = xden_af(u_mid, u_rad, m)
            if xa is None:
                domain_ok = False
                fail_reason = "arc %d/%d domain: %s" % (k, n_arcs, diag)
                break
            max_w_seen = max(max_w_seen, diag["max_w"])
            den_lo = la_abs_lb(xa)
            if worst_den_lower is None or den_lo < worst_den_lower:
                worst_den_lower = den_lo
            if not (den_lo > 0):
                den_ok = False
                fail_reason = "arc %d/%d denominator contains 0: lower=%s" % (k, n_arcs, den_lo)
                break
            per_arc.append((t1, t2))

        if not (domain_ok and den_ok):
            n_arcs *= 2
            continue

        needed_ts = set()
        for t1, t2 in per_arc:
            needed_ts.add(t1)
            needed_ts.add(t2)
        endpoints = {}
        endpoint_ok = True
        for t in needed_ts:
            theta = A(0) if t in (0, 1) else TWO_PI * A(t.numerator) / A(t.denominator)
            u_pt = uc + C(rho) * (C(0, 1) * C(theta)).exp()
            xa, diag = xden_af(u_pt, 0.0, m)
            if xa is None:
                endpoint_ok = False
                fail_reason = "endpoint t=%s domain: %s" % (t, diag)
                break
            re_m = A(xa.c.real.mid())
            im_m = A(xa.c.imag.mid())
            err = A(xa.c.real.rad()) + A(xa.c.imag.rad()) + xa.a.abs_upper() + xa.r
            endpoints[t] = C(A(re_m, err), A(im_m, err))

        if not endpoint_ok:
            n_arcs *= 2
            continue

        total = A(0)
        for t1, t2 in per_arc:
            total = total + (endpoints[t2] / endpoints[t1]).arg()
        wind = total / TWO_PI
        cand = int(round(float(wind.mid())))
        strictly_this = (
            (wind - cand).contains(0)
            and not (wind - (cand - 1)).contains(0)
            and not (wind - (cand + 1)).contains(0)
        )

        rec = {
            "label": label, "m": m,
            "centre_re": centre_re, "centre_im": centre_im, "rho": rho_str,
            "n_arcs": n_arcs,
            "tiling_ok": ok_t,
            "arc_disk_coverage_ok": bool(worst_cov_margin > 0),
            "arc_disk_coverage_worst_margin": ub(worst_cov_margin),
            "domain_ok": True,
            "max_w_upper": ub(max_w_seen),
            "denominator_nonzero_on_contour": bool(worst_den_lower > 0),
            "min_abs_denominator_lower": lb(worst_den_lower),
            "winding_ball": str(wind),
            "winding_candidate": cand,
            "winding_unique": bool(strictly_this),
            "strictly_zero": bool(strictly_this and cand == 0),
            "elapsed_s": round(time.time() - t0, 2),
        }
        rec["pass"] = bool(
            rec["tiling_ok"] and rec["arc_disk_coverage_ok"] and rec["domain_ok"]
            and rec["denominator_nonzero_on_contour"] and rec["winding_unique"]
            and rec["strictly_zero"]
        )
        log("NEW winding %s m=%d N=%d: wind=%s cand=%d strictly_zero=%s min|x|>=%.4e PASS=%s (%.1fs)" % (
            label, m, n_arcs, rec["winding_ball"][:30], cand, rec["strictly_zero"],
            rec["min_abs_denominator_lower"], rec["pass"], rec["elapsed_s"]))
        return rec

    return {"label": label, "m": m, "centre_re": centre_re, "centre_im": centre_im,
            "rho": rho_str, "pass": False, "fail_reason": fail_reason,
            "elapsed_s": round(time.time() - t0, 2)}


# ================================================================ main assembly
def main():
    t0 = time.time()
    log("=== bridge_certificate.py: base->limit denominator bridge over 25 disks ===")

    # ---------- [1] pinned component certificates
    pins = {
        "winding_certificate.json": sha256(WINDING_CERT),
        "h1pkg_certificate.json": sha256(H1PKG_CERT),
        "m8_certificate.json": sha256(M8_CERT),
        "census_A_certificate.json": sha256(CENSUS_A),
        "census_B_certificate.json": sha256(CENSUS_B),
        "z72_certificate.json": sha256(Z72_CERT),
        "localization_certificate.json": sha256(FIX1_CERT),
        "x4_common.py": sha256(X4_PATH),
        "w33_gh_hiprec.json": sha256(GH_PATH),
        "cl34_certificate.json": sha256(CL34_PATH),
        "absolute_margins_arb.json": sha256(ABS36_PATH),
    }

    wind_cert = json.loads(WINDING_CERT.read_text(encoding="utf-8"))
    h1pkg = json.loads(H1PKG_CERT.read_text(encoding="utf-8"))
    m8c = json.loads(M8_CERT.read_text(encoding="utf-8"))

    if not wind_cert.get("all_pass_required"):
        raise RuntimeError("winding_certificate.json does not claim all_pass_required")

    # base winding results, keyed (label, m)
    base_windings = {}
    for d in wind_cert["disks"]:
        base_windings[(d["label"], d["m"])] = {
            "strictly_zero": bool(d.get("strictly_zero")),
            "pass": bool(d.get("pass")),
            "centre_re": str(d["centre_re"]), "centre_im": str(d["centre_im"]),
            "rho": str(d["rho"]), "source": "winding_certificate.json",
            "min_abs_denominator_lower": d.get("min_abs_denominator_lower"),
        }
    log("winding package: %d disk results loaded, all_pass_required=%s" % (
        len(base_windings), wind_cert["all_pass_required"]))

    # ---------- [2] NEW windings: Z57, Z60 at m=8 (geometry from point14);
    #              Z72 at m=7 on the SHIFTED contour (optional, closes the
    #              bridge at both levels for every reading of the base level)
    z72c = json.loads(Z72_CERT.read_text(encoding="utf-8"))
    new_windings = []
    new_specs = [
        ("Z57", str(m8c["disk_results"]["Z57"]["centre_re"]),
         str(m8c["disk_results"]["Z57"]["centre_im"]),
         str(m8c["disk_results"]["Z57"]["rho"]), 8, True),
        ("Z60", str(m8c["disk_results"]["Z60"]["centre_re"]),
         str(m8c["disk_results"]["Z60"]["centre_im"]),
         str(m8c["disk_results"]["Z60"]["rho"]), 8, True),
        # Z72@7 is REQUIRED: required_levels["Z72"] includes 7 (load-bearing
        # holomorphy level), so this winding gates all_disks_bridged; the flag
        # was misleadingly False in an earlier revision (kilo review, H2)
        ("Z72", str(z72c["contour"]["centre_re"]), str(z72c["contour"]["centre_im"]),
         str(z72c["contour"]["rho"]), 7, True),
    ]
    for lbl, cre, cim, rho_s, mm_lvl, required_new in new_specs:
        rec = run_disk_winding(lbl, cre, cim, rho_s, m=mm_lvl)
        rec["required"] = required_new
        new_windings.append(rec)
        if rec.get("pass"):
            base_windings[(lbl, mm_lvl)] = {
                "strictly_zero": bool(rec.get("strictly_zero")),
                "pass": True,
                "centre_re": rec["centre_re"], "centre_im": rec["centre_im"],
                "rho": rec["rho"], "source": "bridge_certificate.py (new, m=%d)" % mm_lvl,
                "min_abs_denominator_lower": rec.get("min_abs_denominator_lower"),
            }

    # ---------- [3] tube arc scan: x128_lower > 0 on every working K100 arc,
    #              PLUS per-family contour-tiling completeness (arc indices
    #              must form a contiguous 0..K-1 set -- a family that covers
    #              only part of the contour must never count as coverage;
    #              this check was added after the fable review found the
    #              stage9 families cover only a subset of the Z72 contour).
    ARC_IDX_RE = re.compile(r"a(\d+)\.json$")
    families = {}      # family_id -> {disk, level, group, indices, min_x128}
    tube_scan = {}     # (disk, level) -> {"families": [family_id, ...]}
    refinement_families = []  # partial-by-design subdivision families (nonblocking)
    stray_labels = []
    n_files_total = 0
    n_neg = 0
    n_working = 0
    worst_x128 = None
    worst_x128_file = None
    min_rs = None
    for gname, gdir in TUBE_GROUPS.items():
        files = sorted(gdir.glob("cert_slice_*_outerbox_tube_K100_*.json"))
        n_files_total += len(files)
        for f in files:
            mm = TUBE_RE.search(f.name)
            if not mm:
                raise RuntimeError("unparsable tube filename: %s" % f.name)
            raw_label = mm.group(1)
            if raw_label.upper().startswith("NEG"):
                n_neg += 1
                continue
            n_working += 1
            d = json.loads(f.read_text(encoding="utf-8"))
            x128 = float(d["x128_lower"])
            if not (x128 > 0):
                raise RuntimeError("x128_lower <= 0 in %s: %s" % (f.name, x128))
            rs = d.get("r_s", d.get("dom_budget_each", d.get("W_tail")))
            if rs is not None:
                rs = float(rs)
                if min_rs is None or rs < min_rs:
                    min_rs = rs
            if worst_x128 is None or x128 < worst_x128:
                worst_x128 = x128
                worst_x128_file = f.name
            # -------- label -> (disk, level) attribution:
            # census_A/B: label as-is, level 7 -- EXCEPT census_B's legacy
            #   Z72 (24 arcs at the ORIGINAL centre; superseded by point17's
            #   shifted contour) -> separate nonblocking bucket.
            # point14: Z57_L7/Z57_L8/Z60_L7/Z60_L8 (explicit level tags);
            #   the stray "ST" file is unattributed.
            # point17: Z72_shifted (FULL 64-arc coverage of the shifted
            #   contour at level 7 -- level evidenced by the H7_abs_lower
            #   field, checked per file below) -> (Z72, 7);
            #   Z72_shifted_L8 (full 64 arcs, H8_abs_lower) -> (Z72, 8);
            #   Z72_stage9_L7/L8: SUBDIVISION of a SUBSET of contour arcs
            #   (indices with gaps) -> refinement bucket, nonblocking,
            #   never counted as contour coverage.
            # fix1: D_MINUS/D_PLUS, level 7.
            base_label, lvl, refinement = None, None, False
            ru = raw_label.upper()
            if gname in ("point10_layer1_census_A", "point10_layer1_census_B"):
                if gname.endswith("_B") and ru == "Z72":
                    base_label, lvl = "Z72_LEGACY_OLD_CONTOUR", 7
                else:
                    base_label, lvl = ru, 7
            elif gname == "point14_m8_base":
                lm = re.match(r"^(Z\d+)_L([78])$", ru)
                if lm:
                    base_label, lvl = lm.group(1), int(lm.group(2))
            elif gname == "point17_z72_geometry":
                if ru == "Z72_SHIFTED":
                    base_label, lvl = "Z72", 7
                elif ru == "Z72_SHIFTED_L8":
                    base_label, lvl = "Z72", 8
                else:
                    lm = re.match(r"^Z72_STAGE9_L([78])$", ru)
                    if lm:
                        base_label, lvl, refinement = "Z72", int(lm.group(1)), True
            elif gname == "point3B_localize_two_roots_agent_fix1":
                if ru in ("D_MINUS", "D_PLUS"):
                    base_label, lvl = ru, 7
            if base_label is None:
                stray_labels.append("%s (group %s)" % (raw_label, gname))
                continue
            # level evidence: the arc file must carry the level's own field
            if not refinement and ("H%d_abs_lower" % lvl) not in d:
                raise RuntimeError("level evidence missing: %s attributed to L%d "
                                   "but has no H%d_abs_lower" % (f.name, lvl, lvl))
            im = ARC_IDX_RE.search(f.name)
            if im is None:
                raise RuntimeError("no arc index in filename: %s" % f.name)
            fam_id = "%s:%s" % (gname, raw_label)
            fam = families.setdefault(fam_id, {
                "disk": base_label, "level": lvl, "group": gname,
                "indices": [], "min_x128_lower": None, "refinement": refinement,
            })
            fam["indices"].append(int(im.group(1)))
            if fam["min_x128_lower"] is None or x128 < fam["min_x128_lower"]:
                fam["min_x128_lower"] = x128

    # family completeness: indices must be exactly 0..K-1 (full contour tiling)
    for fam_id, fam in families.items():
        idx = sorted(fam["indices"])
        fam["n_arcs"] = len(idx)
        fam["contiguous_full"] = (idx == list(range(len(idx))))
        del fam["indices"]
        if fam["refinement"]:
            refinement_families.append(fam_id)
            continue
        if fam["disk"].startswith("Z72_LEGACY"):
            continue
        key = (fam["disk"], fam["level"])
        tube_scan.setdefault(key, []).append(fam_id)
    log("tube scan: %d files total, %d working, %d NEG-excluded, worst x128_lower=%.6e (%s), min r_s=%s" % (
        n_files_total, n_working, n_neg, worst_x128, worst_x128_file, min_rs))
    log("families: %d (refinement, nonblocking: %s)" % (len(families), refinement_families))

    # reconcile with h1pkg accounting
    cov = h1pkg["coverage"]
    recon = {
        "n_files_total_here": n_files_total,
        "n_files_total_h1pkg": cov["n_tube_files_5groups"],
        "n_working_here": n_working,
        "n_working_h1pkg": cov["n_working_arcs_5groups"],
        "n_neg_here": n_neg,
        "n_neg_h1pkg": cov["n_neg_controls_5groups"],
        "counts_match": (n_files_total == cov["n_tube_files_5groups"]
                         and n_working == cov["n_working_arcs_5groups"]
                         and n_neg == cov["n_neg_controls_5groups"]),
        "x128_worst_here": worst_x128,
        "x128_worst_h1pkg": h1pkg["denominator_positivity"]["min_x128_lower"],
        "x128_worst_match": abs(worst_x128 - h1pkg["denominator_positivity"]["min_x128_lower"]) <= 1e-15,
    }
    if not recon["counts_match"]:
        raise RuntimeError("tube accounting does not match h1pkg: %s" % recon)

    # ---------- [4] containment: P_tail < r_s (tube radius)
    tail = h1pkg["tail_resolution"]
    p_tail = float(tail["P_tail_m0_primary_upper"])
    tube_radius = float(tail["tube_radius"])
    containment = {
        "P_tail_m0_primary_upper": p_tail,
        "tube_radius": tube_radius,
        "min_r_s_across_scanned_arcs": min_rs,
        "containment_margin": tube_radius - p_tail,
        "containment_ok": p_tail < tube_radius,
        "containment_ok_vs_min_rs": (min_rs is None) or (p_tail < min_rs),
        "note": "P_tail bounds ||slice_inf - base||_1 uniformly in u (h1pkg tail_resolution, "
                "primary/tight variant M3=1834, applicability argued in h1pkg m3_resolution); "
                "every tube arc certifies x128 != 0 for ALL perturbations up to r_s; "
                "convexity of the ball closes the homotopy (bridge lemma, REPORT_BRIDGE.md).",
    }
    if not (containment["containment_ok"] and containment["containment_ok_vs_min_rs"]):
        raise RuntimeError("containment failed: %s" % containment)

    # ---------- [5] per-disk bridge table: winding level(s) x tube level(s)
    # REQUIRED levels per disk. Level 7 is the LOAD-BEARING level for EVERY
    # disk: the holomorphy of H runs through F_{m0} with m0 = 7 globally
    # (article section 5.2), including the shifted Z72 disk -- the m = 8 work
    # of point14/point17 concerns the H_m winding-transfer margins, not the
    # holomorphy chain (fable review, finding 1: the earlier version of this
    # certificate had Z72's requirement inverted to {8}). For the three disks
    # whose zero-count closure runs at m = 8 (Z57, Z60, Z72) level 8 is kept
    # required as well -- the strictest superset of both readings.
    disk_levels = {}
    for (lbl, lvl) in tube_scan.keys():
        if re.match(r"^Z\d+$", lbl) or lbl in ("D_MINUS", "D_PLUS"):
            disk_levels.setdefault(lbl, set()).add(lvl)
    expected_disks = {d["label"] for d in wind_cert["disks"]}
    if set(disk_levels.keys()) != expected_disks:
        raise RuntimeError("disk set mismatch: tube=%s winding=%s" % (
            sorted(disk_levels.keys()), sorted(expected_disks)))

    required_levels = {lbl: {7} for lbl in expected_disks}
    required_levels["Z57"] = {7, 8}
    required_levels["Z60"] = {7, 8}
    required_levels["Z72"] = {7, 8}

    bridge_table = []
    all_bridged = True
    for lbl in sorted(disk_levels.keys()):
        levels = sorted(disk_levels[lbl])
        rows = []
        bridged_levels = set()
        for lvl in levels:
            w = base_windings.get((lbl, lvl))
            fam_ids = tube_scan.get((lbl, lvl), [])
            fams = [{"family": fid, "group": families[fid]["group"],
                     "n_arcs": families[fid]["n_arcs"],
                     "contiguous_full": families[fid]["contiguous_full"],
                     "min_x128_lower": families[fid]["min_x128_lower"]}
                    for fid in sorted(fam_ids)]
            # coverage requires at least one family that tiles the FULL
            # contour (contiguous 0..K-1) with x128 > 0 throughout
            full_fams = [fm for fm in fams if fm["contiguous_full"] and fm["min_x128_lower"] > 0]
            coverage_complete = len(full_fams) > 0
            tube_min = min((fm["min_x128_lower"] for fm in fams), default=None)
            ok = bool(w and w["pass"] and w["strictly_zero"] and coverage_complete)
            if ok:
                bridged_levels.add(lvl)
            rows.append({
                "level_m": lvl,
                "required": lvl in required_levels[lbl],
                "winding_strictly_zero": bool(w and w["strictly_zero"]),
                "winding_source": (w or {}).get("source"),
                "tube_families": fams,
                "tube_n_arcs": sum(fm["n_arcs"] for fm in fams),
                "tube_min_x128_lower": tube_min,
                "coverage_complete": coverage_complete,
                "bridged": ok,
            })
        disk_ok = required_levels[lbl].issubset(bridged_levels)
        all_bridged = all_bridged and disk_ok
        bridge_table.append({"label": lbl, "levels": levels,
                             "required_levels": sorted(required_levels[lbl]),
                             "bridged_levels": sorted(bridged_levels),
                             "rows": rows, "disk_bridged": disk_ok})

    # geometry consistency: winding geometry == tube-group geometry per disk/level
    # (the winding cert already cross-checks its geometry against the same raw
    #  certs; here we additionally check the NEW m=8 rows against point14)
    geom_checks = []
    for lbl in ("Z57", "Z60"):
        gsrc = m8c["disk_results"][lbl]
        w = base_windings[(lbl, 8)]
        ok = (str(gsrc["centre_re"]) == w["centre_re"] and str(gsrc["centre_im"]) == w["centre_im"]
              and Fraction(str(gsrc["rho"])) == Fraction(w["rho"]))
        geom_checks.append({"label": lbl, "level_m": 8, "match_point14": ok})
        if not ok:
            all_bridged = False

    n_checks = (len(bridge_table) + sum(len(b["rows"]) for b in bridge_table)
                + n_working + len(geom_checks) + 4)

    payload = {
        "run": "bridge_certificate",
        "oid": "bridge14",
        "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "task": "close kit §5.3(v)/§8(5): denominator x_{2^m} of the LIMIT slice has no "
                "zeros inside any of the 25 disks (strict, assembled from pinned components "
                "+ new m=8 windings for Z57/Z60 + convexity homotopy, see REPORT_BRIDGE.md)",
        "prec_bits": flint.ctx.prec,
        "sha256_pins": pins,
        "new_windings": new_windings,
        "tube_reconciliation": recon,
        "containment": containment,
        "stray_tube_labels_nonblocking": sorted(set(stray_labels)),
        "legacy_z72_old_contour_arcs_nonblocking": sum(
            fam["n_arcs"] for fam in families.values()
            if fam["disk"].startswith("Z72_LEGACY")),
        "refinement_families_nonblocking": {
            fid: {"n_arcs": families[fid]["n_arcs"], "level": families[fid]["level"],
                  "contiguous_full": families[fid]["contiguous_full"],
                  "min_x128_lower": families[fid]["min_x128_lower"]}
            for fid in sorted(refinement_families)},
        "bridge_table": bridge_table,
        "geometry_checks_new_m8": geom_checks,
        "n_disks": len(bridge_table),
        "all_disks_bridged": all_bridged,
        "all_pass": bool(all_bridged and recon["counts_match"] and containment["containment_ok"]
                         and all(r["pass"] for r in new_windings if r.get("required"))),
        "n_checks": n_checks,
        "elapsed_total_s": round(time.time() - t0, 1),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log("=== SUMMARY: disks=%d all_bridged=%s all_pass=%s n_checks=%d (%.1fs) ===" % (
        len(bridge_table), all_bridged, payload["all_pass"], n_checks, payload["elapsed_total_s"]))
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
