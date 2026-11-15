# -*- coding: utf-8 -*-
"""512-bit Arb certification of the 100-mode block.

Scope of the certificate:
  * interval construction of DT(G0), full and on q(X=0)=0;
  * interval LU for resolvents on circular grids and resolvent-identity
    coverage between nodes;
  * a finite-block interval-Newton/radii-polynomial enclosure of the left
    delta eigenpair, with explicit G/h-ball perturbations;
  * explicit analytic block-tail bounds from composition contraction.

The final report separately states the remaining dynamical (nonautonomous)
assumption needed to turn these local operator bounds into a theorem for the
whole telescope.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import flint
import numpy as np


ROOT = Path(r"D:\Исследования\И-1 — Нули функции H\Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
LOG_PATH = HERE / "rigorous_block.log"
JSON_PATH = HERE / "rigorous_block.json"
MID_CACHE = HERE / "dt100_midpoint.npz"

os.environ.setdefault("UNC_PREC", "512")
sys.path.insert(0, str(ROOT / "w34" / "w1_cert"))
# Reuse the project's 100-coefficient input/conversion implementation.
from w1_uncond_common_M99 import tc_g, tc_h  # noqa: E402

flint.ctx.prec = 512

M = len(tc_g)
NS = M - 1
R_DISC = flint.arb("2.5")
W0 = flint.arb("-0.4")
DELTA_REF = flint.arb(
    "4.66920160910299067185320382046620161725818557747576863274565134300413"
)
RHO_G = flint.arb("1e-20")
RHO_H = flint.arb("1e-27")
K_D2 = flint.arb("223.77")
SIGMA = flint.arb("1.38")
N_GRID = 128

ZERO = flint.acb(0)
ONE = flint.acb(1)


class Logger:
    def __init__(self, path: Path):
        self.f = path.open("w", encoding="utf-8", buffering=1)
        self.t0 = time.time()

    def __call__(self, msg: str):
        line = f"[{time.strftime('%H:%M:%S')} +{time.time()-self.t0:7.1f}s] {msg}"
        print(line, flush=True)
        self.f.write(line + "\n")
        self.f.flush()
        os.fsync(self.f.fileno())

    def close(self):
        self.f.close()


log = Logger(LOG_PATH)


def ub(x) -> float:
    """A binary64 number rounded one ulp upward from an Arb upper endpoint."""
    if hasattr(x, "upper"):
        x = x.upper()
    return math.nextafter(float(x), math.inf)


def lb(x) -> float:
    if hasattr(x, "lower"):
        x = x.lower()
    return math.nextafter(float(x), -math.inf)


def ps_add(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def ps_sub(a, b):
    return [a[i] - b[i] for i in range(len(a))]


def ps_scale(a, c):
    return [x * c for x in a]


def ps_mul(a, b):
    m = len(a)
    z = [ZERO] * m
    for i in range(m):
        if a[i] == ZERO:
            continue
        for j in range(m - i):
            if b[j] != ZERO:
                z[i + j] += a[i] * b[j]
    return z


def dual_mul(a, b):
    return ps_mul(a[0], b[0]), ps_add(ps_mul(a[0], b[1]), ps_mul(a[1], b[0]))


def dual_compose(cv, cd, arg):
    v = [ZERO] * M
    d = [ZERO] * M
    for k in range(M - 1, -1, -1):
        v, d = dual_mul((v, d), arg)
        v[0] += cv[k]
        d[0] += cd[k]
    return v, d


def t_and_dt(g, direction):
    a, da = g[0], direction[0]
    a2, da2 = a * a, 2 * a * da
    u, du = [ZERO] * M, [ZERO] * M
    u[0], du[0] = (a2 - 1) / R_DISC, da2 / R_DISC
    u[1], du[1] = a2, da2
    gin = dual_compose(g, direction, (u, du))
    gs = dual_mul(gin, gin)
    v, dv = ps_scale(gs[0], 1 / R_DISC), ps_scale(gs[1], 1 / R_DISC)
    v[0] -= 1 / R_DISC
    gout = dual_compose(g, direction, (v, dv))
    return ps_scale(gout[0], 1 / a), ps_add(ps_scale(gout[1], 1 / a), ps_scale(gout[0], -da / (a * a)))


def mat_norm1(a: flint.acb_mat):
    best = flint.arb(0)
    for j in range(a.ncols()):
        s = flint.arb(0)
        for i in range(a.nrows()):
            s += abs(a[i, j])
        if s.upper() > best.upper():
            best = s.upper()
    return best


def mat_norm_inf(a: flint.acb_mat):
    best = flint.arb(0)
    for i in range(a.nrows()):
        s = flint.arb(0)
        for j in range(a.ncols()):
            s += abs(a[i, j])
        if s.upper() > best.upper():
            best = s.upper()
    return best


def vec_norm_inf(a: flint.acb_mat):
    best = flint.arb(0)
    for i in range(a.nrows()):
        x = abs(a[i, 0])
        if x.upper() > best.upper():
            best = x.upper()
    return best


def build_dt():
    full = flint.acb_mat(M, M)
    sl = flint.acb_mat(NS, NS)
    t0 = time.time()
    for j in range(M):
        e = [ZERO] * M
        e[j] = ONE
        _, y = t_and_dt(tc_g, e)
        for i in range(M):
            full[i, j] = y[i]
        if j >= 1:
            d = [ZERO] * M
            d[j] = ONE
            d[0] = -(W0 ** j)
            _, ys = t_and_dt(tc_g, d)
            for i in range(1, M):
                sl[i - 1, j - 1] = ys[i]
        if j % 10 == 0 or j == M - 1:
            elapsed = time.time() - t0
            eta = elapsed / (j + 1) * (M - j - 1)
            log(f"Arb DT columns {j+1}/{M}; elapsed={elapsed:.1f}s; ETA={eta:.1f}s")
    return full, sl


def poly_mul(a, b, n):
    z = [ZERO] * n
    for i, ai in enumerate(a):
        if i >= n:
            break
        for j, bj in enumerate(b):
            if i + j >= n:
                break
            z[i + j] += ai * bj
    return z


def poly_comp_affine(c, u, n):
    z = [ZERO] * n
    for ck in reversed(c):
        z = poly_mul(z, u, n)
        z[0] += ck
    return z


def weighted_l1(c, sigma):
    s = flint.arb(0)
    p = flint.arb(1)
    for x in c:
        s += abs(x) * p
        p *= sigma
    return s


def majorant(c, q):
    s = flint.arb(0)
    p = flint.arb(1)
    for x in c:
        s += abs(x) * p
        p *= q
    return s


def derivative_majorant(c, q):
    s = flint.arb(0)
    p = flint.arb(1)
    for k in range(1, len(c)):
        s += flint.arb(k) * abs(c[k]) * p
        p *= q
    return s


def analytic_tail_bounds():
    """Bounds for the head/tail blocks in ordinary Taylor l1 coordinates."""
    n_poly = 2 * M
    a0 = tc_g[0]
    a2 = a0 * a0
    u = [ZERO] * n_poly
    u[0], u[1] = (a2 - 1) / R_DISC, a2
    gin = poly_comp_affine(tc_g, u, n_poly)
    b = [x / R_DISC for x in poly_mul(gin, gin, n_poly)]
    b[0] -= 1 / R_DISC

    # Perturb G0 by the certified ambient l1 radius rho_G.
    abs_a0 = abs(a0)
    da2 = RHO_G * (2 * abs_a0 + RHO_G)

    def center_and_ball(sigma):
        q_u0 = abs(u[0]) + abs(u[1]) * sigma
        du = da2 * (1 / R_DISC + sigma)
        q_u = q_u0 + du
        gp_u0 = derivative_majorant(tc_g, q_u)
        d_gin = RHO_G + gp_u0 * du
        gin0_w = weighted_l1(gin, sigma)
        q_b0 = weighted_l1(b, sigma)
        d_b = (2 * gin0_w + d_gin) * d_gin / R_DISC
        q_b = q_b0 + d_b
        return q_u0, q_u, q_b0, q_b

    q_u0_1, q_u_1, q_b0_1, q_b_1 = center_and_ball(flint.arb(1))
    q_u0_s, q_u_s, q_b0_s, q_b_s = center_and_ball(SIGMA)

    if not (q_u_s < 1 and q_b_s < 1):
        raise RuntimeError("weighted composition does not contract")

    # Directional multiplier for da=0 and tail-supported inputs.
    gu_1 = majorant(tc_g, q_u_1) + RHO_G
    gpb_1 = derivative_majorant(tc_g, q_b_1) + RHO_G / ((1 - q_b_1) ** 2)
    wind_1 = (2 / R_DISC) * gu_1 * gpb_1
    a_inv = 1 / (abs_a0 - RHO_G)
    tail_action = a_inv * (q_b_1 ** M + wind_1 * q_u_1 ** M)

    # Weighted full derivative bound for head -> output modes >= M.
    gu_s = majorant(tc_g, q_u_s) + RHO_G
    gpu_s = derivative_majorant(tc_g, q_u_s) + RHO_G / ((1 - q_u_s) ** 2)
    gb_s = majorant(tc_g, q_b_s) + RHO_G
    gpb_s = derivative_majorant(tc_g, q_b_s) + RHO_G / ((1 - q_b_s) ** 2)
    du_dir = 2 * (abs_a0 + RHO_G) * (1 / R_DISC + SIGMA)
    dgin_dir = 1 + gpu_s * du_dir
    db_dir = (2 / R_DISC) * gu_s * dgin_dir
    weighted_dt = a_inv * (1 + gpb_s * db_dir) + (a_inv ** 2) * gb_s
    head_to_tail_ambient = weighted_dt * (SIGMA ** (-M))

    # Coordinate slice: a head coordinate vector has ambient norm <=1.4.
    head_to_tail_slice = flint.arb("1.4") * head_to_tail_ambient
    # A tail slice coordinate has an extra constant coefficient <=0.4^M.
    tail_to_all_slice = tail_action + (abs(W0) ** M) * weighted_dt
    out = dict(
        q_u_1=q_u_1,
        q_b_1=q_b_1,
        q_u_sigma=q_u_s,
        q_b_sigma=q_b_s,
        weighted_dt=weighted_dt,
        tail_action_full=tail_action,
        head_to_tail_ambient=head_to_tail_ambient,
        head_to_tail_slice=head_to_tail_slice,
        tail_to_all_slice=tail_to_all_slice,
    )
    for k, v in out.items():
        log(f"tail {k} <= {v}")
    return out


def finite_left_certificate(full, tail):
    cache = np.load(MID_CACHE)
    af = cache["full"]
    hf = cache["h"]
    ew, ev = np.linalg.eig(af.T)
    ii = int(np.argmin(np.abs(ew - float(DELTA_REF))))
    lam0f = float(np.real(ew[ii]))
    lf = np.real(ev[:, ii])
    lf /= float(np.dot(lf, hf))

    n = M + 1
    x0 = flint.acb_mat(n, 1)
    for i in range(M):
        x0[i, 0] = flint.acb(repr(float(lf[i])))
    x0[M, 0] = flint.acb(repr(lam0f))

    f = flint.acb_mat(n, 1)
    lam0 = x0[M, 0]
    for i in range(M):
        s = ZERO
        for j in range(M):
            s += full[j, i] * x0[j, 0]
        f[i, 0] = s - lam0 * x0[i, 0]
    s = ZERO
    for j in range(M):
        s += tc_h[j] * x0[j, 0]
    f[M, 0] = s - 1

    jmat = flint.acb_mat(n, n)
    for i in range(M):
        for j in range(M):
            jmat[i, j] = full[j, i] - (lam0 if i == j else ZERO)
        jmat[i, M] = -x0[i, 0]
    for j in range(M):
        jmat[M, j] = tc_h[j]

    ymat = jmat.inv()
    ynorm = mat_norm_inf(ymat)
    yf = ymat * f
    y = vec_norm_inf(yf)
    ident = flint.acb_mat(n, n)
    for i in range(n):
        ident[i, i] = 1
    z0 = mat_norm_inf(ident - ymat * jmat)

    # True-G finite-block perturbation plus the rigorously bounded tail Schur term.
    lam_lo = DELTA_REF - flint.arb("1e-10")
    dlam = 1 / (lam_lo - tail["tail_action_full"])
    tail_schur = tail["head_to_tail_ambient"] * dlam * tail["tail_action_full"]
    eps_a = K_D2 * RHO_G + tail_schur
    l0norm = max(abs(x0[i, 0]) for i in range(M))
    f_param = eps_a * l0norm + RHO_H * l0norm
    y_total = y + ynorm * f_param
    z_param = ynorm * (eps_a + RHO_H)
    zlin = 2 * ynorm

    # Find an explicit radius with p(r)=zlin*r^2-(1-z0-zparam)r+y_total < 0.
    denom = 1 - z0 - z_param
    rho = 2 * y_total / denom
    pval = zlin * rho * rho - denom * rho + y_total
    if not (pval < 0):
        raise RuntimeError(f"left radii polynomial did not close: p={pval}")

    # Tail of the left functional from the adjoint tail equation.
    lhead = l0norm + rho
    ltail = dlam * tail["tail_action_full"] * lhead

    # Optimize an extension of the restricted functional by adding c*q(X=0).
    # Fixed rational c is enough for a rigorous upper bound.
    c_ann = flint.arb("-1.39051")
    ext_head = flint.arb(0)
    for i in range(M):
        val = abs(x0[i, 0] + c_ann * (W0 ** i)) + rho
        if val.upper() > ext_head.upper():
            ext_head = val.upper()
    ext_tail = ltail + abs(c_ann) * (abs(W0) ** M)
    l_slice_dual = max(ext_head, ext_tail)
    hnorm = sum(abs(x) for x in tc_h) + RHO_H
    pu = hnorm * l_slice_dual
    ps_triangle = 1 + pu

    result = dict(
        lambda_mid=lam0f,
        raw_residual=vec_norm_inf(f),
        Y_inf=ynorm,
        YF_inf=y,
        Z0=z0,
        parameter_operator_error=eps_a,
        radii_rho=rho,
        radii_p=pval,
        l_full_head_inf=lhead,
        l_tail_inf=ltail,
        annihilator_c=c_ann,
        l_slice_dual=l_slice_dual,
        h_l1=hnorm,
        Pu_l1=pu,
        Pperp_triangle_l1=ps_triangle,
    )
    for k, v in result.items():
        log(f"left {k} <= {v}" if k not in ("lambda_mid", "annihilator_c") else f"left {k} = {v}")
    return result


def stable_power2_certificate(sl, left, tail):
    """Certify that the complement of delta has spectrum inside |z|=0.35.

    The finite midpoint product is enclosed by Arb.  The passage to the true
    infinite operator is bounded by a block perturbation estimate; the latter
    is intentionally coarse, since the available margin to 0.35^2 is large.
    """
    cache = np.load(MID_CACHE)
    af = cache["full"]
    hf = cache["h"]
    ew, ev = np.linalg.eig(af.T)
    ii = int(np.argmin(np.abs(ew - float(DELTA_REF))))
    lf = np.real(ev[:, ii])
    lf /= float(np.dot(lf, hf))

    # Restricted covector in coordinates x=(q_1,...,q_99):
    # q_0=-sum_j w0^j x_j, hence ell_red,j=ell_j-ell_0*w0^j.
    lr = []
    for j in range(1, M):
        lr.append(flint.acb(repr(float(lf[j]))) - flint.acb(repr(float(lf[0]))) * (W0 ** j))
    hs = [tc_h[j] for j in range(1, M)]
    p0 = flint.acb_mat(NS, NS)
    for i in range(NS):
        for j in range(NS):
            p0[i, j] = (1 if i == j else 0) - hs[i] * lr[j]
    ap0 = sl * p0
    a2p0 = sl * ap0
    p0norm = mat_norm1(p0)
    ap0norm = mat_norm1(ap0)
    a2p0norm = mat_norm1(a2p0)

    # Infinite-coordinate perturbation A-Abar, where Abar is the 99x99
    # head block extended by zero on the tail.
    eps_head = flint.arb("1.4") * K_D2 * RHO_G
    eps_inf = max(eps_head + tail["head_to_tail_slice"], tail["tail_to_all_slice"])
    abar = mat_norm1(sl)
    atrue = abar + eps_inf

    rho_l = left["radii_rho"]
    dl_head = flint.arb("1.4") * rho_l
    dl_tail = left["l_tail_inf"] + left["l_full_head_inf"] * (abs(W0) ** M)
    dl = max(dl_head, dl_tail)
    lr0norm = max(abs(x) for x in lr)
    hnorm = left["h_l1"]
    pdiff = hnorm * dl + RHO_H * (lr0norm + dl)
    pbar_coarse = 1 + hnorm * lr0norm

    a2diff = (2 * abar + eps_inf) * eps_inf
    correction = a2diff * pbar_coarse + (atrue ** 2) * pdiff
    a2p_coord = a2p0norm + correction
    a2p_ambient = flint.arb("1.4") * a2p_coord
    stable_radius = a2p_ambient.sqrt()

    result = dict(
        P0_coordinate_l1=p0norm,
        AP0_coordinate_l1=ap0norm,
        A2P0_coordinate_l1=a2p0norm,
        infinite_operator_perturbation_coordinate=eps_inf,
        projector_perturbation_coordinate=pdiff,
        A2P_coordinate=a2p_coord,
        A2P_ambient=a2p_ambient,
        stable_spectral_radius=stable_radius,
        circle_035_squared=flint.arb("0.1225"),
    )
    for k, v in result.items():
        log(f"stable {k} <= {v}")
    if not (a2p_ambient < flint.arb("0.1225")):
        raise RuntimeError("failed to put stable spectrum inside r=0.35")
    return result


def node_full_resolvent_bound(m0, radius, tail):
    """Lift finite head inverse norm to the infinite slice coordinate l1 norm."""
    eps_head = flint.arb("1.4") * K_D2 * RHO_G
    m_head = m0 / (1 - m0 * eps_head)
    a_tt = tail["tail_to_all_slice"]
    d_inv = 1 / (radius - a_tt)
    b = tail["tail_to_all_slice"]
    c = tail["head_to_tail_slice"]
    eta = m_head * b * d_inv * c
    s_inv = m_head / (1 - eta)
    head_col = s_inv * (1 + d_inv * c)
    tail_col = d_inv + s_inv * b * d_inv * (1 + d_inv * c)
    return max(head_col, tail_col), dict(m_head=m_head, d_inv=d_inv, eta=eta,
                                         head_col=head_col, tail_col=tail_col)


def resolvent_circle(sl, radius_s: str, tail):
    radius = flint.arb(radius_s)
    node_bounds = []
    worst_meta = None
    worst_k = None
    eye = flint.acb_mat(NS, NS)
    for i in range(NS):
        eye[i, i] = 1
    for k in range(N_GRID):
        theta = 2 * flint.arb.pi() * flint.arb(k) / flint.arb(N_GRID)
        z = flint.acb(radius * theta.cos(), radius * theta.sin())
        mat = -sl
        for i in range(NS):
            mat[i, i] += z
        inv = mat.inv()
        m0 = mat_norm1(inv)
        mf, meta = node_full_resolvent_bound(m0, radius, tail)
        node_bounds.append(mf)
        if worst_k is None or mf.upper() > node_bounds[worst_k].upper():
            worst_k, worst_meta = k, meta
        if k % 16 == 0 or k == N_GRID - 1:
            log(f"resolvent r={radius_s} nodes {k+1}/{N_GRID}; current <= {mf}")
    grid_sup = max(node_bounds, key=lambda x: x.upper())
    chord = 2 * radius * (flint.arb.pi() / (2 * N_GRID)).sin()
    lip_product = grid_sup * chord
    if not (lip_product < 1):
        raise RuntimeError(f"resolvent grid too coarse: M*d={lip_product}")
    continuous_coord = grid_sup / (1 - lip_product)
    continuous_ambient = flint.arb("1.4") * continuous_coord
    cs = radius * continuous_ambient
    result = dict(
        radius=radius,
        n_grid=N_GRID,
        worst_node=worst_k,
        grid_sup_coordinate=grid_sup,
        chord=chord,
        lipschitz_product=lip_product,
        continuous_sup_coordinate=continuous_coord,
        continuous_sup_ambient=continuous_ambient,
        C_s=cs,
        worst_meta=worst_meta,
    )
    log(f"resolvent r={radius_s} GRID sup(coord) <= {grid_sup}")
    log(f"resolvent r={radius_s} chord <= {chord}; M*d <= {lip_product}")
    log(f"resolvent r={radius_s} CONTINUOUS sup(ambient) <= {continuous_ambient}; C_s <= {cs}")
    return result


def serial(obj):
    if isinstance(obj, dict):
        return {k: serial(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serial(v) for v in obj]
    if isinstance(obj, (flint.arb, flint.acb)):
        return {"ball": str(obj), "upper_float": ub(abs(obj)), "lower_float": lb(abs(obj))}
    return obj


def main():
    log(f"START prec={flint.ctx.prec} bits; M={M}; slice dimension={NS}")
    full, sl = build_dt()
    log(f"finite ||DT_full||_1 <= {mat_norm1(full)}")
    log(f"finite ||DT_slice_coordinate||_1 <= {mat_norm1(sl)}")
    tail = analytic_tail_bounds()
    left = finite_left_certificate(full, tail)
    stable = stable_power2_certificate(sl, left, tail)
    circles = {
        "0.35": resolvent_circle(sl, "0.35", tail),
        "0.5": resolvent_circle(sl, "0.5", tail),
    }
    out = {
        "status": "RIGOROUS_100_MODE_BLOCK_AND_ANALYTIC_BLOCK_TAIL",
        "precision_bits": flint.ctx.prec,
        "M_full": M,
        "M_slice": NS,
        "tail": tail,
        "left": left,
        "stable": stable,
        "circles": circles,
    }
    JSON_PATH.write_text(json.dumps(serial(out), ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"wrote {JSON_PATH.name}; DONE")
    log.close()


if __name__ == "__main__":
    main()
