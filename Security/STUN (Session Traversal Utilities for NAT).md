[[Security]] [[NAT Traversal]] [[ICE (Interactive Connectivity Establishment)]] [[TURN server (Traversal Using Relays around NAT)]] [[NAT (Network Address Translation)]] [[WebRTC]] [[WebRTC Signaling channels]] [[SDP (Session Description Protocol)]] [[P2P (Peer-to-Peer)]]

# STUN (Session Traversal Utilities for NAT)

> STUN asks a public server “how does the internet see me?” — you get a public IP:port to share for a direct path.

```txt
        STUN (Session Trav ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** WebRTC/NAT reviews: STUN discovers server-reflexive candidates; it is not …

## Sources
- [RFC 8489 — STUN](https://www.rfc-editor.org/rfc/rfc8489) — deep-dive
- [WebRTC — ICE overview](https://webrtc.org/getting-started/peer-connections) — overview

## Key Concepts
- **Core:** STUN lets a host ask a public server how the internet sees its IP:port, produ…

## Technical Details
```js
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    // Prefer your own STUN in prod; public ones are best-effort
  ],
})

pc.onicecandidate = (e) => {
  // Look for typ srflx in candidate.candidate
  if (e.candidate) signaling.send(e.candidate)
}
```

```bash
# coturn ships a client for Binding tests
turnutils_stunclient stun.l.google.com
# Or: stunclient / stun from package managers

# In Chrome: chrome://webrtc-internals → look for srflx candidates
```

| Knob | Why it matters |
|------|----------------|
| UDP to STUN host:3478 (or 19302) | No UDP out → no srflx |
| Own STUN vs public | Public STUN can rate-limit or fail; ops wants control |
| Dual-stack | Missing IPv6 STUN → half the paths missing |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| No `srflx` candidates | UDP blocked / wrong iceServers | Open outbound UDP; fix STUN URL; test with `turnutils_stunclient` |
| Works on LAN only | Only `host` candidates | Add working STUN; then TURN for hard NATs |
| srflx present, ICE still fails | Symmetric NAT / firewall | Deploy [[TURN server (Traversal Using Relays around NAT)]] |
| Wrong public IP in candidate | Multiple NATs / VPN | Test off VPN; use STUN that sees the path you care about |
| Intermittent Binding timeout | Flaky UDP / CGNAT | Retry; add TURN; prefer stable network path |
| Corporate “connecting” forever | UDP 3478 filtered | Try TURN over TCP/TLS 443 |

## Mistakes to Avoid
- **Mistake:** STUN ≠ relay
- **Mistake:** STUN does not traverse for you
- **Mistake:** Public STUN is not an SLA
- **Mistake:** VPN / split tunnel

## Pros/Cons or Trade-offs
- **Pro:** Enables many direct P2P paths without paying for relay bandwidth.
- **Con:** You already force all media through a media server / SFU with public IPs — path discovery is simpler; STUN optional.
- **Con:** One-to-many OTT — use [[HLS]] / [[DASH]]; not peer NAT punch.
- **Con:** You need guaranteed connectivity across corporate NATs — plan TURN first; STUN alone is not enough.

## Comparison
- vs [[TURN server (Traversal Using Relays around NAT)]]: STUN discovers addresses
- vs [[NAT Traversal]]: STUN is one ICE tool inside broader NAT traversal.


### Use cases
- WebRTC clients gather `srflx` candidates via public STUN (e.g
