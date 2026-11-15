# Appendix B. Constants

All numerical quantities that enter the conclusions of the work, with an indication of their status and the place where the quantity is used. Statuses:

- **rigorous** — certified interval bound, obtained in ball arithmetic at 512 bits with directed rounding;
- **computed** — the quantity has been computed with high precision, but without an interval certificate;
- **known** — a classical constant, accepted as input;
- **calibration** — a quantity defined by a normalization convention, not proved.

## 1. Universal constants and data

| constant | value | status | where it enters |
|---|---|---|---|
| δ (first Feigenbaum constant) | 4.669201609102990671853203820466… | known | everywhere |
| α (second Feigenbaum constant) | −2.5029078750958928… | known | §1, Appendix D |
| α² | 6.264547831217037425109907407592… | known | Proposition 5 |
| AU₀ | 0.41403799908627305889537448439556 | calibration, §2.4 | perturbation scale s_m(u) |
| c_F (Feigenbaum point) | −1.4011551890920506005238268502643 | known | §7 |
| G(1) = −1/α | −0.39953528052313448985758046863369 | analytical consequence | Appendix D |
| ‖G − g₀‖ | ≤ 4.7×10⁻⁶¹ | rigorous | bridge §4 |
| ‖h − h₀‖ | ≤ 1.7×10⁻²⁹ | rigorous | bridge §4 |
| error radius of data g | 10⁻²⁰ | rigorous | §2.1 |
| error radius of data h | 10⁻²⁷ | rigorous | §2.1 |

The multi-digit literals δ, α originate from high-precision computations of the Feigenbaum constants (Briggs 1991).

## 2. Operator-estimate constants (section 5)

| constant | value | status | comment |
|---|---|---|---|
| ‖DT(G)‖ | ≤ 22.191604188675928 | rigorous | second implementation gives 22.19160418867592444…; agreement in 16 digits, the larger is used |
| ‖DT(G)²‖ | ≤ 193.63443782547… | rigorous | two implementations, agreement in 12 digits |
| K — norm of the second derivative of the operator on its own ball | ≤ 284 (rigorous estimate 283.2754150512159) | rigorous | the literal 284 is more conservative than the rigorous estimate by 0.26 % |
| M₃ — norm of the third derivative on its own ball | ≤ 1834 (rigorous estimate 1833.66714697445380) | rigorous | |
| q₂ — quadratic coefficient | ≤ 111.550905120798913 (automatic differentiation) | rigorous | the second, independent method — a contour integral — gives ≤ 111.5509172; agreement in 7 significant digits, leading sums agree in 16 |
| ‖ℓ‖_∞ — norm of the left eigenfunctional | ≤ 1.10485425031978 | rigorous | ℓ∘DT(G) = δ·ℓ, normalization ℓ(h) = 1 |
| ‖h‖ — norm of the eigenfunction | ≤ 6.33119360069264 | rigorous | |
| ‖P_perp‖₁ — norm of the spectral projector | ≤ 2.808542 | rigorous | P_perp = I − h·ℓ |
| C_s — spectral-kernel constant at μ = 0.35 | ≤ 5.495834836322508 (literal 5.4959) | rigorous | ‖DT(G)^j P_perp‖₁ ≤ C_s·μ^j |
| μ — contraction constant on the transverse subspace | 0.35 | rigorous | |
| ratio = μ/δ² | 0.016054 | rigorous | layerwise-majorization denominator |
| spectral convergence signature | 0.4274 < 1 | rigorous | |
| D_star — transverse part of the contribution | ≤ 5.1723×10⁻⁸ (sup at k = 8) | rigorous | |
| e_star — ℓ-component of the contribution | ≤ 1.2453×10⁻⁸ (sup at k = 8) | rigorous | drift along the unstable direction |
| tail beyond the leading block (100 modes) | 2.77×10⁻¹² | rigorous | taken into account analytically, not discarded |
| error of the inexact normalization f_s(0) | ≈ 1.6×10⁻³³ | rigorous | does not grow with the level; quantities entering — `\|h(0)\| ≤ 1.63×10⁻²⁹` (x = 0, i.e. t = −1 in the series `w33_gh_hiprec.json`; `check_gh_at_x0.py`) and `\|s_{m₀}\| ≤ 9.9×10⁻⁵` (`IDENTITY_B.md` §B.4, `cl34_certificate.json`) |

The derivation of D_star/e_star (the variational equation for the differences `slice_{ℓ+1} − slice_ℓ`, not for the slices themselves) is written out in `09-CODE/section5_base_certificates/h1_package_lemma_A/LEMMA_H1.md`, §1, "Step 4 in the nonlinear case — variational equation" (lines 127–146); this is the file that requires line-by-line verification for this step — the mathematics is not transferred to the main text.

## 3. Lemma on the pair invariant

**Lemma W (pair invariant).** The transverse deviation `w` at the boundary of a pair of renormalization levels satisfies `w ≤ C₀·s²` with `C₀ = 1000`, at the intermediate step `w ≤ C₁·s²` with `C₁ = 1280`. From this (Duhamel sum) `Q_j ≤ QCOEF·s_j²` uniformly over the levels; the layerwise estimate is written in closed form. The proof is in `09-CODE/section5_base_certificates/h1_package_lemma_A/LEMMA_H1.md` (step 1); the certified coefficients are in `level_tail_certificate.py:26-34`.

| inequality | value | bound | margin |
|---|---:|---:|---:|
| first single | 261.0804 | 1000 | 73.89 % |
| **mean** | **1279.3512** | **1280** | **0.0507 %** |
| pair | 936.8487 | 1000 | 6.32 % |

All three are rigorous, from the rigorous certificates `09-CODE/section5_base_certificates/h1_package_cert_strict/CERT/level_tail_certificate_strict.py` (and the same-named `.json`) (rigorous ‖DT(G)‖₁ = 22.191604188675928, ‖DT(G)²‖₁ = 193.634437825475… from `ndt_rigorous.json`; independent duplicate — `09-CODE/archive_inputs/w36/proj_codex/rigorous_block.json`). The frozen `09-CODE/archive_inputs/w36/audit_codex/level_tail_certificate.py` uses the literals 22.19/193.63 (rounded down, formally not upper bounds) and gives 1279.2777/936.8200; the provenance of the remaining constants of Lemma W is `CERT/_constants.py`. The mean inequality is the tightest place of the work; on why the tightness is misleading, see §5.4 of the main text.

## 4. Final tail estimate

| quantity | value | status |
|---|---|---|
| P_all — main tail term | ≤ 2.1135×10⁻⁷ | rigorous |
| ‖P_perp‖·D_star — second term | ≤ 1.4527×10⁻⁷ | rigorous |
| ‖h‖·e_star/(1 − 1/δ) — third term | ≤ 1.0033×10⁻⁷ | rigorous |
| two-term form (without the third term) | ≤ 3.566085×10⁻⁷ | rigorous; **insufficient**, see §5.3(iii) |
| **full tail estimate P_tail(m₀)** | **≤ 4.569368×10⁻⁷ + 1.6×10⁻¹⁴** (in the abstract and §5.3(iii) rounded up to 4.5695×10⁻⁷; 1.6×10⁻¹⁴ is the formal projector-replacement correction, §8 item 11) | rigorous |
| tube budget B | 5.44×10⁻⁷ | **imposed, not derived**, see §5.3(iii) |
| margin to the budget | 0.87×10⁻⁷ | rigorous |
| share of q₂ in P_all | ≈ 69 % | computed; see §8 item 7 of the main text |

The printed terms are rounded up to the fourth place, so their sum (4.5695×10⁻⁷) slightly exceeds the certified bound 4.569368×10⁻⁷. Every number shown remains an upper bound.

## 5. Breaking points (certified forks)

A breaking point is the value of a constant at which the **final** derivation stops passing. All forks are obtained by a separate scan with its own verifier.

| constant | fork against the final derivation | margin | fork against the intermediate subgoal |
|---|---|---:|---|
| Lemma threshold C1 (nominal 1280) | [3018, 3019] | **2.36×** | [3049, 3050] |
| quadratic coefficient q₂ (nominal 111.55) | [136.4258, 136.4844] | **1.22×** | ≈ 179 |

The right column is given as a **warning**: the numbers 3050 and 179 are arithmetically correct, but measure the breaking of the intermediate subgoal P_all < 3×10⁻⁷, not of the final derivation. In addition, the estimate "≈ 179" takes into account only one of the two paths by which q₂ enters the derivation (only the main tail term, not the majorant of the nonlinear source, and through it — the second and third terms). Accounting for one path gives a breaking point of 178.29 instead of 136.43. Analysis of the error class — Appendix E, §3.

## 6. Constants of sections 6 and 7

| constant | value | status |
|---|---|---|
| c₂ — quadratic-response coefficient (drift law) | 0.79028031944… | numerical constant (no separate interval certificate; provenance — §7 below) |
| conditional interval of the right zero | [5.9409360413, 5.9409363308] | conditional (geometric-rate hypothesis) |
| unconditional localization of the right zero | disk of radius 1/6 around 5.94 | rigorous |
| winding on the circle \|u\| = 7 | 2, margin 1.55 | rigorous |
| separation margins of the two real zeros | 654 (left, u ≈ −1) and 23.7 (right, u ≈ 5.94) | rigorous |
| \|ε_m\| on the five drift transitions | ≤ 2.9×10⁻⁵ | rigorous |
| **L** = lim (c_{k+1} − c_F)·δ^k | 0.4288374984294040681397073391164 | computed |
| **A** = −1/L — calibration of the bridge to the quadratic family | −2.331885629550704132301427374005… | computed; reproduced by an independent implementation to the 30th digit |
| R_accept(u) — frozen acceptance radius | 0.01 | parameter, fixed before the computation |
| experiment level m | 10 | parameter |
| period | 2^(m+1) = 2048 | parameter |
| distance of the nearest singularity of H from zero | 7.58 / 7.566 (two estimates of one quantity) | computed |

## 7. Notes on the statuses

**Two constants for which no rigorous bound existed.** The norms ‖DT(G)‖ and ‖DT(G)²‖ were originally taken from a midpoint estimate, which is not a rigorous bound and did not declare itself one. The used literal 22.19 turned out to be **smaller** than the true 22.1916 — i.e. it was formally not an upper bound. Both quantities have been recomputed rigorously by two independent implementations; all inequalities have been rechecked and pass. Crucially, the main tail term P_all **does not contain** these norms and has not changed from the replacement.

**Two literals are more conservative than the rigorous estimates.** K = 284 against the rigorous 283.2754150512159 and M₃ = 1834 against 1833.66714697445380. The literal is in both cases larger than the rigorous estimate, i.e. it is used in the right direction.

**c₂ and the status of Theorem 4.** The coefficient c₂ enters the very statement of the drift law: the quantity ε_m is defined as the deviation from a formula containing c₂, so the bound |ε_m| ≤ 2.9×10⁻⁵ makes sense only with a definite c₂. An interval envelope for c₂ exists in the materials, but it has been obtained as a cross-check inside a set marked as a rejected branch, and not by a separate certificate. Therefore the status of Theorem 4 should be read correctly as: **the signs of the increments on five transitions and the bound |ε_m| ≤ 2.9×10⁻⁵ at c₂ = 0.79028031944… are certified; the coefficient c₂ has the status of a numerical constant (no separate interval certificate; provenance — this paragraph)**, whereas c₂ itself has no separate certificate. This discrepancy between the status of the theorem and the status of the constant entering it is marked here explicitly and is to be closed by a separate certificate of c₂.

**q₂ — the dominant constant.** It gives about 69 % of the final quantity. It originates from a file marked as a dead branch; the mark referred to the failed strategy, not to the numbers. The quantity has been re-certified anew and confirmed by a second, methodologically independent method. Details — section 8, item 7 of the main text.
