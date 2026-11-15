# -*- coding: utf-8 -*-
"""Midpoint risk gate for the spectral-projector route.

This is deliberately NOT a certificate.  The Taylor conversion and dual
power-series evaluation are the same algorithms as in
  w33/t3_lit_codex/spectral_audit.py
and
  w34/w1_cert/w1_hcert_M99.py,
but evaluated in float64 for the requested first-hour gate.

All generated files stay in w36/proj_codex.
"""
from __future__ import annotations

import json
import math
import os
import time
from pathlib import Path

import numpy as np


ROOT = Path(r"D:\Исследования\И-1 — Нули функции H\Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
DATA = ROOT / "w33" / "t5_cert_sonnet" / "w33_gh_hiprec.json"
LOG_PATH = HERE / "midpoint_probe.log"
JSON_PATH = HERE / "midpoint_probe.json"
CACHE_PATH = HERE / "dt100_midpoint.npz"

R_DISC = 2.5
DELTA = 4.669201609102990671853
SLICE_W0 = -1.0 / R_DISC  # X=0 corresponds to w=(X-1)/2.5=-0.4


class Logger:
    def __init__(self, path: Path):
        self.f = path.open("w", encoding="utf-8", buffering=1)

    def __call__(self, msg: str):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        self.f.write(line + "\n")
        self.f.flush()
        os.fsync(self.f.fileno())

    def close(self):
        self.f.close()


log = Logger(LOG_PATH)


def cheb_to_taylor(c: np.ndarray) -> np.ndarray:
    """Existing Chebyshev -> Taylor map for w=(X-1)/2.5."""
    m = len(c)
    t = np.zeros((m, m), dtype=np.float64)
    t[0, 0] = 1.0
    if m > 1:
        t[1, 1] = 1.0
    for n in range(2, m):
        t[n, 1 : n + 1] += 2.0 * t[n - 1, :n]
        t[n, : n - 1] -= t[n - 2, : n - 1]
    powers = R_DISC ** np.arange(m)
    return (c[:, None] * t).sum(axis=0) * powers


def ps_mul(a: np.ndarray, b: np.ndarray, m: int) -> np.ndarray:
    return np.convolve(a, b)[:m]


def dual_mul(a, b, m: int):
    av, ad = a
    bv, bd = b
    return ps_mul(av, bv, m), ps_mul(av, bd, m) + ps_mul(ad, bv, m)


def dual_compose(cv: np.ndarray, cd: np.ndarray, arg, m: int):
    v = np.zeros(m, dtype=np.float64)
    d = np.zeros(m, dtype=np.float64)
    for k in range(m - 1, -1, -1):
        v, d = dual_mul((v, d), arg, m)
        v[0] += cv[k]
        d[0] += cd[k]
    return v, d


def t_and_dt(g: np.ndarray, direction: np.ndarray):
    """T(g), DT(g)[direction], verbatim dual-number computation."""
    m = len(g)
    a = g[0]
    da = direction[0]
    a2 = a * a
    da2 = 2.0 * a * da

    u = np.zeros(m, dtype=np.float64)
    du = np.zeros(m, dtype=np.float64)
    u[0] = (a2 - 1.0) / R_DISC
    du[0] = da2 / R_DISC
    if m > 1:
        u[1] = a2
        du[1] = da2

    gin = dual_compose(g, direction, (u, du), m)
    gs = dual_mul(gin, gin, m)
    v = gs[0] / R_DISC
    dv = gs[1] / R_DISC
    v = v.copy()
    v[0] -= 1.0 / R_DISC

    gout = dual_compose(g, direction, (v, dv), m)
    tv = gout[0] / a
    td = gout[1] / a - gout[0] * da / (a * a)
    return tv, td


def build_matrices(g: np.ndarray):
    """Full 100-mode block and invariant q(0)=0 slice (99 coordinates)."""
    m = len(g)
    full = np.zeros((m, m), dtype=np.float64)
    sl = np.zeros((m - 1, m - 1), dtype=np.float64)
    t0 = time.time()
    for j in range(m):
        e = np.zeros(m, dtype=np.float64)
        e[j] = 1.0
        _, y = t_and_dt(g, e)
        full[:, j] = y
        if j >= 1:
            # b_j=e_j-w0^j e_0 has b_j(X=0)=0.
            d = e.copy()
            d[0] = -(SLICE_W0 ** j)
            _, ys = t_and_dt(g, d)
            sl[:, j - 1] = ys[1:]
        if j % 10 == 0 or j == m - 1:
            elapsed = time.time() - t0
            rate = elapsed / (j + 1)
            eta = rate * (m - j - 1)
            log(f"DT columns {j + 1}/{m}; elapsed={elapsed:.1f}s; ETA={eta:.1f}s")
    return full, sl


def induced_slice_norm_upper(b: np.ndarray) -> float:
    """Safe upper bound for ambient Taylor-l1 norm on q(0)=0.

    If x=(q_1,...), then ||q||_1=||x||_1+|sum_j w0^j x_j| >= ||x||_1,
    and the reconstructed output has norm at most 1.4*||Bx||_1.
    """
    return (1.0 + abs(SLICE_W0)) * np.linalg.norm(b, 1)


def reconstructed_column_norms(b: np.ndarray) -> np.ndarray:
    """Ambient l1 norms of the images of the slice basis b_j."""
    weights = SLICE_W0 ** np.arange(1, b.shape[0] + 1)
    constants = -(weights @ b)
    return np.abs(constants) + np.abs(b).sum(axis=0)


def main():
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    gc = np.array([float(x) for x in raw["g_str"]], dtype=np.float64)
    hc = np.array([float(x) for x in raw["h_str"]], dtype=np.float64)
    g = cheb_to_taylor(gc)
    h = cheb_to_taylor(hc)
    m = len(g)
    log(f"M={m}; midpoint=float64; basis w=(X-1)/2.5")
    log(f"||G||_1={np.linalg.norm(g,1):.16g}; ||h||_1={np.linalg.norm(h,1):.16g}")
    log(f"G(X=0)-1={np.polynomial.polynomial.polyval(SLICE_W0,g)-1:.3e}; "
        f"h(X=0)={np.polynomial.polynomial.polyval(SLICE_W0,h):.3e}")

    if CACHE_PATH.exists():
        z = np.load(CACHE_PATH)
        full, sl = z["full"], z["slice"]
        log(f"loaded cached matrices from {CACHE_PATH.name}")
    else:
        full, sl = build_matrices(g)
        np.savez_compressed(CACHE_PATH, full=full, slice=sl, g=g, h=h)
        log(f"saved matrices to {CACHE_PATH.name}")

    tg, dth = t_and_dt(g, h)
    log(f"sanity ||T(G)-G||_1={np.linalg.norm(tg-g,1):.6e}")
    log(f"sanity ||DT(G)h-delta*h||_1={np.linalg.norm(dth-DELTA*h,1):.6e}")
    log(f"||DT_full||_1={np.linalg.norm(full,1):.12g}; "
        f"slice coordinate ||B||_1={np.linalg.norm(sl,1):.12g}; "
        f"slice ambient upper={induced_slice_norm_upper(sl):.12g}")

    # Full left delta eigenfunctional: this reproduces the independent 1.1049 probe.
    ewf, evf = np.linalg.eig(full.T)
    il = int(np.argmin(np.abs(ewf - DELTA)))
    lvec = np.real_if_close(evf[:, il]).real
    lvec /= np.dot(lvec, h)
    lres = np.linalg.norm(full.T @ lvec - ewf[il] * lvec, np.inf)
    log(f"left eigenvalue(full)={ewf[il]:.16g}; ||l||_inf={np.linalg.norm(lvec,np.inf):.12g}; "
        f"argmax={int(np.argmax(np.abs(lvec)))}; residual_inf={lres:.3e}")

    ews = np.linalg.eigvals(sl)
    order = np.argsort(np.abs(ews))[::-1]
    top = [(complex(ews[i]), float(abs(ews[i]))) for i in order[:8]]
    log("slice eigenvalues by modulus: " + "; ".join(f"{z.real:+.12g}{z.imag:+.3g}i |.|={a:.12g}" for z,a in top))

    samples = {}
    for radius in (0.35, 0.5):
        rows = []
        for k in range(16):
            theta = 2.0 * math.pi * k / 16.0
            z = radius * np.exp(1j * theta)
            inv = np.linalg.inv(z * np.eye(m - 1) - sl)
            coord = float(np.linalg.norm(inv, 1))
            amb_upper = induced_slice_norm_upper(inv)
            col_actual = float(reconstructed_column_norms(inv).max())
            rows.append(dict(k=k, theta=theta, z_real=float(z.real), z_imag=float(z.imag),
                             resolvent_coord_l1=coord,
                             resolvent_ambient_basis_columns=col_actual,
                             resolvent_ambient_upper=amb_upper))
            log(f"r={radius:.2f} point={k:02d}/15 theta={theta:.6f}: "
                f"||R||_1(coord)={coord:.9g}; ambient_basis={col_actual:.9g}; "
                f"ambient_upper={amb_upper:.9g}")
        sup_coord = max(x["resolvent_coord_l1"] for x in rows)
        sup_ambient_basis = max(x["resolvent_ambient_basis_columns"] for x in rows)
        sup_ambient_upper = max(x["resolvent_ambient_upper"] for x in rows)
        samples[str(radius)] = dict(rows=rows, sup_coord=sup_coord,
                                    sup_ambient_basis=sup_ambient_basis,
                                    sup_ambient_upper=sup_ambient_upper,
                                    C_s_coord=radius * sup_coord,
                                    C_s_ambient_upper=radius * sup_ambient_upper,
                                    mu=radius)
        log(f"r={radius:.2f} SUMMARY: sup_coord={sup_coord:.12g}; "
            f"sup_ambient_basis={sup_ambient_basis:.12g}; "
            f"sup_ambient_upper={sup_ambient_upper:.12g}; "
            f"C_s<=r*sup={radius*sup_ambient_upper:.12g} (midpoint-grid only)")

    pperp_triangle = 1.0 + np.linalg.norm(h, 1) * np.linalg.norm(lvec, np.inf)
    output = {
        "status": "MIDPOINT_ONLY_NOT_A_CERTIFICATE",
        "M_full": m,
        "M_slice": m - 1,
        "basis": "Taylor w=(X-1)/2.5; invariant slice q(X=0)=0",
        "g_l1": float(np.linalg.norm(g, 1)),
        "h_l1": float(np.linalg.norm(h, 1)),
        "slice_constraint_g_error": float(np.polynomial.polynomial.polyval(SLICE_W0, g) - 1.0),
        "slice_constraint_h_error": float(np.polynomial.polynomial.polyval(SLICE_W0, h)),
        "DT_full_l1": float(np.linalg.norm(full, 1)),
        "DT_slice_coordinate_l1": float(np.linalg.norm(sl, 1)),
        "left_delta": float(np.real(ewf[il])),
        "left_linf": float(np.linalg.norm(lvec, np.inf)),
        "left_argmax": int(np.argmax(np.abs(lvec))),
        "left_residual_inf": float(lres),
        "projector_triangle_bound_midpoint": float(pperp_triangle),
        "slice_top_eigenvalues": [dict(real=float(z.real), imag=float(z.imag), abs=a) for z,a in top],
        "samples": samples,
    }
    JSON_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"midpoint ||P_perp||_1 <= 1+||h||_1||l||_inf = {pperp_triangle:.12g}")
    log(f"wrote {JSON_PATH.name}; DONE")
    log.close()


if __name__ == "__main__":
    main()
