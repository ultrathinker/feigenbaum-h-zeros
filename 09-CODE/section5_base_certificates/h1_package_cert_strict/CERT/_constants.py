# -*- coding: utf-8 -*-
"""CERT/_constants.py -- single source of truth for the package's numerical
constants. Every value is either (i) a chosen round parameter, (ii) a certified
upper bound read from a primary rigorous source in DATA/inputs/, or (iii) a
literal whose validity as an upper bound is certified by RECERT/g_verify.py.

Arb 512 bits with directed rounding. The two delta literals implement the
denominator/numerator split required by BRIEF 3.3(v): delta_lo (truncation,
below the true value) is conservative in every denominator; delta_hi (round-up)
is used wherever delta multiplies a positive upper bound (numerator).
"""
import json
from pathlib import Path
import flint
from flint import arb, ctx

ctx.prec = 512

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
DATA = PKG / "DATA"
INP = DATA / "inputs"


def _load(rel):
    with open(INP / rel, encoding="utf-8") as f:
        return json.load(f)


def _load_text(rel):
    return (INP / rel).read_text(encoding="utf-8")


# ---- Feigenbaum delta: true = 4.6692016091029906718533854932761395015... ----
# delta_lo = truncation at 21 decimals (BELOW true): conservative in denominators.
# delta_hi = round-up at 21 decimals (ABOVE true): conservative in numerators.
DELTA_LO = arb("4.669201609102990671853")
DELTA_HI = arb("4.669201609102990671854")
DELTA_TRUE = arb("4.6692016091029906718533854932761395015")  # reference only

# ---- strict ||DT(G)||_1 = nDT and ||DT(G)^2||_1 = nDT2 ----
# Primary source: cert_G_codex/ndt_rigorous.json (independent duplicate of
# w36/proj_codex/rigorous_block.json). The frozen literals 22.19 / 193.63 are
# BELOW these certified uppers and are NOT valid upper bounds (RECERT confirms).
_ndt = _load("article_v1/v3_work/h1_package/cert_G_codex/ndt_rigorous.json")
NDT_STRICT = arb(repr(_ndt["nDT_upper"]))
NDT2_STRICT = arb(repr(_ndt["nDT2_upper"]))
NDT_FROZEN = arb("22.19")
NDT2_FROZEN = arb("193.63")

# ---- other certified upper bounds (g_verify.py confirms each is a valid upper) ----
K = arb("284")                       # K_global upper (numerator multiplier)
NH = arb("6.331193600692640")        # ||h||_1   (rigorous_block left.h_l1)
Q2 = arb("111.550905120798913")      # ||D^2T(G)[h,h]||_1 / 2 (direct_probe centre.v_l1/2)
PPERP = arb("2.808542")              # ||P_perp||_1 triangle (rigorous_block left.Pperp_triangle_l1)
CS = arb("5.495835")                 # Duhamel kernel constant (rigorous_block circles.0.35.C_s)
MU = arb("0.35")                     # resolvent circle radius (chosen parameter < 1)
LINF = arb("1.104854250319780")      # ||left functional||_inf (rigorous_block left.l_full_head_inf)
RHO = arb("7.5e-4")                  # Lemma-2 tube radius (chosen parameter < 2.5e-3)
T = arb("4.7911")                    # worst |t| = |u|*AU0 (recomputed: AU0_exact*(u_D+R_ARC))

# Lemma W constants (chosen round bounds the package proves against)
C0 = arb("1000")
C1 = arb("1280")

# M3 (certified direct third-derivative norm on B(G,2e-4))
_m3 = _load("w36/audit_codex/m3_global_certificate.json")
M3_CHOSEN = arb(str(_m3["M3_chosen"]))   # 1834


def d2():
    return DELTA_LO ** 2            # denominator -> delta_lo


def d4():
    return DELTA_LO ** 4            # denominator -> delta_lo


def s8():
    return T / (DELTA_LO ** 8)      # denominator -> delta_lo


def sp():
    return s8() / DELTA_LO          # denominator -> delta_lo


def delta_nh():
    """delta*nh in a numerator position -> delta_hi (round-up)."""
    return DELTA_HI * NH


def provenance():
    return {
        "delta_lo": str(DELTA_LO),
        "delta_hi": str(DELTA_HI),
        "delta_true_ref": str(DELTA_TRUE),
        "delta_role_split": ("delta_lo (truncation, below true) used in every denominator "
                             "(d2,d4,s8,sp,s=t/delta^k, exit_de denominator); delta_hi (round-up) "
                             "used wherever delta multiplies a positive upper bound (delta*nh, "
                             "the delta multipliers in the exit_de recursion)."),
        "nDT_strict": str(NDT_STRICT),
        "nDT2_strict": str(NDT2_STRICT),
        "nDT_source": "DATA/inputs/article_v1/v3_work/h1_package/cert_G_codex/ndt_rigorous.json",
        "nDT_frozen": str(NDT_FROZEN),
        "nDT2_frozen": str(NDT2_FROZEN),
        "K": str(K), "NH": str(NH), "Q2": str(Q2), "PPERP": str(PPERP),
        "CS": str(CS), "MU": str(MU), "LINF": str(LINF), "RHO": str(RHO), "T": str(T),
        "C0": str(C0), "C1": str(C1), "M3_chosen": str(M3_CHOSEN),
    }
