[[Multi Stream]] [[ingestion]] [[RTMP]] [[OBS]] [[Encoding]]

# Single Stream

> One publisher → one ingest destination → one encoded bitrate path — **simplest live topology** before ABR and multi-CDN.

---

## Mental model

**Single stream** means **one active encode pipeline** from source to **one ingest endpoint** — not multiple ladder rungs ([[Multi Stream]] ABR) and not fan-out to YouTube + origin simultaneously. OBS defaults here: **one RTMP push** at **one resolution/bitrate**. Origin may still **transcode to ABR** downstream — that's server-side, not publisher multi-stream.

```txt
Single-stream publish path
  Camera ──► OBS ──► one RTMP ──► ingest ──► (optional) ladder ──► [[HLS]]

Contrast [[Multi Stream]]:
  Multi-push: same encode → many RTMP URLs
  ABR: many encodes → one manifest
```

| Aspect | Single stream | When to expand |
|--------|---------------|----------------|
| **Uplink** | One bitrate budget | Need >1 destination without origin |
| **Ops** | Minimal | SLA events → redundant push |
| **Quality** | One rung to ingest | Players need ABR → server ladder |
| **Failure** | Single point | Backup ingest URL (failover encoder config) |

---

## Standard config / commands

### OBS single publish (canonical)

```txt
Settings → Stream → one Custom RTMP URL + Stream Key
Settings → Output → one streaming encoder profile
No secondary URL unless deliberate [[Multi Stream]]
```

See [[OBS]] for bitrate/GOP defaults.

### ffmpeg single publish

```bash
ffmpeg -re -i input.mp4 \
  -c:v libx264 -b:v 3500k -minrate 3500k -maxrate 3500k -bufsize 7000k \
  -g 60 -sc_threshold 0 -c:a aac -b:a 128k \
  -f flv rtmp://ingest.example.com/live/key
```

### Ingest accepts one publisher per key

```nginx
# nginx-rtmp: second publisher with same key kicks first
live on;
drop_idle_publisher 10s;
```

Document behavior for ops — "single stream per key" policy.

### Downstream ABR from single ingest (server-side)

```txt
Publisher: single 1080p30 @ 5 Mbps RTMP
Origin: transcode → 1080/720/480 ladder → [[Manifest (streaming)]]
Publisher unchanged — ABR is not publisher [[Multi Stream]]
```

### Failover without multi-stream (cold standby)

```txt
Primary encoder active; secondary encoder configured but offline
Manual switch on primary failure — not simultaneous push
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| New publish kicks old | Same stream key | Unique keys per event; or intentional takeover |
| Quality OK ingest, bad playback | No server ladder | Enable transcode packager |
| Single viewer OK, scale fails | RTMP to players | Must use [[HLS]]/[[DASH]] for viewers |
| Bitrate wrong for network | Single rung too high | Lower OBS bitrate or 720p output |
| Duplicate events on key reuse | Stale CDN cache | New key per event; purge manifest |

---

## Gotchas

> [!WARNING]
> **Single stream ≠ single bitrate to viewers** — origin may still produce ABR; clarify in runbooks.

> [!WARNING]
> **One RTMP to CDN "live" product** — some CDNs accept RTMP publish then package; still one publisher path.

> [!WARNING]
> **No redundancy** — single laptop OBS is SPOF; plan backup encoder for tier-1 events.

---

## When NOT to use

- **Need simultaneous YouTube + private origin** — [[Multi Stream]] multi-push.
- **Direct ABR from publisher** — multiple encodes or hardware ladder (rare); usually server-side.
- **WebRTC fanout** — SFU architecture, not single RTMP ([[WebRTC]]).

---

## Related

[[Multi Stream]] [[ingestion]] [[RTMP]] [[OBS]] [[Encoding]] [[bitrate streaming]] [[HLS]]
