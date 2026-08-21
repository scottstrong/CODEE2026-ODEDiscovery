"""Table 5: linear R^2 and the gain from adding T^2, on the extended windows.
The gain column is the true difference of the two R^2 values, rounded to 4 decimals."""
from newton import RUNS, EXTENDED, RECORDS, series, fit, OUT

rows = ["Run  Sensor  dT(F)  Linear R2  dR2(Quad)  Leading samples in blue"]
for rec in RECORDS:
    run, sensor = rec.split("-")
    T = series(rec, EXTENDED[rec])
    _, r2_lin = fit(T, 1)
    _, r2_quad = fit(T, 2)
    gain = r2_quad - r2_lin
    blue = EXTENDED[rec][0] - RUNS[run][0]
    rows.append(f"{run:>3} {sensor:>6} {abs(T[-1]-T[0]):6.0f}   {r2_lin:.4f}    {gain:+.4f}   {blue:6d}")

text = "\n".join(rows)
print(text)
(OUT / "table5_incremental_r2.txt").write_text(text + "\n")
