"""Tables 3 and 4: polynomial fits T' = b0 + b1 T + ... + b_d T^d, degrees 1-4,
on the red windows (Table 3) and the extended windows (Table 4)."""
from newton import RED, EXTENDED, RECORDS, series, fit, coef, OUT

for name, windows in [("table3_red", RED), ("table4_extended", EXTENDED)]:
    rows = [f"{'Run-Sensor (dT)':<18}{'b0':>12}{'b1':>10}{'b2':>10}{'b3':>10}{'b4':>10}{'R2':>9}"]
    for rec in RECORDS:
        T = series(rec, windows[rec])
        label = f"{rec} ({T[-1]-T[0]:+.2f})"
        for degree in range(1, 5):
            beta, r2 = fit(T, degree)
            b = list(beta) + [None] * (4 - degree)
            rows.append(f"{label:<18}{coef(b[0]):>12}{coef(b[1]):>10}{coef(b[2]):>10}"
                        f"{coef(b[3]):>10}{coef(b[4]):>10}{r2:9.4f}")
            label = ""
    text = "\n".join(rows)
    print(name); print(text); print()
    (OUT / f"{name}.txt").write_text(text + "\n")
