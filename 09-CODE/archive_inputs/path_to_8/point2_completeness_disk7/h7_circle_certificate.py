# -*- coding: utf-8 -*-
"""Rigorous zero count for H_7 on circles, including infinite l1 tails.

The centre polynomials come from w33.  The full errors of G, h and delta
come from the reproduced CL-34 infinite-dimensional interval Newton
certificate.  At every orbit evaluation an arbitrary l1 function error is
injected as a fresh scalar disk.  This deliberately forgets correlations
but covers every tail mode and every head error.

Each parameter arc is enclosed by an affine complex disk.  If the complete
H_7 image enclosure lies in a disk not containing zero, its argument range
has width < pi.  Rigorous endpoint balls can then be summed without branch
ambiguity to obtain the winding number.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

import flint


ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
DATA_PATH = ROOT / "w33" / "t5_cert_sonnet" / "w33_gh_hiprec.json"
CL34_PATH = ROOT / "w36" / "tail_codex" / "cl34_certificate.json"
OUT_PATH = HERE / "h7_circle_certificate.json"
LOG_PATH = HERE / "h7_circle_certificate.log"

flint.ctx.prec = 512
A = flint.arb
C = flint.acb
ZERO_A = A(0)
ZERO_C = C(0)
ONE_C = C(1)
I = C(0, 1)
PI = A.pi()
TWO_PI = 2 * PI
R_COORD = A("2.5")
AU0 = A("0.41403799908627305889537448439555967803329915886199")
T0 = time.time()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def log(message: str) -> None:
    line = f"[{time.time()-T0:8.2f}s] {message}"
    print(line, flush=True)
    with LOG_PATH.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def mag_ub(z):
    return z.abs_upper()


def mag_lb(z):
    return z.abs_lower()


def up(x):
    return A(x).upper()


def lo(x):
    return A(x).lower()


class AF:
    __slots__ = ("c", "a", "r")

    def __init__(self, c, a=ZERO_C, r=ZERO_A):
        self.c = C(c)
        self.a = C(a)
        self.r = A(r)


def af_const(c):
    return AF(c)


def af_add(x, y):
    return AF(x.c + y.c, x.a + y.a, x.r + y.r)


def af_add_const(x, c):
    return AF(x.c + C(c), x.a, x.r)


def af_scale(x, c):
    c = C(c)
    return AF(x.c * c, x.a * c, x.r * mag_ub(c))


def af_mul(x, y):
    ax = mag_ub(x.a)
    ay = mag_ub(y.a)
    return AF(
        x.c * y.c,
        x.c * y.a + y.c * x.a,
        ax * ay
        + mag_ub(x.c) * y.r
        + mag_ub(y.c) * x.r
        + ax * y.r
        + ay * x.r
        + x.r * y.r,
    )


def af_recip(y):
    centre_lower = mag_lb(y.c)
    rho = mag_ub(y.a) + y.r
    if not (centre_lower > 0 and rho < centre_lower):
        return None
    q = rho / centre_lower
    inv = ONE_C / y.c
    return AF(
        inv,
        -y.a * inv * inv,
        y.r / (centre_lower * centre_lower) + (q * q / (1 - q)) / centre_lower,
    )


def af_horner(coeffs, z):
    value = af_const(ZERO_C)
    for coefficient in reversed(coeffs):
        value = af_add_const(af_mul(value, z), coefficient)
    return value


def af_abs_upper(x):
    return mag_ub(x.c) + mag_ub(x.a) + x.r


def enclosure_metrics(x):
    # ACB is rectangular.  The sum of the real/imaginary radii is a safe
    # Euclidean disk radius around its midpoint.
    cbox_radius = A(x.c.real.rad()) + A(x.c.imag.rad())
    error = cbox_radius + mag_ub(x.a) + x.r
    re = A(x.c.real.mid())
    im = A(x.c.imag.mid())
    midpoint_abs = (re * re + im * im).sqrt()
    lower_abs = midpoint_abs - error
    ratio = error / midpoint_abs if midpoint_abs > 0 else A("inf")
    ball = C(A(re, error), A(im, error))
    return {
        "error": error,
        "midpoint_abs": midpoint_abs,
        "lower_abs": lower_abs,
        "ratio": ratio,
        "ball": ball,
    }


with DATA_PATH.open(encoding="utf-8") as stream:
    data = json.load(stream)
with CL34_PATH.open(encoding="utf-8") as stream:
    cl34 = json.load(stream)

if not cl34.get("pass"):
    raise RuntimeError("CL-34 dependency is not PASS")

eps_g = up(A(cl34["G"]["distance_and_Taylor_tail_upper"]))
eps_h = up(A(cl34["V_h_delta"]["h_error_stored_center_upper"]))
# V_distance is an l1 product-space error and therefore individually
# dominates the delta-coordinate error.
eps_delta = up(A(cl34["V_h_delta"]["V_distance_upper"]))

g_cheb = [A(value) for value in data["g_str"]]
h_cheb = [A(value) for value in data["h_str"]]
N = len(g_cheb)
if N != 100 or len(h_cheb) != N:
    raise RuntimeError("expected 100 centre coefficients")

tcoeff = [[A(0)] * (N + 1) for _ in range(N)]
tcoeff[0][0] = A(1)
tcoeff[1][1] = A(1)
for n in range(2, N):
    for j in range(n + 1):
        value = A(0)
        if j:
            value += 2 * tcoeff[n - 1][j - 1]
        if j <= n - 2:
            value -= tcoeff[n - 2][j]
        tcoeff[n][j] = value


def cheb_to_taylor(values):
    result = []
    for j in range(N):
        result.append(C(sum(
            (values[k] * tcoeff[k][j] * R_COORD ** j for k in range(j, N)),
            A(0),
        )))
    return result


g0 = cheb_to_taylor(g_cheb)
h0 = cheb_to_taylor(h_cheb)
delta0 = A(str(data["delta_rayleigh"]))
delta_ball = C(A(delta0, eps_delta))
s_factor = C(AU0) / (delta_ball ** 7)


def H7_enclosure(u_mid, u_radius):
    u = AF(C(u_mid), C(A(u_radius)))
    s = af_scale(u, s_factor)
    x = af_const(ZERO_C)
    x128 = None
    max_w = A(0)
    for step in range(256):
        w = af_scale(af_add_const(af_mul(x, x), -1), ONE_C / C(R_COORD))
        w_upper = af_abs_upper(w)
        if not (w_upper < 1):
            return None, {"failed": "composition", "step": step, "w_upper": str(w_upper)}
        if w_upper > max_w:
            max_w = w_upper
        vg = af_horner(g0, w)
        vh = af_horner(h0, w)
        x = af_add(vg, af_mul(vh, s))
        # Full infinite-dimensional l1 errors.  Fresh disks at every step
        # are an outer enclosure of the correlations of the actual G and h.
        x.r += eps_g + af_abs_upper(s) * eps_h
        if step + 1 == 128:
            x128 = x
    inv = af_recip(x128)
    if inv is None:
        return None, {"failed": "denominator"}
    return af_mul(x, inv), {"max_w_upper": str(up(max_w))}


def certify_circle(radius_text: str, base_arcs: int, label: str, max_depth: int = 5):
    radius = A(radius_text)
    arcs = []
    all_ok = True
    min_lower = None
    max_ratio = A(0)
    max_w = A(0)
    max_chord = A(0)
    rejected = []
    stack = [
        (Fraction(j, base_arcs), Fraction(j + 1, base_arcs), 0)
        for j in reversed(range(base_arcs))
    ]
    log(f"{label}: radius={radius_text}, base_arcs={base_arcs}, max_depth={max_depth}")
    evaluations = 0
    while stack:
        t1, t2, depth = stack.pop()
        dt = t2 - t1
        tm = (t1 + t2) / 2
        theta = TWO_PI * A(tm.numerator) / A(tm.denominator)
        chord = up(
            2 * radius * (
                PI * A(dt.numerator) / (2 * A(dt.denominator))
            ).sin()
        )
        if chord > max_chord:
            max_chord = chord
        u_mid = C(radius) * (I * C(theta)).exp()
        value, diagnostics = H7_enclosure(u_mid, chord)
        evaluations += 1
        if value is None:
            if depth < max_depth:
                split = (t1 + t2) / 2
                stack.append((split, t2, depth + 1))
                stack.append((t1, split, depth + 1))
            else:
                rejected.append({
                    "t1": str(t1), "t2": str(t2), "depth": depth,
                    "diagnostics": diagnostics,
                })
            continue
        metrics = enclosure_metrics(value)
        passed = bool(lo(metrics["lower_abs"]) > 0 and up(metrics["ratio"]) < 1)
        if not passed:
            if depth < max_depth:
                split = (t1 + t2) / 2
                stack.append((split, t2, depth + 1))
                stack.append((t1, split, depth + 1))
            else:
                rejected.append({
                    "t1": str(t1), "t2": str(t2), "depth": depth,
                    "H_abs_lower": str(lo(metrics["lower_abs"])),
                    "disk_ratio_upper": str(up(metrics["ratio"])),
                })
            continue
        if min_lower is None or lo(metrics["lower_abs"]) < lo(min_lower):
            min_lower = metrics["lower_abs"]
        if metrics["ratio"] > max_ratio:
            max_ratio = metrics["ratio"]
        w_here = A(diagnostics["max_w_upper"])
        if w_here > max_w:
            max_w = w_here
        arcs.append({
            "t1": str(t1),
            "t2": str(t2),
            "depth": depth,
            "pass": True,
            "H_abs_lower": str(lo(metrics["lower_abs"])),
            "disk_ratio_upper": str(up(metrics["ratio"])),
            "max_w_upper": diagnostics["max_w_upper"],
        })
        if len(arcs) % max(1, base_arcs // 4) == 0:
            log(
                f"  accepted={len(arcs)} pending={len(stack)} evals={evaluations} "
                f"depth={depth} |H7|>={lo(metrics['lower_abs'])} ratio<={up(metrics['ratio'])}"
            )

    arcs.sort(key=lambda row: Fraction(row["t1"]))
    all_ok = not rejected and bool(arcs)

    endpoints = {}
    if all_ok:
        endpoint_parameters = sorted(
            {Fraction(row["t1"]) for row in arcs}
            | {Fraction(row["t2"]) for row in arcs}
        )
        for parameter in endpoint_parameters:
            reduced = Fraction(0) if parameter == 1 else parameter
            theta = TWO_PI * A(reduced.numerator) / A(reduced.denominator)
            u = C(radius) * (I * C(theta)).exp()
            value, diagnostics = H7_enclosure(u, A(0))
            if value is None:
                all_ok = False
                endpoints[parameter] = None
            else:
                endpoints[parameter] = enclosure_metrics(value)["ball"]

    count = None
    winding_ball = None
    if all_ok:
        total = A(0)
        for row in arcs:
            t1 = Fraction(row["t1"])
            t2 = Fraction(row["t2"])
            total += (endpoints[t2] / endpoints[t1]).arg()
        winding_ball = total / TWO_PI
        candidate = int(round(float(winding_ball.mid())))
        if ((winding_ball - candidate).contains(0)
                and not (winding_ball - (candidate - 1)).contains(0)
                and not (winding_ball - (candidate + 1)).contains(0)):
            count = candidate

    result = {
        "label": label,
        "radius": radius_text,
        "base_arcs": base_arcs,
        "max_depth_allowed": max_depth,
        "accepted_arcs": len(arcs),
        "arc_evaluations": evaluations,
        "max_chord_upper": str(max_chord),
        "rejected": rejected,
        "boundary_pass": all_ok,
        "count": count,
        "winding_ball": str(winding_ball) if winding_ball is not None else None,
        "min_H7_abs_lower": str(lo(min_lower)) if min_lower is not None else None,
        "max_disk_ratio_upper": str(up(max_ratio)),
        "max_composition_w_upper": str(up(max_w)),
        "arcs": arcs,
        "pass": all_ok and count is not None,
    }
    log(
        f"{label}: boundary={all_ok}, count={count}, min|H7|>={result['min_H7_abs_lower']}, "
        f"maxratio<={result['max_disk_ratio_upper']}"
    )
    return result


def main():
    LOG_PATH.write_text("", encoding="utf-8")
    log(f"PREC=512 epsG<={eps_g} epsH<={eps_h} epsDelta<={eps_delta}")
    main_result = certify_circle("7.0", 64, "MAIN_R7_EXPECT_2", max_depth=5)
    nested_control = certify_circle("5.0", 32, "CONTROL_R5_EXPECT_1", max_depth=5)
    coarse_rejection = certify_circle(
        "7.0", 4, "NEGATIVE_CONTROL_COARSE_ARCS_MUST_REJECT", max_depth=0
    )
    overall = (
        main_result["pass"] and main_result["count"] == 2
        and nested_control["pass"] and nested_control["count"] == 1
        and not coarse_rejection["pass"]
    )
    payload = {
        "status": "RIGOROUS_H7_ARGUMENT_PRINCIPLE_WITH_INFINITE_L1_TAILS",
        "precision_bits": 512,
        "dependencies": {
            "centres": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"),
            "centres_sha256": sha256(DATA_PATH),
            "CL34": str(CL34_PATH.relative_to(ROOT)).replace("\\", "/"),
            "CL34_sha256": sha256(CL34_PATH),
        },
        "full_errors": {
            "G_l1_upper": str(eps_g),
            "h_l1_stored_centre_upper": str(eps_h),
            "delta_upper": str(eps_delta),
        },
        "main": main_result,
        "nested_control": nested_control,
        "negative_control": coarse_rejection,
        "pass": overall,
        "wall_s": time.time() - T0,
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"OVERALL PASS={overall}; wrote {OUT_PATH}")
    if not overall:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
