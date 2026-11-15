# -*- coding: utf-8 -*-
"""radius_K284_certificate.py -- directed-rounding combination of the K=284
Duhamel and gap budgets, retargeted to the package's STRICT level-tail
certificate.

BRIEF 3.3(b): the frozen certificate listed its log sources by bare filename,
and the names 'duhamel_ds.log' / 'compute_ld.log' are AMBIGUOUS -- each exists
twice in the archive, once in w36/audit_codex/ (coarse M3=123479, FAIL) and once
in w36/duhamel_ds/ + w36/ld_ds/ (strict, PASS). This version records FULL paths
and marks the audit_codex twins duhamel_audit.py / ld_audit.py as SUPERSEDED.
"""
import json
import sys
from pathlib import Path
from flint import arb, ctx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import _log  # noqa: E402

ctx.prec = 512
HERE = Path(__file__).resolve().parent

_log.log("CERT radius_K284 START")
lt = json.loads((HERE / "level_tail_certificate_strict.json").read_text(encoding="utf-8"))


def umid(s):
    """midpoint of an Arb ball string (for the decimal ceilings below)."""
    s = str(s).strip().lstrip("[").strip()
    return s.split("+/-")[0].strip()


# Decimal ceilings of the strict level-tail outputs.
P_EXIT = arb(umid(lt["duhamel_all_levels"]["P_all_levels_upper"]))
D_EXIT = arb(umid(lt["DE_geometric_matrix"]["D_star_upper"]))
P_PERP = arb("2.808542")
R_S = P_EXIT + P_PERP * D_EXIT
TUBE_RADIUS = arb("5.44e-7")
HEADROOM = TUBE_RADIUS - R_S

result = {
    "precision_bits": 512,
    "K": "284",
    "P_exit_ceiling": umid(lt["duhamel_all_levels"]["P_all_levels_upper"]),
    "D_exit_ceiling": umid(lt["DE_geometric_matrix"]["D_star_upper"]),
    "P_perp_upper": "2.808542",
    "r_s_upper": str(R_S.upper()),
    "tube_radius": "5.44e-7",
    "headroom_lower": str(HEADROOM.lower()),
    "pass": bool(R_S.upper() <= TUBE_RADIUS.lower()),
    "note": ("r_s here is the TWO-TERM radius P_exit + P_perp*D_exit. The "
             "WORKING tail quantity is the three-term P_tail(m0) (adds the "
             "l-component drift ||h||_1*e_star/(1-1/delta)); see "
             "level_tail_certificate_strict.json tail_three_term."),
    "sources": [
        "DATA/inputs/w36/duhamel_ds/duhamel_ds.log   (strict PASS; M3=1834 via level_tail)",
        "DATA/inputs/w36/ld_ds/compute_ld.log        (strict PASS; conservative M3=123479 robustness)",
        "CERT/level_tail_certificate_strict.json      (P_all, D_star, e_star -- strict norms)",
        "DATA/inputs/w36/audit_codex/k_global_certificate.json  (K=284)",
    ],
    "superseded": {
        "w36/audit_codex/duhamel_ds.log": (
            "SUPERSEDED. This is the COARSE M3=123479 audit (duhamel_audit.py:56), "
            "giving P_star_refined=6.69e-7 > 3e-7 (FAIL). It is kept for the M3-resolution "
            "narrative (Amax provenance) but is NOT a tail bound. The strict tail is "
            "level_tail_certificate (M3=1834, applicable)."),
        "w36/audit_codex/compute_ld.log": (
            "SUPERSEDED as a D_star source for the headline radius. compute_ld.log reports "
            "the CONSERVATIVE D_cp*=6.252e-8 (M3=123479); the value actually used "
            "(D_EXIT=5.17e-8) is the TIGHT one from level_tail (M3=1834). The strict "
            "w36/ld_ds/compute_ld.log is the kept source; the audit_codex twin is the "
            "namesake that once caused a provenance confusion."),
        "duhamel_audit.py": "SUPERSEDED by level_tail_certificate.py (closed form, Lemma W).",
        "ld_audit.py": "SUPERSEDED by level_tail_certificate.py exit_de (closed form).",
    },
}
out = HERE / "radius_K284_certificate.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
_log.log("CERT radius_K284 DONE: r_s<=%s pass=%s ; wrote %s"
         % (str(R_S.upper())[:24], result["pass"], out.name))
print(json.dumps(result, ensure_ascii=False, indent=2))
if not result["pass"]:
    raise SystemExit(1)
