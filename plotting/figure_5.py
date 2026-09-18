"""Display all 15 model sectors without sector aggregation.

Quantitative two-panel comparison: global real output relative to each
year's S0, top 2030 S1/S2 and bottom 2050 S1/S2. Sum across regions
before taking the ratio. Deterministic model results, no uncertainty estimates.
Match Fig1c colours, hatch and legend; only update Fig4 image exports.
"""
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
os.environ['MPLCONFIGDIR'] = str(ROOT / 'mpl_config')

import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

mpl.rcParams.update({
    'font.family': ['Arial', 'DejaVu Sans'], 'font.size': 7,
    'axes.labelsize': 7, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
    'legend.fontsize': 6.5, 'legend.frameon': False,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': .7, 'svg.fonttype': 'none', 'pdf.fonttype': 42,
})
raw = pd.read_csv(REPO / 'cge/output/tables/sector_equilibria_all_nodes.csv')
sectors = raw.sector.drop_duplicates().tolist()
assert len(sectors) == 15
assert not raw.duplicated(['scenario', 'year', 'region', 'sector']).any()
selected = raw[raw.year.isin([2030, 2050])]
assert selected.groupby(['scenario', 'year', 'sector']).region.nunique().eq(18).all()
global_output = selected.groupby(['scenario', 'year', 'sector'], as_index=False).real_output.sum()
base = global_output[global_output.scenario.eq('S0_BASELINE')].drop(columns='scenario').rename(columns={'real_output': 'S0_output'})
data = global_output.merge(base, on=['year', 'sector'], validate='many_to_one')
assert (data.S0_output > 0).all()
data['difference_pct'] = 100 * (data.real_output / data.S0_output - 1)
assert np.isfinite(data.difference_pct).all()
labels = {
    'Crops nec': 'Crops n.e.c.',
    'Bovine cattle, sheep and goats, horses': 'Cattle, sheep, goats & horses',
    'Animal products nec': 'Animal products n.e.c.',
    'Mine': 'Mining', 'Manufac': 'Manufacturing',
    'Petro': 'Petroleum products', 'WatWaste': 'Water & waste',
    'OthServ': 'Other services',
}
fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.4), sharex=True, sharey=True, layout='constrained')
x = np.arange(len(sectors))
for ax, year, code in zip(axes, [2030, 2050], ['a', 'b']):
    for j, scenario in enumerate(['S1_NO_CN', 'S2_CAPACITY']):
        values = data.query('year == @year and scenario == @scenario').set_index('sector').loc[sectors, 'difference_pct']
        assert len(values) == 15
        ax.bar(x + (j - .5) * .36, values, width=.34,
               color='#FF4500' if scenario == 'S1_NO_CN' else '#4682B4',
               edgecolor='black', linewidth=.3,
               hatch='///' if year == 2050 else None,
               label=f'{scenario[:2]}, {year}')
    assert len(ax.patches) == 30
    ax.axhline(0, color='black', linewidth=.6)
    ax.grid(axis='y', alpha=.15)
    ax.set_axisbelow(True)
    ax.set_xticks(x, [labels.get(s, s) for s in sectors], rotation=50, ha='right', rotation_mode='anchor')
    ax.set_xlim(-.65, len(sectors)-.35)
    ax.set_ylabel('Output difference from S0 (%)')
    ax.legend(loc='lower left', ncol=2)
    ax.text(-.03, 1.035, code, transform=ax.transAxes, ha='left', va='bottom', fontsize=8, fontweight='bold', clip_on=False)
axes[0].tick_params(axis='x', labelbottom=False)
fig.get_layout_engine().set(hspace=.025, h_pad=.025)
axes[1].set_xlabel('Sector')
out = REPO / 'Figures/Figure5_sectoral_output'
fig.savefig(out.with_suffix('.pdf'))
fig.savefig(out.with_suffix('.svg'))
fig.savefig(out.with_suffix('.png'), dpi=300)
fig.savefig(out.with_suffix('.tiff'), dpi=600, pil_kwargs={'compression': 'tiff_lzw'})
plt.close(fig)
print('Updated Figure 5: 15 sectors, 60 bars; 2030 and 2050, S1 and S2.')

data.to_csv(REPO/'cge/output/tables/global_sector_comparison.csv',index=False)
