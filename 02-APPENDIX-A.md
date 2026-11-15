# Appendix A. Complete table of localizing disks

This appendix relates to sections 3 and 6 of the main text. It contains all 23 annulus disks of Theorem 2 in machine-verified form, and explains by which certificate each of them is closed. The table is self-contained: from it one can reconstruct all the summary quantities given in the main text.

## 1. What is in the table

| column | meaning |
|---|---|
| **ID** | identifier of the disk (sequential numbering of zeros) |
| **address** | "band.number"; the band is defined by the angular quantity, the number by growth of the modulus of the center inside the band (Theorem 3) |
| **Re, Im of center** | certified center of the localizing disk. Shown as many decimal digits as have been **actually certified**; zeros are not appended at the tail |
| **\|u\|** | modulus of the center; given for convenience, monotonicity in it inside a band guarantees injectivity of the address |
| **digits** | number of certified significant digits of the center: 14–16 (high-precision census) or 5–6 (low-precision) |
| **ρ** | radius of the localizing disk |
| **fingerprint** | arg(x_{2^m}) mod 180°, computed at the exact center; interval width of order 10⁻¹¹ degrees, the middle is shown. **This is not the polar angle of the center** — a quantity of a different nature, and the two must not be confused: for example, at Z72 the fingerprint equals 58.08°, while the polar angle of the position of the zero equals 56.3° |
| **base margin** | per-arc margin at the base level m = 7 in the original form of the tail majorant: H7_abs_lower / Btail_upper. A value > 1 proves winding 1 on the contour and the transfer to the limit |
| **final margin** | the margin **by the closing route actually used** — the quantity by which Theorem 2 is proved for this disk |
| **route** | by which certificate the disk is closed (§3) |
| **arcs** | number of arcs of the contour partition |

## 2. Table

| ID | address | Re(center) | Im(center) | \|u\| | digits | ρ | fingerprint arg(x_{2^m}) mod 180°, ° | base margin | final margin | route | arcs |
|---|---|---|---|---:|---:|---|---:|---:|---:|---|---:|
| Z40 | I.1 | 8.36818444963026 | 3.42161554921713 | 9.0407 | 14 | 0.1 | 21.5996 | 4.4744 | 4.4744 | direct, m=7 | 32 |
| Z60 | I.2 | 8.26332724866471 | 4.01596385048377 | 9.1875 | 14 | 0.1 | 25.5060 | 0.6028 | **> 1** | base m=8 | 64 |
| Z57 | I.3 | 8.589396 | 3.974588 | 9.4644 | 6 | 0.1 | 24.5071 | 0.4709 | **> 1** | base m=8 | 64 |
| Z59 | II.1 | 7.125929 | 4.064322 | 8.2035 | 6 | 0.1 | 28.5514 | 2.9052 | 2.9052 | direct, m=7 | 32 |
| Z02 | III.1 | 5.817868 | 4.476081 | 7.3405 | 6 | 0.1 | 35.0447 | 8.2028 | 8.2028 | direct, m=7 | 32 |
| Z05 | III.2 | 5.011415 | 5.626752 | 7.5349 | 6 | 0.1 | 46.2840 | 3.7173 | 3.7173 | direct, m=7 | 32 |
| Z39 | III.3 | 6.24846326820913 | 5.67889810713901 | 8.4435 | 14 | 0.1 | 42.1826 | 3.9820 | 3.9820 | direct, m=7 | 32 |
| Z63 | III.4 | 6.83110274129083 | 5.23116997709336 | 8.6040 | 14 | 0.1 | 37.2367 | 3.8283 | 3.8283 | direct, m=7 | 32 |
| Z17 | III.5 | 6.681454 | 6.210555 | 9.1221 | 6 | 0.05 | 44.2189 | 2.0261 | 2.0261 | direct, m=7 | 32 |
| Z67 | III.6 | 6.61525908186462 | 6.33935578550363 | 9.1624 | 14 | 0.05 | 45.2998 | 0.9953 | **1.3351** | majorant v2, m=7 | 32 |
| Z64 | III.7 | 7.218228 | 5.788641 | 9.2526 | 6 | 0.05 | 39.6440 | 1.9950 | 1.9950 | direct, m=7 | 32 |
| Z65 | III.8 | 7.36053136328949 | 5.76158912153642 | 9.3474 | 14 | 0.05 | 39.0055 | 0.9478 | **1.2716** | majorant v2, m=7 | 32 |
| Z68 | III.9 | 7.055487 | 6.338351 | 9.4844 | 6 | 0.05 | 43.7150 | 0.9879 | **1.3254** | majorant v2, m=7 | 32 |
| Z66 | III.10 | 7.24399319091292 | 6.18809344211899 | 9.5272 | 14 | 0.05 | 42.1019 | **1.0023** | **1.0023** | direct, m=7 | 32 |
| Z69 | III.11 | 7.26684 | 6.413616 | 9.6923 | 6 | 0.05 | 43.4440 | 0.9546 | **1.2810** | majorant v2, m=7 | 32 |
| Z70 | III.12 | 7.33895547113294 | 6.50543963525410 | 9.8072 | 14 | 0.05 | 43.7633 | 0.8171 | **1.0965** | majorant v2, m=7 | 32 |
| Z19 | IV.1 | 4.008907 | 6.703721 | 7.8110 | 6 | 0.1 | 58.4205 | 6.1540 | 6.1540 | direct, m=7 | 32 |
| Z38 | IV.2 | 4.63702563107768 | 6.75922558655159 | 8.1969 | 14 | 0.1 | 56.0208 | 0.9736 | **1.3051** | majorant v2, m=7 | 32 |
| Z71 | IV.3 | 4.50618857227679 | 7.07800180592392 | 8.3907 | 14 | 0.1 | 58.8530 | 0.7980 | **1.0699** | majorant v2, m=7 | 32 |
| Z72 | IV.4 | 4.758336330290482 | 7.1277051021354385 | 8.5701 | 16 | 0.1 | 58.0781 | — | **> 1.33** | m=8, 176 arcs | 176 |
| Z73 | V.1 | 4.020255 | 8.037592 | 8.9870 | 6 | 0.1 | 67.7741 | 1.9541 | 1.9541 | direct, m=7 | 32 |
| Z74 | V.2 | 4.72725441425135 | 8.68634320415312 | 9.8894 | 14 | 0.1 | 68.6570 | 1.5307 | 1.5307 | direct, m=7 | 32 |
| Z01 | VI.1 | 1.55349371071307 | 8.12380315987080 | 8.2710 | 14 | 0.1 | 81.7080 | 7.0682 | 7.0682 | direct, m=7 | 32 |

## 2.1. Circle |u| = 7

The closed disk |u| ≤ 7 contains both real zeros of Theorem 1; completeness on this very contour is certified separately from the 23 annulus disks and from the two disks of radius 1/6. The adaptive covering of the contour began with 96 arcs; on six of them the first pass failed the Rouché check due to loss of accuracy of the interval covering, and each was divided into four parts — the final covering consists of 114 arcs, exactly tiling the contour without gaps and overlaps.

| quantity | value |
|---|---:|
| rigorous winding of H₇ on |u| = 7 | 2 ± 2.52×10⁻²² |
| worst Rouché ratio margin (min \|H₇\|/\|H−H₇\|) | ≥ 1.5471 |
| minimum absolute gap (min \|H₇\|−\|H−H₇\|) | ≥ 0.05164 |
| maximum working coordinate of the composition Rmax | 0.4011 < 1 |

A nested control on |u| = 5 gives winding 1; a crude negative control was rejected correctly. Assembly check — 22/22. Source: `09-CODE/archive_inputs/path_to_8/point2_completeness_disk7/` (`h7_circle_certificate.py/.json`, `arcwise_rouche_certificate.py/.json`, `pilot_slice.py`, `pilot_slice_summary.json`, `verify_disk7_certificate.py` → `disk7_audit.json`).

## 3. Closing routes — and why nine disks have "base margin" below 1

The "base margin" column shows the value obtained by the **first** form of the tail majorant. For nine disks it turned out below 1, i.e. this form was not enough for the transfer of the winding to the limit. This is not a defect of the result: the transfer is proved for all 23 disks, but for some of them — by a different certificate. A reader looking only at the "base margin" column will see numbers like 0.47 and should know by what they are closed.

**Route 1 — direct, m = 7 (13 disks).** The winding of H₇ equals 1 on the contour, the per-arc transfer margin is greater than 1. The worst case is Z66 with a margin of 1.0023; this is the tightest place of the entire disk census.

**Route 2 — refined tail majorant, m = 7 (7 disks: Z38, Z65, Z67, Z68, Z69, Z70, Z71).** The first form of the tail majorant overestimated the layerwise contribution more than necessary. The second form computes the contribution layer by layer with a recomputed recursion and dominates the far tail separately, remaining a strict upper bound. The improvement is practically the same for all disks and amounts to **1.3406–1.3420 times**:

| disk | base margin | improvement | final margin | verdict |
|---|---:|---:|---:|---|
| Z38 | 0.9736 | 1.3406 | 1.3051 | closed |
| Z65 | 0.9478 | 1.3416 | 1.2716 | closed |
| Z67 | 0.9953 | 1.3414 | 1.3351 | closed |
| Z68 | 0.9879 | 1.3417 | 1.3254 | closed |
| Z69 | 0.9546 | 1.3419 | 1.2810 | closed |
| Z70 | 0.8171 | 1.3420 | 1.0965 | closed |
| Z71 | 0.7980 | 1.3408 | 1.0699 | closed |
| **Z60** | **0.6028** | **1.3415** | **0.8086** | **not closed by this route** |
| **Z57** | **0.4709** | **1.3417** | **0.6318** | **not closed by this route** |

The closing criterion was fixed in advance and is the same for all nine: the margin must exceed 1 **on every arc**, not on average. Two disks did not pass it, and this is recorded as a refusal, not fitted.

**Route 3 — base level m = 8 (2 disks: Z57, Z60).** The disks not closed by the second route have been re-certified from base level 8, i.e. on orbits of doubled length, with a partition of the contour into 64 arcs instead of 32 and with the anchor of the tail majorant at level 7. At this level both are closed.

**Route 4 — m = 8 with subdivision (1 disk: Z72).** The most difficult certificate of the work: 176 arcs, each with a margin above 1.33. The cause of the difficulty is geometric, see §3.1.

Total: 13 + 7 + 2 + 1 = 23.

**The worst margin by the actual route** equals 1.0023 (Z66). All the other disks are closed with a margin no less than 1.0699.

### 3.1. Z72 — the only disk with a shifted center

Z72 is the only one of the 23 disks whose center is **deliberately shifted** from the zero itself. The true zero lies approximately at the point (4.79165, 7.177607), with modulus about 8.63; the disk center is taken at (4.758336, 7.127705), with modulus 8.5701. The shift is about 0.06 in the direction of the origin.

The cause: when centered on the zero itself, the certificate contour touches the boundary of the convergence region of the series used. Shifting the center brings the contour inside the region, while keeping the zero inside the disk of radius 0.1.

This shift is the only non-standard geometry in the table, and it has a direct consequence for section 7 of the main text: the comparison with the quadratic family, if supplied with the disk center, for Z72 compares the wrong object. The analysis is in §7.6 of the main text.

### 3.2. Accuracy of the centers: two classes

Thirteen disks have centers with 14–16 certified significant digits, ten — with 5–6 (Z57, Z59, Z02, Z64, Z69, Z68, Z17, Z05, Z19, Z73). The difference is a consequence of two different censuses, and it **does not weaken the certificates**: the proved error of the center of order 6×10⁻⁷ is five orders of magnitude smaller than the radii of the disks (0.05–0.1), so the zero remains inside the disk with a colossal margin.

The consequence of this difference is different, and it shows up not here, but in section 7: in the comparison with the quadratic family the measured effect has magnitude about 3×10⁻⁵, and the rounding of the low-precision centers to 5–6 digits introduces a spread of several percent into this comparison. The disks with low-precision centers are listed above by name precisely so that this contribution can be separated.

## 4. Bands and marking (Theorem 3)

The twenty-three disks are partitioned by angular quantity into six bands. The proved inter-band gaps:

| boundary | between disks | gap, ° (lower bound) |
|---|---|---:|
| I–II | Z60 → Z59 | **3.0454** |
| II–III | Z59 → Z02 | 6.4933 |
| III–IV | Z05 → Z38 | 9.7368 |
| IV–V | Z71 → Z73 | 8.9211 |
| V–VI | Z74 → Z01 | 13.0510 |

The maximum **intra-band** step equals 2.9075° and is attained in band I between Z40 (21.5996°) and Z57 (24.5071°).

The partition is proved because the minimum inter-band gap is strictly greater than the maximum intra-band step:

    3.0454° > 2.9075°

The injectivity of the address "band.number" follows from this together with the monotonicity of the modulus of the center inside each band (the \|u\| column of the table in §2: inside each band it strictly increases with the number).

**What is certified here and what is not.** What is certified here is the band membership for the **centers** of the disks. The claim that the same partition survives the transition to the envelope of the whole disk — i.e. that band membership is a property of the zero itself, not of the chosen center — is not proved: the rigorous interval envelope of the fingerprint over the disk blows up, and a non-blowing-up method is not implemented. Float reconnaissance gives a spread of the fingerprint over the disk of about 1.6–1.8°, which would suffice with a margin, but this is reconnaissance, not a certificate (section 8, item 9 of the main text).

## 5. Summary quantities

| quantity | value |
|---|---|
| disks in the annulus | 23 (radii 0.05 and 0.1) |
| disks in total (23 annulus + 2 disks of real zeros from Theorem 1) | 25 |
| working arcs with tube certificates | 1465 = 1542 tube-files of five groups (census_A 416, census_B 357, point14 257, point17 384, point3B 128) minus 77 negative controls (`h1pkg_certificate.json`, field coverage). The number 944 (per-disk table of §2) — arcs of the final routes of 23 disks; the circle |u| = 7 is certified separately (114 arcs, folder `point2_completeness_disk7`, not included in 1465) |
| negative controls (not in the coverage) | 77 |
| tube certificates total | 2425 |
| worst per-arc margin by the actual route | 1.0023 (Z66) |
| worst working Rmax | 0.885 |
| minimum of the lower bound of the denominator | 1.1186×10⁻³ on the disk of the left real zero (u ≈ −1) — the minimum over the 1465 working arcs of certificate h1pkg (`h1pkg_certificate.json`, field `min_x128_lower`), worst case, consistent with §5.3(v); separately `winding_certificate.json` gives 1.1166×10⁻³ — minimum over the 25 contours of the winding certificate (the `min_x128_lower` analogue; different sets of arcs, both numbers are lower bounds); on the M-side — minimum distance between box centers 1.02×10⁻⁸ (see §7.3 "Rigour of the M-side" of the main text) |
| disks closed from level 7 | 20 |
| disks requiring level 8 | 3 (Z57, Z60, Z72) |
| disks with centers of 14–16 digits | 13 |
| disks with centers of 5–6 digits | 10 |
| bands | 6 |
| minimum inter-band gap | 3.0454° |
| maximum intra-band step | 2.9075° |

The certified lower bounds of the modulus of H on the contours for four disks: 21.98, 21.50, 17.72 and 9.28. These values substantially exceed the quantity given by a naive estimate through the norm of the fixed point: the latter refers to a partial tower, while the quantity under consideration lives on the full tower up to the zero level and goes to a distance of about 19.7.

## 6. Three corrections to the previous coverage counts

Three numbers of this appendix were previously different, and they were corrected by an independent verifier written without access to the source code. We give them because the error is reproducible and instructive:

- working arcs **1465**, not 1542: 77 negative controls were erroneously included in the coverage — i.e. arcs on which the certificate is required **not** to pass;
- minimum of the lower bound of the denominator **1.1186×10⁻³**, not 5.6×10⁻³, and it is attained on a different disk;
- tube certificates total **2425**, not 2426.

None of the three changes the conclusions: all three are coverage and diagnostic quantities, not inputs of inequalities. But all three stood as verified ones.
