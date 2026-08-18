[[Streaming]] [[WebRTC]] [[WebRTC Signaling channels]] [[ICE (Interactive Connectivity Establishment)]] [[SIP]]

# SDP (Session Description Protocol)

> Text blob that describes a media session — codecs, ports, ICE credentials — swapped as offer/answer before media flows.

## Mental model

**Say it in one breath:** In WebRTC/SIP, SDP is the **session contract** each side proposes; signaling carries it, then [[ICE (Interactive Connectivity Establishment)]] uses the ICE bits inside to find a path. It is **not** Bluetooth Service Discovery Protocol and **not** NIS.

```txt
Peer A                         Signaling                      Peer B
  │── createOffer() → SDP ────────►│──────── SDP offer ─────────►│
  │                                │◄─────── SDP answer ─────────│
  │◄──────── setRemoteDescription ─│                              │
  │                                                                │
  └────────── ICE checks + SRTP / DataChannel ────────────────────┘
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Offer / Answer** | SDP dance (RFC 3264) | “One side offers capabilities; the other answers a subset.” |
| --- | --- | --- |
| **m= lines** | Media sections (audio/video/app) | “Each m-line is a media kind we might send.” |
| **a=fingerprint** | DTLS cert hash | “We verify the DTLS peer matches SDP.” |
| **a=ice-ufrag / ice-pwd** | ICE auth for checks | “Connectivity checks prove we own this SDP.” |
| **a=candidate** | One ICE address (or trickle out-of-SDP) | “Trickle sends candidates separately over signaling.” |
| **setLocal / setRemote** | Apply SDP to the PC | “Never set remote before handling the matching signaling message.” |
| **Renegotiation** | New offer mid-call | “Add track / change direction → new offer/answer.” |

### Acronym collision (say this once)

| Acronym people say “SDP” | Actual meaning | This vault |

| **Session Description Protocol** | WebRTC / SIP session text | **This note** |
| --- | --- | --- |
| Bluetooth **Service Discovery Protocol** | Advertise BT profiles (A2DP, HID, etc.) | Not streaming — different stack |
| **NIS** / directory discovery | Legacy host/user maps | [[Network Information Service (NIS)]] |

> [!INFO]
> When a WebRTC interviewer says SDP, they mean **Session Description Protocol** on [[WebRTC Signaling channels]] — offer/answer, not Bluetooth `sdptool`.

### What an SDP offer answers

| Question | Where in SDP |

| What codecs? | `a=rtpmap` / `a=fmtp` |
| --- | --- |
| Send, receive, or both? | `a=sendrecv` / `sendonly` / `recvonly` / `inactive` |
| How do we authenticate ICE? | `a=ice-ufrag`, `a=ice-pwd` |
| How do we authenticate DTLS? | `a=fingerprint`, `a=setup` |
| DataChannel? | `m=application` + SCTP port / `a=sctp-port` |

Media still needs ICE + DTLS after SDP agrees — SDP alone does not open UDP.

## Standard config / commands

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

Pairs with [[WebRTC Signaling channels]] WHIP/WHEP; still ICE under the hood.

| Knob | Why it matters |

| `createOffer` after `addTrack` | Tracks missing from SDP if added too late without renegotiation |
| --- | --- |
| Trickle ICE | Candidates often **not** all inlined; send via signaling as they appear |
| Perfect negotiation (polite peer) | Avoid glare when both sides offer |
| Codec prefs (`setCodecPreferences`) | Force H.264/VP8/AV1 before offer |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `InvalidStateError` on setRemote | Wrong signaling order | setRemote(offer) before createAnswer; don’t double-apply |
| Connected but no video | `a=inactive` / wrong direction | Renegotiate with sendrecv; verify addTrack |
| DTLS fails | fingerprint mismatch | Don’t rewrite SDP by hand; end-to-end integrity on signaling |
| ICE fails after “have-local-offer” | No candidates / no TURN | See [[ICE (Interactive Connectivity Establishment)]] |
| DataChannel missing | No application m-line | `createDataChannel` before offer or renegotiate ([[SCTP (Stream Control Transmission Protocol)]]) |
| Glare (both offered) | Two offers same time | Polite/impolite peer pattern |
| Codec mismatch | No common rtpmap | Align codec list; SFU may rewrite SDP |

## Gotchas

> [!WARNING]
> **Don’t hand-edit SDP in production** — easy to break ICE ufrag/pwd or fingerprint; use WebRTC APIs / SFU helpers.

> [!WARNING]
> **Logging full SDP** — leaks ICE passwords and fingerprints; treat as sensitive.

> [!WARNING]
> **SDP is not the media path** — swapping offer/answer over HTTPS does not mean UDP/TURN works.

> [!WARNING]
> **Wrong “SDP” in a streaming interview** — Bluetooth Service Discovery is unrelated; pivot to Session Description Protocol + signaling.

> [!WARNING]
> **Bundle / mid** — modern browsers bundle media on one ICE transport; mismatched mid after renegotiation breaks tracks.

## When NOT to use

- **CDN OTT manifests** — [[HLS]] / [[DASH]] use M3U8/MPD, not SDP offer/answer.
- **Bluetooth profile discovery** — different SDP; use BlueZ/`sdptool`, not WebRTC notes.
- **Plain file HTTP streaming** — [[How to attach stream to HTTP handlers]]; no session description.

## Related

[[WebRTC]] [[WebRTC Signaling channels]] [[ICE (Interactive Connectivity Establishment)]] [[TURN server (Traversal Using Relays around NAT)]] [[SCTP (Stream Control Transmission Protocol)]] [[SIP]] [[WebRTC Get Started Guide]] [[Network Information Service (NIS)]]
