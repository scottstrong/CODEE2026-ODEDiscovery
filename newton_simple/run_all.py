"""Run every script, in the order of the paper."""
import runpy

for name in ["table2_summary", "tables3_4_coefficients", "table5_incremental_r2",
             "table6_recovered_equations", "figure7_phase_planes",
             "figure8_threshold_scan", "text_thresholds",
             "exercise18_forward_solve", "exercise19_two_time_scales"]:
    print(f"\n===== {name}")
    runpy.run_path(f"{name}.py")
