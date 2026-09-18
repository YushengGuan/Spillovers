# 2026-09-18 replacement release

* Replaces the former main/Figure_1–6 scripts and single Dataset.xlsx entry point with a documented module-based workflow.
* Uses the revised historical P/S/T/K/E decomposition, the completed 2010–2024 country panel, and the final 18 September cost-to-CGE mapping.
* Retains signed historical contributions and applies common factual-2017 productivity normalization. Main China-related net contributions are 1,313.3085 USD/kW (PV) and 378.5993 USD/kW (wind).
* Supplies the final S0/S1/S2 results through 2050 and the 60.8938931660 USD/tCO₂ compensation increment. No old cumulative-savings headline is reproduced.
* Includes selected-equation diagnostics, prepared alternative-model samples, matched model comparisons and China/USA/Germany source comparisons.
* Supplies all five final main figures, the current US/German supplementary figures, portable entry points, dependency records, input provenance and file checksums.
* Replaces machine-specific paths with repository-relative paths. Removes the old solver-license fallback; no license key is distributed.
* Preserves existing numerical methods and model attribution. The default reproducibility workflow uses archived CGE equilibria; a fresh CGE solve is a separate Julia command.
