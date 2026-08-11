[[Streaming]] [[ICE (Interactive Connectivity Establishment)]] [[WebRTC Signaling channels]] [[TURN server (Traversal Using Relays around NAT)]] [[SCTP (Stream Control Transmission Protocol)]]

# WebRTC

> Browser P2P real-time A/V + data — media is encrypted UDP, not HTTP.

---

## Mental model

**Say it in one breath:** WebRTC lets two browsers (or a browser and a media server) send live audio, video, and data over UDP with encryption — you only write signaling; the browser does capture, encode, NAT traversal, and SRTP.

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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **getUserMedia** | Ask OS for camera/mic | “First I capture a local MediaStream.” |
| **RTCPeerConnection** | The session object | “One PC per remote peer (or SFU edge).” |
| **SDP** | Session Description Protocol — codecs + ICE creds | “Offer/answer swaps what we can send.” |
| **Signaling** | Your app’s side channel | “WebRTC has no built-in signaling — I own that.” |
| **ICE** | Path finder behind NAT | “Gather candidates, check pairs, pick a path.” |
| **STUN / TURN** | Discover public face / relay media | “STUN finds; TURN carries when direct fails.” |
| **DataChannel** | Reliable/unreliable messages | “SCTP over DTLS — not the same pipe as RTP.” |
| **SFU** | Server that fans out media | “Clients uplink once; SFU forwards to N peers.” |

### Three APIs you actually use

| API | Job |
|-----|-----|
| `navigator.mediaDevices.getUserMedia` | Capture camera/mic (or `getDisplayMedia` for screen) |
| `RTCPeerConnection` | Negotiate, ICE, encrypt, send/receive A/V |
| `RTCPeerConnection.createDataChannel` | App messages over [[SCTP (Stream Control Transmission Protocol)]] |

### How the story goes (video call)

1. **Capture** — `getUserMedia` → local preview + tracks on the PC.
2. **Signal** — create offer → setLocalDescription → send SDP via [[WebRTC Signaling channels]]; remote answers.
3. **ICE** — exchange candidates; [[ICE (Interactive Connectivity Establishment)]] picks host → srflx → relay ([[TURN server (Traversal Using Relays around NAT)]]).
4. **Media** — SRTP flows peer-to-peer or via TURN/SFU; DataChannel optional.

> [!INFO]
> Signaling carries **SDP + candidates**. Media never goes through your WebSocket in pure P2P — only through TURN/SFU when those are in the path.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied / black local video | `getUserMedia` error; HTTPS? | Serve over HTTPS (or localhost); fix constraints |
| Stuck “connecting” | ICE in webrtc-internals | Add STUN; deploy TURN; see [[ICE (Interactive Connectivity Establishment)]] |
| Works same Wi‑Fi only | Host-only candidates | STUN for srflx; TURN for hard NATs |
| One-way media | SDP direction / `ontrack` never fired | Ensure remote `addTrack`; renegotiate after late tracks |
| Audio/video OK, chat dead | DataChannel created after answer | Create DataChannel before offer, or renegotiate |
| Connect then silence on network change | `iceConnectionState` failed | `restartIce()` + new offer |
| High CPU / choppy | Encoder overload in stats | Lower resolution/fps; prefer hardware codecs |

---

## Gotchas

> [!WARNING]
> **No signaling in the standard** — you must build WebSocket/HTTPS/WHIP. Forgetting auth on rooms = free SFU / TURN abuse.

> [!WARNING]
> **STUN ≠ TURN** — STUN only discovers addresses. Without [[TURN server (Traversal Using Relays around NAT)]], a slice of users never connect.

> [!WARNING]
> **SDP in logs** — contains ICE passwords and DTLS fingerprints; scrub production logs.

> [!WARNING]
> **P2P tutorials ≠ SFU products** — LiveKit/Janus/mediasoup: you signal to the server; media topology differs.

> [!WARNING]
> **Mobile background** — OS may pause camera; renegotiate or swap tracks on resume.

---

## When NOT to use

- **One-to-many OTT (millions of viewers)** — [[HLS]] / [[DASH]] + CDN; WebRTC is for few peers or SFU-scale interactive.
- **OBS → origin ingest for linear** — usually [[RTMP]] / SRT into a packager ([[flussonic]]), not browser WebRTC.
- **Fire-and-forget file download** — HTTP range / Node streams ([[How to attach stream to HTTP handlers]]); no ICE needed.

---

## Related

[[WebRTC Get Started Guide]] [[WebRTC Signaling channels]] [[ICE (Interactive Connectivity Establishment)]] [[TURN server (Traversal Using Relays around NAT)]] [[SCTP (Stream Control Transmission Protocol)]] [[SDP (Session Description Protocol)]] [[HLS]] [[DASH]] [[RTMP]]
