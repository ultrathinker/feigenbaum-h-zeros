# -*- coding: utf-8 -*-
"""level_tail_certificate_strict.py -- regenerate the analytic all-level
certificate for w, D, e and the Duhamel tails at 512 bits (directed rounding)
using the STRICT values of ||DT(G)||_1 = nDT and ||DT(G)^2||_1 = nDT2, and the
denominator/numerator delta split (BRIEF 3.3 a, v).

This is the package counterpart of the frozen
w36/audit_codex/level_tail_certificate.py. It produces
level_tail_certificate_strict.json with the SAME field structure so the two can
be diffed (see DELTA_FROZEN.md). The frozen file is READ-ONLY and is reproduced
verbatim in DATA/inputs/ for that diff.

Every arithmetic input is an Arb upper bound (RECERT/g_verify.py certifies the
literals; nDT/nDT2 come from the strict ndt_rigorous.json). We rely on Arb's
directed rounding: every `.upper()` is a rigorous ceiling.
"""
import json
import sys
from pathlib import Path

import flint
from flint import arb, ctx

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _constants as C  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import _log  # noqa: E402

ctx.prec = 512
HERE = Path(__file__).resolve().parent

_log.log("CERT level_tail_strict START (Arb %d bits)" % ctx.prec)


def up(x):
    return x.upper()


def us(x):
    return str(up(x))


# -- delta split literals (denominators: delta_lo ; numerators: delta_hi) ---
d2 = C.d2()
d4 = C.d4()
s8 = C.s8()
sp = C.sp()
delta_lo = C.DELTA_LO
delta_hi = C.DELTA_HI

K = C.K
nh = C.NH
nDT = C.NDT_STRICT          # strict
nDT2 = C.NDT2_STRICT        # strict
q2 = C.Q2
rho = C.RHO
linf = C.LINF
pperp = C.PPERP
Cs = C.CS
mu = C.MU
t = C.T
C0 = C.C0
C1 = C.C1
M3 = C.M3_CHOSEN

_log.log("CERT level_tail_strict inputs: nDT=%s nDT2=%s" % (us(nDT)[:24], us(nDT2)[:26]))

# ============================================================================
# Lemma W.  At pair boundaries w<=C0*s^2; at the intermediate step w<=C1*s^2.
# A pair can only start with s<=s8/delta.  delta*nh is a NUMERATOR -> delta_hi.
# ============================================================================
first_single_coeff = (K * nh ** 2 / 2) / d2
c1_unscaled = nDT * C0 + K * (nh + C0 * sp) ** 2 / 2
one_coeff = (nDT * C0 + K * (nh + C0 * sp) ** 2 / 2) / d2
pair_coeff = (nDT2 * C0 + nDT * K * (nh + C0 * sp) ** 2 / 2
              + K * (C.delta_nh() + c1_unscaled * sp) ** 2 / 2) / d4
w_invariant = (up(first_single_coeff) <= C0 and up(one_coeff) <= C1
               and up(pair_coeff) <= C0)
_log.log("CERT level_tail_strict Lemma W: first<=%s one<=%s pair<=%s pass=%s"
         % (us(first_single_coeff)[:16], us(one_coeff)[:20], us(pair_coeff)[:16], w_invariant))

# With C1 valid at every step, Q_j<=QCOEF*s_j^2.  Infinite Duhamel series.
QCOEF = (q2 + K * nh * C1 * s8 + K * C1 ** 2 * s8 ** 2 / 2
         + M3 * (nh + C1 * s8) ** 3 * s8 / 6)
ratioP = mu / d2
kernel_sum = pperp + Cs * ratioP / (1 - ratioP)
P_ALL = QCOEF * s8 ** 2 * kernel_sum
P_TARGET = arb("3e-7")
_log.log("CERT level_tail_strict Duhamel: QCOEF<=%s P_ALL<=%s pass=%s"
         % (us(QCOEF)[:18], us(P_ALL)[:20], bool(up(P_ALL) <= P_TARGET)))

# ============================================================================
# Lemma DE.  Same-parity level increments: V_{n+2} <= B V_n, B=[[q,0],[c,p]].
# L1,L2 use the STRICT nDT/nDT2.  q=L2/d4, p=1/d2 are denominators (delta_lo);
# the delta multipliers inside exit_de are numerators (delta_hi).
# ============================================================================
L1 = nDT + K * rho
L2 = nDT2 + 2 * nDT * K * rho + (K * rho) ** 2
lKrh = linf * K * rho
q = L2 / d4
p = 1 / d2
c = lKrh * (delta_hi + L1) / d4


def Phi(s):
    return q2 * s * s + M3 * nh ** 3 * s ** 3 / 6


def exit_de(k):
    """(D,e) recursion, delta_hi for the delta multipliers, delta_lo for s."""
    n = k - 7
    s = t / (delta_lo ** (k + 1))
    D = Phi(s)
    e = linf * D
    j = 0
    if n % 2:
        e = delta_hi * e + lKrh * D
        D = L1 * D
        j = 1
    while j < n:
        e = (delta_hi ** 2) * e + lKrh * (delta_hi + L1) * D
        D = L2 * D
        j += 2
    return D, e


_log.log("CERT level_tail_strict DE: scanning D_star,e_star k=8..501 ...")
finite = []
Dstar = arb(0)
estar = arb(0)
kD = None
kE = None
t_scan = 0
import time
_t0 = time.time()
for k in range(8, 502):
    D, e = exit_de(k)
    finite.append((k, D, e))
    if up(D) > up(Dstar):
        Dstar = D
        kD = k
    if up(e) > up(estar):
        estar = e
        kE = k
    if k % 100 == 0:
        _log.progress("CERT DE scan", k - 7, 495, t0=_t0)
_log.log("CERT level_tail_strict DE: D_star<=%s(k=%s) e_star<=%s(k=%s)"
         % (us(Dstar)[:24], kD, us(estar)[:24], kE))

tail_rows = {}
for k0 in (500, 501):
    D0, e0 = exit_de(k0)
    Dsum = D0 * q / (1 - q)
    esum = e0 * p / (1 - p) + c * D0 / ((1 - p) * (1 - q))
    tail_rows[str(k0)] = {
        "D_at_base_upper": us(D0),
        "e_at_base_upper": us(e0),
        "sum_D_same_parity_after_base_upper": us(Dsum),
        "sum_e_same_parity_after_base_upper": us(esum),
        "therefore_each_later_D_upper": us(Dsum),
        "therefore_each_later_e_upper": us(esum)}

# ============================================================================
# Three-term tail P_tail(m0) = P_all + ||P_perp||_1*D_star + ||h||_1*e_star/(1-1/delta)
# (archive radius r_s = term1+term2 only; term3 is the l-component drift tail).
# 1/delta is a denominator -> delta_hi gives a conservative (larger) 1/delta,
# hence a smaller (1-1/delta) -> larger third term. e_star is the tight (M3=1834)
# value.
# ============================================================================
inv_delta = 1 / delta_hi               # numerator role for 1/delta -> delta_hi conservative
denom = 1 - inv_delta
third_term = (nh * estar) / denom
r_s_two_term = P_ALL + pperp * Dstar
P_tail = r_s_two_term + third_term
tube_radius = arb("5.44e-7")
_log.log("CERT level_tail_strict P_tail: r_s(2-term)<=%s third<=%s P_tail<=%s pass<tube=%s"
         % (us(r_s_two_term)[:24], us(third_term)[:24], us(P_tail)[:24],
            bool(up(P_tail) < tube_radius.lower())))

payload = {
    "precision_bits": 512,
    "provenance": C.provenance(),
    "w_pair_invariant": {
        "C0_pair_boundary": "1000",
        "C1_intermediate": "1280",
        "first_single_coeff_upper": us(first_single_coeff),
        "intermediate_coeff_upper": us(one_coeff),
        "pair_output_coeff_upper": us(pair_coeff),
        "pass": bool(w_invariant)},
    "duhamel_all_levels": {
        "Qcoef_upper": us(QCOEF),
        "geometric_ratio_mu_over_delta2_upper": us(ratioP),
        "kernel_sum_upper": us(kernel_sum),
        "P_all_levels_upper": us(P_ALL),
        "target": "3e-7",
        "pass": bool(up(P_ALL) <= P_TARGET)},
    "DE_geometric_matrix": {
        "q_L2_over_delta4_upper": us(q),
        "p_delta_minus2_upper": us(p),
        "c_offdiag_upper": us(c),
        "spectral_radius_upper": us(q if up(q) >= up(p) else p),
        "finite_checked": "k=8..501",
        "D_star_upper": us(Dstar),
        "D_star_k": kD,
        "e_star_upper": us(estar),
        "e_star_k": kE,
        "tails_after_500_501": tail_rows,
        "pass": bool(up(q) < 1 and up(p) < 1)},
    "tail_three_term": {
        "formula": "P_tail(m0) = P_all + ||P_perp||_1*D_star + ||h||_1*e_star/(1-1/delta)",
        "term1_P_all_upper": us(P_ALL),
        "term2_Pperp_times_D_star_upper": us(pperp * Dstar),
        "term3_h_norm1_e_star_over_1_minus_inv_delta_upper": us(third_term),
        "r_s_two_term_upper": us(r_s_two_term),
        "P_tail_m0_upper": us(P_tail),
        "tube_radius": "5.44e-7",
        "pass_lt_tube_radius": bool(up(P_tail) < tube_radius.lower())},
    "all_pass": bool(w_invariant and up(P_ALL) <= P_TARGET
                     and up(q) < 1 and up(p) < 1),
}
out = HERE / "level_tail_certificate_strict.json"
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
_log.log("CERT level_tail_strict DONE: wrote %s ; all_pass=%s"
         % (out.name, payload["all_pass"]))
print("level_tail_certificate_strict.json: all_pass=%s" % payload["all_pass"])
print("  one_coeff <= %s" % us(one_coeff)[:30])
print("  pair_coeff <= %s" % us(pair_coeff)[:30])
print("  P_all <= %s" % us(P_ALL)[:24])
print("  P_tail <= %s  (< 5.44e-7: %s)" % (us(P_tail)[:24],
      bool(up(P_tail) < tube_radius.lower())))
if not payload["all_pass"]:
    raise SystemExit(1)
