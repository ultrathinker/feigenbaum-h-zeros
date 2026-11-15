# -*- coding: utf-8 -*-
"""Standalone D2 verification: reproduce sup_k D_exit(k) for both M3 values,
then recompute r_s with the conservative D_EXIT in interval arithmetic.

Mirrors exit_de() in level_tail_certificate.py:51-57 and compute_exit() in
ld_audit.py:63-88 -- they are the same (D,e) DE recursion, only M3 in Phi
differs. Independent flint recomputation, READ-ONLY over the archive.
"""
import os
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
import flint

flint.ctx.prec = 512
A = flint.arb


def up(x):
    return x.upper()


def lo(x):
    return x.lower()


# constants shared identically by both scripts
delta = A("4.669201609102990671853")
linf = A("1.104854250319780")
K = A("284")
rho = A("7.5e-4")
nDT = A("22.19")
nDT2 = A("193.63")
L1 = nDT + K * rho
L2 = nDT2 + 2 * nDT * K * rho + (K * rho) ** 2
lKrh = linf * K * rho
nh = A("6.331193600692640")
# q2: level_tail uses 111.550905120798913 (tighter upper); ld_audit uses the
# rounded-up 111.550905121. Use the tighter one; both are upper bounds and the
# q2 difference is in the 12th sig fig -- negligible vs the M3 gap.
q2 = A("111.550905120798913")
t = A("4.7911")


def make_Phi(M3):
    q3 = M3 * nh ** 3 / A(6)

    def Phi(s):
        return q2 * s * s + q3 * s ** 3
    return Phi


def exit_de(k, M3):
    """Reproduce exit_de(k) from level_tail_certificate.py:51-57 with a given M3."""
    Phi = make_Phi(M3)
    n = k - 7
    s = t / delta ** (k + 1)
    D = Phi(s)
    e = linf * D
    j = 0
    if n % 2:
        e = delta * e + lKrh * D
        D = L1 * D
        j = 1
    while j < n:
        e = delta ** 2 * e + lKrh * (delta + L1) * D
        D = L2 * D
        j += 2
    return D, e


def d_star(M3, kmax=501):
    Dstar = A(0)
    kstar = None
    for k in range(8, kmax + 1):
        D, _ = exit_de(k, M3)
        if up(D) > up(Dstar):
            Dstar = D
            kstar = k
    return Dstar, kstar


print("=== D2 verification: sup_k D_exit(k) for both M3 values ===")
for M3v, tag in [("1834", "tight (level_tail)"), ("123479", "conservative (compute_ld)")]:
    M3 = A(M3v)
    Dstar, kstar = d_star(M3)
    print("M3=%-7s %-22s D_star.upper = %.12e  (k=%d)" % (M3v, tag, float(Dstar.upper()), kstar))
print()
print("Archive references:")
print("  level_tail_certificate.json:25 D_star_upper = 5.17192283219034e-8  (M3=1834)")
print("  compute_ld.json:5            D_star      = 6.252014868072774e-8 (M3=123479)")
print()

# conservative radius in interval arithmetic
P_EXIT = A("2.113426e-7")            # radius_K284_certificate.py:11 (P_all ceiling)
D_EXIT_tight = A("5.171923e-8")      # radius_K284_certificate.py:12 (D_star, M3=1834)
D_EXIT_cons = A("6.252015e-8")       # compute_ld.log D_cp* (M3=123479)
P_PERP = A("2.808542")               # radius_K284_certificate.py:13
TUBE = A("5.44e-7")

r_tight = P_EXIT + P_PERP * D_EXIT_tight
r_cons = P_EXIT + P_PERP * D_EXIT_cons
head_tight = TUBE - r_tight
head_cons = TUBE - r_cons

print("=== r_s in interval arithmetic (radius_K284_certificate.py:14) ===")
print("r_s = P_EXIT + P_PERP * D_EXIT")
print("  P_EXIT  = 2.113426e-7   P_PERP = 2.808542   TUBE = 5.44e-7")
print()
print("D_EXIT = 5.171923e-8 (tight, M3=1834):")
print("  r_s.upper       = %.12e" % float(r_tight.upper()))
print("  headroom.lower  = %.12e" % float(head_tight.lower()))
print("  pass r_s<=TUBE  = %s" % bool(r_tight.upper() <= TUBE.lower()))
print()
print("D_EXIT = 6.252015e-8 (conservative, M3=123479):")
print("  r_s.upper       = %.12e" % float(r_cons.upper()))
print("  headroom.lower  = %.12e" % float(head_cons.lower()))
print("  pass r_s<=TUBE  = %s" % bool(r_cons.upper() <= TUBE.lower()))
print()
print("headroom drop (tight -> conservative) = %.6e" % (
    float(head_tight.lower()) - float(head_cons.lower())))
print("robustness: package output (r_s<TUBE) INDEPENDENT of which D_star is correct:",
      bool(r_tight.upper() <= TUBE.lower()) and bool(r_cons.upper() <= TUBE.lower()))
