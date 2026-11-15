# Appendix F. Protocol of the numerical experiment (to section 7)

This appendix makes section 7 verifiable by numbers. It contains all per-disk results of the frozen run, the design of the controls, the derivation of the calibration constant, and the analysis of two separate cases (Z72 and the early runs).

> **Status.** Everything in this appendix is numerical evidence, not a rigorous result. The computations are carried out in directed high-precision arithmetic (150 decimal digits), but there are no interval certificates here. The values of δ, c_F, α in this header are truncations of the certified literals from Appendix B; the discrepancy between these entries and B.§1 is rounding to different required precision of one and the same certified value, not independently computed numbers.

## 1. Design of the experiment

**What was fixed before the computation.** All parameters listed below are written in the header of the script and were not changed after the first per-point result was obtained:

| parameter | value |
|---|---|
| precision | 150 decimal digits |
| level m | 10 |
| verified period | 2^(m+1) = 2048 |
| δ | 4.669201609102990671853203820466201617258185577475768632745651343004133555868548426390712381266351242 |
| c_F | −1.4011551890920506005238268502643472843821101975214 |
| acceptance radius in the universal coordinate R_accept(u) | 0.01 (dimensionless quantity in the u-coordinate) |
| seed of the control-generator | 20260812 |

**Acceptance rule (three conditions, all mandatory).** A root found by Newton is counted as a match for a catalogue zero if and only if:

1. Newton has converged (not "the last iteration issued as the result");
2. the root has **exact** period 2048 — that is, x_{2^j}(c) ≠ 0 for j = 0, …, 10 (all proper divisors of the period 2¹¹);
3. the root lies closer to the predicted point c_pred than R_accept(c, m) = R_accept(u)/(|A|·δ^m) = 8.70695878622808×10⁻¹⁰.

The distance d_u in the universal coordinate is reported **only** for accepted points; a rejected attempt does not give a "silent zero", but is recorded as a refusal with a reason.

**What was recorded.** Every Newton attempt — successful and unsuccessful — enters the machine log with the starting point, the number of iterations, the final |x|, the status (converged / escaped), the result of the exact-period check and, on refusal, the reason for the refusal. The best converged but rejected candidate is saved separately.

**Run time:** 2176 seconds.

## 2. Calibration: where A comes from

The single free constant of the bridge between the universal coordinate u and the parameter c of the quadratic family is fixed by the real cascade of superstable parameters — before any complex zero is considered.

The cascade c_k (superstable parameter of period 2^k) and the sequence L_k = (c_{k+1} − c_F)·δ^k:

| k | c_{k+1} (period 2^(k+1)) | L_k = (c_{k+1} − c_F)·δ^k |
|---:|---|---|
| 0 | −1.0 | 0.4011551890920506005238 |
| 1 | −1.310702641336832883563 | 0.4223411815261276708402 |
| 2 | −1.381547484432061469540 | 0.4274762685731413531974 |
| 3 | −1.396945359704560641672 | 0.4285409963629786779771 |
| 4 | −1.400253081214782797325 | 0.4287745316223216120835 |
| 5 | −1.400961962944841040296 | 0.4288239442134706481127 |
| 6 | −1.401113804939776123900 | 0.4288346038441126135997 |
| 7 | −1.401146325826946178647 | 0.4288368774652988334034 |
| 8 | −1.401153290849923881474 | 0.4288373655651804604909 |
| 9 | −1.401154782546617841218 | 0.4288374699582101531378 |
| 10 | −1.401155102022463975894 | 0.4288374923336915771431 |
| 11 | −1.401155170444411263765 | 0.4288374971236478950492 |
| 12 | −1.401155185098297290530 | 0.4288374981497802466047 |
| 13 | −1.401155188236710941543 | 0.4288374983695129651167 |
| 14 | −1.401155188908863038563 | 0.4288374984165772279137 |
| 15 | −1.401155189052817434492 | 0.4288374984266569517588 |

The sequence L_k converges geometrically; extrapolation gives

    L = 0.4288374984294040681397073391164…
    A = −1/L = −2.331885629550704132301427374005…

**The form of the link is derived, not fitted.** In u = A·(c − c_F)·δ^m there is no freedom beyond a single constant A: a shift is forbidden, since u = 0 must correspond to c = c_F; the power is pure δ^m without sign alternation, since c_k − c_F preserves its sign along the main cascade, and the factor (−1)^m would generate an even-odd alternation purely arithmetically.

**Two independent checks of the calibration.**

- *Self-consistency:* with this A, the value u(c₁₁), computed at level m = 10, equals −1 with accuracy 1.4214504×10⁻⁸.
- *External:* a separate "clean" implementation, which built its own Newton cascade and its own extrapolation of c_F and read nothing from the main pipeline, gave A = −2.331885629550704132301427374006… — agreement to the 30th digit.

Once A is fixed, the positions of all 23 complex zeros are **pure predictions**: no complex zero participated in the calibration.

## 3. Results by catalogue

All 23 zeros, in order of identifier. The column "Newton attempts" shows how many starting points had to be tried: a value of 1 means a hit on the first attempt.

| zero | u catalogue (Re) | u catalogue (Im) | Newton attempts | exact period 2048 | d_u, ×10⁻⁵ | accepted |
|---|---|---|---:|---|---:|---|
| Z01 | 1.55349371071307 | 8.1238031598708 | 1 | yes | 2.603 | yes |
| Z02 | 5.817868 | 4.476081 | 1 | yes | 2.033 | yes |
| Z05 | 5.011415 | 5.626752 | 1 | yes | 2.027 | yes |
| Z17 | 6.681454 | 6.210555 | 1 | yes | 3.135 | yes |
| Z19 | 4.008907 | 6.703721 | 1 | yes | 2.262 | yes |
| Z38 | 4.63702563107768 | 6.75922558655159 | 1 | yes | 2.588 | yes |
| Z39 | 6.24846326820913 | 5.67889810713901 | 1 | yes | 2.710 | yes |
| Z40 | 8.36818444963026 | 3.42161554921713 | 1 | yes | 3.124 | yes |
| Z57 | 8.589396 | 3.974588 | 1 | yes | 3.358 | yes |
| Z59 | 7.125929 | 4.064322 | 1 | yes | 2.456 | yes |
| Z60 | 8.26332724866471 | 4.01596385048377 | 1 | yes | 3.247 | yes |
| Z63 | 6.83110274129083 | 5.23116997709336 | 1 | yes | 2.806 | yes |
| Z64 | 7.218228 | 5.788641 | 1 | yes | 3.233 | yes |
| Z65 | 7.36053136328949 | 5.76158912153642 | 1 | yes | 3.329 | yes |
| Z66 | 7.24399319091292 | 6.18809344211899 | 1 | yes | 3.471 | yes |
| Z67 | 6.61525908186462 | 6.33935578550363 | 1 | yes | 3.215 | yes |
| Z68 | 7.055487 | 6.338351 | 1 | yes | 3.455 | yes |
| Z69 | 7.26684 | 6.413616 | 1 | yes | 3.602 | yes |
| Z70 | 7.33895547113294 | 6.5054396352541 | 1 | yes | 3.687 | yes |
| Z71 | 4.50618857227679 | 7.07800180592392 | 1 | yes | 2.641 | yes |
| **Z72** | 4.758336330290482 | 7.1277051021354385 | **49** | **no** | — | **no** |
| Z73 | 4.020255 | 8.037592 | 1 | yes | 3.180 | yes |
| Z74 | 4.72725441425135 | 8.68634320415312 | 1 | yes | 3.718 | yes |

**Summary:** 22 accepted, 1 rejected. For all 22 accepted — **one** Newton attempt: the prediction fell into the basin of attraction of the desired root immediately. Range of d_u: from 2.027×10⁻⁵ to 3.718×10⁻⁵, median 3.158×10⁻⁵.

Z72 is the single refusal; on it 49 starting points were spent, and none gave a root satisfying the acceptance rule. Analysis — §5.

## 4. Specificity: how this result differs from a random hit

It is not enough that "a root was found nearby": if the superstable roots densely cover the neighbourhood, then a root will be found near any point. Therefore around each zero the local density has been measured separately: on a grid of 144 nodes Newton was launched, all distinct roots of exact period were collected, and the **median** distance from the predicted point to a randomly hit root was computed.

Specificity = (median of random hit) / (distance to the found partner). It is computed **for each zero separately**.

| zero | grid nodes | converged | distinct roots | d_u, ×10⁻⁵ | median random hit | specificity |
|---|---:|---:|---:|---:|---:|---:|
| Z01 | 144 | 144 | 1 | 2.603 | 0.1725 | 6627 |
| Z02 | 144 | 144 | 1 | 2.033 | 0.1725 | **8486** |
| Z05 | 144 | 144 | 9 | 2.027 | 0.1537 | 7586 |
| Z17 | 144 | 143 | 12 | 3.135 | 0.1060 | 3381 |
| Z19 | 144 | 144 | 1 | 2.262 | 0.1725 | 7624 |
| Z38 | 144 | 143 | 19 | 2.588 | 0.1141 | 4408 |
| Z39 | 144 | 144 | 2 | 2.710 | 0.1725 | 6364 |
| Z40 | 144 | 144 | 1 | 3.124 | 0.1725 | 5522 |
| Z57 | 144 | 138 | 25 | 3.358 | 0.0954 | 2841 |
| Z59 | 144 | 144 | 12 | 2.456 | 0.1475 | 6005 |
| Z60 | 144 | 139 | 20 | 3.247 | 0.1202 | 3702 |
| Z63 | 144 | 144 | 1 | 2.806 | 0.1725 | 6147 |
| Z64 | 144 | 143 | 12 | 3.233 | 0.1060 | 3278 |
| Z65 | 144 | 127 | 20 | 3.329 | 0.0533 | 1600 |
| Z66 | 144 | 131 | 29 | 3.471 | 0.0618 | 1782 |
| Z67 | 144 | 124 | 19 | 3.215 | 0.0503 | 1566 |
| Z68 | 144 | 130 | 31 | 3.455 | 0.0631 | 1825 |
| Z69 | 144 | 117 | 21 | 3.602 | 0.0498 | 1384 |
| Z70 | 144 | 121 | 42 | 3.687 | 0.0364 | **986** |
| Z71 | 144 | 142 | 25 | 2.641 | 0.0955 | 3618 |
| **Z72** | 144 | 124 | **31** | 5998 (= 0.060) | 0.0689 | **1.15** |
| Z73 | 144 | 144 | 14 | 3.180 | 0.1285 | 4042 |
| Z74 | 144 | 142 | 10 | 3.718 | 0.1385 | 3725 |

**Summary for the 22 accepted:** specificity from 986 (Z70) to 8486 (Z02), median **3713**.

Note two circumstances important for reading this table.

*First.* The extreme values of specificity are **not** obtained by dividing the extremes of two distributions: the distances d_u themselves lie in the narrow range 2.03–3.72×10⁻⁵, and the medians of random hits in the wide range 0.036–0.173, but the minimum of one and the maximum of the other are attained on different disks. This is precisely why the ratio is computed per disk, not by aggregates.

*Second.* The specificity is directly related to the local density: on disks where the grid found 1–2 distinct roots (Z01, Z02, Z19, Z40, Z63), the median random hit is large and the specificity is around 6000–8500; on disks with 20–42 roots (Z70, Z69, Z67) the neighbourhood is denser, and the specificity drops to 1000–1600. This is expected behaviour, not spread.

*Z72* stands apart: specificity 1.15, i.e. the found root is **no better than random**. This is a direct consequence of the fact that the comparison was made with the wrong point (§5), not evidence against the hypothesis. It is not included in the range and the median.

**Second, control metric: `stage7_pool_specificity`.** The frozen `09-CODE/section7_mandelbrot/frozen_experiment.py` computes after stages 5–6 (STAGE 7, a "cheap" check on all accepted points) another ratio — not to a random hit on the local grid, but to **the other found partners of the same run**: for each accepted point the median distance to the remaining 21 accepted points of the pool is taken (22 catalogue + 0 controls), divided by d_u. The result is in `results.json` (`stage7_pool_specificity`, `verdict.median_pool_specificity_catalog`); the median over the 22 catalogue ones equals **82338.96**, almost two orders of magnitude larger than the median of 3713 of the grid metric above — because it measures the sparsity of the pool of found points in the scale of the c-plane, not the local density of roots around each individual point. This metric has been computed as a control one, and is not applied in the main specificity metric.

## 5. A separate case: Z72

Z72 is the only one of the 23 disks whose center is deliberately shifted from the zero itself by about 0.06, so that the certificate contour bypasses the boundary of the convergence region of the series (Appendix A, §3.1). The acceptance rule was frozen before the computation and operates on **disk centers**. Therefore for Z72 the point supplied to the comparison was at a distance of 0.06 from the true zero — a quantity two thousand times larger than the measured effect.

The observed picture:

| quantity | value |
|---|---|
| distance to the nearest partner, d_u | 0.05998 |
| ratio of the residual to the drift prediction | 2069 |
| phase discrepancy | 123.7° |
| ratio of the contour shift itself to the drift prediction | 2069.68 |
| discrepancy between these two ratios | 0.033 % |
| difference "residual minus shift" | −2.0×10⁻⁵ |
| for comparison: typical true drift | 2.9×10⁻⁵ |

The arithmetic converges exactly: the observed is the **sum** of the deliberate contour shift and the true drift, where the first term is about two thousand times larger than the second and completely masks it.

**Check with the actual position of the zero.** The numerical (not certified) estimate of the position of the zero Z72 itself is u₀ = 4.79165 + 7.177607i. The superstable partner, found by search near the disk center, lies at the position u_partner:

    u_partner = 4.791660937911268425586256 + 7.177581007211361312933728 i

The distance between them: **2.82×10⁻⁵** — that is, exactly of the same order as for the other 22 zeros (2.03–3.72×10⁻⁵). The subsequent analysis gives for this pair a ratio to the drift prediction of 0.959 and a phase discrepancy of 0.27°, which also places Z72 in the common row.

**Three caveats, mandatory for an honest reading of this item:**

1. The position u₀ = 4.79165 + 7.177607i is a **numerical estimate in double precision, not a certified quantity**. Strictly certified, however, is something larger than the parent disk of radius 0.1: by a separate interval certificate it is proved that exactly one zero of the limit H lies in a disk of radius 0.01 centered at the position of the partner (winding of H₉ = 1 on 128 arcs, transfer to the limit with margin 1.06; in combination with the parent certificate this is exactly the catalogue zero). The "zero ↔ partner" coincidence is thereby rigorously established with accuracy 0.01 (conditional closure, see §8, item 13 of the main text); the accuracy of 2.8×10⁻⁵ is numerical.
2. The ratio 0.959 and the phase 0.27° were obtained in the subsequent analysis, **outside** the frozen run, and do not enter its machine log. The distance of 2.82×10⁻⁵ is checked by direct subtraction of the two numbers given above.
3. The machine results contain the entry "Z72 corrected" with zero residual of the positions. The zero distance in it is **tautological**: as the "corrected" catalogue position the very point to which the search converged was substituted — on a cursory reading the entry looks like a perfect coincidence, which in this part it is not. The substantive content of the entry is different, and it should be named directly: it was performed by the same frozen chain in the same run (as a separate line, excluded from the 22/23 count), and in it the **exact period 2048** of the partner has been confirmed — that very decisive check that sifted out the early erroneous run. The existence of a genuine superstable root of exact period 2048 within 2.8×10⁻⁵ of the numerical position of the zero is a machine-registered fact, and in addition — a theorem: as for the other 22 partners, for this root existence, uniqueness, and exact period in a box of radius 10⁻²⁷ have been certified (§7 of the article, "Rigour of the M-side"; package `09-CODE`). Outside the run only the ratio 0.959 and the phase 0.27° were computed.

**The corrected result is not included in the main 22/23 count.** The acceptance rule was fixed before the computation, and changing it retrospectively for one disk would mean exactly that substitution of the criterion against which this rule was introduced.

## 6. Controls

Twenty control points were generated pseudorandomly in the same annulus as the catalogue, with the only selection condition: the distance to **any** catalogue zero is not less than 0.5 in the universal coordinate. The selection condition and the seed of the generator are fixed before the computation; the generation log preserves also the rejected attempts (points that turned out to be too close to the catalogue).

A control is a point where the prediction of the hypothesis does not work by construction. If the procedure accepts the controls, it means it accepts anything.

| control | attempts | converged to a root of exact period 2048 | accepted |
|---|---:|---:|---|
| CTRL01 | 49 | 49 | no |
| CTRL02 | 49 | 44 | no |
| CTRL03 | 49 | 14 | no |
| CTRL04 | 49 | 49 | no |
| CTRL05 | 49 | 45 | no |
| CTRL06 | 49 | 47 | no |
| CTRL07 | 49 | 48 | no |
| CTRL08 | 49 | 42 | no |
| CTRL09 | 49 | 47 | no |
| CTRL10 | 49 | 17 | no |
| CTRL11 | 49 | 49 | no |
| CTRL12 | 49 | 49 | no |
| CTRL13 | 49 | 40 | no |
| CTRL14 | 49 | 28 | no |
| CTRL15 | 49 | 48 | no |
| CTRL16 | 49 | 38 | no |
| CTRL17 | 49 | 49 | no |
| CTRL18 | 49 | 49 | no |
| CTRL19 | 49 | 46 | no |
| CTRL20 | 49 | 49 | no |
| **total** | **980** | **847** | **0 out of 20** |

Breakdown by status of all 980 attempts: **924 converged** to some root, of which **847** — to a root of **exact** period 2048; 56 escaped.

The full table of all 20 controls is shown; the per-attempt logs of all 980 attempts are in `09-CODE/section7_mandelbrot/results.json`.

This is the main content of the control experiment: roots of exact period 2048 in the neighbourhoods of the control points **do exist, and there are many of them** — in almost 86 % of attempts. The rejection of the controls happens not because there is nothing to find there, but because what is found lies far from the prediction. If the acceptance rule were weak, it would have accepted the controls.

## 7. Vector check against the drift law

The catalogue positions correspond to the finite level 7, and the superstable parameters to the limit. Hence between them there must be a systematic difference, and the drift law (Theorem 4) predicts it — **both in modulus and in direction**. This is the most substantive of the checks: it uses not a single number, but a complex vector.

| zero | \|R\| (actual residual) | \|Δ_pred\| (drift prediction) | ratio | phase discrepancy, ° |
|---|---:|---:|---:|---:|
| Z01 | 2.6027×10⁻⁵ | 2.7004×10⁻⁵ | 0.9638 | −0.030 |
| Z02 | 2.0327×10⁻⁵ | 2.1270×10⁻⁵ | 0.9557 | +0.128 |
| Z05 | 2.0265×10⁻⁵ | 2.2411×10⁻⁵ | 0.9042 | +1.422 |
| Z17 | 3.1355×10⁻⁵ | 3.2847×10⁻⁵ | 0.9546 | −0.786 |
| Z19 | 2.2624×10⁻⁵ | 2.4083×10⁻⁵ | 0.9394 | −1.040 |
| Z38 | 2.5878×10⁻⁵ | 2.6522×10⁻⁵ | 0.9757 | −0.590 |
| Z39 | 2.7104×10⁻⁵ | 2.8142×10⁻⁵ | 0.9631 | +0.217 |
| Z40 | 3.1238×10⁻⁵ | 3.2263×10⁻⁵ | 0.9682 | +0.282 |
| Z57 | 3.3578×10⁻⁵ | 3.5359×10⁻⁵ | 0.9496 | +0.895 |
| Z59 | 2.4561×10⁻⁵ | 2.6565×10⁻⁵ | 0.9246 | +1.074 |
| Z60 | 3.2474×10⁻⁵ | 3.3320×10⁻⁵ | 0.9746 | −0.222 |
| Z63 | 2.8060×10⁻⁵ | 2.9222×10⁻⁵ | 0.9602 | −0.126 |
| Z64 | 3.2331×10⁻⁵ | 3.3794×10⁻⁵ | 0.9567 | −0.318 |
| Z65 | 3.3290×10⁻⁵ | 3.4490×10⁻⁵ | 0.9652 | −0.387 |
| Z66 | 3.4705×10⁻⁵ | 3.5830×10⁻⁵ | 0.9686 | −0.262 |
| Z67 | 3.2148×10⁻⁵ | 3.3138×10⁻⁵ | 0.9701 | +0.093 |
| Z68 | 3.4550×10⁻⁵ | 3.5508×10⁻⁵ | 0.9730 | −0.603 |
| Z69 | 3.6015×10⁻⁵ | 3.7082×10⁻⁵ | 0.9712 | −0.934 |
| Z70 | 3.6874×10⁻⁵ | 3.7966×10⁻⁵ | 0.9712 | −0.292 |
| Z71 | 2.6410×10⁻⁵ | 2.7791×10⁻⁵ | 0.9503 | −0.563 |
| Z73 | 3.1801×10⁻⁵ | 3.1881×10⁻⁵ | 0.9975 | +0.601 |
| Z74 | 3.7179×10⁻⁵ | 3.8605×10⁻⁵ | 0.9631 | −0.004 |

**Median of the ratio by modulus: 0.9635. Median of the phase discrepancy by modulus: 0.35°.**

The phase discrepancy is less than a degree on **19 disks out of 22**; on the remaining three — Z05 (1.422°), Z59 (1.074°) and Z19 (1.040°) — it does not exceed one and a half degrees. This is the strong part of the check. The direction of the residual was not fitted: it is entirely determined by the drift law, derived independently of the experiment.

**Systematic shortfall to 1.** The ratio is systematically below 1: the median 0.9635 against the expected 0.990 with three tail terms. The shortfall is not a property of the drift law: the law itself has been confirmed term by term with accuracy about 10⁻⁶ at exactly three terms. It sits in the bridge between the abstract system H and the real quadratic family: the correspondence formula u = A·(c − c_F)·δ^m is only the **leading order** of universality, and the only available estimate of its accuracy has been withdrawn at |u| around 1, whereas the catalogue lives at |u| from 7 to 10. There the next-order correction gives from 7×10⁻⁷ to 1.2×10⁻⁶, i.e. from 2 to 5 % of the measured effect, systematically and almost in anti-phase.

This is a separate systematic error and should be distinguished from the truncation of the drift tail.

**Note.** The full text of the note — see §7.3 of the main text; briefly: the two-layer structure of drift and the value λ₂ = −0.123652712552687… have been numerically verified on a discretization of the renormalization system with N = 48 ([companion], Appendix G item 21); the certificate is in [companion], it is not entered in the registry of Appendix B of the present work. The purely geometric drift prediction used in this check does not account for the second layer and therefore systematically overestimates the residual drift; this explains the direction of the shortfall (median 0.9635 < 1) and gives a sign-alternating contribution to the phase spread. The quantitative decomposition of the number 0.9635 into the contribution of the two-layer model and the contribution of the above-described correction of the correspondence formula is the subject of a separate publication; it does not affect the status of the check as evidence (22/23 with controls 0/20).

**A secondary source of spread** is accounted for by name: 10 of the 23 localizing disks store the center with only 5–6 significant digits (Appendix A, §3.2). With a typical effect of about 3×10⁻⁵ the rounding of the low-precision center gives a spread of several percent. This is precisely why the disks with low-precision centers are listed by name in Appendix A.

## 8. The early runs and why their numbers are not admitted as evidence

The frozen run that gave all the numbers above was the third. The exposition of this section complements §7.5 of the main text with the quantitative part.

### 8.1. What was in the first two runs

**Run 1.** Scanned levels m = 8…12 in two forms of sign recording, calibrated by the constant

    A_pure = −0.4994184926615044

It had **no** exact-period check and **no** detector of Newton "paralysis": in the absence of convergence the last iteration was issued as the result. At level m = 10 the pure form gave 22 converging roots out of 23 at mean discrepancy 2.4×10⁻⁵ — externally the same result as in the final run. The run's own verdict was negative with a caveat: convergence in m did not follow the law δ^(−m), and odd m failed because of the sign-alternating recording.

**Run 2.** Built to eliminate the four documented defects of the first, including the paralysis detector. The calibration constant remained the same (A_pure). By its own, pre-fixed criteria, it returned a negative verdict for both forms of recording; at level m = 10 **4 roots out of 23** converged.

**The negative verdict was overridden by a decision of its inapplicability, not by a rerun.** Two grounds were given: (1) the auxiliary t*-test continued to use the sign-alternating recording (−δ)^m, from which the main transformation had already been abandoned; (2) a regression of the solver — the new Newton converged in 4 cases out of 23 against 22 of the first run. Neither ground concerned the calibration constant, i.e. the quantity that was actually wrong. This was a methodological error; the correct move — to correct the cause and run again — was made only in the third run.

### 8.2. The quantitative cause: a shift by exactly one layer

The ratio of the calibration constants:

    A_correct / A_pure = −2.3318856295507041… / −0.4994184926615044 = δ

with agreement to the twelfth digit. The error in the calibration was by exactly a factor of δ.

Direct comparison of the positions to which the runs converged gives for the ratio of distances from c_F:

| level m | ratio \|c_ss(early) − c_F\| / \|c_ss(final) − c_F\| | δ^(11−m) | agreement |
|---:|---|---|---|
| 8 | 101.796 | δ³ = 101.79534 | 5 significant digits (relative discrepancy 7×10⁻⁶) |
| 9 | spread (12–55) | (δ² = 21.80144) | early converged only partially |
| 10 | 4.669203 | δ¹ = 4.6692016 | 7 significant digits |
| 11 | spread (0.57–2.53) | (δ⁰ = 1) | early converged only partially |
| 12 | 0.214169 | δ⁻¹ = 0.21416938 | 6 significant digits |

The ratios are computed on all disks on which the early run converged: 21 disks at m = 8 (one is missing) and 22 at m = 10 and m = 12; the median is given in the table.

The spread at m = 9 and m = 11 is the expected sign of the same Newton paralysis that was not detected in the early run. The repeated values of the modulus at these levels betray several disks that have converged to one and the same root.

**Conclusion.** The error in the calibration constant by exactly a factor of δ shifted the search by exactly one self-similar layer. The roots that the early run at level m accepted as target ones lie at a radius characteristic of layer m − 1, and have characteristic period 2^m, not 2^(m+1). Their "closeness" to the prediction is largely tautological: the Newton starting point was built from the catalogue zero through the same erroneous scale, and Newton, not having moved far, found a locally similar root on the foreign layer.

Therefore the "22/23 at 2.4×10⁻⁵" of the early run confirms not the testable hypothesis, but the fact of δ-self-similarity of the Mandelbrot picture itself — which is established anyway. As independent evidence in favour of the correspondence these numbers are not suitable and are not used in the present work.

### 8.3. What remained unchecked

A controlled run in which the previous pipeline was restarted **with a single change** — the corrected constant — has not been carried out. Therefore the contribution of "the corrected calibration" and the contribution of "a more reliable solver and a different acceptance rule" to the success of the third run have not been quantitatively separated.

It is only known that (a) the erroneous constant is real, reproducible, and differs from the correct one by exactly a factor of δ, and (b) the mere absence of the exact-period check is enough to accept a foreign layer as one's own.

Such a controlled run seems useful and feasible; it is not presented here.

## 9. Summary of the experiment

| quantity | value |
|---|---|
| catalogue positions | 23 |
| accepted | 22 |
| rejected | 1 (Z72, analysis in §5) |
| of the accepted ones, how many required only one Newton attempt | 22 out of 22 |
| range of d_u | 2.027×10⁻⁵ … 3.718×10⁻⁵ |
| median d_u | 3.158×10⁻⁵ |
| specificity, range (22 accepted) | 986 … 8486 |
| specificity, median | 3713 |
| control points | 20 |
| controls accepted | **0** |
| Newton attempts on controls | 980 |
| of which converged to some root | 924 |
| of which to a root of exact period 2048 | 847 |
| median ratio of residual to drift prediction | 0.9635 |
| median phase discrepancy | 0.35° |
