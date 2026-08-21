# CODEE2026-ODEDiscovery

Code and data for *Data-driven discovery of canonical models in
undergraduate differential equations education* (CODEE Journal, MS #1123). This repository is the front door. It holds the
Newton warming/cooling study and links each remaining example to the
repository of the author who built it.

## Setup

```bash
git clone https://github.com/scottstrong/CODEE2026-ODEDiscovery
cd CODEE2026-ODEDiscovery
pip install -r requirements.txt
python environment_check.py
pytest -q
```

The paper's numbers were produced with the versions pinned in
`requirements.txt`; the check confirms yours match before anything runs,
and the fourth command recomputes every printed number of the paper's
Sec. 5 from the raw instrument record and asserts it against the
manuscript (`newton_simple/tests/test_paper_numbers.py`, 35 tests).

`gettingstarted/` holds the two on-ramp scripts of the paper's Exercises 1
and 2: `handcalc.py` (the Sec. 3 hand calculation in script form) and
`handcalc_density_pysindy.py` (the data-density experiments).

## What is where

| paper section | code and data |
|---|---|
| Sec. 3 hand calculation | `gettingstarted/handcalc.py` here; the original notebook is in [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |
| Exercises 1-2 getting-started scripts | `gettingstarted/` |
| Sec. 4 logistic (Japan), with the archived `JapanPopulation.csv` | [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |
| Sec. 5 Newton warming/cooling | `newton_simple/` (plain numpy) and `newton_pysindy/` (PySINDy port, identical output), raw and windowed CSVs inside |
| Sec. 6 mass-spring (iOLab) | [mass-spring-SINDy](https://github.com/rainam913/mass-spring-SINDy) |
| Sec. 7 two-tank | [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |
| Sec. 9 exercise datasets (Japan, Italy) | [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |

## One known last-digit difference

Table 5, Run B--I, the incremental $R^2$ column: the paper prints `+0.0328`
and `newton_simple/table5_incremental_r2.py` reports `+0.0327`. The paper's
value is the difference of the two $R^2$ values as printed in Table 4
(0.9937 - 0.9609); the script's is the difference of the underlying unrounded
values (0.03272...). Every other cell agrees under both readings. If you
subtract the printed table and get 0.0328, you have not found an error.

`newton_simple` computes with the paper's own formulas (the Sec. 2 stencils,
STLSQ at alpha = 0, plain numpy); `newton_pysindy` is the same computation
through PySINDy, with the four settings that requires documented inside.
