# Zeros of the universal scaling function of the period-doubling cascade

A self-contained research package: an article and seven appendices. Every definition, every number that enters the conclusions, and every step of the proofs is contained within these files. There are no external references; every link either points to another place in the package or to published literature.

## Contents

| file | contents | size |
|---|---|---|
| **`01-ARTICLE.md`** | **Main article.** Statement, method, proof of holomorphy of the limit, four theorems and one proposition, interpretation through the Mandelbrot set, limitations | ~75 pp. |
| `02-APPENDIX-A.md` | Appendix A. Complete table of 23 localizing disks: centers, radii, margins, closing routes, marking bands | |
| `03-APPENDIX-B.md` | Appendix B. All constants of the work with status "rigorous / computed / calibration" and an indication of where each one enters | |
| `04-APPENDIX-C.md` | Appendix C. Informal explanations of key concepts; does not affect the claims of the work | |
| `05-APPENDIX-D.md` | Appendix D. Full derivation of the coordinate mode (Proposition 5; a classical fact in explicit form), including the explicit origin of the "missing two" | |
| `06-APPENDIX-E.md` | Appendix E. Verification standard, tamper batteries, recurring error type | |
| `07-APPENDIX-F.md` | Appendix F. Numerical-experiment protocol of section 7: per-disk tables, controls, calibration, early runs | |
| `08-REFERENCES.md` | Appendix G. References | |
| `09-CODE/` | Replication package: code and data of sections 5 and 7 under a sha256 manifest, control reruns, instructions (`README-CODE.md`) | |

## What is proved and what is not

The separation is made explicit in every claim. Briefly:

**Rigorous results** (computer-assisted proof, 512-bit interval arithmetic, directed rounding):

- exactly two zeros of the function H in the disk \|u\| < 7, both real and simple;
- exactly one simple zero in each of the 23 certificate disks of the annulus 7 < \|u\| < 10;
- **holomorphy of the limit function H** — the central analytical result, making the two preceding claims unconditional;
- certified marking of the 23 disks into six bands;
- the quadratic drift law on five transitions of finite levels;
- existence and uniqueness of all 23 superstable partners of exact period 2048 (Mandelbrot side) in boxes of radius 10⁻²⁷.

**Analytical result:** the coordinate mode of the doubling operator N = G − x·G′ with eigenvalue α², written out explicitly for our normalization (Appendix D; this is a classical fact — Feigenbaum 1979; Collet–Eckmann–Lanford 1980; Christiansen–Cvitanović–Rugh 1990; Briggs 1994). One link in the derivation is numerical, and this is stated explicitly.

**Not proved, and stated outright:**

- completeness of the list of zeros in the annulus (that there are no other zeros there) **is not claimed**;
- the link with the Mandelbrot set (section 7): both ends of each pair are theorems (a zero of H in a disk, a partner in a box), but the calibration mapping between them is numerical, and a rigorous version of the correspondence as a single theorem has not been established;
- membership in a band is proved for the centers of the disks, not for the zeros themselves;
- the limit asymptotics of the drift law are conditional.

The full list of limitations is in section 8 of the main text.

## How to read

**If you need a quick sense of what the work is about:** the abstract at the beginning of `01-ARTICLE.md`, followed by Appendix C.

**If you need to verify the mathematics:** sections 2–5 of the main text; the narrow points are collected in §5.4 and §5.5. The numbers that enter the conclusions are in Appendix B. The full derivation of Proposition 5 is in Appendix D.

**If you need to verify the numerical part:** Appendix A (the disks) and Appendix F (the experiment of section 7). Both tables are given in full, not in summary form.

**If you are interested in the computer-assisted proof methodology:** Appendix E.

## Notes for the referee

A few places where the work itself points to its own weaknesses; they are not hidden in the text, but they are easy to miss:

- **The winding of the denominator inside the contours** was the last uncertified link of the chain of theorems 1–2 (it was checked numerically); it is closed by a rigorous interval winding certificate on all 25 contours plus a homotopy transfer to the limit slice through a convex tube (§5.3(v), §8 item 5). The machine certificate is included in the replication package.
- **Early runs of the numerical experiment used an erroneous calibration** and produced a seemingly convincing result about roots of an adjacent self-similar layer (§7.5; full analysis — Appendix F, §8; in the main text §7.5 is compressed to a summary). Their numbers are not admitted as evidence.
- **The tube budget 5.44×10⁻⁷ is imposed, not derived** (§5.3(iii)). It is an ℓ¹ budget chosen when assembling the base level. The substantive claim is that domain certification is performed exactly for perturbations of this size.
- **The tightest inequality of the work goes through with a margin of 0.0507 %** (§5.4). The same place explains why the tightness is misleading and what the real margin on the constant is (a factor of 2.36).
- **Nine disks have a margin on the base level smaller than 1** (Appendix A, §3). All 23 disks are closed: of these nine, seven are closed by a refined majorant at level m = 7, and two (Z57, Z60) at the base level m = 8. Separately, Z72 is closed at m = 8 with a contour subdivision, so the total number of disks closed at m = 8 is three. The table shows both margin values.
- **Two literals of the norms in the input data were lower than the true values**, that is, formally not upper bounds (§5.5). The quantities have been recomputed rigorously; all inequalities have been rechecked and hold.
- **The materials of the numerical experiment of section 7 are deposited** in the replication package `09-CODE` together with the code of the key certificates of section 5; when assembling the package each component was rerun from the package itself with reproduction of the registered verdicts (§9). Earlier versions of the package honestly acknowledged an incompleteness here; it is closed.
- **Eleven cases of one error class** — "the quantity is certified with care, but it is not the desired quantity" — are listed by name in Appendix E, §3, together with the numbers that nearly entered the text as a result. The last three were found while the finished package was being reviewed.
