"""Shared pieces for Section 5: the data, the windows, the derivative, the fits.

Units are degrees Fahrenheit and minutes throughout.
"""
import numpy as np
import pandas as pd
from pathlib import Path

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
def derivative(T):
    """T' by finite differences within the window: centred in the interior,
    first-order one-sided at the two ends (numpy.gradient, dt = 1 min)."""
    return np.gradient(T, 1.0)


def library(T, degree):
    """Feature matrix [1, T, T^2, ..., T^degree]."""
    return np.vander(T, degree + 1, increasing=True)


def fit(T, degree):
    """Ordinary least squares of T' on 1..T^degree.  Returns (beta, R^2)."""
    dT = derivative(T)
    X = library(T, degree)
    beta = np.linalg.lstsq(X, dT, rcond=None)[0]
    resid = dT - X @ beta
    r2 = 1 - np.sum(resid**2) / np.sum((dT - dT.mean())**2)
    return beta, r2


def stlsq(T, degree, threshold):
    """Sequentially thresholded least squares, no ridge penalty.

    Fit, zero every coefficient with |beta| < threshold, refit on the survivors,
    repeat until nothing changes.  Returns beta with zeros where eliminated.
    """
    dT = derivative(T)
    X = library(T, degree)
    keep = np.ones(degree + 1, dtype=bool)
    while True:
        beta = np.zeros(degree + 1)
        beta[keep] = np.linalg.lstsq(X[:, keep], dT, rcond=None)[0]
        new_keep = np.abs(beta) >= threshold
        if (new_keep == keep).all():
            return beta
        keep = new_keep


def newton_constants(beta):
    """k, tau, T_A from T' = beta0 + beta1 T."""
    k = -beta[1]
    return k, 1 / k, -beta[0] / beta[1]

# ---------------------------------------------------------------- printing
def coef(x):
    return "--" if x is None else f"{x:.4f}"
