#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""winding_verify.py -- independent verifier for winding_certificate.json.

Deliberately a SEPARATE code path from winding_certificate.py:
  - complex arithmetic is done by hand on (re,im) arb PAIRS (tuples), never
    through flint.acb's `*`/`/` operator overloading;
  - the g,h series are evaluated by DIRECT POWER ACCUMULATION (build z^0..z^99
    forward, weighted-sum) instead of Horner's nested backward form;
  - the arc-covering chord is re-derived via the algebraically-equivalent
    cos-identity  chord = rho*sqrt(2-2*cos(phi))  (phi = pi*dt, the FULL
    angular separation) instead of  2*rho*sin(phi/2);
  - u_mid is built from cos(theta)/sin(theta) directly, not via a complex
    exponential;
  - AU0/DELTA^m is divided by a hand-written complex division formula.
  - geometry (centre, rho, m) is re-read from the SAME raw certificate files
    used by winding_certificate.py and cross-checked against what the
    certificate claims -- never trusted from the certificate JSON alone.
  - EPS_G/EPS_H are re-derived from the pinned CL-34 files, not copied.

It does NOT import winding_certificate.py. Exits 1 on ANY discrepancy: sha256
mismatch, geometry drift, a disk whose independently-recomputed checks
disagree with what the certificate claims (tiling, coverage, domain,
denominator-nonzero, winding count/uniqueness/strictly_zero, pass), or a
top-level aggregate (n_pass, all_pass, n_checks, worst min|x|) that does not
match the independent recomputation.

Usage: python winding_verify.py [path/to/winding_certificate.json]
       (default: winding_certificate.json next to this script)
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

import flint

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
CERT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else (HERE / "winding_certificate.json")

flint.ctx.prec = 512
A = flint.arb

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


def rp(rel):
    return ROOT / rel


sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
import x4_common as xc  # noqa: E402  (READ-ONLY frozen certified input, same as the certificate)

M = xc.M
if M != 100:
    raise RuntimeError("expected M=100, got %d" % M)

X4_PATH = rp("w35/x4_walk_sonnet/x4_common.py")
GH_PATH = rp("w33/t5_cert_sonnet/w33_gh_hiprec.json")
CL34_PATH = rp("w36/tail_codex/cl34_certificate.json")
ABS36_PATH = rp("w36/audit_codex/absolute_margins_arb.json")
CENSUS_A = rp("path_to_8/point10_layer1_census_A/census_A_certificate.json")
CENSUS_B = rp("path_to_8/point10_layer1_census_B/census_B_certificate.json")
Z72_CERT = rp("path_to_8/point17_z72_geometry/z72_certificate.json")
FIX1_CERT = rp("path_to_8/point3B_localize_two_roots_agent_fix1/localization_certificate.json")

PIN_MAP = {
    "x4_common.py": X4_PATH,
    "w33_gh_hiprec.json": GH_PATH,
    "cl34_certificate.json": CL34_PATH,
    "absolute_margins_arb.json": ABS36_PATH,
    "census_A_certificate.json": CENSUS_A,
    "census_B_certificate.json": CENSUS_B,
    "z72_certificate.json": Z72_CERT,
    "localization_certificate.json (fix1, optional disks)": FIX1_CERT,
}


def arb_from_ratio_str(s):
    s = str(s)
    if "/" in s:
        n, d = s.split("/")
        return A(int(n)) / A(int(d))
    return A(s)


# ================================================================== [0] load certificate + sha256
if not CERT_PATH.exists():
    print("certificate not found:", CERT_PATH)
    sys.exit(1)
CERT = json.loads(CERT_PATH.read_text(encoding="utf-8"))

print("[0] sha256 of pinned input files")
for name, path in PIN_MAP.items():
    pinned = CERT.get("sha256_pins", {}).get(name)
    if pinned is None:
        err("certificate missing sha256 pin for %s" % name)
        continue
    if not path.exists():
        err("input missing on disk: %s" % name)
        continue
    actual = sha256(path)
    if actual != pinned:
        err("sha256 mismatch %s\n     cert:   %s\n     actual: %s" % (name, pinned, actual))
print("    %d inputs checked" % len(PIN_MAP))

# EPS_G/EPS_H re-derived fresh from the CL-34 files (not copied from the certificate)
_cl34 = json.loads(CL34_PATH.read_text(encoding="utf-8"))
_abs36 = json.loads(ABS36_PATH.read_text(encoding="utf-8"))
EPS_G = A(_cl34["G"]["distance_and_Taylor_tail_upper"]).upper()
EPS_H = A(_cl34["V_h_delta"]["h_error_stored_center_upper"]).upper()
if str(CERT.get("EPS_G")) != str(EPS_G) or str(CERT.get("EPS_H")) != str(EPS_H):
    # allow whitespace-insensitive comparison, else flag
    if CERT.get("EPS_G", "").split()[0:1] != str(EPS_G).split()[0:1]:
        err("EPS_G drift: cert=%s recomputed=%s" % (CERT.get("EPS_G"), EPS_G))
    if CERT.get("EPS_H", "").split()[0:1] != str(EPS_H).split()[0:1]:
        err("EPS_H drift: cert=%s recomputed=%s" % (CERT.get("EPS_H"), EPS_H))

# safety_factor is a fixed algorithm parameter (expected ~1.000001); sanity
# check the certificate's recorded value against that expectation (its own
# midpoint, parsed as plain text -- not fed through arb parsing).
_sf_raw = str(CERT.get("safety_factor", ""))
try:
    _sf_mid = float(_sf_raw.lstrip("[").split()[0])
    if abs(_sf_mid - 1.000001) > 1e-9:
        err("safety_factor drift: cert=%s expected~1.000001" % _sf_raw)
except Exception:
    err("safety_factor unparsable: %s" % _sf_raw)


# ================================================================== manual complex arithmetic (re,im) tuples
def cmk(re, im=0):
    return (A(re), A(im))


def cadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def csub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def cmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cscale(x, s):
    return (x[0] * s, x[1] * s)


def cdiv(x, y):
    """Hand-written complex division (a+bi)/(c+di) = ((ac+bd)+(bc-ad)i)/(c^2+d^2)."""
    a, b = x
    c, d = y
    denom = c * c + d * d
    return ((a * c + b * d) / denom, (b * c - a * d) / denom)


def cabs2_ub(x):
    return x[0] * x[0] + x[1] * x[1]


def cabs_ub(x):
    return cabs2_ub(x).sqrt()


def cabs_lb(x):
    # same ball; the ball's own .lower() is the rigorous lower bound
    return cabs2_ub(x).sqrt()


def acb_to_pair(z):
    return (A(z.real), A(z.imag))


# affine state: (cre, cim, are, aim, r) -- one complex symbol (are,aim) plus a
# scalar isotropic remainder r (arb).
def vconst(re, im=0):
    return (A(re), A(im), A(0), A(0), A(0))


def vadd(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3], x[4] + y[4])


def vaddc(x, re, im=0):
    return (x[0] + re, x[1] + im, x[2], x[3], x[4])


def vscalec(x, sre, sim=0):
    """scale by a plain complex constant (sre,sim)"""
    c = cmul((x[0], x[1]), (sre, sim))
    a = cmul((x[2], x[3]), (sre, sim))
    r = x[4] * cabs_ub((sre, sim))
    return (c[0], c[1], a[0], a[1], r)


def vmul(x, y):
    xc, yc = (x[0], x[1]), (y[0], y[1])
    xa, ya = (x[2], x[3]), (y[2], y[3])
    c = cmul(xc, yc)
    a1 = cmul(xc, ya)
    a2 = cmul(yc, xa)
    a = cadd(a1, a2)
    axu = cabs_ub(xa)
    ayu = cabs_ub(ya)
    xcu = cabs_ub(xc)
    ycu = cabs_ub(yc)
    r = (axu * ayu + xcu * y[4] + ycu * x[4] + axu * y[4] + ayu * x[4] + x[4] * y[4])
    return (c[0], c[1], a[0], a[1], r)


def vabs_lb(x):
    return cabs_lb((x[0], x[1])).lower() - cabs_ub((x[2], x[3])).upper() - x[4]


def vabs_ub(x):
    return cabs_ub((x[0], x[1])).upper() + cabs_ub((x[2], x[3])).upper() + x[4]


def power_sum_eval(coeffs_pairs, z):
    """Evaluate sum_k coeff_k * z^k by DIRECT power accumulation (forward),
    NOT Horner (the certificate uses reversed-coefficient Horner)."""
    powers = [vconst(1, 0)]
    for _ in range(1, len(coeffs_pairs)):
        powers.append(vmul(powers[-1], z))
    acc = vconst(0, 0)
    for k, (cre, cim) in enumerate(coeffs_pairs):
        acc = vadd(acc, vscalec(powers[k], cre, cim))
    return acc


G_PAIRS = [acb_to_pair(c) for c in xc.tc_g]
H_PAIRS = [acb_to_pair(c) for c in xc.tc_h]
AU0_PAIR = acb_to_pair(xc.AU0)
DELTA_PAIR = acb_to_pair(xc.DELTA_pt)
INV_R_PAIR = cdiv((A(1), A(0)), (xc.r_disc, A(0)))


def cpow_int(x, n):
    r = x
    for _ in range(n - 1):
        r = cmul(r, x)
    return r


def xden_v(u_mid_pair, u_rad, m):
    """Independent recomputation of the AF enclosure of x_{2^m}(u) over
    disk(u_mid,u_rad), via the manual-tuple / power-sum code path."""
    delta_m = cpow_int(DELTA_PAIR, m)
    s_factor = cdiv(AU0_PAIR, delta_m)
    u = (u_mid_pair[0], u_mid_pair[1], A(u_rad), A(0), A(0))
    s = vscalec(u, s_factor[0], s_factor[1])
    s_abs = vabs_ub(s)
    x = vconst(0, 0)
    lev = 1 << m
    max_w = A(0)
    for n in range(lev):
        xx = vmul(x, x)
        xx = vaddc(xx, A(-1), A(0))
        w = vscalec(xx, INV_R_PAIR[0], INV_R_PAIR[1])
        wu = vabs_ub(w)
        if not (wu < 1):
            return None, {"fail": "composition", "step": n}
        if wu > max_w:
            max_w = wu
        vg = power_sum_eval(G_PAIRS, w)
        vh = power_sum_eval(H_PAIRS, w)
        vg = (vg[0], vg[1], vg[2], vg[3], vg[4] + EPS_G)
        vh = (vh[0], vh[1], vh[2], vh[3], vh[4] + EPS_H)
        x = vadd(vg, vmul(vh, s))
        x = (x[0], x[1], x[2], x[3], x[4] + EPS_G + s_abs * EPS_H)
    return x, {"max_w": max_w}


# ================================================================== geometry (re-read raw, cross-check)
def load_disks_raw():
    disks = {}

    ca = json.loads(CENSUS_A.read_text(encoding="utf-8"))
    for lbl, r in ca["disk_results"].items():
        if r.get("count") != 1 or str(lbl).startswith("NEG"):
            continue
        disks[lbl] = {"pack": "A", "m": 7, "required": True,
                       "centre_re": str(r["centre_re"]), "centre_im": str(r["centre_im"]),
                       "rho": str(r["rho"])}

    cb = json.loads(CENSUS_B.read_text(encoding="utf-8"))
    for lbl, r in cb["disk_results"].items():
        if r.get("count") != 1 or str(lbl).startswith("NEG"):
            continue
        disks[lbl] = {"pack": "B", "m": 7, "required": True,
                       "centre_re": str(r["centre_re"]), "centre_im": str(r["centre_im"]),
                       "rho": str(r["rho"])}

    z72 = json.loads(Z72_CERT.read_text(encoding="utf-8"))
    ct = z72["contour"]
    disks["Z72"] = {"pack": "17", "m": 8, "required": True,
                     "centre_re": str(ct["centre_re"]), "centre_im": str(ct["centre_im"]),
                     "rho": str(ct["rho"])}

    fx = json.loads(FIX1_CERT.read_text(encoding="utf-8"))
    for lbl in ("D_minus", "D_plus"):
        d = fx["disks"][lbl]
        disks[lbl.upper()] = {"pack": "3B_fix1", "m": 7, "required": False,
                               "centre_re": d["centre"], "centre_im": "0",
                               "rho": d["rho"]}
    return disks


RAW = load_disks_raw()

print("[1] geometry cross-check (raw certs vs winding_certificate.json)")
n_required_raw = sum(1 for v in RAW.values() if v["required"])
if n_required_raw != 23:
    err("raw geometry: expected 23 required disks, got %d" % n_required_raw)
cert_labels = {d["label"] for d in CERT["disks"]}
if cert_labels != set(RAW.keys()):
    err("disk label set mismatch: cert=%s raw=%s" % (sorted(cert_labels), sorted(RAW.keys())))
for d in CERT["disks"]:
    lbl = d["label"]
    if lbl not in RAW:
        err("certificate has unknown disk label %s (not in raw geometry)" % lbl)
        continue
    g = RAW[lbl]
    if d["pack"] != g["pack"] or d["m"] != g["m"] or bool(d["required"]) != bool(g["required"]):
        err("%s pack/m/required mismatch: cert=(%s,%s,%s) raw=(%s,%s,%s)" % (
            lbl, d["pack"], d["m"], d["required"], g["pack"], g["m"], g["required"]))
    if str(d["centre_re"]) != g["centre_re"] or str(d["centre_im"]) != g["centre_im"]:
        err("%s centre drift: cert=(%s,%s) raw=(%s,%s)" % (
            lbl, d["centre_re"], d["centre_im"], g["centre_re"], g["centre_im"]))
    if Fraction(str(d["rho"])) != Fraction(g["rho"]):
        err("%s rho drift: cert=%s raw=%s" % (lbl, d["rho"], g["rho"]))
print("    %d disks, geometry OK if no FAIL above" % len(RAW))


# ================================================================== [2] per-disk independent recomputation
def check_tiling_v(n_arcs):
    total = Fraction(0)
    for k in range(n_arcs):
        total += Fraction(k + 1, n_arcs) - Fraction(k, n_arcs)
    return total == 1


def coverage_margin_v(rho, t1, t2, u_rad):
    """Cos-identity form: chord = rho*sqrt(2-2*cos(phi)), phi = pi*(t2-t1)
    (FULL angular separation midpoint<->endpoint is phi/2... wait: see note).
    Algebraic identity with the certificate's 2*rho*sin(pi*dt/2): with
    phi = pi*dt (dt=t2-t1), rho*sqrt(2-2*cos(phi)) == 2*rho*sin(phi/2)
    == 2*rho*sin(pi*dt/2). Cross-checked independently below."""
    dt = t2 - t1
    phi = A.pi() * A(dt.numerator) / A(dt.denominator)
    chord_ub = (rho * (2 - 2 * phi.cos()).sqrt()).upper()
    return u_rad - chord_ub, chord_ub


print("[2] per-disk independent recomputation (tiling, coverage, domain, "
      "denominator, winding)")
t0 = time.time()
n_pass_required_v = 0
n_pass_optional_v = 0
worst_min_abs_v = None
n_checks_v = 0

for d in CERT["disks"]:
    lbl = d["label"]
    if lbl not in RAW:
        continue
    g = RAW[lbl]
    m = g["m"]
    uc = acb_to_pair(flint.acb(A(g["centre_re"]), A(g["centre_im"])))
    rho = arb_from_ratio_str(g["rho"])

    if "n_arcs" not in d:
        # certificate itself recorded a hard failure for this disk
        if d.get("pass"):
            err("%s: certificate has no n_arcs but claims pass=True" % lbl)
        continue

    n_arcs = d["n_arcs"]
    n_checks_v += 4 * n_arcs + 2

    tiling_v = check_tiling_v(n_arcs)
    if tiling_v != bool(d.get("tiling_ok")):
        err("%s tiling_ok drift: cert=%s recomputed=%s" % (lbl, d.get("tiling_ok"), tiling_v))

    worst_cov = None
    worst_den = None
    max_w_v = A(0)
    domain_ok_v = True
    den_ok_v = True
    per_arc = []
    fail_arc_msg = None
    TWO_PI = 2 * A.pi()
    for k in range(n_arcs):
        t1 = Fraction(k, n_arcs)
        t2 = Fraction(k + 1, n_arcs)
        tm = (t1 + t2) / 2
        theta = TWO_PI * A(tm.numerator) / A(tm.denominator)
        u_mid = (uc[0] + rho * theta.cos(), uc[1] + rho * theta.sin())

        margin0, chord_ub = coverage_margin_v(rho, t1, t2, A(0))
        # SAFETY_FACTOR is a fixed algorithm parameter (1.000001), not derived
        # data -- defined independently here rather than parsed out of the
        # certificate's arb-ball repr string (which is not a bare decimal).
        u_rad = float(chord_ub) * 1.000001
        margin, _ = coverage_margin_v(rho, t1, t2, A(u_rad))
        if worst_cov is None or margin < worst_cov:
            worst_cov = margin

        xa, diag = xden_v(u_mid, u_rad, m)
        if xa is None:
            domain_ok_v = False
            fail_arc_msg = "%s arc %d domain fail (recomputed)" % (lbl, k)
            break
        if diag["max_w"] > max_w_v:
            max_w_v = diag["max_w"]
        den_lo = vabs_lb(xa)
        if worst_den is None or den_lo < worst_den:
            worst_den = den_lo
        if not (den_lo > 0):
            den_ok_v = False
            fail_arc_msg = "%s arc %d denominator<=0 (recomputed)" % (lbl, k)
            break
        per_arc.append((t1, t2))

    if fail_arc_msg:
        err(fail_arc_msg)
        if d.get("pass"):
            err("%s: certificate claims pass=True despite recomputed failure" % lbl)
        continue

    cov_ok_v = bool(worst_cov is not None and worst_cov > 0)
    if cov_ok_v != bool(d.get("arc_disk_coverage_ok")):
        err("%s arc_disk_coverage_ok drift: cert=%s recomputed=%s" % (
            lbl, d.get("arc_disk_coverage_ok"), cov_ok_v))
    cert_margin = d.get("arc_disk_coverage_worst_margin")
    if cert_margin is not None and worst_cov is not None:
        recomputed_margin = float(worst_cov)
        if cert_margin <= 0 or recomputed_margin <= 0:
            if (cert_margin > 0) != (recomputed_margin > 0):
                err("%s coverage margin sign drift: cert=%.3e recomputed=%.3e" % (
                    lbl, cert_margin, recomputed_margin))
        elif abs(cert_margin - recomputed_margin) > 1e-4 * max(cert_margin, recomputed_margin):
            err("%s coverage margin drift: cert=%.6e recomputed=%.6e" % (
                lbl, cert_margin, recomputed_margin))

    if domain_ok_v != bool(d.get("domain_ok")):
        err("%s domain_ok drift: cert=%s recomputed=%s" % (lbl, d.get("domain_ok"), domain_ok_v))

    den_nonzero_v = bool(worst_den is not None and worst_den > 0)
    if den_nonzero_v != bool(d.get("denominator_nonzero_on_contour")):
        err("%s denominator_nonzero_on_contour drift: cert=%s recomputed=%s" % (
            lbl, d.get("denominator_nonzero_on_contour"), den_nonzero_v))
    cert_min_abs = d.get("min_abs_denominator_lower")
    if cert_min_abs is not None and worst_den is not None:
        recomputed_min_abs = float(worst_den.lower())
        if not (recomputed_min_abs > 0):
            err("%s recomputed min|x_2^m| lower bound <= 0: %.6e" % (lbl, recomputed_min_abs))
        rel = abs(cert_min_abs - recomputed_min_abs) / max(abs(cert_min_abs), abs(recomputed_min_abs), 1e-300)
        if rel > 1e-3:
            err("%s min_abs_denominator_lower drift: cert=%.8e recomputed=%.8e (rel=%.2e)" % (
                lbl, cert_min_abs, recomputed_min_abs, rel))
        if worst_min_abs_v is None or recomputed_min_abs < worst_min_abs_v:
            if g["required"]:
                worst_min_abs_v = recomputed_min_abs

    # endpoints + winding, independent path (cos/sin, manual complex, direct
    # power sum)
    needed_ts = set()
    for t1, t2 in per_arc:
        needed_ts.add(t1)
        needed_ts.add(t2)
    endpoints = {}
    ep_fail = False
    for t in needed_ts:
        theta = A(0) if t in (0, 1) else TWO_PI * A(t.numerator) / A(t.denominator)
        u_pt = (uc[0] + rho * theta.cos(), uc[1] + rho * theta.sin())
        xa, diag = xden_v(u_pt, 0.0, m)
        if xa is None:
            ep_fail = True
            break
        cre, cim, are, aim, rr = xa
        re_m = A(cre.mid())
        im_m = A(cim.mid())
        err_rad = A(cre.rad()) + A(cim.rad()) + cabs_ub((are, aim)).upper() + rr
        endpoints[t] = (re_m, im_m, err_rad)

    if ep_fail:
        err("%s endpoint recompute failed" % lbl)
        continue

    # Balls are assembled into flint.acb only for the FINAL arg() step below
    # (arg() itself is not re-derived by hand; that would just be
    # re-implementing atan2 pointlessly). Everything upstream (the affine
    # orbit itself) is the independent manual-tuple/power-sum computation.
    total = A(0)
    for t1, t2 in per_arc:
        z2 = flint.acb(flint.arb(endpoints[t2][0], endpoints[t2][2]),
                        flint.arb(endpoints[t2][1], endpoints[t2][2]))
        z1 = flint.acb(flint.arb(endpoints[t1][0], endpoints[t1][2]),
                        flint.arb(endpoints[t1][1], endpoints[t1][2]))
        total = total + (z2 / z1).arg()
    TWO_PI_L = 2 * A.pi()
    wind_v = total / TWO_PI_L
    cand_v = int(round(float(wind_v.mid())))
    unique_v = ((wind_v - cand_v).contains(0)
                and not (wind_v - (cand_v - 1)).contains(0)
                and not (wind_v - (cand_v + 1)).contains(0))
    strictly_zero_v = bool(unique_v and cand_v == 0)

    if cand_v != d.get("winding_candidate"):
        err("%s winding_candidate drift: cert=%s recomputed=%s" % (lbl, d.get("winding_candidate"), cand_v))
    if unique_v != bool(d.get("winding_unique")):
        err("%s winding_unique drift: cert=%s recomputed=%s" % (lbl, d.get("winding_unique"), unique_v))
    if strictly_zero_v != bool(d.get("strictly_zero")):
        err("%s strictly_zero drift: cert=%s recomputed=%s" % (lbl, d.get("strictly_zero"), strictly_zero_v))

    pass_v = bool(tiling_v and cov_ok_v and domain_ok_v and den_nonzero_v and unique_v and strictly_zero_v)
    if pass_v != bool(d.get("pass")):
        err("%s pass drift: cert=%s recomputed=%s" % (lbl, d.get("pass"), pass_v))

    if pass_v and g["required"]:
        n_pass_required_v += 1
    if pass_v and not g["required"]:
        n_pass_optional_v += 1

print("    %d disks recomputed via manual-tuple/power-sum path in %.1fs" % (len(CERT["disks"]), time.time() - t0))

# ================================================================== [3] top-level aggregates
print("[3] top-level aggregate cross-check")
if CERT.get("n_pass_required") != n_pass_required_v:
    err("n_pass_required drift: cert=%s recomputed=%s" % (CERT.get("n_pass_required"), n_pass_required_v))
if CERT.get("n_disks_required") != 23:
    err("n_disks_required != 23 in certificate: %s" % CERT.get("n_disks_required"))
all_pass_v = (n_pass_required_v == 23)
if bool(CERT.get("all_pass_required")) != all_pass_v:
    err("all_pass_required drift: cert=%s recomputed=%s" % (CERT.get("all_pass_required"), all_pass_v))
if bool(CERT.get("all_pass")) != bool(CERT.get("all_pass_required")):
    err("all_pass does not match all_pass_required: all_pass=%s all_pass_required=%s" % (
        CERT.get("all_pass"), CERT.get("all_pass_required")))
if CERT.get("n_checks") != n_checks_v:
    err("n_checks drift: cert=%s recomputed=%s" % (CERT.get("n_checks"), n_checks_v))
if worst_min_abs_v is not None:
    cert_worst = CERT.get("worst_min_abs_denominator_required")
    if cert_worst is None:
        err("certificate missing worst_min_abs_denominator_required")
    else:
        rel = abs(cert_worst - worst_min_abs_v) / max(abs(cert_worst), abs(worst_min_abs_v), 1e-300)
        if rel > 1e-3:
            err("worst_min_abs_denominator_required drift: cert=%.8e recomputed=%.8e" % (
                cert_worst, worst_min_abs_v))
if not all_pass_v:
    err("recomputed all_pass_required is False -- required disks do not all pass independently")

print("    n_pass_required=%d/23  n_checks=%s  worst_min_abs=%.4e" % (
    n_pass_required_v, CERT.get("n_checks"), worst_min_abs_v if worst_min_abs_v else float("nan")))

# ================================================================== verdict
print()
if errors:
    print("VERDICT: FAIL (%d error(s))" % len(errors))
    sys.exit(1)
print("VERDICT: PASS -- winding_certificate.json internally consistent; %d input files "
      "sha256-pinned; geometry cross-checked against raw certs; every disk's tiling/"
      "coverage/domain/denominator/winding independently recomputed via a separate "
      "(manual-complex-tuple, direct power-sum, cos-identity chord) code path; "
      "%d/23 required disks strictly wind=0." % (len(PIN_MAP), n_pass_required_v))
sys.exit(0)
