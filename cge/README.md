# Full CGE solve

The default Python workflow uses archived equilibrium CSVs. This directory
contains the Julia runner and the core model modules loaded by the final
historical-net-contribution experiment. Original copyright notices are retained.

## Prerequisites

1. Julia 1.9.3 (the original execution version) and the versions pinned in
   `Project.toml`.
2. Authorized model input and parameter trees matching
   `required_external_files.json`. The directory layout must contain `input/`
   and `param/` beneath a common root. These are the authors' calibrated,
   aggregated inputs, not an unmodified GTAP distribution. Request the exact
   aggregation/preparation from the corresponding author, subject to provider
   terms; possession of GTAP alone does not establish byte-equivalent inputs.
3. An appropriate PATH solver licence supplied via `PATH_LICENSE_STRING`.
   No licence string is embedded in this release. Never commit that variable
   or place it in a public notebook.

```bash
julia --project=cge -e "using Pkg; Pkg.instantiate()"
python cge/run.py --preflight --external-model-data /path/to/authorized/model-data
python cge/run.py --external-model-data /path/to/authorized/model-data
```

Set `PATH_LICENSE_STRING` in your shell environment before these commands.
If Julia is not on PATH, add `--julia /path/to/julia` to the Python commands.
The preflight checks the 285 archived external input hashes and returns exit
code 2 when required resources are absent or differ. It does
not download restricted inputs or silently fall back to a different benchmark.

The runner executes A (S0), B (S1), C (S2 carbon-price search), then EXPORT,
using a local `.cge_runtime/` directory. A must finish before B/C, which load
its calibrated state. Outputs are written under
`.cge_runtime/equilibria_final/fiveyear_2050/`.

To process freshly solved outputs, set `SPILLOVERS_EQUILIBRIA` to that
directory and run `python reproduce.py --stage analysis`. Validation still
compares against the manuscript snapshot, so differences from another
benchmark or solver environment will be reported rather than concealed.

Full solves have not been executed as part of this packaging task. Included
CSV post-processing and archived residual/accounting checks have been tested.
The core preserves the manuscript model's capacity-equivalent interpretation
and shared-capital closure; it does not add a renewable-capital-stock model.
