"""Table 2: summary of the six records and their red / extended windows."""
from newton import RUNS, RED, EXTENDED, RECORDS, series, OUT

rows = ["Run  Sensor  Start(F)  End(F)   dT(F)  Samples  Linear(dT)   Nonlinear(dT)"]
for rec in ["A-I", "A-II", "B-I", "B-II", "C-I", "C-II"]:
    run, sensor = rec.split("-")
    T = series(rec, RUNS[run])
    Tr = series(rec, RED[rec])
    Te = series(rec, EXTENDED[rec])
    rows.append(f"{run:>3} {sensor:>7} {T[0]:9.2f} {T[-1]:8.2f} {T[-1]-T[0]:+8.2f} {len(T):8d}"
                f"   {len(Tr)}({Tr[-1]-Tr[0]:+.2f})   {len(Te)}({Te[-1]-Te[0]:+.2f})")

text = "\n".join(rows)
print(text)
(OUT / "table2_summary.txt").write_text(text + "\n")
