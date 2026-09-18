"""Annual fitted costs and historical China-contribution-restored scenario.

No regression refit; same country sample and fixed 2024 weights as the bar panels.
Observed aggregate points require every main-sample country to be observed.
"""
from pathlib import Path
from functools import lru_cache
from itertools import permutations
import json, hashlib, shutil
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent.parent
ROOT=OUT.parent
C=OUT/'Source_Data/Annual_Inputs'
F=OUT/'Source_Data/Annual_Inputs'
manifest=[]
def read(path,name=None):
 dest=F/(name or path.name)
 if not dest.exists():raise FileNotFoundError(dest)
 manifest.append(dict(file=dest.name,source=str(dest.relative_to(ROOT)),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
 return pd.read_csv(dest)
dest=read(F/'legacy_destination_inputs.csv')
trade=read(F/'bilateral_imports_selected.csv')
prices=read(C/'accepted_supplier_price_paths.csv')
panel=read(F/'direct_balance_panel.csv')
co=read(F/'balance_coefficients.csv')
co=co[co.spec.eq('main_level')].set_index(['technology','iso3','term'])
sc=read(C/'deployment_scenarios.csv')
sc=sc[sc.removed_country.eq('CHN')&sc.definition.eq('no_additions_since_2010')].set_index(['technology','year'])
existing_w=read(C/'baseline_supplier_weights_tariffs.csv')
per=read(F/'documented_policy_pv_tariff_periods.csv')
wind=read(F/'legacy_wind_policy_and_structure.csv')
tariff={t:read(F/f'{t}_bilateral_tariffs.csv').dropna(subset=['applied_rate_pct']).drop_duplicates(['importer_iso3','supplier_iso3','year']) for t in ['pv','wind']}
tariff_ledger=[]
periods={(a,int(b)):z for (a,b),z in per.groupby(['iso3','year'])}
windpol=wind.set_index(['iso3','year'])
policy=F/'policy_functions.py'
if not policy.exists():raise FileNotFoundError(policy)
manifest.append(dict(file=policy.name,sha256=hashlib.sha256(policy.read_bytes()).hexdigest()))
exec(compile(policy.read_text(encoding='utf-8'),str(policy),'exec'))
accepted=pd.read_csv(OUT/'Source_Data/plot_country_data.csv')
main=accepted.copy()
main['weight']=main.net_additions_2024_mw/main.groupby('technology').net_additions_2024_mw.transform('sum')
main.to_csv(OUT/'Source_Data/annual_sample_weights.csv',index=False)
P=prices.set_index(['technology','supplier','year'])
D=dest.set_index(['technology','iso3','year'])
B=panel.set_index(['technology','iso3','year'])
TRADE={(a,b,int(c)):z.groupby('supplier').primaryValue.sum() for (a,b,c),z in trade.groupby(['technology','destination','year'])}
W={};annual_rows=[];audit=[];source_rows=[]
def check(name,actual,expected,tol=1e-7):
 error=float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
 assert error<tol,(name,error)
 audit.append(dict(check=name,error=error,pass_check=True))
def pvalue(tech,supplier,year):
 if (tech,supplier,year) in P.index:return float(P.loc[(tech,supplier,year),'price_usd_kw'])
 z=prices[prices.technology.eq(tech)&prices.year.eq(year)]
 return float(np.exp(np.log(z.price_usd_kw).mean()))
def pricegap(tech,supplier,year):
 if (tech,supplier,year) not in P.index:return 0.
 row=P.loc[(tech,supplier,year)]
 return float(row.price_usd_kw*(sc.loc[(tech,year),'Q_ratio']**row.beta-1))
for r in main.itertuples():
 tech,iso=r.technology,r.iso3
 for year in range(2010,2025):
  row=D.loc[(tech,iso,year)]
  tr=TRADE.get((tech,iso,year),pd.Series(dtype=float))
  suppliers=sorted(set(tr.index)|{iso,'CHN'})
  vals=tr.reindex(suppliers,fill_value=0.).to_numpy(dtype=float,copy=True);vals[suppliers.index(iso)]=0
  importshare=float(row.import_dependency_value)
  e=np.zeros(len(suppliers));e[suppliers.index(iso)]=1-importshare
  if vals.sum()>0:e+=importshare*vals/vals.sum()
  else:assert importshare==0
  pp=np.array([pvalue(tech,s,year) for s in suppliers]);ss=e/pp;ss/=ss.sum()
  tt,rr=border(tech,iso,year,suppliers,pp,True)
  W[(tech,iso,year)]=pd.DataFrame(dict(supplier=suppliers,P=pp,S=ss,T=tt,rent=rr)).set_index('supplier')
  x=float(np.dot(ss,pp*(1+tt+rr)))
  q=float(sc.loc[(tech,year),'Q_global_gw']);ratio=float(sc.loc[(tech,year),'Q_ratio'])
  intercept=float(co.loc[(tech,iso,'const'),'coefficient']);beta=float(co.loc[(tech,iso,'lnQ'),'coefficient'])
  bfit=float(np.exp(intercept+beta*np.log(q)))
  observed=(tech,iso,year) in B.index
  obs=float(B.loc[(tech,iso,year),'tic']) if observed else np.nan
  carry_2011 = tech=='pv' and iso in ['BRA','JPN','KOR'] and year==2010
  anchor_obs=float(B.loc[(tech,iso,2011),'tic']) if carry_2011 else obs
  balance=anchor_obs-x if observed or carry_2011 else bfit
  if observed:check(f'{tech}/{iso}/{year} procurement matches accepted',x,B.loc[(tech,iso,year),'procurement_cost'])
  old=existing_w[existing_w.technology.eq(tech)&existing_w.iso3.eq(iso)&existing_w.year.eq(year)]
  if len(old):
   new=W[(tech,iso,year)].loc[old.supplier]
   for key,col in [('S','quantity_share'),('P','baseline_price_usd_kw'),('T','duty_rate'),('rent','policy_rent_rate')]:check(f'{tech}/{iso}/{year}/{key}',new[key].to_numpy(),old[col].to_numpy())
  annual_rows.append(dict(technology=tech,iso3=iso,year=year,weight=r.weight,observed=obs,procurement_model=x,other_cost_fitted=bfit,other_cost_observed=obs-x if observed else np.nan,model_factual=x+bfit,Q=q,Q_ratio=ratio,beta_B=beta,G_level_gap=balance*(ratio**beta-1) if tech=='pv' else 0.,G_anchor='2011_TIC_carried_to_2010' if carry_2011 else 'observed_residual_preserved' if observed and tech=='pv' else 'fitted_for_missing_observation' if tech=='pv' else 'excluded_for_wind',B_fit_outside_year_range=year<int(co.loc[(tech,iso,'const'),'first_year']) or year>int(co.loc[(tech,iso,'const'),'last_year'])))
rows=pd.DataFrame(annual_rows).set_index(['technology','iso3','year'])
for r in main.itertuples():
 tech,iso=r.technology,r.iso3;w0=W[(tech,iso,2010)]
 for year in range(2010,2025):
  w1=W[(tech,iso,year)];sup=sorted(set(w0.index)|set(w1.index)|{iso,'CHN'})
  p0=np.array([pvalue(tech,s,2010) for s in sup]);p1=np.array([pvalue(tech,s,year) for s in sup])
  s0=w0.S.reindex(sup,fill_value=0.).to_numpy();s1=w1.S.reindex(sup,fill_value=0.).to_numpy()
  t0,r0=border(tech,iso,2010,sup,p0,True);t1,r1=border(tech,iso,year,sup,p1,True)
  assert np.all(r0==0)
  j=sup.index('CHN');nont=np.array([s!='CHN' for s in sup]);c0=s0[j];c1=s1[j]
  assert c0<1 and c1<1
  R0=np.where(nont,s0/(1-c0),0.);R1=np.where(nont,s1/(1-c1),0.)
  gaps0=np.array([pricegap(tech,s,2010) for s in sup]);gaps1=np.array([pricegap(tech,s,year) for s in sup])
  wp=[];wt=[];sh=[]
  for order in permutations('PST'):
   before=order[:order.index('P')];wp.append((s1 if 'S' in before else s0)*(1+(t1 if 'T' in before else t0)))
   before=order[:order.index('T')];wt.append((p1 if 'P' in before else p0)*(s1 if 'S' in before else s0))
   before=order[:order.index('S')];landed=(p1 if 'P' in before else p0)*(1+(t1 if 'T' in before else t0))
   sh.append((c1-c0)*((R0@landed+R1@landed)/2-landed[j]))
  wp=np.mean(wp,axis=0);wt=np.mean(wt,axis=0)
  vals=dict(P_direct=float(wp[j]*(p0[j]-p1[j])),S_share=float(np.mean(sh)),T_cn_tariff=float(wt[j]*(t0[j]-t1[j])),K_spillover=float(np.sum(wp[nont]*(gaps1-gaps0)[nont])),G_other=float(rows.loc[(tech,iso,year),'G_level_gap']-rows.loc[(tech,iso,2010),'G_level_gap']))
  net=sum(vals.values())
  for key,val in vals.items():rows.loc[(tech,iso,year),key]=val
  rows.loc[(tech,iso,year),'china_contribution_since_2010']=net
  rows.loc[(tech,iso,year),'model_without_china_contribution']=rows.loc[(tech,iso,year),'model_factual']+net
  for idx,supplier in enumerate(sup):source_rows.append(dict(technology=tech,iso3=iso,year=year,supplier=supplier,P0=p0[idx],P1=p1[idx],S0=s0[idx],S1=s1[idx],T0=t0[idx],T1=t1[idx],rent0=r0[idx],rent1=r1[idx],price_weight=wp[idx],tariff_weight=wt[idx],price_gap0=gaps0[idx],price_gap1=gaps1[idx]))
  if year==2010:check(f'{tech}/{iso} zero initial historical contribution',net,0.)
  if year==2024 and not (tech=='pv' and iso in ['BRA','JPN','KOR']):
   for key,val in vals.items():check(f'{tech}/{iso} endpoint {key}',val,getattr(r,key))
   check(f'{tech}/{iso} endpoint net',net,r.cn_related_net)
rows=rows.reset_index();rows.to_csv(OUT/'Source_Data/annual_country_costs.csv',index=False)
pd.DataFrame(source_rows).to_csv(OUT/'Source_Data/annual_decomposition_inputs.csv',index=False)
summary=[]
for (tech,year),z in rows.groupby(['technology','year']):
 check(f'{tech}/{year} constant complete sample weights',z.weight.sum(),1.)
 complete=z.observed.notna().all()
 entry=dict(technology=tech,year=year,n_countries=len(z),n_observed=int(z.observed.notna().sum()),observed_complete=complete,
 observed=float(np.dot(z.weight,z.observed)) if complete else np.nan,
 observed_available_subset=float(np.average(z.loc[z.observed.notna(),'observed'],weights=z.loc[z.observed.notna(),'weight'])),
 observed_weight_coverage=float(z.loc[z.observed.notna(),'weight'].sum()))
 for k in ['model_factual','model_without_china_contribution','china_contribution_since_2010','procurement_model','other_cost_fitted','P_direct','S_share','T_cn_tariff','K_spillover','G_other']:entry[k]=float(np.dot(z.weight,z[k]))
 check(f'{tech}/{year} curve gap matches historical net',entry['model_without_china_contribution']-entry['model_factual'],entry['china_contribution_since_2010'])
 summary.append(entry)
summary=pd.DataFrame(summary);summary.to_csv(OUT/'Source_Data/annual_weighted_costs.csv',index=False)
pd.DataFrame(tariff_ledger).drop_duplicates().to_csv(OUT/'Source_Data/annual_tariff_ledger.csv',index=False)
(OUT/'QA/annual_checks.json').write_text(json.dumps(dict(checks=audit,input_manifest=manifest,all_pass=True,rows=len(rows),model_years=15,raw_observations_preserved=True,three_2010_G_anchors_use_2011_TIC=True),indent=2),encoding='utf-8')
print(summary[['technology','year','n_observed','observed','model_factual','model_without_china_contribution']].round(2).to_string(index=False))
