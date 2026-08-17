[[Streaming]] [[ICE (Interactive Connectivity Establishment)]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]] [[SCTP (Stream Control Transmission Protocol)]]

# WebRTC

> Browser P2P real-time A/V + data — media is encrypted UDP, not HTTP.

```txt
        WebRTC ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk WebRTC end-to-end

## Sources
- [Wikipedia — WebRTC](https://en.wikipedia.org/wiki/WebRTC) — overview
- [WebRTC W3C](https://www.w3.org/TR/webrtc/) — deep-dive
- [MDN WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API) — overview

## Key Concepts
- **getUserMedia:** Ask OS for camera/mic — “First I capture a local MediaStream.”
- **RTCPeerConnection:** The session object — “One PC per remote peer (or SFU edge).”
- **SDP:** Session Description Protocol
- **Signaling:** Your app’s side channel — “WebRTC has no built-in signaling — I own that.”
- **ICE:** Path finder behind NAT — “Gather candidates, check pairs, pick a path.”
- **STUN / TURN:** Discover public face / relay media
- **DataChannel:** Reliable/unreliable messages — “SCTP over DTLS — not the same pipe as RTP.”
- **SFU:** Server that fans out media — “Clients uplink once; SFU forwards to N peers.”

**Flow:**

- **Note:** 1. **Capture** — `getUserMedia` → local preview + tracks on the PC.
- **Note:** 2. **Signal**
- **Note:** 3. **ICE** — exchange candidates
- **Note:** 4. **Media** — SRTP flows peer-to-peer or via TURN/SFU; DataChannel optional.

### Three APIs you actually use

| API | Job |
|-----|-----|
| `navigator.mediaDevices.getUserMedia` | Capture camera/mic (or `getDisplayMedia` for screen) |
| `RTCPeerConnection` | Negotiate, ICE, encrypt, send/receive A/V |
| `RTCPeerConnection.createDataChannel` | App messages over [[SCTP (Stream Control Transmission Protocol)]] |


- **Core:** Signaling carries **SDP + candidates**. Media never goes through your WebSock…

## Technical Details
```txt
getUserMedia / getDisplayMedia
        │
        ▼
  MediaStream tracks ──addTrack──► RTCPeerConnection
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
              [[WebRTC Signaling channels]]   [[ICE (Interactive Connectivity Establishment)]]
              (SDP offer/answer +             (host / STUN / TURN path)
               candidates over WS/HTTP)
                                        │
                                        ▼
                         SRTP media (A/V) + DataChannel
                         ([[SCTP (Stream Control Transmission Protocol)]] over DTLS)
```

```js
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    {
      urls: 'turn:turn.example.com:3478',
      username: 'u',
      credential: 'p', // short-lived from your API
    },
  ],
})

const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: true })
stream.getTracks().forEach((t) => pc.addTrack(t, stream))

pc.onicecandidate = (e) => {
  if (e.candidate) signaling.send({ type: 'candidate', candidate: e.candidate })
}
pc.ontrack = (e) => {
  remoteVideo.srcObject = e.streams[0]
}

const offer = await pc.createOffer()
await pc.setLocalDescription(offer)
signaling.send({ type: 'offer', sdp: pc.localDescription })
```

| Knob | Why it matters |
|------|----------------|
| `iceServers` | Without STUN/TURN, only same-LAN host candidates work |
| `addTrack` before offer | Tracks must be on PC so SDP advertises send media |
| Trickle ICE | Send candidates as they arrive — faster connect |
| `getStats()` | Bitrate, packet loss, RTT for live quality dashboards |

- Debug: `chrome://webrtc-internals` — ICE state, selected pair, codecs.

- See [[WebRTC Get Started Guide]] for constraints / device enumeration.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied / black local video | `getUserMedia` error; HTTPS? | Serve over HTTPS (or localhost); fix constraints |
| Stuck “connecting” | ICE in webrtc-internals | Add STUN; deploy TURN; see [[ICE (Interactive Connectivity Establishment)]] |
| Works same Wi‑Fi only | Host-only candidates | STUN for srflx; TURN for hard NATs |
| One-way media | SDP direction / `ontrack` never fired | Ensure remote `addTrack`; renegotiate after late tracks |
| Audio/video OK, chat dead | DataChannel created after answer | Create DataChannel before offer, or renegotiate |
| Connect then silence on network change | `iceConnectionState` failed | `restartIce()` + new offer |
| High CPU / choppy | Encoder overload in stats | Lower resolution/fps; prefer hardware codecs |

- **Mistake:** **No signaling in the standard**
- **Mistake:** **STUN ≠ TURN**
- **Mistake:** **SDP in logs**
- **Mistake:** **P2P tutorials ≠ SFU products**
- **Mistake:** **Mobile background**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **One-to-many OTT (millions of viewers)**
- **Con / skip when:** **OBS → origin ingest for linear**
- **Con / skip when:** **Fire-and-forget file download**

## Comparison
- vs [[HLS]]: **One-to-many OTT (millions of viewers)**
- vs [[RTMP]]: **OBS → origin ingest for linear**
- vs [[How to attach stream to HTTP handlers]]: **Fire-and-forget file download**


### Use cases
- Signaling carries **SDP + candidates**. Media never goes through your WebSock…

- Used wherever WebRTC sits in an ingest → package → CDN → player path
