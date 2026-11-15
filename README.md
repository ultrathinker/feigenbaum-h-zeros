# Zeros of the universal scaling function of the period-doubling cascade

**Yevhen Borzenkov** · ORCID [0009-0002-7946-589X](https://orcid.org/0009-0002-7946-589X)
Preprint, version 2.5 (frozen 16.08.2026), not peer-reviewed. Public edition 15.11.2026.
Русская версия — [README.ru.md](README.ru.md).

Rigorous computer-assisted localization of zeros of the universal function H(u) of the Feigenbaum
period-doubling cascade (quadratic class, d = 2), holomorphy of the limit H = lim H_m, and a
numerical link between the zeros of H and superstable parameters of z² + c near the Feigenbaum point.

## Main results

Rigorous (computer-assisted proof, 512-bit interval arithmetic with directed rounding, python-flint / Arb):

- exactly two zeros of H in the disk |u| < 7, both real and simple;
- exactly one simple zero in each of 23 certificate disks in the annulus 7 < |u| < 10
  (46 zeros with conjugates, 48 localized zeros in |u| < 10; completeness in the annulus is **not** claimed);
- holomorphy of the limit function H on |u| < 7 and near every closed disk used;
- existence and uniqueness of all 23 superstable parameters of exact period 2048 of z² + c in boxes of radius 10⁻²⁷
  (Krawczyk operator, interval Newton);
- certified marking of the 23 disks into six bands and the drift law on five transitions of finite levels.

Numerical, **not** rigorous: in one frozen run (all parameters fixed in advance) the zeros of H match δ-scaled
superstable parameters in 22 of 23 cases, with 0 of 20 controls.

The object and the qualitative picture go back to Milnor (1989); this work adds the rigorous computational
layer. Prior work and attribution are in §1 and Appendix G.

## Repository layout

| Path | Contents |
|---|---|
| [`00-README.md`](00-README.md) | Package overview: what is proved and what is not, notes for the referee |
| [`01-ARTICLE.md`](01-ARTICLE.md) | Main article |
| `02-APPENDIX-A.md` … `07-APPENDIX-F.md` | Appendices A–F (disk table, constants, explanations, coordinate mode, verification standard, experiment protocol) |
| [`08-REFERENCES.md`](08-REFERENCES.md) | Appendix G, references |
| [`09-CODE/`](09-CODE/) | Replication package: code, certificates and data of sections 5 and 7, `MANIFEST.sha256`, instructions in [`09-CODE/README-CODE.md`](09-CODE/README-CODE.md) |
| [`ru/`](ru/) | Russian version of the article and appendices (the code in `09-CODE/` is shared) |
| [`PUBLICATION-NOTES.md`](PUBLICATION-NOTES.md) | What was changed in the package for this public edition |

## Reproducing

Python 3.13, `python-flint` 0.9.0, `mpmath` ≥ 1.3. The frozen scripts address their inputs by an absolute
path, so a rerun starts with reconstructing the tree:

```
python 09-CODE/_tools/rebuild_layout.py <TARGET>
```

then follow the routes in [`09-CODE/README-CODE.md`](09-CODE/README-CODE.md) §4–§6. Quick checks:

```
python 09-CODE/_tools/verify_manifest.py        # integrity of every file of the package
python 09-CODE/_tools/check_article_paths.py    # every path cited in the texts exists
```

Expect one documented sha256-pin mismatch on `x4_common.py` in the verifiers; it is explained in
[`PUBLICATION-NOTES.md`](PUBLICATION-NOTES.md) and does not affect the mathematics.

## Use of AI tools

The computations, code and text were prepared with the help of AI tools; every claim marked rigorous rests
on an interval-arithmetic certificate that is reproduced by the code in this repository.

## Related work by the author

- Companion paper on universality classes d = 2, 4, 6 (reference [companion] in Appendix G) — in preparation.
- Hyperbolicity of period-doubling renormalization at non-integer critical exponent ℓ ∈ [2, 4] —
  Zenodo, DOI [10.5281/zenodo.22306911](https://doi.org/10.5281/zenodo.22306911).

## Citation and license

Citation metadata — [`CITATION.cff`](CITATION.cff). License — MIT ([`LICENSE`](LICENSE)), for code, data and text.
