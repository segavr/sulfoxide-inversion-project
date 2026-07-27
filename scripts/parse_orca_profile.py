"""
parse_orca_profile.py

Parses ORCA .out files for optimized minima and transition states,
extracts final electronic energies, and plots the reaction energy
profile (minimum -> TS -> minimum) for sulfur inversion in
methylphenylsulfoxide, comparing two levels of theory.

Usage:
    python parse_orca_profile.py

Expects the following files relative to the project root
(edit PROJECT_ROOT below if running from elsewhere):
    calculations/step3_b3lyp_opt/step3_opt.out       (SVP minimum)
    calculations/step5_ts_search/attempt2/step5_ts_v2.out  (SVP TS)
    calculations/step4_b3lyp_d3_opt/step4_opt.out    (TZVP minimum)
    calculations/step6_ts_search/step6_ts.out        (TZVP TS)
"""

import re
from pathlib import Path
import matplotlib.pyplot as plt

HARTREE_TO_KCAL = 627.5094740631


def get_final_energy(out_file):
    """
    Extract the last occurrence of 'FINAL SINGLE POINT ENERGY' from an
    ORCA output file. ORCA prints this line at every SCF evaluation
    during geometry optimization; the last one corresponds to the
    converged, final geometry.
    """
    pattern = re.compile(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)")
    energies = []
    with open(out_file, "r", errors="ignore") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                energies.append(float(match.group(1)))
    if not energies:
        raise ValueError(f"No 'FINAL SINGLE POINT ENERGY' found in {out_file}")
    return energies[-1]


def get_imaginary_freq_count(out_file):
    """
    Count vibrational modes marked '***imaginary mode***' in the LAST
    VIBRATIONAL FREQUENCIES block of the file. ORCA prints one such
    block per Hessian evaluation during a TS search (there can be
    several, from intermediate re-calculations of the Hessian); only
    the final block, corresponding to the converged geometry, is
    meaningful. A converged minimum should show 0 such modes; a
    converged first-order TS should show exactly 1.

    Note: the unrelated line "Total number of imaginary
    perturbations ... N" refers to internal numerical-differentiation
    bookkeeping (complex-valued perturbations), not to vibrational
    frequencies, and must not be used for this check.
    """
    block_start_pattern = re.compile(r"VIBRATIONAL FREQUENCIES")
    imag_mode_pattern = re.compile(r"\*\*\*imaginary mode\*\*\*")

    with open(out_file, "r", errors="ignore") as f:
        lines = f.readlines()

    # Find line indices where a new VIBRATIONAL FREQUENCIES block starts
    block_starts = [i for i, line in enumerate(lines) if block_start_pattern.search(line)]
    if not block_starts:
        raise ValueError(f"No VIBRATIONAL FREQUENCIES block found in {out_file}")

    last_start = block_starts[-1]
    # The frequency list ends at the next blank-ish section header;
    # in practice it's safe to scan a generous window (e.g. 80 lines)
    # since ORCA prints at most ~3N frequencies plus a few header lines.
    window = lines[last_start:last_start + 200]

    count = sum(1 for line in window if imag_mode_pattern.search(line))
    return count


def build_profile(min_file, ts_file, label):
    """
    Given output files for a minimum and a TS at the same level of
    theory, return a dict with energies (Hartree and kcal/mol
    relative to the minimum) and sanity-check flags.
    """
    e_min = get_final_energy(min_file)
    e_ts = get_final_energy(ts_file)

    n_imag_min = get_imaginary_freq_count(min_file)
    n_imag_ts = get_imaginary_freq_count(ts_file)

    barrier_kcal = (e_ts - e_min) * HARTREE_TO_KCAL

    return {
        "label": label,
        "e_min": e_min,
        "e_ts": e_ts,
        "barrier_kcal": barrier_kcal,
        "n_imag_min": n_imag_min,
        "n_imag_ts": n_imag_ts,
    }


def sanity_check(profile):
    """Print warnings if the minimum/TS do not have the expected
    number of imaginary frequencies (0 for minimum, 1 for TS)."""
    ok = True
    if profile["n_imag_min"] != 0:
        print(f"  WARNING: {profile['label']} minimum has "
              f"{profile['n_imag_min']} imaginary frequencies (expected 0)")
        ok = False
    if profile["n_imag_ts"] != 1:
        print(f"  WARNING: {profile['label']} TS has "
              f"{profile['n_imag_ts']} imaginary frequencies (expected 1)")
        ok = False
    if ok:
        print(f"  OK: {profile['label']} minimum (0 imag) and "
              f"TS (1 imag) both verified.")
    return ok


def plot_profiles(profiles, output_path):
    fig, ax = plt.subplots(figsize=(7, 5))

    x_positions = [0, 1, 2]  # reactant, TS, product (mirrored minimum)
    x_labels = ["Minimum\n(pyramidal S)", "TS\n(planar S)", "Minimum\n(mirror image)"]

    for profile in profiles:
        y = [0.0, profile["barrier_kcal"], 0.0]
        ax.plot(x_positions, y, marker="o", markersize=8, linewidth=2,
                label=f"{profile['label']} (barrier = {profile['barrier_kcal']:.1f} kcal/mol)")

    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels)
    ax.set_ylabel("Relative electronic energy (kcal/mol)")
    ax.set_title("Sulfur inversion barrier in methylphenylsulfoxide")
    ax.legend(loc="upper center", frameon=True)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"\nPlot saved to: {output_path}")


if __name__ == "__main__":
    PROJECT_ROOT = Path(".")  # run this script from the project root

    svp_min = PROJECT_ROOT / "calculations/step3_b3lyp_opt/step3_opt.out"
    svp_ts = PROJECT_ROOT / "calculations/step5_ts_search/attempt2/step5_ts_v2.out"
    tzvp_min = PROJECT_ROOT / "calculations/step4_b3lyp_d3_opt/step4_opt.out"
    tzvp_ts = PROJECT_ROOT / "calculations/step6_ts_search/step6_ts.out"

    print("Parsing ORCA output files...\n")

    svp_profile = build_profile(svp_min, svp_ts, "B3LYP/def2-SVP")
    tzvp_profile = build_profile(tzvp_min, tzvp_ts, "B3LYP-D3/def2-TZVP")

    print("Sanity checks (imaginary frequency counts):")
    sanity_check(svp_profile)
    sanity_check(tzvp_profile)

    print("\nResults:")
    for p in (svp_profile, tzvp_profile):
        print(f"  {p['label']}: barrier = {p['barrier_kcal']:.2f} kcal/mol")

    diff = svp_profile["barrier_kcal"] - tzvp_profile["barrier_kcal"]
    print(f"\nDifference (SVP - TZVP): {diff:.2f} kcal/mol "
          f"({100*diff/svp_profile['barrier_kcal']:.1f}% relative)")

    plot_profiles([svp_profile, tzvp_profile], PROJECT_ROOT / "results/energy_profile.png")