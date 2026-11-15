# -*- coding: utf-8 -*-
"""Outward-rounded assembly of F* and the five Rouché budgets."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import flint


flint.ctx.prec = 512
HERE = Path(__file__).resolve().parent
LOG = (HERE / "assemble_results.log").open("w", encoding="utf-8", buffering=1)
OUT = HERE / "assemble_results.json"


def p(s):
    print(s, flush=True)
    LOG.write(str(s) + "\n")
    LOG.flush()
    os.fsync(LOG.fileno())


def ub(x):
    return math.nextafter(float(x.upper()), math.inf)


a = flint.arb

# Rounded outwards from rigorous_block.json.
PU = a("1.808542")
PS = a("2.808542")
CS035 = a("5.495835")
AP_STABLE = a("0.878719")
MU = a("0.35")
DELTA_LO = a("4.66920160910298")
DELTA_HI = a("4.66920160910301")
K = a("223.77")
HNORM = a("6.331194")
AU0 = a("0.414037999086273")
U_MAX = a("11.471516303") + a("0.1")

# Fixed-point linear propagation only.  The n=0 term is I, not Pu+Ps.
F_LINEAR = 1 + PU / (DELTA_LO - 1) + CS035 * MU / (DELTA_LO**2 - MU)
p(f"F_linear_fixed_point <= {F_LINEAR}")

# Nonautonomous bridge.  The already-derived tube bound supplies
# ||w_j||+D_j <= 2.8001e-7.  Every derivative input has remaining level >=8.
RHO_GAP = a("2.8001e-7")
RHO_INPUT = AU0 * U_MAX * HNORM / (DELTA_LO**8) + RHO_GAP
E = K * RHO_INPUT
p(f"rho_derivative_input <= {RHO_INPUT}")
p(f"||DT(xi)-DT(G)||_1 <= {E}")

# Component recursion for u_j=||Pu v_j|| and s_j=||Ps v_j||:
# [u';s'] <= MAT [u;s].
MAT = flint.arb_mat(2, 2)
MAT[0, 0] = DELTA_HI + PU * E
MAT[0, 1] = PU * E
MAT[1, 0] = PS * E
MAT[1, 1] = AP_STABLE + PS * E
q = 1 / (DELTA_LO**2)
QM = q * MAT
I = flint.arb_mat(2, 2)
I[0, 0] = I[1, 1] = 1
X0 = flint.arb_mat(2, 1)
X0[0, 0], X0[1, 0] = PU, PS
ONES = flint.arb_mat(1, 2)
ONES[0, 0] = ONES[0, 1] = 1
TAIL = ONES * ((I - QM).inv() - I) * X0
F_NONAUTO = 1 + TAIL[0, 0]
p(f"q*M = {QM}")
p(f"F_nonautonomous <= {F_NONAUTO}")

# Rouché inputs from w36/opus_bootstrap/p5_final.py, r=0.1000 chain.
delta = a("4.669201609102990671853")
d8 = delta**8
r0 = a("0.0025")
nD2hh = a("223.10")
M3 = K / (r0 - a("0.0002"))
q2 = nD2hh / 2
q3 = M3 * HNORM**3 / 6
LAM = a("53459.07")
TE = {"A": "8.270999733", "B": "7.340479780", "C": "11.013820661",
      "D": "11.471516303", "N": "7.534878921"}
CAU = {"A": "14.42", "B": "63.22", "C": "3.740", "D": "55.23", "N": "4814"}
MINH5 = {"A": "0.3603", "B": "1.3106", "C": "0.0825", "D": "0.7530", "N": "23.060"}
D56 = {"A": "0.002088", "B": "0.006300", "C": "0.000869", "D": "0.009780", "N": "0.1628"}

rows = {}
for name in TE:
    s8 = AU0 * (a(TE[name]) + a("0.1")) / d8
    phi = q2 * s8**2 + q3 * s8**3
    l7 = LAM * a(CAU[name])
    btail = l7 * F_NONAUTO * phi
    minh7 = a(MINH5[name]) - a(D56[name])
    fraction = btail / minh7
    margin = minh7 / btail
    rows[name] = dict(L7=l7, phi=phi, B_tail=btail, minH7=minh7,
                      budget_fraction=fraction, margin=margin)
    p(f"{name}: B_tail <= {btail}; B_tail/minH7 <= {fraction}; margin >= {margin}")


def ball(v):
    return {"ball": str(v), "upper_float": ub(v),
            "lower_float": math.nextafter(float(v.lower()), -math.inf)}


payload = {
    "status": "INTERVAL_ARITHMETIC_ASSEMBLY_CONDITIONAL_ON_LISTED_INPUT_CERTIFICATES",
    "F_linear_fixed_point": ball(F_LINEAR),
    "rho_derivative_input": ball(RHO_INPUT),
    "derivative_perturbation": ball(E),
    "F_nonautonomous": ball(F_NONAUTO),
    "rouche": {k: {kk: ball(vv) for kk, vv in v.items()} for k, v in rows.items()},
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
p(f"wrote {OUT.name}")
LOG.close()
