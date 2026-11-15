# -*- coding: utf-8 -*-
"""
check_gh_at_x0.py -- values of the certified Chebyshev pair (g, h) at x = 0.

Convention (the same one x4_common.py uses for every H-certificate):
    the coefficients g_str / h_str in w33_gh_hiprec.json are the series
        g(x) = sum_k c_k * T_k(t),   t = x**2 - 1  in [-1, 1],
    and w = t / 2.5 = (x**2 - 1) / 2.5 is the Taylor variable of radius 2.5
    (x4_common.py: cheb_to_taylor multiplies by 2.5**j and evaluates in w).
    Hence the normalisation point x = 0 is t = -1 (w0 = -0.4), NOT t = -0.4.

Expected output (IDENTITY_B.md, section B.4):
    g(x=0) = 1 (to ~1e-89 within the 100-mode truncation),
    h0(x=0) = 9.957e-32,
so |h(x=0)| <= ||h - h0||_1 + |h0(x=0)| <= 1.63e-29 + 1e-31 (cl34_certificate.json).

Run:  python check_gh_at_x0.py   (needs mpmath; data path relative to 09-CODE)
"""
import json
import os
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "..", "archive_inputs", "w33",
                                     "t5_cert_sonnet", "w33_gh_hiprec.json"))
mp.mp.dps = 120
D = json.load(open(DATA, encoding="utf-8"))
g = [mp.mpf(s) for s in D["g_str"]]
h = [mp.mpf(s) for s in D["h_str"]]


def ev(c, t):
    return sum(ck * mp.chebyt(k, t) for k, ck in enumerate(c))


for label, t in (("x=0  (t=-1, w=-0.4)", mp.mpf(-1)),
                 ("x=1  (t=0,  w=0)", mp.mpf(0)),
                 ("t=-0.4 (x^2=0.6; NOT the normalisation point)", mp.mpf("-0.4"))):
    print("%-48s g = %s   h0 = %s" % (label, mp.nstr(ev(g, t), 20), mp.nstr(ev(h, t), 12)))
