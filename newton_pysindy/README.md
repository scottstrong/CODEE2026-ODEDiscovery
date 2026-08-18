# Newton's law of warming and cooling by sparse regression — PySINDy variant

The same data and the same scripts as the plain-numpy folder, but the
differentiation, feature library, and STLSQ optimizer come from PySINDy.
Only `newton.py` (and the two-state fit in Exercise 19f) differ; the scripts
that produce each table and figure are identical, and so are the numbers.

```
data/temperatures.csv          the record: minute, Sensor I (F), Sensor II (F)
data/raw/                      the untouched instrument exports (see data/README.md)
newton.py                      data, windows, and the PySINDy model used everywhere
table2_summary.py              Table 2
tables3_4_coefficients.py      Tables 3 and 4
table5_incremental_r2.py       Table 5
table6_recovered_equations.py  Table 6 and its caption
figure7_phase_planes.py        Figure 7
figure8_threshold_scan.py      Figure 8 and the B-I plateau
text_thresholds.py             the in-text STLSQ numbers (walkthrough, plateaus, Eq. 5.5)
exercise18_forward_solve.py    Exercise 18
exercise19_two_time_scales.py  Exercise 19 (e) and (f)
output/                        where the tables (text) and figures (png) are written
```

## Running

```
pip install -r requirements.txt
python run_all.py            # about half a minute; the threshold scans dominate
```

## What is used from PySINDy, and the settings that reproduce the paper

```python
ps.SINDy(differentiation_method=ps.SINDyDerivative(kind="finite_difference", k=1),
         feature_library=ps.PolynomialLibrary(degree=d),
         optimizer=ps.STLSQ(threshold=lam, alpha=0, unbias=False,
                            ridge_kw={"solver": "svd"}))
```

- **Differentiation.** `SINDyDerivative(kind="finite_difference", k=1)` is
  centred inside the window and first-order one-sided at the two end samples,
  which is the paper's stencil. PySINDy's own `FiniteDifference` uses
  second-order one-sided ends and does not reproduce the tables (A-I red-window
  linear fit becomes 6.8872 - 0.0927 T instead of 6.6744 - 0.0895 T).
- **Library.** `PolynomialLibrary(degree)` gives `1, T, ..., T^degree`, unscaled.
- **Optimizer.** `STLSQ` with
  - `alpha=0` — no ridge penalty. PySINDy's default is `alpha=0.05`, which on
    these unscaled features changes every coefficient (A-I settled fit becomes
    about 5.14 - 0.0667 T instead of 6.1517 - 0.0815 T).
  - `unbias=False` — the last STLSQ pass is already a plain least-squares refit
    on the surviving terms, so the extra "unbias" refit is redundant; on the
    unscaled quartic columns it is also numerically unsafe and can zero the fit.
  - `ridge_kw={"solver": "svd"}` — with `alpha=0` the default Cholesky solve of
    the normal equations loses the fourth decimal on the ill-conditioned quartic
    library (B-I extended degree-4 constant comes out -1503.6263, the paper prints
    -1503.6255).
- **Scoring.** `model.score()` is R^2 of the fit to the estimated derivative,
  which is what the tables print.
- Tables 3 and 4 are `STLSQ` at `threshold=0`, i.e. ordinary least squares at
  each degree; Table 6, Figure 8, and the walkthrough use `threshold=0.01` on the
  degree-4 library. Units are degrees Fahrenheit and minutes.

Licence: code MIT, data CC BY 4.0 (see `LICENSE`).
