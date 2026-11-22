#!/usr/bin/env python3
"""Read-only proof: sample existing RIPE Atlas DNS measurements. No new measurements."""
import base64,collections,concurrent.futures,datetime,json,statistics,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'.cache'
ROOT.mkdir(exist_ok=True)
BASE='https://atlas.ripe.net/api/v2/'
ROOTS={'a':10309,'b':10310,'c':10311,'d':10312,'e':10313,'f':10304,'g':10314,'h':10315,'i':10305,'j':10316,'k':10301,'l':10308,'m':10306}
def fetch(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'CoolCode AnycastCompass public measurement research'}),timeout=70) as r:return json.load(r)
  except Exception:
   if attempt==2:raise
   time.sleep(2*(attempt+1))
def inside_ring(x,y,ring):
 inside=False
 for a,b in zip(ring,ring[1:]+ring[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
def province(point,boundaries):
 if not point:return 'Unknown'
 for f in boundaries:
  g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  if any(inside_ring(*point,rings[0]) and not any(inside_ring(*point,r) for r in rings[1:]) for rings in polys):return f['properties']['name']
 return 'Unknown'
def instance(result):
 # API ordinarily expands DNS TXT answers. Validate the owner/type; don't infer from destinations.
 values=[]
 for answer in result.get('answers',[]):
  if answer.get('TYPE')=='TXT' and str(answer.get('NAME','')).lower().rstrip('.')=='hostname.bind':
   value=answer.get('RDATA',[])
   if isinstance(value,str):value=[value]
   if isinstance(value,list) and all(isinstance(v,str) for v in value):values.append(''.join(value)[:250])
 return '|'.join(sorted(set(values))) or None

def main():
 data=fetch(BASE+'probes/?country_code=CA&status=1&page_size=500');allprobes=data['results']
 while data.get('next'):data=fetch(data['next']);allprobes+=data['results']
 eligible=sorted([p for p in allprobes if p.get('is_public') and p.get('asn_v4')],key=lambda p:p['id'])
 groups=collections.defaultdict(list)
 for p in eligible:groups[p['asn_v4']].append(p)
 boundaries=json.loads((ROOT.parent/'config/canada-provinces.geojson').read_text())['features']
 province_of={p['id']:province((p.get('geometry') or {}).get('coordinates'),boundaries) for p in eligible}
 selected=[];seen=set()
 # Cover available estimated provinces first, then diversify ASNs deterministically.
 for name in sorted(set(province_of.values())):
  if name=='Unknown':continue
  p=next(p for p in eligible if province_of[p['id']]==name);selected.append(p);seen.add(p['id'])
 for round_index in range(50):
  for asn in sorted(groups):
   if round_index<len(groups[asn]):
    p=groups[asn][round_index]
    if p['id'] not in seen:selected.append(p);seen.add(p['id'])
   if len(selected)>=50:break
  if len(selected)>=50:break
 selected=selected[:50]
 metadata={p['id']:{'probe':p['id'],'asn':p['asn_v4'],'province':province((p.get('geometry') or {}).get('coordinates'),boundaries),'province_method':'Estimated from obfuscated RIPE coordinates and Natural Earth 1:50m boundaries'} for p in selected}
 stop=int(time.time())//3600*3600;start=stop-3600;ids=','.join(str(p['id']) for p in selected)
 def query(item):
  letter,msm=item;url=BASE+f'measurements/{msm}/results/?probe_ids={ids}&start={start}&stop={stop}'
  data=fetch(url);records=[]
  if not isinstance(data,list):raise ValueError('Expected results array')
  for r in data:
   if r.get('prb_id') not in metadata or not start<=r.get('timestamp',0)<stop or r.get('msm_id')!=msm or r.get('af')!=4:continue
   result=r.get('result',{});identifier=instance(result);rt=result.get('rt')
   records.append({**metadata[r['prb_id']],'id':f'{msm}:{r["prb_id"]}:{r["timestamp"]}','root':letter.upper(),'measurement':msm,'timestamp':datetime.datetime.fromtimestamp(r['timestamp'],datetime.timezone.utc).isoformat().replace('+00:00','Z'),'date':datetime.datetime.fromtimestamp(r['timestamp'],datetime.timezone.utc).date().isoformat(),'instance':identifier,'rtt_ms':rt if isinstance(rt,(float,int)) and rt>=0 else None,'status':'answered' if identifier else 'no TXT answer','source':f'https://atlas.ripe.net/measurements/{msm}/'} )
  print(letter,len(records),'answered',sum(r['instance'] is not None for r in records),flush=True)
  return records
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for chunk in pool.map(query,ROOTS.items()):rows+=chunk
 rows=sorted({r['id']:r for r in rows}.values(),key=lambda r:(r['timestamp'],r['probe'],r['root']))
 output={'schema':1,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'source':'https://atlas.ripe.net/docs/getting-started/built-in-measurements/','sample_method':'Public connected Canadian probes with IPv4 ASN: lowest probe ID per available estimated province, then round-robin by ascending ASN and probe ID; maximum 50. Volunteer probes, not representative of Canadian internet users.','eligible_probes':len(eligible),'eligible_asns':len(groups),'selected_probes':list(metadata.values()),'start':datetime.datetime.fromtimestamp(start,datetime.timezone.utc).isoformat(),'stop':datetime.datetime.fromtimestamp(stop,datetime.timezone.utc).isoformat(),'records':rows}
 (ROOT/'anycast-real.json').write_text(json.dumps(output,ensure_ascii=False,separators=(',',':'))+'\n')
 print('DONE',len(rows),'records',len(metadata),'probes',len({r['asn'] for r in rows}),'ASNs',flush=True)
if __name__=='__main__':main()
