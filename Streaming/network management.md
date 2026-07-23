[[ss]] [[ip]] [[Networking]] [[UDP]] [[TCP]] [[Streaming]] [[ingestion]]

# Network management (streaming)

> Diagnose bitrate paths, packet loss, and connection health on live pipelines — **ss/tcpdump/iperf**, not generic IT network admin.

---

## Mental model

Streaming **breaks at the network layer** before the player shows a useful error: **RTMP stall**, **UDP TS gaps**, **CDN 502**, **TLS reset**. Operators correlate **publisher uplink**, **origin ingest**, and **viewer last-mile** — each hop has different tools and SLOs.

```txt
Publisher ──► Ingest (RTMP/SRT) ──► Origin ──► CDN ──► Player
     │              │                  │         │
  iperf/upstream   ss :1935         egress $   tcpdump 443
  OBS stats        packet loss      cache hit   CDN logs
```

| Symptom layer | First tool | Typical culprit |
|---------------|------------|-----------------|
| **Publish fail** | `nc`, RTMP connect | Firewall 1935, bad DNS |
| **Ingest jitter** | `ss -ti`, encoder logs | Wi-Fi, no CBR cap |
| **Segment gap** | Origin m3u8 sequence | Packager crash |
| **Viewer rebuffer** | CDN cache miss, MTR | Origin overload, bad ABR |

This note is **streaming-focused triage** — see [[Networking]] for routing/BGP.

---

## Standard config / commands

### Socket & connection inventory

```bash
# What's listening / connected on ingest ports
ss -tulnp | grep -E '1935|443|9000'
ss -tn state established '( dport = :1935 or sport = :1935 )'

# RTMP/long-lived TCP detail (retransmits hint)
ss -ti | grep -A1 ':1935'
```

### Capture streaming traffic (careful in prod — volume)

```bash
# RTMP handshake + chunk stream (short capture)
sudo tcpdump -i any -nn port 1935 -c 200 -w rtmp_debug.pcap

# HTTPS segment fetch pattern from one client IP
sudo tcpdump -i any -nn host CLIENT_IP and port 443 -c 500

# UDP MPEG-TS multicast
sudo tcpdump -i eth0 -nn 'udp port 1234' -c 100
```

### Bandwidth & loss (publisher site)

```bash
# Need server: iperf3 -s on ingest side
iperf3 -c ingest.example.com -t 30 -R    # downlink from ingest POV
iperf3 -c ingest.example.com -t 30 -u -b 8M  # UDP loss test
mtr -rwzbc100 ingest.example.com           # path stability
```

### Interface & queue

```bash
ip -s link show eth0
ethtool -S eth0 | grep -i drop
nload eth0   # live throughput TUI
```

### CDN / HTTP segment check

```bash
curl -w 'dns:%{time_namelookup} connect:%{time_connect} tls:%{time_appconnect} ttfb:%{time_starttransfer} total:%{time_total}\n' \
  -o /dev/null -s "https://cdn.example.com/live/720p.m3u8"
```

### Firewall quick verify

```bash
sudo nft list ruleset | grep -E '1935|443'
# AWS: security group + NACL both directions
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| OBS disconnect loop | `ss -ti` retransmits; Wi-Fi | Wired uplink; lower bitrate; RTMPS if middlebox |
| Macroblocking but no drop | Uplink not saturated — encode issue | See [[Encoding]] CBR cap |
| TS continuity errors | `tcpdump` UDP gaps | FEC/SRT instead of raw UDP; switch IGMP querier |
| CDN 502 on segments | Origin reachability from CDN POP | Origin health; connection limit ([[half-open connections]]) |
| Regional viewers only fail | Geo DNS / POP routing | CDN failover; check one POP with curl `--resolve` |
| TLS errors on license | Certificate chain | Full chain on 443; see [[TLS (Transport Layer Security)]] |
| High latency live | Segment duration + CDN + playlist | [[HLS]] LL-HLS tuning; not a "network mgmt" knob alone |

---

## Gotchas

> [!WARNING]
> **tcpdump on 10 Gbps ingest** — can drop packets itself; use sampled capture or mirror port.

> [!WARNING]
> **Wi-Fi publisher for broadcast** — jitter buffers hide until catastrophic disconnect; require wired for SLA events.

> [!WARNING]
> **Symmetric NAT + RTMP** — publish outbound OK; don't confuse with viewer UDP/WebRTC paths.

> [!WARNING]
> **CDN cache mistaken for network fix** — stale manifest looks like "network lag"; check `Age` header.

> [!WARNING]
> **Rate-limit on auth webhook** — ingest drops when auth service slow, looks like network failure.

---

## When NOT to use

- **Application codec debug** — use `ffprobe`, not packet capture first.
- **DRM license logic** — network shows 403; root cause is [[EME]]/auth.
- **Full corporate LAN redesign** — escalate to netops; streaming ops prove hop + metric.

---

## Related

[[ss]] [[ip]] [[Networking]] [[RTMP]] [[ingestion]] [[UDP]] [[half-open connections]] [[Egress traffic]]
