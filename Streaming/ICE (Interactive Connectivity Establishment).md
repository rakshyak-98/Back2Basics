[[Streaming]] [[WebRTC]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]]

# ICE (Interactive Connectivity Establishment)

> ICE finds a working path between two peers behind NATs — try direct, then relay.

```txt
        ICE (Interactive C ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you can walk ICE end-to-end

## Sources
- [Wikipedia — ICE](https://en.wikipedia.org/wiki/ICE) — overview
- [RFC 8445 — ICE](https://datatracker.ietf.org/doc/html/rfc8445) — deep-dive

## Key Concepts
- **Candidate:** One address:port you might use — “A candidate is a possible path to reach me.”
- **host:** LAN IP from the machine — “Same Wi‑Fi often works with host only.”
- **srflx (server-reflexive):** Public IP:port STUN saw — “STUN tells me how the internet sees me.”
- **relay:** Address on a TURN server — “If direct fails, media goes through TURN.”
- **Check:** Send a short probe on that pair — “ICE tests pairs until one answers.”
- **Nominated / selected:** The pair media will use — “One pair wins; that carries RTP.”

**Flow:**

- **Note:** 1. **Gather**
- **Note:** 2. **Share**
- **Note:** 3. **Try** — both sides run connectivity checks on candidate pairs.
- **Note:** 4. **Pick** — prefer host → srflx → relay (cheaper / lower latency first). Fa…

### STUN vs TURN (keep them short)

| Tool | Job in one line |
|------|-----------------|
| **STUN** (Session Traversal Utilities for NAT) | Ask a public server: “What is my public IP:port?” |
| **TURN** (Traversal Using Relays around NAT) | If peers cannot punch through, send media through a relay. |

### Signaling (one sentence)

- **Note:** Signaling is how peers **swap** “here are my addresses” before media starts

```js
// Signaling is your channel; ICE is the path finder
const signalingChannel = new SignalingChannel()
```


- **Core:** STUN helps you **find** your public face

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

- Debug: `chrome://webrtc-internals` → ICE candidate pairs / selected candidate.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck “connecting” | No srflx / no relay in internals | Add STUN; deploy TURN; UDP may be blocked |
| Works on same Wi‑Fi only | Only host candidates | STUN for public path; TURN for hard NATs |
| High connect delay | Waiting for full gather | Enable trickle ICE |
| One-way media after “connected” | Wrong pair / firewall mid-call | ICE restart; check `iceConnectionState` |
| All traffic on TURN | Policy or checks failing | Cost/latency spike — fix firewall or return to `all` |
| ICE failed after Wi‑Fi→LTE | Network change | Call `restartIce()` / renegotiate |

- **Mistake:** **STUN ≠ TURN**
- **Mistake:** **Signaling is not ICE**
- **Mistake:** **Symmetric NATs**
- **Mistake:** **Long-lived TURN passwords in the client**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **One-to-many OTT**
- **Con / skip when:** **You only need server push**
- **Con / skip when:** **Ingest from OBS to origin**

## Comparison
- vs [[HLS]]: **One-to-many OTT**
- vs [[RTMP]]: **Ingest from OBS to origin** — usually [[RTMP]] / SRT, not ICE between browsers.


### Use cases
- STUN helps you **find** your public face

- Used wherever ICE sits in an ingest → package → CDN → player path
