export default {
  "title": "Anycast Compass",
  "intro": "Which root-server instances do Canadian probes reach? Follow returned instance names and changes in a dated volunteer-probe sample.",
  "eyebrow": "DNS ROOTS / CANADIAN MEASUREMENT PROBES",
  "accent": "#316a73",
  "tint": "#e0eff0",
  "method": [
    "This tool retrieves existing RIPE Atlas built-in IPv4 hostname.bind DNS measurements for all 13 root letters. It creates no new measurements and does not require credits or a private API key.",
    "Up to 50 public connected Canadian probes are selected reproducibly: first geographical coverage by estimated province, then ASN diversity. One completed UTC hour is captured per daily run. Missing TXT answers stay explicit.",
    "The instance is the returned hostname.bind TXT string. It can identify a serving node but does not necessarily identify a city or physical facility. Changes are measured only within the same probe/root/address-family series.",
    "Province is estimated from RIPE’s obfuscated coordinates and Natural Earth boundaries. Volunteer probes, ASN diversity sampling and one-hour windows are not a representative sample of Canadian users or all traffic."
  ],
  "id": "anycastcompass",
  "explorer-title": "Follow the record.",
  "cadence": "Daily automated collection. Source dates and capture dates are shown separately.",
  "facets": [
    {
      "key": "root",
      "label": "Root server"
    },
    {
      "key": "asn",
      "label": "Probe ASN"
    },
    {
      "key": "province",
      "label": "Estimated province"
    }
  ],
  "columns": [
    {
      "key": "instance",
      "label": "Returned instance name"
    },
    {
      "key": "root",
      "label": "Root"
    },
    {
      "key": "probe",
      "label": "Probe ID"
    },
    {
      "key": "asn",
      "label": "ASN"
    },
    {
      "key": "province",
      "label": "Estimated province"
    },
    {
      "key": "timestamp",
      "label": "Observation (UTC)"
    },
    {
      "key": "rtt_ms",
      "label": "RTT (ms)"
    }
  ],
  "related": [
    {
      "label": "Packet Detour",
      "url": "https://coolcode.ca/packet-detour/"
    },
    {
      "label": "Boomerang Meter",
      "url": "https://coolcode.ca/boomerang-meter/"
    }
  ]
};
