# Sulfur Inversion Barrier in Methylphenylsulfoxide: A DFT Functional Comparison



\## Research Question



How sensitive is the pyramidal sulfur inversion barrier in sulfoxides 

to the choice of DFT functional, and what role does dispersion 

correction play?



\## Motivation



Sulfur chirality in sulfoxides is pharmacologically significant — for 

example, the enantiomers of modafinil's sulfoxide-containing structure 

show different biological activity. This project investigates the 

underlying computational chemistry of sulfur pyramidal inversion using 

a small, tractable model system.



\## Model System



Methylphenylsulfoxide, CH₃-S(=O)-C₆H₅ — chosen as a minimal system 

that retains a chiral sulfoxide center comparable to that in modafinil, 

while remaining small enough for DFT transition-state searches on a 

standard laptop.



\## Methods



\- Geometry generation: RDKit (MMFF initial geometry)

\- Quantum chemistry: ORCA 6.1.1

\- Two levels of theory compared:

&#x20; - \*\*B3LYP/def2-SVP\*\*

&#x20; - \*\*B3LYP-D3(BJ)/def2-TZVP\*\* (dispersion-corrected, larger basis)

\- Minima and transition states verified via vibrational frequency 

&#x20; analysis (0 imaginary frequencies for minima, exactly 1 for TS)

\- Transition state confirmed via IRC (Intrinsic Reaction Coordinate) 

&#x20; calculation at the SVP level, verifying that the TS connects two 

&#x20; mirror-image (enantiomeric) pyramidal minima



\## Results



| Level                | Barrier (kcal/mol, electronic) |

|-----------------------|--------------------------------:|

| B3LYP/def2-SVP        | 41.49                           |

| B3LYP-D3/def2-TZVP    | 42.49                           |



The barrier changes by only \~1 kcal/mol (2.4%) between the two levels 

of theory — smaller than might be expected given the aromatic and 

alkyl substituents near the inversion center. Both transition states 

are essentially planar at sulfur (sum of bond angles = 360.0°), 

consistent with the expected sp³ → sp² rehybridization mechanism.



See `notebooks/01\_analysis\_and\_results.ipynb` for the full analysis, 

including structural comparison of the two transition states and 

detailed conclusions.



\## Repository Structure

├── data/ # Initial RDKit-generated geometry

├── calculations/

│ ├── step3\_b3lyp\_opt/ # Minimum, B3LYP/def2-SVP

│ ├── step4\_b3lyp\_d3\_opt/ # Minimum, B3LYP-D3/def2-TZVP

│ ├── step5\_ts\_search/ # TS search, B3LYP/def2-SVP

│ ├── step6\_ts\_search/ # TS search, B3LYP-D3/def2-TZVP

│ ├── step7\_irc\_svp/ # IRC confirming TS connectivity

│ └── step8\_comparison\_summary.md

├── scripts/

│ └── parse\_orca\_profile.py # Parses ORCA output, plots profile

├── notebooks/

│ ├── 00\_generate\_geometry.ipynb

│ └── 01\_analysis\_and\_results.ipynb

├── results/

│ └── energy\_profile.png

└── README.md

\## Reproducing the Results



```bash

\# Requires ORCA 6.1.1 and Python with RDKit, matplotlib

python scripts/parse\_orca\_profile.py

```



\## Limitations and Future Work



\- Reported barriers are electronic energies only (no ZPE correction)

\- Only the B3LYP functional family was tested; comparison with a 

&#x20; range-separated hybrid (e.g. ωB97X-D3) would further test 

&#x20; sensitivity to exchange treatment

\- IRC was performed only at the SVP level



\## References



Sulfoxide inversion barriers of this magnitude (35–45 kcal/mol) are 

consistent with established literature on pyramidal sulfur inversion 

in sulfoxides.

