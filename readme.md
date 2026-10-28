# Cost Spillovers in Solar and Wind Power: Mechanism Decomposition and Economic Implications

Reproducibility project for **Cost Spillovers in Solar and Wind Power: Mechanism Decomposition and Economic Implications**, *Environmental Science and Ecotechnology*.

**Authors:** Yusheng Guan, Kangxin An, Shihui Zhang, Can Wang, and Kebin He.
**Correspondence:** Shihui Zhang, ritazhang9414@gmail.com.

The project links historical renewable-cost accounting to regional economic
scenarios. It contains the frozen numerical inputs, historical decomposition,
regression refits, archived CGE equilibria, final plotting code, and the CGE
model modules used for the three scenarios. The main figure set has **five**
figures. Earlier experiments and reviewer correspondence are not part of this
release.

## Quick start

Python 3.10 was used for local verification. Use a fresh environment:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_release.py
python reproduce.py
```

The default command refits 68 regression specifications, recomputes the
historical cost decomposition, processes the archived CGE equilibria, and
renders Figures 1–5. It compares recomputed values against the frozen final
data and writes `outputs/reproduction/validation.json`. No network access,
Microsoft Office, external drive path, GTAP installation, or solver licence is
needed for this workflow. Original input files are not overwritten.

```bash
python reproduce.py --stage analysis    # numerical analyses only
python reproduce.py --stage figures     # figures from frozen final results
python reproduce.py --output outputs/my_run
```

The figure renderer produces SVG, PDF, PNG and TIFF in
`outputs/reproduction/figures/Figures/`. Arial is used in the submitted artwork.
Install an appropriately licensed Arial font to match it; otherwise Matplotlib
may substitute a font, changing text layout. The tested Matplotlib version is
pinned because the journal style layer uses Matplotlib rendering internals.

## Reproduction scope

| Component | Included and executable | Boundary |
|---|---|---|
| Equipment and other-cost regressions | Level/difference OLS and calendar-adjacent HAC(1) refits from frozen design samples | Does not re-download or independently re-extract publisher/source workbooks |
| Historical attribution, Figure 1 | Annual procurement accounting, Shapley P/S/T allocation, K and E contributions, observed-series completion and weighting | Uses the accepted supplier-price paths and other-cost coefficients supplied with the manuscript |
| Economic results, Figures 2–5 | Recompute aggregates, contrasts and welfare measures from archived equilibrium CSVs | This is post-processing, not a fresh equilibrium solve |
| Full CGE solve | Julia runner and the 32 loaded core model modules | Requires authorized external benchmark inputs and a PATH licence; see [CGE instructions](cge/README.md) |
| Supplementary analysis | Selected regression designs and their level/difference refits, CGE parameters and diagnostics | Alternative model searches and all supplementary diagnostic tests are not claimed to be reproduced by the default command |

The full nonlinear CGE solve was **not** rerun when preparing this release.
Residual and accounting checks on the archived equilibria are retained.
Binary Julia solver states and embedded licence credentials are excluded.

## Main results and interpretation

- Historical China-related contributions in the studied foreign markets:
  **1,313.3 USD/kW (25.5%)** for PV and **378.6 USD/kW (26.8%)** for wind.
  Percentages are shares of the **observed 2010–2024 installed-cost decline**.
- In 2030, removing these contributions gives about **9,046.5 GW** of renewable
  capacity equivalent, **17.8%** below the 11,000 GW reference target, and a
  global GDP difference of about **−129.0 billion 2024 USD**.
- An additional carbon price of about **60.9 USD/tCO2** restores the target,
  with a GDP difference of about **−761.5 billion 2024 USD**.

The historical sample comprises **10 PV and 13 wind markets**, with fixed
2024 net-added-capacity weights. Coverage is 68.1% and 81.8% of additions
outside China. These weighted sample results are not global extrapolations.
The fitted relationships and historical attribution are conditional; they do
not establish a causal effect of deployment. CGE capacity is generation
divided by a fixed reference capacity factor, not an independently modelled
installed-capacity stock. See [methods and limitations](docs/METHODS.md).

## Project layout

```text
analysis/                 Historical accounting, regression and CGE post-processing
plotting/                 Figure 1–5 code and journal styling
cge/                      Julia model, solver runner and external-input manifest
data/cost_inputs/         Frozen procurement, tariffs, price paths and coefficients
data/regressions/         Frozen design samples and accepted estimates
data/cge/                 Scenario inputs, archived equilibria and final tables
data/figure_source/       Numerical figure source data and original map boundaries
figures/submitted/        Archived submission SVGs and PNG previews
docs/                     Methods, data dictionary, source and figure mappings
provenance/               File inventory, hashes and verification records
scripts/                  Release integrity and numerical validation
outputs/                  Generated locally; excluded from Git
```

See [figure mapping](docs/FIGURE_MAP.md), [data dictionary](docs/DATA_DICTIONARY.md),
[source information](docs/DATA_SOURCES.md), and [Chinese guide](docs/README_ZH.md).


