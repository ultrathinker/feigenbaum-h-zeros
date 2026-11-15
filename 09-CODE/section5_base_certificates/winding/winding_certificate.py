# -*- coding: utf-8 -*-
"""winding_certificate.py -- строгий (интервальный, Arb, направленное округление)
сертификат: wind(x_{2^m}, Gamma) = 0 на контуре каждого из 23 кольцевых дисков
(+ 2 доп. диска радиуса 1/6, best-effort), где x_{2^m} -- ЗНАМЕНАТЕЛЬ отношения
H_m = x_{2^{m+1}}/x_{2^m}.

Задача (article_v1/v3_work/WINDING_BRIEF.md, oid:9595c48c, волна v3, 13.08.2026)
--------------------------------------------------------------------------------
REPORT_POLES.md (v2_work/poles) уже проверил ЧИСЛЕННО (точечная арифметика
flint.acb, NOT RIGOROUS): wind(x_{2^m})=0 на всех 23 контурах, min|x_{2^m}| на
контуре >= 2.367e-3. Эта программа делает то же самое СТРОГО: интервальная
(affine, disk-symbol) арифметика Arb с направленным округлением, как во всех
проверенных сертификатах архива (census_A/B, point14, point17, point3B_fix1).

МЕТОД (заимствован БЕЗ переоткрытия из уже проверенного кода архива)
--------------------------------------------------------------------
Ключевой строительный блок -- "light single-symbol AF" winding из
`path_to_8/point10_layer1_census_A/census_A_certificate.py`, функции
`H7_light`/`compute_winding` (строки ~304-390), тот же метод использован в
census_B, point14 (m8_verify.py Hm_light) и point3B_fix1. Тот сертификат
считает winding(H_m) = winding(отношения), но ВНУТРИ него уже вычисляется
x_{2^m} как промежуточная величина (см. также
`w36/audit_codex/cert_slice_param_audit.py:411-414`: `inv=af_recip(x128);
H=af_mul(x,inv)`). Эта программа берёт ТОЛЬКО x_{2^m} (числитель отбрасывается
-- цикл орбиты останавливается на n=2^m, а не идёт до 2^(m+1), что дешевле)
и вычисляет ЕГО СОБСТВЕННУЮ обмотку тем же проверенным приёмом:

  1. Контур -- окружность |u-u_c|=rho. Разбивается на N равных дуг (points
     t=k/N, k=0..N-1, ТОЧНЫЕ дроби Fraction -- разбиение [0,1) без зазоров по
     построению).
  2. На каждой дуге строится ОДНОСИМВОЛЬНАЯ комплексная affine-форма
     u = u_mid + rho_arc*eps (|eps|<=1, комплексный диск), rho_mid -- середина
     дуги НА окружности, rho_arc = 2*rho*sin(pi*dt/2) (dt=ширина дуги в долях
     оборота) -- ТОЧНОЕ (с округлением ВВЕРХ через Arb, не double!) расстояние
     от u_mid до самой дальней точки дуги (обеих концов); диск(u_mid,rho_arc)
     покрывает ВСЮ дугу целиком (доказательство -- см. ниже, closure-проверка).
  3. Орбита x_{n+1}=g(w_n)+s*h(w_n), w_n=(x_n^2-1)/R прогоняется affine (g,h
     несут CL-34 остаточные радиусы EPS_G/EPS_H, тот же вход, что и во всех
     верификаторах проекта) до n=2^m; получаем affine-форму x_{2^m} над ВСЕЙ
     дугой. Проверяем: (a) композиция |w|<1 на каждом шаге; (b) знаменатель
     не содержит 0 (|x_{2^m}|_lower = |c|_lower - |a|_upper - r > 0).
  4. Условие (b) на ЛЮБОЙ дуге автоматически означает угловой раствор образа
     дуги < pi (диск радиуса R с центром c и R<|c| вписан в сектор с
     полуугла asin(R/|c|)<pi/2 -- элементарный факт, используемый архивом
     НЕЯВНО: не нужно отдельно считать asin, достаточно R<|c|). Значит суммa
     ЗНАКОВ arg() по КОНЦАМ дуг (принципиальная ветвь, (-pi,pi]) -- это
     ТОЧНОЕ непрерывное приращение аргумента, без обёртывания.
  5. Обмотка = (1/2pi) * sum_k arg(x(t_{k+1})/x(t_k)), точки t_k вычислены
     ТОЧЕЧНО (rho_arc=0, только остаточные CL-34 ошибки, без ширины дуги) --
     узкий шар. Итог -- Arb-шар; "строго 0" означает: шар содержит ровно
     целое 0 и НЕ содержит -1 или +1 (та же проверка uniqueness, что и в
     census_A_certificate.py:386-389).

ЧТО НЕ ПЕРЕОТКРЫВАЕТСЯ
-----------------------
Для H1 (посылка "полюс автоматически даёт нуль числителя") эта задача НЕ
нужна -- бриф прямо это говорит, здесь не тронуто. Здесь заново доказывается
ТОЛЬКО отсутствие нулей x_{2^m} ВНУТРИ диска (через wind=0 на контуре) --
именно то, чего не было в существующих сертификатах (они проверяли только
|x_{2^m}|>0 НА дуге, не обмотку).

ВХОДНЫЕ ДАННЫЕ (READ-ONLY, sha256 пинится)
-------------------------------------------
- w35/x4_walk_sonnet/x4_common.py -- замороженные ряды g,h, AU0, delta (тот
  же вход CL-34, что у ВСЕХ верификаторов архива).
- w33/t5_cert_sonnet/w33_gh_hiprec.json -- сырые данные g,h.
- w36/tail_codex/cl34_certificate.json, w36/audit_codex/absolute_margins_arb.json
  -- CL-34 остаточные радиусы EPS_G, EPS_H (тот же источник, что в
  census_A_certificate.py).
- path_to_8/point10_layer1_census_A/census_A_certificate.json,
  path_to_8/point10_layer1_census_B/census_B_certificate.json,
  path_to_8/point17_z72_geometry/z72_certificate.json,
  path_to_8/point3B_localize_two_roots_agent_fix1/localization_certificate.json
  -- ТОЛЬКО геометрия (центр u_c, радиус rho, уровень m) читается отсюда;
  сама обмотка/сертификаты ЭТИХ файлов НЕ используются и НЕ доверяются --
  x_{2^m} и его обмотка пересчитываются заново, независимо, в этой программе.

ЗАПИСЬ: только article_v1/v3_work/winding/winding_certificate.json.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import flint

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "winding_certificate.json"

flint.ctx.prec = 512
A = flint.arb
C = flint.acb
TWO_PI = 2 * A.pi()

sys.path.insert(0, str(ROOT / "w35" / "x4_walk_sonnet"))
import x4_common as xc  # noqa: E402  (READ-ONLY frozen certified input)

G = xc.tc_g
H = xc.tc_h
AU0 = xc.AU0
DELTA = xc.DELTA_pt
R_DISC = xc.r_disc
M = xc.M
if M != 100:
    raise RuntimeError("expected M=100, got %d" % M)

X4_PATH = ROOT / "w35" / "x4_walk_sonnet" / "x4_common.py"
GH_PATH = ROOT / "w33" / "t5_cert_sonnet" / "w33_gh_hiprec.json"
CL34_PATH = ROOT / "w36" / "tail_codex" / "cl34_certificate.json"
ABS36_PATH = ROOT / "w36" / "audit_codex" / "absolute_margins_arb.json"
CENSUS_A = ROOT / "path_to_8" / "point10_layer1_census_A" / "census_A_certificate.json"
CENSUS_B = ROOT / "path_to_8" / "point10_layer1_census_B" / "census_B_certificate.json"
Z72_CERT = ROOT / "path_to_8" / "point17_z72_geometry" / "z72_certificate.json"
FIX1_CERT = ROOT / "path_to_8" / "point3B_localize_two_roots_agent_fix1" / "localization_certificate.json"

N_START = 32
N_CAP = 2048
SAFETY_FACTOR = A("1.000001")  # extra margin on top of the exact upward-rounded chord


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def ub(x) -> float:
    if hasattr(x, "upper"):
        x = x.upper()
    return float(x)


def lb(x) -> float:
    if hasattr(x, "lower"):
        x = x.lower()
    return float(x)


def arb_from_ratio_str(s):
    """Parse an exact rho/centre string that may be 'decimal' or 'p/q'."""
    s = str(s)
    if "/" in s:
        n, d = s.split("/")
        return A(int(n)) / A(int(d))
    return A(s)


# ---------------------------------------------------------------- CL-34 error radii (census_A convention)
_cl34 = json.loads(CL34_PATH.read_text(encoding="utf-8"))
_abs36 = json.loads(ABS36_PATH.read_text(encoding="utf-8"))
EPS_G = A(_cl34["G"]["distance_and_Taylor_tail_upper"]).upper()
EPS_H = A(_cl34["V_h_delta"]["h_error_stored_center_upper"]).upper()
log("EPS_G=%s EPS_H=%s (CL-34, same source as census_A_certificate.py)" % (EPS_G, EPS_H))


# ---------------------------------------------------------------- light single-symbol AF
class LAff:
    __slots__ = ("c", "a", "r")

    def __init__(self, c, a=C(0), r=A(0)):
        self.c = C(c)
        self.a = C(a)
        self.r = A(r)


def la_const(c):
    return LAff(c)


def la_add(x, y):
    return LAff(x.c + y.c, x.a + y.a, x.r + y.r)


def la_addc(x, c):
    return LAff(x.c + C(c), x.a, x.r)


def la_sc(x, c):
    c = C(c)
    return LAff(x.c * c, x.a * c, x.r * c.abs_upper())


def la_mul(x, y):
    ax, ay = x.a.abs_upper(), y.a.abs_upper()
    return LAff(
        x.c * y.c,
        x.c * y.a + y.c * x.a,
        ax * ay + x.c.abs_upper() * y.r + y.c.abs_upper() * x.r + ax * y.r + ay * x.r + x.r * y.r,
    )


def la_horner(coeffs, z):
    v = la_const(C(0))
    for c in reversed(coeffs):
        v = la_addc(la_mul(v, z), c)
    return v


def la_abs_ub(x):
    return x.c.abs_upper() + x.a.abs_upper() + x.r


def la_abs_lb(x):
    return x.c.abs_lower() - x.a.abs_upper() - x.r


INV_R = C(1) / C(R_DISC)


def xden_af(u_mid, u_rad, m):
    """Affine enclosure of x_{2^m}(u) for u ranging over disk(u_mid,u_rad).
    Only the DENOMINATOR is computed: loop stops at n=2^m (cheaper than the
    ratio machinery, which needs 2^(m+1))."""
    s_factor = C(AU0) / (C(DELTA) ** m)
    u = LAff(C(u_mid), C(A(u_rad)))
    s = la_sc(u, s_factor)
    s_abs = la_abs_ub(s)
    x = la_const(C(0))
    lev = 1 << m
    max_w = A(0)
    for n in range(lev):
        w = la_sc(la_addc(la_mul(x, x), -1), INV_R)
        wu = la_abs_ub(w)
        if not (wu < 1):
            return None, {"fail": "composition", "step": n, "w_upper": str(wu)}
        if wu > max_w:
            max_w = wu
        vg = la_horner(G, w)
        vh = la_horner(H, w)
        vg.r = vg.r + EPS_G
        vh.r = vh.r + EPS_H
        x = la_add(vg, la_mul(vh, s))
        x.r = x.r + EPS_G + s_abs * EPS_H
    return x, {"max_w": max_w}


# ---------------------------------------------------------------- geometry (READ-ONLY)
def load_disks():
    disks = []

    ca = json.loads(CENSUS_A.read_text(encoding="utf-8"))
    for lbl, r in ca["disk_results"].items():
        if r.get("count") != 1 or str(lbl).startswith("NEG"):
            continue
        disks.append({
            "label": lbl, "pack": "A", "m": 7, "required": True,
            "centre_re": str(r["centre_re"]), "centre_im": str(r["centre_im"]),
            "rho": str(r["rho"]),
        })

    cb = json.loads(CENSUS_B.read_text(encoding="utf-8"))
    for lbl, r in cb["disk_results"].items():
        if r.get("count") != 1 or str(lbl).startswith("NEG"):
            continue
        disks.append({
            "label": lbl, "pack": "B", "m": 7, "required": True,
            "centre_re": str(r["centre_re"]), "centre_im": str(r["centre_im"]),
            "rho": str(r["rho"]),
        })

    z72 = json.loads(Z72_CERT.read_text(encoding="utf-8"))
    ct = z72["contour"]
    disks.append({
        "label": "Z72", "pack": "17", "m": 8, "required": True,
        "centre_re": str(ct["centre_re"]), "centre_im": str(ct["centre_im"]),
        "rho": str(ct["rho"]),
    })

    fx = json.loads(FIX1_CERT.read_text(encoding="utf-8"))
    for lbl in ("D_minus", "D_plus"):
        d = fx["disks"][lbl]
        disks.append({
            "label": lbl.upper(), "pack": "3B_fix1", "m": 7, "required": False,
            "centre_re": d["centre"], "centre_im": "0",
            "rho": d["rho"],
        })

    return disks


# ---------------------------------------------------------------- per-disk winding
def check_tiling(n_arcs):
    """Arcs t=k/n..(k+1)/n, k=0..n-1: exact-Fraction tiling of [0,1)."""
    total_width = Fraction(0)
    for k in range(n_arcs):
        t1 = Fraction(k, n_arcs)
        t2 = Fraction(k + 1, n_arcs)
        total_width += (t2 - t1)
    ok = (total_width == 1) and (Fraction(0, n_arcs) == 0) and (Fraction(n_arcs, n_arcs) == 1)
    return ok, "sum of %d arc widths = %s (must be 1)" % (n_arcs, total_width)


def arc_coverage_margin(rho, t1, t2, u_rad):
    """Rigorous (Arb, upward-rounded) check that the disk(u_mid,u_rad) covers
    the WHOLE arc [t1,t2] on the circle: farthest point on the arc is exactly
    the endpoint, at distance chord=2*rho*sin(pi*dt/2) from the arc midpoint
    (elementary circle geometry: any interior point is strictly closer)."""
    dt = t2 - t1
    half_span = A.pi() * A(dt.numerator) / A(dt.denominator) / 2
    chord_ub = (2 * rho * half_span.sin()).upper()
    margin = u_rad - chord_ub
    return margin, chord_ub


def run_disk(d, log_prefix=""):
    t0 = time.time()
    label, m = d["label"], d["m"]
    uc_re = A(d["centre_re"])
    uc_im = A(d["centre_im"])
    u_c = C(uc_re, uc_im)
    rho = arb_from_ratio_str(d["rho"])

    n_arcs = N_START
    arcs_result = None
    fail_reason = None
    while n_arcs <= N_CAP:
        ok_t, tiling_detail = check_tiling(n_arcs)
        if not ok_t:
            fail_reason = "tiling: " + tiling_detail
            break

        per_arc = []
        worst_cov_margin = None
        worst_den_lower = None
        max_w_seen = A(0)
        domain_ok = True
        den_ok = True

        for k in range(n_arcs):
            t1 = Fraction(k, n_arcs)
            t2 = Fraction(k + 1, n_arcs)
            tm = (t1 + t2) / 2
            theta = TWO_PI * A(tm.numerator) / A(tm.denominator)
            u_mid = u_c + C(rho) * (C(0, 1) * C(theta)).exp()

            cov_margin, chord_ub = arc_coverage_margin(rho, t1, t2, 0.0)
            u_rad = float(chord_ub) * float(SAFETY_FACTOR)
            cov_margin2, _ = arc_coverage_margin(rho, t1, t2, A(u_rad))
            if worst_cov_margin is None or cov_margin2 < worst_cov_margin:
                worst_cov_margin = cov_margin2

            xa, diag = xden_af(u_mid, u_rad, m)
            if xa is None:
                domain_ok = False
                fail_reason = "arc %d/%d domain: %s" % (k, n_arcs, diag)
                break
            max_w_seen = max(max_w_seen, diag["max_w"])
            den_lo = la_abs_lb(xa)
            if worst_den_lower is None or den_lo < worst_den_lower:
                worst_den_lower = den_lo
            if not (den_lo > 0):
                den_ok = False
                fail_reason = "arc %d/%d denominator contains 0: lower=%s" % (k, n_arcs, den_lo)
                break
            per_arc.append((t1, t2))

        if not (domain_ok and den_ok):
            n_arcs *= 2
            continue

        # endpoints: tight point evaluation (u_rad=0), CL-34 error only.
        # NOTE (matches census_A_certificate.py:compute_winding exactly): the
        # distinct t-values needed are t1,t2 of EVERY arc, i.e. 0,1/n,...,
        # (n-1)/n AND the wrap-around point n/n==1 (a SEPARATE dict key from
        # 0, but forced to the SAME angle th=0 to avoid a tiny extra Arb
        # argument-reduction radius on 2*pi that computing t=1 directly would
        # introduce, and to guarantee the two are bit-identical, not merely
        # close).
        needed_ts = set()
        for t1, t2 in per_arc:
            needed_ts.add(t1)
            needed_ts.add(t2)
        endpoints = {}
        endpoint_ok = True
        for t in needed_ts:
            theta = A(0) if t in (0, 1) else TWO_PI * A(t.numerator) / A(t.denominator)
            u_pt = u_c + C(rho) * (C(0, 1) * C(theta)).exp()
            xa, diag = xden_af(u_pt, 0.0, m)
            if xa is None:
                endpoint_ok = False
                fail_reason = "endpoint t=%s domain: %s" % (t, diag)
                break
            re_m = A(xa.c.real.mid())
            im_m = A(xa.c.imag.mid())
            err = A(xa.c.real.rad()) + A(xa.c.imag.rad()) + xa.a.abs_upper() + xa.r
            endpoints[t] = C(A(re_m, err), A(im_m, err))

        if not endpoint_ok:
            n_arcs *= 2
            continue

        total = A(0)
        for t1, t2 in per_arc:
            total = total + (endpoints[t2] / endpoints[t1]).arg()
        wind = total / TWO_PI
        cand = int(round(float(wind.mid())))
        strictly_this = (
            (wind - cand).contains(0)
            and not (wind - (cand - 1)).contains(0)
            and not (wind - (cand + 1)).contains(0)
        )

        arcs_result = {
            "n_arcs": n_arcs,
            "tiling_ok": ok_t,
            "tiling_detail": tiling_detail,
            "arc_disk_coverage_ok": bool(worst_cov_margin > 0),
            "arc_disk_coverage_worst_margin": ub(worst_cov_margin) if worst_cov_margin is not None else None,
            "domain_ok": domain_ok,
            "max_w_upper": ub(max_w_seen),
            "denominator_nonzero_on_contour": bool(worst_den_lower > 0),
            "min_abs_denominator_lower": lb(worst_den_lower) if worst_den_lower is not None else None,
            "winding_ball": str(wind),
            "winding_candidate": cand,
            "winding_unique": bool(strictly_this),
            "strictly_zero": bool(strictly_this and cand == 0),
        }
        break

    elapsed = time.time() - t0
    if arcs_result is None:
        return {
            "label": label, "pack": d["pack"], "m": m, "required": d["required"],
            "centre_re": d["centre_re"], "centre_im": d["centre_im"], "rho": d["rho"],
            "pass": False, "fail_reason": fail_reason, "elapsed_s": round(elapsed, 2),
        }

    out = {
        "label": label, "pack": d["pack"], "m": m, "required": d["required"],
        "centre_re": d["centre_re"], "centre_im": d["centre_im"], "rho": d["rho"],
        "elapsed_s": round(elapsed, 2),
    }
    out.update(arcs_result)
    out["pass"] = bool(
        arcs_result["tiling_ok"]
        and arcs_result["arc_disk_coverage_ok"]
        and arcs_result["domain_ok"]
        and arcs_result["denominator_nonzero_on_contour"]
        and arcs_result["winding_unique"]
        and arcs_result["strictly_zero"]
    )
    log("%s  [pack %s m=%d N=%d]  wind=%s cand=%d unique=%s strictly_zero=%s  "
        "min|x_%d|>=%.4e  cov_margin>=%.2e  (%.1fs)  PASS=%s" % (
            label, d["pack"], m, arcs_result["n_arcs"], arcs_result["winding_ball"][:32],
            arcs_result["winding_candidate"], arcs_result["winding_unique"],
            arcs_result["strictly_zero"], 1 << m,
            arcs_result["min_abs_denominator_lower"], arcs_result["arc_disk_coverage_worst_margin"],
            elapsed, out["pass"]))
    return out


def n_checks_for(rec):
    if "n_arcs" not in rec:
        return 0
    n = rec["n_arcs"]
    # per arc: domain check + denominator-nonzero check + coverage check
    # + endpoint computation; plus 1 tiling check + 1 winding-uniqueness check
    return 3 * n + n + 2


def main():
    t0 = time.time()
    log("=== winding_certificate.py: rigorous wind(x_2^m)=0 over 23(+2) contours ===")
    log("prec_bits=%d" % flint.ctx.prec)

    disks = load_disks()
    n_required = sum(1 for d in disks if d["required"])
    n_optional = sum(1 for d in disks if not d["required"])
    log("loaded %d disks (%d required, %d optional): %s" % (
        len(disks), n_required, n_optional, ", ".join(d["label"] for d in disks)))
    if n_required != 23:
        raise RuntimeError("expected 23 required disks, got %d" % n_required)

    results = []
    for d in disks:
        r = run_disk(d)
        results.append(r)
        # incremental checkpoint (safety against interruption over a long run)
        _write(results, disks, t0, partial=True)

    _write(results, disks, t0, partial=False)

    n_pass_req = sum(1 for r in results if r["pass"] and r["required"])
    n_pass_opt = sum(1 for r in results if r["pass"] and not r["required"])
    log("=== SUMMARY: required PASS %d/%d, optional PASS %d/%d, total %.1fs ===" % (
        n_pass_req, n_required, n_pass_opt, n_optional, time.time() - t0))


def _write(results, disks, t0, partial):
    n_required = sum(1 for d in disks if d["required"])
    n_optional = sum(1 for d in disks if not d["required"])
    done = {r["label"]: r for r in results}
    n_pass_req = sum(1 for r in results if r.get("pass") and r["required"])
    n_pass_opt = sum(1 for r in results if r.get("pass") and not r["required"])
    all_pass_required = (len(results) >= n_required) and all(
        r["pass"] for r in results if r["required"]
    )
    n_checks_total = sum(n_checks_for(r) for r in results)

    payload = {
        "run": "winding_certificate",
        "partial": partial,
        "task": "strict wind(x_{2^m}, Gamma)=0 on each of the 23 ring contours "
                "(+2 optional rho=1/6 disks), Arb interval arithmetic, directed rounding",
        "not_reopening": "H1 pole question is closed structurally per WINDING_BRIEF.md sec.3; "
                          "not touched here",
        "method": "light single-symbol complex-disk AF (census_A_certificate.py convention): "
                   "arc-covering disk excludes 0 => arc angular span < pi (elementary, R<|c| "
                   "implies asin(R/|c|)<pi/2) => endpoint-only arg() sum is the true continuous "
                   "winding, no wraparound possible; denominator-only orbit (n=2^m, cheaper than "
                   "the ratio H_m which needs 2^(m+1))",
        "prec_bits": flint.ctx.prec,
        "AU0": str(AU0), "delta": str(DELTA), "EPS_G": str(EPS_G), "EPS_H": str(EPS_H),
        "N_START": N_START, "N_CAP": N_CAP, "safety_factor": str(SAFETY_FACTOR),
        "sha256_pins": {
            "x4_common.py": sha256(X4_PATH),
            "w33_gh_hiprec.json": sha256(GH_PATH),
            "cl34_certificate.json": sha256(CL34_PATH),
            "absolute_margins_arb.json": sha256(ABS36_PATH),
            "census_A_certificate.json": sha256(CENSUS_A),
            "census_B_certificate.json": sha256(CENSUS_B),
            "z72_certificate.json": sha256(Z72_CERT),
            "localization_certificate.json (fix1, optional disks)": sha256(FIX1_CERT),
        },
        "n_disks_required": n_required,
        "n_disks_optional": n_optional,
        "n_disks_done": len(results),
        "n_pass_required": n_pass_req,
        "n_pass_optional": n_pass_opt,
        "all_pass_required": all_pass_required,
        "all_pass": all_pass_required,  # optional disks are best-effort, do not block all_pass
        "n_checks": n_checks_total,
        "worst_min_abs_denominator_required": (
            min((r["min_abs_denominator_lower"] for r in results
                 if r["required"] and r.get("min_abs_denominator_lower") is not None), default=None)
        ),
        "elapsed_total_s": round(time.time() - t0, 1),
        "disks": results,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
