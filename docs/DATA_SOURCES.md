# Data sources and preparation boundaries

## What is distributed

This is a replication package from **prepared inputs**. It contains the numeric series, estimation samples and calibrated model inputs actually consumed by the distributed code. It does not claim automated re-extraction from every historical PDF, a complete archive of the source organizations' reports, or a copy of a full commercial database. Source-specific coverage, transcriptions, splices and proxy decisions must be retained when interpreting the estimates.

| Input family | Source family used in the study | Distributed evidence and inputs |
|---|---|---|
| Installed cost and renewable deployment | IRENA Renewable Power Generation Costs series and renewable capacity statistics | `data/source_tables/country_tic_all_cells.csv`, `capacity_countries.csv`; `costs/Source_Data/Annual_Inputs/direct_balance_panel.csv`, `deployment_scenarios.csv`; `cge/inputs/physical_benchmark.csv` |
| PV module-price series | IEA PVPS, NREL and German price material attributed in the revised study to Fraunhofer/BSW | `data/price_provenance/PV_Module_Price_Updated_0915/price_provenance.csv`, `Germany_digitization.csv`, `source_and_window_comparison.csv`; `regressions/data/equipment/pv_regression_panel.csv` |
| Wind equipment-price series and proxies | IRENA, LBNL, Wood Mackenzie and company-series material identified in the revised study | `data/price_provenance/US_Wind_Regression_Replacement_0915/` and `Wind_Country_Proxy_Revision_0915/`, including US/German splices and Danish Vestas proxy; final `regressions/data/equipment/wind_regression_panel.csv` |
| Final supplier prices used by the cost model | Selected series/elasticities and documented interpolation or proxy treatment | `costs/Source_Data/Annual_Inputs/accepted_supplier_price_paths.csv` (including provenance/status fields) |
| Bilateral procurement | UN Comtrade trade values plus domestic-sourcing assumptions, converted to quantity-share proxies using supplier prices | `costs/Source_Data/Annual_Inputs/bilateral_imports_selected.csv`, `legacy_destination_inputs.csv`, `baseline_supplier_weights_tariffs.csv` |
| Border measures | UNCTAD TRAINS via WITS with documented policy-specific adjustments | `costs/Source_Data/Annual_Inputs/pv_bilateral_tariffs.csv`, `wind_bilateral_tariffs.csv`, `documented_policy_pv_tariff_periods.csv`, `policy_functions.py`; generated `annual_tariff_ledger.csv` |
| Other-cost balance | Installed cost minus estimated equipment procurement cost | `direct_balance_panel.csv`; `regressions/data/balance/`; fitted annual paths in `costs/Source_Data/` |
| CPI conversion | US CPI annual values used by the project | `data/source_tables/us_cpi_annual_2010_2024.csv`; 2017-to-2024 conversion factor in `cge/config.json` |
| Knowledge/material controls for supplemental comparisons | Prepared project patent/knowledge and material-price series | `model_comparison/matched/inputs/`, `model_comparison/trials/*/regression_panel.csv` and model-specific samples; these are diagnostic specifications |
| CGE benchmark and dynamics | Project GRID/GHEER benchmark aggregates, energy/power accounts, elasticities, demographic and productivity paths | `cge/model/input/`, `cge/inputs/`, active source modules under `cge/model/jl_r18s15/` |
| Figure maps | Project's existing shapefile and region membership | `data/geography/`; geographic names and polygons are plotting assets, not cost observations |

The source labels in row-level provenance files are the authority for a particular input. A company or agency appearing in the manuscript's broad source list does not imply every final supplier series is a direct observation from that organization. No additional direct company observations were invented during packaging. For bibliographic reference entries, use the final manuscript/SI reference list.

## Completion, weights and frozen inputs

The final cost panel has **334 reported observations and 11 completed cells**: eight internal linear interpolations and three PV 2010 anchors carried from 2011 (Brazil, Japan and South Korea). `observation_imputation_audit.csv` records the completion. Estimation and fitted counterfactuals remain separate from completed observed plotting points.

Figure 1 sample averages use fixed 2024 net additions. CGE regional indices instead use factual cumulative installed capacity. `cge/reference/` retains the country-to-region membership, weights, China reference and uncovered-region paths needed for that mapping; it does not activate an older counterfactual specification. The current S1 country paths are rebuilt from the final historical net contribution by `cge/prepare.py`.

`reference/costs/` holds immutable copies of three final numerical tables for comparison against reruns. `costs/Source_Data/original_mixed_window_results.csv` is retained only as the table schema/metadata used by `update_endpoints.py`; that script replaces the endpoint estimates with the final common 2010–2024 calculation. These supporting files must not be mistaken for headline results.

`docs/PROVENANCE.json` records the original project-relative source and its source hash for copied files. Some code was adapted to relative paths, so source hashes can differ from distributed hashes. The latter are recorded in `MANIFEST_SHA256.csv`. `docs/CSV_CATALOG.csv` inventories the distributed CSV tables and fields.
