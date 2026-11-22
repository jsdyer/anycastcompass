from common import ROOT,save
import source,json,argparse

def main():
 p=argparse.ArgumentParser();p.add_argument('--seed',action='store_true');a=p.parse_args()
 if not a.seed:source.main()
 d=json.loads((source.ROOT/'anycast-real.json').read_text());rows=d['records']
 if not rows or len({r['root'] for r in rows})!=13:raise ValueError('Incomplete root measurement response')
 previous=json.loads((ROOT/'data/current.json').read_text())['records'] if (ROOT/'data/current.json').exists() else []
 last={}
 for r in sorted(previous,key=lambda r:r['timestamp']):
  if r['instance']:last[(r['probe'],r['root'])]=r
 transitions=[]
 for r in sorted(rows,key=lambda r:r['timestamp']):
  if not r['instance']:continue
  key=(r['probe'],r['root']);before=last.get(key)
  if before and before['timestamp']<r['timestamp'] and before['instance']!=r['instance']:transitions.append({'probe':r['probe'],'asn':r['asn'],'root':r['root'],'before':before['instance'],'after':r['instance'],'previous_time':before['timestamp'],'time':r['timestamp']})
  last[key]=r
 save(rows,sources=[{'label':'RIPE Atlas built-in DNS measurements','url':d['source']},{'label':'RIPE Atlas public probe API','url':'https://atlas.ripe.net/api/v2/probes/?country_code=CA&status=1&page_size=500'},{'label':'Natural Earth province boundaries','url':'https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-1-states-provinces/'}],coverage=f"{len(d['selected_probes'])} selected Canadian probes · all 13 IPv4 roots · {d['start']} to {d['stop']}",warnings=[d['sample_method'],'Province is estimated from obfuscated coordinates. Probe coverage is not representative of all subscribers.'],extra={'eligible_probes':d['eligible_probes'],'selected_probes':d['selected_probes'],'window_start':d['start'],'window_end':d['stop'],'transitions':transitions})
if __name__=='__main__':main()
