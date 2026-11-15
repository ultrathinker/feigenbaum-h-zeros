# README-CODE.md — репликационный пакет 09-CODE [oid:repkitK2]

**Дата сборки:** 14.08.2026 [oid:repkitK2] · **Публичное издание:** 15.11.2026, что изменено для публикации — `../PUBLICATION-NOTES.md`. Код лежит в `../09-CODE/` (общий для обеих версий).
**Источник:** `D:\Исследования\И-1 — Нули функции H\Feigenbaum-archive\` (только чтение; архив не изменён —
см. контроль в конце файла). **Сеть:** не требуется и не используется.

Назначение пакета: (а) перезапуск эксперимента раздела 7 статьи (замороженный
Мандельброт-кроссчек + строгая локализация нуля Z72) и (б) перевёрификация
ключевых машинных сертификатов раздела 5 (обмотка winding → сборка H1-пакета
h1pkg → мост обмотки bridge). Все файлы пакета байт-идентичны источнику
(сверка размер+sha256 каждого файла — при сборке; см. `MANIFEST.sha256`).

---

## 1. Состав пакета

| Папка пакета | Источник в архиве | Файлов | Что это |
|---|---|---|---|
| `section7_mandelbrot\` | `article_v1\v2_work\unified_mandelbrot\` | 6 | §7: замороженный эксперимент (frozen_experiment.py, results.json, REPORT_UNIFIED.md, make_report.py, логи) |
| `section7_z72_localization\` | `article_v1\v2_work\z72_localization\` | 10 | §7: строгая Arb-локализация нуля Z72 (z72_zero_build.py / z72_zero_verify.py / z72_zero_certificate.json + разведка) |
| `section7_mside_superstable\` | `article_v1\v4_work\mside_superstable\` | 7 | §7: строгая сертификация 23 суперстабильных параметров (Кравчик/интервальный Ньютон, mside_certificate.py/.json, mside_verify.py, run_tampers.py, REPORT_MSIDE.md, AUDIT_FINDING.md) |
| `section5_winding_bridge\` | `article_v1\v4_work\winding_bridge\` | 6 | §5.3(v): мост обмотки (bridge_certificate.py/.json, bridge_verify.py, run_tampers.py, TAMPER_LOG.md, REPORT_BRIDGE.md) |
| `section5_base_certificates\winding\` | `article_v1\v3_work\winding\` | 10 | §5: строгая интервальная обмотка знаменателя на 25 дисках (генератор, верификатор, батарея, отчёты) |
| `section5_base_certificates\h1_package_cert_D\` | `article_v1\v3_work\h1_package\cert_D\` | 57 | §5: сертификат сборки H1-пакета (генератор h1pkg_certificate.py, тесный пересчёт дуг tight_run.py + tight_arcs\, verify_w.py, verify_d2.py, reconcile_R.py, отчёты) |
| `section5_base_certificates\h1_package_verify_E\` | `article_v1\v3_work\h1_package\verify_E\` | 6 | §5: независимый верификатор H1-пакета (h1_verify_pkg.py, REPORT_E.md, M3_ADJUDICATION.md) |
| `section5_base_certificates\h1_package_tamper_F\` | `article_v1\v3_work\h1_package\tamper_F\` | 10 | §5: батарея порч F (run_tampers.py, run_tampers2.py, TAMPER_F.md, TAMPER_F2.md, verifier_diff*.txt) |
| `section5_base_certificates\h1_package_lemma_A\` | `article_v1\v3_work\h1_package\lemma_A\` | 5 | §5: пиннуемые формулировки леммы (LEMMA_H1.md, IDENTITY_B.md, ADDENDUM_A0.md) + независимые проверки-скрипты `check_gh_at_x0.py` (g/h в x=0 из `w33_gh_hiprec.json`, см. IDENTITY_B.md §B.4), `check_gprime_at_1.py` (G′(1) = −α, 132 совпадающих знака) |
| `section5_base_certificates\h1_package_cert_strict\` | `article_v1\v3_work\release_h1\CERT\` (подмножество) + 2 входа | 10 | §5: строгие сертификаты леммы W и радиуса r_s — `CERT\level_tail_certificate_strict.py/.json` (‖DT(G)‖₁=22.191604188675928, ‖DT(G)²‖₁=193.634437825475…), `CERT\radius_K284_certificate.py/.json`, `CERT\_constants.py`; входы в `DATA\inputs\` (`ndt_rigorous.json`, `m3_global_certificate.json`); см. `README-STRICT.md` |
| `archive_inputs\` | `w33\`, `w35\`, `w36\`, `bench_parallel\`, `path_to_8\…` | ≈2469 | Замороженные входы с пинами: 22 именованных файла (x4_common.py, w33_gh_hiprec.json, cl34/absolute_margins/level_tail/m3/k_global/radius_K284/duhamel_ds, l_hat_fable, сертификаты точек 1/8b/8c/10A/10B/14/17/3B/15) + ферма 2425 дуговых файлов `*_tube_K100_*.json` (5 рабочих групп: 1542; audit_codex 438; slice_all 144; point2 217 — из них папка `point2_completeness_disk7\`: 217 tube-файлов + 14 файлов сертификата окружности |u| = 7 (DISK7_COMPLETENESS_PROOF.md, h7_circle_certificate.py/.json/.log, pilot_slice.py, run_pilot_slices.py, pilot_slice_summary.json, arcwise_rouche_certificate.py/.json/.log, h7_refined_cover.json, refine_failed_h7_arcs.py, verify_disk7_certificate.py, disk7_audit.json); point6 40; point11 12; bench_parallel 32) + `w36\proj_codex\` (8 файлов: `rigorous_block.json/.py`, `midpoint_probe.json/.py`, `assemble_results.json/.py`, `w36_proj.md`, `dt100_midpoint.npz` — независимый дубликат строгих ‖DT(G)‖/‖DT(G)²‖ для леммы W) |
| `_tools\` | создано сборщиком | 3 | `rebuild_layout.py`, `verify_manifest.py` (см. §5 и §8), `check_article_paths.py` — проверяет, что все пути `09-CODE/…` и архивные (`w33`, `w35`, `w36`, `path_to_8`, `bench_parallel`), упомянутые в текстах комплекта (00-README.md, 01-ARTICLE.md, приложения, это README), физически существуют; запуск: `python 09-CODE/_tools/check_article_paths.py`, exit 0 = все пути разрешились |

Все компоненты < 200 МБ (весь пакет ≈ 12.5 МБ, ≈ 2600 файлов, точное число — в `MANIFEST.sha256`; счёт вырос на 14 после добавления `point2_completeness_disk7\` в §1, манифест будет пересчитан при следующей пересборке) — правило «>200 МБ не
копировать» не сработало ни для одного компонента; ничего не оставлено за бортом
по размеру.

## 2. Что НЕ включено и почему

| Исключено | Причина |
|---|---|
| `winding_bridge\review_fable\`, `review_kilo\` | Прямой запрет брифа (материалы ревизий; их выводы уже внесены в сертификат и TAMPER_LOG) |
| `winding_bridge\tamper_tmp\` (17 json) | Мусор батареи порч: `run_tampers.py` пересоздаёт её сам |
| `winding\__pycache__\`, `tamper_F\__pycache__\` | Производный кэш интерпретатора |
| `tamper_F\sandbox\` (1542 копии дуг), `run1_backup\`, `run_logs*\`, `archive_integrity*.txt` | Регенерируются батареей F при запуске; снапшоты хэшей всего архива невоспроизводимы из пакета и не нужны для перезапуска |
| `verify_E\ds_E.log`, `ds_F2.log`, `kilo_F2b.log`; `lemma_A\kilo_*.log`, `progress.log`; `cert_D\kilo_*.log` | Терминальные журналы сессий агентов; верификаторы и отчёты включены |
| `article_v1\v3_work\release_h1\`, `release_h1_v2\` (2×3082 дубликатных дуг) | Релизная упаковка H1, созданная ПОСЛЕ генерации h1pkg-сертификата; в счётчики сертификата не входит (см. §9 «дрейф архива»); из неё включено подмножество CERT — см. `h1_package_cert_strict\` |
| Прочие волны архива (`w35` кроме x4_common.py, `w36` кроме перечисленного, соседние point-папки) | Не читаются ни одним скриптом пакета (проверено полным grep-аудитом путей + контрольными прогонами) |

## 3. Зависимости

- **Python 3.13** (оригинал: 3.13.13); пакеты: **mpmath** (≥1.3; для §7),
  **python-flint** (0.9.0; Arb-интервалы, для §5 и z72-локализации).
- Windows: пути в замороженных скриптах — прямые слэши `C:/...`, кириллица не
  используется в путях; POSIX — см. маршрут A2 в §5.
- Всё однопроцессное, кроме bridge_verify/winding (малый пул воркеров).
- Время прогонов (замерено при сборке, машина сборщика): см. §7.

## 4. Восстановление дерева (обязательно перед перезапуском)

Замороженные скрипты адресуют входы абсолютным путём
`D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive/…`. Файлы менять нельзя — их sha256
запинена в сертификатах. Поэтому перезапуск = реконструкция дерева:

```
python _tools\rebuild_layout.py <ЦЕЛЕВАЯ_ПАПКА>
```

Скрипт разложит секции пакета и `archive_inputs\` по rel-путям архива
(`article_v1\v2_work\…`, `path_to_8\…`, `w33\…` и т.д.), откажется работать при
любом конфликте с существующими файлами и распечатает дальнейшие шаги.

## 5. ROOT: как запустить (три маршрута)

> **Примечание к публичному изданию.** На любом маршруте верификаторы поставленных сертификатов дают ровно одно расхождение пина sha256 — на `x4_common.py`: сертификаты закрепили его версию от 14.08.2026, а 05.09.2026 в нём изменили одну строку (абсолютный путь локального архива, `BASE`). Если вернуть эту строку, хеш совпадает с пином в точности; математика не затронута. Подробно — `../PUBLICATION-NOTES.md`.

- **A1 (Windows, без правок, пины целы).** Сделать реконструкцию видимой по
  буквальному пути: из повышенного промпта
  `mklink /J "D:\Исследования\И-1 — Нули функции H\Feigenbaum-archive" "<ЦЕЛЕВАЯ_ПАПКА>"`.
  ⚠ На машине автора, где этот путь — реальный архив, так делать НЕЛЬЗЯ.
- **A2 (POSIX, без правок, пины целы).** Создать целевую папку с именем `D:`
  (буквально), внутри — `Исследования/И-1 — Нули функции H/Feigenbaum-archive/…`, и запускать
  всё с cwd = родитель этой `D:` — Python на POSIX резолвит `D:/…` относительно cwd.
- **B (любой путь, правка одной строки).** Заменить литерал
  `D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive` на вашу целевую папку во всех
  23 .py реконструкции (включая `w35\x4_walk_sonnet\x4_common.py`, строка BASE).
  Следствие: у ШИПОВАННЫХ сертификатов верификаторы дадут ровно ОДИН ожидаемый
  отказ пина (sha256 x4_common.py); вся математика и остальные пины пройдут.
  Регенерация СВОЕЙ цепочки сертификатов полностью самосогласованна.

Далее `<R>` = корень реконструкции (или литеральный путь для A1/A2).
**Работайте на копии реконструкции:** генераторы перезаписывают свои выходы
(results.json, *_certificate.json, логи) в папке скрипта.

## 6. Как перезапустить каждый компонент

Порядок зависимостей ветки §5: `winding` → `h1pkg (cert_D)` → `bridge`
(мост пинит sha256 обоих предыдущих сертификатов).

```bash
# --- §7: замороженный эксперимент (мандельброт-кроссчек, ~40 мин, mpmath) ---
cd <R>/article_v1/v2_work/unified_mandelbrot
python frozen_experiment.py            # вход: path_to_8/point15_layer1_addressing/address_certificate.json
python make_report.py                  # перерисует REPORT_UNIFIED.md из results.json

# --- §7: строгая локализация нуля Z72 (Arb, ~8 мин) ---
cd <R>/article_v1/v2_work/z72_localization
python z72_zero_build.py 0.01 9 128    # аргументы шипованного сертификата (r0, level_m, n_arcs)
python z72_zero_verify.py              # перевёрификация z72_zero_certificate.json
python explore_z72loc.py               # (опционально) численная разведка

# --- §5: обмотка (генератор ~4 мин, верификатор ~7 мин, батарея ~1 ч) ---
cd <R>/article_v1/v3_work/winding
python winding_certificate.py          # → winding_certificate.json (25 дисков, wind=0)
python winding_verify.py               # независимый путь, VERDICT: PASS, exit 0
python run_tampers.py                  # 8/8 порч, TAMPER_LOG.md

# --- §5: сертификат сборки H1-пакета ---
cd <R>/article_v1/v3_work/h1_package/cert_D
python h1pkg_certificate.py            # ~секунды; покрытие 1542 дуг + архивный контроль 2425
python tight_run.py                    # (опционально) тесный пересчёт 6 дуг Z72, 4 воркера
python verify_w.py                     # ADDENDUM W: пересчёт неравенств леммы W (512-bit Arb)
cd <R>/article_v1/v3_work/h1_package/verify_E
python h1_verify_pkg.py                # независимый верификатор пакета: 26/26 проверок
cd <R>/article_v1/v3_work/h1_package/tamper_F
python run_tampers.py                  # батарея F (строит sandbox сам)
python run_tampers2.py                 # батарея F2

# --- §5.3(v): мост обмотки (генератор ~1 мин, верификатор ~35 с, батарея ~10 мин) ---
cd <R>/article_v1/v4_work/winding_bridge
python bridge_certificate.py           # входы: winding+h1pkg сертификаты, m8/census/z72/fix1, 1542 дуги
python bridge_verify.py                # VERDICT: PASS, exit 0
python run_tampers.py                  # 17/17 порч + чистый контроль, TAMPER_LOG.md

# --- §7: сертификаты M-стороны (Кравчик/Ньютон, генератор ~1 с, верификатор ~1 с, батарея ~6 с) ---
cd <R>/article_v1/v4_work/mside_superstable
python mside_certificate.py           # вход: v2_work/unified_mandelbrot/results.json (pin)
python mside_verify.py                # VERDICT: PASS, exit 0
python run_tampers.py                 # 10/10 порч + чистый контроль, TAMPER_LOG.md
```

## 7. Ожидаемые результаты и exit-коды (фиксация контрольных прогонов [oid:repkitK2])

Контрольные прогоны выполнены сборщиком из этого пакета (реконструкция во
временной папке, Windows, Python 3.13.13, flint 0.9.0, mpmath 1.3.0; правка
только строки ROOT в одноразовых копиях скриптов — все пины прошли):

| Компонент | Время | Результат | exit |
|---|---|---|---|
| `frozen_experiment.py` | 2407 с | вердикт воспроизведён в точности: 22/23 MATCH, Z72 rejected, median d_u = 3.157819135948192e-05, 0/20 контролей | 0 |
| `make_report.py` | <1 с | REPORT_UNIFIED.md регенерирован (отличие только в полях wall time) | 0 |
| `z72_zero_build.py` (defaults) | 232 с | VERDICT: RIGOROUS (worst_margin 1.165 при n_arcs=64; шипованный прогон — 128 дуг, margin 1.06408) | 0 |
| `z72_zero_verify.py` | 502 с | VERIFY: PASS (пересчёт другим кодовым путём + 5 внутренних порч пойманы) | 0 |
| `winding_certificate.py` | 241 с | 25/25 дисков wind=0 (согласовано с REPORT_WINDING) | 0 |
| `winding_verify.py` | 437 с | VERDICT: PASS, 23/23 обязательных, worst_min_abs=2.3631e-03 | 0 |
| `h1pkg_certificate.py` | 2 с | покрытие 1542/1465/77, архивный контроль 2425 — точное совпадение с шипованным, all_pass=true | 0 |
| `h1_verify_pkg.py` (E) | ~1 мин | 26/26 проверок PASS (после добавления duhamel_ds.json в пакет) | 0 |
| `bridge_certificate.py` | 48 с | сертификат моста регенерирован; отличие от шипованного только date/тайминги/пины пересобранных входов | 0 |
| `bridge_verify.py` | 34 с | VERDICT: PASS: 3 обмотки пересчитаны, 1542 файла пересканированы (1465 рабочих, 77 NEG), все вердикты моста воспроизведены | 0 |
| `run_tampers.py` (мост) | 565 с | 17/17 порч пойманы, чистый контроль OK, exit 0 | 0 |
| `mside_verify.py` | 0.4 с | VERDICT: PASS, 23 корня пересчитаны кортежным путём (прогон аудитора по архивной копии, идентичной пакету по манифесту) | 0 |
| `run_tampers.py` (mside) | 6.2 с | 10/10 порч пойманы, чистый контроль OK (прогон аудитора, там же) | 0 |

Общее правило: верификаторы печатают `VERDICT: PASS`/`VERIFY: PASS` и exit 0;
любое расхождение — `FAIL` и exit 1. Батареи порч выходят 0 только если чистый
контроль прошёл и ВСЕ порчи пойманы.

## 8. Целостность пакета

`MANIFEST.sha256` (формат `<sha256>  <относительный путь>`, сортировка по пути)
покрывает 100% файлов пакета, кроме самого манифеста. Не входят в пакет и
потому не в манифесте: `BRIEF.md` (задание владельца) и `kilo_run.log`
(живой журнал сессии сборки). Проверка:

```bash
sha256sum -c MANIFEST.sha256          # git-bash / Linux / macOS
python _tools\verify_manifest.py      # кросс-платформенно, проверяет и полноту покрытия
```

**Инструменты.** `_tools\check_article_paths.py` — отдельная проверка (не про контрольные суммы, а про целостность ссылок): вытаскивает из всех `.md`-файлов комплекта (00-README, 01-ARTICLE, приложения A–G, это README) все пути вида `09-CODE/…` и `w33|w35|w36|path_to_8|bench_parallel/…` и проверяет, что каждый физически существует в пакете. Запуск: `python 09-CODE/_tools/check_article_paths.py` (из любого места); exit 0 = все пути разрешились, exit 1 = список мёртвых путей в stdout.

## 9. Честные ограничения

1. **Байтовая воспроизводимость сертификатов.** Генераторы пишут в JSON дату,
   тайминги и sha256-пины пересобранных входов — байт-в-байт совпадение
   регенерата с шипованным файлом не ожидается (и не требуется); верификаторы
   сверяют все содержательные поля. Для моста пересборка в правильном порядке
   (winding → h1pkg → bridge) даёт полностью самосогласованную цепочку
   (проверено; см. §7).
2. **Дрейф архива.** Поле `n_k100_archive_total = 2425` — снимок на 13.08.
   Сегодня реальный архив содержит ещё 6168 дубликатных дуговых файлов
   (release_h1/release_h1_v2), т.е. перезапуск генератора h1pkg НА АРХИВЕ
   автора дал бы 8593. Реконструкция из ЭТОГО пакета воспроизводит 2425 точно.
3. **z72_localization.** REPORT_Z72LOC.md помечен владельцем «в работе»;
   авторитетные артефакты — z72_zero_certificate.json + z72_zero_verify.py
   (PASS). Аргументы шипованного прогона билда: `0.01 9 128`.
4. **Замороженность.** Никакой файл пакета не редактировался; исключение —
   файлы, созданные сборщиком (README, MANIFEST, `_tools\*`), помечены тегом.
5. **Контроль источника.** Каждый из 2555 скопированных файлов сверен с
   архивом по размеру и sha256 при сборке; архив-источник не изменялся
   (все контрольные прогоны шли по копиям во временной папке).

## 10. Карта соответствия пакета ↔ архива

`_tools\rebuild_layout.py` (словарь MAP) — машинно-читаемая карта; вручную:
`section7_mandelbrot → article_v1/v2_work/unified_mandelbrot`,
`section7_z72_localization → article_v1/v2_work/z72_localization`,
`section5_winding_bridge → article_v1/v4_work/winding_bridge`,
`section7_mside_superstable → article_v1/v4_work/mside_superstable`,
`section5_base_certificates/winding → article_v1/v3_work/winding`,
`section5_base_certificates/h1_package_* → article_v1/v3_work/h1_package/{cert_D,verify_E,tamper_F,lemma_A}`,
`archive_inputs/<rel> → <rel>` (от корня архива).
