"""Shared pieces for Section 5: the data, the windows, and the fits done with PySINDy.

Same interface as newton.py in the plain-numpy folder, so the scripts are the
same; only this file differs.  Units are degrees Fahrenheit and minutes.
"""
import warnings
import numpy as np
import pandas as pd
import pysindy as ps
from pathlib import Path

warnings.filterwarnings("ignore", module="pysindy")   # e.g. 'sparsity parameter too big' during the threshold scans

HERE = Path(__file__).parent
OUT = HERE / "output"

# ---------------------------------------------------------------- the data
def load():
    """Two arrays of 116 one-minute samples (minute = index): Sensor I, Sensor II."""
    df = pd.read_csv(HERE / "data" / "temperatures.csv")
    return df["sensor_I"].to_numpy(), df["sensor_II"].to_numpy()

# ---------------------------------------------------------------- the windows
# Minutes are global sample indices, inclusive on both ends.

# The four environments of Table 1.
RUNS = {"A": (74, 115), "B": (12, 29), "C": (30, 73)}   # room, sauna, fridge/freezer

# Red (linear) and purple (extended) windows of Fig. 7 / Tables 3-5.
RED = {"A-I": (81, 102), "A-II": (81, 102),
       "B-I": (17, 27),  "B-II": (17, 27),
       "C-I": (34, 53),  "C-II": (34, 53)}
EXTENDED = {"A-I": (79, 115), "A-II": (78, 115),
            "B-I": (15, 27),  "B-II": (15, 29),
            "C-I": (30, 71),  "C-II": (30, 71)}

# Settled windows of Table 6: fifth minute after each move to the end of the
# environment, except B-I, which stops at 27 (see the Table 6 caption).
SETTLED = {"A-I": (79, 115), "A-II": (79, 115),
           "B-I": (17, 27),  "B-II": (17, 29),
           "C-I": (35, 73),  "C-II": (35, 73)}

RECORDS = ["A-I", "B-I", "C-I", "A-II", "B-II", "C-II"]   # the tables' row order


def series(record, window):
    """Temperature samples of one record ('A-I', ...) over an inclusive window."""
    I, II = load()
    T = I if record.endswith("-I") else II
    a, b = window
    return T[a:b + 1]

# ---------------------------------------------------------------- the pipeline
def sindy(degree, threshold):
    """A PySINDy model with the paper's differentiation, library, and optimizer."""
    return ps.SINDy(
        # centred differences inside the window, first-order one-sided at the ends
        differentiation_method=ps.SINDyDerivative(kind="finite_difference", k=1),
        # 1, T, T^2, ..., T^degree, unscaled
        feature_library=ps.PolynomialLibrary(degree=degree),
        # no ridge penalty (PySINDy's default is 0.05); no extra unbias refit, the
        # last STLSQ pass already is one; SVD solve for the ill-conditioned T^4 columns
        optimizer=ps.STLSQ(threshold=threshold, alpha=0, unbias=False,
                           ridge_kw={"solver": "svd"}))


def derivative(T):
    """T' by finite differences within the window (dt = 1 min)."""
    method = sindy(1, 0).differentiation_method
    return method(T.reshape(-1, 1), np.arange(len(T), dtype=float)).ravel()


def fit(T, degree):
    """Least squares of T' on 1..T^degree (STLSQ at threshold 0).  Returns (beta, R^2)."""
    model = sindy(degree, threshold=0)
    model.fit(T.reshape(-1, 1), t=1.0)
    return model.coefficients()[0], model.score(T.reshape(-1, 1), t=1.0)


def stlsq(T, degree, threshold):
    """Sequentially thresholded least squares.  Returns beta with zeros where eliminated."""
    model = sindy(degree, threshold)
    model.fit(T.reshape(-1, 1), t=1.0)
    return model.coefficients()[0]


def newton_constants(beta):
    """k, tau, T_A from T' = beta0 + beta1 T."""
    k = -beta[1]
    return k, 1 / k, -beta[0] / beta[1]

# ---------------------------------------------------------------- printing
def coef(x):
    return "--" if x is None else f"{x:.4f}"
