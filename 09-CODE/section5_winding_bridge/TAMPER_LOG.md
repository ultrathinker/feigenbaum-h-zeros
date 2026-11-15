# TAMPER_LOG.md -- tamper battery for bridge_certificate.json

Date: 2026-08-14 15:15. Clean control: exit=0 (expect 0) -> OK.

| # | corruption | caught | exit | first failing check |
|---|---|---|---|---|
| T1 | T1 Z57@8 winding_candidate := 1 (strictly_zero/pass/aggregates kept true) | CAUGHT | 1 | FAIL: Z57@m=8 winding_candidate drift: cert=1 recomputed=0 |
| T2 | T2 Z60@8 max_w_upper 0.4 -> 0.999 (below the /w/<1 threshold) | CAUGHT | 1 | FAIL: Z60@m=8 max_w_upper drift: cert=0.999 recomputed=0.4 |
| T3 | T3 Z01@L7 tube_min_x128_lower /= 1000 (still > 0, flags kept) | CAUGHT | 1 | FAIL: Z01@L7 tube min drift: cert=4.349307507007647e-06 rescanned=0.004349307507007647 |
| T4 | T4 sha256 pin winding_certificate.json := 000...0 | CAUGHT | 1 | FAIL: sha256 mismatch winding_certificate.json: cert=0000000000000000000000000000000000000000000000000000000000000000 actual=9d6415e496b3d2dd6ac87dab80307ccf56c |
| T5 | T5 containment P_tail := 6e-7 (> tube radius) with flags kept true | CAUGHT | 1 | FAIL: P_tail drift: cert=6e-07 h1pkg=4.569263785657037e-07 |
| T6 | T6 Z72@L8 tube_n_arcs 64 -> 128 | CAUGHT | 1 | FAIL: Z72@L8 tube_n_arcs drift: cert=128 rescanned=64 |
| T7 | T7 Z57 required_levels [7,8] -> [7] | CAUGHT | 1 | FAIL: Z57 required_levels drift: cert=[7] expected=[7, 8] |
| T8 | T8 Z60@8 centre_re last digit nudged (vs raw m8_certificate.json) | CAUGHT | 1 | FAIL: Z60@m=8 geometry drift vs raw cert: cert=(8.26332724866472,4.01596385048377,0.1) raw=(8.26332724866471,4.01596385048377,0.1) |
| T9 | T9 legacy_z72_old_contour_arcs 24 -> 0 | CAUGHT | 1 | FAIL: legacy Z72 arc count drift: cert=0 rescanned=24 |
| T10 | T10 Z72@L7 coverage claimed via partial stage9 family (pre-fix bug simulated) | CAUGHT | 1 | FAIL: Z72@L7 tube_n_arcs drift: cert=128 rescanned=64 |
| T11 | T11 containment_margin := 1.874e-7 (two-term headroom instead of real one) | CAUGHT | 1 | FAIL: containment_margin drift: cert=1.874e-07 recomputed=8.70736214342963e-08 |
| T12 | T12 Z57@8 min_abs_denominator_lower *= 0.985 (inside old 2e-2 tolerance) | CAUGHT | 1 | FAIL: Z57@m=8 min_abs_denominator drift: cert=0.0030308582676307873 recomputed=0.0030765787110826697 |
| T13 | T13 Z01 tube family attributed to census_B instead of census_A | CAUGHT | 1 | FAIL: Z01@L7 family set drift: cert=['point10_layer1_census_B:Z01'] rescanned=['point10_layer1_census_A:Z01'] |
| T14 | T14 (kilo K1) stray_tube_labels_nonblocking := [] | CAUGHT | 1 | FAIL: stray list drift: cert=[] rescanned=['ST (group point14_m8_base)'] |
| T15 | T15 (kilo K2) Z40@L7 winding_source forged | CAUGHT | 1 | FAIL: Z40@L7 winding_source drift: cert=bridge_certificate.py (new, m=7) expected=winding_certificate.json |
| T16 | T16 (kilo K3) Z57@8 n_arcs 32 -> 64 | CAUGHT | 1 | FAIL: Z57@m=8 n_arcs drift: cert=64 adaptive-recomputed=32 |
| T17 | T17 (kilo K4) Z40@L7 winding_strictly_zero := false (bridged kept true) | CAUGHT | 1 | FAIL: Z40@L7 winding_strictly_zero drift: cert=False recomputed=True |

**Total: 17/17 caught. Clean control OK.** (555s)