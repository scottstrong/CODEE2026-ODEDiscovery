"""Exercise 19: a thermometer has two time scales.

(e) Fit T(t) = T_env + f D exp(-t/tau_fast) + (1-f) D exp(-t/tau_slow) to Run C,
    simulate that record on the instrument's 0.1 C grid, and pass it through the
    Section 5 pipeline; compare the quadratic gain with Table 5.
(f) Simulate the two-state system with both states observed and run STLSQ on it.
    The 2 x 2 system comes back exactly when the sampling resolves the fast mode;
    at one-minute sampling with finite differences it does not.
"""
import numpy as np
from scipy.optimize import curve_fit
from scipy.linalg import expm
from newton import RUNS, EXTENDED, series, fit, derivative

def two_exp(t, T_env, D, f, tau_fast, tau_slow):
    return T_env + f * D * np.exp(-t / tau_fast) + (1 - f) * D * np.exp(-t / tau_slow)

def to_grid(T):
    """Round to the instrument's 0.1 C grid, then back to F."""
    return np.round((T - 32) * 5 / 9, 1) * 9 / 5 + 32

# ---- (e)
print("(e) Run C, two-exponential fit and the simulated record through the pipeline")
for rec in ["C-I", "C-II"]:
    T = series(rec, RUNS["C"])
    t = np.arange(len(T), dtype=float)
    p, _ = curve_fit(two_exp, t, T, p0=[T[-1], T[0] - T[-1], 0.2, 1.0, 13.0])
    T_env, D, f, tau_fast, tau_slow = p
    print(f"  {rec}: tau_fast = {tau_fast:.2f} min, tau_slow = {tau_slow:.1f} min, fast fraction {f:.2f}")

    n = EXTENDED[rec][1] - EXTENDED[rec][0] + 1
    T_sim = to_grid(two_exp(np.arange(n, dtype=float), T_env, D, f, 1.1, 13.0))
    _, r2_lin = fit(T_sim, 1)
    _, r2_quad = fit(T_sim, 2)
    _, m_lin = fit(series(rec, EXTENDED[rec]), 1)
    _, m_quad = fit(series(rec, EXTENDED[rec]), 2)
    print(f"        simulated: linear R2 {r2_lin:.4f}, dR2(quad) {r2_quad - r2_lin:+.4f}"
          f"   measured (Table 5): {m_lin:.4f}, {m_quad - m_lin:+.4f}")
    _, r2_lin5 = fit(T_sim[5:], 1)
    _, r2_quad5 = fit(T_sim[5:], 2)
    print(f"        simulated, first five samples dropped: dR2(quad) {r2_quad5 - r2_lin5:+.4f}")

# ---- (f)
print("\n(f) Two-state system u1' = -a u1 + a u2,  u2' = b u1 - (b+c) u2, both states observed")
a, b, c = 0.85, 0.05, 0.08                     # eigenvalues give tau_fast ~1.1, tau_slow ~13
A = np.array([[-a, a], [b, -(b + c)]])
print(f"    true: u1' = {-a:+.4f} u1 {a:+.4f} u2,   u2' = {b:+.4f} u1 {-(b+c):+.4f} u2")

def stlsq_two_state(dt, minutes=42, threshold=0.01):
    t = np.arange(0, minutes, dt)
    U = np.array([expm(A * ti) @ [80.0, 40.0] for ti in t])      # start above ambient
    u1, u2 = U[:, 0], U[:, 1]
    X = np.column_stack([np.ones_like(u1), u1, u2, u1**2, u1 * u2, u2**2])
    names = ["1", "u1", "u2", "u1^2", "u1u2", "u2^2"]
    for label, du in [("u1'", np.gradient(u1, dt)), ("u2'", np.gradient(u2, dt))]:
        keep = np.ones(6, dtype=bool)
        while True:
            beta = np.zeros(6)
            beta[keep] = np.linalg.lstsq(X[:, keep], du, rcond=None)[0]
            new_keep = np.abs(beta) >= threshold
            if (new_keep == keep).all():
                break
            keep = new_keep
        terms = "  ".join(f"{beta[i]:+.4f} {names[i]}" for i in range(6) if beta[i] != 0)
        print(f"    dt = {dt:<5} {label} = {terms}")

stlsq_two_state(dt=0.01)
stlsq_two_state(dt=1.0)
