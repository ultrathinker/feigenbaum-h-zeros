# Appendix E. Verification standard and the recurring type of error

The work was carried out in a regime where every result must survive an attempt to break it. Below is the design of this circuit. We give it in the appendix not as an organizational detail, but because in computer-assisted proof the design of the verification is part of the content of the result: the statement "proved by machine" is exactly as strong as the procedure that separates the proof from the agreement is.

## 1. Certificate and verifier are different programs

For every result a machine **certificate** is composed — a file with all the numbers — and an **independent verifier** that recomputes every numerical field with explicit tolerances and exits with an error on any discrepancy.

The key requirement: the verifier is written to a specification composed **before** the certificate appears, and its author has no access to the code of the certificate's author. Otherwise one gets not a check but an agreement: the verifier reproduces the same assumptions, including the wrong ones, and the green result carries no information.

This requirement is not formal. Three coverage numbers, which stood in the working materials as verified ones, turned out to be incorrect, and they were found precisely by the verifier written in isolation (Appendix A, §6). None of the three changed the conclusions — but none would have been found by cross-checking with one's own code.

**Where the report of the independent verifier and its materials lie.** The full verification set — the report, the M3 analysis, and the code itself — is assembled in the replication package at the path `09-CODE/section5_base_certificates/h1_package_verify_E/` (REPORT_E.md, M3_ADJUDICATION.md, h1_verify_pkg.py). These materials close the requirement "verifier specification before the certificate appears" — the specification is fixed in REPORT_E.md and is implemented in h1_verify_pkg.py without importing the certificate's code.

## 2. Corruptions are mandatory

Naive verifiers are systematically "green" on corrupted data: some fields are never checked. During the work such defects were uncovered **eight times**, and each time — only by deliberate corruption of the file, never by reading the code. (This count should not be confused with the list of §3: there it is a different class — substitution of the very quantity — and there are eleven of those.)

### 2.1. Design of the battery

The verifier of the certificates of the holomorphy proof — 26 checks — was subjected to a battery of twelve corruptions:

1. substitution of the final quantity by another, still passing number;
2. substitution of a constant;
3. truncation of the certificate radius below the actual reaching of the orbit (corruption of **applicability**, not of a number);
4. exceeding the threshold on one arc;
5. negative denominator;
6. deletion of a file;
7. renaming of a working disk into a negative control;
8. reversal of a negative control;
9. mismatch of budgets;
10. perturbation of a coefficient in the twentieth digit;
11. breaking of the spectral signature;
12. plus one corruption **the other way round** — a cosmetic rearrangement of keys, on which the verifier must not fall.

### 2.2. Result of the first run: two corruptions passed unnoticed

Nine corruptions were caught, the cosmetic one was correctly not caught, **two passed**.

- **The spectral-signature check** recomputed it from constants **written into the body of the verifier itself**, not read from the file under verification. The specification required "recompute from the primary constants"; the author understood "primary" as "the ones I typed". The substitution of a constant in the data was invisible to this check.
- **The coverage check** *printed* the breakdown of working and control arcs, but the verdict of the line was hung on a different condition. Renaming a working disk into a control one passed silently — a mapping without enforcement.

Both holes were closed, and the battery was run again in full: eleven corruptions out of eleven are caught, the cosmetic one is still not caught. Separately it was checked that the substitution of the spectral constant brings down exactly that check, and for that reason, rather than just giving a nonzero return code.

### 2.3. The episode for the sake of which it is worth reading about corruptions

One of the corruptions in a later revision **did not work**: its log matched the base one byte-for-byte. The corruption was meaningful — a narrowing of the budget in the certificate — and was supposed to break something.

On analysis it turned out: the central check compared the quantity with a **literal embedded in the code**, not with a field of the certificate, whereas the auxiliary one read the field. The corruption of the budget simply did not reach the central check. After replacing the literal by reading from the artifact, the corruption worked.

Crucially, the defect was visible **only** through the failure of the check. On a green run both checks passed, the numbers agreed, and nothing indicated that one of them was protecting something other than what it seemed. Hence the practical rule: **a non-triggered corruption is the same signal as a triggered one**, and requires analysis until it becomes clear why it should not have triggered.

In the same revision it was discovered that one of the verifiers computes the verdicts correctly, but always exits with a zero return code and does not print the failure. A reader looking at the return code or at a brief summary would not notice the substitution. A gate on the verdicts was added, checked in both directions: on corrupted data the return code is 1 with an indication of the broken constant, on clean ones it is 0.

## 3. The recurring type of error: "the quantity is certified with care, but it is not the desired quantity"

We separately mark the class of defects that occurred in this work **eleven times** and, in our experience, is the most dangerous in computer-assisted proof.

1. The estimate of the accumulated deviation was issued as the estimate of the sum of layerwise increments — different things, related by the triangle inequality in an inconvenient direction.
2. The verifier computed the "primary constants" from its own literals instead of from the file under verification (§2.2).
3. The rigorous bound of the operator norm turned out to be the bound of its contraction on the first hundred modes: the tail was absent. The sign — coincidence with the midpoint estimate down to the fifteenth digit; an honest upper bound must differ from it by the size of the tail.
4. The constant was taken from a source that declared itself a probe rather than a certificate.
5. The margin on the threshold constant of the lemma was measured against the intermediate subgoal, not against the final derivation: a one-time calculation gave a breaking point of 3050, the certified scan — a fork of [3018, 3019]. Both numbers are correct, the questions are different.
6. The same thing, independently, repeated itself with the margin on the quadratic coefficient: the one-time estimate "up to about 179" also referred to the subgoal, and the certified fork against the derivation is [136.4258, 136.4844].
7. In the same calculation only one of the two dependencies was taken into account: the quadratic coefficient enters not only the main tail term, but also the majorant of the nonlinear source, and through it — the second and third terms. Accounting for one path gave a breaking point of 178.29 instead of 136.43.
8. The text nearly included the claim that the tube budget 5.44×10⁻⁷ is derived from a certificate of the K-radius. In the same file the field with a similar name equals 3.566×10⁻⁷; the budget is imposed, not derived.
9. The observed ratio of the radii of the early and final runs at m = 8 (101.796) was printed as the value of δ³. The true δ³ = 101.79534; the printed 101.797 agreed neither with the observation nor with the theory, and at the same time overstated the claimed accuracy of the agreement (section 7.5).
10. The "fingerprint" arg(x_{2^m}) mod 180° for disk Z72 (58.08°) was issued as the polar angle of the position of the zero (56.3°). The cause — both quantities were called in the table by the single word "angle" (section 7.6, Appendix A §1).
11. An aggregate property was issued as a per-instance one: from the fact that the median phase discrepancy in the vector drift check equals 0.35°, it was deduced that the "phase discrepancy is less than a degree **on all** 22 disks". By the table of Appendix F §7 itself, three disks (Z05, Z59, Z19) exceed one degree; the correct statement is "19 out of 22". A variety of the same class: substitution not of another quantity, but of another quantifier.

**The common feature.** The error is not in the arithmetic, and therefore is not caught by recomputing: recompute as many times as you like, you get the same correct number. It is caught only by the question "what exactly is bounded above here" — i.e. by comparing the quantity with the statement, not with another quantity. Case 11 adds to this a second check: **by which quantifier** the quantity is tied to the objects. An aggregate ("the median is small") and a per-instance statement ("it is small at each one") are different statements, and the first does not imply the second.

We also note how these cases were found. The ninth and tenth were found by a reviewer who recomputed all the numbers anew in rigorous arithmetic; the eleventh — by the same reviewer, comparing the statement with the table in the same appendix. A parallel reviewer checking the same text not only missed the eleventh case, but also included the false statement in his list of confirmed ones. The coincidence of two checks here would have meant not confirmation, but shared blindness.

**Two applied conclusions.**

*First.* The acceptance criteria of a number should be written **before** the number is obtained. Twice in this work the obtained value fell exactly under the threshold — the most tempting case for not looking closely.

*Second.* The checker must be told directly **what exactly he is checking and whose work**, and that agreement with already available numbers is not acceptance. Telling is the distribution of these eleven cases: almost all were made on the side that combined the results, and they were found by checkers to whom this instruction was given explicitly. A checker who was not told this reproduces the numbers and reports agreement — which was precisely what was not to be checked.

## 4. What independence costs

A practical observation that we consider important to record: **independence is lost silently, and looks like confirmation.**

A checker who has been given access to the report of a neighbour begins to quote it; a checker who knows the expected answer finds it. Neither looks like a violation — both produce a coherent result, and it is precisely the coherence that creates a false impression of strength.

The practical consequences we used:

- parallel checkers — different working areas, without access to one another's materials;
- in a blind review, leave at least one reviewer **without numbers**: a reviewer with numbers checks "was it computed correctly", a reviewer without numbers checks "was the right thing computed". The second question is not caught by machines at all;
- the verifier specification is written before the certificate and is not changed after the certificate has appeared.

## 5. Methodological conclusions

1. **Hollow PASS.** A checking program written together with the certificate is often green even on corrupted data. Corruptions are mandatory for every verifier.

2. **Interval blow-up gives two-sided errors.** Not only false refusals, but also silently underestimated margins. The hardest disk of the work (Z72, 176 arcs) was closed solely by subdividing the arcs — without a single change of mathematics.

3. **The boundary of the tool resembles the structure of the object.** The support of the certified series carves a jagged lamella on the map, which is easy to mistake for a singularity of the function itself. The separation "property of the object versus property of the tool" required separate maps.

4. **Float reconnaissance, interval conclusions.** Double precision confidently showed an anomalous rate of drift of the left zero; the rigorous recomputation refuted the anomaly.

5. **The exhaustion of a method is not the exhaustion of the problem.** The conclusion that the holomorphy of the limit is unattainable by computational means was correct exactly for one route — controlling the orbit of full length. The operator route along the renormalization tower turned out to be open, and most of the necessary certificates already existed.

6. **Acceptance criteria — before obtaining the number.** Otherwise the acceptance is adjusted to the result, especially when the result falls exactly under the threshold.

7. **A test on a self-similar picture must fix the scale independently.** Otherwise it confirms any of its floors. An error in the calibration constant by exactly a factor of δ shifted the search to the neighbouring renormalization layer, where the match statistics are the same in order, — and the early version of the experiment gave a seemingly convincing result about the wrong roots. The layers are distinguished only by an independent period check (sections 7.4, 7.5 of the main text).

8. **A negative verdict is overridden by a rerun, not by a decision of its inapplicability.** If the acceptance criterion, fixed in advance, worked against us, the only correct move is to correct the cause and run again. Everything else turns the preliminary fixation of criteria into a decoration. We broke this rule once, and the analysis of the episode is in §7.5 of the main text; precisely for this reason the numbers of the early runs are not admitted as evidence in any form.

9. **A non-triggered corruption is a signal.** See §2.3. A corruption that was supposed to break something and did not break it points to the fact that the check protects something other than what it seems.
