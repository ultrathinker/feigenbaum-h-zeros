# TAMPER_LOG.md — winding_certificate.json (oid 9595c48c, волна v3)

**Режим:** каждая порча -- на СВЕЖЕЙ КОПИИ `winding_certificate.json`; `winding_verify.py` запускается на копии; ожидается `exit 1` и конкретная проверка-ловушка (строка `FAIL:`).

**Чистый запуск (контроль):** `python winding_verify.py` -> exit 0 (PASS).

| # | Категория (бриф §5) | Что сломал | Какая проверка поймала | exit |
|---|---|---|---|---|
| T1 | щель в покрытии | T1 щель в покрытии дуг: disks[Z40].arc_disk_coverage_ok := false, worst_margin := -1e-6 (ложное утверждение о разрыве) | Z40 arc_disk_coverage_ok drift: cert=False recomputed=True ; Z40 coverage margin sign drift: cert=-1.000e-06 recomputed=9.814e-09 | 1 |
| T2 | обмотка (завышена/искажена) | T2 обмотка искажена: disks[Z63].winding_candidate := 1, strictly_zero := false (ложно утверждается полюс внутри контура) | Z63 winding_candidate drift: cert=1 recomputed=0 ; Z63 strictly_zero drift: cert=False recomputed=True | 1 |
| T3 | min|x| | T3 min|x_2^m| испорчен: disks[Z72].min_abs_denominator_lower := -5e-4 (< 0) | Z72 min_abs_denominator_lower drift: cert=-5.00000000e-04 recomputed=2.36311456e-03 (rel=1.21e+00) | 1 |
| T4 | sha256 | T4 sha256 пин испорчен: sha256_pins['census_A_certificate.json'] := 0000...0000 | sha256 mismatch census_A_certificate.json | 1 |
| T5 | число дуг | T5 число дуг занижено: disks[Z01].n_arcs := 2 (недостаточно, покрывающий диск дуги слишком широк) | Z01 coverage margin drift: cert=9.813535e-09 recomputed=1.414214e-07 ; Z01 min_abs_denominator_lower drift: cert=4.34931134e-03 recomputed=4.26905150e-03 (rel=1.85e-02) ; n_checks drift: cert=3250 recomputed=3130 | 1 |
| T6 | знак | T6 знак центра диска перевёрнут: disks[Z74].centre_im := -8.68634320415312 (было +) | Z74 centre drift: cert=(4.72725441425135,-8.68634320415312) raw=(4.72725441425135,8.68634320415312) | 1 |
| T7 | верхнеуровневый счётчик (бонус) | T7 верхнеуровневый счётчик испорчен: n_pass_required := 22 (было 23, all_pass оставлен true) | n_pass_required drift: cert=22 recomputed=23 | 1 |
| T8 | n_checks (бонус) | T8 n_checks не сходится с формулой: n_checks := 1 | n_checks drift: cert=1 recomputed=3250 | 1 |

**Итого:** 8 порч (>= 6 требуемых брифом), поймано 8. Все ожидают exit=1.

**Контроль (чистый сертификат, без порчи):**
- `python winding_verify.py` -> exit=0, FAIL-строк=0 (PASS как и ожидалось)