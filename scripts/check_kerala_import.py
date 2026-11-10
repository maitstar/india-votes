"""Check the committed import with standard-library tools; no network required."""
from pathlib import Path
import csv,hashlib,json,collections
root=Path(__file__).resolve().parents[1]/'data/imports/kerala'
m=json.loads((root/'manifest.json').read_text())
for name,v in m['outputs'].items():
 assert hashlib.sha256((root/name).read_bytes()).hexdigest()==v['sha256'],name
rows=list(csv.DictReader((root/'candidate-results.csv').open()))
assert len(rows)==4433
byyear=collections.defaultdict(set)
for row in rows:
 assert int(row['total_votes'])>=0
 byyear[row['election_year']].add(int(row['constituency_no']))
assert set(byyear)=={'2011','2016','2021','2026'}
assert all(ids==set(range(1,141)) for ids in byyear.values())
post=list(csv.DictReader((root/'assembly-to-parliament-post2008.csv').open()))
assert len(post)==140 and len({r['ac_no'] for r in post})==140
assert len({r['pc_no'] for r in post})==20
ponnani=next(r for r in post if r['ac_no']=='48')
assert ponnani['pc_no']=='7' and ponnani['pc_name'].lower()=='ponnani'
pre=list(csv.DictReader((root/'assembly-to-parliament-pre2008.csv').open()))
assert next(r for r in pre if r['ac_no']=='48')['ac_name'].lower()=='malampuzha'
v=json.loads((root/'validation.json').read_text())
assert not v['applicationAtlasChanged']
assert len(v['winnerVoteDiscrepancies'])==10
assert 'quarantined' in v['mappingCoverage']['pre2008']['status']
print('PASS: checksums, 4,433 rows, all 140 seats per cycle, era-specific Ponnani mapping and unresolved-record quarantine.')
