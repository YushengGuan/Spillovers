"""OLS and calendar-adjacent HAC(1) refits of the archived model designs.

This refits both level and difference specifications. Missing calendar years
are not treated as adjacent observations. No imputed TIC observations enter
these regression samples.
"""
from pathlib import Path
import json, os
import numpy as np
import pandas as pd
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ['SPILLOVERS_OUTPUT'])/'regressions'
OUT.mkdir(parents=True,exist_ok=True)
checks=[]
for group in ['equipment','other_costs']:
    samples=pd.read_csv(ROOT/f'data/regressions/{group}/fit_samples.csv')
    archived=pd.read_csv(ROOT/f'data/regressions/{group}/coefficients.csv')
    rows=[]
    for model_id, coeff in archived.groupby('model_id',sort=False):
        d=samples[samples.model_id.eq(model_id)].sort_values('year')
        terms=coeff.term.tolist()
        x=np.column_stack([np.ones(len(d)) if term=='const' else d['x' if term=='lnQ' else term].to_numpy() for term in terms])
        y=d.y.to_numpy();n,k=x.shape
        beta=np.linalg.lstsq(x,y,rcond=None)[0]
        residual=y-x@beta
        xu=x*residual[:,None]
        meat=xu.T@xu
        years=d.year.to_numpy()
        for i in range(1,n):
            if years[i]-years[i-1]==1:
                cross=np.outer(xu[i],xu[i-1]);meat+=0.5*(cross+cross.T)
        bread=np.linalg.inv(x.T@x)
        cov=(bread@meat@bread)*n/(n-k)
        se=np.sqrt(np.diag(cov));p=2*t.sf(np.abs(beta/se),n-k)
        for j,term in enumerate(terms):
            old=coeff.iloc[j]
            for field,value in [('coefficient',beta[j]),('SE_HAC',se[j]),('p_HAC_raw',p[j])]:
                assert np.isclose(value,old[field],rtol=2e-5,atol=1e-8),(group,model_id,term,field,value,old[field])
            rows.append(dict(model_id=model_id,term=term,n=n,coefficient=beta[j],SE_HAC=se[j],p_HAC_raw=p[j],CI95_low=beta[j]-t.ppf(.975,n-k)*se[j],CI95_high=beta[j]+t.ppf(.975,n-k)*se[j]))
        checks.append(dict(group=group,model_id=model_id,n=n,terms=terms,status='PASS'))
    pd.DataFrame(rows).to_csv(OUT/f'{group}_refitted_coefficients.csv',index=False)
(OUT/'validation.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {len(checks)} regression specifications reproduce coefficients, HAC SEs and p values.')
