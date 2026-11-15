# -*- coding: utf-8 -*-
"""
run_tampers.py — батарея порч (BRIEF F) против независимого верификатора.

Железное правило: архив READ-ONLY. Все записи — только внутри tamper_F/.
Порчи делаются на копиях в tamper_F/sandbox/. До и после — sha256 сверка
файлов архива (того множества, что читает верификатор).

Верификатор НЕ правится: его копия лежит в tamper_F/h1_verify_pkg.py и
отличается от оригинала ТОЛЬКО константой корня архива (одна строка).
"""
import sys, os, json, hashlib, shutil, subprocess, time, io
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- корни ----------------------------------------------------------------
HERE      = Path(__file__).resolve().parent                       # tamper_F/
ARCH      = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")  # READ-ONLY
SANDBOX   = HERE / "sandbox"
LOGDIR    = HERE / "run_logs"
PROG      = HERE / "progress.log"
VERIFY_PY = HERE / "h1_verify_pkg.py"            # наша (патченная) копия
VERIFY_ORIG = Path(__file__).resolve().parent.parent / "verify_E" / "h1_verify_pkg.py"

os.environ["PYTHONIOENCODING"] = "utf-8"

# --- множество файлов архива, которые читает верификатор ------------------
GROUPS = ["point10_layer1_census_A", "point10_layer1_census_B",
          "point14_m8_base", "point17_z72_geometry",
          "point3B_localize_two_roots_agent_fix1"]

CERT_FILES = [
    "w36/audit_codex/level_tail_certificate.py",
    "w36/audit_codex/level_tail_certificate.json",
    "w36/audit_codex/m3_global_certificate.json",
    "w36/audit_codex/k_global_certificate.json",
    "w36/audit_codex/radius_K284_certificate.json",
    "w36/audit_codex/cert_slice_param_audit.py",
    "w36/audit_codex/duhamel_ds.json",
    "path_to_8/point1_A1/a1_certificate.json",
    "w33/t5_cert_sonnet/w33_gh_hiprec.json",
]

# конкретные трубочные цели (детерминированные)
T_REC_RMAX = "path_to_8/point10_layer1_census_B/cert_slice_Z72_outerbox_tube_K100_P732a6.json"
T_MIN_X128 = "path_to_8/point3B_localize_two_roots_agent_fix1/cert_slice_D_MINUS_outerbox_tube_K100_P748a23.json"
T_M8_FIRST = "path_to_8/point14_m8_base/cert_slice_ST_outerbox_tube_K100_P732a0.json"
T_CENS_A   = "path_to_8/point10_layer1_census_A/cert_slice_Z01_outerbox_tube_K100_P732a0.json"

# --------------------------------------------------------------------------
def logp(msg):
    line = time.strftime('%Y-%m-%d %H:%M:%S') + "  " + msg
    with open(PROG, "a", encoding="utf-8") as f:
        f.write(line + "\n"); f.flush()
    print(line, flush=True)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def archive_read_set():
    """Все (относительные) пути архива, читаемые верификатором."""
    s = list(CERT_FILES)
    for g in GROUPS:
        for fp in sorted((ARCH / "path_to_8" / g).glob("*_outerbox_tube_K100_*.json")):
            s.append(str(fp.relative_to(ARCH)).replace("\\", "/"))
    return sorted(set(s))

def snapshot_archive(tag):
    """Вернуть dict relpath -> sha256 для множества archive_read_set()."""
    snap = {}
    for rel in archive_read_set():
        fp = ARCH / rel
        snap[rel] = sha256_file(fp) if fp.exists() else "MISSING"
    out = HERE / ("archive_integrity_%s.txt" % tag)
    with open(out, "w", encoding="utf-8") as f:
        f.write("# sha256 снимок архива (%s); %d файлов\n" % (tag, len(snap)))
        f.write("# ARCH = %s   (READ-ONLY)\n" % ARCH)
        for rel in sorted(snap):
            f.write("%s  %s\n" % (snap[rel], rel))
    return snap

# --- сборка чистой песочницы ----------------------------------------------
def build_sandbox():
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    SANDBOX.mkdir(parents=True)
    # сертификаты
    for rel in CERT_FILES:
        src = ARCH / rel; dst = SANDBOX / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    # трубочные сертификаты 5 групп (1542 файла)
    n = 0
    for g in GROUPS:
        for fp in sorted((ARCH / "path_to_8" / g).glob("*_outerbox_tube_K100_*.json")):
            rel = fp.relative_to(ARCH)
            dst = SANDBOX / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fp, dst); n += 1
    return n

def restore(rel):
    """Восстановить файл песочницы из архива (чистое состояние)."""
    src = ARCH / rel; dst = SANDBOX / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def restore_all():
    """Полный пересинк песочницы из архива (гарантия чистоты)."""
    for rel in CERT_FILES:
        restore(rel)
    for g in GROUPS:
        for fp in sorted((ARCH / "path_to_8" / g).glob("*_outerbox_tube_K100_*.json")):
            restore(str(fp.relative_to(ARCH)).replace("\\", "/"))

# --- патч единственной строки в копии верификатора ------------------------
def patch_verifier():
    text = VERIFY_ORIG.read_text(encoding="utf-8")
    orig_line = 'ARCH = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")'
    new_line  = 'ARCH = Path(r"%s")' % str(SANDBOX).replace("\\", "/")
    assert text.count(orig_line) == 1, "ожидалась ровно одна строка ARCH"
    patched = text.replace(orig_line, new_line, 1)
    VERIFY_PY.write_text(patched, encoding="utf-8")
    # однострочный diff
    diff_path = HERE / "verifier_diff.txt"
    with open(diff_path, "w", encoding="utf-8") as f:
        f.write("односточный diff копии верификатора (verify_E -> tamper_F):\n")
        f.write("--- verify_E/h1_verify_pkg.py (строка 20)\n")
        f.write("+++ tamper_F/h1_verify_pkg.py\n")
        f.write("-@~line20~ %s\n" % orig_line)
        f.write("++        %s\n" % new_line)
        f.write("\nДругих правок нет. sha256 оригинала: %s\n" % sha256_file(VERIFY_ORIG))
        f.write("sha256 копии (патченой): %s\n" % sha256_file(VERIFY_PY))
    return orig_line, new_line

# --- запуск верификатора в песочнице --------------------------------------
def run_verifier(label):
    t0 = time.time()
    logp("[%s] run start" % label)
    proc = subprocess.run([sys.executable, str(VERIFY_PY)],
                          cwd=str(HERE), capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    dt = time.time() - t0
    out = proc.stdout or ""
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / ("%s.log" % label)).write_text(out + ("\n[exit=%d]\n" % proc.returncode), encoding="utf-8")
    logp("[%s] run done exit=%d  %.1fs" % (label, proc.returncode, dt))
    return proc.returncode, out, dt

def parse_blocks(out):
    """Вернуть (set_упавших_блоков, list_mismatch_строк)."""
    blocks = []
    import re
    for line in out.splitlines():
        m = re.search(r"=>\s*Проверка\s*(\d+):\s*(PASS|FAIL)", line)
        if m:
            blocks.append((m.group(1), m.group(2)))
    failed_blocks = [b for b, v in blocks if v == "FAIL"]
    mism = [l.strip() for l in out.splitlines() if "[MISMATCH]" in l]
    summary_line = ""
    for l in out.splitlines():
        if l.strip().startswith("упавшие блоки:"):
            summary_line = l.strip()
    return failed_blocks, mism, summary_line, blocks

# ============================ ПОРЧИ =======================================
def load(rel):
    return json.loads((SANDBOX / rel).read_text(encoding="utf-8"))
def dump(rel, obj):
    (SANDBOX / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def T01(rels):
    """P_all_levels_upper -> 2.9e-7 (всё ещё < 3e-7)."""
    restore(rels[0])
    d = load(rels[0])
    d["duhamel_all_levels"]["P_all_levels_upper"] = "[2.9e-7 +/- 0]"
    dump(rels[0], d)
    return "level_tail.P_all_levels_upper = 2.1134e-7 -> [2.9e-7 +/- 0] (всё ещё < 3e-7)"

def T02(rels):
    restore(rels[0])
    d = load(rels[0]); d["M3_chosen"] = "123479"; dump(rels[0], d)
    return "m3_global.M3_chosen = '1834' -> '123479'"

def T03(rels):
    restore(rels[0])
    d = load(rels[0]); d["radius"] = "1e-4"; dump(rels[0], d)
    return "m3_global.radius = '2e-4' -> '1e-4' (ниже Amax=1.348e-4; формула сходится, применимость исчезла)"

def T04(rels):
    restore(rels[0])
    d = load(rels[0]); d["Rmax_upper"] = 1.05; dump(rels[0], d)
    return "tube(rec Rmax P732a6).Rmax_upper = 0.885 -> 1.05 (> порога 1)"

def T05(rels):
    restore(rels[0])
    d = load(rels[0]); d["x128_lower"] = -1e-3; dump(rels[0], d)
    return "tube(min x128 P748a23).x128_lower = 1.12e-3 -> -1e-3 (знаменатель обнуляется)"

def T06(rels):
    restore(rels[0])
    p = SANDBOX / rels[0]
    if p.exists(): p.unlink()
    return "удалён один рабочий tube-JSON (point14_m8_base ...P732a0) -> счёт покрытия 1542 -> 1541"

def T07(rels):
    restore(rels[0])
    p = SANDBOX / rels[0]
    newp = p.with_name("cert_slice_NEG_" + p.name[len("cert_slice_"):])
    if newp.exists(): newp.unlink()
    p.rename(newp)
    return "рабочий диск point14_m8_base ...P732a0 переименован в cert_slice_NEG_... (total=1542, pos=1464)"

def T08(rels):
    restore(rels[0])
    d = load(rels[0])
    for c in d["negative_controls"]:
        r = str(c.get("radius", ""))
        if "0.0500000" in r or "0.05000" in r or "+/-" in r and abs(float(r.split("+/-")[0].strip("[] ")) - 0.05) < 1e-9:
            c["pass"] = True
    dump(rels[0], d)
    return "a1 негативный контроль (radius 0.05).pass = false -> true"

def T09(rels):
    restore(rels[0])
    d = load(rels[0]); base = float(d["dom_budget_each"]); d["r_s"] = base + 1e-9; dump(rels[0], d)
    return "tube(census_A Z01 P732a0).r_s != dom_budget_each (сдвиг на +1e-9)"

def T10(rels):
    restore(rels[0])
    d = load(rels[0])
    from mpmath import mp, mpf
    mp.dps = 120
    old = mpf(d["h_str"][2])
    new = old + mpf("1e-20")           # возмущение в 20-м знаке
    d["h_str"][2] = mp.nstr(new, 30)
    dump(rels[0], d)
    return "w33_gh_hiprec.h_str[2] возмущён на +1e-20 (20-й знак) -> тождество ренормализации"

def T11(rels):
    restore(rels[0])
    d = load(rels[0]); d["nDT2"] = 600.0; dump(rels[0], d)
    return "duhamel_ds.nDT2 = 193.63 -> 600.0 (L2/delta^4 -> q ~ 1.26 > 1)"

def T12(rels):
    restore(rels[0])
    d = load(rels[0])
    # переставить ключи верхнего уровня, сменить отступ, дописать посторонний ключ
    keys = list(d.keys()); keys = keys[1:] + keys[:1]
    nd = {k: d[k] for k in keys}
    nd["_audit_note_benign"] = "cosmetic-only change"
    (SANDBOX / rels[0]).write_text(json.dumps(nd, indent=4, ensure_ascii=False), encoding="utf-8")
    return "level_tail: переставлены ключи, indent 2->4, дописан посторонний ключ _audit_note_benign (косметика)"

TAMPERS = [
    ("T01", "P_all_levels_upper -> 2.9e-7",       ["w36/audit_codex/level_tail_certificate.json"], T01),
    ("T02", "M3_chosen -> 123479",                 ["w36/audit_codex/m3_global_certificate.json"], T02),
    ("T03", "radius -> 1e-4 (ниже Amax)",          ["w36/audit_codex/m3_global_certificate.json"], T03),
    ("T04", "tube Rmax_upper -> 1.05",             [T_REC_RMAX], T04),
    ("T05", "tube x128_lower -> -1e-3",            [T_MIN_X128], T05),
    ("T06", "удалить один tube-JSON",              [T_M8_FIRST], T06),
    ("T07", "переименовать рабочий диск в NEG_",   [T_M8_FIRST], T07),
    ("T08", "a1 neg-контроль 0.05 pass -> true",   ["path_to_8/point1_A1/a1_certificate.json"], T08),
    ("T09", "tube r_s != dom_budget_each",         [T_CENS_A], T09),
    ("T10", "w33 коэф. возмущён в 20-м знаке",     ["w33/t5_cert_sonnet/w33_gh_hiprec.json"], T10),
    ("T11", "nDT2 -> 600 (q > 1)",                 ["w36/audit_codex/duhamel_ds.json"], T11),
    ("T12", "косметика (ключи/пробелы/лишний ключ)",["w36/audit_codex/level_tail_certificate.json"], T12),
]

# ============================ MAIN ========================================
def main():
    LOGDIR.mkdir(parents=True, exist_ok=True)
    # обнулить прогресс-лог (новый прогон)
    PROG.write_text("", encoding="utf-8")
    logp("=== BRIEF F: батарея порч против verify_E ===")
    logp("ARCH (READ-ONLY) = %s" % ARCH)
    logp("SANDBOX          = %s" % SANDBOX)

    # 1) снимок архива ДО
    logp("step1: sha256 архива ДО")
    snap_before = snapshot_archive("BEFORE")

    # 2) сборка песочницы + патч верификатора
    logp("step2: сборка чистой песочницы")
    ntubes = build_sandbox()
    logp("       скопировано tube-файлов: %d (ожидается 1542)" % ntubes)
    logp("step2b: патч единственной строки ARCH в копии верификатора")
    orig_line, new_line = patch_verifier()
    logp("       diff: -%s" % orig_line)
    logp("              +%s" % new_line)

    # 3) baseline
    logp("step3: baseline прогон на чистой песочнице (ожидание exit 0)")
    restore_all()
    rc, out, dt = run_verifier("T00_baseline")
    fb, mm, summ, blocks = parse_blocks(out)
    logp("       baseline exit=%d упавшие_блоки=%s за %.1fs" % (rc, fb, dt))
    baseline_ok = (rc == 0 and not fb)
    if not baseline_ok:
        logp("!!! BASELINE НЕ ПРОШЁЛ — песочница кривая, дальше бессмысленно")

    # 4) 12 порч
    # ВАЖНО: перед каждой порчей — ПОЛНЫЙ пересбор песочницы (rmtree + copy),
    # иначе остатки от T06(удаление)/T07(переименование в NEG_) не чистятся и
    # счётчик файлов в check3 съезжает, маскируя чужие результаты.
    results = []
    for tid, title, rels, fn in TAMPERS:
        logp("--- %s %s ---" % (tid, title))
        build_sandbox()
        desc = fn(rels)
        rc, out, dt = run_verifier(tid)
        fb, mm, summ, blocksd = parse_blocks(out)
        caught = (rc == 1)
        results.append(dict(tid=tid, title=title, desc=desc,
                            exit=rc, caught=caught,
                            failed_blocks=fb, mismatches=mm, summary=summ,
                            dt=dt))
        logp("       %s exit=%d caught=%s blocks=%s за %.1fs"
             % (tid, rc, caught, fb, dt))

    # 5) снимок архива ПОСЛЕ
    logp("step5: sha256 архива ПОСЛЕ (sandbox вернутa в чистое состояние)")
    build_sandbox()
    snap_after = snapshot_archive("AFTER")
    changed = [r for r in snap_before if snap_before[r] != snap_after.get(r)]
    unchanged = (len(changed) == 0)
    logp("       изменённых файлов архива: %d  => %s"
         % (len(changed), "АРХИВ НЕ ИЗМЕНИЛСЯ" if unchanged else "АРХИВ ИЗМЕНЁН!!!"))

    # 6) archive_integrity.txt (финальный)
    write_integrity(snap_before, snap_after, changed, unchanged,
                    baseline_ok, orig_line, new_line, sha256_file(VERIFY_ORIG))
    # 7) TAMPER_F.md
    write_report(results, baseline_ok, unchanged, ntubes,
                 orig_line, new_line, sha256_file(VERIFY_ORIG), sha256_file(VERIFY_PY))
    logp("=== DONE ===")

def write_integrity(before, after, changed, unchanged, baseline_ok, ol, nl, h_orig):
    p = HERE / "archive_integrity.txt"
    with open(p, "w", encoding="utf-8") as f:
        f.write("# Целостность архива (IRON RULE: архив READ-ONLY)\n")
        f.write("# ARCH = %s\n" % ARCH)
        f.write("# Множество: все файлы, читаемые верификатором (%d файлов: сертификаты + 1542 tube)\n" % len(before))
        f.write("# sha256 оригинала verify_E/h1_verify_pkg.py = %s\n" % h_orig)
        f.write("#\n")
        f.write("# Снимок ДО (%d файлов):\n" % len(before))
        for r in sorted(before):
            f.write("BEFORE %s  %s\n" % (before[r], r))
        f.write("#\n")
        f.write("# Снимок ПОСЛЕ (%d файлов):\n" % len(after))
        for r in sorted(after):
            f.write("AFTER  %s  %s\n" % (after[r], r))
        f.write("#\n")
        f.write("# СВЕРКА: %d/%d файлов совпадают\n" % (len(before)-len(changed), len(before)))
        f.write("# ИЗМЕНЁННЫЕ: %s\n" % (changed if changed else "НЕТ"))
        f.write("#\n")
        f.write("ВЕРДИКТ: %s\n" % ("АРХИВ НЕ ИЗМЕНИЛСЯ — ни один байт не записан в архив. Все порчи шли на копии в tamper_F/sandbox/." if unchanged
                                    else "АРХИВ ИЗМЕНЁН — НАРУШЕНИЕ IRON RULE!"))
    return p

def write_report(results, baseline_ok, unchanged, ntubes, ol, nl, h_orig, h_copy):
    p = HERE / "TAMPER_F.md"
    L = []
    L.append("# TAMPER_F — батарея порч против независимого верификатора (verify_E)\n")
    L.append("Рабочая папка: `article_v1/v3_work/h1_package/tamper_F/`.\n")
    L.append("Верификатор-мишень: `verify_E/h1_verify_pkg.py` (НЕ правился; читался).\n")
    L.append("Копия-мишень в песочнице: `tamper_F/h1_verify_pkg.py` — отличается **одной** строкой.\n\n")
    L.append("## Целостность архива\n")
    L.append("- Множество под сверкой: %d файлов (все сертификаты + 1542 трубочных).\n" % len(archive_read_set()))
    L.append("- **Вердикт: АРХИВ НЕ ИЗМЕНИЛСЯ** (см. `archive_integrity.txt`, sha256 ДО == ПОСЛЕ).\n" if unchanged
             else "- **Вердикт: АРХИВ ИЗМЕНЁН — НАРУШЕНИЕ!**\n")
    L.append("- sha256 `verify_E/h1_verify_pkg.py` = `%s`\n\n" % h_orig)
    L.append("## Патч копии верификатора (одна строка)\n")
    L.append("```diff\n")
    L.append("- строка 20:  %s\n" % ol)
    L.append("+ строка 20:  %s\n" % nl)
    L.append("```\n")
    L.append("Других правок в копии нет. sha256 копии = `%s`\n\n" % h_copy)
    L.append("## Baseline\n")
    L.append("- чистая песочница, %d tube-файлов: exit code = %s (ожидание 0 / 26 из 26).\n\n"
             % (ntubes, "0 — PASS" if baseline_ok else "НЕ 0 — FAIL (песочница кривая)"))
    L.append("## Таблица: 12 порч\n\n")
    L.append("| № | Порча (на копии) | Ожидание | Факт: exit / упавшие блоки | Вердикт |\n")
    L.append("|---|---|---|---|---|\n")
    # ожидания
    expect = {
        "T01": "exit 1, Проверка 1 (P_all пересчёт) + Проверка 2 (P_exit==P_all)",
        "T02": "exit 1, Проверка 1 (M3_chosen==1834)",
        "T03": "exit 1, применимость: Amax < radius (Проверка 1)",
        "T04": "exit 1, Проверка 3 (Rmax_upper<1)",
        "T05": "exit 1, Проверка 3 (x128_lower>0)",
        "T06": "exit 1, Проверка 3 (всего файлов==1542)",
        "T07": "exit 1, Проверка 3 (25 дисков == 1465)",
        "T08": "exit 1, Проверка 5 (neg 0.05 pass==False)",
        "T09": "exit 1, Проверка 3 (r_s==dom_budget_each)",
        "T10": "exit 1, Проверка 6 (невязка <=1e-26)",
        "T11": "exit 1, Проверка 4 (max(q,p)<1)",
        "T12": "exit 0 (верификатор НЕ должен падать на косметике)",
    }
    verdict_ru = {True: "ЛОЖИТ (CAUGHT)", False: "НЕ ЛОВИТ"}
    for r in results:
        if r["tid"] == "T12":
            # для контрольной порчи «наоборот»: хорошо, когда exit 0
            v = "НЕ ЛОВИТ (и это правильно)" if not r["caught"] else "ЛОЖИТ (дефект: падает на косметике)"
        else:
            v = verdict_ru[r["caught"]]
        blocks = ", ".join(("Проверка %s" % b) for b in r["failed_blocks"]) if r["failed_blocks"] else "—"
        L.append("| %s | %s | %s | exit=%d; блоки: %s | **%s** |\n"
                 % (r["tid"], r["desc"], expect[r["tid"]], r["exit"], blocks, v))
    L.append("\n")
    # детали по каждой
    L.append("## Детали по каждой порче\n\n")
    for r in results:
        L.append("### %s — %s\n" % (r["tid"], r["title"]))
        L.append("- действие: %s\n" % r["desc"])
        L.append("- exit=%d, время %.1fs\n" % (r["exit"], r["dt"]))
        L.append("- упавшие блоки: %s\n" % (r["failed_blocks"] or "нет"))
        if r["mismatches"]:
            for m in r["mismatches"][:8]:
                L.append("  - %s\n" % m)
        L.append("- итоговая строка сводки: `%s`\n\n" % (r["summary"] or "—"))
    p.write_text("".join(L), encoding="utf-8")
    return p

if __name__ == "__main__":
    main()
