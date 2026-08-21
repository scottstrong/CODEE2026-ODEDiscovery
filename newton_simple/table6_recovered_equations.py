"""Table 6: Newton's law recovered on the settled windows, with k, tau, T_A,
and the caption's check of the Run A ambients against the room baseline."""
from newton import SETTLED, series, load, fit, newton_constants, OUT

rows = ["Run-Sensor  Minutes   n   Recovered equation           k(1/min)  tau(min)  T_A(F)"]
ambient = {}
for rec in ["A-I", "A-II", "B-I", "B-II", "C-I", "C-II"]:
    a, b = SETTLED[rec]
    T = series(rec, (a, b))
    beta, _ = fit(T, 1)
    k, tau, TA = newton_constants(beta)
    ambient[rec] = TA
    rows.append(f"{rec:<9} {a:>3}-{b:<3} {len(T):3d}   T' = {beta[0]:.4f} {beta[1]:+.4f} T"
                f"    {k:.4f}    {tau:5.1f}   {TA:7.2f}")

I, II = load()
rows.append("")
rows.append("Room baseline, minutes 0-11:  Sensor I %.2f F, Sensor II %.2f F" % (I[:12].mean(), II[:12].mean()))
rows.append("Recovered Run A ambient error: %.2f and %.2f F"
            % (abs(ambient["A-I"] - I[:12].mean()), abs(ambient["A-II"] - II[:12].mean())))
rows.append("B-I minutes 27, 28, 29 read %.1f, %.1f, %.1f F" % tuple(I[27:30]))

text = "\n".join(rows)
print(text)
(OUT / "table6_recovered_equations.txt").write_text(text + "\n")
