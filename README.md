# CODEE2026-ODEDiscovery

Code and data for *Canonical models in undergraduate differential equations
education and discovery via regression of sampled and synthetic data*
(CODEE Journal, MS #1123). This repository is the front door. It holds the
Newton warming/cooling study and links each remaining example to the
repository of the author who built it.

## Setup

```bash
git clone https://github.com/scottstrong/CODEE2026-ODEDiscovery
cd CODEE2026-ODEDiscovery
pip install -r requirements.txt
python environment_check.py
```

The paper's numbers were produced with the versions pinned in
`requirements.txt`; the check confirms yours match before anything runs.

## What is where

| paper section | code and data |
|---|---|
| Sec. 3 hand calculation and the getting-started density scripts | [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |
| Sec. 4 logistic (Japan), with the archived `JapanPopulation.csv` | [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |
| Sec. 5 Newton warming/cooling | `newton_simple/` (plain numpy) and `newton_pysindy/` (PySINDy port, identical output), raw and windowed CSVs inside |
| Sec. 6 mass-spring (iOLab) | [mass-spring-SINDy](https://github.com/rainam913/mass-spring-SINDy) |
| Sec. 7 two-tank | [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |
| Sec. 9 exercise datasets (Japan, Italy) | [dgarls/CODEE-SINDyCode](https://github.com/dgarls/CODEE-SINDyCode) |

`newton_simple` computes with the paper's own formulas (the Sec. 2 stencils,
STLSQ at alpha = 0, plain numpy); `newton_pysindy` is the same computation
through PySINDy, with the four settings that requires documented inside.
