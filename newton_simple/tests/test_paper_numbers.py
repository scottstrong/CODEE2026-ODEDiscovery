"""Regression tests: the printed numbers of Section 5 against the raw record.

Every expectation below is a literal transcribed from the manuscript's tables
and in-text claims (MS #1123, revision of 2026-08-20). The tests recompute
everything from ``data/temperatures.csv`` through ``newton.py`` and compare
against those literals -- nothing is read from a stored output file.

Run from the repository root with ``pytest -q`` (pytest.ini sets the path).

The eighteen-window common threshold interval is asserted at 0.007--0.024;
the value 0.025 used in earlier drafts fails on the A-I linear-regime window.

ONE KNOWN LAST-DIGIT DIFFERENCE FROM THE SUBMITTED PAPER.
Table 5, Run B-I, Delta R^2(quad):

    submitted manuscript prints   +0.0328
    this suite asserts            +0.0327

Both are defensible and the difference is confined to that one cell. The
manuscript's value is the difference of the two R^2 values as printed in
Table 4, 0.9937 - 0.9609, which is what a reader subtracting the table gets.
The value here is the difference of the underlying unrounded R^2 values,
0.03272..., which is the true gain. Every other cell of Table 5 agrees under
both readings. We assert the true difference because that is what the code
computes; a reader who subtracts the printed table and gets 0.0328 has not
found an error.
"""
import numpy as np
import pytest

from newton import (RUNS, RED, EXTENDED, SETTLED, RECORDS,
                    load, series, fit, stlsq, newton_constants)

# ----------------------------------------------------------------- helpers

def r4(x):
    return round(float(x), 4)


def keeps_exactly_linear(T, th):
    beta = stlsq(T, 4, th)
    return [b != 0 for b in beta] == [True, True, False, False, False]


# ------------------------------------------------------------ the record

def test_record_shape_and_baseline():
    I, II = load()
    assert len(I) == 116 and len(II) == 116          # 116 one-minute samples
    assert round(I[:12].mean(), 2) == 75.78          # Table 1 room baseline
    assert round(II[:12].mean(), 2) == 74.89


# -------------------------------------------------------------- Table 2

TABLE2 = {  # start, end, dT, samples, (n_red, dT_red), (n_ext, dT_ext)
    "A-I":  (36.50, 74.48,  +37.98, 42, (22, +14.76), (37, +20.52)),
    "A-II": (-0.04, 72.32,  +72.36, 42, (22, +25.74), (38, +40.50)),
    "B-I":  (75.56, 139.60, +64.04, 18, (11, +27.40), (13, +38.90)),
    "B-II": (74.66, 145.60, +70.94, 18, (11, +27.50), (15, +44.30)),
    "C-I":  (117.70, 36.50, -81.20, 44, (20, -41.04), (42, -80.84)),
    "C-II": (122.70, 0.14, -122.56, 44, (20, -57.06), (42, -122.20)),
}

@pytest.mark.parametrize("rec", RECORDS)
def test_table2(rec):
    start, end, dT, n, (nr, dTr), (ne, dTe) = TABLE2[rec]
    T = series(rec, RUNS[rec.split("-")[0]])
    assert (round(T[0], 2), round(T[-1], 2)) == (start, end)
    assert round(T[-1] - T[0], 2) == dT and len(T) == n
    R = series(rec, RED[rec]); E = series(rec, EXTENDED[rec])
    assert (len(R), round(R[-1] - R[0], 2)) == (nr, dTr)
    assert (len(E), round(E[-1] - E[0], 2)) == (ne, dTe)


# ----------------------------------------- Tables 3 and 4, degree-1 rows

DEG1 = {  # (b0, b1, R2) on the red window; same on the extended window
    "A-I":  ((6.6744, -0.0895, 0.9056), (6.1517, -0.0815, 0.9491)),
    "B-I":  ((14.1144, -0.0886, 0.9903), (18.2266, -0.1198, 0.9609)),
    "C-I":  ((2.5696, -0.0771, 0.9969), (4.6053, -0.1190, 0.8893)),
    "A-II": ((5.1537, -0.0682, 0.9915), (6.0064, -0.0813, 0.9655)),
    "B-II": ((16.5282, -0.1048, 0.9800), (22.1845, -0.1462, 0.9536)),
    "C-II": ((-0.2452, -0.0820, 0.9941), (0.7567, -0.1449, 0.8679)),
}

@pytest.mark.parametrize("rec", RECORDS)
def test_degree1_rows(rec):
    for window, want in zip((RED[rec], EXTENDED[rec]), DEG1[rec]):
        beta, r2 = fit(series(rec, window), 1)
        assert (r4(beta[0]), r4(beta[1]), r4(r2)) == want


def test_BI_quartic_row():
    """The degree-4 row quoted verbatim in the Section 5 discussion."""
    beta, r2 = fit(series("B-I", EXTENDED["B-I"]), 4)
    assert [r4(b) for b in beta] == [-1503.6255, 51.1980, -0.6439, 0.0036, -0.0000]
    assert r4(r2) == 0.9984


# -------------------------------------------------------------- Table 5

TABLE5 = {  # linear R2, true Delta R^2 (quad); B-I differs from the
            # manuscript in the last digit -- see the module docstring
    "A-I": (0.9491, +0.0000), "B-I": (0.9609, +0.0327), "C-I": (0.8893, +0.0876),
    "A-II": (0.9655, +0.0248), "B-II": (0.9536, +0.0352), "C-II": (0.8679, +0.1124),
}

@pytest.mark.parametrize("rec", RECORDS)
def test_table5(rec):
    T = series(rec, EXTENDED[rec])
    _, rl = fit(T, 1); _, rq = fit(T, 2)
    assert r4(rl) == TABLE5[rec][0]
    assert r4(rq - rl) == TABLE5[rec][1]


def test_table5_monotone_in_excursion():
    """The quadratic gain is monotone in |dT| on each sensor."""
    for sensor in ("I", "II"):
        recs = [f"{run}-{sensor}" for run in "ABC"]
        gains, spans = [], []
        for rec in recs:
            T = series(rec, EXTENDED[rec])
            _, rl = fit(T, 1); _, rq = fit(T, 2)
            gains.append(rq - rl); spans.append(abs(T[-1] - T[0]))
        order = np.argsort(spans)
        assert list(np.argsort(gains)) == list(order)


# -------------------------------------------------------------- Table 6

TABLE6 = {  # b0, b1, k, tau, T_A, n
    "A-I":  (6.1517, -0.0815, 0.0815, 12.3, 75.53, 37),
    "A-II": (5.5935, -0.0749, 0.0749, 13.4, 74.71, 37),
    "B-I":  (14.1144, -0.0886, 0.0886, 11.3, 159.31, 11),
    "B-II": (16.5300, -0.1048, 0.1048, 9.5, 157.67, 13),
    "C-I":  (2.5921, -0.0771, 0.0771, 13.0, 33.63, 39),
    "C-II": (-0.2557, -0.0812, 0.0812, 12.3, -3.15, 39),
}

@pytest.mark.parametrize("rec", RECORDS)
def test_table6(rec):
    b0, b1, kk, tau, TA, n = TABLE6[rec]
    T = series(rec, SETTLED[rec])
    beta, _ = fit(T, 1)
    k, t, A = newton_constants(beta)
    assert len(T) == n
    assert (r4(beta[0]), r4(beta[1])) == (b0, b1)
    assert (r4(k), round(t, 1), round(A, 2)) == (kk, tau, TA)


def test_ambient_validation():
    """Caption's independent check: Run A ambients vs the unused baseline."""
    I, II = load()
    errs = []
    for rec, base in (("A-I", I[:12].mean()), ("A-II", II[:12].mean())):
        beta, _ = fit(series(rec, SETTLED[rec]), 1)
        errs.append(abs(newton_constants(beta)[2] - base))
    assert [round(e, 2) for e in errs] == [0.26, 0.18]
    assert all(e < 0.54 for e in errs)               # inside sensor accuracy


def test_BI_stops_at_27():
    """B-I's last three nominal-sauna readings justify ending at minute 27."""
    I, _ = load()
    assert [round(x, 1) for x in I[27:30]] == [140.0, 141.8, 139.6]


# ------------------------------------------------- the STLSQ walkthrough

def test_stlsq_walkthrough_BI():
    T = series("B-I", EXTENDED["B-I"])
    beta2, _ = fit(T, 2)                              # after removing T^3, T^4
    assert [r4(b) for b in beta2] == [47.3137, -0.6032, 0.0020]
    final = stlsq(T, 4, 0.01)
    assert [r4(b) for b in final] == [18.2266, -0.1198, 0.0, 0.0, 0.0]


def test_whole_run_selection():
    """STLSQ at 0.01 keeps exactly {1, T} on every whole run, no windowing."""
    for rec in RECORDS:
        T = series(rec, RUNS[rec.split("-")[0]])
        assert keeps_exactly_linear(T, 0.01)


# ------------------------------------------------- the threshold claims

def test_BI_plateau():
    T = series("B-I", EXTENDED["B-I"])
    assert keeps_exactly_linear(T, 0.002)
    assert keeps_exactly_linear(T, 0.119)
    assert not keeps_exactly_linear(T, 0.13)


def test_six_settled_windows_range():
    """Factor-of-seventy claim: 0.00106 to 0.0748 on the six settled windows."""
    for rec in RECORDS:
        T = series(rec, SETTLED[rec])
        assert keeps_exactly_linear(T, 0.00106)
        assert keeps_exactly_linear(T, 0.0748)
    assert 0.0748 / 0.00106 > 70


def test_eighteen_window_interval():
    """0.007--0.024 works on all eighteen windows; 0.0249 breaks A-I red."""
    for windows in (SETTLED, RED, EXTENDED):
        for rec in RECORDS:
            T = series(rec, windows[rec])
            assert keeps_exactly_linear(T, 0.007)
            assert keeps_exactly_linear(T, 0.024)
    assert not keeps_exactly_linear(series("A-I", RED["A-I"]), 0.0249)


# --------------------------------------- the Stefan-Boltzmann detection limit

def test_sb_bound_factor_of_forty():
    """beta2 = -3k/(2 T_A), T_A absolute, lands in [-2.7e-4, -2.1e-4]:
    smaller than the threshold 0.01 by a factor of about forty."""
    preds = []
    for rec in RECORDS:
        beta, _ = fit(series(rec, SETTLED[rec]), 1)
        k, _, TA = newton_constants(beta)
        preds.append(-3 * k / (2 * (TA + 459.67)))    # Rankine
    assert min(preds) >= -2.7e-4 and max(preds) <= -2.1e-4
    factors = [0.01 / abs(p) for p in preds]
    assert 30 < min(factors) and max(factors) < 50
