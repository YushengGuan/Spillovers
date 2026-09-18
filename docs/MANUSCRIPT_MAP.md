# Manuscript and SI to repository map

Use the final revised manuscript/SI as the exposition. This repository supplies machine-readable input and result tables; it does not reproduce the Word response letters or track-changes documents.

| Manuscript item | Calculation / source | Machine-readable result / figure |
|---|---|---|
| Section 2 cost and regression framework | `regressions/analyse.py`; `costs/Code/build_annual.py` | `regressions/data/`, `regressions/results/`, `costs/Source_Data/Annual_Inputs/` |
| Section 3.1 and Figure 1 | `costs/Code/`; `plotting/figure_1.py` | `costs/Source_Data/annual_country_costs_completed.csv`, `results.csv`, `weighted_shapley_summary.csv`; `Figures/Figure1_costs.*` |
| Scenario construction and productivity mapping | `cge/prepare.py`, `cge/src/experiment.jl` | `cge/inputs/country_tfp_history.csv`, `regional_tfp_paths.csv` |
| Section 3.2 and Figure 2 | `cge/analyze.py`, `plotting/figures_2_3_4.py` | `cge/output/tables/group_equilibria_all_nodes.csv`, `capacity_price_search.csv`, `global_generation_comparison.csv`, `global_final_energy_comparison.csv`; `Figures/Figure2_transition.*` |
| Emissions and Figure 3 | `cge/analyze.py`, `cge/analyze_details.py`, `plotting/figures_2_3_4.py` | `cge/output/tables/regional_contrasts.csv`, `sector_emissions_contrasts.csv`, `power_emissions_contrasts.csv`; `Figures/Figure3_emissions.*` |
| GDP/welfare and Figure 4 | `cge/analyze.py`, `plotting/figures_2_3_4.py` | `cge/output/tables/regional_equilibria_all_nodes.csv`, `global_and_group_deviations.csv`; `Figures/Figure4_equity.*` |
| Sectoral output and Figure 5 | `plotting/figure_5.py` | `cge/output/tables/sector_equilibria_all_nodes.csv`, `global_sector_comparison.csv`; `Figures/Figure5_sectoral_output.*` |
| SI selected equipment-price regression tables | `regressions/data/equipment/accepted_models.csv`, `accepted_coefficients.csv` | `regressions/results/coefficient_comparison.csv`, filter `group=equipment` |
| SI selected other-cost regression tables | `regressions/data/balance/models.csv`, `coefficients.csv`, `fit_samples.csv` | `regressions/results/coefficient_comparison.csv`, filter `group=balance` |
| SI level/difference/trend, ADF and cointegration diagnostics | `regressions/analyse.py` | `regressions/results/coefficient_comparison.csv`, `time_series_diagnostics.csv`, `analysis_samples.csv` |
| SI alternative global/domestic and knowledge specifications | `model_comparison/matched/run_analysis.py`, `model_comparison/refit_trials.py` | `model_comparison/matched/output/`, `model_comparison/results/`; specification metadata in `trials/*/models.csv` |
| SI Table S2.1, region/sector definitions | `cge/model/jl_r18s15/sam/sam_set_r18s15.jl` | Active 18-region / 15-sector code labels; geographic membership also in `data/geography/map_name.csv` |
| SI Table S2.2, cost-shock coverage | `cge/prepare.py` | `cge/inputs/regional_tfp_paths.csv`: `countries`, `mapping_status`, `technology` |
| SI Section 2.6 / Table S2.3, calibration | `cge/src/experiment.jl` | `cge/inputs/physical_benchmark.csv`, `power_targets.csv`, `dynamic_paths.csv`; `cge/equilibria_final/fiveyear_2050/A/calibration.csv` and `power.csv` |
| SI Table S3.1, historical source-country comparison | `source_comparison/Code/analyze.py` | `source_comparison/Source_Data/weighted_endpoints.csv` (`scope=common_receivers`) |
| SI Table S3.2, separate 2024 deployment-withdrawal comparison | `source_comparison/Code/analyze.py` | `source_comparison/Source_Data/joint_2024_summary.csv` |
| SI US/German historical mechanism figures | `source_comparison/Code/plot_figures.py` | `source_comparison/Figures/Fig_S_USA_Historical_Mechanisms.*`, `Fig_S_DEU_Historical_Mechanisms.*` |

Date-stamped folder names in `model_comparison/trials/` identify specification provenance; they do not identify the final CGE scenario vintage. The matched alternative-model exercise is a separate diagnostic dataset and should not be substituted for the selected final equipment/balance equations.
