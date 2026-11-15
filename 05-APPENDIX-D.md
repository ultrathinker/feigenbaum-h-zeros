# Appendix D. Coordinate mode (classical fact), explicit derivation for our normalization

**Self-contained appendix.** All definitions are given within; a reader familiar with Banach analysis and the Cvitanović–Feigenbaum renormalization theory can reconstruct the derivation entirely, without resorting to any external materials. The numerical inputs are clearly separated from the analytical steps (§6). The missing two is derived explicitly (§2, the core of the appendix), not postulated.

> **Proposition 5 (coordinate mode; a classical fact in explicit form for our normalization).** Let `φ` be the evaluation-at-zero functional in the even representation, normalized by the condition `φ(G) = 1`. Then `φ ∘ DT(G) = c · φ`, with `c = G′(1)/G(1) = α² = 6.264547831217…` in the notation through the derivative with respect to `x` (equivalently `c = 2G′_X(1)/G(1)` in the notation through `X = x²`), and the same factor `c` is the eigenvalue of the coordinate mode `N = G − x·G′ = G − 2X·G′_X`: `DT(G) N = c · N`.
>
> **Attention to the notation.** The two belongs exclusively to the `X`-notation. The expression `2G′(1)/G(1)` with the derivative with respect to `x` equals `2α²`, not `α²`; mixing the two notations is the most frequent mistake at this point, and §2 is dedicated precisely to it.

In this appendix the symbol of the prime `G′` without a lower index means **the derivative with respect to the real variable `x`** (`dG/dx`); the notation `G′_X` means the derivative with respect to `X = x²` (`dG/dX`). They are connected by the chain rule — and this is exactly where the two lives (§2).

---

## 1. Statement and definitions

**Space.** We work in the Banach space of even functions given by a power series in `w = (X − 1)/2.5`, `X = x²`:

```
v(X) = Σ_{k≥0} v_k · w^k ,   w = (X − 1)/2.5 ,   ‖v‖₁ = Σ|v_k|.       (B = ℓ¹)
```

Evenness is built into the representation: `v(x) := v(X = x²)` automatically satisfies `v(−x) = v(x)`. All the points needed below (`x = 0` ⇒ `X = 0` ⇒ `w = −0.4`; `x = 1` ⇒ `X = 1` ⇒ `w = 0`) lie inside the closed unit disk in `w` (`|w| ≤ 1`), so the series converge absolutely and the rearrangement of sums under composition and differentiation is legal (the convergence has been established by rigorous methods and is accepted as input of the present work — Lanford 1982, Campanino–Epstein 1981).

**Functional and slice.**

```
φ : B → ℝ ,   φ(v) := v(X = 0) = v(x = 0) = Σ_k (−0.4)^k v_k .
M := { q ∈ B : φ(q) = 1 }   (q(0) = 1 — the standard Feigenbaum normalization),
E₀ := ker φ  (tangent space to M).
```

`φ` is continuous: `|φ(v)| ≤ Σ 0.4^k |v_k| ≤ ‖v‖₁`.

**Doubling operator (self-applied form).** The universal fixed point `G` is defined by the self-applied doubling operator — the same form as used in the main text for `δ` and `h`:

```
(T q)(X) := q( q(a² · X)² ) / a ,   a := q(X = 1) = value of q at w = 0.   (T)
```

`G` is its fixed point: `(T G)(X) = G(X)`. Real form: `G(x) = −α · G(G(x/α))`, where `α` is the second Feigenbaum constant. The domain of `T` is `{q : q(1) ≠ 0}` (open); for `G` and its small neighbourhood this is satisfied.

**Constant α and its sign.** The certified data of the pair (G, h) from §2.1 of the main text give

```
α = +2.502907875095892822283902873218…      (positive convention)
λ := G(1) = −0.39953528052313448985758046863369…
```

Self-consistency (one identity, at the point `x = 0`): the normalization `G(0) = 1` and the equation `G(x) = −α·G(G(x/α))` at `x = 0` give `1 = −α·G(G(0)) = −α·G(1) = −α·λ`, i.e. **`λ = G(1) = −1/α`**. This is an ANALYTICAL consequence of the equation and the normalization; numerically it has been confirmed to 159 significant digits — to the full precision of the data (`|G(1) + 1/α|/(1/α) ≈ 1.1·10⁻¹⁵⁹`). We will need this in §2 and §4.

*(For reference: in section 1 of the main text `α` is given with the opposite sign; `α²` is independent of the sign. Below everywhere `α > 0`.)*

---

## 2. CORE OF THE APPENDIX: the missing two

Here we derive what in short formulations is usually simply asserted. In the `X`-notation the eigenvalue equals `c = 2G′_X(1)/G(1)` — with the two. Let us show **where this two comes from** and why "naive" differentiation gives exactly one half.

### 2.1. Source of the two: evenness and the chain rule

The function `G` is even in `x`, and its "natural" variable is not `x`, but `X = x²`. Write `G` as a function of `X`: `G(x) = g(X)`, `X = x²`. Then the derivatives with respect to different variables are related by the chain rule:

```
dG/dx  =  (dg/dX) · (dX/dx)  =  (dg/dX) · 2x .                       (chain)
```

At the point `x = 1` (where `X = 1`):

```
G′(1) [in x]  =  2 · (dg/dX)|_{X=1}  =  2 · G′_X(1) .
```

**This is the whole two:** it comes from `d(x²)/dx = 2x`, evaluated at `x = 1`. This is exactly that "two from differentiating the square" of which the statement of the theorem speaks: *because of the even representation, the substitution of a number means the substitution of its square, and the missing two comes from differentiating the square*. To substitute a number `x` into an even function means to substitute `x²` into the function of `X`; to differentiate with respect to `x` means to go through the chain rule via `x²`, which multiplies by `2x`.

### 2.2. Why the "naive" form gives half

If, when computing the eigenvalue, one differentiates "directly in `X`", forgetting the chain rule (i.e. takes `(dg/dX)(1)/G(1)` instead of `(dG/dx)(1)/G(1)`), one obtains **exactly one half**:

```
c_naive := G′_X(1)/G(1)  =  (1/2)·(dG/dx)(1)/G(1)  =  c/2  =  α²/2 .
```

Numerically (independent recomputation in high-precision arithmetic on the same certified data; `G` is represented by 100 Chebyshev coefficients, the Chebyshev → Taylor conversion in the `w`-basis has been performed anew):

```
G(1)            = −0.39953528052313448985758046863369…   (= −1/α)
(dg/dX)(1)      = −1.25145393754794641114195143660911…
(dG/dx)(1)      = −2.50290787509589282228390287321822…   = 2·(dg/dX)(1)
c := (dG/dx)(1)/G(1)  = 6.26454783121703742510990740759157…   = α²
c_naive := (dg/dX)(1)/G(1) = 3.13227391560851871255495370379578… = α²/2
```

Thus the constant in the `X`-notation is written as `c = 2G′_X(1)/G(1)` (the two explicit), and in the "raw" `x`-notation as `c = G′(1)/G(1)` (the two hidden in the definition of `G′` as the derivative with respect to `x`). This is **one and the same number**; the confusion between the notations is what produces the "naive form gives half" effect. No separate "correction factor 2" is glued onto the derivation — it is simply the chain rule for `X = x²`.

### 2.3. Cross-check of the two derivative conventions

| quantity | notation | value |
|---|---|---|
| derivative with respect to `x` (RAW) | `G′(1) = (dG/dx)(1) = 2G′_X(1)` | −2.5029078750958928… = −α |
| derivative with respect to `X` | `G′_X(1) = (dG/dX)(1)` | −1.2514539375479464… |
| constant, RAW | `c = G′(1)/G(1)` | 6.2645478312170374… = α² |
| constant, `X`-notation | `c = 2G′_X(1)/G(1)` | the same |

Note that `G′(1) = −α` numerically (132 significant digits of coincidence with the certified `α`). This is **not** an analytical identity — it is not derived from the functional equation (see §6), and its precision is limited by the precision of the approximation of `G` (truncation `M = 99`), not by rounding. It is precisely this — the single numerical link — that turns the analytical construction of §3–§5 into the literal `c = α²`.

---

## 3. Fréchet derivative `DT(G) v` (for arbitrary `x`)

Let `v ∈ B`, `f_ε = G + ε·v`. By definition `(DT(G) v)(x) = d/dε[(T f_ε)(x)]|_{ε=0}`. Set `a(ε) = f_ε(1) = λ + ε·β`, `β := v(1)`.

**Inner composition** `p(ε,x) = f_ε(a(ε)·x)`. Differentiating with respect to `ε` (`a′(0) = β`):

```
∂p/∂ε|₀ = G′(λ x)·x·β  +  v(λ x).                                       (3a)
```

**Outer** `Num(ε,x) = f_ε(p(ε,x))`:

```
∂Num/∂ε|₀ = G′(G(λ x))·[ x·β·G′(λ x) + v(λ x) ]  +  v(G(λ x)).          (3b)
```

**Division** by `a(ε)` (quotient rule, `a(0) = λ`):

```
DT(G)v(x) = [ (∂Num/∂ε|₀)·λ − Num(0,x)·β ] / λ² .
```

We use that `G` is a fixed point: `G(G(λ x)) = λ·G(x)` (this is `(T G) = G`, multiplied by `λ`). Then `−Num(0,x)·β/λ² = −G(x)·β/λ`. Next, differentiating the identity `G(x) = G(G(λ x))/λ` with respect to `x`, we obtain the key simplification `G′(x) = G′(G(λ x))·G′(λ x)` (the factors `λ` cancel), so `x·G′(G(λ x))·G′(λ x) = x·G′(x)`. Collecting:

```
DT(G) v (x) = (1/λ)·[ v(G(λ x)) + G′(G(λ x))·v(λ x) ]
              + (β/λ)·[ x·G′(x) − G(x) ].                                 (3c, RAW)
```

Substituting `λ = −1/α` (i.e. `λ x = −x/α`, `1/λ = −α`) and denoting `N(x) := G(x) − x·G′(x)` (coordinate vector, §5; note `x·G′(x) − G(x) = −N(x)`):

```
DT(G) v (x) = −α·[ v(G(−x/α)) + G′(G(−x/α))·v(−x/α) ]  +  α·v(1)·N(x).   (**)
```

**The first term** is the "main term". **The second** is the correction `+α·v(1)·N(x)`, proportional to `v(1)`. It vanishes identically only when `v(1) = 0`. In particular, exactly at the point `x = 0` both terms containing `v(1)` cancel (see §4), which explains why formulations that work only with `φ` (evaluation at zero) do not notice this correction. Away from zero (when `v(1) ≠ 0`) without it the formula is incorrect.

---

## 4. Identity `φ ∘ DT(G) = c·φ` (Lemma E₀)

**Step 1.** `T` maps the slice `M` to `M` exactly, for any `q ∈ M`: when `q(0) = 1`, `a = q(1)`, `(T q)(0) = q(q(0)²)/a = q(1)/a = a/a = 1`. An algebraic identity, not an approximation.

**Step 2.** Hence `E₀ = ker φ` is invariant under `DT(q)` for any `q ∈ M`: for `v ∈ E₀` the curve `q + ε·v` lies in `M` for all `ε`, its image `(T(q + ε v))(0) = 1` is constant in `ε`, and differentiating at zero gives `φ(DT(q) v) = 0`. In particular for `q = G`.

**Step 3.** `DT(G)` takes `ker φ` to `ker φ`, hence the functional `φ ∘ DT(G)` vanishes on `ker φ`. Linear algebra: a functional that vanishes on the kernel of a nonzero functional `φ` is a multiple of it:

```
φ ∘ DT(G) = c · φ    for some scalar c.                                 (Lemma E₀)
```

**Value of `c`.** Substitute into (**) `x = 0`. We have `N(0) = G(0) − 0·G′(0) = 1`, `G(−0/α) = G(0) = 1`, `v(−0/α) = v(0) = φ(v)`, `v(G(0)) = v(1) = β`. Then:

```
DT(G)v(0) = −α·[ v(1) + G′(1)·φ(v) ]  +  α·v(1)·1
          = −α·G′(1)·φ(v).      (terms with v(1) = β cancel: −α·β + α·β = 0)
```

Since `DT(G)v(0) = φ(DT(G) v)`, comparison with `φ(DT(G)v) = c·φ(v)` gives

```
c = −α·G′(1) = G′(1)/λ = G′(1)/G(1)   (RAW; = 2G′_X(1)/G(1) in X-notation).
```

The two `2` in the `X`-notation is exactly the chain rule of §2 (`G′(1) = 2G′_X(1)`). So `φ ∘ DT(G) = c·φ` for **any** `v ∈ B`, entirely algebraically, without numerical inputs. The value of `c` as a **number** is discussed in §6.

---

## 5. Coordinate mode: `DT(G) N = c·N`

### 5.1. Where the family of solutions comes from

The equation `G(x) = −α·G(G(x/α))` is the normalized (`G(0) = 1`) case of the **unnormalized** Cvitanović–Feigenbaum equation

```
g(x) = −α · g( g(x/α) ).                                                 (CF-un)
```

If `g_F` is a solution, then for **any** `c₀ ≠ 0` the function `g_{c₀}(x) := c₀ · g_F(x/c₀)` is also a solution. The check is a pure substitution:

```
−α·g_{c₀}(g_{c₀}(x/α))
   = −α·c₀·g_F( g_{c₀}(x/α)/c₀ )          [definition of g_{c₀}]
   = −α·c₀·g_F( g_F( x/(c₀ α) ) )          [g_{c₀}(y)/c₀ = g_F(y/c₀)]
   = −α·c₀·( −g_F(x/c₀)/α )               [(CF-un) at argument x/c₀]
   = c₀·g_F(x/c₀) = g_{c₀}(x).            ✓
```

This is the standard coordinate ("gauge") freedom `x ↦ c₀·x` of the equation before imposing the normalization `g(0) = 1` (for `c₀ ≠ 1` we have `g_{c₀}(0) = c₀ ≠ 1`, so only `g₁ = G` satisfies the normalization). No properties of the specific `G` other than that it solves (CF-un) are used; no external reference is needed.

### 5.2. Why `N` is tangent and why the eigenvalue equals `c`

Differentiating `g_{c₀}(x) = c₀·g_F(x/c₀)` with respect to the parameter `c₀` at `c₀ = 1`:

```
N(x) := d/dc₀ [ g_{c₀}(x) ]|_{c₀=1} = G(x) − x·G′(x).                   (N)
```

**Cross-check with the notation `N = G − 2X·G′_X`.** This is the same function: `x·G′(x) [in x] = x·(2x·G′_X) = 2X·G′_X(X)`, so `G(x) − x·G′(x) = G(X) − 2X·G′_X(X)` — literally the formula of the theorem (the two `2` again from `dX/dx = 2x`, §2).

Since `g_{c₀}` is a curve of **fixed points** of the operator `S(f)(x) := −α·f(f(x/α))` ("fixed-α" form; easy to check that `g_{c₀} = S(g_{c₀})` for all `c₀`), differentiating the identity `g_{c₀} = S(g_{c₀})` with respect to `c₀` at `c₀ = 1` gives

```
N = DS(G) · N ,    i.e. N is an eigenvector of DS(G) with eigenvalue EXACTLY 1.
```

This is a trivial consequence of the continuous coordinate symmetry ("marginal mode"). But `S` is the operator with fixed `α`, not the self-applied `T` (where `a = q(1)` changes under variation). Their connection is given by the formula of §3: the main term (**) for an even `v` coincides with `DS(G)v` (here it suffices that `λ x = −x/α`). Since `N` is even (`x·G′(x)` is a product of two odd functions), substitute `v = N`:

```
DT(G) N(x) = DS(G)N(x) + α·N(1)·N(x) = N(x) + α·N(1)·N(x) = (1 + α·N(1))·N(x).   (5.1)
```

**Algebraic simplification** `1 + α·N(1) = c`:

```
N(1) = G(1) − 1·G′(1) = λ − G′(1),
α·N(1) = α·λ − α·G′(1) = −1 − α·G′(1),           [α·λ = α·(−1/α) = −1]
1 + α·N(1) = −α·G′(1) = G′(1)/λ = c.             [−α = 1/λ;  c = G′(1)/λ from §4]
```

In total

```
DT(G) N (x) = c · N(x)   for all x,                                        (T-mode)
```

with the **same** `c = G′(1)/G(1)` as in §4 (not a new number). Proved analytically: (i) direct substitution — `g_{c₀}` solves (CF-un) for all `c₀` (§5.1); (ii) differentiation of this identity with respect to the parameter (§5.2); (iii) the Fréchet-derivative formula of `T` from §3. **Not a single step uses numerical values of the coefficients of `G`** — holds for any even function that satisfies (CF) and (CF-un) with the same `α`.

Structural outcome: `α²` is the eigenvalue of the coordinate mode `N`, and the identity for `φ` is its dual (left-eigenvector) form. The "two theorems" (about `φ` and about `N`) share **one** common constant `c`.

---

## 6. The single numerical link: `c = α²`

The construction of §3–§5 gives `c = G′(1)/G(1)` (the same for `φ` and `N`) purely analytically. It remains to show that this **number** equals `α²`. Since `G(1) = −1/α` is an exact analytical consequence (§1, 159 digits), the equality `c = α²` is equivalent to

```
G′(1) = −α.                                                              (★)
```

**This link is numerical, not analytical.** From the functional equation `G(x) = −α·G(G(x/α))` the identity (★) is not derived: differentiating the equation gives `G′(x) = −G′(G(x/α))·G′(x/α)`, and at no point does it close on `G′(1) = −α` (at `x = 0` both sides are zeros of an even function, `0 = 0`, without information). Thus (★) is a specific numerical property of the particular universal function `G`, of the same depth level as its existence itself and the value of `α`.

**Independent cross-check** (560 bits; the same certified data, 100 Chebyshev coefficients; Chebyshev → Taylor conversion in the `w`-basis performed anew, by a separate program):

```
G′(1) [in x]  = −2.50290787509589282228390287321821578638127137672…
α              = +2.50290787509589282228390287321821578638127137672…
c = G′(1)/G(1)=  6.264547831217037425109907407591569949820210471188…
α²             =  6.264547831217037425109907407591569949820210471188…
|G′(1) + α|/α ≈ 2.5·10⁻¹³²        →  (★) holds with accuracy ~132 digits
|c − α²|/α²   ≈ 2.5·10⁻¹³²        →  c = α² with accuracy ~132 digits
```

The coincidence is limited to **132 significant digits** (independent verification by direct differentiation of the Chebyshev series in t — `09-CODE/section5_base_certificates/h1_package_lemma_A/check_gprime_at_1.py`, 132 matching digits), which is less than the full precision of the data (~159 digits for `G(1) = −1/α`, which is analytical). This confirms: (★) is not an exact algebraic identity, but a numerical characteristic of this `G`; the accuracy of 132 digits corresponds to the precision to which the truncated (`M = 99`) approximation reproduces the true `G` (rather than rounding: the relative residual 2.5·10⁻¹³² is by orders of magnitude larger than the arithmetic ball ~10⁻¹⁶⁸). Independent cross-check of `α` with the published high-precision value gives ~130 digits — the same scale.

**Honest conclusion.** To prove `c = α²` "from pure algebra" would mean, in essence, independently re-proving the existence and characterization of the universal `G` and the number `α` — something that has already been done by rigorous computer-assisted methods and accepted as input. This appendix **does not** claim such a proof. It does something different: it reduces Proposition 5 to [fully analytical construction] + [exactly one numerical characteristic `G′(1) = −α`, confirmed to ~132 digits]. The numerical check here is separated from the derivation and is not passed off as a derivation.

---

## 7. Status: what is analytical, what is numerical

**Attribution.** The result as stated is a classical fact in explicit form for our normalization: the substitutions `x → x + ε x^n` give eigenvalues `α^{1−n}` of the doubling operator (Feigenbaum 1979; Collet–Eckmann–Lanford 1980; Christiansen–Cvitanović–Rugh 1990; Briggs 1994 — the last explicitly uses the term "gauge"). The present work considers only the special case d = 2; the general form for classes `|x|^d` and the inter-class verification (d = 4, 6) is a separate work [companion], Appendix A, Corollary 3. We do not claim priority for the identity itself.

**Proved analytically (without numerical inputs):**

- The Fréchet-derivative formula `DT(G)v(x)` of the self-applied operator `T`, for arbitrary `v ∈ B` and `x` — §3, formula (**), with the explicit correction `+α·v(1)·N(x)` to the main term.
- **The missing two** `c = 2G′_X(1)/G(1)` — derived explicitly from `dX/dx = 2x` (`X = x²`) at the point `x = 1`, §2; the "naive" `X`-derivative gives exactly `c/2`.
- `φ ∘ DT(G) = c·φ` for any `v`, `c = G′(1)/G(1)` — §4 (Lemma E₀).
- `DT(G)N = c·N` for all `x` — §5 (coordinate family `g_{c₀}`, differentiation with respect to the parameter, formula of §3).
- Coincidence of the constants `c` in §4 and §5 — §5.2, pure algebra.
- `G(1) = −1/α` — an exact consequence of the normalization and the equation, §1 (159 digits).

**Remains numerical (not derived analytically):**

- `G′(1) = −α`, equivalent to `c = α²`, — §6. Confirmed to ~132 significant digits (independent recomputation on the certified data; separately — a finite-difference reverification of the formulas of §3–§5 to 74–84 digits). This is the single numerical link of the entire construction.

**Accepted inputs** (not re-proved either here or in the main text): existence, analyticity, and normalization of the universal `G` and the constant `α` (rigorous computer-assisted proofs, Lanford 1982, Campanino–Epstein 1981); convergence and correctness of the composition of series for `T` in the disk `|w| ≤ 1`.

**Attribution.** The statement of Proposition 5 in the main text leaves priority and the exact reference open: the identity is rooted in the classical structure of the renormalization equation, and we do not claim it as a new independent fact. The coordinate freedom `x ↦ c₀ x` (§5.1) is proved here by direct substitution and does not require external attribution. The novelty of the present appendix is in the explicit derivation, not in the identity itself.
