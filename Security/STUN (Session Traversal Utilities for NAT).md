[[Security]] [[NAT Traversal]] [[ICE (Interactive Connectivity Establishment)]] [[TURN server (Traversal Using Relays around NAT)]] [[NAT (Network Address Translation)]] [[WebRTC]] [[WebRTC Signaling channels]] [[SDP (Session Description Protocol)]] [[P2P (Peer-to-Peer)]]

# STUN (Session Traversal Utilities for NAT)

> STUN asks a public server “how does the internet see me?” — you get a public IP:port to share for a direct path.

## Interview Relevance

WebRTC/NAT interviews: STUN discovers server-reflexive candidates; it is not a relay — TURN is.

## Sources

- [RFC 8489 — STUN](https://www.rfc-editor.org/rfc/rfc8489) — deep-dive
- [WebRTC — ICE overview](https://webrtc.org/getting-started/peer-connections) — overview

## Core Definition

STUN lets a host ask a public server how the internet sees its IP:port, producing a server-reflexive address for ICE candidate gathering.

## Key Concepts

```txt
Client (private 192.168.1.10:4000)
        │  Binding Request (UDP)
        ▼
   STUN server (public)
        │  Binding Response: XOR-MAPPED-ADDRESS = 203.0.113.5:6000
        ▼
Client now has an srflx candidate for [[ICE (Interactive Connectivity Establishment)]]
```

### Interview map (words you can say)

| Word                         | Plain meaning                                                    | Say in interview                                        |
| ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- |
| **Binding**                  | The STUN request/response that asks “what is my mapped address?” | “I send a Binding request; STUN echoes my public face.” |
| **srflx** (server-reflexive) | Public IP:port STUN saw                                          | “srflx is how the internet sees this socket.”           |
| **NAT type**                 | How the mapping behaves (full cone vs symmetric, etc.)           | “Symmetric NAT often breaks STUN-only paths.”           |
| **Hole punch**               | Both sides send so NATs allow return traffic                     | “STUN gives the address; punching still has to work.”   |
| **Signaling**                | Side channel that swaps addresses/SDP                            | “STUN discovers; signaling shares; ICE picks.”          |

### STUN vs TURN (one line each)

| Tool                                                           | Job                                      |
| -------------------------------------------------------------- | ---------------------------------------- |
| **STUN**                                                       | Discover public IP:port — no media relay |
| **TURN** ([[TURN server (Traversal Using Relays around NAT)]]) | Relay media when direct/punch fails      |

> [!INFO]
> STUN helps you **find** your public face. TURN **carries** media. ICE **chooses** the path.

### How the story goes

1. Client binds a local UDP socket and queries STUN.
2. STUN returns mapped address → becomes an ICE **srflx** candidate.
3. Peers exchange candidates over [[WebRTC Signaling channels]] / [[SDP (Session Description Protocol)]].
4. Connectivity checks try the pair; if NAT is too hostile, fall back to TURN.

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

## Real-World Applications

WebRTC clients gather `srflx` candidates via public STUN (e.g. Google 19302) before trying TURN.

## Pros/Cons or Trade-offs

- **Pro:** Enables many direct P2P paths without paying for relay bandwidth.
- **Con:** You already force all media through a media server / SFU with public IPs — path discovery is simpler; STUN optional.
- **Con:** One-to-many OTT — use [[HLS]] / [[DASH]]; not peer NAT punch.
- **Con:** You need guaranteed connectivity across corporate NATs — plan TURN first; STUN alone is not enough.

## Comparison

- vs [[TURN server (Traversal Using Relays around NAT)]]: STUN discovers addresses; TURN relays media.
- vs [[NAT Traversal]]: STUN is one ICE tool inside broader NAT traversal.

## Mistakes to Avoid

- STUN ≠ relay — discovering an address does not mean peers can reach it. Symmetric NAT and strict firewalls need TURN.
- STUN does not traverse for you — it only reports the mapping. Hole punching and ICE checks still must succeed.
- Public STUN is not an SLA — fine for demos; production wants your own STUN/TURN (or a paid edge).
- VPN / split tunnel — mapped address may be the VPN egress, not the path your peer expects.
