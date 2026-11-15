# -*- coding: utf-8 -*-
# ПАРАМЕТРИЗОВАННАЯ КОПИЯ slice_sonnet/cert_slice.py (оркестратор, 10.08 поздний вечер).
# Диффы ТОЛЬКО: TOOTH/N_ARCS/ARC_IDX из argv[4..6], TAG с зубом/дугой, key из TOOTH.
# Перед доверием обязана воспроизвести base- и tube-числа оригинала на D/32/дуга 9.

"""Probe of Sonnet idea #1: named (symbolic) tube perturbation on the slice
{q: l(q)=0} inside cert_orbitchan.py's orbit-response machine, on the worst
arc of tooth D.

Baseline mode (K_DOM=0): must reproduce cert_orbitchan_D_32arcs.json's worst
arc (arc index 9) bit-for-bit-consistent upper bound N_s<=146981.667... .

Tube mode (K_DOM=20): adds K_DOM named eps_j symbols carrying the dominant
b_j = e_j - l_j*h directions (l(h)=1 exactly, checked), |c_j|<=weight_j,
plus a scalar remainder radius on G1 covering (a) the non-dominant head
modes 0<=j<100 not chosen as symbols and (b) is bookended analytically
(not fed into the machine) for the j>=100 tail via the R<=0.403 decay
argument. sum of ALL weights (dominant + head-rest + tail) = r_s.

Usage: python cert_slice.py base           -> baseline (K_DOM=0), sverka
       python cert_slice.py tube [K_DOM]   -> tube probe (default K_DOM=20)
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import flint

ROOT = Path(r"D:\Исследования\И-1 — Нули функции H\Feigenbaum-archive")
W36 = ROOT / "w36"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
import x4_common as xc  # noqa: E402
from x4_common import AF, ZERO_ARB, mag_lb, mag_ub  # noqa: E402

flint.ctx.prec = 512

MODE = sys.argv[1] if len(sys.argv) > 1 else "base"
if MODE not in ("base", "tube"):
    raise SystemExit("MODE must be base or tube")
K_DOM = int(sys.argv[2]) if len(sys.argv) > 2 else (0 if MODE == "base" else 100)
DIAG = sys.argv[3] if len(sys.argv) > 3 else ""  # "" | "noRest" | "domOnly1" | "restOnly"
OUTER_BOX = os.environ.get("SLICE_OUTER_BOX", "0") == "1"
RUN_LABEL = os.environ.get("SLICE_RUN_LABEL", "")
INJECT_TAIL = os.environ.get("SLICE_INJECT_TAIL", "1") == "1"

TOOTH = sys.argv[4] if len(sys.argv) > 4 else "D"
N_ARCS = int(sys.argv[5]) if len(sys.argv) > 5 else 32
ARC_IDX = int(sys.argv[6]) if len(sys.argv) > 6 else 9
FAT = 0.01
R_CONTOUR = 0.1
M = xc.M
if M != 100:
    raise RuntimeError(f"expected M=100, got {M}")
R_S = flint.arb("5.44e-7")  # trubka l1 budget, w36_final_assembly section 4 item 5

TAG = f"{RUN_LABEL}{'outerbox_' if OUTER_BOX else ''}{MODE}_K{K_DOM}_{TOOTH}{N_ARCS}a{ARC_IDX}"
LOG_PATH = HERE / f"cert_slice_{TAG}.log"
JSON_PATH = HERE / f"cert_slice_{TAG}.json"
LOGF = LOG_PATH.open("w", encoding="utf-8", buffering=1)
T0 = time.time()


def log(s: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')} +{time.time()-T0:8.1f}s] {s}"
    print(line, flush=True)
    LOGF.write(line + "\n")
    LOGF.flush()
    os.fsync(LOGF.fileno())


def ub(x) -> float:
    if hasattr(x, "upper"):
        x = x.upper()
    return math.nextafter(float(x), math.inf)


def lb(x) -> float:
    if hasattr(x, "lower"):
        x = x.lower()
    return math.nextafter(float(x), -math.inf)


ZERO_ACB = flint.acb(0)
ONE_ACB = flint.acb(1)
INV_R = flint.acb(1) / flint.acb("2.5")
TWO_OVER_R = flint.acb(2) / flint.acb("2.5")

S = 1 + K_DOM + (1 if INJECT_TAIL else 0)
# slots: 0=u(arc disk), 1..K_DOM=head b_j, last=the arbitrary l1 tail j>=100
TAIL_SLOT = 1 + K_DOM if INJECT_TAIL else None
ZERO_VECS = [ZERO_ACB] * S

log(f"=== MODE={MODE} K_DOM={K_DOM} S={S} tail_symbol={INJECT_TAIL} tooth={TOOTH} arc={ARC_IDX}/{N_ARCS} precision={flint.ctx.prec} ===")


# ---------------------------------------------------------------- AF algebra
def af_const(c):
    return AF(c, ZERO_VECS, ZERO_ARB)


def l1(a):
    s = ZERO_ARB
    for v in a:
        s = s + mag_ub(v)
    return s


def af_add(x, y):
    return AF(x.c + y.c, [x.a[i] + y.a[i] for i in range(S)], x.r + y.r)


def af_add_const(x, c):
    return AF(x.c + c, x.a, x.r)


def af_scale_const(x, c):
    return AF(x.c * c, [ai * c for ai in x.a], x.r * mag_ub(c))


def af_mul(x, y):
    lx, ly = l1(x.a), l1(y.a)
    return AF(
        x.c * y.c,
        [x.c * y.a[i] + y.c * x.a[i] for i in range(S)],
        lx * ly
        + mag_ub(x.c) * y.r
        + mag_ub(y.c) * x.r
        + lx * y.r
        + ly * x.r
        + x.r * y.r,
    )


def af_recip(y):
    cy_lo = mag_lb(y.c)
    rho = l1(y.a) + y.r
    if cy_lo <= ZERO_ARB or not (rho < cy_lo):
        return None, rho / cy_lo if cy_lo > ZERO_ARB else flint.arb("inf")
    q = rho / cy_lo
    invc = ONE_ACB / y.c
    return AF(
        invc,
        [-y.a[i] * invc * invc for i in range(S)],
        y.r / (cy_lo * cy_lo) + (q * q / (1 - q)) / cy_lo,
    ), q


def af_horner(coeffs, z):
    a = af_const(ZERO_ACB)
    for ck in reversed(coeffs):
        a = af_add(af_mul(a, z), ck)
    return a


def af_abs_upper(x):
    return mag_ub(x.c) + l1(x.a) + x.r


def af_abs_lower(x):
    return mag_lb(x.c) - l1(x.a) - x.r


def af_symbol_disk(slot, radius):
    """Complex disk |z|<=radius, attached to one named unit symbol.

    ACB stores rectangles, so [-radius,radius]+i[-radius,radius] is used;
    it contains the disk (and deliberately costs at most sqrt(2)).
    """
    a = list(ZERO_VECS)
    a[slot] = flint.acb(flint.arb(0, radius), flint.arb(0, radius))
    return AF(ZERO_ACB, a, ZERO_ARB)


def response(y256, y128, H, inv_x128):
    return af_mul(af_add(y256, af_scale_const(af_mul(H, y128), flint.acb(-1))), inv_x128)


# ---------------------------------------------------------------- data
lh_raw = json.load((W36 / "finish_fable" / "l_hat_fable.json").open())
LHAT = [flint.acb(flint.arb(a), flint.arb(b)) for a, b in zip(lh_raw["l_hat_re"], lh_raw["l_hat_im"])]
RHO_L = flint.arb("1.588343e-14")
LHAT_L0_DISTANCE = flint.arb("7.925e-15")
L_HEAD_RADIUS = RHO_L + LHAT_L0_DISTANCE
L_TAIL_INF = flint.arb("6.990710e-17")
LINF_L = flint.arb("1.104854250319731866")  # ||l||_inf, w36_orbitchan.md sec.6, direction-down cert
H_L1_FULL = flint.arb("6.331194")

# l(h)=1 sverka (needed for b_j=e_j-l_j*h to satisfy l(b_j)=0 exactly)
_lh_check = flint.acb(0)
for _k in range(M):
    _lh_check += LHAT[_k] * xc.tc_h[_k]
log(f"l(h) head-sum check: {_lh_check}  (must be 1 within tiny radius)")
if not (mag_ub(af_const(_lh_check - ONE_ACB).c) < flint.arb("1e-100")):
    raise RuntimeError("l(h) != 1 to required precision; b_j construction invalid")

H_INF_HEAD = flint.arb(0)
for _k in range(M):
    v = mag_ub(xc.tc_h[_k])
    if v > H_INF_HEAD:
        H_INF_HEAD = v
log(f"max_{{k<100}}|h_k| = {ub(H_INF_HEAD):.6e}")

delta_ball = flint.acb(flint.arb(xc.DELTA_pt.real.mid(), flint.arb(xc.RHO_D)))
d7inv_ball = ONE_ACB / (delta_ball**7)
DNEG7 = AF(
    flint.acb(d7inv_ball.real.mid(), d7inv_ball.imag.mid()),
    ZERO_VECS,
    flint.arb(d7inv_ball.real.rad()) + flint.arb(d7inv_ball.imag.rad()),
)
DSDU = af_scale_const(DNEG7, xc.AU0)

gf = np.array([complex(float(z.real.mid()), float(z.imag.mid())) for z in xc.tc_g])
hf = np.array([complex(float(z.real.mid()), float(z.imag.mid())) for z in xc.tc_h])
dgf = np.arange(1, M) * gf[1:]
dhf = np.arange(1, M) * hf[1:]
deltaf = float(xc.DELTA_pt.real.mid())
au0f = float(xc.AU0.real.mid())
d7f = deltaf**7


def pv(c, z):
    a = 0j
    for ck in c[::-1]:
        a = a * z + ck
    return a


def float_channels(u):
    s = u * au0f / d7f
    x = 0j
    yh = 0j
    x128 = yh128 = None
    for n in range(256):
        z = (x * x - 1.0) / 2.5
        vg, vh = pv(gf, z), pv(hf, z)
        yh = (pv(dgf, z) + s * pv(dhf, z)) * (2.0 * x / 2.5) * yh + vh
        x = vg + s * vh
        if n + 1 == 128:
            x128, yh128 = x, yh
    H = x / x128
    phih = (yh - H * yh128) / x128
    return phih


def exact_float_acb(z: complex):
    return flint.acb(flint.arb(repr(float(z.real))), flint.arb(repr(float(z.imag))))


# ---------------------------------------------------------------- worst-arc geometry (D, 32 arcs, arc 9)
key = {"A": "A", "B": "B", "C": "C", "D": "D", "N": "new"}[TOOTH]
r0, arg0 = xc.TEETH_NEW[key]
u0c = r0 * complex(math.cos(arg0), math.sin(arg0))
th_lo = 2.0 * math.pi * ARC_IDX / N_ARCS
th_hi = 2.0 * math.pi * (ARC_IDX + 1) / N_ARCS
th_mid = 0.5 * (th_lo + th_hi)
rho_arc = 2.0 * R_CONTOUR * math.sin((th_hi - th_lo) / 4.0) * (1.0 + 1e-9) + FAT
umc = u0c + R_CONTOUR * complex(math.cos(th_mid), math.sin(th_mid))
um = flint.acb(repr(umc.real), repr(umc.imag))
ph_center = float_channels(umc)
c_fixed = exact_float_acb(ph_center)
log(f"arc geometry: u_mid={umc}, rho={rho_arc!r}, c={ph_center}")


# ---------------------------------------------------------------- build G1/H1/DG1/DH1 for given symbol setup
def bnorm1(j):
    """||b_j||_1 (head part k<100); tail part of b_j (k>=100) contributes at
    most |l_j|*sum_{k>=100}|h_k| <= L_TAIL_INF-scale*CL-34 h-tail, negligible
    (Taylor h-tail certified <= 2.025e-30 by cl34_certificate.json)."""
    lj = LHAT[j]
    s = flint.arb(0)
    for k in range(M):
        base_kj = ONE_ACB if k == j else ZERO_ACB
        s += mag_ub(base_kj - lj * xc.tc_h[k])
    return s


def build_inputs(dom_modes, dom_budget, extra_r_head):
    """dom_modes: list of head indices j (0<=j<100) chosen as named symbols.
    dom_budget: matching list of L1-BUDGETS w_budget_j (contribution to ||v||_1),
    symbol i+1 <-> dom_modes[i]. Actual coefficient bound is
    |c_j| <= w_budget_j/||b_j||_1 so that |c_j|*||b_j||_1 <= w_budget_j exactly
    (||b_j||_1 for low j is NOT ~1 -- e.g. ||b_0||_1~8 -- so this normalization
    is required, not optional; caught by the R_n>=1 blowup on the first
    unnormalized attempt, see worklog).
    extra_r_head: flint.arb scalar radius added (per-coefficient, uniformly) to
    every G1[k]/DG1 to cover non-dominant head modes' worst-case l1 contribution.
    """
    assert len(dom_modes) == len(dom_budget) == K_DOM
    # b_j[k] = delta_{jk} - l_j*h_k ; symbol slot (1+i) carries c_i*b_{j_i}[k]
    # with c_i = w_budget_i / ||b_{j_i}||_1
    bcoef = {}  # (i,k) -> acb value = c_i * b_{j_i}[k]
    dom_cbound = []
    for i, (j, wbudget) in enumerate(zip(dom_modes, dom_budget)):
        lj = LHAT[j]
        bn = bnorm1(j)
        cbound = wbudget / bn
        dom_cbound.append(cbound)
        cacb = flint.acb(cbound)
        for k in range(M):
            base = ONE_ACB if k == j else ZERO_ACB
            bjk = base - lj * xc.tc_h[k]
            bcoef[(i, k)] = cacb * bjk

    G1 = []
    for k in range(M):
        a = list(ZERO_VECS)
        for i in range(K_DOM):
            a[1 + i] = bcoef[(i, k)]
        r = flint.arb(xc.RHO_G) + extra_r_head
        G1.append(AF(xc.tc_g[k], a, r))

    DG1 = []
    for k in range(1, M):
        a = list(ZERO_VECS)
        kacb = flint.acb(k)
        for i in range(K_DOM):
            a[1 + i] = kacb * bcoef[(i, k)]
        r = flint.arb(k) * (flint.arb(xc.RHO_G) + extra_r_head)
        DG1.append(AF(kacb * xc.tc_g[k], a, r))

    H1 = [AF(xc.tc_h[k], ZERO_VECS, flint.arb(xc.RHO_H)) for k in range(M)]
    DH1 = [AF(flint.acb(k) * xc.tc_h[k], ZERO_VECS, flint.arb(k) * flint.arb(xc.RHO_H)) for k in range(1, M)]
    return G1, H1, DG1, DH1, dom_cbound


def compute_arc(G1, H1, DG1, DH1, u_mid, rho, c_fixed_local,
                tail_budget=flint.arb(0)):
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
    max_tail_value = flint.arb(0)
    max_tail_derivative = flint.arb(0)
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
        if INJECT_TAIL and tail_budget > 0:
            # q(z)=sum_{j>=M} v_j (z^j-l_j h(z)), sum|v_j|<=tail_budget.
            # The geometric derivative sum is an explicit (conservative)
            # envelope for sup_{j>=M} j*r^(j-1); no finite tail cutoff occurs.
            tail_value_bound = tail_budget * (
                rz**M + L_TAIL_INF * af_abs_upper(vh)
            )
            tail_deriv_geom = (
                flint.arb(M) * rz**(M-1) - flint.arb(M-1) * rz**M
            ) / ((1-rz)*(1-rz))
            tail_derivative_bound = tail_budget * (
                tail_deriv_geom + L_TAIL_INF * af_abs_upper(vhp)
            )
            vg = af_add(vg, af_symbol_disk(TAIL_SLOT, tail_value_bound))
            vgp = af_add(vgp, af_symbol_disk(TAIL_SLOT, tail_derivative_bound))
            if tail_value_bound > max_tail_value:
                max_tail_value = tail_value_bound
            if tail_derivative_bound > max_tail_derivative:
                max_tail_derivative = tail_derivative_bound
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
        yh_new = af_add(
            af_mul(fpw, af_scale_const(af_mul(x, yh), TWO_OVER_R)),
            vh,
        )
        x_new = af_add(vg, af_mul(vh, s))

        tail_source = (rz**M) / (1 - rz)
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
    head_values = []
    head_best = flint.arb(0)
    head_argmax = -1
    for k in range(M):
        v = af_add(psi[k], af_scale_const(dhc, LHAT[k]))
        uval = af_abs_upper(v) + c_abs * L_HEAD_RADIUS
        head_values.append((uval, v))
        if uval > head_best:
            head_best, head_argmax = uval, k

    den_lo = af_abs_lower(x128)
    if not (den_lo > 0):
        raise RuntimeError(f"nonpositive lower |x128|: {den_lo}")
    tail_phi = tail_q / den_lo + af_abs_upper(x) * tail_q128 / (den_lo * den_lo)
    tail_l = c_abs * L_TAIL_INF
    tail_total = tail_phi + tail_l
    total = max(head_best, tail_total)
    return {
        "total": total,
        "head": head_best,
        "head_argmax": head_argmax,
        "head_values": head_values,
        "tail_phi_sum": tail_phi,
        "tail_l": tail_l,
        "tail_total": tail_total,
        "Rmax": max_r,
        "fxmax": max_fx,
        "x128_lower": den_lo,
        "recip_q": q_recip,
        "phih": phih,
        "phih_upper": af_abs_upper(phih),
        "tail_symbol_budget": tail_budget,
        "tail_symbol_value_max": max_tail_value,
        "tail_symbol_derivative_max": max_tail_derivative,
    }


# ---------------------------------------------------------------- main
if MODE == "base":
    G1, H1, DG1, DH1, _ = build_inputs([], [], flint.arb(0))
    t_a = time.time()
    out = compute_arc(G1, H1, DG1, DH1, um, flint.arb(repr(rho_arc)), c_fixed,
                      flint.arb(0))
    log(f"baseline arc computed in {time.time()-t_a:.2f}s")
    log(f"N_s_base <= {ub(out['total']):.12e}  (JSON reference: 146981.6673903488)")
    log(f"head_argmax={out['head_argmax']}  phih_upper={ub(out['phih_upper']):.12e} (JSON reference: 1561536.113574741)")
    log(f"Rmax<={ub(out['Rmax']):.12f}  x128_lower={lb(out['x128_lower']):.12e}")
    log(f"tail_total<={ub(out['tail_total']):.6e}")

    head_sorted = sorted(range(M), key=lambda k: ub(out["head_values"][k][0]), reverse=True)
    log("top-25 head modes by response magnitude (k, |dF[b_k]| upper):")
    for k in head_sorted[:25]:
        log(f"  k={k:3d}  |dF[b_k]|<={ub(out['head_values'][k][0]):.6e}")

    result = {
        "mode": "base",
        "N_s_base_upper": ub(out["total"]),
        "head_argmax": out["head_argmax"],
        "phih_upper": ub(out["phih_upper"]),
        "Rmax_upper": ub(out["Rmax"]),
        "x128_lower": lb(out["x128_lower"]),
        "tail_total_upper": ub(out["tail_total"]),
        "head_values_upper": [ub(out["head_values"][k][0]) for k in range(M)],
        "head_values_r": [ub(out["head_values"][k][1].r) for k in range(M)],
        "head_sorted_desc": head_sorted,
        "time_s": time.time() - T0,
    }
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"RESULT written to {JSON_PATH.name}")

else:  # tube
    base_json = HERE / f"cert_slice_{RUN_LABEL}{'outerbox_' if OUTER_BOX else ''}base_K0_{TOOTH}{N_ARCS}a{ARC_IDX}.json"
    if not base_json.exists():
        raise SystemExit("run 'python cert_slice.py base' first")
    base = json.load(base_json.open())
    dom_modes = base["head_sorted_desc"][:K_DOM]
    rest_modes = base["head_sorted_desc"][K_DOM:]
    log(f"named modes (top {K_DOM} by base response): {dom_modes[:10]}{'...' if K_DOM > 10 else ''}")

    if not rest_modes:
        # K_DOM==100: EVERY head coefficient is a named symbol (elegant fix for
        # the scalar-remainder blowup found below -- see worklog milestone 2:
        # a uniform scalar ball on G1, even at ~1e-11 magnitude (0.002% of r_s),
        # reproduces the disk-death mechanism (kappa scales ~linearly with the
        # ball up to ~1e-12, then super-linearly, domain failure by ~1e-8).
        # Since naming costs little (S=101 vs S=21, seconds not minutes), the
        # fix is: name everything representable (all 100 head coefficients),
        # leave ONLY the structurally-unrepresentable j>=100 tail to the
        # analytic R<=0.403 majorant (it cannot be fed to G1 at all: G1 has
        # exactly 100 slots).
        W_DOM_TOTAL = flint.arb("0.999") * R_S
        W_HEAD_REST = flint.arb(0)
        W_TAIL = R_S if (OUTER_BOX and INJECT_TAIL) else flint.arb("0.001") * R_S
        extra_r_head = flint.arb(0)
        bmin_rest = None
    else:
        W_DOM_TOTAL = flint.arb("0.90") * R_S
        W_HEAD_REST = flint.arb("0.08") * R_S
        W_TAIL = flint.arb("0.02") * R_S
        # rest-bucket normalization: worst-case ratio sup_{j in rest}[(1+||l||_inf*max|h_k|)/||b_j||_1]
        bmin_rest = None
        for j in rest_modes:
            bn = bnorm1(j)
            if bmin_rest is None or bn < bmin_rest:
                bmin_rest = bn
        ratio_rest = (flint.arb(1) + LINF_L * H_INF_HEAD) / bmin_rest
        extra_r_head = W_HEAD_REST * ratio_rest
        log(f"rest bucket: min_{{j in rest}}||b_j||_1 <= {ub(bmin_rest):.6e} (worst-case denominator), "
            f"ratio<={ub(ratio_rest):.6e} -> extra_r_head={ub(extra_r_head):.6e} (added to EVERY G1[k].r)")

    # Outer-cover mode: for v=sum_j v_j b_j with ||v||_1<=r_s one has
    # |v_j|<=r_s.  Hence EVERY coordinate must receive r_s/||b_j||_1,
    # represented here by the l1 contribution budget r_s.  The old equal
    # split W_DOM_TOTAL/K_DOM was an inner cross-polytope, not an outer box.
    dom_budget_each = R_S if OUTER_BOX else W_DOM_TOTAL / K_DOM
    dom_budgets = [dom_budget_each] * K_DOM
    if OUTER_BOX:
        log(f"OUTER BOX enabled: every named coordinate receives full l1 budget r_s={ub(R_S):.6e}; "
            f"box l1 envelope={ub(R_S*K_DOM):.6e}")

    # ||b_j||_1 for named modes (needed for normalization |c_j|=budget/||b_j||_1)
    bnorms_dom = {j: bnorm1(j) for j in dom_modes}
    for j in dom_modes[:5] + dom_modes[-5:]:
        log(f"  ||b_{j}||_1 (head part) <= {ub(bnorms_dom[j]):.6e}  ->  |c_{j}|<={ub(dom_budget_each/bnorms_dom[j]):.6e}")

    log(f"weights: W_dom_total={ub(W_DOM_TOTAL):.6e} (budget {ub(dom_budget_each):.6e} x{K_DOM}), "
        f"W_head_rest={ub(W_HEAD_REST):.6e}, W_tail={ub(W_TAIL):.6e} "
        f"({'injected named symbol' if INJECT_TAIL else 'NOT injected'})")
    if OUTER_BOX:
        log("outer-cover check: each head coordinate and the aggregate l1 tail receive the full r_s; no inner-simplex weight sum is used")
    else:
        log(f"weight sum check: {ub(W_DOM_TOTAL + W_HEAD_REST + W_TAIL):.6e} vs r_s={ub(R_S):.6e}")

    if DIAG == "noRest":
        log("DIAG noRest: forcing extra_r_head=0 (isolate dominant-symbol effect)")
        extra_r_head = flint.arb(0)
    elif DIAG == "restOnly":
        log("DIAG restOnly: forcing dom_budgets=0 (isolate extra_r_head effect)")
        dom_budgets = [flint.arb(0)] * K_DOM
    elif DIAG == "dom1":
        log("DIAG dom1: only symbol 0 (k=0) active, full dom budget on it, extra_r_head=0")
        dom_budgets = [W_DOM_TOTAL] + [flint.arb(0)] * (K_DOM - 1)
        extra_r_head = flint.arb(0)
    elif DIAG.startswith("restMag:"):
        mag = flint.arb(DIAG.split(":", 1)[1])
        log(f"DIAG restMag: dom_budgets=0, extra_r_head forced to {ub(mag):.6e}")
        dom_budgets = [flint.arb(0)] * K_DOM
        extra_r_head = mag
    elif DIAG.startswith("scale:"):
        fac = flint.arb(DIAG.split(":", 1)[1])
        log(f"DIAG scale: multiplying all eps budgets by {ub(fac):.6e} (r_delta scaling test)")
        dom_budgets = [b * fac for b in dom_budgets]
        extra_r_head = extra_r_head * fac

    G1, H1, DG1, DH1, dom_cbound = build_inputs(dom_modes, dom_budgets, extra_r_head)
    log(f"actual |c_j| bounds used (dominant, first 5): {[f'{ub(c):.4e}' for c in dom_cbound[:5]]}")
    rho_used = flint.arb(0) if DIAG == "rho0" else flint.arb(repr(rho_arc))
    if DIAG == "rho0":
        log("DIAG rho0: u-disk radius forced to 0 (isolate pure eps-eps term from u x eps mixing)")
    t_a = time.time()
    # If sum |c_j|*||b_j||_1 <= r_s in the slice basis, then for j>=100,
    # ||b_j||_1 >= 1-|l_j|*||h||_1 >= 1-L_TAIL_INF*H_L1_FULL.  This converts
    # the weighted tail budget to the coefficient-l1 budget used in q(z).
    tail_coeff_budget = W_TAIL / (1 - L_TAIL_INF * H_L1_FULL)
    out = compute_arc(G1, H1, DG1, DH1, um, rho_used, c_fixed,
                      tail_coeff_budget if INJECT_TAIL else flint.arb(0))
    log(f"tube arc computed in {time.time()-t_a:.2f}s")

    N_s_tube = ub(out["total"])
    phih_tube = ub(out["phih_upper"])
    log(f"N_s_tube <= {N_s_tube:.12e}   (base {base['N_s_base_upper']:.12e})")
    log(f"phih_tube(U proxy) <= {phih_tube:.12e}   (base {base['phih_upper']:.12e})")
    log(f"tube head_argmax = {out['head_argmax']}  (base head_argmax = {base['head_argmax']})")

    kappa_Ns = N_s_tube / base["N_s_base_upper"] - 1.0
    kappa_U = phih_tube / base["phih_upper"] - 1.0
    kappa_D = max(kappa_Ns, kappa_U)
    log(f"kappa_Ns = {kappa_Ns:.6e}   kappa_U = {kappa_U:.6e}   kappa_D = {kappa_D:.6e}")

    # linear vs quadratic split at the tube's argmax head index
    k_star = out["head_argmax"]
    uval_star, v_star = out["head_values"][k_star]
    eps_linear_l1 = flint.arb(0)
    for i in range(1, S):
        eps_linear_l1 += mag_ub(v_star.a[i])
    r_tube_star = v_star.r
    r_base_star = base["head_values_r"][k_star]
    r_delta_star = ub(r_tube_star) - r_base_star  # extra remainder (quadratic wraparound) contributed by tube ext.
    quad_over_linear = r_delta_star / ub(eps_linear_l1) if ub(eps_linear_l1) > 0 else float("inf")
    log(f"k_star={k_star}: eps-linear l1 <= {ub(eps_linear_l1):.6e}; "
        f"AF remainder r: base={r_base_star:.6e} -> tube={ub(r_tube_star):.6e} "
        f"(delta/quadratic part <= {r_delta_star:.6e}); quad/linear ratio <= {quad_over_linear:.6e}")

    # cross-check: also evaluate the split at k=0 (global head_argmax in both runs, by construction)
    result = {
        "mode": "tube",
        "outer_box": OUTER_BOX,
        "coverage_statement": ("head coordinate box plus aggregate tail symbol contains every slice vector with basis l1 norm <= r_s"
                               if OUTER_BOX and INJECT_TAIL else
                               "contains every 100-mode slice vector with l1 norm <= r_s"
                               if OUTER_BOX else "legacy inner coordinate box"),
        "tail_symbol_injected": INJECT_TAIL,
        "tail_coverage_statement": ("one named complex disk symbol covers every l1 tail supported in j>=100"
                                     if INJECT_TAIL else "tail not injected"),
        "K_DOM": K_DOM,
        "dom_modes": dom_modes,
        "dom_budget_each": ub(dom_budget_each),
        "dom_cbound_first5": [ub(c) for c in dom_cbound[:5]],
        "dom_cbound_last5": [ub(c) for c in dom_cbound[-5:]],
        "W_dom_total": ub(W_DOM_TOTAL),
        "W_head_rest": ub(W_HEAD_REST),
        "extra_r_head": ub(extra_r_head),
        "bmin_rest": (ub(bmin_rest) if bmin_rest is not None else None),
        "W_tail": ub(W_TAIL),
        "tail_coeff_l1_budget": ub(tail_coeff_budget),
        "tail_basis_norm_lower": lb(1 - L_TAIL_INF * H_L1_FULL),
        "tail_symbol_value_max": ub(out["tail_symbol_value_max"]),
        "tail_symbol_derivative_max": ub(out["tail_symbol_derivative_max"]),
        "r_s": ub(R_S),
        "N_s_base_upper": base["N_s_base_upper"],
        "N_s_tube_upper": N_s_tube,
        "phih_base_upper": base["phih_upper"],
        "phih_tube_upper": phih_tube,
        "kappa_Ns": kappa_Ns,
        "kappa_U": kappa_U,
        "kappa_D": kappa_D,
        "k_star": k_star,
        "eps_linear_l1_at_kstar": ub(eps_linear_l1),
        "r_remainder_tube_at_kstar": ub(r_tube_star),
        "r_remainder_base_at_kstar": r_base_star,
        "r_remainder_delta_at_kstar": r_delta_star,
        "quad_over_linear_at_kstar": quad_over_linear,
        "Rmax_upper": ub(out["Rmax"]),
        "x128_lower": lb(out["x128_lower"]),
        "recip_q_upper": ub(out["recip_q"]),
        "time_s": time.time() - T0,
    }
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log(f"RESULT written to {JSON_PATH.name}")

LOGF.close()
