"""Figure 7: (T, T') phase planes for Runs A, B, C on both sensors.
Red = linear window, purple = extension, blue = unused (sensor transitions)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from newton import RUNS, RED, EXTENDED, series, derivative, OUT

for run, (a, b) in RUNS.items():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, sensor in zip(axes, ["I", "II"]):
        rec = f"{run}-{sensor}"
        T = series(rec, (a, b))
        dT = derivative(T)                       # differenced over the whole run, for display
        for i, minute in enumerate(range(a, b + 1)):
            if RED[rec][0] <= minute <= RED[rec][1]:
                color = "red"
            elif EXTENDED[rec][0] <= minute <= EXTENDED[rec][1]:
                color = "purple"
            else:
                color = "blue"
            ax.plot(T[i], dT[i], "o", color=color, ms=5)
        ax.axhline(0, color="gray", lw=0.5, ls="--")
        ax.set_xlabel("T (°F)")
        ax.set_ylabel("T' (°F/min)")
        ax.set_title(f"Run {run}, Sensor {sensor}")
    fig.tight_layout()
    fig.savefig(OUT / f"figure7_run_{run}.png", dpi=150)
    print("wrote", f"figure7_run_{run}.png")
