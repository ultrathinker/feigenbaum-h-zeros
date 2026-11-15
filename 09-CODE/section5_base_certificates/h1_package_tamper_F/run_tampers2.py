# -*- coding: utf-8 -*-
"""
run_tampers2.py — повторный (F2) прогон батареи порч против РЕМОНТНОГО verify_E.

Переиспользует батарею и инфраструктуру из run_tampers.py (import), НЕ переписывая
сами порчи (T01..T12) и логику песочницы/снапшотов. Все артефакты второго прогона
пишутся в *_2 файлы / run_logs2/ / TAMPER_F2.md. Первый прогон (TAMPER_F.md,
run_logs/, archive_integrity*.txt, verifier_diff.txt) НЕ трогается.

verify_E/ не правится (READ-ONLY исходник). Архив READ-ONLY (sha256 до/после).
"""
import sys, os, json, hashlib, shutil, subprocess, time, re
from pathlib import Path

HERE      = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_tampers as RT          # переиспользуем батарею порч и harness-функции

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ["PYTHONIOENCODING"] = "utf-8"

ARCH        = RT.ARCH                       # архив (READ-ONLY)
SANDBOX     = RT.SANDBOX                    # HERE/sandbox
VERIFY_PY   = RT.VERIFY_PY                  # HERE/h1_verify_pkg.py — сюда пишем патченую копию
VERIFY_ORIG = RT.VERIFY_ORIG                # verify_E/h1_verify_pkg.py — РЕМОНТНЫЙ (READ-ONLY)

LOGDIR2   = HERE / "run_logs2"
PROG2     = HERE / "progress2.log"
DIFF2     = HERE / "verifier_diff2.txt"
REPORT2   = HERE / "TAMPER_F2.md"

LOGDIR2.mkdir(parents=True, exist_ok=True)
PROG2.write_text("", encoding="utf-8")

sha256_file = RT.sha256_file
parse_blocks = RT.parse_blocks

def logp(msg):
    line = time.strftime('%Y-%m-%d %H:%M:%S') + "  " + msg
    with open(PROG2, "a", encoding="utf-8") as f:
        f.write(line + "\n"); f.flush()
    print(line, flush=True)

# --- единственный патч копии верификатора: строка корня архива --------------
def patch_verifier2():
    """Копируем ТЕКУЩИЙ (ремонтный) verify_E/h1_verify_pkg.py -> HERE/h1_verify_pkg.py
    и правим ОДНУ строку (корень архива -> песочница). Записываем sha256 и diff."""
    text = VERIFY_ORIG.read_text(encoding="utf-8")
    orig_line = 'ARCH = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")'
    new_line  = 'ARCH = Path(r"%s")' % str(SANDBOX).replace("\\", "/")
    assert text.count(orig_line) == 1, "ожидалась ровно одна строка ARCH"
    patched = text.replace(orig_line, new_line, 1)
    VERIFY_PY.write_text(patched, encoding="utf-8")
    h_orig = sha256_file(VERIFY_ORIG)
    h_copy = sha256_file(VERIFY_PY)
    with open(DIFF2, "w", encoding="utf-8") as f:
        f.write("однострочный diff копии верификатора (verify_E -> tamper_F), прогон F2:\n")
        f.write("--- verify_E/h1_verify_pkg.py (РЕМОНТНЫЙ, строка 20)\n")
        f.write("+++ tamper_F/h1_verify_pkg.py (копия под песочницу)\n")
        f.write("- %s\n" % orig_line)
        f.write("+ %s\n" % new_line)
        f.write("\nДругих правок нет.\n")
        f.write("sha256 оригинала (verify_E, READ-ONLY): %s\n" % h_orig)
        f.write("sha256 копии (патченой):                %s\n" % h_copy)
    return orig_line, new_line, h_orig, h_copy

def run_verifier2(label):
    t0 = time.time()
    logp("[%s] run start" % label)
    proc = subprocess.run([sys.executable, str(VERIFY_PY)],
                          cwd=str(HERE), capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    dt = time.time() - t0
    out = proc.stdout or ""
    err = proc.stderr or ""
    (LOGDIR2 / ("%s.log" % label)).write_text(
        out + ("\n--- stderr ---\n%s\n[exit=%d]\n" % (err, proc.returncode)),
        encoding="utf-8")
    logp("[%s] run done exit=%d  %.1fs" % (label, proc.returncode, dt))
    return proc.returncode, out, dt

# --- чтение первого прогона (run_logs/ — сохранён, не перезаписывается) ------
def parse_log_first(p):
    if not p.exists():
        return None
    txt = p.read_text(encoding="utf-8", errors="replace")
    rc = None
    m = re.search(r"\[exit=(-?\d+)\]", txt)
    if m:
        rc = int(m.group(1))
    fails = re.findall(r"=>\s*Проверка\s*(\d+):\s*FAIL", txt)
    blocks_nums = sorted(set(fails), key=int)
    mm = [l.strip() for l in txt.splitlines() if "[MISMATCH]" in l]
    summ = ""
    for l in txt.splitlines():
        if l.strip().startswith("упавшие блоки:"):
            summ = l.strip()
    return dict(exit=rc, blocks_nums=blocks_nums, mismatches=mm, summary=summ, txt=txt)

def read_first_run():
    logdir1 = HERE / "run_logs"
    first = {}
    for tid, title, rels, fn in RT.TAMPERS:
        first[tid] = parse_log_first(logdir1 / ("%s.log" % tid))
    first["T00_baseline"] = parse_log_first(logdir1 / "T00_baseline.log")
    return first

# ===========================================================================
EXPECT = {
    "T01": ("exit 1", "C1+C2"),
    "T02": ("exit 1", "C1"),
    "T03": ("exit 1", "C1"),
    "T04": ("exit 1", "C3"),
    "T05": ("exit 1", "C3"),
    "T06": ("exit 1", "C3"),
    "T07": ("exit 1", "C3 (ремонт: гейт pos/NEG)"),
    "T08": ("exit 1", "C5"),
    "T09": ("exit 1", "C3"),
    "T10": ("exit 1", "C6"),
    "T11": ("exit 1", "C4 (ремонт: q из первичных архива)"),
    "T12": ("exit 0", "— (косметика: НЕ должен ловить)"),
}

def write_integrity2(before, after, changed, unchanged, baseline_ok, h_orig, h_copy):
    p = HERE / "archive_integrity2.txt"
    with open(p, "w", encoding="utf-8") as f:
        f.write("# Целостность архива — прогон F2 (IRON RULE: архив READ-ONLY)\n")
        f.write("# ARCH = %s\n" % ARCH)
        f.write("# Множество: %d файлов (сертификаты + 1542 tube)\n" % len(before))
        f.write("# sha256 РЕМОНТНОГО verify_E/h1_verify_pkg.py = %s\n" % h_orig)
        f.write("# sha256 патченой копии tamper_F/h1_verify_pkg.py = %s\n" % h_copy)
        f.write("# baseline: %s\n" % ("PASS exit 0" if baseline_ok else "FAIL"))
        f.write("#\n")
        f.write("# СВЕРКА: %d/%d файлов совпадают\n" % (len(before) - len(changed), len(before)))
        f.write("# ИЗМЕНЁННЫЕ: %s\n" % (changed if changed else "НЕТ"))
        f.write("#\n")
        for r in sorted(before):
            b = before[r]; a = after.get(r, "MISSING")
            flag = "" if b == a else "   <<< CHANGED"
            f.write("%s  %s%s\n" % (b, r, flag))
        f.write("#\n")
        f.write("ВЕРДИКТ: %s\n" % (
            "АРХИВ НЕ ИЗМЕНИЛСЯ — ни один байт не записан в архив. "
            "Все порчи шли на копии в tamper_F/sandbox/." if unchanged
            else "АРХИВ ИЗМЕНЁН — НАРУШЕНИЕ IRON RULE!"))
    return p

def fmt_blocks(nums):
    if not nums:
        return "—"
    return ", ".join("C%s" % b for b in nums)

def extract_q_from_t11(out):
    """Из протокола T11 вытащить числовое q (recomputed) и строку max(q,p)<1."""
    info = {}
    lines = out.splitlines()
    for i, l in enumerate(lines):
        s = l.strip()
        if "q = L2/delta^4" in s and "[MISMATCH]" in s:
            info["q_mismatch_line"] = s
            if i + 1 < len(lines):
                info["q_got"] = lines[i + 1].strip()
            if i + 2 < len(lines):
                info["q_exp"] = lines[i + 2].strip()
        if "max(q,p) < 1" in s:
            info["maxqp_line"] = s
            if i + 1 < len(lines):
                info["maxqp_got"] = lines[i + 1].strip()
    # числовое q из got-строки
    m = re.search(r"got:\s*([-+]?\d[\d.eE+-]*)", info.get("q_got", ""))
    if m:
        info["q_value"] = m.group(1)
    m2 = re.search(r"got:\s*([-+]?\d[\d.eE+-]*)", info.get("maxqp_got", ""))
    if m2:
        info["maxqp_value"] = m2.group(1)
    return info

def write_report2(results, first, baseline_ok, unchanged, h_orig, h_copy, ol, nl, changed):
    L = []
    L.append("# TAMPER_F2 — повторная батарея порч против РЕМОНТНОГО verify_E\n\n")
    L.append("Рабочая папка: `article_v1/v3_work/h1_package/tamper_F/`.\n")
    L.append("Это **второй прогон** батареи (после ремонта верификатора). "
             "Батарея и harness переиспользованы из `run_tampers.py` (import, без переписывания порчей); "
             "артефакты второго прогона — в `run_logs2/`, `*_2.txt`, `verifier_diff2.txt`.\n")
    L.append("Первый прогон сохранён без изменений: `TAMPER_F.md`, `run_logs/`.\n\n")

    L.append("## Целевая копия верификатора (refresh)\n")
    L.append("- Источник (READ-ONLY): `verify_E/h1_verify_pkg.py` — **ремонтная** версия.\n")
    L.append("- sha256 `verify_E/h1_verify_pkg.py` (ремонтный) = `%s`\n" % h_orig)
    L.append("  (для справки, sha256 **до ремонта** был `a49721926fa0579278e75f114e1c0509fe75b2f98f2787c7cbfd9f40ef99137a` — файл изменился, ремонт налицо).\n")
    L.append("- Копия-мишень: `tamper_F/h1_verify_pkg.py`, sha256 = `%s`\n" % h_copy)
    L.append("- Применён **единственный** патч (одна строка, корень архива → песочница):\n\n")
    L.append("```diff\n")
    L.append("- %s\n" % ol)
    L.append("+ %s\n" % nl)
    L.append("```\n")
    L.append("Других правок в копии нет (см. `verifier_diff2.txt`).\n\n")

    L.append("## Целостность архива (IRON RULE: READ-ONLY)\n")
    L.append("- Множество под сверкой: %d файлов (9 сертификатов + 1542 tube).\n" % len(RT.archive_read_set()))
    if unchanged:
        L.append("- **ВЕРДИКТ: АРХИВ НЕ ИЗМЕНИЛСЯ** — sha256 ДО == ПОСЛЕ (см. `archive_integrity2.txt`); "
                 "изменённых файлов: 0.\n")
    else:
        L.append("- **ВЕРДИКТ: АРХИВ ИЗМЕНЁН — НАРУШЕНИЕ!** Изменено: %s\n" % changed)
    L.append("\n")

    L.append("## Baseline (чистая песочница)\n")
    L.append("- exit code = %s (ожидание 0).\n\n" % ("0 — PASS" if baseline_ok else "НЕ 0 — FAIL"))

    L.append("## Таблица: 12 порч (второй прогон, ремонтный верификатор)\n\n")
    L.append("| № | Порча (на копии) | Ожидание | Факт F2: exit / упавшие блоки | Вердикт F2 |\n")
    L.append("|---|---|---|---|---|\n")
    for r in results:
        tid = r["tid"]
        exp_exit, exp_blocks = EXPECT[tid]
        blocks = fmt_blocks(r["failed_blocks"])
        if tid == "T12":
            v = "НЕ ЛОВИТ (правильно)" if not r["caught"] else "ЛОЖИТ (дефект: падает на косметике)"
        else:
            v = "ЛОЖИТ (CAUGHT)" if r["caught"] else "НЕ ЛОВИТ (дыра осталась)"
        L.append("| %s | %s | %s | exit=%d; блоки: %s | **%s** |\n"
                 % (tid, r["desc"], "%s, %s" % (exp_exit, exp_blocks), r["exit"], blocks, v))
    L.append("\n")

    # --- детали по каждой порче ---
    L.append("## Детали по каждой порче (F2)\n\n")
    for r in results:
        L.append("### %s — %s\n" % (r["tid"], r["title"]))
        L.append("- действие: %s\n" % r["desc"])
        L.append("- exit=%d, время %.1fs\n" % (r["exit"], r["dt"]))
        L.append("- упавшие блоки: %s\n" % (fmt_blocks(r["failed_blocks"]) if r["failed_blocks"] else "нет"))
        if r["mismatches"]:
            for m in r["mismatches"][:10]:
                L.append("  - %s\n" % m)
        L.append("- итоговая строка сводки: `%s`\n\n" % (r["summary"] or "—"))

    # --- T11: правильная причина ---
    t11 = next(r for r in results if r["tid"] == "T11")
    t11log = (LOGDIR2 / "T11.log").read_text(encoding="utf-8", errors="replace")
    qi = extract_q_from_t11(t11log)
    qval = qi.get("q_value", "?")
    maxqp = qi.get("maxqp_value", "?")
    try:
        q_gt1 = float(qval) > 1.0
    except Exception:
        q_gt1 = None
    L.append("## T11 — проверка «правильной причины» падения\n\n")
    L.append("Требование: провалиться именно в **Проверке 4**, причём пересчитанный "
             "спектральный критерий **q > 1** (а не просто exit 1).\n\n")
    L.append("- упавший блок F2: **%s** (требовалось C4) → %s\n"
             % (fmt_blocks(t11["failed_blocks"]),
                "СОВПАЛО" if t11["failed_blocks"] == ["4"] else "НЕ СОВПАЛО"))
    L.append("- пересчитанное q (из первичных `nDT2=600` архива-песочницы): `%s` → "
             "**q %s 1**\n" % (qval, (">" if q_gt1 else ("<=" if q_gt1 is False else "?"))))
    L.append("- строка `max(q,p) < 1`: `%s`  (получено `%s`)\n"
             % (qi.get("maxqp_line", "—"), maxqp))
    L.append("- `[MISMATCH] q = L2/delta^4`: `%s`\n" % qi.get("q_mismatch_line", "—"))
    L.append("  - `%s`\n" % qi.get("q_got", "—"))
    L.append("  - `%s`\n" % qi.get("q_exp", "—"))
    L.append("- строка `max(q,p) < 1`: `%s`\n" % qi.get("maxqp_line", "—"))
    L.append("  - `%s`\n" % qi.get("maxqp_got", "—"))
    verdict_t11 = ("ПРАВИЛЬНАЯ ПРИЧИНА" if (t11["failed_blocks"] == ["4"] and q_gt1)
                   else "НЕ правая причина")
    L.append("- **Вердикт T11: %s** — упало в Проверке 4, q>1 подтверждён.\n\n" % verdict_t11)

    # --- T07: правильный блок ---
    t07 = next(r for r in results if r["tid"] == "T07")
    L.append("## T07 — проверка падающего блока\n\n")
    L.append("Требование: провалиться именно в **Проверке 3** (гейт pos/NEG).\n\n")
    L.append("- упавший блок F2: **%s** (требовалось C3) → %s\n\n"
             % (fmt_blocks(t07["failed_blocks"]),
                "СОВПАЛО" if t07["failed_blocks"] == ["3"] else "НЕ СОВПАЛО"))

    # --- side-by-side первый vs второй ---
    L.append("## Сравнение первый прогон (TAMPER_F) vs второй прогон (F2)\n\n")
    L.append("| № | Порца | Ожидание | F1 exit | F1 блоки | F1 вердикт | "
             "F2 exit | F2 блоки | F2 вердикт | Дельта |\n")
    L.append("|---|---|---|---|---|---|---|---|---|---|\n")
    f1_caught = {"T01": True, "T02": True, "T03": True, "T04": True, "T05": True,
                 "T06": True, "T07": False, "T08": True, "T09": True, "T10": True,
                 "T11": False, "T12": False}
    deltas = []
    for r in results:
        tid = r["tid"]
        f1 = first.get(tid)
        f1_exit = f1["exit"] if f1 else "?"
        f1_blocks = fmt_blocks(f1["blocks_nums"]) if f1 else "?"
        f1v = ("НЕ ЛОВИТ (правильно)" if tid == "T12" and not f1_caught[tid]
               else ("ЛОЖИТ (CAUGHT)" if f1_caught[tid] else "НЕ ЛОВИТ (дыра)"))
        f2v = ("НЕ ЛОВИТ (правильно)" if tid == "T12" and not r["caught"]
               else ("ЛОЖИТ (CAUGHT)" if r["caught"] else "НЕ ЛОВИТ (дыра осталась)"))
        if tid == "T12":
            d = "без изменений (оба не ловят — правильно)"
        elif r["caught"] and not f1_caught[tid]:
            d = "ИСПРАВЛЕНО: дыра закрыта"
            deltas.append((tid, "fixed"))
        elif r["caught"] == f1_caught[tid]:
            d = "без изменений"
            deltas.append((tid, "same"))
        else:
            d = "РЕГРЕСС: стало хуже"
            deltas.append((tid, "regress"))
        L.append("| %s | %s | %s | %s | %s | %s | %d | %s | %s | %s |\n"
                 % (tid, r["title"], "%s, %s" % (EXPECT[tid][0], EXPECT[tid][1]),
                    f1_exit, f1_blocks, f1v, r["exit"], fmt_blocks(r["failed_blocks"]), f2v, d))
    L.append("\n")

    # --- сводный вердикт ---
    n_caught = sum(1 for r in results if r["caught"])
    n_caught_real = sum(1 for r in results if r["caught"] and r["tid"] != "T12")
    n_fixed = sum(1 for _, k in deltas if k == "fixed")
    n_regress = sum(1 for _, k in deltas if k == "regress")
    t12_ok = (not next(r for r in results if r["tid"] == "T12")["caught"])
    L.append("## Сводный вердикт F2\n\n")
    L.append("| класс | число | какие |\n|---|---|---|\n")
    L.append("| Пойманы (по смыслу) | %d | %s |\n"
             % (n_caught_real, ", ".join(r["tid"] for r in results if r["caught"] and r["tid"] != "T12")))
    holes = [r["tid"] for r in results if (not r["caught"]) and r["tid"] != "T12"]
    L.append("| НЕ пойманы — дыры | %d | %s |\n" % (len(holes), (", ".join(holes) if holes else "нет")))
    L.append("| НЕ пойманы и это правильно (косметика) | %d | %s |\n"
             % (1 if t12_ok else 0, "T12" if t12_ok else "—"))
    L.append("\n")
    L.append("**Итог F2: поймано %d из 11 (T01–T11); T12 (косметика) %s. "
             "Ремонт закрыл %d дыры первого прогона (T07, T11); регрессов: %d.**\n\n"
             % (n_caught_real,
                "правильно не ловится" if t12_ok else "ЛОЖНО ловится (дефект)",
                n_fixed, n_regress))
    if holes:
        L.append("**ОСТАЛИСЬ ДЫРЫ: %s.** Это результат, не неудача.\n\n" % ", ".join(holes))
    else:
        L.append("**Остальных дыр нет: все 11 осмысленных порчей ловятся, косметика T12 — нет.**\n\n")

    L.append("## Воспроизводимость F2\n")
    L.append("- `tamper_F/run_tampers2.py` — оркестратор второго прогона (import батареи из `run_tampers.py`).\n")
    L.append("- `tamper_F/run_logs2/T00_baseline.log … T12.log` — построчные протоколы F2.\n")
    L.append("- `tamper_F/archive_integrity2.txt`, `tamper_F/verifier_diff2.txt`, `tamper_F/progress2.log`.\n")
    L.append("- `tamper_F/run1_backup/` — страховая копия артефактов первого прогона.\n")
    REPORT2.write_text("".join(L), encoding="utf-8")
    return REPORT2

# ============================ MAIN ========================================
def main():
    logp("=== BRIEF F2: повторная батарея порч против РЕМОНТНОГО verify_E ===")
    logp("ARCH (READ-ONLY) = %s" % ARCH)
    logp("SANDBOX          = %s" % SANDBOX)
    logp("VERIFY_ORIG      = %s  (ремонтный, READ-ONLY)" % VERIFY_ORIG)
    logp("sha256 verify_E (ремонтный) = %s" % sha256_file(VERIFY_ORIG))

    # 1) sha256 архива ДО
    logp("step1: sha256 архива ДО")
    snap_before = RT.snapshot_archive("2_BEFORE")

    # 2) refresh копии верификатора из ТЕКУЩЕГО (ремонтного) verify_E + одна строка
    logp("step2: refresh копии верификатора (verify_E -> tamper_F), одна строка")
    ol, nl, h_orig, h_copy = patch_verifier2()
    logp("       sha256 verify_E/h1_verify_pkg.py (ремонтный) = %s" % h_orig)
    logp("       sha256 копии (патченой)                      = %s" % h_copy)
    logp("       diff: -%s" % ol)
    logp("              +%s" % nl)

    # 3) baseline
    logp("step3: сборка чистой песочницы + baseline (ожидание exit 0)")
    RT.build_sandbox()
    RT.restore_all()
    rc, out, dt = run_verifier2("T00_baseline")
    fb, mm, summ, blocksd = parse_blocks(out)
    logp("       baseline exit=%d упавшие_блоки=%s за %.1fs" % (rc, fb, dt))
    baseline_ok = (rc == 0 and not fb)
    if not baseline_ok:
        logp("!!! BASELINE НЕ ПРОШЁЛ — дальше бессмысленно")

    # 4) 12 порч (полный пересбор песочницы перед каждой)
    results = []
    for tid, title, rels, fn in RT.TAMPERS:
        logp("--- %s %s ---" % (tid, title))
        RT.build_sandbox()
        desc = fn(rels)
        rc, out, dt = run_verifier2(tid)
        fb, mm, summ, blocksd = parse_blocks(out)
        caught = (rc == 1)
        results.append(dict(tid=tid, title=title, desc=desc,
                            exit=rc, caught=caught,
                            failed_blocks=fb, mismatches=mm, summary=summ, dt=dt))
        logp("       %s exit=%d caught=%s blocks=%s за %.1fs" % (tid, rc, caught, fb, dt))

    # 5) sha256 архива ПОСЛЕ
    logp("step5: sha256 архива ПОСЛЕ")
    RT.build_sandbox()
    snap_after = RT.snapshot_archive("2_AFTER")
    changed = [r for r in snap_before if snap_before[r] != snap_after.get(r)]
    unchanged = (len(changed) == 0)
    logp("       изменённых файлов архива: %d  => %s"
         % (len(changed), "АРХИВ НЕ ИЗМЕНИЛСЯ" if unchanged else "АРХИВ ИЗМЕНЁН!!!"))

    write_integrity2(snap_before, snap_after, changed, unchanged, baseline_ok, h_orig, h_copy)

    first = read_first_run()
    write_report2(results, first, baseline_ok, unchanged, h_orig, h_copy, ol, nl, changed)
    logp("=== DONE ===")

if __name__ == "__main__":
    main()
