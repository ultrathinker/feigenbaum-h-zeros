# -*- coding: utf-8 -*-
"""
check_article_paths.py -- every path of the form 09-CODE/... (or 09-CODE\\...)
quoted in the manuscript files (00-README.md, 01-ARTICLE.md, 02..08 appendices,
09-CODE/README-CODE.md) must exist in the package.  Also checks the bare
archive-style paths `w33/...`, `w35/...`, `w36/...`, `path_to_8/...`,
`bench_parallel/...` against 09-CODE/archive_inputs/.

Usage:  python 09-CODE/_tools/check_article_paths.py   (from the package root or anywhere)
Exit code 0 = all resolved, 1 = dead paths found (listed).
"""
import os
import re
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(TOOLS)               # .../09-CODE
ROOT = os.path.dirname(CODE)                # package root with 00-README.md etc.

md_files = [f for f in os.listdir(ROOT) if f.lower().endswith(".md")]
md_files = [os.path.join(ROOT, f) for f in sorted(md_files)]
md_files.append(os.path.join(CODE, "README-CODE.md"))

pat_code = re.compile(r"09-CODE[\\/][^\s`'\"\)\]\|>,;:]*")
pat_arch = re.compile(r"(?<![\w/\\.-])((?:w33|w35|w36|path_to_8|bench_parallel)[\\/][^\s`'\"\)\]\|>,;:]*)")

dead = []
seen = set()
for f in md_files:
    if not os.path.exists(f):
        continue
    txt = open(f, encoding="utf-8", errors="replace").read()
    for m in pat_code.finditer(txt):
        p = m.group(0).rstrip(".…")
        rel = re.sub(r"^09-CODE[\\/]", "", p).replace("\\", "/")
        # strip trailing ':<line numbers>' like file.py:26-34
        rel_nol = re.sub(r":\d[\d\-–,]*$", "", rel)
        cand = os.path.join(CODE, rel_nol)
        key = (os.path.basename(f), p)
        if key in seen:
            continue
        seen.add(key)
        if not os.path.exists(cand):
            dead.append((os.path.basename(f), p))
    for m in pat_arch.finditer(txt):
        p = m.group(1).rstrip(".…")
        rel = p.replace("\\", "/")
        rel_nol = re.sub(r":\d[\d\-–,]*$", "", rel).rstrip("/")
        if not rel_nol.split("/", 1)[1:] :      # bare 'w36/' — folder mention, skip
            continue
        cand = os.path.join(CODE, "archive_inputs", rel_nol)
        key = (os.path.basename(f), p)
        if key in seen:
            continue
        seen.add(key)
        if not os.path.exists(cand):
            dead.append((os.path.basename(f), p))

print("checked %d manuscript files, %d distinct path mentions" % (len(md_files), len(seen)))
if dead:
    print("DEAD PATHS (%d):" % len(dead))
    for f, p in dead:
        print("  %-22s %s" % (f, p))
    sys.exit(1)
print("all paths resolve inside the package")
