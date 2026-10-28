"""Refresh release manifests after an intentional, reviewed source update.

Do not use this to bypass a failed integrity check on an unreviewed download.
Runtime outputs and local external CGE inputs are not release files.
"""
from pathlib import Path
import csv, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'outputs','.cge_runtime','.git','.venv','__pycache__','.pytest_cache'}
def included(p):
    rel=p.relative_to(ROOT)
    return not any(x in EXCLUDED for x in rel.parts) and not str(rel).replace('\\','/').startswith(('cge/model/input/','cge/model/param/')) and p.name not in ['.env','file_manifest.json'] and p.suffix not in ['.pyc','.log','.jls']
def main():
    csvs=[]
    for p in sorted(ROOT.rglob('*.csv')):
        if not included(p):continue
        with p.open(encoding='utf-8-sig',newline='') as stream:
            reader=csv.reader(stream);columns=next(reader,[]);rows=sum(1 for _ in reader)
        csvs.append(dict(file=p.relative_to(ROOT).as_posix(),rows=rows,columns=columns))
    (ROOT/'provenance/csv_inventory.json').write_text(json.dumps(csvs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or not included(p):continue
        rows.append(dict(file=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    (ROOT/'provenance/file_manifest.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print(f'Manifest: {len(rows)} files, {sum(x["bytes"] for x in rows)/1e6:.1f} MB; {len(csvs)} CSV tables.')
if __name__=='__main__':main()
