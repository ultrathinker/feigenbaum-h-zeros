# -*- coding: utf-8 -*-
"""TIGHT launcher for the w36 tube kernel -- COPY of
`path_to_8/point10_layer1_census_B/census_B_pilot.py` with ONE extra patch:
the tube l1 budget R_S is overridden from the conservative `tube_radius`
5.44e-7 to the ACTUAL certified exit radius `r_s_upper` 3.566e-7 from
`w36/audit_codex/radius_K284_certificate.json` (item C of BRIEF_C_D.md).

Policy (per BRIEF_C_D.md §C and project rules):
  - The frozen kernel `w36/audit_codex/cert_slice_param_audit.py` is NEVER
    copied or edited on disk; this script reads its source by absolute path,
    checks sha256 on entry (hard refusal on mismatch), and applies the SAME
    point string-replacements the validated pilots already use, PLUS the one
    extra R_S replacement. Reusing byte-identical patches minimizes the chance
    of a new defect.
  - All outputs (cert_slice_*.json/.log) land next to THIS script, i.e. inside
    cert_D/tight_arcs/, never inside the archive.

This launcher is structurally identical to census_B_pilot.py; the only delta is
patch step #0 (R_S override). Every other patch (radius, geometry, CL-34
injection, H7 fields) is byte-for-byte the same, so a tube run here with R_S
patched OUT must reproduce census_B's archive JSONs bit-for-bit -- the
sanity cross-check.
"""
from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(r"D:/Исследования/И-1 — Нули функции H/Feigenbaum-archive")
SOURCE = ROOT / "w36" / "audit_codex" / "cert_slice_param_audit.py"

EXPECTED_SHA256 = "950ba8a078ca6ecac1b5aab242d4347bcd6d0784e1c48b2c498344055f4c4694"
import hashlib
_actual_sha256 = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
if _actual_sha256 != EXPECTED_SHA256:
    raise RuntimeError(
        f"frozen kernel sha256 mismatch: expected {EXPECTED_SHA256}, got {_actual_sha256}. "
        "Refusing to run against a modified 'frozen' kernel."
    )

source = SOURCE.read_text(encoding="utf-8")

# 0. *** ITEM C PATCH *** -- tighten the tube l1 budget from conservative
#    tube_radius (5.44e-7) to the actual certified exit r_s (3.566e-7).
#    Source of truth: w36/audit_codex/radius_K284_certificate.json
#      r_s_upper = 3.5659822966266...e-7  (line "r_s_upper")
#      tube_radius = 5.44e-7              (line "tube_radius") -- what the
#    frozen kernel bakes in at its line 61. We replace ONLY the literal value.
old_rs = 'R_S = flint.arb("5.44e-7")  # trubka l1 budget, w36_final_assembly section 4 item 5'
new_rs = ('R_S = flint.arb("3.566e-7")  # TIGHT (item C): actual r_s_upper from radius_K284_certificate.json, replaces conservative tube_radius 5.44e-7')
assert source.count(old_rs) == 1, "frozen kernel R_S line changed"
source = source.replace(old_rs, new_rs)

# 1. Radius + fat
old = "FAT = 0.01\nR_CONTOUR = 0.1"
new = ("FAT = float(os.environ.get('PILOT_FAT', '0.0'))\n"
       "R_CONTOUR = float(os.environ.get('PILOT_RADIUS', '7.0'))")
assert source.count(old) == 1, "frozen kernel constants changed"
source = source.replace(old, new)

# 2. Geometry: local circle centre
old_geo = '''key = {"A": "A", "B": "B", "C": "C", "D": "D", "N": "new"}[TOOTH]
r0, arg0 = xc.TEETH_NEW[key]
u0c = r0 * complex(math.cos(arg0), math.sin(arg0))'''
new_geo = '''if TOOTH != "P7":
    raise RuntimeError(f"pilot launcher expects TOOTH=P7, got {TOOTH!r}")
u0c = complex(
    float(os.environ.get("PILOT_CENTER_RE", "0.0")),
    float(os.environ.get("PILOT_CENTER_IM", "0.0")),
)'''
assert source.count(old_geo) == 1, "frozen kernel geometry changed"
source = source.replace(old_geo, new_geo)

# 3. CL-34 error injection (same as fix1_pilot.py / sector_pilot.py)
old_tail = """ZERO_ACB = flint.acb(0)
ONE_ACB = flint.acb(1)"""
new_tail = """ZERO_ACB = flint.acb(0)
ONE_ACB = flint.acb(1)
_CL34 = json.load((W36 / "tail_codex" / "cl34_certificate.json").open())
EPS_G_FULL = flint.arb(_CL34["G"]["distance_and_Taylor_tail_upper"]).upper()
EPS_H_FULL = flint.arb(_CL34["V_h_delta"]["h_error_stored_center_upper"]).upper()"""
assert source.count(old_tail) == 1, "frozen kernel tail anchor changed"
source = source.replace(old_tail, new_tail)

old_horner = """        vg = af_horner(G1, z)
        vh = af_horner(H1, z)
        vgp = af_horner(DG1, z)
        vhp = af_horner(DH1, z)"""
new_horner = """        vg = af_horner(G1, z)
        vh = af_horner(H1, z)
        vgp = af_horner(DG1, z)
        vhp = af_horner(DH1, z)
        _derivative_tail_factor = 1 / ((1-rz)*(1-rz))
        vg = AF(vg.c, vg.a, vg.r + EPS_G_FULL)
        vh = AF(vh.c, vh.a, vh.r + EPS_H_FULL)
        vgp = AF(vgp.c, vgp.a, vgp.r + EPS_G_FULL*_derivative_tail_factor)
        vhp = AF(vhp.c, vhp.a, vhp.r + EPS_H_FULL*_derivative_tail_factor)"""
assert source.count(old_horner) == 1, "frozen kernel Horner block changed"
source = source.replace(old_horner, new_horner)

# 4. Add H7 enclosure to compute_arc's return dict
old_ret = '        "x128_lower": den_lo,'
new_ret = ('        "x128_lower": den_lo,\n'
           '        "H7_abs_lower_cert": lb(af_abs_lower(H)),\n'
           '        "H7_abs_upper_cert": ub(af_abs_upper(H)),')
assert source.count(old_ret) == 1, "frozen kernel return block changed"
source = source.replace(old_ret, new_ret)

# 5. Add H7 fields to the outer result dict
old_res = '"tail_symbol_injected": INJECT_TAIL,'
new_res = ('"tail_symbol_injected": INJECT_TAIL,\n'
           '        "H7_abs_lower": lb(out["H7_abs_lower_cert"]),\n'
           '        "CL34_full_G_h_errors_injected": True,\n'
           '        "EPS_G_FULL": ub(EPS_G_FULL),\n'
           '        "EPS_H_FULL": ub(EPS_H_FULL),')
assert source.count(old_res) == 1, "frozen kernel result block changed"
source = source.replace(old_res, new_res)

exec(compile(source, str(SOURCE), "exec"), globals(), globals())
