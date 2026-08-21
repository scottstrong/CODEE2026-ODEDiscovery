"""The hand calculation of Sec. 3, in script form (Exercise 1).

Three samples of x' = x, x(0) = 1, at t = 0, 1, 2. Derivatives by the
paper's stencils (forward, centered, backward), library {x, x^2}, one pass
of ordinary least squares through the normal equations.

Convention, matching the manuscript's displays: the walkthrough works from
the four-decimal samples (1, 2.7183, 7.3891) and four-decimal derivative
estimates, forms the normal equations from them, rounds the system to four
decimals, and solves the system *as printed* -- so a reader with a
scientific calculator reproduces (1.5724, -0.1275) digit for digit.
"""
import numpy as np

t = np.array([0.0, 1.0, 2.0])
xe = np.exp(t)                                  # exact samples
x = np.round(xe, 4)                             # 1, 2.7183, 7.3891 as displayed

# Derivative estimates: forward, centered, backward (dt = 1), as displayed
# (formed from the exact samples, then rounded: 1.7183, 3.1945, 4.6708)
xdot = np.round([xe[1] - xe[0], (xe[2] - xe[0]) / 2, xe[2] - xe[1]], 4)
print("data            x =", x)
print("derivatives x-dot =", xdot)              # 1.7183, 3.1945, 4.6708

# Library {x, x^2} and the four-decimal normal equations
Theta = np.column_stack([x, x**2])
G = np.round(Theta.T @ Theta, 4)
b = np.round(Theta.T @ xdot, 4)
print("\nTheta =\n", np.round(Theta, 4))
print("\nTheta^T Theta =\n", G)
print("Theta^T x-dot =", b)

assert np.abs(G - [[62.9880, 424.5219], [424.5219, 3036.6284]]).max() < 1e-9
assert np.abs(b - [44.9149, 280.3430]).max() < 1e-9

beta = np.linalg.solve(G, b)                    # solve the system as printed
print("\nleast-squares solution beta =", np.round(beta, 4))
print(f"\nrecovered ODE:  x' = {beta[0]:.4f} x {beta[1]:+.4f} x^2")

assert np.abs(np.round(beta, 4) - [1.5724, -0.1275]).max() < 1e-9
print("matches the Sec. 3 walkthrough: (1.5724, -0.1275)")
