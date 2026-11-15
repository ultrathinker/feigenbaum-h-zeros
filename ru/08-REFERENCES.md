# Приложение G. Литература

*(Библиографический список оформлен как приложение G и хранится в файле `08-REFERENCES.md`: нумерация файлов сквозная по комплекту, буквенная нумерация — по приложениям, и они не совпадают.)*

## Универсальность Фейгенбаума: открытие и строгие доказательства

1. Feigenbaum M. J. (1978). Quantitative universality for a class of nonlinear transformations. *J. Stat. Phys.* **19**(1), 25–52.
2. Feigenbaum M. J. (1979). The universal metric properties of nonlinear transformations. *J. Stat. Phys.* **21**(6), 669–706.
3. Coullet P., Tresser C. (1978). Itérations d'endomorphismes et groupe de renormalisation. *J. Physique Colloques* **39**(C5), 25–28.
4. Cvitanović P. (ed.) (1984). *Universality in Chaos.* Adam Hilger, Bristol.

## Существование и свойства неподвижной точки ренормализации

5. Lanford O. E. III (1982). A computer-assisted proof of the Feigenbaum conjectures. *Bull. Amer. Math. Soc.* **6**(3), 427–434.
6. Campanino M., Epstein H. (1981). On the existence of Feigenbaum's fixed point. *Comm. Math. Phys.* **79**(2), 261–302.
7. Epstein H., Lascoux J. (1980). Analyticity properties of the Feigenbaum function. *Comm. Math. Phys.* **77**(1), 65–86.
8. Eckmann J.-P., Wittwer P. (1987). A complete proof of the Feigenbaum conjectures. *J. Stat. Phys.* **46**(3–4), 455–477.
9. Collet P., Eckmann J.-P. (1980). *Iterated Maps on the Interval as Dynamical Systems.* Birkhäuser, Boston.
10. Вул Е. Б., Синай Я. Г., Ханин К. М. (1984). Универсальность Фейгенбаума и термодинамический формализм. *УМН* **39**(3), 3–37.

Пункты 5 и 6 — источники, из которых настоящая работа принимает существование, аналитичность и нормировку универсальной функции G и константы α как вход (приложение D, §7). Эти факты здесь не передоказываются.

## Множество Мандельброта, самоподобие и гипотеза волосатости

11. Douady A., Hubbard J. H. (1984–1985). Étude dynamique des polynômes complexes I–II; On the dynamics of polynomial-like mappings. *Ann. Sci. ENS* **18**(2), 287–343.
12. Milnor J. (1989). Self-similarity and hairiness in the Mandelbrot set. *Lect. Notes Pure Appl. Math.* **114**, 211–257.
13. Lyubich M. (1999). Feigenbaum-Coullet-Tresser universality and Milnor's hairiness conjecture. *Ann. of Math.* **149**(2), 319–420.
14. Dudko D., Lyubich M. Local connectivity of the Mandelbrot set at some satellite parameters of bounded type. Препринт.

Пункты 12 и 13 — источник рамочного утверждения раздела 7.1: δ-масштабированное самоподобие множества Мандельброта вблизи точки Фейгенбаума есть установленный результат, и настоящая работа на его открытие не претендует.

## Строгая (валидированная) вычислительная арифметика

15. Johansson F. (2017). Arb: efficient arbitrary-precision midpoint-radius interval arithmetic. *IEEE Trans. Comput.* **66**(8), 1281–1292.
16. Tucker W. (2011). *Validated Numerics: A Short Introduction to Rigorous Computations.* Princeton University Press.
17. Rump S. M. (2010). Verification methods: rigorous results using floating-point arithmetic. *Acta Numerica* **19**, 287–449.

Пункт 15 описывает арифметику типа «середина—радиус», в которой ведутся все строгие вычисления настоящей работы (512 бит, направленное округление). Пункты 16 и 17 — общая методология computer-assisted proof, к которой относится приложение E.

## Координатные («gauge») собственные значения оператора удвоения

18. Collet P., Eckmann J.-P., Lanford O. E. (1980). Universal properties of maps on an interval. *Comm. Math. Phys.* **76**(3), 211–254. DOI: 10.1007/BF02193555.
19. Christiansen F., Cvitanović P., Rugh H. H. (1990). The spectrum of the period-doubling operator in terms of cycles. *J. Phys. A* **23**(14), L713–L717. DOI: 10.1088/0305-4470/23/14/005.
20. Briggs K. M. (1994). Corrections to universal scaling in real maps. *Phys. Lett. A* **191**(1–2), 108–112; arXiv:chao-dyn/9407019. DOI: 10.1016/0375-9601(94)90567-3.

Пункты 18–20 — источники атрибуции §6 таблицы статусов и утверждения 5: то, что замены координат `x → x + ε x^n` дают собственные значения `α^{1−n}` оператора удвоения, — классический факт; Briggs (1994) явно употребляет термин «gauge».

## Статья-компаньон

21. [компаньон] Borzenkov Y. (2026). Явная реализация соответствия «параметр ↔ неустойчивое многообразие» для классов универсальности удвоения периода. Рукопись; препринт будет размещён одновременно с настоящей работой. Используется для атрибуции общей формы утверждения 5 (Приложение A, следствие 3) и для межклассовой проверки §7.1 (d = 4, 6).

## Гиперболичность ренормализации, CAP-методология, высокоточные константы

22. Sullivan D. (1992). Bounds, quadratic differentials, and renormalization conjectures. В сб.: *Mathematics into the Twenty-first Century* (AMS Centennial Publications, vol. 2), American Mathematical Society, Providence, RI, pp. 417–466.
23. McMullen C. T. (1994). *Complex Dynamics and Renormalization*. Annals of Mathematics Studies 135, Princeton University Press.
24. Eckmann J.-P., Koch H., Wittwer P. (1984). A computer-assisted proof of universality for area-preserving maps. *Memoirs Amer. Math. Soc.* 47 (289).
25. Briggs K. (1991). A precise calculation of the Feigenbaum constants. *Math. Comp.* 57 (195), 435–439.

Пункты 22–23 — источники фразы §1 о гиперболичности оператора ренормализации в комплексной постановке и о комплексном самоподобии множества Мандельброта вблизи точки Фейгенбаума. Пункт 24 — методология CAP, на которую опирается раздел 5. Пункт 25 — источник высокоточных многозначных литералов δ, α (приложение B, §1).
