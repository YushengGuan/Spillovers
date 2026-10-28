# Data sources and access

The packaged CSVs are the authors' frozen analytical extracts and model
outputs used for the final R2 figures. They are not a complete mirror of the
underlying third-party databases. Consult the article's references for the
specific reports, years and source choices.

| Data | Source described in manuscript | Packaged location / access |
|---|---|---|
| Installed costs and renewable capacity | IRENA Renewable Power Generation Costs reports and IRENASTAT | `data/cost_inputs/`, cost figure sources and regression panels |
| PV supplier prices and silicon-price controls | IEA PVPS, NREL, BSW and IRENA source reports | Equipment regression panels and accepted supplier-price paths |
| Wind turbine prices | IRENA and Lawrence Berkeley National Laboratory | Equipment regression panels and accepted supplier-price paths |
| Bilateral trade | United Nations Comtrade | `bilateral_imports_selected.csv` and procurement extracts |
| Tariffs and policy adjustments | UNCTAD TRAINS via World Bank WITS, plus documented policy adjustments | Bilateral tariffs, policy periods and `policy_functions.py` |
| Other-cost balances | Authors' subtraction of estimated procurement from observed installed costs | Other-cost regression panel and frozen balance coefficients |
| Macro benchmark | GTAP 11, 2017 accounts, aggregated for GHEER | Not included; authorized external model inputs are required for a fresh solve |
| Model outputs | Authors' GHEER runs | `data/cge/equilibria/`, `data/cge/tables/` |
| Geographic boundaries | Author-supplied shapefile used for the submitted maps | `data/figure_source/Geography/`; source/licence confirmation remains necessary before public upload |

Official access points: [IRENA](https://www.irena.org/Data),
[IEA PVPS](https://iea-pvps.org/), [UN Comtrade](https://comtradeplus.un.org/),
[WITS](https://wits.worldbank.org/), and
[GTAP](https://www.gtap.agecon.purdue.edu/databases/).
No provider redistribution licence is implied by these links.

No DOI has been assigned to this prepared local snapshot. The existing GitHub
URL is not evidence that this snapshot is already uploaded. After publication
of an authorized release, record its commit/tag and, if obtained, its archival
DOI in CITATION.cff and the manuscript availability statement.
