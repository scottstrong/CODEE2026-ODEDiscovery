# Newton's law of warming and cooling by sparse regression

Data and scripts for Section 5 of the paper (and its exercises in Section 9.6).
Each script is named for the item of the paper it produces.

```
data/temperatures.csv          the record: minute, Sensor I (F), Sensor II (F)
data/raw/                      the untouched instrument exports (see data/README.md)
newton.py                      shared pieces: data, windows, derivative, fits, STLSQ
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
python run_all.py
```

or run any script on its own, e.g. `python table6_recovered_equations.py`.
Every table prints to the terminal at the paper's precision and is also written
to `output/`.

## Conventions the numbers depend on

- Derivatives are finite differences taken **within** each window: centred in the
  interior, first-order one-sided at the two end samples (`numpy.gradient`).
- Fits are plain least squares on `1, T, ..., T^d`; no scaling, no ridge penalty.
  (PySINDy's STLSQ adds a ridge penalty by default; pass `alpha=0` to match.)
- R^2 scores the fit to the estimated derivative T', on the same window.
- STLSQ zeroes every coefficient below the threshold and refits on the survivors
  until nothing changes. The threshold 0.01 is for degrees Fahrenheit and minutes.
- Windows are given in minutes (= sample index) at the top of `newton.py`.
- Table 5's gain column is the difference of the printed (4-decimal) R^2 values.
- Exercise 19(f) recovers the 2 x 2 system exactly only when the sampling resolves
  the fast mode; the script shows both the fine and the one-minute case.

Licence: code MIT, data CC BY 4.0 (see `LICENSE`).
