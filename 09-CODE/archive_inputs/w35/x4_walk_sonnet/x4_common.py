# -*- coding: utf-8 -*-
"""
w35/X4 -- shared affine-arithmetic machine for the m=8,9,10 unconditional
walk with the NEW (wave 34) certificate and the CORRECTED AU0.

REUSE POLICY (per brief: "importировать, не переписывать"): the AF class and
all af_* primitives (af_mul/af_add/af_horner/af_recip/leg_analysis/
delta_af_negm/orb_leg_affine-style loops) are copied VERBATIM from
w31/w31_uncond_common.py (same file wave 32/33/34 all reused the same way,
since it is a monolithic script, not an importable library -- "import by
copying and re-parametrizing" is the established project convention, see
w34/w1_cert/w1_uncond_common_M99.py's own docstring for the same argument).
Only the module-level CONSTANTS differ from w31_uncond_common.py:

  1. DATA_PATH -> w33/t5_cert_sonnet/w33_gh_hiprec.json (M=100 coefficients,
     same file w34/W1 used to rebuild the certificate) instead of the old
     45-coefficient w12_gh.json.
  2. AU0 -> CORRECTED value 0.41403799908627305889537448439555967803329915886199
     (w34/W5, three independent methods, 16-17 digit agreement) instead of
     the wrong 0.414038052831 that w34/w1_cert's OWN w1_uncond_common_M99.py
     still carries (verified by reading that file directly -- it was not
     fixed there because W1 and W5 were parallel, independent wave-34 tasks).
     THIS is the single most important correction this task must not skip.
  3. RHO_G/RHO_H/RHO_D -> the NEW certificate from w34/w1_cert
     (rho_G=1e-20, rho_H=1e-27, rho_D=1e-27 -- rho_D structurally equal to
     rho_H per w34/W1's fix of the old, disconnected rho_D=1e-7).
  4. TEETH_NEW -> the wave-34/W5 updated catalog coordinates (u-units,
     modulus@phase radians), each good to 8-11 digits per w34/w5_catalog_sonnet.
     TEETH_OLD is kept alongside for the brief's explicit item-5 sanity
     check (old coords + old AU0 vs new coords + new AU0 on one tooth).

PREC = 512 bits, matching w34/w1_cert (M=100 data needs more working
precision than the old M=44 setup; w34's own rounding channel stayed at
~1e-143, far below every other channel, confirming 512 bits has ample
headroom even at the deeper orbit lengths this task pushes to).
"""
import os
import json
import math
import flint
from decimal import Decimal
from fractions import Fraction

PREC = int(os.environ.get('X4_PREC', '512'))
flint.ctx.prec = PREC

BASE = 'D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive/'
DATA_PATH = BASE + 'w33/t5_cert_sonnet/w33_gh_hiprec.json'
D = json.load(open(DATA_PATH))


def dec_fmpq(s):
    fr = Fraction(Decimal(str(s)))
    return flint.fmpq(fr.numerator, fr.denominator)


def fmpq_arb(q):
    return flint.arb(flint.fmpz(q.p)) / flint.fmpz(q.q)


g_arb = [flint.arb(s) for s in D['g_str']]
h_arb = [flint.arb(s) for s in D['h_str']]
N_full = len(g_arb)
M = N_full          # 100
r_disc = flint.arb('2.5')

tcoeff = [[flint.arb(0)] * (N_full + 1) for _ in range(N_full)]
tcoeff[0][0] = flint.arb(1)
if N_full >= 2:
    tcoeff[1][1] = flint.arb(1)
for n in range(2, N_full):
    for j in range(n + 1):
        val = flint.arb(0)
        if j > 0:
            val += 2 * tcoeff[n - 1][j - 1]
        if j <= n - 2:
            val -= tcoeff[n - 2][j]
        tcoeff[n][j] = val


def cheb_to_taylor(arb_arr):
    taylor = []
    for j in range(N_full):
        s = flint.arb(0)
        for k in range(j, N_full):
            s += arb_arr[k] * tcoeff[k][j] * (r_disc ** j)
        taylor.append(s)
    return taylor


tc_g = [flint.acb(c) for c in cheb_to_taylor(g_arb)]
tc_h = [flint.acb(c) for c in cheb_to_taylor(h_arb)]

DELTA_pt = flint.acb(fmpq_arb(dec_fmpq(str(D['delta_rayleigh']))))

# --- THE FIX: corrected AU0 (w34/W5), NOT the old 0.414038052831 ---------
AU0_NEW_STR = '0.41403799908627305889537448439555967803329915886199'
AU0_OLD_STR = '0.414038052831'
AU0 = flint.acb(fmpq_arb(dec_fmpq(AU0_NEW_STR)))
AU0_OLD = flint.acb(fmpq_arb(dec_fmpq(AU0_OLD_STR)))

# --- THE NEW CERTIFICATE (w34/w1_cert) -----------------------------------
RHO_G = float(os.environ.get('X4_RHO_G', '1e-20'))
RHO_H = float(os.environ.get('X4_RHO_H', '1e-27'))
RHO_D = float(os.environ.get('X4_RHO_D', '1e-27'))

K = 2 * M + 2
IDX_DELTA = 2 * M
IDX_U = 2 * M + 1

ZERO_ACB = flint.acb(0)
ZERO_ARB = flint.arb(0)
ZERO_VEC = [ZERO_ACB] * K


def mag_ub(z):
    return z.abs_upper()


def mag_lb(z):
    return z.abs_lower()


class AF:
    __slots__ = ('c', 'a', 'r')

    def __init__(self, c, a=None, r=None):
        self.c = c
        self.a = a if a is not None else ZERO_VEC
        self.r = r if r is not None else ZERO_ARB


def l1(vec):
    s = ZERO_ARB
    for v in vec:
        s = s + mag_ub(v)
    return s


def af_const(c):
    return AF(c, ZERO_VEC, ZERO_ARB)


def af_add(x, y):
    return AF(x.c + y.c, [x.a[i] + y.a[i] for i in range(K)], x.r + y.r)


def af_add_const(x, k):
    return AF(x.c + k, x.a, x.r)


def af_scale_const(x, k):
    return AF(x.c * k, [ai * k for ai in x.a], x.r * mag_ub(k))


def af_mul(x, y):
    C = x.c * y.c
    A = [x.c * y.a[i] + y.c * x.a[i] for i in range(K)]
    L1x = l1(x.a)
    L1y = l1(y.a)
    R = (L1x * L1y
         + mag_ub(x.c) * y.r + mag_ub(y.c) * x.r
         + L1x * y.r + L1y * x.r
         + x.r * y.r)
    return AF(C, A, R)


def af_recip(y):
    cy_lo = mag_lb(y.c)
    rho_y = l1(y.a) + y.r
    if cy_lo <= ZERO_ARB or not (rho_y < cy_lo):
        return None, (rho_y / cy_lo if cy_lo > ZERO_ARB else flint.arb('inf'))
    q = rho_y / cy_lo
    inv_cy = flint.acb(1) / y.c
    C = inv_cy
    A = [-(y.a[i]) * inv_cy * inv_cy for i in range(K)]
    term1 = y.r / (cy_lo * cy_lo)
    term2 = (q * q / (1 - q)) / cy_lo
    R = term1 + term2
    return AF(C, A, R), q


def af_pow_int(x, n):
    result = x
    for _ in range(n - 1):
        result = af_mul(result, x)
    return result


def af_horner(coeffs_af, w_af):
    n = len(coeffs_af)
    b = af_const(ZERO_ACB)
    for k in range(n - 1, -1, -1):
        b = af_mul(b, w_af)
        b = af_add(b, coeffs_af[k])
    return b


def c_rad(z):
    return flint.arb(z.real.rad()) + flint.arb(z.imag.rad())


def _build_gh_inputs():
    g_af = []
    for k in range(M):
        a = [ZERO_ACB] * K
        a[k] = flint.acb(RHO_G)
        g_af.append(AF(tc_g[k], a, ZERO_ARB))
    h_af = []
    for k in range(M):
        a = [ZERO_ACB] * K
        a[M + k] = flint.acb(RHO_H)
        h_af.append(AF(tc_h[k], a, ZERO_ARB))
    return g_af, h_af


_G_AF, _H_AF = _build_gh_inputs()


def leg_analysis(x_af):
    """(cabs, total_rad, details) -- details = (g,h,d,u,r,rnd,cabs,rel)."""
    max_g = ZERO_ARB
    for k in range(M):
        v = mag_ub(x_af.a[k])
        if v > max_g:
            max_g = v
    max_h = ZERO_ARB
    for k in range(M, 2 * M):
        v = mag_ub(x_af.a[k])
        if v > max_h:
            max_h = v
    mag_d = mag_ub(x_af.a[IDX_DELTA])
    mag_u = mag_ub(x_af.a[IDX_U])
    r = x_af.r
    cabs = math.hypot(float(x_af.c.real.mid()), float(x_af.c.imag.mid()))
    cres = float(c_rad(x_af.c))
    total = max_g + max_h + mag_d + mag_u + r + cres
    gs = float(max_g); hs = float(max_h); ds = float(mag_d); us = float(mag_u); rs = float(r)
    if cabs > 0:
        rel = float(total) / cabs
    else:
        rel = float('inf')
    return cabs, total, (gs, hs, ds, us, rs, cres, cabs, rel)


_delta_af_cache = {}


def delta_af_negm(m):
    if m in _delta_af_cache:
        return _delta_af_cache[m]
    delta_af = AF(DELTA_pt, [(flint.acb(RHO_D) if i == IDX_DELTA else ZERO_ACB) for i in range(K)], ZERO_ARB)
    dm = af_pow_int(delta_af, m)
    dneg, q = af_recip(dm)
    if dneg is None:
        raise RuntimeError('delta(-m) reciprocal failed, q=%s' % q)
    _delta_af_cache[m] = (dneg, float(q))
    return _delta_af_cache[m]


def cabs(z):
    return math.hypot(float(z.real.mid()), float(z.imag.mid()))


# --- catalog: NEW (wave 34/W5) and OLD (pre-w34) tooth coordinates -------
TEETH_NEW = {
    'A':   (8.270999733, 1.381846811),
    'B':   (7.340479780, 0.655780025),
    'C':   (11.013820661, 0.106204238),
    'D':   (11.471516303, 0.370552201),
    'new': (7.534878921, 0.843173982),
}
TEETH_OLD = {
    'A':   (8.2709998, 1.38184683),
    'B':   (7.3404799, 0.65578004),
    'C':   (11.0138211, 0.10620424),
    'D':   (11.4715167, 0.37055221),
    'new': (7.534880, 0.8431741),
}


def u_center(r, arg):
    return flint.acb(r * math.cos(arg), r * math.sin(arg))


# --- point-evaluation orbit (plain acb, no affine bookkeeping) -----------
def H_point(u_val, m, au0=None):
    """Plain (non-affine) point value H_m(u) = x_{2^(m+1)}/x_{2^m} at the
    NEW 100-coeff center coefficients. au0 overrides AU0 (for the old/new
    AU0 sanity check)."""
    au0 = AU0 if au0 is None else au0
    s = u_val * au0 / (DELTA_pt ** m)
    x = flint.acb(0)
    xden = None
    lev_num = 2 ** (m + 1)
    lev_den = 2 ** m
    for n in range(lev_num):
        xx = x * x - flint.acb(1)
        w = xx / r_disc
        vg = flint.acb(0)
        for k in range(M - 1, -1, -1):
            vg = vg * w + tc_g[k]
        vh = flint.acb(0)
        for k in range(M - 1, -1, -1):
            vh = vh * w + tc_h[k]
        x = vg + s * vh
        if n + 1 == lev_den:
            xden = x
    return x / xden


# --- affine (rigorous) orbit: numerator+denominator share one loop -------
def compute_H_af_point(u_val, m):
    """AF enclosure of H_m(u) = x_{2^(m+1)}/x_{2^m} at an EXACT point u
    (chord_half=0, no arc-width channel) but full (g,h,delta) certified-ball
    uncertainty. Cost: 2^(m+1) affine steps (num and den share one loop, den
    captured in-flight at level 2^m, exactly as w34/w1_cert's compute_H_af)."""
    dneg, q_delta = delta_af_negm(m)
    s_af = af_mul(af_scale_const(dneg, AU0), AF(u_val, ZERO_VEC, ZERO_ARB))
    lev_den = 2 ** m
    lev_num = 2 ** (m + 1)
    x = af_const(ZERO_ACB)
    x_den = None
    for n in range(lev_num):
        xx = af_add_const(af_mul(x, x), flint.acb(-1))
        w = af_scale_const(xx, flint.acb(1) / r_disc)
        vg = af_horner(_G_AF, w)
        vh = af_horner(_H_AF, w)
        x = af_add(vg, af_mul(vh, s_af))
        if n + 1 == lev_den:
            x_den = x
    inv, q = af_recip(x_den)
    if inv is None:
        return None, q
    return af_mul(x, inv), q


def compute_H_af_arc(u_mid, chord_half, m):
    """AF enclosure of H_m over the arc-disk(u_mid, chord_half) -- u carried
    as the IDX_U-th affine symbol with radius = exact half-chord (same trick
    as w31_uncond_common.py / w32/a3_new_tooth_arcs.py), full (g,h,delta)
    certified-ball uncertainty simultaneously. Cost: 2^(m+1) affine steps."""
    dneg, q_delta = delta_af_negm(m)
    u_af = AF(u_mid, [(flint.acb(chord_half) if i == IDX_U else ZERO_ACB) for i in range(K)], ZERO_ARB)
    s_af = af_mul(af_scale_const(dneg, AU0), u_af)
    lev_den = 2 ** m
    lev_num = 2 ** (m + 1)
    x = af_const(ZERO_ACB)
    x_den = None
    for n in range(lev_num):
        xx = af_add_const(af_mul(x, x), flint.acb(-1))
        w = af_scale_const(xx, flint.acb(1) / r_disc)
        vg = af_horner(_G_AF, w)
        vh = af_horner(_H_AF, w)
        x = af_add(vg, af_mul(vh, s_af))
        if n + 1 == lev_den:
            x_den = x
    inv, q = af_recip(x_den)
    if inv is None:
        return None, q
    return af_mul(x, inv), q


def diff_af(H_hi, H_lo):
    diff_c = H_hi.c - H_lo.c
    diff_a = [H_hi.a[i] - H_lo.a[i] for i in range(K)]
    diff_r = H_hi.r + H_lo.r
    return AF(diff_c, diff_a, diff_r)
