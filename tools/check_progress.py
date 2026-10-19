#!/usr/bin/env python3
"""
DQMJ1 Decompilation Progression Tracker
Scans reconstructed C functions and outputs matching coverage statistics.
"""

import os
import sys

# Target binary weights (Total: 7,140 functions)
BINARY_SPECS = {
    "arm9.bin": {
        "weight_pct": 36,
        "total_funcs": 2541,
        "dirs": ["src/kernel", "src/arm9"],
    },
    "overlay_0001.bin": {
        "weight_pct": 29,
        "total_funcs": 2105,
        "dirs": ["src/battle"],
    },
    "overlay_0000.bin": {
        "weight_pct": 16,
        "total_funcs": 1120,
        "dirs": ["src/synthesis"],
    },
    "overlay_0002.bin": {
        "weight_pct": 15,
        "total_funcs": 1062,
        "dirs": ["src/save", "src/script"],
    },
    "arm7.bin": {
        "weight_pct": 4,
        "total_funcs": 312,
        "dirs": ["src/arm7"],
    },
}

def count_c_functions(directory):
    if not os.path.exists(directory):
        return 0
    func_count = 0
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".c") and not f.startswith("arm") and not f.startswith("overlay"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                    for line in fp:
                        line = line.strip()
                        # Simple heuristic for C function definition
                        if line.endswith("{") and "(" in line and ")" in line and not line.startswith("if") and not line.startswith("for") and not line.startswith("while") and not line.startswith("switch"):
                            func_count += 1
    return func_count

def main():
    print("=" * 68)
    print("  DQMJ1 (NTR-AJRP-EUR) - Decompilation Progression Status")
    print("=" * 68)
    print(f"{'Module':<20} | {'Weight':<8} | {'Total Funcs':<12} | {'Matched':<8} | {'Coverage'}")
    print("-" * 68)

    total_funcs_all = 0
    total_matched_all = 0

    for module, spec in BINARY_SPECS.items():
        matched = 0
        for d in spec["dirs"]:
            matched += count_c_functions(d)

        total_funcs_all += spec["total_funcs"]
        total_matched_all += matched
        pct = (matched / spec["total_funcs"]) * 100.0

        print(f"{module:<20} | {spec['weight_pct']:>5}%  | {spec['total_funcs']:>10}   | {matched:>7}  | {pct:>6.2f}%")

    print("-" * 68)
    overall_pct = (total_matched_all / total_funcs_all) * 100.0 if total_funcs_all else 0.0
    print(f"{'TOTAL':<20} | {'100%':<8} | {total_funcs_all:>10}   | {total_matched_all:>7}  | {overall_pct:>6.2f}%")
    print("=" * 68)
    print("Baseline: 100% cataloged (7,140 functions). Clean-room matching in progress.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
