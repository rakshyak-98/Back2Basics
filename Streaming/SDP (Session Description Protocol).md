[[Streaming]] [[WebRTC]] [[WebRTC Signaling channels]] [[ICE (Interactive Connectivity Establishment)]] [[SIP]] [[TURN server (Traversal Using Relays around NAT)]] [[SCTP (Stream Control Transmission Protocol)]] [[WebRTC Get Started Guide]] [[Network Information Service (NIS)]]

# SDP (Session Description Protocol)

> Text blob that describes a media session — codecs, ports, ICE credentials — swapped as offer/answer before media flows.

```txt
        SDP (Session Descr ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk SDP end-to-end

## Sources
- [Wikipedia — SDP](https://en.wikipedia.org/wiki/SDP) — overview
- [RFC 8866 — SDP](https://datatracker.ietf.org/doc/html/rfc8866) — deep-dive

## Key Concepts
- **Offer / Answer:** SDP dance (RFC 3264)
- **m= lines:** Media sections (audio/video/app)
- **a=fingerprint:** DTLS cert hash — “We verify the DTLS peer matches SDP.”
- **a=ice-ufrag / ice-pwd:** ICE auth for checks — “Connectivity checks prove we own this SDP.”
- **a=candidate:** One ICE address (or trickle out-of-SDP)
- **setLocal / setRemote:** Apply SDP to the PC
- **Renegotiation:** New offer mid-call — “Add track / change direction → new offer/answer.”
- **Acronym people say “SDP”:** Actual meaning — This vault
- **Session Description Protocol:** WebRTC / SIP session text — **This note**
- **Bluetooth Service Discovery Protocol:** Advertise BT profiles (A2DP, HID, etc.) — Not streaming — different stack
- **NIS / directory discovery:** Legacy host/user maps — [[Network Information Service (NIS)]]

### Acronym collision (say this once)

| Acronym people say “SDP” | Actual meaning | This vault |
|--------------------------|----------------|------------|
| **Session Description Protocol** | WebRTC / SIP session text | **This note** |
| Bluetooth **Service Discovery Protocol** | Advertise BT profiles (A2DP, HID, etc.) | Not streaming — different stack |
| **NIS** / directory discovery | Legacy host/user maps | [[Network Information Service (NIS)]] |

### What an SDP offer answers

| Question | Where in SDP |
|----------|----------------|
| What codecs? | `a=rtpmap` / `a=fmtp` |
| Send, receive, or both? | `a=sendrecv` / `sendonly` / `recvonly` / `inactive` |
| How do we authenticate ICE? | `a=ice-ufrag`, `a=ice-pwd` |
| How do we authenticate DTLS? | `a=fingerprint`, `a=setup` |
| DataChannel? | `m=application` + SCTP port / `a=sctp-port` |

- **Note:** Media still needs ICE + DTLS after SDP agrees — SDP alone does not open UDP.


- **Core:** When a WebRTC reviewer says SDP, they mean **Session Description Protocol*…

## Technical Details
```txt
Peer A                         Signaling                      Peer B
  │── createOffer() → SDP ────────►│──────── SDP offer ─────────►│
  │                                │◄─────── SDP answer ─────────│
  │◄──────── setRemoteDescription ─│                              │
  │                                                                │
  └────────── ICE checks + SRTP / DataChannel ────────────────────┘
```

### Browser offer/answer

```js
const pc = new RTCPeerConnection({
  iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
})

// Offerer
const offer = await pc.createOffer()
await pc.setLocalDescription(offer)
signaling.send({ type: 'offer', sdp: pc.localDescription.sdp })

// Answerer (on message)
await pc.setRemoteDescription({ type: 'offer', sdp: msg.sdp })
const answer = await pc.createAnswer()
await pc.setLocalDescription(answer)
signaling.send({ type: 'answer', sdp: pc.localDescription.sdp })
```

### Inspect (Chrome)

```txt
chrome://webrtc-internals → createOffer / setLocalDescription / setRemoteDescription
Look for: m= lines, ice-ufrag, fingerprint, selected candidate pair
```

### WHIP-style HTTP (ingest)

```txt
POST /whip  Content-Type: application/sdp
<body = offer SDP>
← 201  body = answer SDP
```

- Pairs with [[WebRTC Signaling channels]] WHIP/WHEP; still ICE under the hood.

| Knob | Why it matters |
|------|----------------|
| `createOffer` after `addTrack` | Tracks missing from SDP if added too late without renegotiation |
| Trickle ICE | Candidates often **not** all inlined; send via signaling as they appear |
| Perfect negotiation (polite peer) | Avoid glare when both sides offer |
| Codec prefs (`setCodecPreferences`) | Force H.264/VP8/AV1 before offer |

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| `InvalidStateError` on setRemote | Wrong signaling order | setRemote(offer) before createAnswer; don’t double-apply |
| Connected but no video | `a=inactive` / wrong direction | Renegotiate with sendrecv; verify addTrack |
| DTLS fails | fingerprint mismatch | Don’t rewrite SDP by hand; end-to-end integrity on signaling |
| ICE fails after “have-local-offer” | No candidates / no TURN | See [[ICE (Interactive Connectivity Establishment)]] |
| DataChannel missing | No application m-line | `createDataChannel` before offer or renegotiate ([[SCTP (Stream Control Transmission Protocol)]]) |
| Glare (both offered) | Two offers same time | Polite/impolite peer pattern |
| Codec mismatch | No common rtpmap | Align codec list; SFU may rewrite SDP |

- **Mistake:** **Don’t hand-edit SDP in production**
- **Mistake:** **Logging full SDP**
- **Mistake:** **SDP is not the media path**
- **Mistake:** **Wrong “SDP” in a streaming review**
- **Mistake:** **Bundle / mid**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **CDN OTT manifests**
- **Con / skip when:** **Bluetooth profile discovery**
- **Con / skip when:** **Plain file HTTP streaming**

## Comparison
- vs [[HLS]]: **CDN OTT manifests** — [[HLS]] / [[DASH]] use M3U8/MPD, not SDP offer/answer.
- vs [[How to attach stream to HTTP handlers]]: **Plain file HTTP streaming**


### Use cases
- When a WebRTC reviewer says SDP, they mean **Session Description Protocol*…

- Used wherever SDP sits in an ingest → package → CDN → player path
