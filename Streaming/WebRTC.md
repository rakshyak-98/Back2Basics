[[Streaming]] [[ICE (Interactive Connectivity Establishment)]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]] [[SCTP (Stream Control Transmission Protocol)]]

# WebRTC

> Browser P2P real-time A/V + data — media is encrypted UDP, not HTTP.

## Interview Relevance

Interviewers probe whether you can walk WebRTC end-to-end — not just name it. Signal fluency with **getUserMedia**, **RTCPeerConnection**, **SDP**, **Signaling** and when you would pick a different path.

## Sources

- [Wikipedia — WebRTC](https://en.wikipedia.org/wiki/WebRTC) — overview
- [WebRTC W3C](https://www.w3.org/TR/webrtc/) — deep-dive
- [MDN WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API) — overview

## Core Definition

Signaling carries **SDP + candidates**. Media never goes through your WebSocket in pure P2P — only through TURN/SFU when those are in the path.

## Key Concepts

- **getUserMedia:** Ask OS for camera/mic — “First I capture a local MediaStream.”
- **RTCPeerConnection:** The session object — “One PC per remote peer (or SFU edge).”
- **SDP:** Session Description Protocol — codecs + ICE creds — “Offer/answer swaps what we can send.”
- **Signaling:** Your app’s side channel — “WebRTC has no built-in signaling — I own that.”
- **ICE:** Path finder behind NAT — “Gather candidates, check pairs, pick a path.”
- **STUN / TURN:** Discover public face / relay media — “STUN finds; TURN carries when direct fails.”
- **DataChannel:** Reliable/unreliable messages — “SCTP over DTLS — not the same pipe as RTP.”
- **SFU:** Server that fans out media — “Clients uplink once; SFU forwards to N peers.”

**Flow:**

1. **Capture** — `getUserMedia` → local preview + tracks on the PC.
2. **Signal** — create offer → setLocalDescription → send SDP via [[WebRTC Signaling channels]]; remote answers.
3. **ICE** — exchange candidates; [[ICE (Interactive Connectivity Establishment)]] picks host → srflx → relay ([[TURN server (Traversal Using Relays around NAT)]]).
4. **Media** — SRTP flows peer-to-peer or via TURN/SFU; DataChannel optional.

### Three APIs you actually use

| API | Job |
|-----|-----|
| `navigator.mediaDevices.getUserMedia` | Capture camera/mic (or `getDisplayMedia` for screen) |
| `RTCPeerConnection` | Negotiate, ICE, encrypt, send/receive A/V |
| `RTCPeerConnection.createDataChannel` | App messages over [[SCTP (Stream Control Transmission Protocol)]] |

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

Debug: `chrome://webrtc-internals` — ICE state, selected pair, codecs.

See [[WebRTC Get Started Guide]] for constraints / device enumeration.

## Real-World Applications

Signaling carries **SDP + candidates**. Media never goes through your WebSocket in pure P2P — only through TURN/SFU when those are in the path.

Used wherever WebRTC sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **One-to-many OTT (millions of viewers)** — [[HLS]] / [[DASH]] + CDN; WebRTC is for few peers or SFU-scale interactive.
- **Con / skip when:** **OBS → origin ingest for linear** — usually [[RTMP]] / SRT into a packager ([[flussonic]]), not browser WebRTC.
- **Con / skip when:** **Fire-and-forget file download** — HTTP range / Node streams ([[How to attach stream to HTTP handlers]]); no ICE needed.

## Comparison

- vs [[HLS]]: **One-to-many OTT (millions of viewers)** — [[HLS]] / [[DASH]] + CDN; WebRTC is for few peers or SFU-scale interactive.
- vs [[RTMP]]: **OBS → origin ingest for linear** — usually [[RTMP]] / SRT into a packager ([[flussonic]]), not browser WebRTC.
- vs [[How to attach stream to HTTP handlers]]: **Fire-and-forget file download** — HTTP range / Node streams ([[How to attach stream to HTTP handlers]]); no ICE needed.

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

- **No signaling in the standard** — you must build WebSocket/HTTPS/WHIP. Forgetting auth on rooms = free SFU / TURN abuse.
- **STUN ≠ TURN** — STUN only discovers addresses. Without [[TURN server (Traversal Using Relays around NAT)]], a slice of users never connect.
- **SDP in logs** — contains ICE passwords and DTLS fingerprints; scrub production logs.
- **P2P tutorials ≠ SFU products** — LiveKit/Janus/mediasoup: you signal to the server; media topology differs.
- **Mobile background** — OS may pause camera; renegotiate or swap tracks on resume.
