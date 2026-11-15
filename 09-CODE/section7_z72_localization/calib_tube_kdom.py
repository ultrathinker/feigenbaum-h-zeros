# -*- coding: utf-8 -*-
"""calib_tube_kdom.py -- найти минимальный K_DOM (число named-символов), при
котором compute_arc НЕ раздувается на дугах малого контура, + тайминг и величина
L7. Метод -- точная копия machinery ядра cert_slice_param_audit.py (tube mode),
параметризованная геометрией малого контура."""
from __future__ import annotations
import math, time, sys
from fractions import Fraction
from pathlib import Path
import flint

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
import json
W36 = ROOT / "w36"
sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
import x4_common as xc
from x4_common import AF, ZERO_ARB, mag_lb, mag_ub

flint.ctx.prec = 512
A, C = flint.arb, flint.acb
PI = A.pi()
TWO_PI = 2 * PI
I_UNIT = C(0, 1)
ZERO_ACB = C(0)
ONE_ACB = C(1)
INV_R = C(1) / C("2.5")
TWO_OVER_R = C(2) / C("2.5")
M = xc.M
LIN_F = A("1.10485425032")
PPERP = A("2.808542")

lh_raw = json.loads((W36 / "finish_fable" / "l_hat_fable.json").read_text(encoding="utf-8"))
LHAT = [C(A(a), A(b)) for a, b in zip(lh_raw["l_hat_re"], lh_raw["l_hat_im"])]
RHO_L = A("1.588343e-14")
LHAT_L0_DISTANCE = A("7.925e-15")
L_HEAD_RADIUS = RHO_L + LHAT_L0_DISTANCE
L_TAIL_INF = A("6.990710e-17")
R_S = A("5.44e-7")

delta_ball = C(A(xc.DELTA_pt.real.mid(), A(xc.RHO_D)))
d7inv_ball = ONE_ACB / (delta_ball ** 7)
DNEG7 = AF(C(d7inv_ball.real.mid(), d7inv_ball.imag.mid()), [], A(d7inv_ball.real.rad()) + A(d7inv_ball.imag.rad()))
DSDU_C = DNEG7.c * xc.AU0
DSDU_R = (DNEG7.r * mag_ub(xc.AU0)).upper()


def make_machine(K_DOM, inject_tail):
    S = 1 + K_DOM + (1 if inject_tail else 0)
    TAIL_SLOT = 1 + K_DOM if inject_tail else None
    zv = [ZERO_ACB] * S

    def l1(a):
        s = ZERO_ARB
        for v in a:
            s = s + mag_ub(v)
        return s

    def af_const(c):
        return AF(c, list(zv), ZERO_ARB)

    def af_add(x, y):
        return AF(x.c + y.c, [x.a[i] + y.a[i] for i in range(S)], x.r + y.r)

    def af_addc(x, c):
        return AF(x.c + c, list(x.a), x.r)

    def af_sc(x, c):
        return AF(x.c * c, [ai * c for ai in x.a], x.r * mag_ub(c))

    def af_mul(x, y):
        lx, ly = l1(x.a), l1(y.a)
        return AF(x.c * y.c, [x.c * y.a[i] + y.c * x.a[i] for i in range(S)],
                  lx * ly + mag_ub(x.c) * y.r + mag_ub(y.c) * x.r + lx * y.r + ly * x.r + x.r * y.r)

    def af_recip(y):
        cy_lo = mag_lb(y.c)
        rho = l1(y.a) + y.r
        if cy_lo <= ZERO_ARB or not (rho < cy_lo):
            return None, rho / cy_lo if cy_lo > ZERO_ARB else A("inf")
        q = rho / cy_lo
        invc = ONE_ACB / y.c
        return AF(invc, [-y.a[i] * invc * invc for i in range(S)],
                  y.r / (cy_lo * cy_lo) + (q * q / (1 - q)) / cy_lo), q

    def af_horner(coeffs, z):
        a = af_const(ZERO_ACB)
        for ck in reversed(coeffs):
            a = af_add(af_mul(a, z), ck)
        return a

    def af_abs_u(x):
        return mag_ub(x.c) + l1(x.a) + x.r

    def af_abs_l(x):
        return mag_lb(x.c) - l1(x.a) - x.r

    def af_symb(slot, radius):
        a = list(zv)
        a[slot] = C(A(0, radius), A(0, radius))
        return AF(ZERO_ACB, a, ZERO_ARB)

    def bnorm1(j):
        lj = LHAT[j]
        s = ZERO_ARB
        for k in range(M):
            base = ONE_ACB if k == j else ZERO_ACB
            s += mag_ub(base - lj * xc.tc_h[k])
        return s

    def build_inputs(dom_modes, dom_budget, extra_r_head):
        bcoef = {}
        for i, (j, wbudget) in enumerate(zip(dom_modes, dom_budget)):
            lj = LHAT[j]
            bn = bnorm1(j)
            cbound = wbudget / bn
            cacb = C(cbound)
            for k in range(M):
                base = ONE_ACB if k == j else ZERO_ACB
                bcoef[(i, k)] = cacb * (base - lj * xc.tc_h[k])
        G1 = []
        for k in range(M):
            a = list(zv)
            for i in range(K_DOM):
                a[1 + i] = bcoef[(i, k)]
            G1.append(AF(xc.tc_g[k], a, A(xc.RHO_G) + extra_r_head))
        DG1 = []
        for k in range(1, M):
            a = list(zv)
            kacb = C(k)
            for i in range(K_DOM):
                a[1 + i] = kacb * bcoef[(i, k)]
            DG1.append(AF(kacb * xc.tc_g[k], a, A(k) * (A(xc.RHO_G) + extra_r_head)))
        H1 = [AF(xc.tc_h[k], list(zv), A(xc.RHO_H)) for k in range(M)]
        DH1 = [AF(C(k) * xc.tc_h[k], list(zv), A(k) * A(xc.RHO_H)) for k in range(1, M)]
        return G1, H1, DG1, DH1

    def response(y256, y128, H, inv):
        return af_mul(af_add(y256, af_sc(af_mul(H, y128), C(-1))), inv)

    def compute_arc(G1, H1, DG1, DH1, u_mid, rho, c_fixed_local, tail_budget=A(0)):
        u_a = list(zv)
        u_a[0] = C(rho)
        u = AF(u_mid, u_a, ZERO_ARB)
        s = AF(DSDU_C * u.c, [DSDU_C * u.a[i] for i in range(S)], (DSDU_R * mag_ub(u.c) + DSDU_C.abs_upper() * u.r + u.r * DSDU_R).upper())
        x = af_const(ZERO_ACB)
        yh = af_const(ZERO_ACB)
        ys = [af_const(ZERO_ACB) for _ in range(M)]
        tail_q = ZERO_ARB
        max_r = ZERO_ARB
        max_tail_value = ZERO_ARB
        x128 = yh128 = None
        ys128 = None
        tail_q128 = None
        for n in range(256):
            xx = af_addc(af_mul(x, x), C(-1))
            z = af_sc(xx, INV_R)
            rz = af_abs_u(z).upper()
            if not (rz < 1):
                return None, {"fail": "Rmax", "step": n, "rz": float(rz)}
            if rz > max_r:
                max_r = rz
            vg = af_horner(G1, z)
            vh = af_horner(H1, z)
            vgp = af_horner(DG1, z)
            vhp = af_horner(DH1, z)
            if inject_tail and tail_budget > 0:
                tail_value_bound = tail_budget * (rz ** M + L_TAIL_INF * af_abs_u(vh))
                tail_deriv_geom = (A(M) * rz ** (M - 1) - A(M - 1) * rz ** M) / ((1 - rz) * (1 - rz))
                tail_derivative_bound = tail_budget * (tail_deriv_geom + L_TAIL_INF * af_abs_u(vhp))
                vg = af_add(vg, af_symb(TAIL_SLOT, tail_value_bound))
                vgp = af_add(vgp, af_symb(TAIL_SLOT, tail_derivative_bound))
                if tail_value_bound > max_tail_value:
                    max_tail_value = tail_value_bound
            fpw = af_add(vgp, af_mul(s, vhp))
            powers = [af_const(ONE_ACB)]
            for k in range(1, M):
                powers.append(af_mul(powers[-1], z))
            new_ys = []
            for k in range(M):
                propagated = af_mul(fpw, af_sc(af_mul(x, ys[k]), TWO_OVER_R))
                source = af_add(powers[k], af_sc(vh, -LHAT[k]))
                new_ys.append(af_add(propagated, source))
            yh_new = af_add(af_mul(fpw, af_sc(af_mul(x, yh), TWO_OVER_R)), vh)
            x_new = af_add(vg, af_mul(vh, s))
            fxu = af_abs_u(af_mul(fpw, af_sc(x, TWO_OVER_R))).upper()
            tail_source = (rz ** M) / (1 - rz)
            tail_q = fxu * tail_q + tail_source
            x, yh, ys = x_new, yh_new, new_ys
            if n + 1 == 128:
                x128, yh128, ys128 = x, yh, list(ys)
                tail_q128 = tail_q
        inv, q_recip = af_recip(x128)
        if inv is None:
            return None, {"fail": "recip", "q": float(q_recip)}
        H = af_mul(x, inv)
        phih = response(yh, yh128, H, inv)
        psi = [response(ys[k], ys128[k], H, inv) for k in range(M)]
        dhc = af_addc(phih, -c_fixed_local)
        c_abs = mag_ub(c_fixed_local).upper()
        head_best = ZERO_ARB
        head_argmax = -1
        for k in range(M):
            v = af_add(psi[k], af_sc(dhc, LHAT[k]))
            uval = af_abs_u(v) + c_abs * L_HEAD_RADIUS
            if uval > head_best:
                head_best, head_argmax = uval, k
        den_lo = af_abs_l(x128)
        if not (den_lo > 0):
            return None, {"fail": "denlo"}
        tail_phi = tail_q / den_lo + af_abs_u(x) * tail_q128 / (den_lo * den_lo)
        tail_l = c_abs * L_TAIL_INF
        tail_total = tail_phi + tail_l
        total = max(head_best, tail_total)
        return {"total": total, "head": head_best, "head_argmax": head_argmax,
                "tail_total": tail_total, "Rmax": max_r, "x128_lower": den_lo,
                "phih_upper": af_abs_u(phih)}, None

    return build_inputs, compute_arc, S


def main():
    U0_RE, U0_IM = "4.791660937911268", "7.177581007211361"
    uc = C(A(U0_RE), A(U0_IM))
    r0 = 0.01
    N = 64
    H_L1_FULL = A("6.331194")

    # OUTER_BOX config: each named coord gets full R_S budget; K_DOM=100 names
    # all head modes (no rest -> extra_r_head=0); tail injected.
    K_DOM = 100
    inject = True
    outer_box = True
    build_inputs, compute_arc, S = make_machine(K_DOM, inject)
    modes = list(range(K_DOM))  # all 100 head indices named
    W_TAIL = R_S if (outer_box and inject) else A("0.001") * R_S
    dom_budget_each = R_S if outer_box else (A("0.90") * R_S / K_DOM)
    budgets = [dom_budget_each] * K_DOM
    extra_r_head = ZERO_ARB  # K_DOM==100 -> no rest
    tail_coeff_budget = (W_TAIL / (1 - L_TAIL_INF * H_L1_FULL)).upper()
    G1, H1, DG1, DH1 = build_inputs(modes, budgets, extra_r_head)
    print("K_DOM=%d outer_box=%s inject=%s S=%d tail_coeff_budget=%.4e" % (
        K_DOM, outer_box, inject, S, float(tail_coeff_budget)), flush=True)
    worst_L7 = 0.0
    worst_arc = -1
    t_all = time.time()
    test_arcs = list(range(0, 64, 8)) + [63]
    for j in test_arcs:
        t1 = Fraction(j, N); t2 = Fraction(j + 1, N); tm = (t1 + t2) / 2; dt = t2 - t1
        th = TWO_PI * A(tm.numerator) / A(tm.denominator)
        chord = (2 * A(r0) * (PI * A(dt.numerator) / (2 * A(dt.denominator))).sin()).upper()
        um = uc + C(A(r0)) * (I_UNIT * C(th)).exp()
        ts = time.time()
        out, err = compute_arc(G1, H1, DG1, DH1, um, C(chord), um, tail_coeff_budget)
        dt1 = time.time() - ts
        if out is None:
            print("  arc %2d FAIL %s (%.1fs)" % (j, err, dt1), flush=True)
            continue
        phih_u = float(out["phih_upper"])
        ns_u = float(out["total"])
        L7 = float((LIN_F * out["phih_upper"] + PPERP * out["total"]).upper())
        if L7 > worst_L7:
            worst_L7, worst_arc = L7, j
        print("  arc %2d  Rmax=%.4f  phih<=%.4e  Ns<=%.4e  L7<=%.4e  (%.1fs)" % (
            j, float(out["Rmax"]), phih_u, ns_u, L7, dt1), flush=True)
    print("\nworst L7 (sampled) <= %.4e @ arc %d   sampled time/arc avg" % (worst_L7, worst_arc), flush=True)
    print("m9 margin @r0=0.01: min|H9|_lb=3.83 / (L7*1.7007e-8) = %.4f" % (3.83 / (worst_L7 * 1.7007e-08)), flush=True)
    print("m8 margin @r0=0.01: min|H8|_lb=3.97 / (L7*4.5818e-8) = %.4f" % (3.97 / (worst_L7 * 4.5818e-08)), flush=True)


if __name__ == "__main__":
    main()
