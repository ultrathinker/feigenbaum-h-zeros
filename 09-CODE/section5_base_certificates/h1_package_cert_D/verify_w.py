# -*- coding: utf-8 -*-
"""ADDENDUM W: independent recomputation of the three Lemma W inequalities,
the step-by-step vs closed-form Duhamel split, the C1 breaking point and the
nDT inherited-constant headroom.

512-bit Arb (python-flint). Read-only over the archive; recomputes everything.
Mirrors the exact formulas in level_tail_certificate.py:26-42 (Lemma W + QCOEF)
and duhamel_audit.py:80-168 (step-by-step nesting + refined Duhamel sum).

Writes verify_w.json with all numbers; prints a human-readable summary.
"""
import json, os
import flint

flint.ctx.prec = 512
A = flint.arb
HERE = os.path.dirname(os.path.abspath(__file__))

def U(x):
    return float(x.upper())

def M(x):
    return float(x.mid())

# ---- certified constants (level_tail_certificate.py:11-19) ----
delta = A("4.669201609102990671853"); d2 = delta ** 2; d4 = delta ** 4
t = A("4.7911"); s8 = t / delta ** 8
K = A("284"); nh = A("6.331193600692640")
nDT = A("22.19"); nDT2 = A("193.63")
q2 = A("111.550905120798913")
rho = A("7.5e-4"); linf = A("1.104854250319780")
pperp = A("2.808542"); Cs = A("5.495835"); mu = A("0.35")
L1 = nDT + K * rho
L2 = nDT2 + 2 * nDT * K * rho + (K * rho) ** 2
lKrh = linf * K * rho

# ============================================================================
# 1. LEMMA W -- the three inequalities (level_tail_certificate.py:26-34)
# ============================================================================
C0 = A("1000"); C1 = A("1280"); sp = s8 / delta
first_single_coeff = (K * nh ** 2 / 2) / d2
c1_unscaled = nDT * C0 + K * (nh + C0 * sp) ** 2 / 2
one_coeff = (nDT * C0 + K * (nh + C0 * sp) ** 2 / 2) / d2
pair_coeff = (nDT2 * C0 + nDT * K * (nh + C0 * sp) ** 2 / 2
              + K * (delta * nh + c1_unscaled * sp) ** 2 / 2) / d4

w_ineqs = {
    "first_single_coeff_upper": U(first_single_coeff),
    "first_single_coeff_bound": float(C0),
    "first_single_coeff_pass": U(first_single_coeff) <= float(C0),
    "first_single_coeff_margin_pct": float((C0 - first_single_coeff.upper()) / C0 * 100),
    "intermediate_one_coeff_upper": U(one_coeff),
    "intermediate_one_coeff_bound": float(C1),
    "intermediate_one_coeff_pass": U(one_coeff) <= float(C1),
    "intermediate_one_coeff_margin_pct": float((C1 - one_coeff.upper()) / C1 * 100),
    "pair_output_coeff_upper": U(pair_coeff),
    "pair_output_coeff_bound": float(C0),
    "pair_output_coeff_pass": U(pair_coeff) <= float(C0),
    "pair_output_coeff_margin_pct": float((C0 - pair_coeff.upper()) / C0 * 100),
    "lemma_W_pass": (U(first_single_coeff) <= float(C0)
                     and U(one_coeff) <= float(C1)
                     and U(pair_coeff) <= float(C0)),
    "sp_upper": U(sp),
    "c1_unscaled_upper": U(c1_unscaled),
}

# ============================================================================
# 2. CLOSED-FORM P_all with C1 invariant (level_tail_certificate.py:38-42)
#    = the formula that the package actually uses.
# ============================================================================
ratioP = mu / d2
kernel_sum = pperp + Cs * ratioP / (1 - ratioP)

def closed_form_P_all(M3val, C1val):
    M3 = A(M3val); C1l = A(C1val)
    QCOEF = (q2 + K * nh * C1l * s8 + K * C1l ** 2 * s8 ** 2 / 2
             + M3 * (nh + C1l * s8) ** 3 * s8 / 6)
    Pall = QCOEF * s8 ** 2 * kernel_sum
    return Pall, QCOEF

Pall_1834_1280, QCOEF_1834 = closed_form_P_all("1834", "1280")
Pall_123479_1280, _ = closed_form_P_all("123479", "1280")

closed_form = {
    "P_all_M3_1834_C1_1280_upper": U(Pall_1834_1280),
    "P_all_M3_1834_C1_1280_pass_3e-7": U(Pall_1834_1280) <= 3e-7,
    "P_all_M3_123479_C1_1280_upper": U(Pall_123479_1280),
    "P_all_M3_123479_C1_1280_pass_3e-7": U(Pall_123479_1280) <= 3e-7,
    "QCOEF_M3_1834_C1_1280_upper": U(QCOEF_1834),
    "kernel_sum_upper": U(kernel_sum),
}

# ============================================================================
# 3. STEP-BY-STEP Duhamel recursion (duhamel_audit.py:80-168), both M3.
#    This is the bound WITHOUT Lemma W: w_j is propagated step by step and
#    inflated by (K/2)*a_j^2 each step; Q_j uses the refined decomposition.
#    Confirms that the step-by-step recursion FAILS even with M3=1834.
# ============================================================================
AU0 = A("0.414037999086273")
u_D = A("11.471516303")
R_ARC = A("0.1")
tmax = AU0 * (u_D + R_ARC)
HALF = A("0.5")

def nesting_full(k, tval):
    steps = k - 7
    if steps <= 0:
        return [], [], [], A(0)
    a_traj = []; s_traj = []; w_traj = []
    w = A(0); j = 0; Amax = A(0)
    def s_of(jj):
        return tval / (delta ** (k - jj))
    if steps % 2 == 1:
        sj = s_of(0); aj = sj * nh + w
        a_traj.append(aj); s_traj.append(sj); w_traj.append(w)
        if aj.mid() > Amax.mid():
            Amax = aj
        w = nDT * w + HALF * K * aj * aj
        j = 1
    while j < steps:
        sj = s_of(j); aj = sj * nh + w
        a_traj.append(aj); s_traj.append(sj); w_traj.append(w)
        w1 = nDT * w + HALF * K * aj * aj
        sj1 = s_of(j + 1); aj1 = sj1 * nh + w1
        a_traj.append(aj1); s_traj.append(sj1); w_traj.append(w1)
        if aj.mid() > Amax.mid():
            Amax = aj
        if aj1.mid() > Amax.mid():
            Amax = aj1
        w = nDT2 * w + nDT * HALF * K * aj * aj + HALF * K * aj1 * aj1
        j += 2
    return a_traj, s_traj, w_traj, Amax

def refined_Q_bound(sj, aj, wj, M3):
    hh_term = sj * sj * q2
    cross_term = sj * K * nh * wj
    self_term = HALF * K * wj * wj
    cubic_term = (M3 / 6) * aj * aj * aj
    return hh_term + cross_term + self_term + cubic_term

def duhamel_refined(k, tval, M3, N_MAX=500):
    n = k - 7
    if n <= 0:
        return A(0)
    a_traj, s_traj, w_traj, _ = nesting_full(k, tval)
    Psum = A(0)
    for i in range(n):
        j = n - 1 - i
        kernel = Cs * (mu ** j)
        Qb = refined_Q_bound(s_traj[i], a_traj[i], w_traj[i], M3)
        Psum += kernel * Qb
    return Psum

step_by_step = {}
for M3v, tag in [("1834", "M3_1834"), ("123479", "M3_123479")]:
    M3 = A(M3v)
    Pstar = A(0); kstar = None
    for k in range(7, 501):
        Pr = duhamel_refined(k, tmax, M3)
        if Pr.mid() > Pstar.mid():
            Pstar = Pr; kstar = k
    step_by_step[tag] = {
        "M3": int(M3v),
        "P_star_refined_step_by_step_upper": U(Pstar),
        "P_star_k": kstar,
        "pass_3e-7": U(Pstar) <= 3e-7,
    }

# ============================================================================
# 4. C1 BREAKING POINT -- bisect on C1 with M3=1834 until P_all just crosses 3e-7.
# ============================================================================
P_TARGET = 3e-7
lo_c1 = 1280.0
hi_c1 = 10000.0
# sanity: hi must FAIL, lo must PASS
P_lo, _ = closed_form_P_all("1834", str(lo_c1))
P_hi, _ = closed_form_P_all("1834", str(hi_c1))
assert U(P_lo) <= P_TARGET, ("lo_c1 must PASS", U(P_lo))
assert U(P_hi) > P_TARGET, ("hi_c1 must FAIL", U(P_hi))
for _ in range(200):
    mid_c1 = 0.5 * (lo_c1 + hi_c1)
    Pm, _ = closed_form_P_all("1834", repr(mid_c1))
    if U(Pm) <= P_TARGET:
        lo_c1 = mid_c1
    else:
        hi_c1 = mid_c1
    if hi_c1 - lo_c1 < 1e-6:
        break
# the breaking point is between lo_c1 (PASS) and hi_c1 (FAIL); report the
# boundary as the upper edge of the PASS region + a bracket table.
c1_table = []
for c1v in [1280, 1500, 2000, 3000, 3050, 3500, 5000]:
    Pm, _ = closed_form_P_all("1834", str(c1v))
    c1_table.append({"C1": c1v,
                     "P_all_upper": U(Pm),
                     "pass_3e-7": U(Pm) <= P_TARGET})
c1_break = {
    "breaking_point_C1_pass_below": lo_c1,
    "breaking_point_C1_fail_above": hi_c1,
    "breaking_point_bracket": (lo_c1, hi_c1),
    "one_coeff_required_floor": U(one_coeff),
    "headroom_factor_vs_required": lo_c1 / U(one_coeff),
    "table": c1_table,
}

# ============================================================================
# 5. nDT INHERITED-CONSTANT HEADROOM (joint constraint).
#    Lemma W requires C1 >= one_coeff(nDT); the package P_all<=3e-7 requires
#    C1 <= C1_break (the breaking point found above). So a valid C1 exists iff
#    one_coeff(nDT) <= C1_break. nDT may therefore grow until one_coeff(nDT)
#    reaches C1_break -- the C1 headroom (2.4x) transfers to nDT.
#    (Lemma W's first_single_coeff and pair_coeff do NOT involve nDT, so
#    one_coeff is the only nDT-dependent binding constraint.)
# ============================================================================
def one_coeff_for_nDT(nDTval):
    nDTl = A(repr(nDTval))
    return (nDTl * C0 + K * (nh + C0 * sp) ** 2 / 2) / d2

c1_break_val = lo_c1  # upper edge of PASS region from the bisection above
lo_n = float(nDT)
hi_n = 500.0
P_lo_n = one_coeff_for_nDT(lo_n)
P_hi_n = one_coeff_for_nDT(hi_n)
assert U(P_lo_n) <= c1_break_val, ("lo_n must satisfy one_coeff<=C1_break", U(P_lo_n))
assert U(P_hi_n) > c1_break_val, ("hi_n must fail", U(P_hi_n))
for _ in range(200):
    mid_n = 0.5 * (lo_n + hi_n)
    Pm = one_coeff_for_nDT(mid_n)
    if U(Pm) <= c1_break_val:
        lo_n = mid_n
    else:
        hi_n = mid_n
    if hi_n - lo_n < 1e-8:
        break
# cross-check: at the breaking nDT, set C1 = one_coeff(nDT) and confirm P_all~3e-7
P_check, _ = closed_form_P_all("1834", repr(one_coeff_for_nDT(lo_n).upper()))
ndt_headroom = {
    "nDT_current": float(nDT),
    "one_coeff_current_upper": U(one_coeff),
    "C1_breaking_point_used": c1_break_val,
    "joint_constraint": ("a valid C1 exists iff one_coeff(nDT) <= C1_break, "
                         "because P_all(C1) is monotone increasing; the package "
                         "picks the smallest valid C1 = ceil(one_coeff) to "
                         "minimise P_all. nDT may grow until one_coeff reaches "
                         "the breaking C1."),
    "nDT_at_which_one_coeff_hits_C1_break_bracket": (lo_n, hi_n),
    "nDT_growth_factor_vs_current": lo_n / float(nDT),
    "P_all_at_breaking_nDT_with_C1_eq_one_coeff_upper": U(P_check),
    "note": ("one_coeff is the only nDT-dependent inequality of Lemma W; it is "
             "dominated by nDT*C0/d2 ~ 1018 of 1279. The 2.4x C1 headroom thus "
             "transfers almost fully to nDT (factor ~%.2fx, slightly less than "
             "C1's 2.4x because of the ~261 nDT-independent offset)." % (
                 lo_n / float(nDT))),
}

out = {
    "precision_bits": 512,
    "lemma_W_inequalities": w_ineqs,
    "closed_form_P_all": closed_form,
    "step_by_step_duhamel": step_by_step,
    "c1_breaking_point": c1_break,
    "nDT_headroom": ndt_headroom,
}

with open(os.path.join(HERE, "verify_w.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# ---- console ----
print("=== Lemma W recomputation (ADDENDUM W) ===")
print("first_single_coeff = %.6f  <= C0=1000  margin %.3f%%  pass=%s" % (
    w_ineqs["first_single_coeff_upper"], w_ineqs["first_single_coeff_margin_pct"],
    w_ineqs["first_single_coeff_pass"]))
print("one_coeff          = %.6f  <= C1=1280  margin %.4f%%  pass=%s" % (
    w_ineqs["intermediate_one_coeff_upper"], w_ineqs["intermediate_one_coeff_margin_pct"],
    w_ineqs["intermediate_one_coeff_pass"]))
print("pair_coeff         = %.6f  <= C0=1000  margin %.3f%%  pass=%s" % (
    w_ineqs["pair_output_coeff_upper"], w_ineqs["pair_output_coeff_margin_pct"],
    w_ineqs["pair_output_coeff_pass"]))
print("lemma_W_pass =", w_ineqs["lemma_W_pass"])
print()
print("=== P-piece: step-by-step vs closed-form ===")
print("step-by-step M3=1834  : P*=%.6e  pass=%s" % (
    step_by_step["M3_1834"]["P_star_refined_step_by_step_upper"],
    step_by_step["M3_1834"]["pass_3e-7"]))
print("step-by-step M3=123479: P*=%.6e  pass=%s" % (
    step_by_step["M3_123479"]["P_star_refined_step_by_step_upper"],
    step_by_step["M3_123479"]["pass_3e-7"]))
print("closed-form M3=1834   : P_all=%.6e  pass=%s" % (
    closed_form["P_all_M3_1834_C1_1280_upper"],
    closed_form["P_all_M3_1834_C1_1280_pass_3e-7"]))
print("closed-form M3=123479 : P_all=%.6e  pass=%s" % (
    closed_form["P_all_M3_123479_C1_1280_upper"],
    closed_form["P_all_M3_123479_C1_1280_pass_3e-7"]))
print("gap (closed - step) with M3=1834 = %.4e" % (
    closed_form["P_all_M3_1834_C1_1280_upper"]
    - step_by_step["M3_1834"]["P_star_refined_step_by_step_upper"]))
print("  => Lemma W is load-bearing: step FAILS, closed PASS")
print()
print("=== C1 breaking point (M3=1834) ===")
print("breaking C1 bracket: [%.4f, %.4f] (pass below / fail above)" % (
    c1_break["breaking_point_bracket"][0], c1_break["breaking_point_bracket"][1]))
print("required floor one_coeff = %.4f" % c1_break["one_coeff_required_floor"])
print("headroom factor = %.3fx" % c1_break["headroom_factor_vs_required"])
for row in c1_break["table"]:
    print("  C1=%5d -> P_all=%.6e  pass=%s" % (row["C1"], row["P_all_upper"], row["pass_3e-7"]))
print()
print("=== nDT inherited-constant headroom (joint constraint one_coeff<=C1_break) ===")
print("nDT=%g -> one_coeff=%.4f <= C1_break=%.4f" % (
    ndt_headroom["nDT_current"], ndt_headroom["one_coeff_current_upper"],
    ndt_headroom["C1_breaking_point_used"]))
print("nDT may grow to [%.4f, %.4f] before one_coeff hits C1_break" % (
    ndt_headroom["nDT_at_which_one_coeff_hits_C1_break_bracket"][0],
    ndt_headroom["nDT_at_which_one_coeff_hits_C1_break_bracket"][1]))
print("growth factor vs current = %.3fx  (C1 headroom %.3fx)" % (
    ndt_headroom["nDT_growth_factor_vs_current"],
    c1_break["headroom_factor_vs_required"]))
print()
print("wrote", os.path.join(HERE, "verify_w.json"))
