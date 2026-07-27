# Sulfur Inversion Barrier in Methylphenylsulfoxide: A DFT Functional Comparison

## Research Question

How sensitive is the pyramidal sulfur inversion barrier in sulfoxides to the choice of DFT functional, and what role does dispersion correction play?

## Motivation

Sulfur chirality in sulfoxides is pharmacologically significant — for example, the enantiomers of modafinil's sulfoxide-containing structure show different biological activity. This project investigates the underlying computational chemistry of sulfur pyramidal inversion using a small, tractable model system.

## Model System

Methylphenylsulfoxide, CH₃-S(=O)-C₆H₅ — chosen as a minimal system that retains a chiral sulfoxide center comparable to that in modafinil, while remaining small enough for DFT transition-state searches on a standard laptop.

## Methods

- Geometry generation: RDKit (MMFF initial geometry)
- Quantum chemistry: ORCA 6.1.1
- Two levels of theory compared:
  - **B3LYP/def2-SVP**
  - **B3LYP-D3(BJ)/def2-TZVP** (dispersion-corrected, larger basis)
- Minima and transition states verified via vibrational frequency analysis (0 imaginary frequencies for minima, exactly 1 for TS)
- Transition state confirmed via IRC (Intrinsic Reaction Coordinate) calculation at the SVP level, verifying that the TS connects two mirror-image (enantiomeric) pyramidal minima

## Results

| Level | Electronic barrier (kcal/mol) | ZPE-corrected barrier (kcal/mol) |
|---|---:|---:|
| B3LYP/def2-SVP | 41.49 | 40.58 |
| B3LYP-D3/def2-TZVP | 42.49 | 41.57 |

Zero-point energy correction lowers both barriers by ~0.9 kcal/mol, but the relative difference between the two levels of theory remains essentially unchanged (2.4%). The barrier is thus remarkably insensitive to dispersion correction and basis set enlargement, whether or not ZPE is included. Both transition states are essentially planar at sulfur (sum of bond angles = 360.0°), consistent with the expected sp³ → sp² rehybridization mechanism.

See [`notebooks/01_analysis_and_results.ipynb`](notebooks/01_analysis_and_results.ipynb) for the full analysis, including structural comparison of the two transition states and detailed conclusions.

## Repository Structure

```
├── data/                          # Initial RDKit-generated geometry
├── calculations/
│   ├── step3_b3lyp_opt/           # Minimum, B3LYP/def2-SVP
│   ├── step4_b3lyp_d3_opt/        # Minimum, B3LYP-D3/def2-TZVP
│   ├── step5_ts_search/           # TS search, B3LYP/def2-SVP
│   ├── step6_ts_search/           # TS search, B3LYP-D3/def2-TZVP
│   ├── step7_irc_svp/             # IRC confirming TS connectivity
│   └── step8_comparison_summary.md
├── scripts/
│   └── parse_orca_profile.py      # Parses ORCA output, plots profile
├── notebooks/
│   ├── 00_generate_geometry.ipynb
│   └── 01_analysis_and_results.ipynb
├── results/
│   └── energy_profile.png
└── README.md
```

## Reproducing the Results

```bash
# Requires ORCA 6.1.1 and Python with RDKit, matplotlib
python scripts/parse_orca_profile.py
```

## Limitations and Future Work

- Reported barriers are electronic energies only (no ZPE correction)
- Only the B3LYP functional family was tested; comparison with a range-separated hybrid (e.g. ωB97X-D3) would further test sensitivity to exchange treatment
- IRC was performed only at the SVP level

## References

Sulfoxide inversion barriers of this magnitude (35–45 kcal/mol) are consistent with established literature on pyramidal sulfur inversion in sulfoxides.
