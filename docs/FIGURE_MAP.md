# Figure and source-data mapping

| Final figure | Subject | Script | Primary inputs |
|---|---|---|---|
| Figure 1 | Historical installed costs and country contributions | `plotting/figure_costs.py` | `data/figure_source/Costs/results.csv`, `annual_plot_costs.csv`, capacity weights and coverage |
| Figure 2 | Capacity equivalent, carbon-price search and energy responses | `plotting/figures.py` | CGE group/power tables, `capacity_price_search.csv`, `capacity_policy_selected.csv`, `final_energy_mix.csv` |
| Figure 3 | Regional and global CO2 emissions | `plotting/figures.py` | `regional_equilibria_all_nodes.csv`, geography files |
| Figure 4 | Regional GDP and household welfare | `plotting/figures.py` | `regional_equilibria_all_nodes.csv`, geography files |
| Figure 5 | Sectoral output changes | `plotting/figure_sectors.py` | `sector_equilibria_all_nodes.csv` |

All CGE plotting input tables are in `data/cge/tables/`. Detailed chart-ready
exports are in `data/figure_source/CGE/` and regenerated under the output
directory. Figure 1 uses 10 PV and 13 wind markets; the macro maps use the
18 CGE regions. Do not interchange these geographic samples.

`figures/submitted/` preserves the SVGs checked against the submission folder,
plus PNG previews. Graphical abstracts and manuscript Word files are not part
of this code release.

The selected regression refits support the equipment and other-cost model
estimates in Supplementary Tables S1.1/S1.2. This mapping does not claim that
all supplementary robustness tables are rebuilt by the default workflow.
