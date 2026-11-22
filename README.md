# Anycast Compass

Which root-server instances do Canadian probes reach? Follow returned instance names and changes in a dated volunteer-probe sample.

Open https://coolcode.ca/anycastcompass/

<!-- coolcode:guide -->
Filter a root server and probe ASN. Instance names are returned TXT answers, not destinations inferred from IP geography. Province is estimated from obfuscated probe coordinates; volunteer probes are not representative of all ISP customers.
<!-- /coolcode:guide -->

## Sources and interpretation

This tool retrieves existing RIPE Atlas built-in IPv4 hostname.bind DNS measurements for all 13 root letters. It creates no new measurements and does not require credits or a private API key.

Up to 50 public connected Canadian probes are selected reproducibly: first geographical coverage by estimated province, then ASN diversity. One completed UTC hour is captured per daily run. Missing TXT answers stay explicit.

The instance is the returned hostname.bind TXT string. It can identify a serving node but does not necessarily identify a city or physical facility. Changes are measured only within the same probe/root/address-family series.

Province is estimated from RIPE’s obfuscated coordinates and Natural Earth boundaries. Volunteer probes, ASN diversity sampling and one-hour windows are not a representative sample of Canadian users or all traffic.

## Collection and archive

Schedule: **Daily** (`47 12 * * *`, UTC). GitHub schedules are best effort. Scheduled and manual runs collect, validate, commit dated snapshots and deploy. A first code push also collects if no saved dataset exists. Other code pushes rebuild the saved dataset offline.

`data/current.json` contains the latest normalized source records and metadata. `archive/YYYY-MM/*.json.gz` retains distinct captured versions; `data/history.json` lists them. Identical data checks update the check time without manufacturing a change. An initial capture is labelled baseline. Archive data is tracked in Git and does not expire with Actions artifacts. The site has snapshot selection, filtering, source detail, CSV export and an RSS change feed.

The default build needs no network. Failed source validation does not replace the published dataset. Optional `HEALTHCHECKS_PING_URL` sends start/success/failure pings for collection runs; no accuracy email is implied.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/collect.py
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

## Privacy

Search and filters are local to the browser; no upstream request is made by filtering. Public data collection runs in GitHub Actions. The shared CoolCode counter records aggregate page opens, without searches or filter values. The explorer and collector run without Cloudflare changes. To enable shared visit counts and private issue reports, add `anycastcompass` to the existing `coolcode-visitor-api` Worker’s `toolList` and deploy it, if not already registered. See the [batch setup notes](https://github.com/jsdyer/jsdyer.github.io/blob/main/docs/tier1-tools.md).

## Software and attribution

Application code is MIT licensed; upstream data retains its original licence and attribution. Follow the source links for original records and terms.
