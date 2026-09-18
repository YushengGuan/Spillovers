"""Build, solve, or export the CGE model using the repository Julia environment."""
from pathlib import Path
import argparse, os, shutil, subprocess

ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['check','solve','export'])
    p.add_argument('--julia',default=os.environ.get('JULIA',shutil.which('julia')))
    a=p.parse_args()
    if not a.julia:p.error('Julia not found; use --julia /path/to/julia or set JULIA.')
    if a.action=='solve' and not os.environ.get('PATH_LICENSE_STRING'):
        p.error('Set your own PATH_LICENSE_STRING before solving the full model.')
    scenarios={'check':['CHECK'],'solve':['A','B','C','EXPORT'],'export':['EXPORT']}[a.action]
    if a.action=='export' and not os.environ.get('PATH_LICENSE_STRING'):
        p.error('Set PATH_LICENSE_STRING for the Julia export runner, or use the supplied CSV exports.')
    env=os.environ.copy();env.pop('LEGACY_RUN_ID',None)
    for scenario in scenarios:
        subprocess.run([a.julia,'--startup-file=no',f'--project={ROOT}',str(ROOT/'src/runner.jl'),
                        str(ROOT),'fiveyear_2050',scenario,'2050'],cwd=ROOT,env=env,check=True)
if __name__=='__main__':main()
