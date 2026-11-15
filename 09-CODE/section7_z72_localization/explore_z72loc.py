# -*- coding: utf-8 -*-
"""explore_z72loc.py -- ЧИСЛЕННАЯ (NOT RIGOROUS) разведка для брифа Z72_LOC_BRIEF
[oid:9595c48c]: строгая локализация нуля Z72 внутри его сертификатного диска.

Цель: понять magnitudes для выбора r0:
  * H8 (и H7) в точке u0 (float-оценка нуля) -- должно быть ~0
  * |H8| на окружности D(u0, r) для r in {0.01, 0.005, 0.0025, ...} -> min|H8|
  * наклон |H8'|~min|H8|/r
  * контурный уровень B_tail = S_disk(|u0|+r) - Phi(s8) (мажоранта, контур-level)
  * грубая оценка L7 (из LAff H7_light, upper bound на машинный 'a'-коэфф + Rmax)
  * грубый margin = min|H8| / (L7_est * (S_disk-Phi(s8)))

Арифметика: python-flint acb (точечная орбита, НЕ интервальная книга) + Arb для
S_disk. Это разведка; строгий сертификат -- отдельный скрипт.
"""
from __future__ import annotations
import json, math, time, hashlib
from fractions import Fraction
from pathlib import Path

import flint

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "explore_results.json"

flint.ctx.prec = 200
A, C = flint.arb, flint.acb
PI = A.pi()
TWO_PI = 2 * PI
I_UNIT = C(0, 1)

sys_path_add = str(ROOT / "w35" / "x4_walk_sonnet")
import sys
sys.path.insert(0, sys_path_add)
import x4_common as xc

AU0 = xc.AU0
DELTA = xc.DELTA_pt
R_DISC = xc.r_disc
DELTA_LO = DELTA.real.lower()

X4_PATH = ROOT / "w35" / "x4_walk_sonnet" / "x4_common.py"
GH_PATH = ROOT / "w33" / "t5_cert_sonnet" / "w33_gh_hiprec.json"
CL34_PATH = ROOT / "w36" / "tail_codex" / "cl34_certificate.json"
ABS36_PATH = ROOT / "w36" / "audit_codex" / "absolute_margins_arb.json"
POINT8B_JSON = ROOT / "path_to_8" / "point8b_spectral_certificate" / "spectral_certificate.json"
POINT8C_JSON = ROOT / "path_to_8" / "point8c_spectral_theta" / "theta_certificate.json"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def horner(coeffs, w):
    a = C(0)
    for ck in reversed(coeffs):
        a = a * w + ck
    return a


def H_point(u, m):
    """Point value H_m(u) = x_{2^{m+1}}/x_{2^m} (poles_check style)."""
    s = u * AU0 / (DELTA ** m)
    x = C(0)
    xden = None
    lev_num = 1 << (m + 1)
    lev_den = 1 << m
    for n in range(lev_num):
        w = (x * x - C(1)) / C(R_DISC)
        x = horner(xc.tc_g, w) + s * horner(xc.tc_h, w)
        if n + 1 == lev_den:
            xden = x
    return x, xden


# ---- S_disk_for (verbatim from z72_certificate / z72_verify) ----
_cl34 = json.loads(CL34_PATH.read_text(encoding="utf-8"))
_abs36 = json.loads(ABS36_PATH.read_text(encoding="utf-8"))
EPS_H = A(_cl34["V_h_delta"]["h_error_stored_center_upper"]).upper()
nh = A(_abs36["nh_upper"]).upper() + EPS_H

DELTA0 = A("4.66920160910299067185320382046620161725818557747576863274565134300413")
DELTA_ERR = A("9.452e-30")
DELTA_WIDENED = DELTA0 + A(0, DELTA_ERR)
LEFT_HEAD_NORM = A("1.104854250319780")
K284 = A("284")
RHO_STAR = A("7.5e-4")
PPERP_NORM = A("2.808542")
RESOLVENT_CS = A("5.495835")
RESOLVENT_MU = A("0.35")
TAIL_MARGIN = 250
J_MAX = 360
NDT_REF = A("22.19")
NDT2_REF = A("193.63")
M3 = A("1834")
Q2 = A("111.550905120798913")

L1 = (NDT_REF + K284 * RHO_STAR).upper()
L2 = (NDT2_REF + 2 * NDT_REF * K284 * RHO_STAR + (K284 * RHO_STAR) ** 2).upper()
q_direct = (L2 / (DELTA_LO ** 4)).upper()
q3 = (M3 * nh ** 3 / A(6)).upper()


def build_Lam_final():
    point8b = json.loads(POINT8B_JSON.read_text(encoding="utf-8"))
    u_table = {row["j"]: A(row["U_j_upper"]) for row in point8b["final_table"]}

    def U(j):
        if j == 0:
            return PPERP_NORM
        if j in u_table:
            return u_table[j]
        return RESOLVENT_CS * (RESOLVENT_MU ** j)

    delta_u = DELTA_WIDENED.upper()
    Krho = (K284 * RHO_STAR).upper()
    Hcoef = (LEFT_HEAD_NORM * nh).upper()
    delta_pow = [A(1)]
    for _ in range(J_MAX):
        delta_pow.append((delta_pow[-1] * delta_u).upper())
    Lam_new = [A(1)]
    Lam_final = [A(1)]
    for j in range(1, J_MAX + 1):
        acc = A(0)
        for m in range(j):
            bracket = (Hcoef * delta_pow[j - 1 - m] + U(j - 1 - m)).upper()
            acc = (acc + Lam_new[m] * bracket).upper()
        lam_new_j = (Hcoef * delta_pow[j] + U(j) + Krho * acc).upper()
        lam_old_j = (A(L2) ** (j // 2)).upper() if j % 2 == 0 else (A(L1) * A(L2) ** ((j - 1) // 2)).upper()
        Lam_new.append(lam_new_j)
        Lam_final.append(lam_new_j if float(lam_new_j) <= float(lam_old_j) else lam_old_j)
    return Lam_final


LAM = build_Lam_final()


def S_disk_minus_Phi_s8(abs_uc_rho):
    def Phi(s):
        return (Q2 * s * s + q3 * s ** 3).upper()

    def s_of(k):
        return (abs_uc_rho * A(AU0.real.mid()) / (DELTA_LO ** (k + 1))).upper()

    def D_new(k):
        return (A(LAM[k - 7]) * Phi(s_of(k))).upper()

    def D_old(k):
        j = k - 7
        lam_old = (A(L2) ** (j // 2)).upper() if j % 2 == 0 else (A(L1) * A(L2) ** ((j - 1) // 2)).upper()
        return (lam_old * Phi(s_of(k))).upper()

    K_CUT = 7 + TAIL_MARGIN
    near = A(0)
    for k in range(7, K_CUT):
        near = (near + D_new(k)).upper()
    far_tail = ((D_old(K_CUT) + D_old(K_CUT + 1)) / (A(1) - q_direct)).upper()
    S_new = (near + far_tail).upper()
    Phi_s8 = Phi(s_of(7))
    return float(S_new), float(Phi_s8), float((S_new - Phi_s8).upper()), float(far_tail)


def main():
    t0 = time.time()
    U0_RE = "4.791660937911268"
    U0_IM = "7.177581007211361"
    u0 = C(A(U0_RE), A(U0_IM))
    u0_abs = (A(U0_RE) * A(U0_RE) + A(U0_IM) * A(U0_IM)).sqrt()
    print("u0 = %s + %si" % (U0_RE, U0_IM), flush=True)
    print("|u0| = %s" % u0_abs, flush=True)
    print("x4 sha256: %s" % sha256(X4_PATH), flush=True)
    print("gh  sha256: %s" % sha256(GH_PATH), flush=True)

    # H7, H8 at u0
    h7num, h7den = H_point(u0, 7)
    h8num, h8den = H_point(u0, 8)
    H7 = h7num / h7den
    H8 = h8num / h8den
    print("\nH7(u0) = %s + %si   |H7|=%.6e" % (H7.real, H7.imag, abs(complex(H7.real.mid(), H7.imag.mid()))), flush=True)
    print("H8(u0) = %s + %si   |H8|=%.6e" % (H8.real, H8.imag, abs(complex(H8.real.mid(), H8.imag.mid()))), flush=True)

    # min|H8| on circles + slope estimate
    radii = [0.01, 0.005, 0.0025, 0.00125, 0.000625]
    rows = []
    for r in radii:
        N = 512
        min_abs = None
        vals = []
        for k in range(N):
            th = TWO_PI * A(k) / A(N)
            u = u0 + C(A(str(r))) * (I_UNIT * C(th)).exp()
            hn, hd = H_point(u, 8)
            Hv = hn / hd
            av = abs(complex(Hv.real.mid(), Hv.imag.mid()))
            vals.append(av)
            if min_abs is None or av < min_abs:
                min_abs = av
        abs_uc_rho = float((u0_abs + A(str(r))).upper())
        S_new, Phi_s8, S_minus, far_tail = S_disk_minus_Phi_s8(A(abs_uc_rho))
        rows.append({"r": r, "min_abs_H8": min_abs, "max_abs_H8": max(vals),
                      "abs_uc_rho": abs_uc_rho, "S_new": S_new, "Phi_s8": Phi_s8,
                      "S_minus_Phi_s8": S_minus})
        print("r=%.5f  min|H8|=%.6e  max|H8|=%.6e  |u|+r=%.5f  S_disk=%.4e  Phi(s8)=%.4e  S-Phi=%.4e" % (
            r, min_abs, max(vals), abs_uc_rho, S_new, Phi_s8, S_minus), flush=True)

    # slope estimate from finite differences at u0
    du = 1e-5
    slopes = []
    for (dre, dim) in [(du, 0.0), (0.0, du), (-du, 0.0), (0.0, -du)]:
        uu = C(A(U0_RE) + A(str(dre)), A(U0_IM) + A(str(dim)))
        hn, hd = H_point(uu, 8)
        Hv = hn / hd
        h8_0 = complex(H8.real.mid(), H8.imag.mid())
        hv = complex(Hv.real.mid(), Hv.imag.mid())
        slopes.append(abs(hv - h8_0) / du)
    slope_est = sum(slopes) / len(slopes)
    print("\nestimated |H8'(u0)| ~ %.6e (mean of 4 finite-diff)" % slope_est, flush=True)

    # rough margin: need L7. Estimate conservatively from Z72 worst L7 ~ 1.5e6 (we'll
    # compute the rigorous L7 in the builder). Report margin for a RANGE of L7 guesses.
    print("\n--- rough margin = min|H8| / (L7_est * (S_disk - Phi(s8))) ---", flush=True)
    L7_guesses = [5e5, 1e6, 2e6, 5e6]
    margin_table = {}
    for row in rows:
        r = row["r"]
        Sminus = row["S_minus_Phi_s8"]
        minh = row["min_abs_H8"]
        margin_table[r] = {}
        for L7g in L7_guesses:
            m = minh / (L7g * Sminus) if L7g * Sminus > 0 else float("inf")
            margin_table[r][L7g] = m
            print("r=%.5f L7=%g -> margin~%.4f" % (r, L7g, m), flush=True)

    payload = {
        "run": "explore_z72loc (NOT RIGOROUS numerical exploration)",
        "u0_re": U0_RE, "u0_im": U0_IM, "u0_abs": float(u0_abs),
        "H7_at_u0_abs": abs(complex(H7.real.mid(), H7.imag.mid())),
        "H8_at_u0_abs": abs(complex(H8.real.mid(), H8.imag.mid())),
        "slope_H8_est": slope_est,
        "radii_rows": rows,
        "margin_table_L7guess": margin_table,
        "x4_common_sha256": sha256(X4_PATH),
        "w33_gh_sha256": sha256(GH_PATH),
        "prec_bits": flint.ctx.prec,
        "elapsed": round(time.time() - t0, 1),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n-> %s (%.1fs)" % (OUT_JSON.name, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
