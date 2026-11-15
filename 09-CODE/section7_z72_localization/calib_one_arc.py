# -*- coding: utf-8 -*-
"""calib_one_arc.py -- калибровка: level-7 tube (compute_arc, base mode) на
ОДНОЙ дуге малого контура D(u0, r0), чтобы узнать величину L7_arc и тайминг.
Копия machinery ядра cert_slice_param_audit.py (base mode, K_DOM=0)."""
from __future__ import annotations
import math, time
from fractions import Fraction
from pathlib import Path
import flint

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
flint.ctx.prec = 512
A, C = flint.arb, flint.acb
import sys
sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
import x4_common as xc
from x4_common import AF, ZERO_ARB, mag_lb, mag_ub

import json
W36 = ROOT / "w36"
ZERO_ACB = flint.acb(0)
ONE_ACB = flint.acb(1)
INV_R = flint.acb(1) / flint.acb("2.5")
TWO_OVER_R = flint.acb(2) / flint.acb("2.5")
M = xc.M
FAT = 0.0  # no extra fat for small contour (we control chord exactly)

# data
lh_raw = json.load((W36 / "finish_fable" / "l_hat_fable.json").open())
LHAT = [flint.acb(flint.arb(a), flint.arb(b)) for a, b in zip(lh_raw["l_hat_re"], lh_raw["l_hat_im"])]
RHO_L = flint.arb("1.588343e-14")
LHAT_L0_DISTANCE = flint.arb("7.925e-15")
L_HEAD_RADIUS = RHO_L + LHAT_L0_DISTANCE
L_TAIL_INF = flint.arb("6.990710e-17")
LINF_L = flint.arb("1.104854250319731866")

delta_ball = flint.acb(flint.arb(xc.DELTA_pt.real.mid(), flint.arb(xc.RHO_D)))
d7inv_ball = ONE_ACB / (delta_ball ** 7)
DNEG7 = AF(flint.acb(d7inv_ball.real.mid(), d7inv_ball.imag.mid()), [ZERO_ACB], flint.arb(d7inv_ball.real.rad()) + flint.arb(d7inv_ball.imag.rad()))
DSDU = AF(DNEG7.c, [DNEG7.a[0] * xc.AU0], DNEG7.r * mag_ub(xc.AU0))

S = 1  # base mode, single symbol (u)
ZERO_VECS = [ZERO_ACB] * S


def l1(a):
    s = ZERO_ARB
    for v in a:
        s = s + mag_ub(v)
    return s


def af_const(c):
    return AF(c, list(ZERO_VECS), ZERO_ARB)


def af_add(x, y):
    return AF(x.c + y.c, [x.a[i] + y.a[i] for i in range(S)], x.r + y.r)


def af_add_const(x, c):
    return AF(x.c + c, list(x.a), x.r)


def af_scale_const(x, c):
    return AF(x.c * c, [ai * c for ai in x.a], x.r * mag_ub(c))


def af_mul(x, y):
    lx, ly = l1(x.a), l1(y.a)
    return AF(x.c * y.c, [x.c * y.a[i] + y.c * x.a[i] for i in range(S)],
              lx * ly + mag_ub(x.c) * y.r + mag_ub(y.c) * x.r + lx * y.r + ly * x.r + x.r * y.r)


def af_recip(y):
    cy_lo = mag_lb(y.c)
    rho = l1(y.a) + y.r
    if cy_lo <= ZERO_ARB or not (rho < cy_lo):
        return None, rho / cy_lo if cy_lo > ZERO_ARB else flint.arb("inf")
    q = rho / cy_lo
    invc = ONE_ACB / y.c
    return AF(invc, [-y.a[i] * invc * invc for i in range(S)],
              y.r / (cy_lo * cy_lo) + (q * q / (1 - q)) / cy_lo), q


def af_horner(coeffs, z):
    a = af_const(ZERO_ACB)
    for ck in reversed(coeffs):
        a = af_add(af_mul(a, z), ck)
    return a


def af_abs_upper(x):
    return mag_ub(x.c) + l1(x.a) + x.r


def af_abs_lower(x):
    return mag_lb(x.c) - l1(x.a) - x.r


def response(y256, y128, H, inv_x128):
    return af_mul(af_add(y256, af_scale_const(af_mul(H, y128), flint.acb(-1))), inv_x128)


def bnorm1(j):
    lj = LHAT[j]
    s = flint.arb(0)
    for k in range(M):
        base_kj = ONE_ACB if k == j else ZERO_ACB
        s += mag_ub(base_kj - lj * xc.tc_h[k])
    return s


def build_inputs_base():
    G1 = [AF(xc.tc_g[k], list(ZERO_VECS), flint.arb(xc.RHO_G)) for k in range(M)]
    DG1 = [AF(flint.acb(k) * xc.tc_g[k], list(ZERO_VECS), flint.arb(k) * flint.arb(xc.RHO_G)) for k in range(1, M)]
    H1 = [AF(xc.tc_h[k], list(ZERO_VECS), flint.arb(xc.RHO_H)) for k in range(M)]
    DH1 = [AF(flint.acb(k) * xc.tc_h[k], list(ZERO_VECS), flint.arb(k) * flint.arb(xc.RHO_H)) for k in range(1, M)]
    return G1, H1, DG1, DH1


def compute_arc(G1, H1, DG1, DH1, u_mid, rho, c_fixed_local):
    u_a = [ZERO_ACB] * S
    u_a[0] = flint.acb(rho)
    u = AF(u_mid, u_a, ZERO_ARB)
    s = af_mul(DSDU, u)
    x = af_const(ZERO_ACB)
    yh = af_const(ZERO_ACB)
    ys = [af_const(ZERO_ACB) for _ in range(M)]
    tail_q = flint.arb(0)
    max_r = flint.arb(0)
    max_fx = flint.arb(0)
    x128 = yh128 = ys128 = None
    tail_q128 = None
    for n in range(256):
        xx = af_add_const(af_mul(x, x), flint.acb(-1))
        z = af_scale_const(xx, INV_R)
        rz = af_abs_upper(z).upper()
        if not (rz < 1):
            raise RuntimeError(f"R_n>=1 at n={n}: {rz}")
        if rz > max_r:
            max_r = rz
        vg = af_horner(G1, z)
        vh = af_horner(H1, z)
        vgp = af_horner(DG1, z)
        vhp = af_horner(DH1, z)
        fpw = af_add(vgp, af_mul(s, vhp))
        fx = af_mul(fpw, af_scale_const(x, TWO_OVER_R))
        fxu = af_abs_upper(fx).upper()
        if fxu > max_fx:
            max_fx = fxu
        powers = [af_const(ONE_ACB)]
        for k in range(1, M):
            powers.append(af_mul(powers[-1], z))
        new_ys = []
        for k in range(M):
            propagated = af_mul(fpw, af_scale_const(af_mul(x, ys[k]), TWO_OVER_R))
            source = af_add(powers[k], af_scale_const(vh, -LHAT[k]))
            new_ys.append(af_add(propagated, source))
        yh_new = af_add(af_mul(fpw, af_scale_const(af_mul(x, yh), TWO_OVER_R)), vh)
        x_new = af_add(vg, af_mul(vh, s))
        tail_source = (rz ** M) / (1 - rz)
        tail_q = fxu * tail_q + tail_source
        x, yh, ys = x_new, yh_new, new_ys
        if n + 1 == 128:
            x128, yh128, ys128 = x, yh, list(ys)
            tail_q128 = tail_q
    inv, q_recip = af_recip(x128)
    if inv is None:
        raise RuntimeError(f"x128 reciprocal failed q={q_recip}")
    H = af_mul(x, inv)
    phih = response(yh, yh128, H, inv)
    psi = [response(ys[k], ys128[k], H, inv) for k in range(M)]
    dhc = af_add_const(phih, -c_fixed_local)
    c_abs = mag_ub(c_fixed_local).upper()
    head_best = flint.arb(0)
    head_argmax = -1
    for k in range(M):
        v = af_add(psi[k], af_scale_const(dhc, LHAT[k]))
        uval = af_abs_upper(v) + c_abs * L_HEAD_RADIUS
        if uval > head_best:
            head_best, head_argmax = uval, k
    den_lo = af_abs_lower(x128)
    tail_phi = tail_q / den_lo + af_abs_upper(x) * tail_q128 / (den_lo * den_lo)
    tail_l = c_abs * L_TAIL_INF
    tail_total = tail_phi + tail_l
    total = max(head_best, tail_total)
    return {"total": total, "head": head_best, "head_argmax": head_argmax,
            "tail_total": tail_total, "Rmax": max_r, "fxmax": max_fx,
            "x128_lower": den_lo, "phih": phih, "phih_upper": af_abs_upper(phih)}


def main():
    U0_RE, U0_IM = "4.791660937911268", "7.177581007211361"
    r0 = 0.01
    N = 64
    G1, H1, DG1, DH1 = build_inputs_base()
    print("base-mode compute_arc calibration on small-contour arcs (r0=%g, N=%d)" % (r0, N), flush=True)
    LIN_F = flint.arb("1.10485425032")
    PPERP = flint.arb("2.808542")
    worst = 0.0
    worst_arc = -1
    t_all = time.time()
    for j in range(N):
        t1 = Fraction(j, N)
        t2 = Fraction(j + 1, N)
        tm = (t1 + t2) / 2
        TWO_PI = 2 * flint.arb.pi()
        theta = TWO_PI * flint.arb(tm.numerator) / flint.arb(tm.denominator)
        chord = (2 * flint.arb(r0) * (flint.arb.pi() * flint.arb((t2 - t1).numerator) / (2 * flint.arb((t2 - t1).denominator))).sin()).upper()
        um_re = float(flint.arb(U0_RE)) + r0 * math.cos(float(theta))
        um_im = float(flint.arb(U0_IM)) + r0 * math.sin(float(theta))
        um = flint.acb(flint.arb(repr(um_re)), flint.arb(repr(um_im)))
        # float center for phih (use midpoint float orbit)
        ts = time.time()
        out = compute_arc(G1, H1, DG1, DH1, um, flint.arb(repr(float(chord))), um)
        dt = time.time() - ts
        phih_u = float(out["phih_upper"])
        ns_u = float(out["total"])
        L7 = float((LIN_F * out["phih_upper"] + PPERP * out["total"]).upper())
        if L7 > worst:
            worst, worst_arc = L7, j
        if j % 8 == 0 or j == N - 1:
            print("  arc %2d  Rmax=%.4f  phih<=%.4e  Ns<=%.4e  L7<=%.4e  x128_lo=%.4e  (%.2fs)" % (
                j, float(out["Rmax"]), phih_u, ns_u, L7, float(out["x128_lower"]), dt), flush=True)
    print("\nWORST L7_arc(base) <= %.4e at arc %d   total calib time=%.1fs (N=%d)" % (
        worst, worst_arc, time.time() - t_all, N), flush=True)
    # margin at r0=0.01 with this worst L7
    S_minus = 4.6395e-08
    minH8 = 4.172852
    print("rough margin @r0=0.01 with worst L7_base: min|H8|/(L7*(S-Phi)) = %.4f" % (minH8 / (worst * S_minus)), flush=True)


if __name__ == "__main__":
    main()
