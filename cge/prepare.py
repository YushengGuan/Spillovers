from pathlib import Path
import shutil,json,hashlib
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
OLD=ROOT/'reference'
SRC=REPO/'costs/Source_Data'
(ROOT/'inputs').mkdir(exist_ok=True)
(ROOT/'output').mkdir(exist_ok=True)
paths=pd.read_csv(SRC/'annual_country_costs_completed.csv')
summary=pd.read_csv(SRC/'weighted_shapley_summary.csv')
oldhist=pd.read_csv(OLD/'country_tfp_history.csv')
oldreg=pd.read_csv(OLD/'regional_tfp_paths.csv')
components=['P_direct','S_share','T_cn_tariff','K_spillover','G_other']
assert len(paths)==345 and not paths.duplicated(['technology','iso3','year']).any()
assert np.allclose(paths[components].sum(axis=1),paths.china_contribution_since_2010)
assert np.allclose(paths.model_without_china_contribution-paths.model_factual,paths.china_contribution_since_2010)
assert (paths[['model_factual','model_without_china_contribution']]>0).all().all()
assert paths.loc[paths.year.eq(2010),'china_contribution_since_2010'].eq(0).all()
checkrows=[]
for tech,z in paths[paths.year.eq(2024)].groupby('technology'):
    value=np.dot(z.weight,z.china_contribution_since_2010)
    expected=summary.query('technology==@tech and sample=="main"').cn_related_net.iloc[0]
    assert np.isclose(value,expected,rtol=1e-12)
    checkrows.append(dict(technology=tech,markets=len(z),historical_net_2024_USD_kW=value,section31_value=expected))

hist=[]
for (tech,iso),z in paths.groupby(['technology','iso3']):
    z=z.sort_values('year').copy()
    prior=oldhist[oldhist.technology.eq(tech)&oldhist.iso3.eq(iso)].set_index('year')
    z['region']=prior.region.iloc[0]
    z['country_name']=prior.country_name.iloc[0]
    z['cost_actual']=z.model_factual
    z['cost_cf']=z.model_without_china_contribution
    # Before 2017, weights are diagnostic only; all weights actually used by
    # CGE aggregation (2017-2024) are copied without any change.
    z['capacity_weight_MW']=prior.capacity_weight_MW.reindex(z.year).bfill().to_numpy()
    z['tfp_start_year']=2010;z['alpha']=1.0
    for sc in ['actual','cf']:
        c=z['cost_'+sc].to_numpy()
        z['annual_cost_reduction_'+sc]=np.r_[0,1-c[1:]/c[:-1]]
        z['tfp_growth_factor_'+sc]=np.r_[1,c[:-1]/c[1:]]
        z['tfp_growth_rate_'+sc]=z['tfp_growth_factor_'+sc]-1
        z['tfp_raw_'+sc]=np.cumprod(z['tfp_growth_factor_'+sc])
        assert np.allclose(z['tfp_raw_'+sc],c[0]/c)
    norm=float(z.loc[z.year.eq(2017),'tfp_raw_actual'].iloc[0])
    z['tfp_actual']=z.tfp_raw_actual/norm
    z['tfp_cf']=z.tfp_raw_cf/norm
    z['tfp_multiplier']=z.tfp_cf/z.tfp_actual
    assert np.allclose(z.tfp_multiplier,z.cost_actual/z.cost_cf)
    hist.append(z)
# China's domestic reference productivity is unchanged and receives no inward shock.
hist.append(oldhist[oldhist.iso3.eq('CHN')].copy())
h=pd.concat(hist,ignore_index=True)
regional=[]
for row in oldreg.itertuples(index=False):
    q=h[h.technology.eq(row.technology)&h.region.eq(row.region)&h.year.eq(min(row.year,2024))]
    if len(q):
        w=q.capacity_weight_MW.to_numpy();w=np.ones(len(w)) if w.sum()==0 else w;w=w/w.sum()
        a=float(w@q.tfp_actual);b=float(w@q.tfp_cf)
        mode='historical_net_same_country_paths_as_section31';isos=','.join(q.iso3)
        if row.region=='China':b=a;mode='China_no_inward_shock'
    else:
        a=b=row.baseline_tfp;mode='uncovered_neutral_legacy_reference';isos=''
    regional.append(dict(year=row.year,source_year=min(row.year,2024),region=row.region,technology=row.technology,baseline_tfp=a,cf_tfp=b,tfp_multiplier=b/a,alpha=1.,mapping_status=mode,countries=isos))
r=pd.DataFrame(regional)
h.to_csv(ROOT/'inputs/country_tfp_history.csv',index=False,encoding='utf-8-sig')
r.to_csv(ROOT/'inputs/regional_tfp_paths.csv',index=False,encoding='utf-8-sig')
checks={'source_counts':{'pv':150,'wind':195},'historical_contribution':checkrows,'positive_cost_paths':True,'zero_2010_contribution':True,'tfp_inverse_identity':True}
(ROOT/'output/preflight_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
print(r.query('year==2024')[['technology','region','tfp_multiplier']].to_string(index=False))
