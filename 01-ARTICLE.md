# Zeros of the universal scaling function of the period-doubling cascade: rigorous computer-assisted localization, holomorphy of the limit, and the link with the Mandelbrot set

**Yevhen Borzenkov** · ORCID [0009-0002-7946-589X](https://orcid.org/0009-0002-7946-589X) · preprint, version 2.5 (16.08.2026), not peer-reviewed

**About the package.** This text is self-contained. Every definition, every number that enters the conclusions, and every step of the proofs is given here and in Appendices A–F. There are no external references; every link either points to another place in this same text or to the published literature (Appendix G). The separation "proved rigorously" / "checked numerically" is made explicit in every claim.

---

## Abstract

For the Feigenbaum period-doubling cascade we construct a single complex-analytic function H(u) that measures the ratio of adjacent scales of the critical orbit of the universal (limit) family, and we carry out a rigorous computer census of its zeros in the disk |u| < 10.

Three rigorous results:

(i) **Census of zeros of H in the disk |u| < 10 and holomorphy of the limit.** In the disk |u| < 7 the function H has exactly two zeros, both real and simple: the left one in a disk of radius 1/6 around −1; the right one is unconditionally localized in a disk of radius 1/6 around 5.94, and, under the additional hypothesis of a geometric rate (the hypothesis is stated in Theorem 4 / §8 item 2), is conditionally localized in the narrower interval [5.9409360413, 5.9409363308]. In the upper half-plane of the annulus 7 < |u| < 10 there lies a single simple zero in each of 23 certificate disks; together with their complex conjugates this gives 46 zeros of the annulus, and together with the two real zeros of the disk — 48 localized zeros in the disk |u| < 10. By "localized zeros" we mean zeros for which we have proved the existence of exactly one simple zero in each of the indicated disks; the existence of other zeros in the annulus 7 < |u| < 10 is not claimed. Completeness of the list in the annulus is not claimed. The limit function H = lim H_m is holomorphic in a neighbourhood of each of the closed disks under consideration, and in the disk |u| < 7 on its entire interior (section 5); the absence of zeros of the denominator inside the contours is certified by a rigorous interval winding with a homotopy transfer to the limit slice (section 5.3(v)), and over the whole disk |u| < 7 additionally by a winding certificate on the circle |u| = 7 (114 arcs) and a lemma on the removability of singularities of the ratio (section 5.3(v)).

(ii) **23 superstable parameters.** All 23 superstable parameters of the family z² + c, paired in section 7 with the annulus zeros, exist and are unique: for each one a box of radius 10⁻²⁷ has been certified that contains exactly one parameter of exact period 2048 (Krawczyk operator and interval Newton; §7, "Rigour of the M-side").

(iii) **Drift law and marking.** The 23 localizing disks admit a certified marking: their centers are distributed over six bands of angular size with proved gaps, and the address "band, number" is injective. For the two real zeros the signs of the increments (negative) on five transitions of finite levels are certified, together with the bounds |ε_m| ≤ 2.9×10⁻⁵ at the numerical constant c₂ (drift law, Theorem 4).

Statements (i)–(iii) are results about the function H constructed with the certified literal AU₀; as such they are unconditional, and only the interpretation of the calibration normalization (§2.4, §8) is conditional.

All results are obtained in the sense of a computer-assisted proof, with rigorous interval arithmetic (512 bits) and directed rounding.

Finally, section 7 gives **numerical evidence (not a rigorous result; one frozen run, 22/23)**: numerically — without a rigorous certificate, but checked without free parameters — it has been established that the zeros of H are δ-scaled limit positions of superstable parameters of the quadratic family near the Feigenbaum point (the renormalization-group picture — Feigenbaum 1978/79, Coullet–Tresser 1978; for d = 2 — Milnor 1989, Lyubich 1999); the present article treats only the special case d = 2, and the inter-class verification (d = 4, 6) is a separate work [companion]. The frozen experiment gives 22 matches out of 23 catalogue positions under mandatory verification of exact period — the acceptance rule and all parameters were fixed before the computation; this result was obtained in a single frozen numerical run, has no independent reproducibility outside the author's pipeline, and carries no certificate. The early runs of the experiment that used an erroneous calibration, and the reason their results are not evidence, are set out in section 7.5 and in Appendix F.

Along the way, in explicit form for our normalization, the classical coordinate mode of the doubling operator is written out (eigenvalue α²; Appendix D).

---

## 1. Introduction: the period-doubling cascade and the two constants

Let a family of maps of an interval — say, x → r·x·(1−x) — depend smoothly on a parameter. As the parameter grows, the stable cycle of length 1 is replaced by a cycle of length 2, then 4, 8, 16; the parameter values at which the doublings occur accumulate to a limit geometrically, with ratio

    δ = 4.669201609102990671853203820466…

M. Feigenbaum (1975–1978) discovered that δ does not depend on the choice of family: it is a universal constant — the same for the logistic family, for the sine family, and for any smooth family with a quadratic maximum, under standard regularity and transversality conditions of the family to the stable manifold of the renormalization. The second universal constant

    α = −2.5029078750958928…

describes by how many times the geometry of the orbit near the critical point compresses at each doubling. The sign here is a matter of convention: in Appendix D, where the coordinate mode is derived (Proposition 5), the opposite convention α > 0 is more convenient, and it is stated there explicitly. The sign has no effect on α², the only combination that enters our claims.

The renormalization-group explains the universality. The doubling operator

    (T f)(x) = −α · f(f(−x/α))

has a fixed point g satisfying the Cvitanović–Feigenbaum equation g(x) = −α·g(g(−x/α)). This fixed point is hyperbolic: the linearization has exactly one expanding eigenvalue, equal to δ, with eigenfunction h. The existence and properties of g have been proved rigorously in the classical computer-assisted works, starting with Lanford (1982); we accept them as input and do not re-prove them. The hyperbolicity of the renormalization operator in the complex setting and the complex self-similarity of the Mandelbrot set near the Feigenbaum point are due to Sullivan (1992), McMullen (1994).

*(Informal explanation — Appendix C.1.)*

## 2. The object: the universal family and the function H

### 2.1. Data

We work with certified data for the pair (g, h): polynomial approximations of 100 terms with rigorously proved error radii — 10⁻²⁰ for g and 10⁻²⁷ for h — on the disk |w| < 1 after the change of variable

    w = (x² − 1) / 2.5

All further computations are carried out in ball-interval arithmetic at 512 bits with directed rounding, so that all quantities of the rigorous results are guaranteed intervals. The decimal entries in the text are roundings of their endpoints; the numbers of the non-rigorous section 7 and the conditional asymptotics are marked in place.

### 2.2. The universal perturbed family

We define a one-parameter family through the orbit

    x₀ = 0,   x_{n+1} = g(w_n) + s · h(w_n),   w_n = (x_n² − 1)/2.5

where the perturbation amplitude s is parameterized through the "microscope coordinate":

    s_m(u) = u · AU₀ / δ^m,   AU₀ = 0.414037999086…

The main object of the work is

    H_m(u) = x_{2^{m+1}}(u) / x_{2^m}(u),   H(u) = lim_{m→∞} H_m(u)

The function H_m compares two adjacent scales of the critical orbit: after 2^m steps and after 2^{m+1} steps.

### 2.3. Why the zeros of H are interesting

The equality x_{2^{m+1}}(u) = 0 means that the orbit of the perturbed universal map returns exactly to the critical point in 2^{m+1} steps — a "superstable event" of the universal family. The zeros of the limit H are the universal limit positions of such events: they are tied to no specific family, but describe the renormalization limit itself. Complex zeros extend this picture to the complex range of the parameter.

### 2.4. On the normalization

The condition H(−1) = 0 is a calibration that defines the exact constant AU₀ through the zero itself, not a computational theorem. The computations use the certified decimal literal AU₀ = 0.414037999086…, and it has not been proved that it equals the exact calibration constant. Theorems 1–2 are statements about the function H constructed with this literal AU₀ = 0.41403799908627305889537448439556, and as such they are unconditional; only the interpretation of the normalization (the left zero exactly at −1) is conditional: replacing AU₀ by the exact calibration constant rescales the argument u ↦ u·AU₀/AU₀*, which does not change the number of zeros in the disks as long as the relative correction is smaller than the margin of separation of the zeros from the contours (this estimate is not certified here; see §8, "Status of AU₀"). Therefore the correct formulation for the computed H is: the left zero is rigorously localized in a small disk around −1.

*(Informal explanation — Appendix C.2.)*

## 3. Method of counting zeros

### 3.1. Argument principle and transfer to the limit

The number of zeros of a holomorphic function inside a contour equals the number of revolutions of its image around zero. We compute this number of revolutions (the winding) for a finite level H_m via an arc partition of the circle with rigorous interval envelopes, and then transfer the count to the limit H.

Care is needed in two places.

**First**, the argument principle for H_m itself counts the difference "zeros minus poles"; the poles of H_m are the zeros of the denominator x_{2^m} (the lemma in §5.3(v) shows that these singularities are removable: H_m has no poles).

**Second**, the transfer to the limit is used not as the classical Rouché theorem between two holomorphic functions, but as the **winding-stability lemma**: from the inequality |H − H_m| < |H_m| on the contour Γ it follows that the windings of the images are equal. This is a statement about continuous functions on Γ, and holomorphy is not required at all.

Holomorphy is needed only at the last step — when the winding of the limit H is interpreted as the number of its zeros inside the disk. This is precisely the step that constitutes the content of section 5.

**Simplicity of the zeros is automatic:** the argument principle counts zeros with multiplicity, so a winding equal to one means exactly one simple zero.

### 3.2. Combating interval blow-up

In long compositions the interval envelopes grow parasitically. This gives errors in both directions: both false refusals of the form "the orbit has left the domain", and silently underestimated margins of inequalities. The remedy is an adaptive splitting of the arcs of the contour: in the worst places the arcs were split up to eight times, and all 176 final pieces of the most difficult certificate have a margin above 1.33.

It is worth emphasizing that the second effect is more dangerous than the first. A false refusal is immediately visible; an underestimated margin looks like an honest result, just a little less convincing, and pushes one to weaken the claim where it was not necessary to weaken it.

*(Informal explanation — Appendix C.3.)*

## 4. Identification with the canonical object

All theorems refer to the function H constructed from explicit certified polynomial data (g, h). The bridge to the canonical object — the exact g and h — is built separately and consists of two certificates:

- **interval Newton–Kantorovich in the space of summable sequences**: existence and local uniqueness of the exact fixed point G and the eigenpair (h, δ), with estimates ‖G − g₀‖ ≤ 4.7×10⁻⁶¹, ‖h − h₀‖ ≤ 1.7×10⁻²⁹, |δ| ≥ 4.669201609103;
- **Fréchet-holomorphy certificate** of the doubling operator on the ball around G.

Since 4.7×10⁻⁶¹ is less than 10⁻²⁰, and 1.7×10⁻²⁹ is less than 10⁻²⁷, the exact functions lie inside the very error balls with which the theorems are proved. The bridge closes the main conditionality of the work.

Both certificates were independently verified: double re-run of the verifiers, complete regeneration of both certificates from scratch with byte-for-byte agreement, and three batteries of deliberate corruption (12 + 6 + 3). The first round of verification exposed holes in the verification harness — the absence of a separate verifier for one of the certificates and non-checkable fields; they were closed by new verifiers of 51 and 107 checks, after which all corruptions are caught. The design of this circuit is described in Appendix E.

## 5. Holomorphy of the limit function

This is the central analytical result of the work: it is precisely what makes Theorems 1 and 2 unconditional. The last link of the chain — the absence of zeros of the denominator inside the contours — is certified by a rigorous interval winding (see 5.3(v)). The computer-assisted proof (CAP) methodology for related renormalization problems is due to Eckmann–Koch–Wittwer (1984).

### 5.1. Statement

**To be proved.** The limit function H(u) = lim_{m→∞} H_m(u) is holomorphic in a neighbourhood of each of the 25 closed disks under consideration — these are the 23 certificate disks of the annulus (Theorem 2) and the 2 disks localizing the real zeros in the disk (Theorem 1), and also in a neighbourhood of the closed disk |u| ≤ 7 (Theorem 1). For the disk, the condition |w_n| < 1 of the base orbit is certified on the circle |u| = 7 for the whole tube of radius B (114 arcs, maximum coordinate of the composition ≤ 0.4011 < 1; `09-CODE/archive_inputs/path_to_8/point2_completeness_disk7/pilot_slice_summary.json`), the transfer to the interior is by the same maximum principle as in §5.3(v); the absence of poles is given by the lemma in §5.3(v); the holomorphy of the limit slice slice_∞(u) does not depend on the position of u inside the disk (the tail estimates of §5.3(ii)–(iv) depend only on |t| = |u|·AU₀ ≤ 4.7911, which covers |u| ≤ 11.57 ⊃ {|u| ≤ 7}).

The direct path — controlling the orbit of length 2^m as m grows — does not work: the depth of the telescope doubles with each level, and the accumulated interval blow-up eats any margin. Crucially, the exhaustion of this path is not the exhaustion of the problem: the operator route along the renormalization tower, set out below, remains open and leads to the goal.

### 5.2. The key: the renormalization identity

Denote

    slice_k(u) := T^{k−m₀} f_{s_k(u)},   where f_s = G + s·h,
    F_{m₀}(f) := (T^{m₀} f)(1),   m₀ = 7      (the argument is a function, not a point)

Then

    H_k(u) = F_{m₀}(slice_k(u)) + η_k(u),   |η_k(u)| ≤ 1.6×10⁻³³    (∗)

The meaning of the identity: instead of tracing the orbit of length 2^k, we go up the renormalization tower by k − m₀ steps and apply the same base functional. **The depth drops from 2^m to m.** This is precisely what makes the problem countable.

The algebra of the identity is derived by induction: under the normalization f(0) = 1 and a := f(1), with (Tf)(x) = f(f(ax))/a, we have (Tf)^n(0) = f^{2n}(0)/a, whence x_{2n}(f) = a·x_n(Tf); the factor a in the ratio cancels, which gives H_m(f) = H_{m−1}(Tf). The descent by induction carries this to H_m(f) = H₀(T^m f), and for a normalized function q with q(0) = 1 we have x₁(q) = q(0) = 1 and x₂(q) = q(1), i.e. H₀(q) = q(1). This is exactly what relates the ratio of orbit points to the evaluation of the function at 1.

**Dictionary of notations.** g from §2.2 (variable w = (x²−1)/2.5, expansion in t = 2.5·w = x²−1) and f from the present item (operator (Tf)(x) = f(f(ax))/a, normalization f(0) = 1) are one and the same function in different variables; the dictionary between the notations is given in Appendix D, §1.

The identity (∗) is **not exact**, and this is essential: the normalization is only approximate, because f_s(0) = g(0) + s·h(0) ≠ 1. The resulting term η_k is estimated explicitly and uniformly in k and in u: |η_k| ≤ 1.6×10⁻³³, and it does **not grow with the level** — the amplification δ^(k−m₀) is exactly canceled by the decrease of s_k. The uniformity in k is what allows the passage to the limit: η_k does not accumulate along the tower, so the limit equality H = F_{m₀}(slice_∞) holds with the same estimate 1.6×10⁻³³ — twenty-six orders of magnitude smaller than the additive remainder to the budget (0.87×10⁻⁷, §5.3(iii)). Below, (∗) is written as an equality for readability; this estimate is understood everywhere.

**The estimate of η_k (rigorous).** The quantities involved: `h(0)` — the value of the eigenfunction of the doubling operator at the normalization point x = 0. The Chebyshev series of the data `w33_gh_hiprec.json` is written in the variable t = x² − 1 ∈ [−1, 1] (in the Taylor variable w = t/2.5 used in §2.1, this is w₀ = −0.4); the point x = 0 corresponds to t = −1. Direct computation gives g(0) = 1, h₀(0) = 9.96×10⁻³² (`09-CODE/section5_base_certificates/h1_package_lemma_A/check_gh_at_x0.py`), and the certified bound |h(0)| ≤ ‖h − h₀‖₁ + |h₀(0)| ≤ 1.63×10⁻²⁹ + 10⁻³¹ (`cl34_certificate.json`, `IDENTITY_B.md` §B.4); `s_{m₀} = u·AU₀/δ^m₀` — the perturbation amplitude at the base level, `|s_{m₀}| ≤ |u|·AU₀/δ^7 ≤ 4.7911/δ^7 ≈ 9.9×10⁻⁵` over the 25 disks (T = 4.7911 = AU₀·(u_D + R_ARC) — a conservative upper bound for |t| = |u|·AU₀, `_constants.py`; corresponds to |u| ≤ 11.57 and covers all contours of the work). The scheme: `|η_k(u)| ≤ |s_{m₀}|·|h(0)|` (the factor `δ^{k−m₀}` in `s_{m₀}` cancels as `k` grows, so `η_k` does not grow with the level). Substitution gives `|η_k| ≤ 9.9×10⁻⁵·1.63×10⁻²⁹ ≤ 1.6×10⁻³³` — independently of `k` and `u ∈ D̄`.


### 5.3. Proof scheme

Denote B := 5.44×10⁻⁷ — the tube budget. All estimates of this section and of Theorems 1–2 are formulated for this fixed budget; the certification is carried out for perturbations of exactly this size.

**(i) Holomorphy of the slices.** The dependence u ↦ f_{s_k(u)} is affine. The operator T is Fréchet-holomorphic on the ball B(G, 2.5×10⁻³) — this is a separate certificate with stress tests over the radius: at the enlarged radius 0.01 the check still passes, and at the negative control 0.05 and higher it predictably fails. The whole chain T^j f_{s_k(u)} stays inside B(G, 6.27×10⁻⁴). The composition of holomorphic maps is holomorphic.

**(ii) Convergence of the slices.** The slices form a Cauchy sequence uniformly in u in the space of summable sequences. The accumulated transverse deviation decomposes into a sum of Duhamel layerwise contributions; the contribution of a level r steps away from the base is dominated by an amount of order ratio^r (the closed-form layerwise estimate rests on Lemma W, §5.4) with

    ratio = μ / δ² = 0.016054 < 1

Crucially, the estimate of the contribution does not depend on the depth of the source: adding a deeper level adds one new term without changing the dragging of the existing ones.

**This is a delicate point, and it is worth naming it explicitly.** In the linear approximation the increment of the slice equals the contribution of the new level, and the sum of increments is dominated by a single constant. In the nonlinear case the increment also contains changes to the already accumulated contributions, and the inequality "the difference of the slices is no larger than the tail of contributions" requires a derivation, not a postulate. There is no way around it via the triangle inequality: boundedness of each slice alone only yields an estimate by twice the constant, which does not tend to zero and gives no Cauchy property.

The derivation is closed via the variational equation for the **differences** slice_{k+1} − slice_k — not for the slices themselves — and rests on two facts, one structural and one quantitative. The difference is worth emphasizing, because this is where it is easy to make a mistake: an estimate of the form ‖p_{l+1}‖ ≤ q·‖p_l‖ + C bounds the sequence but does not give convergence; what is needed is an estimate of the increment, and it is given by the telescoping decomposition by levels. The decomposition itself is computed by the certificate and is not written out here; below we give its structure, the quantities involved, and the result. The variational equation for the differences `slice_{ℓ+1} − slice_ℓ` and the complete chain of inequalities are written out in `09-CODE/section5_base_certificates/h1_package_lemma_A/LEMMA_H1.md`, §1, "Step 4 in the nonlinear case — variational equation" (lines 127–146); verifying this specific step requires a line-by-line reading of that file.

**Structural fact.** Let ℓ be the left eigenfunctional of the linearization corresponding to the eigenvalue δ: ℓ∘DT(G) = δ·ℓ, normalization ℓ(h) = 1, ‖ℓ‖_∞ ≤ 1.10486. Then ℓ(DT(G)p) = δ·ℓ(p), and therefore DT(G) preserves the transverse subspace ker ℓ: if ℓ(p) = 0, then ℓ(DT(G)p) = 0. Hence the **linear** dragging generates no unstable component — it leaves zero as zero.

**Quantitative fact.** The nonlinear source does generate it. Let Q(s) be the nonlinear-contribution vector of a level, and Φ(s) = q₂·s² + (M₃‖h‖³/6)·s³ a majorant of its norm, ‖Q(s)‖₁ ≤ Φ(s). The projection onto the unstable direction is then bounded above by:

    |ℓ(Q(s))| ≤ ‖ℓ‖_∞ · ‖Q(s)‖₁ ≤ ‖ℓ‖_∞ · Φ(s)

and it is precisely this majorant that is computed in the certificate. Its supremum over levels, e_star = 1.2453×10⁻⁸, gives the third tail term ‖h‖·e_star/(1 − 1/δ).

So: the linear propagator does **not create** the unstable component, the nonlinear source does, and it is dominated by a separate third term — with its own denominator 1 − 1/δ, slower than the spectral kernel μ/δ² = 0.016. From this the derivation does not collapse, but becomes sharper: where it would be formally simpler to say "is not created", there is an explicit estimate of what exactly is created and at what rate.

**Quantities entering the tail estimate.** μ is the contraction constant of the linearization on the transverse subspace: ‖DT(G)^j P_perp‖₁ ≤ C_s·μ^j with μ = 0.35 and C_s ≤ 5.4959; P_perp = I − h·ℓ is the spectral projector onto the transverse subspace, ‖P_perp‖₁ ≤ 2.808542. The quantity D_star is the supremum over levels k ≥ 8 of the transverse part of the contribution, dragged from the source down to the base m₀ = 7; e_star is the supremum of the ℓ-component of the same contribution, i.e. its drift along the unstable direction. Numerically D_star ≤ 5.1723×10⁻⁸ and e_star ≤ 1.2453×10⁻⁸; both suprema are attained at k = 8.

The price is speed. The conservative estimate gives a Cauchy denominator of 0.654 instead of 0.016: the convergence remains geometric, but substantially slower.

**(iii) Full tail estimate.** Below we give the decomposition scheme, all quantities involved, and the result; the layerwise sums themselves are computed by machine certificate (the closed form is Lemma W, §5.4), and we reproduce here their structure and result, not the step-by-step arithmetic. Each constant entering is listed in Appendix B with its status.

The tail has three terms, not one:

    P_tail(m₀) = P_all + ‖P_perp‖ · D_star + ‖h‖ · e_star/(1 − 1/δ)
               ≤ 2.1135×10⁻⁷ + 1.4527×10⁻⁷ + 1.0033×10⁻⁷ + 1.6×10⁻¹⁴
               = 4.5695×10⁻⁷   <   B = tube budget

The fourth term is the contribution of the error of replacing the exact spectral projector `I − h·ℓ` by `P_perp`, estimated to be of order 1.6×10⁻¹⁴ (see item 11 of section 8); it is inserted explicitly in the inequality and remains negligible relative to the margin 0.87×10⁻⁷. The terms are rounded **upwards** to the fourth place, so their sum is a little larger than the certified upper bound, which equals 4.569368×10⁻⁷. A reader adding up what is printed gets the printed result, and every number shown remains an upper bound.

About the quantity B it should be said plainly: it is not derived, but **imposed**. It is an ℓ¹ tube budget chosen when assembling the base level and hard-coded as a constant into all scripts of domain verification. The substantive claim is that the entire domain certification — the condition |w_n| < 1 and the separation of the denominator from zero on all working arcs — has been carried out **exactly for perturbations of this size**. Therefore the inequality P_tail(m₀) < B is read literally: the accumulated deviation stays inside the region where the orbit condition is certified.

**Lemma (assembly).** If (i) the domain certification (condition |w_n| < 1, separation of the denominator on the contours) has been carried out for all perturbations of the ball of radius B around the base slice and (ii) P_tail < B, then the limit slice lies in this ball and F_{m₀} is holomorphic on it. Condition (i) is certified exactly for B = 5.44×10⁻⁷ (`dom_budget_each` in the tube certificates); if B is changed, certificate (i) must be re-verified.

Note that the two-term form of the estimate — P_all + ‖P_perp‖·D_star ≤ 3.5662×10⁻⁷ (certified value 3.566085×10⁻⁷) — is insufficient: the third term, the drift along the unstable direction, must be taken into account. The margin to the budget is therefore 0.87×10⁻⁷, not 1.87×10⁻⁷ given by the two-term form.

**(iv) Holomorphy of the limit of the slices.** By the Weierstrass theorem for holomorphic functions with values in a Banach space, uniform convergence implies holomorphy of the limit.

**(v) Holomorphy of the base functional.** The functional F_{m₀} is Fréchet-holomorphic on the tube. The proof is by induction along the orbit of length 2^{m₀+1} = 256, at the base level exactly the value of F_{m₀} being certified: each step x_{n+1} = g(w_n) + s·h(w_n) is holomorphic for |w_n| < 1, and the division by x_{2^{m₀}} is legal because the denominator is separated from zero. The condition |w_n| < 1 is certified **on the contour** and for all perturbations of the tube; the transfer to the interior of the closed disk is given by the maximum principle, applicable because for a fixed perturbation w_n is a single holomorphic function of u. The tube is needed only for the envelope of estimates, not for holomorphy.

The separation of the denominator from zero is certified on all **1465 working arcs** of the 25 disks; the worst value of the lower bound is 1.1186×10⁻³ and is attained at the disk of the left real zero (u ≈ −1) — the minimum over the 1465 working arcs of certificate h1pkg (`h1pkg_certificate.json`, field `min_x128_lower`). Separately, `09-CODE/section5_base_certificates/winding/winding_certificate.json` gives a minimum of 1.1166×10⁻³ over the 25 contours of the winding certificate (the `min_x128_lower` analogue); these are different sets of arcs, and both numbers are lower bounds.

**Transfer to the interior of the disk.** What has been said above certifies |w_n| < 1 and |x_{2^{m₀}}| > 0 **on the contour**. For the holomorphy of F_{m₀} on the closed disk we need non-degeneracy of the denominator throughout its interior, and the maximum principle by itself does not give this: it transfers upper bounds inward, but not separation from zero. The missing link — the absence of zeros of the denominator inside the contour — is closed in two steps.

Step one: **rigorous interval certificate of the winding of the denominator of the base slice** — wind(x_{2^m}, Γ) = 0 on all 25 contours (= 25 disks) (Arb, directed rounding; winding-ball radius no higher than 1.2×10⁻²⁴; worst lower bound of |x_{2^m}| on the contour 1.11×10⁻³). For the three disks closed at level m = 8 (Z57, Z60, Z72), the winding is certified at both levels 7 and 8 (at m = 8 the worst bound is 2.3×10⁻³).

Step two: **homotopy transfer from the base slice to the limit.** The denominator is separated from zero on the contour for all perturbations of the tube-ball of radius B (the same 1465 working arcs), the limit slice lies in this ball with margin (P_tail = 4.57×10⁻⁷ < B), and the ball is convex — hence the segment from the base slice to the limit does not leave the ball, the winding along the homotopy does not change and equals zero also for the limit slice. By the argument principle, the denominator of the limit slice has no zeros inside the disks, and the division is legal throughout the interior. Earlier versions of the work relied here on a numerically computed winding; this limitation has been removed (section 8, item 5).

**Lemma (removability of singularities of the ratio).** Let f be an even function, analytic in a region containing the orbit x₀ = 0, x_{n+1} = f(x_n), n < 2^{m+1} (condition |w_n| < 1). Set F := f^{2^m}. Then F is even and analytic in a neighbourhood of zero, F(0) = x_{2^m}, and F(x) − F(0) = x²·φ(x) with φ analytic in a neighbourhood of zero. Since x_{2^{m+1}} = F(x_{2^m}), for small |x_{2^m}| we obtain x_{2^{m+1}} = x_{2^m}·(1 + x_{2^m}·φ(x_{2^m})), i.e. H_m = 1 + x_{2^m}·φ(x_{2^m}). *Consequence.* At a point u₀ where x_{2^m}(u₀) = 0, the ratio H_m has a removable singularity with value H_m(u₀) = 1; H_m has no poles in the region where |w_n| < 1 holds. The same holds for the functional F_{m₀} on the tube (φ depends holomorphically on f). In particular, points of exact period 2^m (u ≈ −δ, −δ², …) are neither zeros nor poles of H_m. The winding certificate of the denominator (below) is therefore not required for holomorphy; it is kept as an independent check of the absence of zeros of the denominator inside the disks.

**(vi) Composition.** H(u) = F_{m₀}(slice_∞(u)) is holomorphic as a composition of holomorphic maps. Q.E.D.


### 5.4. Where the proof is tight

Honest answer: not in the convergence.

The numerical threshold only holds thanks to the auxiliary lemma on the pair invariant (Lemma W), which allows the layerwise estimate to be written in closed form instead of step-by-step recursion. Without it the threshold value does not pass **even with the correct value of the third derivative**: step-by-step recursion gives 3.95×10⁻⁷ against the threshold 3×10⁻⁷, while the closed formula gives 2.11×10⁻⁷.

**Lemma W (pair invariant).** Let `w` be the transverse deviation at the boundary of a pair of renormalization levels, `s` the perturbation amplitude. Then the transverse deviation at the boundary of the pair satisfies `w ≤ C₀·s²` with constant `C₀ = 1000`, and at the intermediate step `w ≤ C₁·s²` with constant `C₁ = 1280`. The proof is by Duhamel expansion: from this `Q_j ≤ QCOEF·s_j²` uniformly over all source levels `k`, and the layerwise estimate is written in closed form. The proof and certification are given in `09-CODE/section5_base_certificates/h1_package_lemma_A/LEMMA_H1.md` (step 1); the certified coefficients are in `level_tail_certificate.py:26-34` (512 bits, directed rounding).

The mean of the three inequalities of this lemma holds with a margin of 0.0507 % to the nominal threshold 1280 — formally this is the tightest place of the whole work; as shown below, the tightness is misleading, and the real margin on this constant is a factor of 2.36:

| inequality | value | bound | margin |
|---|---:|---:|---:|
| first single | 261.0804 | 1000 | 73.89 % |
| **mean** | **1279.3512** | **1280** | **0.0507 %** |
| pair | 936.8487 | 1000 | 6.32 % |

The printed 261.0804/1279.3512/936.8487 are from the rigorous certificates `09-CODE/section5_base_certificates/h1_package_cert_strict/CERT/level_tail_certificate_strict.py` (and the same-named `.json`) (rigorous ‖DT(G)‖₁ = 22.191604188675928, ‖DT(G)²‖₁ = 193.634437825475… from `ndt_rigorous.json`; independent duplicate — `09-CODE/archive_inputs/w36/proj_codex/rigorous_block.json`). The frozen `09-CODE/archive_inputs/w36/audit_codex/level_tail_certificate.py` uses the literals 22.19/193.63 (rounded down, formally not upper bounds) and gives 1279.2777/936.8200; the printed 1279.3512/936.8487 and the resulting P_all, P_tail are from the strict version. The provenance of the remaining constants of Lemma W is `CERT/_constants.py`.

But the tightness here is misleading, and it is important to understand it correctly. The number 1280 is not a threshold dictated by the problem, but a round constant chosen tightly. It enters the final quantity weakly and only through P_all. The dependence has been computed by a separate certificate — on rigorous norms, with its own verifier and corruption battery — and the breaking point is given by an interval fork: at C₁ = 3018 the derivation still passes, at C₁ = 3019 it already fails. Here, at the first mention of this fork, both should be fixed: **the final fork C₁ [3018, 3019]** — for the final derivation; **the intermediate fork (subgoal P_all < 3×10⁻⁷) [3049, 3050]** — for the intermediate subgoal. **The margin on this constant [for the final fork C₁] is a factor of 2.36.**

**Note: the number 3050 corresponds to a different subgoal (P_all < 3×10⁻⁷); the final fork C₁ [3018, 3019] refers to the final derivation.** The number 3050 is arithmetically correct, but measures a different threshold — the breaking of the intermediate subgoal P_all < 3×10⁻⁷, taken without the third tail term; against this subgoal the certified **intermediate fork [3049, 3050]** equals exactly [3049, 3050]. Both values are correct, but answer different questions, and substituting one for the other overstates the claimed margin. This is a special case of the error class analyzed in Appendix E, §3.

### 5.5. Re-certification of inputs

The proof rests on a set of operator-estimate constants. They have all been traced back to the inputs; the result is given in full, including the unpleasant part.

Seven constants — the norm of the second derivative of the operator on its own ball, the norm of the third derivative on its own, the norm of the eigenfunction h (ℓ¹ norm, ‖h‖₁ ≤ 6.33119360069264, as for P_perp and for the layerwise estimates of §5.3), the quadratic coefficient, the norm of the left eigenfunctional ‖ℓ‖_∞ ≤ 1.10486, the norm of the projector ‖P_perp‖₁ ≤ 2.808542, and the spectral-kernel constant C_s ≤ 5.4959 — turned out to be correct upper bounds, taken from rigorous certificates and rounded in the right direction. The construction of the two main certificates was checked separately: the leading block of 100 modes plus an analytic tail cover the whole space, the input and output tails are taken into account, the full degree of output is 19602, rounding is everywhere upwards, the maximum points are indicated.

**Two constants — the norms of the linearization and its square — had no rigorous bound at all.** Their source was a midpoint estimate, which does not give a rigorous bound; the source itself declared this. Moreover, the used value 22.19 turned out to be **smaller** than the computed 22.1916, i.e. the upper bound had been rounded down.

These two quantities have been recomputed rigorously, by two independent implementations with different tail-majorization schemes:

    ‖DT(G)‖    ≤ 22.191604188675928
    ‖DT(G)²‖   ≤ 193.63443782547…

The two computations agreed in sixteen significant digits for the first quantity and in twelve for the second; the larger of the two values, i.e. the more conservative, is used in the calculations. The tail beyond the leading block is taken into account analytically through a weighted majorant and amounts to 2.77×10⁻¹² — it is small by count, not by assumption.

With these rigorous values all inequalities still hold, and the threshold constant 1280 is preserved. Let us emphasize a subtlety essential for reviewing: **the original frozen data file contains a value below the true norm**, and the correctness of the derivation is guaranteed not by this file, but by the fact that all inequalities have been re-checked with the rigorous values and still pass.

**Where ‖DT(G)‖ and ‖DT(G)²‖ are used in §5.3.** The norm ‖DT(G)‖ enters the coefficient of the first single inequality of Lemma W (via `first_single_coeff = (K·‖h‖²/2)/δ²` — uses `K` and `‖h‖`, not `nDT` directly; see `level_tail_certificate.py:29`) and into the intermediate-inequality term `one_coeff = (nDT·C₀ + K·(‖h‖+C₀·s_p)²/2)/δ²` (`level_tail_certificate.py:30`). The norm ‖DT(G)²‖ enters the pair inequality `pair_coeff = (nDT2·C₀ + nDT·K·(‖h‖+C₀·s_p)²/2 + K·(δ·‖h‖+c1_unscaled·s_p)²/2)/δ⁴` (`level_tail_certificate.py:32-33`); also into the DE-matrix quantity `q = (nDT2 + 2·nDT·K·ρ + (K·ρ)²)/δ⁴` (`level_tail_certificate.py:47`), which sets the second bearing speed `√q ≈ 0.654` in the (nonlinear) proof of lemma (a0). The rigorous values (22.191604188675928 / 193.63443782547…) have been re-certified in `09-CODE` (`section5_base_certificates/h1_package_cert_strict/CERT/level_tail_certificate_strict.py/.json`, independent duplicate — `archive_inputs/w36/proj_codex/rigorous_block.json`) — the recalculation of P_all, P_tail and of the final fork C₁ [3018, 3019] gives the same final numbers (P_all ≤ 2.1135×10⁻⁷, P_tail ≤ 4.569368×10⁻⁷ < 5.44×10⁻⁷, margin 2.36×).

## 6. Rigorous results

**Table of claim statuses.**

| Claim | Status |
|---|---|
| T1: two zeros in the disk of radius 7 | CAP theorem (unconditional as a statement about H with the literal AU₀, see §2.4, §8; holomorphy of the limit proved in section 5, including the certified winding of the denominator — 5.3(v)); holomorphy in the disk \|u\| ≤ 7 — by the circle certificate (114 arcs) + the lemma on removability |
| T2: 23 disks in the annulus | the same; unconditional as a statement about H with the literal AU₀; completeness of the annulus is not claimed |
| T3: marking of the disks | rigorous CAP theorem at the band level |
| T4: drift law | signs of the increments and bounds \|ε_m\| ≤ 2.9×10⁻⁵ at c₂ = 0.79028031944… are certified; the coefficient c₂ has the status of a numerical constant (no separate interval certificate; provenance — Appendix B §7); the limit intervals are conditional |
| P5: coordinate mode α² | classical fact (coordinate eigenvalues α^{1−n}: Feigenbaum 1979; Collet–Eckmann–Lanford 1980; Christiansen–Cvitanović–Rugh 1990; Briggs 1994), written out explicitly for our normalization; numerical link G′(1) = −α |
| Section 7: link with the Mandelbrot set | non-rigorous numerical experiment |
| Identification of inputs with the exact G, h | certificates and verifiers have passed independent verification |

**Theorem 1 (the disk |u| < 7).** The function H has in the disk |u| < 7 exactly two zeros, both real and simple: the left one in a disk of radius 1/6 around −1, the right one unconditionally localized in a disk of radius 1/6 around 5.94. The winding on the circle |u| = 7 equals 2 with a margin of 1.55; each zero is separated in its own disk of radius 1/6 with margins 654 (left, u ≈ −1) and 23.7 (right, u ≈ 5.94) respectively. Realness follows from conjugation symmetry.

**Where the winding 2 on |u| = 7 comes from.** The rigorous winding of H₇ on |u| = 7 equals 2 ± 2.52×10⁻²² (`h7_circle_certificate.json`; nested control |u| = 5 gives 1; crude negative control rejected); on each of the 114 arcs of the circle |H₇| > |H − H₇| (`arcwise_rouche_certificate.json`: ratio margin ≥ 1.547, absolute gap ≥ 0.0516) — by the winding-stability lemma the winding of H equals 2; H is holomorphic in the disk (§5.1) and without poles (lemma of §5.3(v)) — hence exactly two zeros with multiplicity; their simplicity and localization come from the two disks of radius 1/6. Assembly check: `verify_disk7_certificate.py`, 22/22.

**Theorem 2 (annulus 7 < |u| < 10).** In each of the 23 certificate disks — radii 0.05 and 0.1, upper half-plane — lies exactly one simple zero of the limit H. Proof: winding equal to one, plus the transfer to the limit in each disk. Twenty disks are closed from the base level m = 7; three required work at level m = 8, i.e. orbits of length 512, with the anchor of the tail majorant at level 7.

The worst per-arc transfer margin over all 25 disks, computed by the closing route actually used for each disk, equals 1.002 and is attained at disk Z66; in the most difficult certificate, where the contour is split into 176 pieces, every piece has a margin above 1.33. The complete table of disks — with centers, radii, margins, and the closing route of each — is given in Appendix A; there we also explain why nine disks have a margin at the base level below 1 and which certificate closes them.

By conjugation symmetry the zeros come in pairs, so altogether in the disk |u| < 10 there are 48 localized zeros.

Completeness of the list in the annulus — that there are no other zeros there — **is not claimed**.

**Fingerprint (definition, verbatim from Appendix A, §1).** arg(x_{2^m}) mod 180°, computed at the exact center; the interval width is of order 10⁻¹¹ degrees, the middle is shown. This is not the polar angle of the center — a quantity of a different nature, and the two must not be confused: for example, at Z72 the fingerprint equals 58.08°, while the polar angle of the position of the zero equals 56.3°.

**Theorem 3 (marking of the disks).** The angular quantity (fingerprint), computed at the exact centers of the disks with interval widths of order 10⁻¹¹ degrees, partitions the 23 disks into 6 bands with proved gaps: the minimum inter-band gap of 3.045° exceeds the maximum intra-band pitch of 2.9075°. The marking of exactly the **chosen centers** of the localizing disks is certified here, not of the zeros themselves.

A non-rigorous observation, given separately and as reconnaissance. A float probe shows that the same partition into six bands is preserved at the level of the envelope of the whole disk: the inter-band gaps remain positive with a minimum of about 1.6°. There is no rigorous interval confirmation of this — the naive tiling blows up, and the non-naive method is not implemented (section 8, item 9). By the same probe it has been obtained that the finer condition — pairwise non-overlap of the fingerprints at the level of the envelopes — **does not hold**: out of 253 pairs of disks the **fingerprint intervals** overlap in 13 (the disks themselves are pairwise disjoint: minimum gap between them 0.0168 — this is float reconnaissance by the centers of the H-side, see Appendix F), and in 10 cases the ordering of the fingerprints inside a band is violated. Injectivity of the address is not affected, since the number is determined by the modulus of the center, strictly monotone inside the band.

**Theorem 4 (drift law).** The signs of the increments and the bounds |ε_m| ≤ 2.9×10⁻⁵ at c₂ = 0.79028031944… are certified; the coefficient c₂ itself has the status of a numerical constant (no separate interval certificate; provenance — Appendix B §7). The positions of the zero at finite levels drift by the law

    z_{m+1} − z_m = −(c₂ · AU₀ / δ^{m+2}) · z_m² · (1 + ε_m)

where c₂ = 0.79028031944… is the quadratic-response coefficient. The certified increments are negative, and on the five proved transitions |ε_m| ≤ 2.9×10⁻⁵. Under the assumption of a geometric rate of decay of the corrections, the limit positions are localized in intervals of width about 3×10⁻⁷; the conditional interval of the right zero is [5.9409360413, 5.9409363308].

The "anomaly" of the rate for the left zero observed in double-precision computations has been rigorously refuted: it is an artifact of float arithmetic.

**Proposition 5 (coordinate mode; a classical fact in explicit form).** Let φ be the evaluation-at-zero functional in the even representation, normalized by the condition φ(G) = 1. Then φ∘DT(G) = c·φ with c = G′(1)/G(1) = α² = 6.264547831217… (independent of the sign of α, see §1), where the prime denotes the derivative with respect to the real variable x. In the notation through X = x² the same constant reads as c = 2G′_X(1)/G(1); the two comes from the chain rule dX/dx = 2x and appears only in the X-notation. The two notations must not be mixed: after the substitution `G(1) = −1/α` we have `G′(1)/G(1) = α²`; doubling this expression, `2·α²`, is a frequent mistake, analyzed in D.§2.2. The same expression in `2G′(1)/G(1)` with `G′(1) = −α` gives `2(−α)/(−1/α) = 2α²` literally, and the notation `c = 2G′_X(1)/G(1)` is more compact, but it must not be mixed with `c = G′(1)/G(1)`.

Let us emphasize that φ is not the same functional as ℓ from section 5: ℓ has eigenvalue δ = 4.669… and normalization ℓ(h) = 1, φ has eigenvalue α² = 6.264… and normalization φ(G) = 1. These are different objects, and the coincidence of the word "functional" in their descriptions is the only thing they have in common.

An essential subtlety: the "naive" form, which is true as an equality of values at the fixed point, gives exactly one half upon differentiation — because of the even representation, the substitution of a number means the substitution of its square, and the missing two comes from differentiating the square.


A structural explanation: the explicit tangent vector to the coordinate family of solutions is N = G − x·G′ in the x-notation, the same N = G − 2X·G′_X in the X-notation, and it satisfies DT(G)N = c·N. This is proved **analytically** (Appendix D, §5): by differentiating the coordinate symmetry g_{c₀}(x) = c₀·g_F(x/c₀) with respect to the parameter, without numerical inputs. The equality c = α² rests on the single numerical link G′(1) = −α, confirmed to about 132 significant digits. The full derivation, including the explicit origin of the missing two, is moved to Appendix D.

**Attribution.** That the coordinate changes x → x + εx^n give eigenvalues α^{1−n} of the doubling operator is a classical fact in explicit form for our normalization: Feigenbaum (1979), Collet–Eckmann–Lanford (1980), Christiansen–Cvitanović–Rugh (1990); Briggs (1994) explicitly uses the term "gauge" for this. The general form for classes |x|^d — [companion], Appendix A, Corollary 3. The original contribution of the present work is the explicit derivation with the "missing two" in the X-notation as a technical detail; we do not claim priority for the identity itself.

## 7. Interpretation: zeros of H and the Mandelbrot set (numerical evidence)

> **Status of the section.** Everything stated below is numerical evidence, not a rigorous result. The quantitative outcomes were obtained by a single frozen computational experiment: one script, all parameters and the acceptance rule fixed before any per-point result was obtained, and every Newton attempt — successful and unsuccessful — written to a machine log. The full protocol of the experiment, including the per-disk tables, is given in Appendix F.

### 7.1. Frame: what is known here and is not our claim

The Mandelbrot set contains the Feigenbaum point c_F = −1.4011551890920506… — the limit of the real period-doubling cascade. The qualitative self-similarity of the set near this point with scaling factor δ is an established result ([12] Milnor 1989; [13] Lyubich 1999; the renormalization-group picture — Feigenbaum 1978/79, Coullet–Tresser 1978). The hyperbolicity of the renormalization operator implies Milnor's "hairiness" conjecture and, in particular, the δ-scaling of the picture of the centers of hyperbolic components. The appearance of a δ-scaled pattern near c_F is expected, and the present work does not claim to discover the fact of its existence itself.

The correspondence "zeros of the function on the unstable manifold ↔ superstable parameters" is a consequence of the universality of the parameter space; the general form for |x|^d and the inter-class verification (d = 4, 6) is a separate work [companion]; the present article uses only the special case d = 2, proved here (Appendix D).

This framing statement will be needed below in the analysis of the methodological episode (§7.4): precisely because self-similarity with factor δ is an established fact, a test built on the self-similar picture must fix the scale independently, otherwise it does not distinguish one "floor" of the picture from a neighbouring one.

### 7.2. Our contribution: from "the pattern exists" to a testable prediction

The contribution is quantitative and constructive (not conceptual):

- an explicit canonical function H whose zeros define the limit pattern in the universal coordinate, not tied to any specific family;
- a rigorously certified catalogue of positions — 23 complex zeros in the annulus and 2 real ones in the disk — with localizing disks, margins, and marking;
- the correspondence constant and the drift law, connecting the universal coordinate with the parameter of the quadratic family and predicting not only the address of each center but also the systematic shift of finite depth of the catalogue, so that the correspondence is checked simultaneously by modulus and by the direction of the residual.

### 7.3. Hypothesis and its verification

**Hypothesis.** The zeros of H are δ-scaled limit positions of the superstable parameters: under the mapping u = A·(c − c_F)·δ^m the superstable parameters of exact period 2^(m+1) converge to the zeros of H.

**The form of the link is derived, not fitted.** A shift is forbidden: u = 0 must correspond to c = c_F, where the perturbation vanishes. The power is pure δ^m without sign alternation (the sign (−1)^m would produce an even-odd alternation purely arithmetically, since c_k − c_F preserves its sign along the main cascade). The single calibration constant A is fixed by the real cascade of superstable parameters:

    L := lim_{k→∞} (c_{k+1} − c_F)·δ^k = 0.4288374984294040681397073391164…
    A  := −1/L = −2.331885629550704132301427374005…

Internal consistency check: with this constant, u(c₁₁), computed at level m = 10, equals −1 with accuracy 1.4214504×10⁻⁸. The same constant has been independently reproduced by a fully independent implementation, which read nothing from the main pipeline, with agreement to the 30th digit. Once A is fixed, the positions of all 23 complex zeros are pure predictions.

**Acceptance rule.** A root found by Newton is counted as a match for a catalogue zero if and only if three conditions hold: (i) Newton has converged, (ii) the root has exact period 2^(m+1) = 2048, and (iii) it lies closer to the predicted point c_pred than the frozen acceptance radius R_accept(c, m) = R_accept(u)/(|A|·δ^m) with R_accept(u) = 0.01. The distance d_u in the universal coordinate is reported only for accepted points; rejected attempts never give a "silent zero". Of these three conditions, the second — the verification of exact period — is not a technical detail; its role is explained separately in §7.4.

**Results.**

- **Catalogue:** 22 out of 23 positions find a superstable partner of exact period 2048 **on the first Newton attempt**; the distances in the universal coordinate range from 2.03 to 3.72×10⁻⁵ with median 3.16×10⁻⁵. The single failure (zero Z72) is analyzed in §7.6.
- **Specificity:** around each zero the local density of superstable roots has been measured. The ratio of "median distance of a random hit in the same region" to "distance of the found partner" is computed **separately for each zero** and for the 22 accepted lies between 986 (Z70) and 8486 (Z02) with median 3713. Let us emphasize that this ratio is not recovered by dividing the extremes of two distributions — the distances themselves lie between 2.03×10⁻⁵ and 3.72×10⁻⁵, while the median distances of a random hit lie between 0.036 and 0.173, but the minimum of one and the maximum of the other are attained on different disks. Z72 stands apart with a ratio of 1.15, i.e. "no better than random": this is a consequence of the local clustering of roots, analyzed in §7.6, and it is included neither in the range nor in the median. Out of 20 control points "not from the catalogue" none was accepted — while 924 of 980 Newton attempts on the controls converged to some root, and 847 of them to a root of **exact** period 2048. The rejection happens by closeness to the prediction, not by the absence of roots: roots are there, and many of them.
- **Rigour of the M-side.** The found partners are not merely numerical objects. For all 23 roots (including the corrected root Z72 of §7.6) existence and uniqueness have been proved by intervals: the Krawczyk operator and interval Newton in ball arithmetic (512 bits) certify that in the box of radius 10⁻²⁷ around each numerical root there lies exactly one parameter c* for which P_c^{2048}(0) = 0, and the lower bounds |P_c^{2^j}(0)| > 0 over the whole box for all j = 0..10 (worst 3.95×10⁻⁴) guarantee the **exact** period 2048. The Krawczyk contraction margin is no worse than a factor of two hundred; the boxes are pairwise disjoint (minimum distance between centers 1.02×10⁻⁸), i.e. these are 23 distinct parameters. The certificate, an independent verifier by a second code path, and a battery of 10 corruptions are in the replication package (`09-CODE`). Thus both ends of each pair exist as theorems: the zero of H in its disk (section 6), the superstable parameter in its box; what remains numerical is the calibration of the mapping u = A(c−c_F)δ^m between them.
- **Vector check against the drift law** — a check simultaneously by modulus and by phase, not just by modulus: a residual of order (2–4)×10⁻⁵ is not noise. The catalogue positions correspond to level 7, and the superstable parameters to the limit, and the difference is predicted by the drift law as the cumulative drift from level 7 to the limit. The ratio of the actual residual to the prediction: median by modulus 0.9635, median phase discrepancy 0.35°, with 19 disks out of 22 having a discrepancy below 1° and the remaining three lying in 1.0–1.5° (per-disk table — Appendix F, §7).

The systematic shortfall to 1 — 0.9635 instead of the expected 0.990 with three tail terms — is not a property of the drift law: the law itself has been confirmed term by term with accuracy about 10⁻⁶ at exactly three terms. The shortfall sits in the bridge between the abstract system H and the real quadratic family: the correspondence formula is only the leading order of universality, and the only available estimate of its accuracy has been withdrawn at |u| around 1, whereas the catalogue lives at |u| from 7 to 10, where the next-order correction gives from 7×10⁻⁷ to 1.2×10⁻⁶ — that is, from 2 to 5 % of the measured effect, systematically and almost in anti-phase. This is a separate systematic error and should be distinguished from the truncation of the drift tail. The secondary source of spread is listed by name: 10 of the 23 localizing disks store the center with only 5–6 significant digits, while the other 13 with 14–16; with a typical effect of about 3×10⁻⁵ the rounding of the low-precision centers gives a spread of several percent. Without [21] the median 0.9635 remains a systematic discrepancy of ~3 %, not explained in the present work.

**Note.**
Continuation of the work on universality classes of other degrees ([companion], [21]) gives grounds for the hypothesis that the drift of levels has a two-layer structure: besides the geometric δ-layer, a sign-alternating layer of the sub-leading essential eigenvalue of the linearization of the doubling operator, λ₂ = −0.123652712552687… (decay ratio 1/|λ₂| ≈ 8.087 per level), is presumptively present. The value λ₂ is **numerically verified on a discretization of the renormalization system with N = 48; the certificate is in [companion]; it is not entered in the registry of Appendix B of the present work**. The comparison of λ₂ = −0.1236… with the spectrum of the doubling operator (Christiansen–Cvitanović–Rugh 1990) and with the essential-spectrum radius is in the companion article. If the purely geometric drift prediction used in this check does not account for the second layer, it would systematically overshoot the residual drift; such a hypothesis — a possible explanation (hypothesis), leaning on the companion article, not a proof — would explain the direction of the shortfall (median 0.9635 < 1) and the sign-alternating contribution to the phase spread. The quantitative decomposition of the number 0.9635 into the contribution of the two-layer model and the contribution of the above-described correction of the correspondence formula is the subject of a separate publication ([companion]); it does not affect the status of the check as evidence (22/23 with controls 0/20).

### 7.4. Why the exact-period check is a load-bearing part of the argument

The self-similarity of the Mandelbrot picture near c_F with factor δ has a direct consequence that makes the exact-period check not cosmetic but logically necessary. The superstable parameters line up along renormalization "layers": the root of exact period 2^(m+1) lies at a radius of order δ^(−(m+1)) from c_F, and at a radius δ times larger lies a self-similar copy of the same pattern, populated by roots of period 2^(m) (and then 2^(m−1), etc.). A root of period 2^(m) trivially satisfies the equation x_(2^(m+1))(c) = 0 (every divisor of a period gives a root of the multiple equation), so Newton, seeking a zero of x_(2^(m+1)), does not distinguish a root of exact period 2^(m+1) from an "inherited" root of period 2^(m) — unless it is told so explicitly.

This danger is not a speculation: it was realized in an early version of the experiment and was discovered post-hoc precisely because that version had no exact-period check (§7.5). Here we fix the principle. A test built on a self-similar picture must fix the scale (i.e. the period) independently of the search procedure. Without this it confirms any "floor", because on every floor the local pattern of superstable centers has the same shape and gives distance statistics of the same order. The exact-period check 2^(m+1) = 2048 is precisely this Newton-independent condition that distinguishes the target layer from neighbouring ones.

### 7.5. Preceding runs and why they are not evidence

The frozen run, whose numbers are printed in §7.3, was not the first attempt. A chain of three runs, the methodological mistake of overriding the negative verdict of run 2 without correcting the cause, and the quantitative analysis of why the "22/23 at 2.4×10⁻⁵" of the early run confirms the δ-self-similarity of the Mandelbrot picture (§7.1), not the testable hypothesis — all this is set out in Appendix F, §8. The numbers of runs 1 and 2 are not admitted as evidence.

### 7.6. An instructive episode: choice of representative

One zero out of 23, Z72, lies near the boundary of the region of applicability of the certified series, and the center of its certificate disk is deliberately shifted by about 0.06 from the zero itself, so that the certificate contour bypasses this boundary (Appendix A, §3.1). In the comparison, as for the rest, the disk center was supplied; within 0.05998 of the predicted point no partner was found, and the direction of the residual disagreed with the drift law by 124°. After substitution of the actual position of the zero the partner is found (distance 2.8×10⁻⁵, ratio to the prediction 0.959, phase discrepancy 0.27°); the zero itself and the partner are each rigorously certified in their own disk/box, and the claim "the zero and the partner coincide" has been rigorously established with accuracy 0.01 (conditional closure, see §8, item 13). This corrected result is not included in the main count 22/23: the acceptance rule was frozen before the computation and operates on the disk centers. Full analysis — in §7.6. **The lesson** is of the same kind as in §7.4: one should compare the positions of the zeros themselves, not the centers of the localizing disks, even when they usually coincide.

### 7.7. What this experiment does not prove

- **Not rigorous.** All computations are directed high-precision arithmetic, not interval certificates; the verdict "22/23" is numerical evidence. A rigorous version of the correspondence (an interval certificate for at least one zero) seems attainable, but is not presented here.
- **One level.** The catalogue describes the limit objects (period 2^∞); the check is performed at one fixed level m = 10 (period 2048) as a sufficiently deep approximation. Convergence of the correspondence in m has not been separately certified — precisely because, as shown in §7.4–7.5, without the exact-period check "convergence in m" measures a shift along the layers rather than the quality of the calibration.
- **Not separated.** A controlled run in which the previous pipeline was restarted with a single change — the corrected constant — has not been carried out. Therefore the contribution of "the corrected calibration" and the contribution of "a more reliable solver and a different acceptance rule" to the success of the final run have not been quantitatively separated. It is only known that (a) the erroneous constant is real and reproducible, and (b) the single decisive defect of the early run — the absence of the exact-period check — is sufficient to accept another layer as one's own.
- **Z72.** The single refusal of the catalogue is an artifact of the substitution of the disk center by the true position (§7.6), not a failure of the hypothesis; but it is honestly not included in the main count 22/23.


## 8. Limitations and open problems

1. **Completeness of the annulus.** It is proved that "in each of the 23 disks there is exactly one zero", but not that "there are no other zeros in the annulus".

2. **Conditionality of the limit asymptotics of the drift.** The geometric-rate hypothesis; on the proved levels it holds, beyond them it is assumed.

3. **Interpretation through the Mandelbrot set — rigorous at both ends, numerical in the calibration.** Both ends of each of the 23 pairs are certified by intervals: the zeros of H by the theorems of section 6, all 23 superstable partners by the Krawczyk/Newton certificate (existence, uniqueness, exact period 2048 in a box of radius 10⁻²⁷; see §7, "Rigour of the M-side"). For Z72, in addition, the zero is rigorously localized in a disk of radius 0.01 centered at the position of the partner (Appendix F, §5). What remains numerical is the mapping between the ends — u = A(c−c_F)δ^m with calibration constants A and c_F; a rigorous estimate of its error (control of higher-order universality corrections) is a separate open problem.

4. **Conjugate zeros** are covered by the symmetry of the construction; a separate machine certificate of symmetry has not been written out.

5. **Rigorous certificate of the winding of the denominator — closed.** In earlier versions the absence of poles of H_m inside the contours relied on a numerically computed winding of the denominator, and this was the only uncertified link in the chain of theorems 1 and 2. The link is closed: the winding of the denominator is certified by intervals on all 25 contours (for disks of level m = 8 — at both levels 7 and 8), and the transfer from the base slice to the limit is given by a homotopy over a convex tube-ball (section 5.3(v)). The item is kept in the list for the history of the question and the stability of reference numbering.

6. **Singularities of H beyond the radius of convergence from zero.** The Taylor series of H at zero "sees" only the nearest singularity. Two independent numerical estimates of its distance from zero give 7.58 (direct localization of the singular point) and 7.566 (radius of convergence by the growth rate of the coefficients); the discrepancy in the third digit reflects the accuracy of both estimates, not the difference of the quantities — theoretically these are the same number. Nothing is known about the singularities **beyond** this radius: the series from zero does not testify about them. Yet all 23 annulus disks lie exactly there. Any "gaps to the singularity" used as a qualitative regularity safeguard therefore measure the distance to the **single known** singularity — a necessary but not sufficient condition.

Note that the proof of section 5 is not affected by this limitation: it does not rest on an expansion from zero, but builds holomorphy through the renormalization tower. The limitation concerns only qualitative arguments about regularity.

7. **Provenance of the dominant constant.** The quadratic coefficient q₂, giving about 69 % of the final quantity, comes from a data set marked as belonging to a rejected strategy. The mark has been analyzed: it refers to the strategy itself — a binary gate on the collinearity of the second derivative with the eigenfunction was failed — and not to the numbers computed in this set. Independently of this, the quantity has been re-certified anew, with a leading block, an explicit count of the far modes, and an analytic majorant of the tail, none of which was in the original set at all; the original value is an upper bound of the new one, i.e. the estimate is more conservative than necessary. In addition, the same quantity has been computed **by a second, independent method** — a contour integral over the parameter instead of automatic differentiation. The leading sums of the two methods agreed in sixteen digits, and the rigorous bound of the contour method was 111.5509172, which exceeds the value of the first method by 1.2×10⁻⁵ and agrees with it in seven significant digits. The two methods have nothing in common except the input coefficients.

The breaking point on this constant has been certified by a separate scan and is given by a fork: at q₂ = 136.4258 the derivation still passes, at q₂ = 136.4844 it already fails. The margin is therefore a factor of 1.22. A warning about the value "about 179", which naturally arises in the same question: it measures the breaking of the intermediate subgoal, not the final derivation, and moreover takes into account only one of the two paths by which q₂ enters the estimate (see Appendix E, §3).

8. **Frozen literals of two norms.** The original data file contains values of the linearization norms below the true ones, i.e. formally not upper bounds. The certificate has been regenerated with rigorous values (section 5.5); the discrepancies are listed line by line. Crucially, the main tail term has **not changed at all** from this replacement — it does not contain these norms.

9. **Envelope marking of the bands.** Theorem 3 certifies band membership for the **centers** of the localizing disks. The claim that the same partition survives the transition to the envelope of the whole disk remains non-rigorous: the naive interval tiling blows up, and the non-naive method is not implemented. Float reconnaissance gives a spread of the fingerprint over the disk of about 1.6–1.8°, which would suffice with a margin, but no rigorous enclosure exists, and therefore the claim "band membership is a property of the zero itself, not of the chosen center" has not been proved today.

10. **Double bookkeeping of names in the original data.** A coarse estimate of the third derivative, obtained via a Cauchy estimate on the Taylor coefficients (Cauchy integral formula), and exceeding the certified one by a factor of 67, is present in three diagnostic scripts; none enters the certified chain. The danger was elsewhere: the source list of one of the certificates listed journal names **without paths**, and files with such names exist in two different places — with a coarse and with a precise value. The correct one was used, but this was not visible from the source list, and on this set of namesakes one quantity, computed by two different constants, was once taken for two different methodologies. References to sources are given in full, the substituted computations are marked as such.

11. **Unestimated projector replacement.** In the layerwise estimates of section 5, the exact spectral projector I − h·ℓ is replaced by P_perp, and the error of this replacement is estimated to be of order 1.6×10⁻¹⁴. This contribution has been inserted explicitly into the final budget: `P_tail = P_all + ‖P_perp‖·D_star + ‖h‖·e_star/(1 − 1/δ) + 1.6×10⁻¹⁴ ≤ 4.569368×10⁻⁷ + 1.6×10⁻¹⁴ < 5.44×10⁻⁷` (see §5.3(iii)). Item 11 is closed: the replacement error has been inserted into the inequality (final formula §5.3(iii): P_tail ≤ 4.569368×10⁻⁷ + 1.6×10⁻¹⁴; Appendix B §4) and remains negligible relative to the margin 0.87×10⁻⁷.

12. **The coefficient c₂ has no separate certificate.** It enters the statement of the drift law (Theorem 4), and the bound |ε_m| ≤ 2.9×10⁻⁵ is defined relative to it. c₂ has the status of a numerical constant (no separate interval certificate; provenance — Appendix B, §7). An interval envelope for c₂ exists, but has been obtained by cross-check, not by an independent certificate. The status of Theorem 4 in the summary table has been adjusted accordingly: "the signs of the increments and the bounds |ε_m| ≤ 2.9×10⁻⁵ at c₂ = 0.79028031944… are certified; c₂ itself is a numerical constant".

13. **Rigorous theorem of the correspondence (zero ↔ parameter pair).** The correspondence "zero of H — superstable parameter" is currently established as follows: each of the two ends of the pair has been certified independently (the zeros of H by the theorems of section 6, the superstable parameters by the Krawczyk/Newton certificate, see item 3), and between them lies the numerical calibration u = A(c − c_F)δ^m. A rigorous theorem of the form "the zero and the partner coincide" is an open problem. A conditional closure has been achieved for one zero, Z72: its own zero is rigorously localized in a disk of radius 0.01 centered at the position of the partner (Appendix F, §5; §7.6), but this closure rests on an independent rigorous localization of the zero itself and does not cover the remaining 22 pairs. Full certification of the correspondence is a separate project.

14. **Status of AU₀.** Theorems 1–2 are statements about the function H constructed with the literal AU₀ = 0.41403799908627305889537448439556, and as such they are unconditional; only the interpretation of the normalization (the left zero exactly at −1) is conditional: replacing AU₀ by the exact calibration constant rescales the argument u ↦ u·AU₀/AU₀*, which does not change the number of zeros in the disks as long as the relative correction is smaller than the margin of separation of the zeros from the contours (this estimate is not certified here).

## 9. Status of computational artifacts

**What the reader holds and what they do not hold.** The present package is self-contained **as a text**: every number that enters the conclusions is given in Appendix B, the complete table of disks is in Appendix A, the full protocol of the numerical experiment is in Appendix F, the complete derivation of Proposition 5 is in Appendix D. All the arithmetic and the logic of the derivation can be checked against them.

The machine artifacts — certificates, verifiers, frozen data, corruption batteries — enter the main part as the **replication package `09-CODE`**: the frozen experiment of section 7, the rigorous localization of zero Z72, the winding bridge of section 5.3(v), the base certificates of winding and assembly H1, the primary input data (2558 files under a checksum manifest), and the restart instructions. The package has been verified by control restarts from the package itself (see below). The replication set of section 5 is part of the package (`09-CODE/section5_base_certificates/`, `09-CODE/section5_winding_bridge/`) and is available to the reader simultaneously with the article. Below we describe which checks have been performed; the design of the verification circuit is in Appendix E.

All certificates, verifiers, and frozen data are gathered with fixed checksums. The entire check is launched by a single command and runs 20 batch checks; the key quantities are additionally reproduced on an independent interval library — 37 out of 37 control values agreed within the tolerances.

Section 7 rests on a single frozen experiment: one script with the parameters and the acceptance rule fixed in the header, the full machine protocol of all attempts, refusals, and controls.

The proof of section 5 is packaged as a separate replication set, assembled so that an external reader can reproduce the main numbers without access to the working materials. It contains: the text of the proof with an exact reference to the source of every number; copies of all frozen input data, covered by a checksum manifest; a regenerated assembly certificate; an independent verifier written to a specification composed before the certificate appeared, and not importing the code of the certificate; a corruption battery; certificates of re-certification of inherited constants; a glossary of notations; a document on the discrepancies with the frozen data and their causes; and an explicit quarantine of all inputs that do not have the status of a rigorous certificate, with an indication of whether anything from them is used in the proof.

This set has passed a blind run: a reviewer, who had not seen either the article or the working materials, reproduced from it by launching all the key quantities — the three inequalities of the auxiliary lemma, P_all, the full tail estimate and the margin to the tube budget — checked the integrity of the manifest, and fired the corruption battery. Separately he tried to break the set: corrupted the input file and verified that the verifier notices this; and independently searched for marks of non-rigor, comparing what he found with the quarantine. The report of the independent verifier and his materials (REPORT_E.md, M3_ADJUDICATION.md, h1_verify_pkg.py) lie in the package at the path `09-CODE/section5_base_certificates/h1_package_verify_E/`.

None of his remarks concern the mathematics. The two substantive ones: the certificate of the dominant quadratic coefficient lies outside the set, although the number itself enters the proof, and in one of the checks the values pass through an intermediate double-precision representation — this does not affect the verdict, since the decisive inequality reads the quantity directly, but in a set devoted to rigor, such an approach is out of place. Both remarks have been accepted.

**Restartability from the package.** The previous edition of this section honestly acknowledged that the materials of the experiment of section 7 are not part of the package and the reader cannot restart it. This limitation has been closed by the package `09-CODE`: when it was assembled, every component was restarted **from the package itself** (from copies in a temporary folder, not from the working archive) — the frozen experiment reproduced the verdict exactly (22/23 matches, median distance 3.158×10⁻⁵, 0/20 false acceptances on the controls), the rigorous localization of Z72, the winding of all 25 contours, the H1 assembly certificate and the winding bridge were regenerated with the same content fields, and the corruption batteries caught all the introduced corruptions under clean control runs. Outside the package remain the working archive of the study (intermediate waves, session logs) and the deep set of section 5 mentioned above.

---

## Contents of the package

| file | contents |
|---|---|
| `01-ARTICLE.md` | this text |
| `02-APPENDIX-A.md` | Appendix A. Complete table of 23 disks: centers, radii, margins, closing routes, bands |
| `03-APPENDIX-B.md` | Appendix B. All constants of the work with status "rigorous / computed / calibration" |
| `04-APPENDIX-C.md` | Appendix C. Informal explanations of key concepts |
| `05-APPENDIX-D.md` | Appendix D. Full derivation of the coordinate mode (Proposition 5) |
| `06-APPENDIX-E.md` | Appendix E. Verification standard and recurring error type |
| `07-APPENDIX-F.md` | Appendix F. Protocol of the numerical experiment of section 7, per-disk tables |
| `08-REFERENCES.md` | Appendix G. References |
| `09-CODE/` | Replication package: code and data of sections 5 and 7, checksum manifest, restart instructions (`README-CODE.md`) |
