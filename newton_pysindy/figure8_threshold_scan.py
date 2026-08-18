"""Figure 8: which library terms survive STLSQ as the threshold is raised,
on the Run B-I extended window.  Also prints the plateau on which only
{1, T} survive (the paper: 0.002 to 0.119)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from newton import EXTENDED, series, stlsq, OUT

T = series("B-I", EXTENDED["B-I"])
thresholds = np.logspace(-7, 1.2, 800)
alive = np.array([stlsq(T, 4, th) != 0 for th in thresholds])   # (threshold, term)

fig, ax = plt.subplots(figsize=(9, 4))
for term in range(5):
    on = thresholds[alive[:, term]]
    ax.hlines(term, on.min(), on.max(), lw=8, color="steelblue")
ax.axvline(0.01, color="k", ls="--", lw=1, label="threshold used, 0.01")
ax.set_xscale("log")
ax.set_yticks(range(5), ["1", "T", "T$^2$", "T$^3$", "T$^4$"])
ax.set_xlabel("threshold value")
ax.set_ylabel("library term")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "figure8_threshold_scan.png", dpi=150)
print("wrote figure8_threshold_scan.png")

only_linear = thresholds[(alive == [True, True, False, False, False]).all(axis=1)]
print(f"only 1 and T survive for thresholds from {only_linear.min():.4f} to {only_linear.max():.4f}")
