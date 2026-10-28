# Methods and numerical conventions

## Historical accounting

Annual installed cost is equipment procurement cost plus an other-cost
balance. Supplier prices, quantities proxied from spending shares, domestic
sourcing, tariffs and documented policy adjustments enter procurement.
The Shapley calculation averages across the six P/S/T orderings. K attributes
deployment-related changes transmitted through non-Chinese supplier prices.
The other-cost experience contribution is included for PV and set to zero
for wind.

Legacy column `G_other` corresponds to **E** in the final manuscript. It is
not a sixth mechanism. `P_direct`, `S_share`, `T_cn_tariff`, `K_spillover`, and
`G_other` sum to `cn_related_net` / `china_contribution_since_2010`. Positive
values denote a contribution to falling costs; adverse contributions retain
their sign. The tariff contribution can be negative. Early negative wind
contributions are not clipped.

The counterfactual plotted cost is the fitted factual cost plus the historical
China-related net contribution. It is not a separate deployment-only causal
counterfactual. The decomposition uses fixed accepted regression coefficients.
Regression refits run independently and verify these estimates; they do not
overwrite the accepted input parameters.

The 345 country-year rows comprise 23 markets over 2010–2024. Of these, 334
observed TIC values are retained; three PV 2010 endpoints use the respective
2011 values (Brazil, Japan, South Korea), and eight internal missing values
are linearly interpolated within country. The audit table preserves the
source cell, anchors and method. These completions are for the observed
figure series and endpoint accounting, not regression imputation.
India wind has a negative initial other-cost balance; the archived output
also reports the aggregate excluding India.

## Regression refits

Equipment price: PV uses log global cumulative capacity and log silicon
price; wind uses log global cumulative capacity. Other-cost balances use
log global cumulative capacity, excluding nonpositive balances from the
log regression. The design samples include level and annual-difference
specifications. HAC(1) uses Bartlett weights, actual adjacent calendar years,
the n/(n-k) finite-sample correction and two-sided Student t inference.

The included refit routine verifies coefficients, HAC standard errors and raw
p values against all 68 archived specifications. It does not independently
rebuild every supplementary robustness or model-selection exercise. Sample
tables distinguish the regression coverage (11 PV/14 wind other-cost
equations) from the 10 PV/13 wind markets in the common historical figure.

## CGE scenarios

| Internal ID | Output ID | Interpretation |
|---|---|---|
| A | S0_BASELINE | Calibrated reference |
| B | S1_NO_CN | Removes China-related historical cost contributions |
| C | S2_CAPACITY | S1 plus a uniform additional carbon price restoring the 2030 target |

The model has 18 regions, 15 sectors and eight generation technologies.
Nodes are 2017, 2020, 2025, 2030, 2035, 2040, 2045 and 2050. Annual cost
reductions map to inverse-cost productivity paths, with a common factual
2017 normalization; the S1/S0 multiplier equals factual/counterfactual cost.
CGE regional aggregation uses cumulative-capacity weights, distinct from
the fixed 2024 net-addition weights used to report the historical sample.

China receives no inward shock. Covered technology productivity paths are
held at 2024 values thereafter; uncovered regions have no direct shock.
Capital is shared by activities within regions. There is no renewable-specific
capital stock or generation ceiling in this specification. The selected
carbon-price increment starts in 2017 and persists through 2050.

Monetary CGE output tables are in billion 2024 USD unless the column states
otherwise. The archived raw equilibria are in the model's base-price units;
post-processing applies deflator 1.279736455613577. Emissions are Mt CO2,
electricity TWh, final energy Mtoe, and generation-derived capacity equivalent
GW. Welfare is equivalent variation at reference consumer prices.

## What was changed for packaging

External drive paths were replaced by paths relative to this project or an
explicit output argument. Outputs are written to a separate work directory.
The figure code retains the final numerical logic and journal styling.
The public CGE post-processor omits binary-state existence checks because
those states are not distributed; accepted-equilibrium residual and accounting
checks remain. A new file manifest verifies release input integrity.
Solver credentials are read only from the user's environment.

No paper results, sample definitions, fitted coefficients or accepted costs
were deliberately changed. Numerical equality is tested against the archived
R2 tables; image files need not be byte-identical across export timestamps
or font environments.
