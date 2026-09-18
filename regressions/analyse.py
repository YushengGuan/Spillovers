"""Diagnostics of the selected archived equations; never bridge calendar gaps."""
from pathlib import Path
import hashlib, json, warnings
import numpy as np
import pandas as pd
import scipy, scipy.stats as st
import statsmodels, statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent/'results'
OUT.mkdir(parents=True,exist_ok=True)
PRICE = ROOT/'regressions/data/equipment'
BAL = ROOT/'regressions/data/balance'
sources = [PRICE/x for x in ['accepted_models.csv','accepted_coefficients.csv','pv_regression_panel.csv','wind_regression_panel.csv']] + [BAL/x for x in ['models.csv','coefficients.csv','fit_samples.csv']]
pm, pc, pv, wind, bm, bc, bs = [pd.read_csv(p) for p in sources]
models=[]
for m in pm[pm.spec.eq('main_level')].itertuples():
    if m.technology=='pv':
        z=pv[pv.iso3.eq(m.series)].rename(columns={'logP':'y'}).copy(); terms=['logQ','logM']
    else:
        z=wind[wind.series.eq(m.series)].rename(columns={'logp':'y'}).copy();terms=['logQ']
    years=[int(v) for v in m.years.split(',')]
    z=z[z.year.isin(years)][['year','y']+terms].sort_values('year').dropna()
    assert z.year.tolist()==years
    models.append(dict(id=m.model_id.replace('__main_level',''),group='equipment',technology=m.technology,series=m.series,z=z,terms=terms,arch=pc[pc.technology.eq(m.technology)&pc.series.eq(m.series)]))
for m in bm[bm.spec.eq('main_level')].itertuples():
    z=bs[bs.model_id.eq(m.model_id)][['year','y','x']].rename(columns={'x':'logQ'}).sort_values('year')
    arch=bc[bc.technology.eq(m.technology)&bc.iso3.eq(m.iso3)].copy();arch['term']=arch.term.replace({'lnQ':'logQ'})
    models.append(dict(id=m.model_id.replace('__main_level','')+'__balance',group='balance',technology=m.technology,series=m.iso3,z=z,terms=['logQ'],arch=arch))

def fit(z,terms):
    X=sm.add_constant(z[terms],has_constant='add').to_numpy();y=z.y.to_numpy();years=z.year.to_numpy()
    f=sm.OLS(y,X).fit();n,k=X.shape
    score=X*f.resid[:,None];meat=score.T@score
    for i in range(1,n):
        if years[i]-years[i-1]==1:
            cross=np.outer(score[i],score[i-1]);meat+=0.5*(cross+cross.T)
    bread=np.linalg.inv(X.T@X);cov=bread@meat@bread*n/(n-k)
    se=np.sqrt(np.maximum(0,np.diag(cov)));ps=2*st.t.sf(np.abs(f.params/se),n-k);q=st.t.ppf(.975,n-k)
    return f,se,ps,f.params-q*se,f.params+q*se

coeff=[]; diag=[]; sample=[];checks=[]
for m in models:
    z=m['z'].copy();base={k:m[k] for k in ['id','group','technology','series']}
    for spec in ['main_level','annual_difference','time_trend']:
        terms=m['terms'].copy();v=z.copy()
        if spec=='annual_difference':
            v[['y']+terms]=v[['y']+terms].diff();v=v[z.year.diff().eq(1)].copy()
        if spec=='time_trend':v['trend']=v.year-v.year.min();terms+=['trend']
        f,se,ps,lo,hi=fit(v,terms)
        for j,term in enumerate(['const']+terms):
            row={**base,'spec':spec,'term':term,'n':len(v),'df_resid':int(f.df_resid),'years':','.join(map(str,v.year.tolist())),'coefficient':f.params[j],'SE_HAC':se[j],'p_raw':ps[j],'CI95_low':lo[j],'CI95_high':hi[j],'R2':f.rsquared}
            if term=='logQ':row.update(LR_pct=100*(1-2**f.params[j]),LR_CI95_low=100*(1-2**hi[j]),LR_CI95_high=100*(1-2**lo[j]))
            coeff.append(row)
            if spec!='time_trend':
                a=m['arch'];a=a[a.spec.eq(spec)&a.term.eq(term)].iloc[0]
                checks.append({'id':m['id'],'spec':spec,'term':term,'coef_abs_error':abs(f.params[j]-a.coefficient),'se_abs_error':abs(se[j]-a.SE_HAC)})
        for r in v.to_dict('records'):sample.append({**base,'spec':spec,**r})
    # Longest contiguous complete annual block; ties choose earliest, independent of results.
    blocks=[v for _,v in z.groupby(z.year.diff().ne(1).cumsum())]
    block=max(blocks,key=len);n=len(block)
    info={**base,'full_n':len(z),'n_block':n,'block_years':','.join(map(str,block.year.tolist())),'status':'computed' if n>=10 else 'not_computed_fewer_than_10_contiguous_years'}
    for lag in [1,0]:
        for deterministic in ['c','ct']:
            for var in ['y']+m['terms']:
                row={**info,'test':'ADF','variable':var,'deterministic':deterministic,'lag':lag}
                if n>=10:
                    ans=adfuller(block[var],regression=deterministic,maxlag=lag,autolag=None)
                    row.update(statistic=ans[0],p_raw=ans[1],test_nobs=ans[3],critical_1pct=ans[4]['1%'],critical_5pct=ans[4]['5%'],critical_10pct=ans[4]['10%'])
                diag.append(row)
            row={**info,'test':'Engle_Granger','variable':'y~'+'+'.join(m['terms']),'deterministic':deterministic,'lag':lag}
            if n>=10:
                with warnings.catch_warnings(record=True) as ws:
                    ans=coint(block.y,block[m['terms']],trend=deterministic,maxlag=lag,autolag=None)
                row.update(statistic=ans[0],p_raw=ans[1],critical_1pct=ans[2][0],critical_5pct=ans[2][1],critical_10pct=ans[2][2],warnings='; '.join(str(w.message) for w in ws))
            diag.append(row)

c=pd.DataFrame(coeff);d=pd.DataFrame(diag);ck=pd.DataFrame(checks)
assert ck.coef_abs_error.max()<1e-8
assert ck.se_abs_error.max()<1e-7
# BH families for the explanatory deployment slope within outcome group, technology and specification.
for _,g in c[c.term.eq('logQ')].groupby(['group','technology','spec']):c.loc[g.index,'q_BH']=multipletests(g.p_raw,method='fdr_bh')[1]
# Deduplicate shared predictor tests within each family before BH adjustment.
for _,g in d[d.status.eq('computed')].groupby(['group','technology','test','deterministic','lag']):
    keys=[]
    for i,r in g.iterrows():
        m=next(m for m in models if m['id']==r.id);b=m['z'][m['z'].year.isin([int(y) for y in r.block_years.split(',')])]
        vars=[r.variable] if r.test=='ADF' else ['y']+m['terms']
        key=hashlib.sha256(b[['year']+vars].to_numpy().tobytes()).hexdigest();keys.append((i,key))
    unique={}
    for i,key in keys:unique.setdefault(key,d.loc[i,'p_raw'])
    q=dict(zip(unique,multipletests(list(unique.values()),method='fdr_bh')[1]))
    for i,key in keys:d.loc[i,'q_BH']=q[key]

c.to_csv(OUT/'coefficient_comparison.csv',index=False)
d.to_csv(OUT/'time_series_diagnostics.csv',index=False)
pd.DataFrame(sample).to_csv(OUT/'analysis_samples.csv',index=False)
ck.to_csv(OUT/'archive_reproduction_checks.csv',index=False)
summary={'models':len(models),'max_archived_coefficient_error':ck.coef_abs_error.max(),'max_archived_SE_error':ck.se_abs_error.max(),'versions':{'statsmodels':statsmodels.__version__,'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__},'sources':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources]}
(OUT/'audit.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
print(c[c.term.eq('logQ')&c.group.eq('equipment')][['technology','series','spec','n','coefficient','p_raw','LR_pct']].to_string(index=False))
eg=d[d.test.eq('Engle_Granger')&d.lag.eq(1)&d.deterministic.eq('c')]
print('EG lag1 constant:');print(eg[['group','technology','series','n_block','status','p_raw','q_BH']].to_string(index=False))
