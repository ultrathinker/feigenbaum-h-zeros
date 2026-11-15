#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tamper battery for winding_certificate.json (oid 9595c48c, wave v3).

Applies >=6 corruptions, EACH on a fresh copy of winding_certificate.json,
runs the independent verifier (winding_verify.py) on the copy, and records
what was broken, which check caught it, and the verifier's exit code.
Per WINDING_BRIEF.md sec.5 (TAMPER_LOG.md, minimum 6: gap in coverage,
inflated winding, min|x|, sha256, arc count, sign).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(HERE, "winding_certificate.json")
VERIFY = os.path.join(HERE, "winding_verify.py")
PY = sys.executable


def load():
    return json.load(open(CLEAN, encoding="utf-8"))


def disk(d, label):
    for rec in d["disks"]:
        if rec["label"] == label:
            return rec
    raise KeyError(label)


def apply_tamper(mutator):
    d = load()
    desc = mutator(d)
    path = os.path.join(HERE, "_tampered.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    return path, desc


def run_verify(path):
    r = subprocess.run([PY, VERIFY, path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip()
    fails = [ln for ln in out.splitlines() if "FAIL:" in ln]
    return r.returncode, fails, out


# ------------------------------------------------------------------ each tamper (category per brief sec.5)
def t1(d):
    # category: gap in arc coverage
    rec = disk(d, "Z40")
    rec["arc_disk_coverage_ok"] = False
    rec["arc_disk_coverage_worst_margin"] = -1.0e-6
    return ("T1 щель в покрытии дуг: disks[Z40].arc_disk_coverage_ok := false, "
            "worst_margin := -1e-6 (ложное утверждение о разрыве)")


def t2(d):
    # category: inflated/falsified winding
    rec = disk(d, "Z63")
    rec["winding_candidate"] = 1
    rec["winding_unique"] = True
    rec["strictly_zero"] = False
    return ("T2 обмотка искажена: disks[Z63].winding_candidate := 1, "
            "strictly_zero := false (ложно утверждается полюс внутри контура)")


def t3(d):
    # category: min|x| falsified (claims a much smaller/negative lower bound)
    rec = disk(d, "Z72")
    rec["min_abs_denominator_lower"] = -5.0e-4
    rec["denominator_nonzero_on_contour"] = True  # left inconsistently True
    return "T3 min|x_2^m| испорчен: disks[Z72].min_abs_denominator_lower := -5e-4 (< 0)"


def t4(d):
    # category: sha256 pin corrupted
    k = "census_A_certificate.json"
    d["sha256_pins"][k] = "0" * 64
    return "T4 sha256 пин испорчен: sha256_pins['%s'] := 0000...0000" % k


def t5(d):
    # category: number of arcs understated (insufficient for the arc-covering
    # disk to keep the composition domain valid / denominator nonzero)
    rec = disk(d, "Z01")
    rec["n_arcs"] = 2
    return "T5 число дуг занижено: disks[Z01].n_arcs := 2 (недостаточно, покрывающий диск дуги слишком широк)"


def t6(d):
    # category: sign flipped on a geometric input
    rec = disk(d, "Z74")
    rec["centre_im"] = "-8.68634320415312"
    return "T6 знак центра диска перевёрнут: disks[Z74].centre_im := -8.68634320415312 (было +)"


def t7(d):
    # top-level: n_pass_required inconsistent with all_pass_required/all_pass
    d["n_pass_required"] = 22
    return "T7 верхнеуровневый счётчик испорчен: n_pass_required := 22 (было 23, all_pass оставлен true)"


def t8(d):
    # top-level: n_checks does not match the per-disk formula
    d["n_checks"] = 1
    return "T8 n_checks не сходится с формулой: n_checks := 1"


TAMPERS = [t1, t2, t3, t4, t5, t6, t7, t8]


def main():
    lines = []
    lines.append("# TAMPER_LOG.md — winding_certificate.json (oid 9595c48c, волна v3)\n")
    lines.append("**Режим:** каждая порча -- на СВЕЖЕЙ КОПИИ `winding_certificate.json`; "
                 "`winding_verify.py` запускается на копии; ожидается `exit 1` и конкретная "
                 "проверка-ловушка (строка `FAIL:`).\n")
    lines.append("**Чистый запуск (контроль):** `python winding_verify.py` -> exit 0 (PASS).\n")
    lines.append("| # | Категория (бриф §5) | Что сломал | Какая проверка поймала | exit |")
    lines.append("|---|---|---|---|---|")
    categories = {
        1: "щель в покрытии", 2: "обмотка (завышена/искажена)", 3: "min|x|",
        4: "sha256", 5: "число дуг", 6: "знак",
        7: "верхнеуровневый счётчик (бонус)", 8: "n_checks (бонус)",
    }
    n_caught = 0
    for i, t in enumerate(TAMPERS, 1):
        path, desc = apply_tamper(t)
        rc, fails, out = run_verify(path)
        caught = " ; ".join(f.replace("FAIL:", "").strip() for f in fails[:3]) if fails else "(НЕ ПОЙМАНА!)"
        ok = (rc == 1) and bool(fails)
        if ok:
            n_caught += 1
        lines.append("| T%d | %s | %s | %s | %d |" % (i, categories[i], desc, caught, rc))
        print("T%d [%s] exit=%d caught=%s" % (i, categories[i], rc, ok))
    if os.path.exists(os.path.join(HERE, "_tampered.json")):
        os.remove(os.path.join(HERE, "_tampered.json"))
    lines.append("")
    lines.append("**Итого:** %d порч (>= 6 требуемых брифом), поймано %d. Все ожидают exit=1." % (
        len(TAMPERS), n_caught))
    lines.append("")
    lines.append("**Контроль (чистый сертификат, без порчи):**")
    rc0, fails0, out0 = run_verify(CLEAN)
    lines.append("- `python winding_verify.py` -> exit=%d, FAIL-строк=%d (%s)" % (
        rc0, len(fails0), "PASS как и ожидалось" if rc0 == 0 else "!!! НЕОЖИДАННО НЕ PASS"))
    log = "\n".join(lines)
    with open(os.path.join(HERE, "TAMPER_LOG.md"), "w", encoding="utf-8") as f:
        f.write(log)
    print()
    print("TAMPER_LOG.md written. caught %d/%d tampers (each must exit 1); clean control exit=%d." % (
        n_caught, len(TAMPERS), rc0))


if __name__ == "__main__":
    main()
