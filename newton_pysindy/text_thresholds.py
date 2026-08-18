"""The in-text numbers of the STLSQ discussion in Section 5:
  - the Run B-I walkthrough at threshold 0.01,
  - selection of {1, T} on every red, extended, and whole-run window,
  - the threshold plateau on the six settled windows (0.00106 to 0.0748),
  - the range common to the eighteen windows (0.007 to 0.025),
  - the quadratic coefficient Eq. (5.5) predicts from Table 6."""
import numpy as np
from newton import RUNS, RED, EXTENDED, SETTLED, RECORDS, series, fit, stlsq, newton_constants

LINEAR = [True, True, False, False, False]
thresholds = np.logspace(-5, 0.5, 600)


def keeps_linear(T, th):
    return (stlsq(T, 4, th) != 0).tolist() == LINEAR


def edge(T, inside, outside):
    """Bisect between a threshold that keeps {1, T} and one that does not."""
    for _ in range(40):
        mid = (inside + outside) / 2
        if keeps_linear(T, mid):
            inside = mid
        else:
            outside = mid
    return inside


def linear_interval(T):
    """Threshold interval containing 0.01 on which STLSQ keeps exactly {1, T}."""
    ok = np.array([keeps_linear(T, th) for th in thresholds])
    i = np.searchsorted(thresholds, 0.01)
    lo, hi = i, i
    while lo > 0 and ok[lo - 1]:
        lo -= 1
    while hi < len(ok) - 1 and ok[hi + 1]:
        hi += 1
    return (edge(T, thresholds[lo], thresholds[lo - 1]),
            edge(T, thresholds[hi], thresholds[hi + 1]))


print("Run B-I extended window, STLSQ at threshold 0.01, pass by pass:")
T = series("B-I", EXTENDED["B-I"])
for degree, note in [(4, "T^3 and T^4 fall below 0.01 and are removed"),
                     (2, "refit on what remains; T^2 falls below 0.01 and is removed"),
                     (1, "refit on what remains; nothing more is removed")]:
    beta, _ = fit(T, degree)
    print("   ", "  ".join(f"{b:+.4f}" for b in beta), " ", note)
print("    STLSQ returns:", "  ".join(f"{b:+.4f}" for b in stlsq(T, 4, 0.01)))

print("\nTerms kept at threshold 0.01 (1 = kept), degree-4 library:")
whole = {rec: RUNS[rec[0]] for rec in RECORDS}
for name, windows in [("red", RED), ("extended", EXTENDED), ("whole run", whole)]:
    for rec in RECORDS:
        kept = (stlsq(series(rec, windows[rec]), 4, 0.01) != 0).astype(int)
        print(f"    {rec:<5} {name:<10} {kept}")

print("\nThreshold interval on which only {1, T} survive:")
lo_s, hi_s, lo_all, hi_all = 0, 1, 0, 1
for name, windows in [("settled", SETTLED), ("red", RED), ("extended", EXTENDED)]:
    for rec in RECORDS:
        lo, hi = linear_interval(series(rec, windows[rec]))
        print(f"    {rec:<5} {name:<9} {lo:.5f} to {hi:.4f}")
        lo_all, hi_all = max(lo_all, lo), min(hi_all, hi)
        if name == "settled":
            lo_s, hi_s = max(lo_s, lo), min(hi_s, hi)
print(f"  common to the six settled windows: {lo_s:.5f} to {hi_s:.4f}  (ratio {hi_s/lo_s:.0f})")
print(f"  common to all eighteen:            {lo_all:.4f} to {hi_all:.4f}")

print("\nEq. (5.5): beta2 = -3k / (2 T_A), T_A in degrees Rankine, from Table 6:")
for rec in RECORDS:
    k, _, TA = newton_constants(fit(series(rec, SETTLED[rec]), 1)[0])
    beta2 = -3 * k / (2 * (TA + 459.67))
    print(f"    {rec:<5} beta2 = {beta2:.2e}   threshold/|beta2| = {0.01/abs(beta2):.0f}")
