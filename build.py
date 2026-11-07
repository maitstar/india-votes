from pathlib import Path
import json,re,copy
root=Path(__file__).parent;out=root/'dist';out.mkdir(exist_ok=True);assets=out/'assets';assets.mkdir(exist_ok=True)
def write(name,data):
 p=assets/name;p.write_text(json.dumps(data,separators=(',',':')).replace('<','\\u003c'));return 'assets/'+name
x=json.loads((root/'data/atlas.json').read_text());boot=copy.deepcopy(x);rosters={}
def rdp(pts,epsilon=.01):
 if len(pts)<4:return pts
 a,b=pts[0],pts[-1];dx=b[0]-a[0];dy=b[1]-a[1];den=dx*dx+dy*dy
 def dist(p):
  t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
  return (p[0]-a[0]-t*dx)**2+(p[1]-a[1]-t*dy)**2
 i=max(range(1,len(pts)-1),key=lambda i:dist(pts[i]))
 if dist(pts[i])>epsilon**2:return rdp(pts[:i+1],epsilon)[:-1]+rdp(pts[i:],epsilon)
 return [a,b]
def simple(p):
 # Simplify country overview only (~1km tolerance). Constituency polygons remain untouched.
 parts=[]
 for seg in re.findall(r'M[^M]+',p):
  pts=[(float(a),float(b)) for a,b in re.findall(r'(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)',seg)]
  kept=rdp(pts) if len(pts)>3 else pts
  if len(kept)<3:kept=pts
  if kept:parts.append('M'+'L'.join(f'{a:.3f},{b:.3f}' for a,b in kept)+'Z')
 return ''.join(parts)
def stub(s,name):
 t={k:v for k,v in s.items() if k not in ['seats','previous','map','countryPath','turnout']};t.update(seats={},previous={},map={},_url=write(name,s))
 if s.get('mapRef'):t['_mapUrl']=write('geometry-'+s['mapRef']+'.json',next(a['map'] for a in x['states'] if a['code']==s['mapRef']))
 if s.get('mapReuseYear'):t['_mapReuseUrl']=write('geometry-LS-'+str(s['mapReuseYear'])+'.json',x['national'][str(s['mapReuseYear'])]['map'])
 t['_seatTallies']={'party':{},'alliance':{}}
 for seat in s['seats'].values():
  w=next(c for c in seat['candidates'] if c['party']!='NOTA')
  for mode,k in [('party',w['party']),('alliance',w.get('coalition',w.get('alliance',w['party'])))]:t['_seatTallies'][mode][k]=t['_seatTallies'][mode].get(k,0)+1
 return t
for i,s in enumerate(x['states']):
 t=stub(s,f'{s["code"]}-{s["year"]}.json');t['countryPath']=simple(s['countryPath']);t['candidateCount']=sum(len(a['candidates']) for a in s['seats'].values());boot['states'][i]=t
 rosters[s['code']]={'seats':s['seats'],'previous':{k:{'candidates':v['candidates'][:1]} for k,v in s['previous'].items()}}
boot['rosterUrl']=write('state-rosters.json',rosters)
for c,versions in x['elections'].items():
 for y,s in versions.items():
  if not s.get('latestRef'):boot['elections'][c][y]=stub(s,f'{c}-{y}.json')
for y,s in x['national'].items():boot['national'][y]=stub(s,f'LS-{y}.json')
boot['candidateReview']={'records':[],'bios':[],'coverage':{},'_url':write('kerala-candidate-review.json',x['candidateReview'])}
css=(root/'style.css').read_text()+'\n'+(root/'redesign.css').read_text()+'\n'+(root/'clarity.css').read_text();app=(root/'app.js').read_text();extra=(root/'redesign.js').read_text()+'\n'+(root/'clarity.js').read_text();app=app.replace('for(const s of latestStates)hydrate(s);',extra+'\nfor(const s of latestStates)hydrate(s);')
html=(root/'template.html').read_text().replace('/*STYLE*/',css).replace('/*DATA*/',json.dumps(boot,separators=(',',':')).replace('<','\\u003c')).replace('/*APP*/',app)
(out/'index.html').write_text(html);(out/'vercel.json').write_text(json.dumps({'framework':None,'cleanUrls':True,'headers':[{'source':'/assets/(.*)','headers':[{'key':'Cache-Control','value':'public, max-age=0, must-revalidate'}]}]},indent=2))
print('HTML',len(html.encode()),'bytes; data loaded by election;',len(list(assets.glob('*.json'))),'data files')
