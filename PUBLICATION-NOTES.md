# Public edition: what was changed

This repository is the replication package of version 2.5 (frozen 16.08.2026), prepared for publication on
15.11.2026. The mathematics, the certificates and the data are untouched. Everything that differs from the
frozen package is listed here.

The frozen manifest is kept as `09-CODE/_tools/MANIFEST.original.sha256`; the current one is
`09-CODE/MANIFEST.sha256`. Of the 2599 entries of the frozen manifest, **2584 are byte-identical** in this
repository, 11 were modified and 4 removed; 1 files were added.

## 1. Removed

Terminal logs of tool sessions that were used while assembling the package; they are not inputs or outputs of
any certificate. The package build brief (`BRIEF.md` in `09-CODE/`; it was never part of the frozen manifest) and the
working folder of the translation and editorial review were not published either.

Inside `09-CODE/`:

- `section5_base_certificates/h1_package_cert_D/kilo_CD.log`
- `section5_base_certificates/h1_package_cert_D/kilo_D2.log`
- `section5_base_certificates/h1_package_cert_D/kilo_R.log`
- `section5_base_certificates/h1_package_cert_D/kilo_W.log`

## 2. Modified

- Run logs (`*.log`): the absolute path of the author's local archive was replaced by `<ARCHIVE_ROOT>`.
  Logs are not pinned by any certificate.
- `README-CODE.md`: build line, public-edition notes, and the POSIX route A2 corrected to the current path.
- `_tools/rebuild_layout.py`: the printed POSIX hint corrected to the current path (the layout map is unchanged).

- `09-CODE/README-CODE.md`
- `09-CODE/_tools/rebuild_layout.py`
- `09-CODE/archive_inputs/path_to_8/point2_completeness_disk7/arcwise_rouche_certificate.log`
- `09-CODE/archive_inputs/path_to_8/point2_completeness_disk7/h7_circle_certificate.log`
- `09-CODE/section5_base_certificates/h1_package_cert_D/progress.log`
- `09-CODE/section5_base_certificates/h1_package_tamper_F/h1_verify_pkg.log`
- `09-CODE/section5_base_certificates/h1_package_tamper_F/progress.log`
- `09-CODE/section5_base_certificates/h1_package_tamper_F/progress2.log`
- `09-CODE/section5_base_certificates/h1_package_verify_E/h1_verify_pkg.log`
- `09-CODE/section7_mandelbrot/progress.log`
- `09-CODE/section7_mandelbrot/run_stdout.log`

Outside `09-CODE/`: author line added under the title of `01-ARTICLE.md` and `ru/01-ARTICLE.md`.

## 3. Added

- `09-CODE/_tools/MANIFEST.original.sha256`

Repository files: `README.md`, `README.ru.md`, `PUBLICATION-NOTES.md`, `CITATION.cff`, `LICENSE`,
`.gitattributes` (stores every file byte-for-byte, so the sha256 checks hold after cloning on any platform),
and `ru/` (Russian text of the article and appendices, `ru/README-CODE.md`; the code is shared).

## 4. The one expected pin mismatch: `x4_common.py`

`09-CODE/archive_inputs/w35/x4_walk_sonnet/x4_common.py` is a pinned input of the winding-bridge certificate.
The certificate pins its version of 14.08.2026 (sha256 `1770a7bec2677e999a608543b5c2dc70b19e4cf00b554ee9a776db4a3e020f08`).
On 05.09.2026 the local archive was moved, and the absolute path in the single line `BASE` of this file (and of
the other frozen scripts) was updated. Therefore `bridge_verify.py` reports exactly one discrepancy, the sha256 of
`x4_common.py`, on every route of `README-CODE.md` §5. Replacing the current `BASE` literal by the original one
reproduces the pinned hash exactly (checked 15.11.2026); the file differs in nothing else.

## 5. Checks run on this edition (15.11.2026)

On a tree rebuilt from this repository with `_tools/rebuild_layout.py` and route B of `README-CODE.md` §5
(Windows, Python 3.13.13, python-flint 0.9.0):

| Verifier | Result |
|---|---|
| `mside_verify.py` | `VERDICT: PASS` — 23 roots recomputed (Krawczyk, interval Newton) |
| `h1_verify_pkg.py` | 26 of 26 checks passed |
| `bridge_verify.py` | all checks passed except the expected `x4_common.py` pin (section 4) |
| `_tools/verify_manifest.py` | `RESULT: OK` — the manifest covers 100% of files, all hashes match |
| `_tools/check_article_paths.py` | exit 0 — every path cited in the texts exists |

Longer components (the frozen experiment of §7, about 40 min; winding, z72 localization, tamper batteries) were
not rerun for this edition; their registered results are in `README-CODE.md` §7.
