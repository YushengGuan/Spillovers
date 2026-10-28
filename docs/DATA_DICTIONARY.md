# Data dictionary

CSV files use UTF-8 (some original exports include a BOM), decimal points and
comma separators. Empty numeric cells/NaN mean unavailable or inapplicable,
not zero. Country codes are ISO3 unless a model-region name is supplied.
`provenance/csv_inventory.json` lists every CSV's columns and row count.

| File family / fields | Definition and units |
|---|---|
| `cost_inputs/*` | Frozen inputs to the historical accounting; original provider releases are not re-downloaded |
| `results.csv`: `total_decline` | Observed installed-cost decline between common endpoints, 2024 USD/kW |
| `P_direct` | Chinese supplier equipment-price contribution, 2024 USD/kW |
| `S_share` | Chinese sourcing-share contribution, 2024 USD/kW |
| `T_cn_tariff` | Chinese-equipment tariff contribution, 2024 USD/kW |
| `K_spillover` | Deployment spillover through non-Chinese supplier equipment prices, 2024 USD/kW |
| `G_other` | Final manuscript E: PV other-cost experience contribution, 2024 USD/kW; zero for wind |
| `cn_related_net` | Sum of the five signed contributions, 2024 USD/kW |
| `remainder` | Observed decline less the China-related net contribution, 2024 USD/kW |
| `*_pct` in cost tables | 100 × contribution / observed installed-cost decline |
| `weight` | Technology-specific fixed share of 2024 net capacity additions in the study sample |
| `net_additions_2024_mw` | 2024 net capacity additions, MW |
| `annual_country_costs_completed.csv`: `observed` | Original reported TIC, 2024 USD/kW; missing values retained |
| `observed_completed`, `completion_method` | Observed series after disclosed endpoint carry/internal interpolation and its flag |
| `model_factual`, `model_without_china_contribution` | Fitted costs and fitted costs plus historical net contribution, 2024 USD/kW |
| `regressions/*/fit_samples.csv`: `y` | Log price/balance or its annual difference, according to the model ID |
| `logQ` / `x` | Log global deployment or its annual difference |
| `logM` | Log silicon-price control or its annual difference |
| `model_id` | Technology, supplier/recipient and specification identifier |
| `coefficient`, `SE_HAC`, `p_HAC_raw` | OLS estimate, calendar-year HAC(1) standard error, unadjusted two-sided t-test p value |
| `country_tfp_history.csv` | Factual/counterfactual costs, inverse-cost productivity, common normalization and regional weights |
| `regional_tfp_paths.csv`: `tfp_multiplier` | Counterfactual/reference technology productivity ratio |
| `scenario` | `S0_BASELINE`, `S1_NO_CN`, `S2_CAPACITY`; raw equilibria use A/B/C |
| `real_GDP`, `real_output`, `EV` in final CGE tables | Real GDP, sector output, equivalent variation; billion 2024 USD |
| `CO2_Mt` | Carbon dioxide emissions, million tonnes |
| `generation_TWh` | Electricity generation, TWh |
| `renewable_capacity_GW`, `capacity_proxy_GW` | Capacity equivalent derived from generation and fixed reference capacity factor, GW |
| `reference_CF` | Reference capacity factor, fraction |
| `modeled_final_demand_Mtoe` | Household plus non-energy-industry final energy use, Mtoe |
| `additional_price_2024USD_t` | Uniform additional carbon price, 2024 USD/tCO2 |
| `GDP_pct`, `CO2_pct` | Scenario difference as a percentage of S0 |
| `EV_pct_C0` | Equivalent variation as a percentage of S0 household consumption |

Raw equilibrium tables in `data/cge/equilibria/` retain base-price values and
diagnostic variables. Use the post-processed `data/cge/tables/` for figure units.
Do not apply the deflator twice. `endpoint_template.csv` is legacy metadata
used by the endpoint updater; its historical effect values are replaced by
the recomputed common-window results before publication outputs are produced.
