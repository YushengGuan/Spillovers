"""Align all 23 Shapley bars and summaries to the common 2010–2024 window."""
from pathlib import Path
import pandas as pd
import numpy as np
OUT=Path(__file__).resolve().parent.parent;SRC=OUT/'Source_Data'
old=pd.read_csv(SRC/'original_mixed_window_results.csv')
d=old.loc[old.method.eq('Shapley')].copy().set_index(['technology','iso3'])
annual=pd.read_csv(SRC/'annual_country_costs_completed.csv').set_index(['technology','iso3','year'])
source=pd.read_csv(SRC/'annual_decomposition_inputs.csv')
effects=['P_direct','S_share','T_cn_tariff','K_spillover','G_other']
for (tech,iso),r in d.iterrows():
 a=annual.loc[(tech,iso,2010)];b=annual.loc[(tech,iso,2024)]
 decline=a.observed_completed-b.observed_completed
 for key in effects:d.loc[(tech,iso),key]=b[key]
 net=b[effects].sum()
 d.loc[(tech,iso),'start_year']=2010
 d.loc[(tech,iso),'total_decline']=decline
 d.loc[(tech,iso),'cn_related_net']=net
 d.loc[(tech,iso),'remainder']=decline-net
 d.loc[(tech,iso),'cn_tariff_cost_increase']=-b.T_cn_tariff
 z=source[source.technology.eq(tech)&source.iso3.eq(iso)&source.year.eq(2024)&source.supplier.ne('CHN')]
 d.loc[(tech,iso),'other_origin_tariff']=float((z.tariff_weight*(z.T0-z.T1)).sum())
 for short,key in zip(['P','S','T','K','G','net'],effects+['cn_related_net']):
  d.loc[(tech,iso),short+'_pct']=100*d.loc[(tech,iso),key]/decline
d=d.reset_index()
assert (d.start_year==2010).all() and len(d)==23
assert np.allclose(d[effects].sum(axis=1)+d.remainder,d.total_decline)
d.to_csv(SRC/'results.csv',index=False)
comp=d.merge(old[old.method.eq('Shapley')],on=['technology','iso3'],suffixes=('_new','_previous'))
comp=comp[comp.technology.eq('pv')&comp.iso3.isin(['BRA','JPN','KOR'])]
comp.to_csv(SRC/'three_country_endpoint_comparison.csv',index=False)
print(d[['technology','iso3','total_decline','cn_related_net','net_pct']].round(3).to_string(index=False))
