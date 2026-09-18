# ChinaContribution — revised manuscript replication package

**Cost Spillovers in Solar and Wind Power: Mechanism Decomposition and Economic Implications**  
Yusheng Guan, Kangxin An, Shihui Zhang, Can Wang and Kebin He  
Release: **18 September 2026** · [中文说明](README_zh.md)

This package replaces the earlier repository workflow with the analysis supporting the revised manuscript and Supplementary Information (SI). It contains prepared input data, estimation samples, calculation and plotting code, final CGE equilibria, tabular results and publication figures. The numerical reference is the **18 September historical net-contribution CGE analysis**, using the same annual cost paths as the main historical decomposition.

## Quick start

Python **3.10 or later** is required; Python 3.10.11 was tested. From the extracted repository root:

```bash
python -m venv .venv
# Activate .venv using the command for your operating system.
python -m pip install -r requirements-tested.txt
python run_pipeline.py
```

The default command refits the selected regressions and supplemental comparisons, reconstructs historical costs and productivity inputs, analyzes the **included final CGE equilibrium CSVs**, regenerates all five main figures and two source-country comparison figures, and runs numerical checks. It does not require Julia or a PATH license. It starts from the frozen, prepared datasets in this repository; downloading and extracting all original third-party reports is outside this pipeline.

To inspect the supplied results without regenerating figures:

```bash
python verify.py
python verify.py --integrity
```

`--integrity` compares files with the original ZIP release manifest. Run it before changing or regenerating files; differences after a rerun can reflect generated timestamps or figure metadata, not changed scientific results. Individual workflow stages are available with `python run_pipeline.py --stage regressions`, `costs`, `comparisons`, `cge-analysis`, `figures` or `verify`. Run `costs` before `cge-analysis` if cost inputs have changed. The latter checks consistency against the archived equilibria; it does not solve new equilibria for changed shocks.

## Repository contents

| Directory/file | Contents |
|---|---|
| `costs/` | 2010–2024 annual costs; procurement, price, tariff and deployment inputs; Shapley decomposition and sample checks |
| `regressions/` | Selected equipment-price and other-cost equations, estimation panels, level/difference/trend fits, HAC inference and time-series diagnostics |
| `model_comparison/` | Matched global/domestic model comparison and prepared samples for supplemental alternative specifications |
| `source_comparison/` | China/USA/Germany attribution on matched recipient samples, separate joint deployment-withdrawal diagnostic, and supplementary plots |
| `cge/` | Julia model, benchmark inputs, cost-to-productivity mapping, final scenario states, CSV exports and Python postprocessing |
| `plotting/` | Scripts for Figures 1–5 |
| `Figures/` | Final main figures in PDF, SVG, PNG and TIFF |
| `data/` | Equipment-price provenance, source tables, CPI and map files |
| `reference/` | Immutable final cost tables used to check numerical reproduction |
| `docs/` | Data dictionary, source notes, manuscript-to-file map, provenance and reproducibility report |
| `QA/` | Package-level numerical verification |
| `MANIFEST_SHA256.csv` | File sizes and SHA-256 checksums of the distributed files |

Begin with [MANUSCRIPT_MAP.md](docs/MANUSCRIPT_MAP.md), [DATA_SOURCES.md](docs/DATA_SOURCES.md) and [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).

## Numerical reference

All reported historical costs are in **constant 2024 US dollars per kW**. The 2024 China-related historical net contribution is **1,313.3085 USD/kW for PV** and **378.5993 USD/kW for wind**. Main reporting samples comprise **10 PV and 13 wind markets outside China**, with 15 annual observations per market after documented completion (345 rows). The sample averages use fixed **2024 net-added-capacity weights**.

| Quantity | 2030 S1 | 2030 S2 | 2050 S1 | 2050 S2 |
|---|---:|---:|---:|---:|
| Renewable capacity equivalent (GW) | 9,046.51 | 10,999.96 | 12,429.26 | 15,464.15 |
| CO₂ difference from S0 (Mt/year) | 152.08 | −7,815.43 | 188.91 | −9,170.81 |
| Real GDP difference from S0 (billion 2024 USD/year) | −128.97 | −761.48 | −106.78 | −1,461.92 |
| Equivalent variation (billion 2024 USD/year) | −249.28 | −2,047.73 | −379.45 | −2,832.05 |

S0 is the reference; S1 restores the estimated China-related historical net cost contribution to the fitted factual costs; S2 adds a uniform **60.8938931660 USD/tCO₂** increment to region-specific reference carbon prices from 2017 through 2050. S0 reaches 11,000 GW equivalent in 2030. The capacity outcome is generation converted using fixed capacity factors, not an independently modeled installed-capacity stock.

### Definitions that matter

* Cost columns `P_direct`, `S_share`, `T_cn_tariff`, `K_spillover`, `G_other` correspond to manuscript **P, S, T, K, E**. The legacy column name `G_other` denotes the other-cost channel E; it is not the patent/knowledge-stock regressor G. Wind E is fixed to zero.
* The historical counterfactual cost is `model_factual + P_direct + S_share + T_cn_tariff + K_spillover + G_other`. It is a historical mechanism accounting exercise, not an identified causal effect of removing all Chinese activity. Signed contributions are preserved.
* Regression-based contrasts subtract fitted values; no sampled regression residual is added. Differenced/trend and time-series tests are diagnostics, not replacements for the selected equations.
* CGE aggregation uses factual **cumulative deployment** weights within each region, distinct from the net-addition weights used in Figure 1. Both productivity paths share factual-2017 normalization; at country level the S1/S0 productivity ratio is factual cost divided by counterfactual cost.
* Covered cost/productivity paths are frozen after 2024. China and uncovered regions receive no direct inward shock, but may respond through general-equilibrium links. The model is coupled in one direction from estimated costs to CGE shocks.
* The historical source-country comparison uses eight PV and eleven wind recipients after excluding China, USA and Germany. SI's joint deployment-withdrawal exercise is separate and cannot be obtained by adding historical mechanism accounts.
* Older trillion-dollar cumulative-savings headlines and old Figure 1–6 workflows are not the outputs of this release.

## Re-solving the CGE model (optional)

The default workflow already includes and checks the final equilibria. To solve again, install **Julia 1.9.3**, instantiate the recorded environment and provide your own valid PATH solver license through the `PATH_LICENSE_STRING` environment variable. No key is included.

```bash
julia --project=cge -e "using Pkg; Pkg.instantiate()"
python cge/run.py check
python cge/run.py solve
python run_pipeline.py --stage cge-analysis
python run_pipeline.py --stage figures
python verify.py
```

Use `--julia /path/to/julia` if Julia is not on PATH. `check` builds the model without solving; `solve` executes A (S0), B (S1), the C (S2) carbon-price search and the final CSV export. Solving writes to `cge/equilibria_final/`; run it in a working copy if you want to preserve the distributed equilibria. The saved `.jls` states are Julia-version-specific; CSV exports are the portable reading format. This packaging run checked model construction but did **not** repeat the full CGE optimization.

## Citation and attribution

See [CITATION.cff](CITATION.cff) for the manuscript authors and release identity. No publication DOI has been assigned in this package. Original model attribution is retained; see [RIGHTS_AND_ATTRIBUTION.md](docs/RIGHTS_AND_ATTRIBUTION.md). Third-party source reports and full commercial databases are not reproduced here.
