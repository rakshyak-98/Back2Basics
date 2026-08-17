[[Streaming]] [[WebRTC]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]]

# ICE (Interactive Connectivity Establishment)

> ICE finds a working path between two peers behind NATs — try direct, then relay.





## Interview Relevance
Interviewers probe whether you can walk ICE end-to-end — not just name it. Signal fluency with **Candidate**, **host**, **srflx (server-reflexive)**, **relay** and when you would pick a different path.

## Sources
- [Wikipedia — ICE](https://en.wikipedia.org/wiki/ICE) — overview
- [RFC 8445 — ICE](https://datatracker.ietf.org/doc/html/rfc8445) — deep-dive

## Core Definition
STUN helps you **find** your public face. TURN **carries** the media when direct fails. ICE **chooses** which path to use.

## Key Concepts
- **Candidate:** One address:port you might use — “A candidate is a possible path to reach me.”
- **host:** LAN IP from the machine — “Same Wi‑Fi often works with host only.”
- **srflx (server-reflexive):** Public IP:port STUN saw — “STUN tells me how the internet sees me.”
- **relay:** Address on a TURN server — “If direct fails, media goes through TURN.”
- **Check:** Send a short probe on that pair — “ICE tests pairs until one answers.”
- **Nominated / selected:** The pair media will use — “One pair wins; that carries RTP.”

**Flow:**

1. **Gather** — each peer collects host, STUN (srflx), and optionally TURN (relay) candidates.
2. **Share** — send candidates (+ SDP) over [[WebRTC Signaling channels]] (HTTP/WebSocket — not the media UDP).
3. **Try** — both sides run connectivity checks on candidate pairs.
4. **Pick** — prefer host → srflx → relay (cheaper / lower latency first). Fall back to TURN when firewalls block UDP peer-to-peer.

### STUN vs TURN (keep them short)

| Tool | Job in one line |
|------|-----------------|
| **STUN** (Session Traversal Utilities for NAT) | Ask a public server: “What is my public IP:port?” |
| **TURN** (Traversal Using Relays around NAT) | If peers cannot punch through, send media through a relay. |

### Signaling (one sentence)

Signaling is how peers **swap** “here are my addresses” before media starts — usually your application’s Web API or WebSocket.

```js
// Signaling is your channel; ICE is the path finder
const signalingChannel = new SignalingChannel()
```

## Technical Details
```txt
Peer A                          Peer B
  │                               │
  ├─ gather candidates ───────────┤  (host / STUN public / TURN relay)
  │                               │
  ├──── share via signaling ──────┤  (not the media path)
  │                               │
  ├──── try pairs (checks) ───────┤
  │                               │
  └──── pick best working path ───┘  (prefer direct; else TURN)
```

```js
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    {
      urls: 'turn:turn.example.com:3478',
      username: 'u',
      credential: 'p', // prefer short-lived REST credentials
    },
  ],
  iceTransportPolicy: 'all', // 'relay' = force TURN (debug / policy)
})

pc.onicecandidate = (e) => {
  if (e.candidate) signaling.send({ type: 'candidate', candidate: e.candidate })
}
```

| Knob | Why it matters |
|------|----------------|
| `stun:` URL | Gives srflx candidates — needed across NATs |
| `turn:` + auth | Fallback when corporate / symmetric NAT blocks direct |
| `iceTransportPolicy: 'relay'` | Forces TURN — prove media works when ICE looks “stuck” |
| Trickle ICE | Send candidates as they appear — don’t wait for full gather |

Debug: `chrome://webrtc-internals` → ICE candidate pairs / selected candidate.

## Real-World Applications
STUN helps you **find** your public face. TURN **carries** the media when direct fails. ICE **chooses** which path to use.

Used wherever ICE sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **One-to-many OTT** — use [[HLS]] / [[DASH]] + CDN; ICE is for few peers, not millions of viewers.
- **Con / skip when:** **You only need server push** — WebSockets/SSE; no NAT punch required.
- **Con / skip when:** **Ingest from OBS to origin** — usually [[RTMP]] / SRT, not ICE between browsers.

## Comparison
- vs [[HLS]]: **One-to-many OTT** — use [[HLS]] / [[DASH]] + CDN; ICE is for few peers, not millions of viewers.
- vs [[RTMP]]: **Ingest from OBS to origin** — usually [[RTMP]] / SRT, not ICE between browsers.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck “connecting” | No srflx / no relay in internals | Add STUN; deploy TURN; UDP may be blocked |
| Works on same Wi‑Fi only | Only host candidates | STUN for public path; TURN for hard NATs |
| High connect delay | Waiting for full gather | Enable trickle ICE |
| One-way media after “connected” | Wrong pair / firewall mid-call | ICE restart; check `iceConnectionState` |
| All traffic on TURN | Policy or checks failing | Cost/latency spike — fix firewall or return to `all` |
| ICE failed after Wi‑Fi→LTE | Network change | Call `restartIce()` / renegotiate |

- **STUN ≠ TURN** — STUN only discovers addresses; it never relays media. No TURN ⇒ ~5–15% of users never connect.
- **Signaling is not ICE** — your WebSocket carries SDP/candidates; STUN/TURN URLs go in `RTCPeerConnection` config.
- **Symmetric NATs** — STUN srflx often fails pairwise checks; you need TURN.
- **Long-lived TURN passwords in the client** — prefer short-lived credentials from your API.
