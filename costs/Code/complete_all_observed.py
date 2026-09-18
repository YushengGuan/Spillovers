"""Country-only completion: requested 2011-to-2010 carry, then internal interpolation."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent.parent
SRC=OUT/'Source_Data'
d=pd.read_csv(SRC/'annual_country_costs.csv')
source=pd.read_csv(SRC/'Annual_Inputs/country_tic_all_cells.csv')
names={'BRA':'Brazil','JPN':'Japan','KOR':'Republic of Korea','ITA':'Italy','ESP':'Spain','POL':'Poland'}
filled=[];audit=[]
for (tech,iso),g in d.groupby(['technology','iso3']):
 g=g.sort_values('year').copy()
 assert list(g.year)==list(range(2010,2025))
 x=g.year.to_numpy();raw=g.observed.to_numpy();v=raw.copy()
 method=np.where(np.isfinite(raw),'reported','internal_linear_interpolation').astype(object)
 carry=tech=='pv' and iso in ['BRA','JPN','KOR']
 if carry:
  assert np.isnan(v[0]) and np.isfinite(v[1])
  v[0]=v[1];method[0]='2011_value_carried_to_2010_per_user'
 mask=np.isfinite(v)
 assert mask[0] and mask[-1] and np.all(np.diff(x[mask])>0)
 complete=np.interp(x,x[mask],v[mask])
 assert np.array_equal(complete[np.isfinite(raw)],raw[np.isfinite(raw)])
 for i in np.flatnonzero(~np.isfinite(raw)):
  y=int(x[i])
  if carry and y==2010: left=right=2011;vl=vr=float(raw[1])
  else:
   left=int(x[mask & (x<y)].max());right=int(x[mask & (x>y)].min())
   vl=float(v[np.where(x==left)[0][0]]);vr=float(v[np.where(x==right)[0][0]])
   assert abs(complete[i]-(vl+(vr-vl)*(y-left)/(right-left)))<1e-9
  sr=source[source.technology.eq(tech)&source.country.eq(names[iso])&source.year.eq(y)]
  assert len(sr)==1,(tech,iso,y,names[iso])
  sr=sr.iloc[0];assert pd.isna(sr.tic) and sr.source_status=='source_blank'
  audit.append(dict(technology=tech,iso3=iso,year=y,source_sheet=sr.source_sheet,source_cell=sr.source_cell,source_status=sr.source_status,left_year=left,left_value=vl,right_year=right,right_value=vr,completed_value=float(complete[i]),method=method[i],unit='2024 USD/kW'))
 g['observed_completed']=complete;g['observation_imputed']=~np.isfinite(raw);g['completion_method']=method
 filled.append(g)
result=pd.concat(filled,ignore_index=True)
result.to_csv(SRC/'annual_country_costs_completed.csv',index=False)
pd.DataFrame(audit).to_csv(SRC/'observation_imputation_audit.csv',index=False)
ag=[]
for (tech,year),g in result.groupby(['technology','year']):
 assert np.isclose(g.weight.sum(),1.)
 assert len(g)==(10 if tech=='pv' else 13)
 ag.append(dict(technology=tech,year=year,observed_completed=float(np.dot(g.weight,g.observed_completed)),n_imputed=int(g.observation_imputed.sum()),imputed_weight=float(g.loc[g.observation_imputed,'weight'].sum()),contains_imputation=bool(g.observation_imputed.any())))
annual=pd.read_csv(SRC/'annual_weighted_costs.csv').merge(pd.DataFrame(ag),on=['technology','year'],validate='one_to_one')
assert len(annual)==30 and annual.observed_completed.notna().all()
assert len(result)==345 and len(audit)==11
assert np.allclose(annual.loc[~annual.contains_imputation,'observed_completed'],annual.loc[~annual.contains_imputation,'observed'])
annual.to_csv(SRC/'annual_plot_costs.csv',index=False)
(OUT/'QA/completed_observation_checks.json').write_text(json.dumps(dict(country_years=345,reported_country_years=334,filled_country_years=11,carried_2011_to_2010=3,internal_linear_interpolations=8,annual_points=30,aggregate_points_containing_imputation=int(annual.contains_imputation.sum()),all_reported_values_unchanged=True,weights_identical_to_model=True,model_not_used_for_imputation=True),indent=2),encoding='utf-8')
print(pd.DataFrame(audit)[['technology','iso3','year','completed_value','method']].to_string(index=False))
