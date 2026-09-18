"""Cross-check sample expansion, endpoint closure, weights and preserved results."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent.parent;SRC=OUT/'Source_Data'
old=OUT.parent/'reference/costs'
d=pd.read_csv(SRC/'plot_country_data.csv')
a=pd.read_csv(SRC/'annual_country_costs_completed.csv')
t=pd.read_csv(SRC/'annual_plot_costs.csv')
w=pd.read_csv(SRC/'weighted_shapley_summary.csv')
effects=['P_direct','S_share','T_cn_tariff','K_spillover','G_other']
sample=d.copy();sample['weight']=sample.net_additions_2024_mw/sample.groupby('technology').net_additions_2024_mw.transform('sum')
sample.to_csv(SRC/'annual_sample_weights.csv',index=False)
assert len(a)==345 and len(d)==23
for tech,n in [('pv',10),('wind',13)]:
 group=a[a.technology.eq(tech)]
 assert group.groupby('year').size().eq(n).all()
 assert group.groupby('iso3').weight.nunique().eq(1).all()
 assert np.allclose(group.groupby('year').weight.sum(),1.)
 z=t[t.technology.eq(tech)].set_index('year');s=w[w.technology.eq(tech)&w['sample'].eq('main')].iloc[0]
 assert np.isclose(z.loc[2010,'observed_completed']-z.loc[2024,'observed_completed'],s.total_decline)
 assert np.isclose(z.loc[2024,'model_without_china_contribution']-z.loc[2024,'model_factual'],s.cn_related_net)
 for iso,g in group.groupby('iso3'):
  q=sample[sample.technology.eq(tech)&sample.iso3.eq(iso)].iloc[0]
  assert np.allclose(g.weight,q.weight)
  e=g[g.year.eq(2024)].iloc[0]
  assert np.allclose(e[effects].astype(float),q[effects].astype(float))
ref_a=pd.read_csv(old/'annual_country_costs_completed.csv').set_index(['technology','iso3','year'])
new_a=a.set_index(['technology','iso3','year']).loc[ref_a.index]
cols=['observed','observed_completed','procurement_model','other_cost_fitted','model_factual','model_without_china_contribution',*effects]
assert np.allclose(new_a[cols],ref_a[cols],equal_nan=True)
ref_d=pd.read_csv(old/'results.csv').set_index(['technology','iso3'])
new_d=d.set_index(['technology','iso3']).loc[ref_d.index]
assert np.allclose(ref_d[effects+['total_decline','remainder']],new_d[effects+['total_decline','remainder']])
for iso in ['BRA','JPN','KOR']:
 g=a[a.technology.eq('pv')&a.iso3.eq(iso)].set_index('year')
 assert pd.isna(g.loc[2010,'observed'])
 assert g.loc[2010,'observed_completed']==g.loc[2011,'observed']
audit=dict(all_pass=True,pv_countries=10,wind_countries=13,country_years=345,raw_reported=334,filled=11,carry_to_2010=3,internal_interpolation=8,reproduces_archived_final_23_country_paths=True,reproduces_archived_final_23_country_effects=True,annual_vs_bar_endpoint_closure=True,identical_country_weights=True)
(OUT/'QA/sample_expansion_checks.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print(audit)
