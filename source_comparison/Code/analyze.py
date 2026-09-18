"""Three source-country historical attributions, using the requested historical-price P.
No re-estimation. Shared-receiver comparison excludes CHN/USA/DEU under all cases.
"""
from pathlib import Path
from functools import lru_cache
from itertools import permutations
import shutil, json, hashlib
import numpy as np
import pandas as pd

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parent
PRIOR=OUT/'Inputs'
for name in ['Inputs','Source_Data','Figures','Text','QA']:(OUT/name).mkdir(exist_ok=True)
manifest=[]
def read(name,annual=True):
    src=PRIOR/name
    dst=src
    manifest.append(dict(file=name,source=str(src.relative_to(ROOT)),sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
    return pd.read_csv(dst)
dest=read('legacy_destination_inputs.csv')
trade=read('bilateral_imports_selected.csv')
prices=read('accepted_supplier_price_paths.csv')
panel=read('direct_balance_panel.csv')
co=read('balance_coefficients.csv');co=co[co.spec.eq('main_level')].set_index(['technology','iso3','term'])
sc=read('deployment_scenarios.csv');sc=sc[sc.definition.eq('no_additions_since_2010')].set_index(['technology','removed_country','year'])
per=read('documented_policy_pv_tariff_periods.csv')
wind=read('legacy_wind_policy_and_structure.csv')
tariff={t:read(t+'_bilateral_tariffs.csv').dropna(subset=['applied_rate_pct']).drop_duplicates(['importer_iso3','supplier_iso3','year']) for t in ['pv','wind']}
capacity=read('capacity_weights_all_countries.csv',False)
tariff_ledger=[]
periods={(a,int(b)):z for (a,b),z in per.groupby(['iso3','year'])}
windpol=wind.set_index(['iso3','year'])
policy=OUT/'Inputs/policy_functions.py'
exec(compile(policy.read_text(encoding='utf-8'),str(policy),'exec'))
P=prices.set_index(['technology','supplier','year'])
D=dest.set_index(['technology','iso3','year'])
B=panel.set_index(['technology','iso3','year'])
TRADE={(a,b,int(c)):z.groupby('supplier').primaryValue.sum() for (a,b,c),z in trade.groupby(['technology','destination','year'])}
TARGETS=['CHN','USA','DEU']; EFFECTS=['P','S','T','K','E']
NAMES={'CHN':'China','USA':'USA','DEU':'Germany','AUS':'Australia','BRA':'Brazil','CAN':'Canada','ESP':'Spain','FRA':'France','GBR':'UK','IND':'India','ITA':'Italy','JPN':'Japan','KOR':'South Korea','POL':'Poland','SWE':'Sweden','TUR':'Türkiye'}
CAP_NAMES={**NAMES,'KOR':'Korea Rep'}
weights={}
for tech,g in dest.groupby('technology'):
    for iso in g.iso3.unique():
        z=capacity[capacity.technology.eq(tech)&capacity.country.eq(CAP_NAMES[iso])]
        assert len(z)==1,(tech,iso,CAP_NAMES[iso])
        weights[tech,iso]=float(z.net_additions_2024_mw.iloc[0]);assert weights[tech,iso]>0
def pvalue(tech,s,year):
    if (tech,s,year) in P.index:return float(P.loc[(tech,s,year),'price_usd_kw'])
    return float(np.exp(np.log(prices.loc[prices.technology.eq(tech)&prices.year.eq(year),'price_usd_kw']).mean()))
def pgap(tech,s,year,target):
    if (tech,s,year) not in P.index:return 0.
    r=P.loc[(tech,s,year)]
    return float(r.price_usd_kw*(sc.loc[(tech,target,year),'Q_ratio']**r.beta-1))

W={}; base=[];checks=[]
def ck(label,a,b,tol=1e-7):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    assert err<tol,(label,err)
    checks.append(dict(check=label,max_error=err))
for tech,g in dest.groupby('technology'):
    for iso in sorted(g.iso3.unique()):
        for year in range(2010,2025):
            r=D.loc[(tech,iso,year)]
            tr=TRADE.get((tech,iso,year),pd.Series(dtype=float))
            suppliers=sorted(set(tr.index)|{iso}|set(TARGETS))
            vals=tr.reindex(suppliers,fill_value=0.).to_numpy(dtype=float,copy=True);vals[suppliers.index(iso)]=0.
            imp=float(r.import_dependency_value)
            e=np.zeros(len(suppliers));e[suppliers.index(iso)]=1-imp
            if vals.sum()>0:e+=imp*vals/vals.sum()
            else:assert imp==0
            pp=np.array([pvalue(tech,s,year) for s in suppliers]);ss=e/pp;ss/=ss.sum()
            tt,rr=border(tech,iso,year,suppliers,pp,True)
            W[tech,iso,year]=pd.DataFrame(dict(supplier=suppliers,P=pp,S=ss,T=tt,rent=rr)).set_index('supplier')
            x=float(ss@(pp*(1+tt+rr)))
            q=float(sc.loc[(tech,'CHN',year),'Q_global_gw'])
            a=float(co.loc[(tech,iso,'const'),'coefficient']);b=float(co.loc[(tech,iso,'lnQ'),'coefficient'])
            fit=float(np.exp(a+b*np.log(q)))
            observed=(tech,iso,year) in B.index
            obs=float(B.loc[(tech,iso,year),'tic']) if observed else np.nan
            carry=tech=='pv' and iso in ['BRA','JPN','KOR'] and year==2010
            anchor=float(B.loc[(tech,iso,2011),'tic']) if carry else obs
            bal=anchor-x if observed or carry else fit
            if observed:ck(f'procurement {tech}/{iso}/{year}',x,B.loc[(tech,iso,year),'procurement_cost'])
            base.append(dict(technology=tech,iso3=iso,year=year,observed=obs,procurement=x,B_fit=fit,B_anchor=bal,beta_B=b,model_factual=x+fit,capacity_weight=weights[tech,iso],observation_rule='reported' if observed else 'carry_2011' if carry else 'interpolate_country'))
base=pd.DataFrame(base)
for _,g in base.groupby(['technology','iso3']):
    z=g.sort_values('year');obs=z.observed.copy()
    if z.iloc[0].observation_rule=='carry_2011':obs.iloc[0]=obs.iloc[1]
    obs=obs.interpolate(limit_area='inside');assert obs.notna().all()
    base.loc[z.index,'observed_completed']=obs
base=base.set_index(['technology','iso3','year'])
annual=[];source=[]
for target in TARGETS:
 for tech,g in dest.groupby('technology'):
  for iso in sorted(set(g.iso3)-{target}):
   w0=W[tech,iso,2010]
   for year in range(2010,2025):
    w1=W[tech,iso,year];sup=sorted(set(w0.index)|set(w1.index))
    p0=np.array([pvalue(tech,s,2010) for s in sup]);p1=np.array([pvalue(tech,s,year) for s in sup])
    s0=w0.S.reindex(sup,fill_value=0.).to_numpy();s1=w1.S.reindex(sup,fill_value=0.).to_numpy()
    t0,r0=border(tech,iso,2010,sup,p0,True);t1,r1=border(tech,iso,year,sup,p1,True)
    j=sup.index(target);other=np.array([s!=target for s in sup]);c0=s0[j];c1=s1[j]
    assert c0<1 and c1<1
    R0=np.where(other,s0/(1-c0),0.);R1=np.where(other,s1/(1-c1),0.)
    gaps0=np.array([pgap(tech,s,2010,target) for s in sup]);gaps1=np.array([pgap(tech,s,year,target) for s in sup])
    wp=[];wt=[];sh=[]
    for order in permutations('PST'):
     before=order[:order.index('P')];wp.append((s1 if 'S' in before else s0)*(1+(t1 if 'T' in before else t0)))
     before=order[:order.index('T')];wt.append((p1 if 'P' in before else p0)*(s1 if 'S' in before else s0))
     before=order[:order.index('S')];landed=(p1 if 'P' in before else p0)*(1+(t1 if 'T' in before else t0))
     sh.append((c1-c0)*((R0@landed+R1@landed)/2-landed[j]))
    wp=np.mean(wp,axis=0);wt=np.mean(wt,axis=0)
    b=base.loc[(tech,iso,year)];b0=base.loc[(tech,iso,2010)]
    q0=float(sc.loc[(tech,target,2010),'Q_ratio']);qt=float(sc.loc[(tech,target,year),'Q_ratio'])
    v=dict(P=float(wp[j]*(p0[j]-p1[j])),S=float(np.mean(sh)),T=float(wt[j]*(t0[j]-t1[j])),K=float(np.sum(wp[other]*(gaps1-gaps0)[other])),E=float(b.B_anchor*(qt**b.beta_B-1)-b0.B_anchor*(q0**b0.beta_B-1)) if tech=='pv' else 0.)
    net=sum(v.values());decline=float(b0.observed_completed-b.observed_completed)
    annual.append(dict(target=target,technology=tech,iso3=iso,year=year,**b.to_dict(),**v,net=net,total_decline=decline,remainder=decline-net,model_without_source_contribution=b.model_factual+net))
    if year==2010:ck(f'initial net {target}/{tech}/{iso}',net,0.)
    if year==2024:
     for k,s in enumerate(sup):source.append(dict(target=target,technology=tech,iso3=iso,supplier=s,P0=p0[k],P1=p1[k],S0=s0[k],S1=s1[k],T0=t0[k],T1=t1[k],price_weight=wp[k],tariff_weight=wt[k],gap0=gaps0[k],gap1=gaps1[k]))
a=pd.DataFrame(annual);a['net_pct']=100*a.net/a.total_decline.replace(0,np.nan)
end=a[a.year.eq(2024)].copy();assert len(end)==69
ck('closure',end[EFFECTS].sum(axis=1)+end.remainder,end.total_decline)
prev=pd.read_csv(PRIOR/'archived_china_endpoints.csv').set_index(['technology','iso3'])
china=end[end.target.eq('CHN')].set_index(['technology','iso3'])
for key,old in [('P','P_historical_price_decline'),('S','S_share'),('T','T_cn_tariff'),('K','K_spillover'),('E','G_other'),('total_decline','total_decline')]:
 ck('China replication '+key,china[key],prev.loc[china.index,old])
# Independent endpoint replication against the three-source archived results.
for tech,folder in [('pv','PV_Four_Effects_0915'),('wind','Wind_Three_Effects_Final_0915')]:
 old=pd.read_csv(PRIOR/f'{tech}_archived_targets.csv')
 old=old[old.method.eq('Shapley')&~old.excluded_target_receiver&old.start_year.eq(2010)].set_index(['target','iso3'])
 new=end[end.technology.eq(tech)].set_index(['target','iso3']).loc[old.index]
 for key,col in [('P','direct_price_effect'),('S','target_share_effect'),('K','spillover_other_origins')]+([('E','global_experience_contribution')] if tech=='pv' else []):ck('Archived '+tech+' '+key,new[key],old[col])

weighted=[]
for target in TARGETS:
 for tech in ['pv','wind']:
  for scope in ['foreign_sample','common_receivers','common_without_India']:
   z=a[a.target.eq(target)&a.technology.eq(tech)].copy()
   if scope!='foreign_sample':z=z[~z.iso3.isin(TARGETS)]
   if scope=='common_without_India':z=z[z.iso3.ne('IND')]
   for year,g in z.groupby('year'):
    w=g.capacity_weight/g.capacity_weight.sum()
    r=dict(target=target,technology=tech,scope=scope,year=int(year),n=len(g),capacity_weight_sum=g.capacity_weight.sum())
    for k in EFFECTS+['net','total_decline','remainder','observed_completed','model_factual','model_without_source_contribution']:
     r[k]=float(w@g[k])
    r['net_pct']=100*r['net']/r['total_decline'] if year!=2010 else np.nan
    r['deployment_channels_K_E']=r['K']+r['E']
    weighted.append(r)
w=pd.DataFrame(weighted)

# A separate diagnostic addresses simultaneous withdrawal without adding hybrid accounts.
# 2024 levels; all equipment origins respond to one jointly reduced Q, B only for PV.
joint=[]
for tech in ['pv','wind']:
 receivers=sorted(set(dest.loc[dest.technology.eq(tech),'iso3'])-set(TARGETS))
 for iso in receivers:
  b=base.loc[(tech,iso,2024)];wp=W[tech,iso,2024]
  qt=float(sc.loc[(tech,'CHN',2024),'Q_global_gw'])
  for label,targets in [(t,[t]) for t in TARGETS]+[('JOINT',TARGETS)]:
   removed=sum(float(sc.loc[(tech,t,2024),'removed_experience_gw']) for t in targets)
   ratio=(qt-removed)/qt;assert ratio>0
   equipment=0.
   for supplier,row in wp.iterrows():
    if (tech,supplier,2024) in P.index:
     pp=P.loc[(tech,supplier,2024)];gap=pp.price_usd_kw*(ratio**pp.beta-1)
     equipment+=row['S']*(1+row['T']+row['rent'])*gap
   other=float(b.B_anchor*(ratio**b.beta_B-1)) if tech=='pv' else 0.
   joint.append(dict(target=label,technology=tech,iso3=iso,capacity_weight=weights[tech,iso],equipment_gap=equipment,other_gap=other,total_gap=equipment+other,Q_ratio=ratio))
j=pd.DataFrame(joint);js=[]
for (target,tech),g in j.groupby(['target','technology']):
 ww=g.capacity_weight/g.capacity_weight.sum()
 js.append(dict(target=target,technology=tech,n=len(g),equipment_gap=float(ww@g.equipment_gap),other_gap=float(ww@g.other_gap),total_gap=float(ww@g.total_gap),Q_ratio=float(g.Q_ratio.iloc[0])))
for name,data in [('annual_country',a),('country_endpoints',end),('weighted_annual',w),('weighted_endpoints',w[w.year.eq(2024)]),('endpoint_inputs',pd.DataFrame(source)),('joint_2024_countries',j),('joint_2024_summary',pd.DataFrame(js)),('completed_factual_panel',base.reset_index())]:data.to_csv(OUT/'Source_Data'/f'{name}.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(tariff_ledger).drop_duplicates().to_csv(OUT/'Source_Data/tariff_ledger.csv',index=False)
(OUT/'QA/analysis_checks.json').write_text(json.dumps(dict(all_pass=True,checks=checks,rows=len(a),country_endpoints=len(end),P_definition='all historical target-origin equipment-price reductions',common_sample_excludes=TARGETS,regressions_refitted=False,original_China_Figure1_modified=False),indent=2),encoding='utf-8')
(OUT/'QA/input_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(w[w.year.eq(2024)&w.scope.ne('common_without_India')][['target','technology','scope','n','P','S','T','K','E','net','net_pct']].round(3).to_string(index=False))
print(pd.DataFrame(js).round(3).to_string(index=False))
