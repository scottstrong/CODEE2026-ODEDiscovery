"""Exercise 18: solve each Table 6 equation forward from the first sample of its
settled window, T(t) = T_A + (T0 - T_A) exp(-k t), and score the mean absolute
error against the record.  Compare with the sensor's stated 0.54 F accuracy."""
import numpy as np
from newton import SETTLED, series, fit, newton_constants

print("record   mean absolute error (F)")
for rec in ["A-I", "A-II", "B-I", "B-II", "C-I", "C-II"]:
    T = series(rec, SETTLED[rec])
    k, _, TA = newton_constants(fit(T, 1)[0])
    t = np.arange(len(T))
    T_model = TA + (T[0] - TA) * np.exp(-k * t)
    print(f"{rec:<8} {np.abs(T_model - T).mean():.3f}")
