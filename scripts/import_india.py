"""Pull all pinned result bundles and mappings; retain raw issues, never overwrite atlas.
Install scripts/requirements-import.txt. Use --cache DIR for existing downloads.
"""
import argparse,collections,csv,hashlib,json,re,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(v):return re.sub('[^a-z0-9]','',str(v).lower())
def statekey(v):
 key=norm(v)
 return {"nctofdelhi":"delhi","jammuandkashmir":"jammukashmir"}.get(key,key)
def nota(v):return norm(v) in {'nota','noneoftheabove','noneoftheabovenota'}
def writejson(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def writecsv(path,rows,fields):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def main():
 import pandas as pd
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache',type=Path);a=p.parse_args()
 cache=a.cache or ROOT/'.cache/india-import';cache.mkdir(parents=True,exist_ok=True)
 out=ROOT/'data/imports/india';out.mkdir(parents=True,exist_ok=True)
 lock=json.loads((ROOT/'scripts/india-source-lock.json').read_text())
 for name,s in lock['sources'].items():
  target=cache/name
  if not target.exists():subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','90',s['url'],'-o',str(target)],check=True)
  if sha(target)!=s['sha256']:raise ValueError('Checksum mismatch: '+name)
  if 'gitBlobSHA' in s:
   content=target.read_bytes();blob=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
   if blob!=s['gitBlobSHA']:raise ValueError('Upstream blob mismatch: '+name)
 atlas=json.loads((ROOT/'data/atlas.json').read_text());byname={norm(s['name']):s['code'] for s in atlas['states']};byname['nctofdelhi']='DL'
 snapshots={}
 for code,years in atlas['elections'].items():
  for year,s in years.items():snapshots[(code,int(year))]=next(x for x in atlas['states'] if x['code']==code) if s.get('latestRef') else s
 frame=pd.read_parquet(cache/'assembly.parquet')
 shutil.copy2(cache/'assembly.parquet',out/'assembly-source.parquet')
 historical=out/'assembly-by-state';historical.mkdir(exist_ok=True)
 for state,g in frame.groupby('state_name'):
  filename=byname.get(norm(state),norm(state))+'.csv';g.to_csv(historical/filename,index=False)
 summary=[];discrepancies=[];issues=[]
 def compare(groups,code,year,source,invalid_seats=set(),date_uncertain=False):
  s=snapshots.get((code,int(year)));counts=collections.Counter()
  if not s:return {'atlasSnapshotAvailable':False,'comparedSeats':0}
  for seat_id,rows in groups.items():
   if seat_id in invalid_seats or date_uncertain:counts['skippedUnresolvedSeats']+=1;continue
   seat=s['seats'].get(str(int(seat_id)))
   if not seat:counts['unmatchedSeatIds']+=1;continue
   candidates=[r for r in rows if not nota(r['candidate']) and r['votes'] is not None]
   if not candidates:counts['skippedUnresolvedSeats']+=1;continue
   top=max(candidates,key=lambda r:r['votes']);winner=next(c for c in seat['candidates'] if not nota(c['party']))
   counts['comparedSeats']+=1
   if winner['votes']==top['votes']:counts['winnerVoteTotalsMatching']+=1
   else:
    counts['winnerVoteTotalsDiffering']+=1
    discrepancies.append({'source':source,'stateCode':code,'year':int(year),'seatId':str(int(seat_id)),'constituency':seat['name'],'atlasCandidate':winner['name'],'atlasVotes':winner['votes'],'upstreamCandidate':top['candidate'],'upstreamVotes':top['votes'],'status':'unresolved; no automatic overwrite'})
  return {'atlasSnapshotAvailable':True,'expectedAtlasSeats':s['total'],**counts}
 for eid,g in frame.groupby('election_id',sort=True):
  state=str(g.iloc[0].state_name);year=int(g.iloc[0].election_year);code=byname.get(norm(state));votes=g.total_votes
  flags={'missingVoteRows':int(votes.isna().sum()),'negativeVoteRows':int((votes<0).sum()),'fractionalVoteRows':int(((votes.fillna(0)%1)!=0).sum()),'missingMonthRows':int(g.election_month.isna().sum())}
  bad=g[votes.isna()|(votes<0)|((votes.fillna(0)%1)!=0)]
  badseats=set(bad.constituency_no.tolist())
  for idx,row in bad.iterrows():
   value=row.total_votes
   issues.append({'electionId':eid,'sourceRowIndex':int(idx),'constituencyNo':int(row.constituency_no),'candidate':row.candidate,'rawTotalVotes':None if pd.isna(value) else float(value),'reason':'missing' if pd.isna(value) else 'negative' if value<0 else 'fractional'})
  groups={int(n):[{'candidate':r.candidate,'votes':None if pd.isna(r.total_votes) else float(r.total_votes)} for r in h.itertuples()] for n,h in g.groupby('constituency_no')}
  audit=compare(groups,code,year,'historical-assembly',badseats,flags['missingMonthRows']>0)
  summary.append({'source':'historical-assembly','electionId':str(eid),'state':state,'stateCode':code,'sourceYear':year,'rows':len(g),'seats':len(groups),'sourceKinds':sorted(g.source_kind.dropna().unique().tolist()),'quality':flags,'reviewRequired':bool(sum(flags.values()) or audit.get('winnerVoteTotalsDiffering',0)),**audit})
 recent=out/'recent-assembly';recent.mkdir(exist_ok=True)
 for name in sorted(n for n in lock['sources'] if 'Assembly-' in n):
  shutil.copy2(cache/name,recent/name);rows=list(csv.DictReader((cache/name).open()));groups=collections.defaultdict(list);badseats=set();badrows=0
  for r in rows:
   seat=int(r['constituency_no']);parts=[r['evm_votes'].replace(',','').strip(),r['postal_votes'].replace(',','').strip()]
   if not all(v.isdigit() for v in parts):votes=None;badseats.add(seat);badrows+=1
   else:votes=sum(map(int,parts))
   groups[seat].append({'candidate':r['candidate'],'votes':votes})
  year=int(rows[0]['election_year']);code=rows[0]['election_state']
  summary.append({'source':'recent-assembly','file':name,'stateCode':code,'sourceYear':year,'rows':len(rows),'seats':len(groups),'invalidVoteRows':badrows,**compare(groups,code,year,'recent-assembly',badseats)})
 for record in summary:
  if record['source']=='recent-assembly':record['reviewRequired']=bool(record['invalidVoteRows'] or record.get('winnerVoteTotalsDiffering',0))
 mappings=[]
 for era in ['pre2008','post2008']:
  name=f'ac_pc_{era}.csv';shutil.copy2(cache/name,out/name);d=pd.read_csv(cache/name)
  for state,g in d.groupby('st_code'):
   mappings.append({'era':era,'stateCode':state,'state':str(g.iloc[0].st_name),'rows':len(g),'uniqueAssemblyIds':int(g.ac_no.nunique()),'distinctParentSeats':int(g.pc_no.nunique()),'missingParentRows':int(g.pc_no.isna().sum()),'status':'reference-only; independently review by era before joining'})
 # The national CSV's constituency IDs are known to be truncated; compare by state/name only.
 shutil.copy2(cache/'lok-sabha-2024.csv',out/'lok-sabha-2024-source.csv')
 nr=list(csv.DictReader((cache/'lok-sabha-2024.csv').open(),delimiter=';'));ng=collections.defaultdict(list)
 for r in nr:ng[(statekey(r['State']),norm(r['Constituency']))].append(r)
 national={'2024':{'source':'fresh pinned upstream CSV','rows':len(nr),'seats':len(ng),'comparedSeats':0,'matchingWinnerVotes':0,'unmatchedSeats':[],'nonNumericVoteRows':[],'discrepancies':[]}}
 current={(statekey(s['region']),norm(s['name'])):s for s in atlas['national']['2024']['seats'].values()}
 for key,rows in ng.items():
  for r in rows:
   if not r['Votes'].replace(',','').isdigit():national['2024']['nonNumericVoteRows'].append({'constituency':r['Constituency'],'candidate':r['Candidate'],'value':r['Votes'],'note':'preserved; unopposed is not zero votes'})
  eligible=[r for r in rows if r['Votes'].replace(',','').isdigit() and not nota(r['Candidate'])]
  if key not in current:national['2024']['unmatchedSeats'].append({'state':rows[0]['State'],'constituency':rows[0]['Constituency']});continue
  if not eligible:continue
  winner=max(eligible,key=lambda r:int(r['Votes'].replace(',','')));old=next(c for c in current[key]['candidates'] if not nota(c['party']))
  national['2024']['comparedSeats']+=1
  if old['votes']==int(winner['Votes'].replace(',','')):national['2024']['matchingWinnerVotes']+=1
  else:national['2024']['discrepancies'].append({'state':rows[0]['State'],'constituency':rows[0]['Constituency'],'atlasVotes':old['votes'],'upstreamVotes':int(winner['Votes'].replace(',',''))})
 # 2019 is an export of the retained atlas, NOT a new independent download.
 rows=[]
 for seat in atlas['national']['2019']['seats'].values():
  for c in seat['candidates']:rows.append({'year':2019,'seat_id':seat['id'],'state':seat['region'],'constituency':seat['name'],'candidate':c['name'],'party':c['party'],'votes':c['votes'],'source':seat.get('source','')})
 writecsv(out/'lok-sabha-2019-atlas-export.csv',rows,['year','seat_id','state','constituency','candidate','party','votes','source'])
 national['2019']={'source':'derived export from existing atlas, not an independent import or validation','rows':len(rows),'seats':len(atlas['national']['2019']['seats']),'atlasSHA256':sha(ROOT/'data/atlas.json')}
 report={'date':'2026-11-10','applicationAtlasChanged':False,'historicalRows':len(frame),'historicalElectionIds':int(frame.election_id.nunique()),'historicalStateLabels':int(frame.state_name.nunique()),'recentFiles':len(list(recent.glob('*.csv'))),'recentRows':sum(r['rows'] for r in summary if r['source']=='recent-assembly'),'historicalQualityTotals':{k:sum(r['quality'][k] for r in summary if r['source']=='historical-assembly') for k in ['missingVoteRows','negativeVoteRows','fractionalVoteRows','missingMonthRows']},'national':national,'coverage':summary,'mappingCoverage':mappings,'limitations':['Raw election IDs are not a validated count of general elections; some source dates are ambiguous.','Recent files overlap the historical bundle: do not sum row counts as unique candidates.','Winner-vote comparisons do not verify identity, full candidate rosters, party or coalition labels.','All mappings are era-specific references; pre/post delimitation IDs must not be joined directly.','No pre-2009 state results, pre-2019 national results, legislative careers, new biographies or manifesto assessments are imported here.']}
 fields=['source','election','stateCode','year','rows','seats','comparedSeats','winnerVoteTotalsDiffering','reviewRequired']
 coverage=[{'source':r['source'],'election':r.get('electionId',r.get('file','')),'stateCode':r.get('stateCode',''),'year':r['sourceYear'],'rows':r['rows'],'seats':r['seats'],'comparedSeats':r.get('comparedSeats',0),'winnerVoteTotalsDiffering':r.get('winnerVoteTotalsDiffering',0),'reviewRequired':r.get('reviewRequired',False)} for r in summary]
 writecsv(out/'assembly-coverage.csv',coverage,fields)
 writejson(out/'validation.json',report);writejson(out/'assembly-winner-discrepancies.json',discrepancies);writejson(out/'historical-vote-issues.json',issues)
 manifest={'date':'2026-11-10','inputs':lock['sources'],'applicationAtlasSHA256':sha(ROOT/'data/atlas.json'),'outputs':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='manifest.json'}}
 writejson(out/'manifest.json',manifest)
 print(json.dumps({k:report[k] for k in ['historicalRows','historicalElectionIds','historicalStateLabels','recentFiles','recentRows','historicalQualityTotals','national']},indent=2))
 print('Assembly winner discrepancies:',len(discrepancies))
if __name__=='__main__':main()
