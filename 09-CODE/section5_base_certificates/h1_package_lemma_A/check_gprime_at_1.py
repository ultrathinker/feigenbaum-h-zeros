# -*- coding: utf-8 -*-
"""
check_gprime_at_1.py -- independent check of the single numerical link of
Statement 5 (Appendix D, section 6):  G'(1) = -alpha  (derivative w.r.t. x).

Method (deliberately different from the Chebyshev->Taylor->differentiate chain
of the main pipeline): differentiate the Chebyshev series directly,
    g(x) = sum_k c_k T_k(t),  t = x**2 - 1,
    dg/dx = 2x * sum_k c_k * k * U_{k-1}(t)      (T_k' = k U_{k-1}),
and evaluate at x = 1 (t = 0) with mpmath at 200 digits.  The result is
compared digit-by-digit with the certified alpha literal stored in the same
data file (w33_gh_hiprec.json, field "alpha").

Run:  python check_gprime_at_1.py   (needs mpmath)
"""
import json
import os
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "..", "archive_inputs", "w33",
                                     "t5_cert_sonnet", "w33_gh_hiprec.json"))
mp.mp.dps = 200
D = json.load(open(DATA, encoding="utf-8"))
c = [mp.mpf(s) for s in D["g_str"]]
alpha = mp.mpf(D["alpha"])

t = mp.mpf(0)                       # x = 1  <=>  t = x^2 - 1 = 0
dg_dt = sum(ck * k * mp.chebyu(k - 1, t) for k, ck in enumerate(c) if k >= 1)
gprime_x = 2 * 1 * dg_dt            # chain rule, dt/dx = 2x
g1 = sum(ck * mp.chebyt(k, t) for k, ck in enumerate(c))

print("G(1)              =", mp.nstr(g1, 30))
print("G'(1) [d/dx]      =", mp.nstr(gprime_x, 40))
print("-alpha (certified)=", mp.nstr(-alpha, 40))
diff = abs(gprime_x + alpha)
print("|G'(1) + alpha|   =", mp.nstr(diff, 5))
# number of agreeing significant digits
s1 = mp.nstr(-gprime_x, 160).replace(".", "")
s2 = mp.nstr(alpha, 160).replace(".", "")
n = 0
for a, b in zip(s1, s2):
    if a == b:
        n += 1
    else:
        break
print("agreeing significant digits:", n)
print("c = G'(1)/G(1)    =", mp.nstr(gprime_x / g1, 30), "  alpha^2 =", mp.nstr(alpha ** 2, 30))
