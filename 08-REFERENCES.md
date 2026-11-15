# Appendix G. References

*(The bibliography is organized as Appendix G and stored in the file `08-REFERENCES.md`: file numbering is sequential across the package, letter numbering is per appendix, and they do not coincide.)*

## Feigenbaum universality: discovery and rigorous proofs

1. Feigenbaum M. J. (1978). Quantitative universality for a class of nonlinear transformations. *J. Stat. Phys.* **19**(1), 25–52.
2. Feigenbaum M. J. (1979). The universal metric properties of nonlinear transformations. *J. Stat. Phys.* **21**(6), 669–706.
3. Coullet P., Tresser C. (1978). Itérations d'endomorphismes et groupe de renormalisation. *J. Physique Colloques* **39**(C5), 25–28.
4. Cvitanović P. (ed.) (1984). *Universality in Chaos.* Adam Hilger, Bristol.

## Existence and properties of the renormalization fixed point

5. Lanford O. E. III (1982). A computer-assisted proof of the Feigenbaum conjectures. *Bull. Amer. Math. Soc.* **6**(3), 427–434.
6. Campanino M., Epstein H. (1981). On the existence of Feigenbaum's fixed point. *Comm. Math. Phys.* **79**(2), 261–302.
7. Epstein H., Lascoux J. (1980). Analyticity properties of the Feigenbaum function. *Comm. Math. Phys.* **77**(1), 65–86.
8. Eckmann J.-P., Wittwer P. (1987). A complete proof of the Feigenbaum conjectures. *J. Stat. Phys.* **46**(3–4), 455–477.
9. Collet P., Eckmann J.-P. (1980). *Iterated Maps on the Interval as Dynamical Systems.* Birkhäuser, Boston.
10. Vul E. B., Sinai Ya. G., Khanin K. M. (1984). Feigenbaum universality and thermodynamic formalism. *Russian Math. Surveys* **39**(3), 1–39.

Items 5 and 6 are the sources from which the present work accepts the existence, analyticity, and normalization of the universal function G and of the constant α as input (Appendix D, §7). These facts are not re-proved here.

## Mandelbrot set, self-similarity and the hairiness conjecture

11. Douady A., Hubbard J. H. (1984–1985). Étude dynamique des polynômes complexes I–II; On the dynamics of polynomial-like mappings. *Ann. Sci. ENS* **18**(2), 287–343.
12. Milnor J. (1989). Self-similarity and hairiness in the Mandelbrot set. *Lect. Notes Pure Appl. Math.* **114**, 211–257.
13. Lyubich M. (1999). Feigenbaum-Coullet-Tresser universality and Milnor's hairiness conjecture. *Ann. of Math.* **149**(2), 319–420.
14. Dudko D., Lyubich M. Local connectivity of the Mandelbrot set at some satellite parameters of bounded type. Preprint.

Items 12 and 13 are the source of the framing statement of section 7.1: δ-scaled self-similarity of the Mandelbrot set near the Feigenbaum point is an established result, and the present work makes no claim to its discovery.

## Rigorous (validated) computational arithmetic

15. Johansson F. (2017). Arb: efficient arbitrary-precision midpoint-radius interval arithmetic. *IEEE Trans. Comput.* **66**(8), 1281–1292.
16. Tucker W. (2011). *Validated Numerics: A Short Introduction to Rigorous Computations.* Princeton University Press.
17. Rump S. M. (2010). Verification methods: rigorous results using floating-point arithmetic. *Acta Numerica* **19**, 287–449.

Item 15 describes the midpoint–radius arithmetic in which all rigorous computations of the present work are carried out (512 bits, directed rounding). Items 16 and 17 give the general methodology of computer-assisted proof to which Appendix E belongs.

## Coordinate (gauge) eigenvalues of the doubling operator

18. Collet P., Eckmann J.-P., Lanford O. E. (1980). Universal properties of maps on an interval. *Comm. Math. Phys.* **76**(3), 211–254. DOI: 10.1007/BF02193555.
19. Christiansen F., Cvitanović P., Rugh H. H. (1990). The spectrum of the period-doubling operator in terms of cycles. *J. Phys. A* **23**(14), L713–L717. DOI: 10.1088/0305-4470/23/14/005.
20. Briggs K. M. (1994). Corrections to universal scaling in real maps. *Phys. Lett. A* **191**(1–2), 108–112; arXiv:chao-dyn/9407019. DOI: 10.1016/0375-9601(94)90567-3.

Items 18–20 are the attribution sources for §6 of the status table and for Proposition 5: the fact that coordinate substitutions `x → x + ε x^n` give eigenvalues `α^{1−n}` of the doubling operator is classical; Briggs (1994) explicitly uses the term "gauge".

## Companion paper

21. [companion] Borzenkov Y. (2026). Explicit realization of the correspondence "parameter ↔ unstable manifold" for universality classes of period doubling. Manuscript; preprint will be released simultaneously with the present work. Used for the attribution of the general form of Proposition 5 (Appendix A, Corollary 3) and for the inter-class verification of §7.1 (d = 4, 6).

## Renormalization hyperbolicity, CAP methodology, high-precision constants

22. Sullivan D. (1992). Bounds, quadratic differentials, and renormalization conjectures. In: *Mathematics into the Twenty-first Century* (AMS Centennial Publications, vol. 2), American Mathematical Society, Providence, RI, pp. 417–466.
23. McMullen C. T. (1994). *Complex Dynamics and Renormalization*. Annals of Mathematics Studies 135, Princeton University Press.
24. Eckmann J.-P., Koch H., Wittwer P. (1984). A computer-assisted proof of universality for area-preserving maps. *Memoirs Amer. Math. Soc.* 47 (289).
25. Briggs K. (1991). A precise calculation of the Feigenbaum constants. *Math. Comp.* 57 (195), 435–439.

Items 22–23 are the source of the §1 statement about the hyperbolicity of the renormalization operator in the complex setting and about complex self-similarity of the Mandelbrot set near the Feigenbaum point. Item 24 is the CAP methodology on which section 5 relies. Item 25 is the source of the high-precision multi-digit literals of δ, α (Appendix B, §1).
