# Reproducibility report — 18 September 2026

## Checks actually performed for this release

The staged repository was copied to a separate directory and executed using repository-relative input paths. The calculation and plotting scripts completed without reading the original research directories. The test used the existing installed Python/Julia libraries recorded in `TESTED_ENVIRONMENT.json`; it was not a test of downloading packages on a new computer.

| Check | Observed outcome |
|---|---|
| Selected equipment and balance equations | 34 selected equations; level, annual-difference and time-trend fits executed; maximum discrepancy from archived coefficient 5.78×10⁻¹⁴ and HAC standard error 1.63×10⁻¹³ |
| Time-series diagnostics | ADF/Engle–Granger tests and BH-adjusted tables regenerated; ineligible short contiguous blocks retain explicit non-computed status |
| Supplemental prepared-sample regressions | 245 equations refitted; maximum archived coefficient discrepancy 4.55×10⁻¹² and HAC standard-error discrepancy 5.46×10⁻⁸ |
| Matched model comparison | 150 fits; all 1,483 internal checks passed |
| Historical cost reconstruction | 345 country-years, 10 PV and 13 wind markets; 334 reported cells plus 11 documented completions; component, weight and final-endpoint checks passed |
| China/USA/Germany comparisons | Annual/endpoint comparisons and joint deployment diagnostic regenerated; internal checks passed; both supplementary figures regenerated |
| CGE input mapping and postprocessing | Country/regional productivity paths rebuilt; all 220 postprocessing checks passed against supplied final equilibria |
| CGE construction | Julia 1.9.3 loaded the packaged model and benchmark files and built 29,056 variables without a solver key |
| Main plots | Figures 1–5 regenerated in PDF, SVG, PNG and TIFF; Figures 1 and 4 additionally inspected visually |
| Package verification | `python verify.py` passed 51 checks, including headline costs, carbon price and 2030/2050 scenario results |
| File checks | Python syntax checked; no machine-specific Windows drive paths, credential-pattern matches, private Git metadata, or files above 25 MiB in the distributed content |

The supplied CGE archive records three scenarios over eight model nodes (24 final equilibria). Their convergence/accounting records are checked by `cge/analyze.py`. **The full nonlinear CGE optimization and carbon-price search were not repeated during packaging.** A fresh solve requires Julia and a valid user-supplied PATH license; use the commands in the main README.

## Expected reproducibility limits

* The pipeline begins with frozen prepared data and regression samples. Manual report extraction, source selection and splice decisions are documented in the distributed provenance tables; they are not automated downloads.
* Numerical assertions use tolerances, because floating-point libraries and solver environments can differ. Generated PDF/SVG metadata, font substitution, timestamps and software versions can also change file hashes while leaving numerical results unchanged.
* The original archived 24 CGE states and CSV exports are retained. Julia `.jls` serialization should be read with the specified Julia environment. Readers needing only results should use the CSV tables.
* Historical mechanism estimates and CGE scenarios are conditional model outputs. This repository adds no causal identification, out-of-sample CGE validation or joint uncertainty intervals beyond the revised study.
* The 2018–2024 rolling comparisons under `model_comparison/matched/` use contemporaneously known regressors and previously prepared cost series. They are retrospective conditional-prediction diagnostics, not a real-time forecast evaluation or validation of CGE projections.

## Entry points

`run_pipeline.py` runs the tested Python steps in dependency order. It uses archived CGE equilibria. `cge/run.py check` builds the Julia model; `cge/run.py solve` reruns A/B/C and exports final states. If changing cost inputs, regenerate CGE equilibria before interpreting new macroeconomic results; the archived-equilibrium checks are intentionally designed to reject inconsistent input/output combinations.

`MANIFEST_SHA256.csv` records the release contents (excluding the manifest itself). `python verify.py --integrity` checks the intact release before regeneration. `QA/release_verification.json`, the regression audits, the matched-comparison audit, cost QA and `cge/output/tables/validation_checks.csv` provide machine-readable verification records.
