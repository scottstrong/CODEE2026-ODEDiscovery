#!/usr/bin/env python3
"""Environment check for the CODEE SINDy examples (MS #1123).

Run this before anything else:

    python environment_check.py

It prints the versions this machine has, compares them against the versions
the paper's results were produced with (pinned in requirements.txt), and says
plainly whether every figure and table should reproduce here.

Exit code 0 = match; 1 = mismatch or missing package.
"""

import sys

# The tested versions. Keep these in sync with requirements.txt.
PINNED = {
    "numpy": "2.4.3",
    "scipy": "1.17.1",
    "pandas": "3.0.2",
    "pysindy": "2.1.0",
    "matplotlib": "3.10.8",
}

PY_MIN = (3, 10)


def main() -> int:
    ok = True
    v = sys.version_info
    py = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) >= PY_MIN:
        print(f"[ok]   Python {py}")
    else:
        ok = False
        print(f"[FAIL] Python {py} (need >= {PY_MIN[0]}.{PY_MIN[1]})")

    try:
        from importlib.metadata import version, PackageNotFoundError
    except ImportError:  # very old Python; already failed above
        return 1

    for pkg, want in PINNED.items():
        try:
            have = version(pkg)
        except PackageNotFoundError:
            ok = False
            print(f"[FAIL] {pkg}: not installed  (pip install -r requirements.txt)")
            continue
        if want.startswith("TODO"):
            print(f"[??]   {pkg} {have}  (paper's tested version not yet pinned)")
        elif have == want:
            print(f"[ok]   {pkg} {have}")
        else:
            ok = False
            print(f"[FAIL] {pkg} {have}  (paper used {want})")

    print()
    if ok:
        print("Environment matches. Every result in the paper should reproduce here.")
        print("Next: Problem 0 — run the logistic notebook unchanged and match the")
        print("published Japan-population figure.")
    else:
        print("Environment does NOT match the paper's. Results may differ; fix the")
        print("[FAIL] lines above (usually: pip install -r requirements.txt).")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
