# -*- coding: utf-8 -*-
"""Run the audited w36 stable-slice machine on a generic pilot circle.

The large proof kernel remains the frozen
``w36/audit_codex/cert_slice_param_audit.py``.  This launcher performs
three exact source substitutions before execution: the contour radius,
the optional fattening, and the tooth-centre lookup.  Keeping the kernel
unchanged makes later diff/audit straightforward while allowing the new
circle |u|=R about the origin.

Usage:
  python pilot_slice.py base 0 "" P7 128 0
  python pilot_slice.py tube 100 "" P7 128 0
"""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
SOURCE = ROOT / "w36" / "audit_codex" / "cert_slice_param_audit.py"

source = SOURCE.read_text(encoding="utf-8")

old_constants = "FAT = 0.01\nR_CONTOUR = 0.1"
new_constants = (
    "FAT = float(os.environ.get('PILOT_FAT', '0.0'))\n"
    "R_CONTOUR = float(os.environ.get('PILOT_RADIUS', '7.0'))"
)
if source.count(old_constants) != 1:
    raise RuntimeError("frozen kernel constants no longer match")
source = source.replace(old_constants, new_constants)

old_geometry = """key = {"A": "A", "B": "B", "C": "C", "D": "D", "N": "new"}[TOOTH]
r0, arg0 = xc.TEETH_NEW[key]
u0c = r0 * complex(math.cos(arg0), math.sin(arg0))"""
new_geometry = """if TOOTH != "P7":
    raise RuntimeError(f"pilot launcher expects TOOTH=P7, got {TOOTH!r}")
u0c = complex(
    float(os.environ.get("PILOT_CENTER_RE", "0.0")),
    float(os.environ.get("PILOT_CENTER_IM", "0.0")),
)"""
if source.count(old_geometry) != 1:
    raise RuntimeError("frozen kernel geometry no longer matches")
source = source.replace(old_geometry, new_geometry)

# Close the inherited base-function tail gap explicitly.  CL-34 gives full
# l1 distances from the stored polynomial centres.  For |z|=r<1,
# |e(z)|<=||e||_1 and |e'(z)|<=||e||_1/(1-r)^2.  Fresh scalar disks at every
# step forget correlations and are therefore a rigorous outer enclosure.
old_tail_anchor = """ZERO_ACB = flint.acb(0)
ONE_ACB = flint.acb(1)"""
new_tail_anchor = """ZERO_ACB = flint.acb(0)
ONE_ACB = flint.acb(1)
_CL34 = json.load((W36 / "tail_codex" / "cl34_certificate.json").open())
EPS_G_FULL = flint.arb(_CL34["G"]["distance_and_Taylor_tail_upper"]).upper()
EPS_H_FULL = flint.arb(_CL34["V_h_delta"]["h_error_stored_center_upper"]).upper()"""
if source.count(old_tail_anchor) != 1:
    raise RuntimeError("frozen kernel tail anchor no longer matches")
source = source.replace(old_tail_anchor, new_tail_anchor)

old_horner_block = """        vg = af_horner(G1, z)
        vh = af_horner(H1, z)
        vgp = af_horner(DG1, z)
        vhp = af_horner(DH1, z)"""
new_horner_block = """        vg = af_horner(G1, z)
        vh = af_horner(H1, z)
        vgp = af_horner(DG1, z)
        vhp = af_horner(DH1, z)
        _derivative_tail_factor = 1 / ((1-rz)*(1-rz))
        vg = AF(vg.c, vg.a, vg.r + EPS_G_FULL)
        vh = AF(vh.c, vh.a, vh.r + EPS_H_FULL)
        vgp = AF(vgp.c, vgp.a, vgp.r + EPS_G_FULL*_derivative_tail_factor)
        vhp = AF(vhp.c, vhp.a, vhp.r + EPS_H_FULL*_derivative_tail_factor)"""
if source.count(old_horner_block) != 1:
    raise RuntimeError("frozen kernel Horner block no longer matches")
source = source.replace(old_horner_block, new_horner_block)

old_result_tail = '"tail_symbol_injected": INJECT_TAIL,'
new_result_tail = '''"tail_symbol_injected": INJECT_TAIL,
        "CL34_full_G_h_errors_injected": True,
        "EPS_G_FULL": ub(EPS_G_FULL),
        "EPS_H_FULL": ub(EPS_H_FULL),'''
if source.count(old_result_tail) != 1:
    raise RuntimeError("frozen kernel result block no longer matches")
source = source.replace(old_result_tail, new_result_tail)

# Executing with this launcher's __file__ deliberately redirects every log
# and JSON result into the point2 directory instead of modifying w36.
exec(compile(source, str(SOURCE), "exec"), globals(), globals())
