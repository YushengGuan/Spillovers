"""Validate checksums, Python syntax and accidental local/credential inclusion."""
from pathlib import Path
import ast, hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'provenance/file_manifest.json').read_text(encoding='utf-8'))
errors=[]
for row in manifest:
    p=ROOT/row['file']
    if not p.is_file():errors.append(row['file']+': missing');continue
    if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:errors.append(row['file']+': checksum mismatch')
    if p.suffix=='.py':
        try:ast.parse(p.read_text(encoding='utf-8-sig'),filename=row['file'])
        except SyntaxError:errors.append(row['file']+': Python syntax error')
    if p.suffix in ['.py','.jl','.json','.toml','.md','.yml','.cff','.csv']:
        s=p.read_text(encoding='utf-8-sig')
        if re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]',s):errors.append(row['file']+': absolute Windows path')
        if re.search(r'c_api_License_SetString\("[^"\n]+"\)',s):errors.append(row['file']+': embedded solver licence')
        if re.search(r'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{25,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)',s):errors.append(row['file']+': credential-like content')
    if p.stat().st_size>40_000_000:errors.append(row['file']+': unexpectedly large file')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(manifest)} release files; checksums, Python syntax and local-secret checks.')
