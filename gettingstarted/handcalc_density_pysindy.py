"""Exercise 2: edit the data and watch the discovered equation respond.

The warmup problem x' = x fit with PySINDy's own routines, library {x, x^2}
(no constant column), under three data edits:

  (a) fix dt = 1 and extend the record: 3 points -> 100 points. At the
      script's threshold of 0.1 the recovered coefficient crawls from 0.863
      to 0.878 and stalls; the per-sample derivative error is set by the
      spacing, not by how many samples follow.
  (b) fix the window [0, 3] and refine the sampling. The same coefficient
      marches from 0.863 to 1.000: denser data helps when the window does
      not shrink with it.
  (c) the hand calculation itself, ported. At threshold 0.001 the original
      three points return 1.1246 x - 0.0388 x^2, not the by-hand
      (1.5724, -0.1275): PySINDy's differentiator defaults to second-order
      one-sided endpoint formulae where the paper's stencils are
      first-order. Exercise 9 derives the second-order formulae.
"""
import numpy as np
import pysindy as ps

def fit(t, threshold):
    X = np.exp(t).reshape(-1, 1)
    m = ps.SINDy(
        feature_library=ps.PolynomialLibrary(degree=2, include_bias=False),
        optimizer=ps.STLSQ(threshold=threshold),
    )
    m.fit(x=X, t=t)
    return np.asarray(m.coefficients())[0]

print("(a) dt = 1, extend the record (threshold 0.1):")
for N in [3, 5, 10, 25, 50, 100]:
    c = fit(np.arange(0, N, 1.0), 0.1)
    print(f"    N = {N:>3}:  x' = {c[0]:.4f} x {c[1]:+.4f} x^2")

print("\n(b) window fixed at [0, 3], refine the sampling (threshold 0.1):")
for dt in [1, 0.5, 0.25, 0.1, 0.05, 0.01]:
    t = np.arange(0, 3.0 + dt / 2, dt)
    c = fit(t, 0.1)
    print(f"    dt = {dt:>5}:  x' = {c[0]:.4f} x {c[1]:+.4f} x^2")

print("\n(c) the three-point hand calculation at threshold 0.001:")
c = fit(np.array([0.0, 1.0, 2.0]), 0.001)
print(f"    x' = {c[0]:.4f} x {c[1]:+.4f} x^2   (by hand: 1.5724 x - 0.1275 x^2)")
assert abs(c[0] - 1.1246) < 5e-4 and abs(c[1] + 0.0388) < 5e-4
