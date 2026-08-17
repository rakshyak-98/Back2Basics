[[WebRTC]] [[UDP]] [[TCP]] [[DTLS]] [[ICE (Interactive Connectivity Establishment)]] [[WebRTC Signaling channels]] [[webSocket]]

# SCTP (Stream Control Transmission Protocol)

> SCTP (Stream Control Transmission Protocol) — SCTP sits above IP, offering multiple streams with optional reliable ordered delivery — unlike TCP's single byte stream. In WebRTC, SCTP runs

```txt
        SCTP (Stream Contr ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about SCTP to see if you understand the pipeline role, failu…

## Sources
- [Wikipedia — SCTP](https://en.wikipedia.org/wiki/SCTP) — overview
- [RFC 9260 — SCTP](https://datatracker.ietf.org/doc/html/rfc9260) — deep-dive

## Key Concepts
- **Note:** **SCTP** sits **above IP**, offering **multiple streams** with optional **rel…

| Feature | SCTP | TCP | UDP |
|---------|------|-----|-----|
| **Delivery** | Reliable or partial | Reliable | Best-effort |
| **Ordering** | Per-stream | Global | None |
| **Head-of-line blocking** | Avoidable (multi-stream) | Yes | N/A |
| **WebRTC DataChannel** | Native | No | Raw only |

- **Note:** Telecom origin (SS7 transport)

## Technical Details
```txt
WebRTC stack (simplified)
  Media: SRTP (UDP) — A/V
  Data:  SCTP ─ inside ─ DTLS ─ UDP — DataChannel

NOT used for: [[HLS]] segments, [[RTMP]], [[MPEG-TS]] broadcast
```

### Browser DataChannel (application code)

```javascript
const pc = new RTCPeerConnection();
const dc = pc.createDataChannel('control', {
  ordered: true,           // false for low-latency loss-tolerant
  maxRetransmits: 0,       // unreliable mode when ordered:false
});

dc.onopen = () => dc.send(JSON.stringify({ type: 'hello' }));
dc.onmessage = (e) => console.log('recv', e.data);
```

- Signaling uses separate channel — see [[WebRTC Signaling channels]].

### SCTP vs media path (architecture)

```txt
Low-latency A/V        → SRTP (not SCTP)
Metadata / chat / ctrl → SCTP DataChannel
Fallback file sync     → HTTPS, not SCTP
```

### Debug WebRTC (Chrome)

```txt
chrome://webrtc-internals
  → SCTP transport section: messages sent/recv, congestion
  → Compare with candidate pair (ICE) state
```

### Server-side WebRTC (Pion / mediasoup pattern)

```txt
Signaling: WebSocket ([[WebRTC Signaling channels]])
ICE: STUN/TURN ([[ICE (Interactive Connectivity Establishment)]])
Media: UDP SRTP
Data: SCTP association per PeerConnection
```

- No ffmpeg flag for SCTP — it's browser/stack internal.

### When SCTP association fails

```bash
# Network: UDP must flow (SCTP over DTLS uses UDP port from ICE)
# Corporate firewall often blocks UDP — need TURN relay
mtr -u turn.example.com
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| DataChannel never opens | `pc.connectionState` | ICE failure; add TURN |
| Messages stall, video OK | SCTP congestion | Reduce message rate; binary vs JSON size |
| Ordered lag | `ordered: true` + loss | `ordered: false` for time-sensitive |
| Works LAN, fails remote | UDP blocked | TURN over TLS 443 |
| Duplicate messages | App layer no dedupe | Idempotent handlers |
| SCTP abort on reconnect | New PeerConnection | Re-establish DataChannel on ICE restart |

- **Mistake:** **Confusing SCTP with [[RTMP]]/[[SRT]]**
- **Mistake:** **Large messages**
- **Mistake:** **Reliable ordered on lossy Wi-Fi**
- **Mistake:** **No SCTP to CDN**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **VoD / live OTT at scale**
- **Con / skip when:** **Replacing TCP API**
- **Con / skip when:** **Broadcast MPEG-TS**

## Comparison
- vs [[HLS]]: **VoD / live OTT at scale** — [[HLS]]/[[DASH]] + CDN, not peer SCTP.


### Use cases
- Used wherever SCTP sits in an ingest → package → CDN → player path
