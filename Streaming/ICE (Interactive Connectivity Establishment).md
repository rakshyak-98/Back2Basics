[[Streaming]] [[WebRTC]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]]

# ICE (Interactive Connectivity Establishment)

> ICE finds a working path between two peers behind NATs — try direct, then relay.

---

## Mental model

**Say it in one breath:** ICE asks each peer for address options (candidates), both sides share them, then they test pairs until one path works.

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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Candidate** | One address:port you might use | “A candidate is a possible path to reach me.” |
| **host** | LAN IP from the machine | “Same Wi‑Fi often works with host only.” |
| **srflx** (server-reflexive) | Public IP:port STUN saw | “STUN tells me how the internet sees me.” |
| **relay** | Address on a TURN server | “If direct fails, media goes through TURN.” |
| **Check** | Send a short probe on that pair | “ICE tests pairs until one answers.” |
| **Nominated / selected** | The pair media will use | “One pair wins; that carries RTP.” |

### STUN vs TURN (keep them short)

| Tool | Job in one line |
|------|-----------------|
| **STUN** (Session Traversal Utilities for NAT) | Ask a public server: “What is my public IP:port?” |
| **TURN** (Traversal Using Relays around NAT) | If peers cannot punch through, send media through a relay. |

> [!INFO]
> STUN helps you **find** your public face. TURN **carries** the media when direct fails. ICE **chooses** which path to use.

### How the story goes (4 steps)

1. **Gather** — each peer collects host, STUN (srflx), and optionally TURN (relay) candidates.
2. **Share** — send candidates (+ SDP) over [[WebRTC Signaling channels]] (HTTP/WebSocket — not the media UDP).
3. **Try** — both sides run connectivity checks on candidate pairs.
4. **Pick** — prefer host → srflx → relay (cheaper / lower latency first). Fall back to TURN when firewalls block UDP peer-to-peer.

### Signaling (one sentence)

Signaling is how peers **swap** “here are my addresses” before media starts — usually your app’s Web API or WebSocket.

```js
// Signaling is your channel; ICE is the path finder
const signalingChannel = new SignalingChannel()
```

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck “connecting” | No srflx / no relay in internals | Add STUN; deploy TURN; UDP may be blocked |
| Works on same Wi‑Fi only | Only host candidates | STUN for public path; TURN for hard NATs |
| High connect delay | Waiting for full gather | Enable trickle ICE |
| One-way media after “connected” | Wrong pair / firewall mid-call | ICE restart; check `iceConnectionState` |
| All traffic on TURN | Policy or checks failing | Cost/latency spike — fix firewall or return to `all` |
| ICE failed after Wi‑Fi→LTE | Network change | Call `restartIce()` / renegotiate |

---

## Gotchas

> [!WARNING]
> **STUN ≠ TURN** — STUN only discovers addresses; it never relays media. No TURN ⇒ ~5–15% of users never connect.

> [!WARNING]
> **Signaling is not ICE** — your WebSocket carries SDP/candidates; STUN/TURN URLs go in `RTCPeerConnection` config.

> [!WARNING]
> **Symmetric NATs** — STUN srflx often fails pairwise checks; you need TURN.

> [!WARNING]
> **Long-lived TURN passwords in the client** — prefer short-lived credentials from your API.

---

## When NOT to use

- **One-to-many OTT** — use [[HLS]] / [[DASH]] + CDN; ICE is for few peers, not millions of viewers.
- **You only need server push** — WebSockets/SSE; no NAT punch required.
- **Ingest from OBS to origin** — usually [[RTMP]] / SRT, not ICE between browsers.

---

## Related

[[WebRTC]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]] [[WebRTC Get Started Guide]] [[NAT (Network Address Translation)]] [[SCTP (Stream Control Transmission Protocol)]]
