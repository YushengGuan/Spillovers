"""Matched-sample specification comparison; no downstream model replacement."""
from pathlib import Path
import json, hashlib, shutil, platform
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

ROOT=Path(__file__).resolve().parent
REPO=ROOT
INP=ROOT/'inputs';OUT=ROOT/'output'
INP.mkdir(parents=True,exist_ok=True);OUT.mkdir(exist_ok=True)
FILES={
 'pv.xlsx':'Review1/Patents_panel_PV.xlsx',
 'wind.xlsx':'Review1/Patents_panel_wind.xlsx',
 'cost_capacity.xlsx':'Code_update/Code_iScience_2024/Data_raw.xlsx',
 'selected_regressions.csv':'Review1/response_bilingual_0912/frozen_response/evidence/current_regressions_and_learning_rates.csv',
 'selected_stock_panel.csv':'Review1/patent_start2010_sensitivity_0911/output/stock_panel.csv',
 'country_map.csv':'Review1/patent_start2010_sensitivity_0911/output/input_audit.csv'}
manifest=[]
for name,rel in FILES.items():
    src=INP/name;dest=src
    digest=hashlib.sha256(src.read_bytes()).hexdigest()
    if dest.exists():assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest
    else:shutil.copy2(src,dest)
    manifest.append(dict(source="inputs/"+name,frozen=name,sha256=digest))
SPECS={'G0':('global',None),'D0':('domestic',None),'GD':('global','domestic'),
       'DD':('domestic','domestic'),'DG':('domestic','global'),'GG':('global','global')}
OFFICES={'EPO','WIPO','EAPO'}
countries=pd.read_csv(INP/'country_map.csv')
selected=pd.read_csv(INP/'selected_regressions.csv')
oldstocks=pd.read_csv(INP/'selected_stock_panel.csv')
oldstocks=oldstocks[oldstocks.spec.eq('pre2008_flow_lag0')]
checks=[]
def ck(label,ok):
    checks.append(dict(check=label,passed=bool(ok)))
    assert ok,label
flows=[];globalrows=[];panels=[];fits=[];coefficients=[];predictions=[];samples=[];replication=[]
for tech,suffix in [('pv','solar'),('wind','wind')]:
    raw=pd.read_excel(INP/f'{tech}.xlsx',sheet_name='Sheet1')
    raw.Country=raw.Country.str.strip();raw.Year=raw.Year.astype(int)
    ck(tech+' raw unique country-years',not raw.duplicated(['Country','Year']).any())
    ck(tech+' nonnegative integer flows',raw.Coount.notna().all() and raw.Coount.ge(0).all() and raw.Coount.mod(1).eq(0).all())
    raw['exclude_office']=raw.Country.isin(OFFICES)
    raw.assign(technology=tech).to_csv(OUT/f'{tech}_patent_source_audit.csv',index=False,encoding='utf-8-sig')
    years=np.arange(2008,2025)
    country_stock={}
    included=raw[~raw.exclude_office]
    for country,g in included.groupby('Country'):
        series=g.set_index('Year').Coount
        f=series.reindex(years).fillna(0.).to_numpy(float)
        h=np.zeros(len(years));h[0]=f[0]/.1
        for i in range(1,len(years)):h[i]=.9*h[i-1]+f[i]
        country_stock[country]=h
        for i,y in enumerate(years):
            flows.append(dict(technology=tech,patent_geography=country,year=int(y),F=f[i],H=h[i],record_present=int(y) in series.index,fill_rule='observed' if int(y) in series.index else 'unlisted_assumed_zero'))
    fg=included.groupby('Year').Coount.sum().reindex(years,fill_value=0).to_numpy(float)
    hg=np.zeros(len(years));hg[0]=fg[0]/.1
    for i in range(1,len(years)):hg[i]=.9*hg[i-1]+fg[i]
    ck(tech+' global stock equals sum of geography stocks',np.allclose(hg,np.array(list(country_stock.values())).sum(axis=0),rtol=1e-12))
    for i,y in enumerate(years):
        globalrows.append(dict(technology=tech,year=int(y),F_global=fg[i],H_global=hg[i],reported_geographies=int((included.Year==y).sum()),excluded_office_flow=float(raw.loc[raw.exclude_office&raw.Year.eq(y),'Coount'].sum()),total_geographies=len(country_stock)))
    cap=pd.read_excel(INP/'cost_capacity.xlsx',sheet_name='Capacity_'+suffix).set_index('Year').sort_index()
    cost=pd.read_excel(INP/'cost_capacity.xlsx',sheet_name='Cost_'+suffix)
    cost=cost.rename(columns={cost.columns[0]:'Year'}).set_index('Year')
    cumulative=cap.drop(columns=['Global_cum','Other_cum']).cumsum()
    ck(tech+' capacity cumulative reconstruction',np.allclose(cumulative.Global,cap.Global_cum,atol=1e-10,rtol=1e-12))
    for r in countries[countries.technology.eq(tech)].itertuples():
        patent_name={'South Korea':'Korea','United Kingdom':'Great Britain'}.get(r.country,r.country)
        hd=pd.Series(country_stock[patent_name],index=years)
        hs=oldstocks[(oldstocks.technology==tech)&(oldstocks.iso3==r.iso3)].set_index('year').H
        ck(tech+' '+r.iso3+' selected domestic stock reproduced',np.allclose(hd.loc[hs.index],hs,atol=1e-10,rtol=1e-12))
        start=2011 if tech=='wind' or r.iso3=='JPN' else 2010
        yrs=np.arange(start,2025)
        p=pd.DataFrame(dict(year=yrs,cost=cost.loc[yrs,r.country].to_numpy(float),Q_global=cap.loc[yrs,'Global_cum'].to_numpy(float),Q_domestic=cumulative.loc[yrs,r.country].to_numpy(float),H_domestic=hd.loc[yrs].to_numpy(float),H_global=pd.Series(hg,index=years).loc[yrs].to_numpy(float)))
        ck(tech+' '+r.iso3+' same complete positive-cost/capacity sample',p.notna().all().all() and p[['cost','Q_global','Q_domestic']].gt(0).all().all() and p[['H_domestic','H_global']].ge(0).all().all())
        ident=dict(technology=tech,iso3=r.iso3,country=r.country,country_cn=r.country_cn)
        panels.append(p.assign(**ident))
        y=np.log(p.cost.to_numpy())
        for spec,(q_scope,h_scope) in SPECS.items():
            regressors=[np.log(p['Q_'+q_scope].to_numpy())]
            if h_scope:regressors.append(np.log1p(p['H_'+h_scope].to_numpy()))
            X=sm.add_constant(np.column_stack(regressors));n,k=X.shape
            ck(tech+' '+r.iso3+' '+spec+' full rank',np.linalg.matrix_rank(X)==k)
            fit=sm.OLS(y,X).fit(use_t=True)
            robust=fit.get_robustcov_results(cov_type='HAC',maxlags=1,use_correction=True,use_t=True)
            ck(tech+' '+r.iso3+' '+spec+' coefficients independently reproduced',np.allclose(fit.params,np.linalg.lstsq(X,y,rcond=None)[0],atol=1e-10))
            meta=dict(**ident,spec=spec,Q_scope=q_scope,H_scope=h_scope or 'none',first_year=start,last_year=2024,N=n,p_mean=k,df_resid=n-k)
            # Gaussian likelihood criterion counts both mean coefficients and residual variance.
            K=k+1;aic=-2*fit.llf+2*K
            corr=np.corrcoef(X[:,1:].T)[0,1] if h_scope else np.nan
            vif=1/(1-corr**2) if h_scope else 1.
            row=dict(**meta,R2=fit.rsquared,adj_R2=fit.rsquared_adj,RMSE_log=float(np.sqrt(np.mean(fit.resid**2))),AIC=aic,AICc=aic+2*K*(K+1)/(n-K-1),BIC=-2*fit.llf+np.log(n)*K,VIF=vif,correlation_logQ_logH=corr,condition_standardized=np.linalg.cond(np.column_stack([np.ones(n),(X[:,1:]-X[:,1:].mean(axis=0))/X[:,1:].std(axis=0)])),a=fit.params[0],b=fit.params[1],g=fit.params[2] if h_scope else np.nan,p_HAC_b=robust.pvalues[1],p_HAC_g=robust.pvalues[2] if h_scope else np.nan,covariance_HAC=json.dumps(robust.cov_params().tolist()))
            for j,term in enumerate(['a','b','g'] if h_scope else ['a','b']):
                coefficients.append(dict(**meta,term=term,coefficient=fit.params[j],se_OLS=fit.bse[j],p_OLS=fit.pvalues[j],se_HAC=robust.bse[j],t_HAC=robust.tvalues[j],p_HAC=robust.pvalues[j],CI_HAC_lower=robust.conf_int()[j,0],CI_HAC_upper=robust.conf_int()[j,1]))
            errs=[]
            for year in range(2018,2025):
                train=p.year.to_numpy()<year;test=p.year.to_numpy()==year
                ck(tech+' '+r.iso3+' '+spec+' '+str(year)+' chronological holdout',train.sum()>=7 and p.year[train].max()<year)
                pred=float(X[test][0]@sm.OLS(y[train],X[train]).fit().params)
                err=pred-float(y[test][0]);errs.append(err)
                predictions.append(dict(**meta,test_year=year,training_N=int(train.sum()),training_last_year=year-1,actual_log=float(y[test][0]),prediction_log=pred,error_log=err))
            row['rolling_RMSE_log']=np.sqrt(np.mean(np.square(errs)));row['rolling_MAE_log']=np.mean(np.abs(errs));row['rolling_test_N']=len(errs)
            fits.append(row)
            for j,year in enumerate(yrs):samples.append(dict(**meta,year=int(year),actual_log=y[j],fitted_log=fit.fittedvalues[j],residual_log=fit.resid[j]))
            if spec==('GD' if tech=='pv' else 'G0'):
                prior=selected[selected.technology.eq(tech)&selected.iso3.eq(r.iso3)].iloc[0]
                differences={name:float(row[key]-prior[name]) for name,key in [('a','a'),('b_capacity','b'),('R2','R2'),('adj_R2','adj_R2'),('p_HAC_b','p_HAC_b')]}
                if h_scope:differences.update(g_knowledge=float(row['g']-prior.g_knowledge),p_HAC_g=float(row['p_HAC_g']-prior.p_HAC_g))
                ck('published replication '+tech+' '+r.iso3,max(abs(v) for v in differences.values())<1e-10 and n==prior.N)
                replication.append(dict(**ident,spec=spec,max_abs_difference=max(abs(v) for v in differences.values()),**differences))

fits=pd.DataFrame(fits);coef=pd.DataFrame(coefficients)
for (tech,spec),g in coef[coef.term!='a'].groupby(['technology','spec']):coef.loc[g.index,'q_BH_within_technology_spec']=multipletests(g.p_HAC,method='fdr_bh')[1]
for tech,g in coef[coef.term!='a'].groupby('technology'):coef.loc[g.index,'q_BH_all_explored_slopes_technology']=multipletests(g.p_HAC,method='fdr_bh')[1]
pairwise=[]
for (tech,iso),g in fits.groupby(['technology','iso3']):
    g=g.set_index('spec');base='GD' if tech=='pv' else 'G0'
    ck(tech+' '+iso+' global nested R2 monotonic',g.loc['GD','R2']>=g.loc['G0','R2']-1e-12 and g.loc['GG','R2']>=g.loc['G0','R2']-1e-12)
    ck(tech+' '+iso+' domestic nested R2 monotonic',g.loc['DD','R2']>=g.loc['D0','R2']-1e-12 and g.loc['DG','R2']>=g.loc['D0','R2']-1e-12)
    for alt in SPECS:
        if alt==base:continue
        d=dict(technology=tech,iso3=iso,country=g.loc[base,'country'],country_cn=g.loc[base,'country_cn'],current=base,alternative=alt)
        for metric in ['R2','adj_R2','AICc','BIC','rolling_RMSE_log']:
            current=float(g.loc[base,metric]);other=float(g.loc[alt,metric]);difference=current-other
            d[metric+'_current']=current;d[metric+'_alternative']=other;d[metric+'_current_minus_alternative']=difference
            favorable=difference if metric in ['R2','adj_R2'] else -difference
            d[metric+'_current_better']=favorable>1e-10;d[metric+'_tie']=abs(difference)<=1e-10
        pairwise.append(d)
pairwise=pd.DataFrame(pairwise)
summary=[]
for (tech,alt),g in pairwise.groupby(['technology','alternative']):
    row=dict(technology=tech,current=g.current.iloc[0],alternative=alt,countries=len(g))
    for m in ['R2','adj_R2','AICc','BIC','rolling_RMSE_log']:
        row[m+'_current_better']=int(g[m+'_current_better'].sum());row[m+'_ties']=int(g[m+'_tie'].sum());row[m+'_median_difference']=g[m+'_current_minus_alternative'].median()
    summary.append(row)
summary=pd.DataFrame(summary)
for name,df in [('patent_flows_and_stocks',pd.DataFrame(flows)),('global_patent_stock',pd.DataFrame(globalrows)),('matched_input_panel',pd.concat(panels,ignore_index=True)),('all_model_fits',fits),('all_coefficients',coef),('all_fitted_values',pd.DataFrame(samples)),('rolling_predictions',pd.DataFrame(predictions)),('current_model_replication',pd.DataFrame(replication)),('pairwise_current_vs_alternatives',pairwise),('pairwise_summary',summary)]:
    df.to_csv(OUT/f'{name}.csv',index=False,encoding='utf-8-sig')
modelsummary=fits.groupby(['technology','spec']).agg(countries=('iso3','size'),median_R2=('R2','median'),median_adj_R2=('adj_R2','median'),median_AICc=('AICc','median'),median_rolling_RMSE_log=('rolling_RMSE_log','median'),median_VIF=('VIF','median'),negative_b=('b',lambda s:int((s<0).sum())),negative_g=('g',lambda s:int((s<0).sum())),HAC_p_g_lt_05=('p_HAC_g',lambda s:int((s<.05).sum()))).reset_index()
modelsummary.to_csv(OUT/'model_summary.csv',index=False,encoding='utf-8-sig')
audit=dict(passed=all(c['passed'] for c in checks),checks=checks,input_manifest=manifest,specs=SPECS,models=len(fits),country_technology_pairs=25,delta=.1,lag=0,initialization='H2008=F2008/0.1; Ht=.9H[t-1]+Ft for t>=2009',global_patents='Sum of all reported country/geography flows, excluding EPO/WIPO/EAPO; not validated globally unique patent families',domestic_capacity='Cumulative sum of country columns from the source 2000 initial row through year t; global accumulation independently matched to supplied Global_cum',missing_patents='Unlisted country-years assumed zero under frozen convention; not confirmed zero observations',sample='PV 2010-2024 except Japan 2011-2024; all wind 2011-2024; identical years for every spec within country/technology',inference='HAC(1) Bartlett with n/(n-p) correction, two-sided Student t; raw p and BH across slopes within tech/spec and all explored tech slopes',AICc='-2LL+2K+2K(K+1)/(n-K-1), K=mean coefficient count+1 residual variance',rolling='2018-2024 expanding chronological cost holdout, contemporaneous regressors known, input costs retain prior interpolation; retrospective conditional prediction, not a real-time forecasting experiment',model_selection='Exploratory comparison only; no automatic replacement of selected PV/wind models or downstream costs/CGE',software=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,statsmodels=statsmodels.__version__))
(ROOT/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print(summary[['technology','current','alternative','countries','R2_current_better','adj_R2_current_better','AICc_current_better','rolling_RMSE_log_current_better']].to_string(index=False))
print('PASS',len(checks),'checks;',len(fits),'fits')
