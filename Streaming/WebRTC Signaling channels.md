[[WebRTC]] [[ICE (Interactive Connectivity Establishment)]] [[SCTP (Stream Control Transmission Protocol)]] [[webSocket]] [[ingestion]] [[WebRTC Get Started Guide]]

# WebRTC Signaling channels

> Out-of-band exchange of SDP + ICE candidates — no media on signaling; required before the peer connection.

```txt
        WebRTC Signaling c ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about WebRTC Signaling channels to see if you understand the…

## Sources
- [Wikipedia — WebRTC Signaling channels](https://en.wikipedia.org/wiki/WebRTC_Signaling_channels) — overview

## Technical Details
```txt
Browser A                    Signaling server                 Browser B
    │── offer (SDP) ─────────────►│◄── join room ────────────────│
    │◄── answer (SDP) ────────────│──────── offer/answer ───────►│
    │── ICE candidate ───────────►│◄── ICE candidate ────────────│
    │                                                             │
    └────────────── SRTP media (direct or via TURN) ──────────────┘
```

### Minimal WebSocket signaling (Node pattern)

```javascript
// Server relays JSON to room peers — auth omitted for brevity
wss.on('connection', (ws) => {
  ws.on('message', (raw) => {
    const msg = JSON.parse(raw);
    if (msg.type === 'join') ws.room = msg.room;
    wss.clients.forEach((c) => {
      if (c !== ws && c.room === ws.room) c.send(raw);
    });
  });
});
```

```javascript
// Client: create offer after join
const pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
pc.onicecandidate = (e) => e.candidate && ws.send(JSON.stringify({ type: 'candidate', candidate: e.candidate }));
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);
ws.send(JSON.stringify({ type: 'offer', sdp: pc.localDescription }));
```

### Production signaling checklist

```txt
1. TLS on WebSocket (wss://)
2. Auth (JWT) before join room
3. Room ID unguessable (UUID)
4. Rate-limit offer/answer floods
5. TURN credentials short-lived (REST API)
6. Log signaling errors — not SDP bodies (PII)
```

### WHIP/WHEP (HTTP signaling — emerging)

```txt
WHIP: POST SDP offer to https://origin/whip/session → answer SDP
Reduces custom WebSocket for ** ingest to SFU ** (broadcast use case)
```

- Pair with [[ingestion]] for live; classic P2P still uses WebSocket/XMPP.

### ICE + STUN/TURN config

```javascript
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'turn:turn.example.com:3478', username: 'u', credential: 'p' },
  ],
  iceTransportPolicy: 'all', // 'relay' forces TURN debug
});
```

- See [[ICE (Interactive Connectivity Establishment)]].

### Debug

```txt
chrome://webrtc-internals — signaling state machine timeline
Server logs: join/leave, failed JSON parse, unauthorized room
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Stuck "connecting" | ICE failed in internals | Add TURN; corporate UDP block |
| One-way audio/video | SDP direction / addTrack order | Renegotiate; verify sendrecv |
| Works same network only | Host candidates only | STUN srflx; deploy TURN |
| Signaling 401 | JWT expired | Refresh token before offer |
| Duplicate answers | Glare (both offer) | Polite/impolite peer pattern |
| DataChannel dead, media OK | Separate negotiation | CreateDataChannel before offer or renegotiate |
| High connect latency | Trickle ICE disabled | Enable trickle; don't wait full gather |

- **Mistake:** **Signaling != TURN**
- **Mistake:** **Broadcasting SDP in logs**
- **Mistake:** **No signaling redundancy**
- **Mistake:** **SFU vs P2P**
- **Mistake:** **[[SCTP (Stream Control Transmission Protocol)]] setup**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **One-to-many OTT viewers**
- **Con / skip when:** **RTMP ingest from OBS**
- **Con / skip when:** **Unauthenticated public rooms**

## Comparison
- vs [[HLS]]: **One-to-many OTT viewers**
- vs [[RTMP]]: **RTMP ingest from OBS** — [[RTMP]] to origin, not WebRTC signaling ([[OBS]]).


### Use cases
- Used wherever WebRTC Signaling channels sits in an ingest → package → CDN → p…
