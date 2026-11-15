#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [oid:repkitK2] verify_manifest.py -- check MANIFEST.sha256 of this package.
# Covers 100% of package files (manifest itself excluded). Files that are
# deliberately NOT part of the package (BRIEF.md = owner's task file,
# kilo_run.log = live session log of the packaging run) are reported as
# documented exceptions, not as coverage gaps.
#
# Usage:  python verify_manifest.py [path-to-MANIFEST.sha256]
import hashlib
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
MANIFEST = Path(sys.argv[1]) if len(sys.argv) > 1 else PKG / "MANIFEST.sha256"
EXCEPTIONS = {"BRIEF.md", "kilo_run.log",
              "section5_base_certificates/h1_package_cert_strict/progress.log"}  # runtime log of the strict certificates

entries = {}
for line in MANIFEST.read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    h, _, rel = line.partition("  ")
    assert len(h) == 64, f"bad hash line: {line!r}"
    entries[rel.strip()] = h

def sha256(p: Path) -> str:
    hsh = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            hsh.update(chunk)
    return hsh.hexdigest()

bad = 0
for rel, h in sorted(entries.items()):
    p = PKG / rel
    if not p.is_file():
        print(f"MISSING  {rel}")
        bad += 1
    elif sha256(p) != h:
        print(f"HASH MISMATCH  {rel}")
        bad += 1

on_disk = {p.relative_to(PKG).as_posix() for p in PKG.rglob("*") if p.is_file()}
uncovered = sorted(on_disk - set(entries) - EXCEPTIONS - {MANIFEST.name})
missing_on_disk = sorted(set(entries) - on_disk)

print(f"manifest entries: {len(entries)}; files on disk (package root): {len(on_disk)}")
if uncovered:
    print("FILES NOT COVERED BY MANIFEST:")
    for r in uncovered:
        print("  ", r)
    bad += len(uncovered)
for r in missing_on_disk:
    print("MANIFEST ENTRY WITHOUT FILE:", r)
print("RESULT:", "FAIL" if bad else "OK -- manifest covers 100% of package files, all hashes match")
sys.exit(1 if bad else 0)
