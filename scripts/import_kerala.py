"""Import pinned upstream Kerala data without overwriting the application atlas.
Requires pandas and pyarrow. Pass --cache PATH to reuse downloaded source files.
"""
import argparse,csv,hashlib,json,re,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULTS='1fe9a2e00d3ca451e95be46e753d71af0ede78fe'
MAPS='efceae39d3922f04fc5ea91106b7b316bf8ddf8f'
SOURCES={
 'assembly.parquet':f'https://raw.githubusercontent.com/skthewimp/elections/{RESULTS}/assembly/data/assembly_candidate_results_since_2009.parquet',
 'ac_pc_post2008.csv':f'https://raw.githubusercontent.com/skthewimp/india-constituency-maps/{MAPS}/mappings/ac_pc_post2008.csv',
 'ac_pc_pre2008.csv':f'https://raw.githubusercontent.com/skthewimp/india-constituency-maps/{MAPS}/mappings/ac_pc_pre2008.csv'}
EXPECTED_SHA256={'assembly.parquet': '646734f553c5662a185dd14ba6f54a33d99e6608fd89e8e66a434649489d5e9b', 'ac_pc_post2008.csv': 'c2197e521eb1192d6912a5cf10788043ccc324f7b2dd6386e5525287e7da0f3f', 'ac_pc_pre2008.csv': '815b142f461a45a0b04ac974ccfc1604f65fb18286e939ca6f1e9f91e6f167b1'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 import pandas as pd
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache',type=Path);args=p.parse_args()
 cache=args.cache or ROOT/'.cache/kerala-import';cache.mkdir(parents=True,exist_ok=True)
 out=ROOT/'data/imports/kerala';out.mkdir(parents=True,exist_ok=True)
 for name,url in SOURCES.items():
  target=cache/name
  if not target.exists():
   with urllib.request.urlopen(url,timeout=90) as r:target.write_bytes(r.read())
  if digest(target)!=EXPECTED_SHA256[name]:raise ValueError(f"Source checksum mismatch: {name}")
 frame=pd.read_parquet(cache/'assembly.parquet');frame=frame[frame.state_name.eq('Kerala')].copy()
 # Only the four general-election cycles supplied in this pinned archive.
 assert set(frame.election_year)=={2011,2016,2021,2026}
 assert frame.total_votes.notna().all() and (frame.total_votes>=0).all()
 assert (frame.total_votes%1==0).all()
 frame['total_votes']=frame.total_votes.astype('int64')
 frame=frame.sort_values(['election_year','constituency_no','position','candidate'])
 frame.to_csv(out/'candidate-results.csv',index=False)
 mappings={}
 for era in ['pre2008','post2008']:
  d=pd.read_csv(cache/f'ac_pc_{era}.csv');d=d[d.st_code.eq('S11')].sort_values('ac_no')
  assert len(d)==140 and d.ac_no.nunique()==140
  d.to_csv(out/f'assembly-to-parliament-{era}.csv',index=False)
  mappings[era]={'assemblySeats':len(d),'distinctParliamentSeats':int(d.pc_no.nunique()),'era':era,'status':'reference-only; not a boundary crosswalk between eras' if era=='post2008' else 'quarantined: only 18 distinct parent seats; requires independent review'}
 atlas=json.loads((ROOT/'data/atlas.json').read_text());latest=next(s for s in atlas['states'] if s['code']=='KL')
 summary=[];differences=[]
 for year,g in frame.groupby('election_year'):
  snapshot=latest if latest['year']==year else atlas['elections']['KL'][str(year)]
  seats=g.groupby('constituency_no');assert seats.ngroups==140
  winner_matches=0
  for no,candidates in seats:
   candidates=candidates[~candidates.candidate.str.lower().isin(['nota','none of the above'])].sort_values('total_votes',ascending=False)
   winner=candidates.iloc[0];current=next(c for c in snapshot['seats'][str(no)]['candidates'] if c['party']!='NOTA')
   same=current['votes']==int(winner.total_votes);winner_matches+=int(same)
   if not same:
    differences.append({'year':int(year),'assemblySeatId':int(no),'constituency':winner.constituency_name,'atlasCandidate':current['name'],'atlasWinnerVotes':current['votes'],'upstreamCandidate':winner.candidate,'upstreamWinnerVotes':int(winner.total_votes),'differenceUpstreamMinusAtlas':int(winner.total_votes)-current['votes'],'status':'unresolved; neither source adjudicated against official report'})
  summary.append({'year':int(year),'seats':140,'rowsIncludingNOTAWherePresent':len(g),'winnerVoteTotalsMatchingAtlas':winner_matches,'winnerVoteTotalsDiffering':140-winner_matches,'sourceKinds':sorted(g.source_kind.dropna().unique().tolist())})
 report={'reviewDate':'2026-11-10','scope':'Kerala general-election result rows and AC-PC reference mappings. No IndiaVotes website scraping.','applicationAtlasChanged':False,'elections':summary,'winnerVoteDiscrepancies':differences,'mappingCoverage':mappings,'limitations':['Matching winner vote totals is not verification of candidate identity, complete rosters, runner-up totals, party labels or official accuracy.','2011/2016 atlas-versus-upstream discrepancies require official report checks.','The pre-2008 mapping is quarantined pending review; do not match eras by constituency number or name alone.','Election-month metadata is retained verbatim and is not independently verified.','No pre-2011 results were supplied by this pinned results bundle.']}
 (out/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 manifest={'retrievedDate':'2026-11-10','upstreamCommits':{'results':RESULTS,'maps':MAPS},'inputs':{n:{'url':u,'sha256':digest(cache/n)} for n,u in SOURCES.items()},'outputs':{f.name:{'sha256':digest(f),'bytes':f.stat().st_size} for f in sorted(out.glob('*')) if f.name!='manifest.json'},'reuse':'Retain archive MIT notices and boundary attribution; third-party underlying data retain their terms. See docs/KERALA_IMPORT.md.'}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'resultRows':len(frame),'elections':len(summary),'winnerVoteDiscrepancies':len(differences),'output':str(out)},indent=2))
if __name__=='__main__':main()
