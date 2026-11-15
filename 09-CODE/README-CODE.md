# README-CODE.md — replication package 09-CODE [oid:repkitK2]

**Build date:** 14.08.2026 [oid:repkitK2] · **Public edition:** 15.11.2026, what changed for publication — `../PUBLICATION-NOTES.md`
**Source:** `D:\Исследования\И-1 — Нули функции H\Feigenbaum-archive\` (read only; archive not modified — see the control at the end of the file). **Network:** not required and not used.

Purpose of the package: (a) rerunning the experiment of section 7 of the article (the frozen Mandelbrot cross-check + rigorous localization of the zero Z72) and (b) re-verification of the key machine certificates of section 5 (the winding computation → assembly of the H1-package h1pkg → winding bridge). All files of the package are byte-identical to the source (size+sha256 check of every file at build time; see `MANIFEST.sha256`).

---

## 1. Package contents

| Package folder | Source in archive | Files | What it is |
|---|---|---:|---|
| `section7_mandelbrot\` | `article_v1\v2_work\unified_mandelbrot\` | 6 | §7: frozen experiment (frozen_experiment.py, results.json, REPORT_UNIFIED.md, make_report.py, logs) |
| `section7_z72_localization\` | `article_v1\v2_work\z72_localization\` | 10 | §7: rigorous Arb-localization of the zero Z72 (z72_zero_build.py / z72_zero_verify.py / z72_zero_certificate.json + exploration) |
| `section7_mside_superstable\` | `article_v1\v4_work\mside_superstable\` | 7 | §7: rigorous certification of 23 superstable parameters (Krawczyk/interval Newton, mside_certificate.py/.json, mside_verify.py, run_tampers.py, REPORT_MSIDE.md, AUDIT_FINDING.md) |
| `section5_winding_bridge\` | `article_v1\v4_work\winding_bridge\` | 6 | §5.3(v): winding bridge (bridge_certificate.py/.json, bridge_verify.py, run_tampers.py, TAMPER_LOG.md, REPORT_BRIDGE.md) |
| `section5_base_certificates\winding\` | `article_v1\v3_work\winding\` | 10 | §5: rigorous interval winding of the denominator on 25 disks (generator, verifier, battery, reports) |
| `section5_base_certificates\h1_package_cert_D\` | `article_v1\v3_work\h1_package\cert_D\` | 57 | §5: certificate of H1-package assembly (generator h1pkg_certificate.py, tight recomputation of arcs tight_run.py + tight_arcs\, verify_w.py, verify_d2.py, reconcile_R.py, reports) |
| `section5_base_certificates\h1_package_verify_E\` | `article_v1\v3_work\h1_package\verify_E\` | 6 | §5: independent verifier of the H1-package (h1_verify_pkg.py, REPORT_E.md, M3_ADJUDICATION.md) |
| `section5_base_certificates\h1_package_tamper_F\` | `article_v1\v3_work\h1_package\tamper_F\` | 10 | §5: tamper battery F (run_tampers.py, run_tampers2.py, TAMPER_F.md, TAMPER_F2.md, verifier_diff*.txt) |
| `section5_base_certificates\h1_package_lemma_A\` | `article_v1\v3_work\h1_package\lemma_A\` | 5 | §5: pinned formulations of the lemma (LEMMA_H1.md, IDENTITY_B.md, ADDENDUM_A0.md) + independent verification scripts `check_gh_at_x0.py` (g/h at x=0 from `w33_gh_hiprec.json`, see IDENTITY_B.md §B.4), `check_gprime_at_1.py` (G′(1) = −α, 132 matching digits) |
| `section5_base_certificates\h1_package_cert_strict\` | `article_v1\v3_work\release_h1\CERT\` (subset) + 2 inputs | 10 | §5: strict certificates of Lemma W and of the radius r_s — `CERT\level_tail_certificate_strict.py/.json` (‖DT(G)‖₁=22.191604188675928, ‖DT(G)²‖₁=193.634437825475…), `CERT\radius_K284_certificate.py/.json`, `CERT\_constants.py`; inputs in `DATA\inputs\` (`ndt_rigorous.json`, `m3_global_certificate.json`); see `README-STRICT.md` |
| `archive_inputs\` | `w33\`, `w35\`, `w36\`, `bench_parallel\`, `path_to_8\…` | ≈2469 | Frozen inputs with pins: 22 named files (x4_common.py, w33_gh_hiprec.json, cl34/absolute_margins/level_tail/m3/k_global/radius_K284/duhamel_ds, l_hat_fable, certificates of points 1/8b/8c/10A/10B/14/17/3B/15) + a farm of 2425 arc files `*_tube_K100_*.json` (5 working groups: 1542; audit_codex 438; slice_all 144; point2 217 — of which the folder `point2_completeness_disk7\`: 217 tube files + 14 files of the certificate of the circle |u| = 7 (DISK7_COMPLETENESS_PROOF.md, h7_circle_certificate.py/.json/.log, pilot_slice.py, run_pilot_slices.py, pilot_slice_summary.json, arcwise_rouche_certificate.py/.json/.log, h7_refined_cover.json, refine_failed_h7_arcs.py, verify_disk7_certificate.py, disk7_audit.json); point6 40; point11 12; bench_parallel 32) + `w36\proj_codex\` (8 files: `rigorous_block.json/.py`, `midpoint_probe.json/.py`, `assemble_results.json/.py`, `w36_proj.md`, `dt100_midpoint.npz` — an independent duplicate of the rigorous ‖DT(G)‖/‖DT(G)²‖ for Lemma W) |
| `_tools\` | created by builder | 3 | `rebuild_layout.py`, `verify_manifest.py` (see §5 and §8), `check_article_paths.py` — checks that all paths `09-CODE/…` and archive paths (`w33`, `w35`, `w36`, `path_to_8`, `bench_parallel`) mentioned in the package texts (00-README.md, 01-ARTICLE.md, appendices, this README) physically exist; run: `python 09-CODE/_tools/check_article_paths.py`, exit 0 = all paths resolved |

All components are < 200 MB (the whole package ≈ 12.5 MB, ≈ 2600 files, the exact number is in `MANIFEST.sha256`; the count grew by 14 after the addition of `point2_completeness_disk7\` in §1, the manifest will be recomputed on the next rebuild) — the "do not copy >200 MB" rule triggered for no component; nothing was left out by size.

## 2. What is NOT included and why

| Excluded | Reason |
|---|---|
| `winding_bridge\review_fable\`, `review_kilo\` | Direct prohibition of the brief (review materials; their conclusions are already incorporated in the certificate and TAMPER_LOG) |
| `winding_bridge\tamper_tmp\` (17 json) | Battery-tampering junk: `run_tampers.py` recreates it itself |
| `winding\__pycache__\`, `tamper_F\__pycache__\` | Interpreter-derived cache |
| `tamper_F\sandbox\` (1542 copies of arcs), `run1_backup\`, `run_logs*\`, `archive_integrity*.txt` | Regenerated by battery F on launch; snapshots of hashes of the entire archive are unreproducible from the package and are not needed for rerun |
| `verify_E\ds_E.log`, `ds_F2.log`, `kilo_F2b.log`; `lemma_A\kilo_*.log`, `progress.log`; `cert_D\kilo_*.log` | Terminal logs of agent sessions; verifiers and reports are included |
| `article_v1\v3_work\release_h1\`, `release_h1_v2\` (2×3082 duplicate arcs) | Release packaging of H1, created AFTER generation of the h1pkg certificate; not included in the certificate counters (see §9 "archive drift"); from it the subset CERT is included — see `h1_package_cert_strict\` |
| Other waves of the archive (`w35` except x4_common.py, `w36` except what is listed, neighbouring point folders) | Not read by any script of the package (verified by full grep audit of paths + control runs) |

## 3. Dependencies

- **Python 3.13** (original: 3.13.13); packages: **mpmath** (≥1.3; for §7),
  **python-flint** (0.9.0; Arb intervals, for §5 and z72-localization).
- Windows: paths in the frozen scripts are forward slashes `C:/...`, Cyrillic is not
  used in paths; POSIX — see route A2 in §5.
- Everything is single-process, except bridge_verify/winding (a small worker pool).
- Run times (measured at build time on the builder's machine): see §7.

## 4. Restoring the tree (mandatory before rerun)

The frozen scripts address inputs by the absolute path
`D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive/…`. The files must not be changed — their sha256
are pinned in the certificates. Therefore rerun = tree reconstruction:

```
python _tools\rebuild_layout.py <TARGET_FOLDER>
```

The script will lay out the package sections and `archive_inputs\` along the relative paths of the archive
(`article_v1\v2_work\…`, `path_to_8\…`, `w33\…`, etc.), refuse to work in case of any
conflict with existing files and print the next steps.

## 5. ROOT: how to launch (three routes)

> **Public edition note.** On every route the verifiers of the shipped certificates report exactly one sha256-pin mismatch, on `x4_common.py`: the certificates pin its 14.08.2026 version, and on 05.09.2026 one line of it (the absolute path of the local archive, `BASE`) was changed. Restoring that line reproduces the pinned hash exactly; no mathematics is affected. Details — `../PUBLICATION-NOTES.md`.

- **A1 (Windows, no edits, pins intact).** Make the reconstruction visible under the literal path: from an elevated prompt
  `mklink /J "D:\Исследования\И-1 — Нули функции H\Feigenbaum-archive" "<TARGET_FOLDER>"`.
  ⚠ On the author's machine, where this path is the real archive, this must NOT be done.
- **A2 (POSIX, no edits, pins intact).** Create a target folder literally named `D:`,
  inside it `Исследования/И-1 — Нули функции H/Feigenbaum-archive/…`, and run everything with cwd = the parent of this `D:` — on POSIX Python resolves `D:/…` relative to cwd.
- **B (any path, edit one line).** Replace the literal
  `D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive` with your target folder in all
  23 reconstruction .py files (including `w35\x4_walk_sonnet\x4_common.py`, line BASE).
  Consequence: on the PINNED certificates the verifiers will give exactly ONE expected pin failure (sha256 of x4_common.py); all the mathematics and the other pins will pass.
  Regeneration of YOUR OWN chain of certificates is fully self-consistent.

Below `<R>` = the root of the reconstruction (or the literal path for A1/A2).
**Work on a copy of the reconstruction:** the generators overwrite their own outputs
(results.json, *_certificate.json, logs) in the script folder.

## 6. How to rerun each component

Order of §5 branch dependencies: `winding` → `h1pkg (cert_D)` → `bridge`
(the bridge pins the sha256 of both previous certificates).

```bash
# --- §7: frozen experiment (Mandelbrot cross-check, ~40 min, mpmath) ---
cd <R>/article_v1/v2_work/unified_mandelbrot
python frozen_experiment.py            # input: path_to_8/point15_layer1_addressing/address_certificate.json
python make_report.py                  # regenerates REPORT_UNIFIED.md from results.json

# --- §7: rigorous localization of the zero Z72 (Arb, ~8 min) ---
cd <R>/article_v1/v2_work/z72_localization
python z72_zero_build.py 0.01 9 128    # arguments of the pinned certificate (r0, level_m, n_arcs)
python z72_zero_verify.py              # re-verification of z72_zero_certificate.json
python explore_z72loc.py               # (optional) numerical exploration

# --- §5: winding (generator ~4 min, verifier ~7 min, battery ~1 h) ---
cd <R>/article_v1/v3_work/winding
python winding_certificate.py          # → winding_certificate.json (25 disks, wind=0)
python winding_verify.py               # independent path, VERDICT: PASS, exit 0
python run_tampers.py                  # 8/8 tampers, TAMPER_LOG.md

# --- §5: certificate of H1-package assembly ---
cd <R>/article_v1/v3_work/h1_package/cert_D
python h1pkg_certificate.py            # ~seconds; coverage 1542 arcs + archive control 2425
python tight_run.py                    # (optional) tight recomputation of 6 arcs Z72, 4 workers
python verify_w.py                     # ADDENDUM W: recomputation of Lemma W inequalities (512-bit Arb)
cd <R>/article_v1/v3_work/h1_package/verify_E
python h1_verify_pkg.py                # independent verifier of the package: 26/26 checks
cd <R>/article_v1/v3_work/h1_package/tamper_F
python run_tampers.py                  # battery F (builds sandbox itself)
python run_tampers2.py                 # battery F2

# --- §5.3(v): winding bridge (generator ~1 min, verifier ~35 s, battery ~10 min) ---
cd <R>/article_v1/v4_work/winding_bridge
python bridge_certificate.py           # inputs: winding+h1pkg certificates, m8/census/z72/fix1, 1542 arcs
python bridge_verify.py                # VERDICT: PASS, exit 0
python run_tampers.py                  # 17/17 tampers + clean control, TAMPER_LOG.md

# --- §7: certificates of the M-side (Krawczyk/Newton, generator ~1 s, verifier ~1 s, battery ~6 s) ---
cd <R>/article_v1/v4_work/mside_superstable
python mside_certificate.py           # input: v2_work/unified_mandelbrot/results.json (pin)
python mside_verify.py                # VERDICT: PASS, exit 0
python run_tampers.py                 # 10/10 tampers + clean control, TAMPER_LOG.md
```

## 7. Expected results and exit codes (control runs [oid:repkitK2])

Control runs were performed by the builder from this package (reconstruction in a
temporary folder, Windows, Python 3.13.13, flint 0.9.0, mpmath 1.3.0; editing only
the ROOT line in one-time copies of scripts — all pins passed):

| Component | Time | Result | exit |
|---|---|---|---|
| `frozen_experiment.py` | 2407 s | verdict reproduced exactly: 22/23 MATCH, Z72 rejected, median d_u = 3.157819135948192e-05, 0/20 controls | 0 |
| `make_report.py` | <1 s | REPORT_UNIFIED.md regenerated (differences only in wall-time fields) | 0 |
| `z72_zero_build.py` (defaults) | 232 s | VERDICT: RIGOROUS (worst_margin 1.165 at n_arcs=64; pinned run — 128 arcs, margin 1.06408) | 0 |
| `z72_zero_verify.py` | 502 s | VERIFY: PASS (recomputation by a different code path + 5 internal tampers caught) | 0 |
| `winding_certificate.py` | 241 s | 25/25 disks wind=0 (in agreement with REPORT_WINDING) | 0 |
| `winding_verify.py` | 437 s | VERDICT: PASS, 23/23 mandatory, worst_min_abs=2.3631e-03 | 0 |
| `h1pkg_certificate.py` | 2 s | coverage 1542/1465/77, archive control 2425 — exact match with pinned, all_pass=true | 0 |
| `h1_verify_pkg.py` (E) | ~1 min | 26/26 checks PASS (after adding duhamel_ds.json to the package) | 0 |
| `bridge_certificate.py` | 48 s | bridge certificate regenerated; differs from the pinned only in date/timings/pins of reassembled inputs | 0 |
| `bridge_verify.py` | 34 s | VERDICT: PASS: 3 windings recomputed, 1542 files rescanned (1465 working, 77 NEG), all bridge verdicts reproduced | 0 |
| `run_tampers.py` (bridge) | 565 s | 17/17 tampers caught, clean control OK, exit 0 | 0 |
| `mside_verify.py` | 0.4 s | VERDICT: PASS, 23 roots recomputed via the tuple path (auditor run on an archive copy, identical to the package by manifest) | 0 |
| `run_tampers.py` (mside) | 6.2 s | 10/10 tampers caught, clean control OK (auditor run, same place) | 0 |

General rule: verifiers print `VERDICT: PASS`/`VERIFY: PASS` and exit 0;
any discrepancy — `FAIL` and exit 1. Tamper batteries exit 0 only if the clean
control passed and ALL tampers were caught.

## 8. Integrity of the package

`MANIFEST.sha256` (format `<sha256>  <relative path>`, sorted by path)
covers 100% of the files of the package, except the manifest itself. Not in the package and
therefore not in the manifest: `BRIEF.md` (owner's assignment) and `kilo_run.log`
(live log of the build session). Verification:

```bash
sha256sum -c MANIFEST.sha256          # git-bash / Linux / macOS
python _tools\verify_manifest.py      # cross-platform, also checks completeness of coverage
```

**Tools.** `_tools\check_article_paths.py` — a separate check (not about checksums, but about link integrity): extracts from all `.md`-files of the package (00-README, 01-ARTICLE, appendices A–G, this README) all paths of the form `09-CODE/…` and `w33|w35|w36|path_to_8|bench_parallel/…` and checks that each one physically exists in the package. Run: `python 09-CODE/_tools/check_article_paths.py` (from anywhere); exit 0 = all paths resolved, exit 1 = list of dead paths in stdout.

## 9. Honest limitations

1. **Byte reproducibility of certificates.** Generators write into JSON the date,
   timings and sha256 pins of reassembled inputs — byte-for-byte coincidence of the
   regenerator with the pinned file is not expected (and not required); verifiers
   check all meaningful fields. For the bridge, reassembly in the correct order
   (winding → h1pkg → bridge) gives a fully self-consistent chain
   (verified; see §7).
2. **Archive drift.** The field `n_k100_archive_total = 2425` — snapshot on 13.08.
   Today the real archive also contains 6168 duplicate arc files
   (release_h1/release_h1_v2), i.e. rerunning the h1pkg generator ON THE AUTHOR'S ARCHIVE
   would give 8593. Reconstruction from THIS package reproduces 2425 exactly.
3. **z72_localization.** REPORT_Z72LOC.md is marked "in progress" by the owner;
   the authoritative artifacts are z72_zero_certificate.json + z72_zero_verify.py
   (PASS). Arguments of the pinned run of build: `0.01 9 128`.
4. **Frost.** No file of the package was edited; the exception —
   files created by the builder (README, MANIFEST, `_tools\*`) are marked with a tag.
5. **Source control.** Each of the 2555 copied files was checked against the archive
   by size and sha256 at build time; the source archive was not modified
   (all control runs were on copies in a temporary folder).

## 10. Package ↔ archive correspondence map

`_tools\rebuild_layout.py` (dictionary MAP) — a machine-readable map; manually:
`section7_mandelbrot → article_v1/v2_work/unified_mandelbrot`,
`section7_z72_localization → article_v1/v2_work/z72_localization`,
`section5_winding_bridge → article_v1/v4_work/winding_bridge`,
`section7_mside_superstable → article_v1/v4_work/mside_superstable`,
`section5_base_certificates/winding → article_v1/v3_work/winding`,
`section5_base_certificates/h1_package_* → article_v1/v3_work/h1_package/{cert_D,verify_E,tamper_F,lemma_A}`,
`archive_inputs/<rel> → <rel>` (from the archive root).
