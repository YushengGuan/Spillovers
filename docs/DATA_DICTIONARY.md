# Core data dictionary

Column-level inventories for every CSV are in `CSV_CATALOG.csv`. Files preserve established variable names to keep numerical correspondence with the final analysis.

| Field | Meaning / unit |
|---|---|
| `technology` | `pv` or `wind` in historical analysis; named electricity technologies in CGE outputs |
| `iso3` / `supplier` / `destination` | ISO country identifiers or explicitly documented supplier proxy |
| `year` | Calendar year; annual 2010–2024 cost panel; CGE nodes 2017, 2020, 2025, …, 2050 |
| `observed` | Reported total installed cost, 2024 USD/kW; missing values remain missing |
| `observed_completed` | Observed total installed cost with documented completion for reporting |
| `procurement_model` | Modeled equipment procurement cost including relevant border terms, 2024 USD/kW |
| `other_cost_fitted` | Fitted balance outside equipment procurement, 2024 USD/kW |
| `model_factual` | Fitted factual procurement plus fitted other cost, 2024 USD/kW |
| `model_without_china_contribution` | Factual fitted cost plus historical net contribution, 2024 USD/kW |
| `P_direct` | Historical target-origin equipment-price effect P, 2024 USD/kW |
| `S_share` | Sourcing-share effect S, 2024 USD/kW |
| `T_cn_tariff` | China-related border-policy effect T, 2024 USD/kW |
| `K_spillover` | Equipment deployment-learning spillover K, 2024 USD/kW |
| `G_other` | Other-cost effect E, 2024 USD/kW; legacy field name; zero for wind |
| `china_contribution_since_2010` / `cn_related_net` | Sum P+S+T+K+E; signed contribution; annual / endpoint form |
| `total_decline` / `remainder` | Observed endpoint cost decline / part not attributed to the five China-related channels, 2024 USD/kW |
| `weight` / `net_additions_2024_mw` | Fixed within-technology reporting weight / 2024 net added capacity used to construct it |
| `capacity_weight_MW` | Country's factual cumulative capacity used for CGE regional aggregation, MW |
| `cost_actual` / `cost_cf` | Country factual / historical-contribution-restored cost, 2024 USD/kW |
| `tfp_raw_actual` / `tfp_raw_cf` | Inverse-cost productivity paths normalized to each path's 2010 value |
| `tfp_actual` / `tfp_cf` | Both raw paths divided by factual-2017 normalization |
| `tfp_multiplier` | Counterfactual-to-factual productivity ratio; neutral value is 1 |
| `mapping_status` / `countries` | Regional coverage or proxy rule and countries contributing to each cost index |
| `coefficient` / `SE_HAC` | OLS coefficient / heteroskedasticity-and-autocorrelation-consistent standard error |
| `p_raw`, `q_BH` | Unadjusted p value / Benjamini–Hochberg adjusted value within stated testing family |
| `LR_pct` | Learning-rate transformation 100×(1−2^coefficient), percent |
| `logQ`, `logG`, `logK`, `logM`, `x`, `y` | Natural-log or transformed regression variables; check the model-specific panel and specification metadata. In final balance panels `x` is log deployment. Supplemental samples may already be differenced. |
| `scenario` | Exported labels S0_BASELINE, S1_NO_CN, S2_CAPACITY; raw Julia directories A, B, C correspond in that order |
| `real_GDP` / `EV` in `cge/output/tables/` | Real GDP / equivalent variation, billion 2024 USD; flow at the reporting year, not a cumulative amount |
| `CO2_Mt` | Modeled CO₂ emissions, Mt/year |
| `generation_TWh` | Electricity generation, TWh/year |
| `renewable_capacity_GW`, `capacity_proxy_GW` | Capacity equivalent obtained from generation/(8.76×fixed capacity factor), GW |
| `additional_carbon_price_2024USD_t` | Uniform S2 increment above region-specific reference price, 2024 USD/tCO₂ |
| `real_output` in sector output tables | Sectoral real output in billion 2024 USD; `_pct` contrasts are percent changes against S0 |
| `modeled_final_demand_Mtoe` | Household plus non-energy-industry final energy demand; excludes transformation inputs |
| `deviation` / `difference` / `_gap` | Scenario value minus S0 unless a table explicitly states another comparator |

Raw files under `cge/equilibria_final/` retain solver-side units where labeled (including 2017-dollar carbon prices). Use `cge/output/tables/` for manuscript monetary results in 2024 dollars. The CPI factor is 1.279736455613577. Shares may be stored as fractions or percentages according to the field suffix; tariff `applied_rate_pct` is percent, while the internal T term is a rate.

Missing values in source panels and inapplicable diagnostics are intentional; no blanket zero fill is appropriate. The supplementary `source_comparison` tables use P/S/T/K/E column names directly, with `scope` identifying the recipient sample. The `JOINT` rows in `joint_2024_summary.csv` represent a separate nonlinear deployment intervention.
