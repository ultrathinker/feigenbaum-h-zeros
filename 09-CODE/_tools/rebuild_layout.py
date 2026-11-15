#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [oid:repkitK2] rebuild_layout.py -- reconstruct the archive-relative directory
# tree expected by the frozen scripts of this replication package.
#
# The frozen scripts (generators/verifiers of sections 5 and 7) address every
# input by the ABSOLUTE path  D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive/...
# (byte-frozen: their sha256 is pinned inside the shipped certificates, so the
# package MUST NOT edit them). This helper copies the package contents into a
# target directory laid out exactly like the archive, so that either
#   (A) the target IS made to appear under that literal path (junction / POSIX
#       "C:" subdirectory trick), and the scripts run unmodified with all
#       sha256 pins intact; or
#   (B) the target is any path and you replace the literal
#       D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive with your target path in
#       the .py files (see README-CODE.md, "Route B").
#
# Safety: the script REFUSES to overwrite an existing file. If the target tree
# already contains the real archive (author's machine), it aborts before
# touching anything.
#
# Usage:  python rebuild_layout.py <TARGET_ROOT>
import shutil
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(2)

PKG = Path(__file__).resolve().parent.parent
TARGET = Path(sys.argv[1]).resolve()
LITERAL = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")

MAP = {
    "section7_mandelbrot": "article_v1/v2_work/unified_mandelbrot",
    "section7_z72_localization": "article_v1/v2_work/z72_localization",
    "section5_winding_bridge": "article_v1/v4_work/winding_bridge",
    "section7_mside_superstable": "article_v1/v4_work/mside_superstable",
    "section5_base_certificates/winding": "article_v1/v3_work/winding",
    "section5_base_certificates/h1_package_cert_D": "article_v1/v3_work/h1_package/cert_D",
    "section5_base_certificates/h1_package_verify_E": "article_v1/v3_work/h1_package/verify_E",
    "section5_base_certificates/h1_package_tamper_F": "article_v1/v3_work/h1_package/tamper_F",
    "section5_base_certificates/h1_package_lemma_A": "article_v1/v3_work/h1_package/lemma_A",
}

if TARGET == LITERAL:
    print("REFUSED: the target IS the literal archive path. Rebuilding into the")
    print("real archive is forbidden (it must stay untouched). Use a different")
    print("target and route A (junction) or route B (ROOT line edit).")
    sys.exit(2)

plan = []
for src_pre, dst_rel in MAP.items():
    for p in sorted((PKG / src_pre).rglob("*")):
        if p.is_file():
            plan.append((p, TARGET / dst_rel / p.relative_to(PKG / src_pre)))
for p in sorted((PKG / "archive_inputs").rglob("*")):
    if p.is_file():
        plan.append((p, TARGET / p.relative_to(PKG / "archive_inputs")))

clash = [(s, d) for s, d in plan if d.exists()]
if clash:
    print(f"REFUSED: {len(clash)} target file(s) already exist, e.g.:")
    for s, d in clash[:5]:
        print("  ", d)
    sys.exit(1)

for s, d in plan:
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)
print(f"OK: {len(plan)} files reconstructed under {TARGET}")

print("""
Next steps (see README-CODE.md section 'ROOT: how to re-run'):
  Route A (zero edits; sha256 pins intact except the one documented
           x4_common.py mismatch, see PUBLICATION-NOTES.md):
    Windows: make TARGET visible at the literal path, e.g. from an elevated
             prompt:  mklink /J "D:\\Исследования\\И-1 — Нули функции H\\Feigenbaum-archive" "<TARGET>"
             (do NOT do this on the author's machine, where that path is the
             real, read-only archive).
    POSIX:   choose TARGET = <CWD>/D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive
             (first component literally named  D:) and run everything with
             cwd = <CWD> -- Python resolves "D:/..." relative to cwd on POSIX.
  Route B (any path, one-line edits): in every .py under TARGET replace
             D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive  with  <TARGET>.
             Verifiers of the SHIPPED certificates will then report exactly
             one expected sha256-pin failure (x4_common.py, a pinned input);
             regenerating your own certificate chain is fully self-consistent.
""")
