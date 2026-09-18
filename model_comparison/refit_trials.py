"""Refit supplemental alternatives from archived model-specific estimation samples.

The samples already contain any differencing/transformation used by each model.
HAC(1) uses adjacent calendar years, Bartlett weights and the n/(n-k) correction.
These alternatives do not replace the selected equations used by the cost pipeline.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import t

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
rows=[];checks=[]
for folder in sorted((ROOT/'trials').iterdir()):
    samples=pd.read_csv(next(folder.glob('*fit_samples.csv')))
    coefficients=pd.read_csv(next(folder.glob('*coefficients.csv')))
    for mid,archive in coefficients.groupby('model_id',sort=False):
        z=samples[samples.model_id.eq(mid)].sort_values('year')
        terms=archive.term.tolist()
        ycol=next(c for c in ['y','logp','logC'] if c in z and z[c].notna().all())
        X=np.column_stack([np.ones(len(z)) if term=='const' else z[term].to_numpy() for term in terms])
        f=sm.OLS(z[ycol].to_numpy(),X).fit();n,k=X.shape
        scores=X*f.resid[:,None];meat=scores.T@scores;years=z.year.to_numpy()
        for i in range(1,n):
            if years[i]-years[i-1]==1:
                cross=np.outer(scores[i],scores[i-1]);meat+=.5*(cross+cross.T)
        bread=np.linalg.inv(X.T@X);cov=bread@meat@bread*n/(n-k)
        se=np.sqrt(np.maximum(0,np.diag(cov)))
        for j,(_,a) in enumerate(archive.iterrows()):
            rows.append(dict(group=folder.name,model_id=mid,term=a.term,n=n,coefficient=f.params[j],
                             SE_HAC=se[j],p_HAC_raw=2*t.sf(abs(f.params[j]/se[j]),n-k),R2=f.rsquared))
            checks.append(dict(group=folder.name,model_id=mid,term=a.term,
                               coefficient_error=abs(f.params[j]-a.coefficient),SE_error=abs(se[j]-a.SE_HAC)))
r=pd.DataFrame(rows);c=pd.DataFrame(checks)
r.to_csv(OUT/'refitted_coefficients.csv',index=False)
c.to_csv(OUT/'refit_checks.csv',index=False)
assert c.coefficient_error.max()<1e-7
assert c.SE_error.max()<1e-6
summary={'models':r[['group','model_id']].drop_duplicates().shape[0],
         'max_coefficient_error':float(c.coefficient_error.max()),'max_SE_error':float(c.SE_error.max()),
         'prepared_samples':True,'all_pass':True}
(OUT/'refit_audit.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
