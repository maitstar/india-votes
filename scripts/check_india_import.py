"""Offline integrity and accounting checks for the committed nationwide import."""
import collections,csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];data=ROOT/'data/imports/india'
manifest=json.loads((data/'manifest.json').read_text())
for name,record in manifest['outputs'].items():
 path=data/name
 assert path.stat().st_size==record['bytes'],name
 assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],name
report=json.loads((data/'validation.json').read_text())
assert report['applicationAtlasChanged'] is False
historical=[r for r in report['coverage'] if r['source']=='historical-assembly']
recent=[r for r in report['coverage'] if r['source']=='recent-assembly']
assert len(historical)==report['historicalElectionIds']==119
assert len({r['state'] for r in historical})==report['historicalStateLabels']==31
assert sum(r['rows'] for r in historical)==report['historicalRows']==161760
partitions=collections.Counter()
for path in (data/'assembly-by-state').glob('*.csv'):
 with path.open() as f:
  for row in csv.DictReader(f):partitions[row['election_id']]+=1
assert partitions==collections.Counter({r['electionId']:r['rows'] for r in historical})
assert len(recent)==report['recentFiles']==20
assert sum(r['rows'] for r in recent)==report['recentRows']==32563
for r in recent:
 with (data/'recent-assembly'/r['file']).open() as f:rows=list(csv.DictReader(f))
 assert len(rows)==r['rows']
 assert len({x['constituency_no'] for x in rows})==r['seats']
for r in report['coverage']:
 assert r.get('comparedSeats',0)==r.get('winnerVoteTotalsMatching',0)+r.get('winnerVoteTotalsDiffering',0)
differences=json.loads((data/'assembly-winner-discrepancies.json').read_text())
assert len(differences)==sum(r.get('winnerVoteTotalsDiffering',0) for r in report['coverage'])==263
issues=json.loads((data/'historical-vote-issues.json').read_text())
assert collections.Counter(x['reason'] for x in issues)=={'missing':542,'fractional':2703}
for era in ['pre2008','post2008']:
 with (data/f'ac_pc_{era}.csv').open() as f:rows=list(csv.DictReader(f))
 assert len(rows)==sum(r['rows'] for r in report['mappingCoverage'] if r['era']==era)
n=report['national']['2024'];assert n['seats']==543 and n['comparedSeats']==n['matchingWinnerVotes']==542
assert not n['unmatchedSeats'] and not n['discrepancies']
assert len(n['nonNumericVoteRows'])==1 and n['nonNumericVoteRows'][0]['constituency']=='Surat'
with (data/'lok-sabha-2019-atlas-export.csv').open() as f:rows=list(csv.DictReader(f))
assert len({r['seat_id'] for r in rows})==543
assert len(rows)==report['national']['2019']['rows']==8570
print('PASS: nationwide hashes, state partitions, coverage, unresolved-row accounting, mapping counts and national exports.')
