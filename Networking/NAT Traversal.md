[[Networking]] [[NAT (Network Address Translation)]] [[ICE (Interactive Connectivity Establishment)]]

# NAT Traversal

> NAT traversal gets two peers behind NATs talking — discover public addresses, try direct, else relay.

---

## Mental model

**Say it in one breath:** Private IPs cannot be dialed from the internet. Traversal means learn your public face, try to punch a hole, and if that fails send media through a relay.

```txt
User A (LAN) ---- NAT A ---- Internet ---- NAT B ---- User B (LAN)
                     ▲                        ▲
                     └──── need a path both sides accept ────┘
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Hole punching** | Both sides send outbound so NATs open mappings | “We poke both NATs so return packets are allowed.” |
| **STUN** | Ask a server your public IP:port | “STUN shows how the internet sees me.” |
| **ICE** | Try many address pairs; pick one that works | “ICE finds a working path.” |
| **TURN** | Relay when direct fails | “TURN carries media when punch fails.” |
| **Symmetric NAT** | Mapping changes per remote peer | “Symmetric NAT usually forces TURN.” |

### How the story goes (3 steps)

1. **Discover** — each peer asks [[STUN (Session Traversal Utilities for NAT)]] for its public IP:port.
2. **Try direct** — [[ICE (Interactive Connectivity Establishment)]] checks candidate pairs (host → srflx).
3. **Relay** — if checks fail, use [[TURN server (Traversal Using Relays around NAT)]].

Phone analogy: desk extension = private IP; main company number = public IP; receptionist = STUN; operator = TURN.

---

## Standard config / commands

WebRTC (browser):

```js
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'turn:turn.example.com:3478', username: 'u', credential: 'p' },
  ],
})
```

Debug: `chrome://webrtc-internals` → ICE candidate types (host / srflx / relay).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Works same Wi‑Fi only | Only host candidates | Add STUN; confirm UDP egress |
| Stuck connecting | No relay candidates | Deploy TURN with short-lived creds |
| One side behind corp firewall | UDP 3478/443 blocked | TURN over TCP/TLS 443 |
| High latency / cost | All pairs are relay | Fix firewall; prefer `iceTransportPolicy: 'all'` |
| Works then dies on network switch | Binding gone | ICE restart |

---

## Gotchas

> [!WARNING]
> **STUN alone is not enough** — it discovers addresses; it does not relay media.

> [!WARNING]
> **Signaling ≠ traversal** — your WebSocket only swaps SDP/candidates; STUN/TURN URLs live in the peer connection config.

> [!WARNING]
> **CGNAT / symmetric NAT** — expect ~5–15% of users to need TURN in production.

---

## When NOT to use

- **Client → your public server only** — normal TCP/TLS; no peer punch required.
- **One-to-many OTT** — [[HLS]] / [[DASH]] via CDN, not P2P traversal.

---

## Related

[[NAT (Network Address Translation)]] [[ICE (Interactive Connectivity Establishment)]] [[STUN (Session Traversal Utilities for NAT)]] [[TURN server (Traversal Using Relays around NAT)]] [[P2P (Peer-to-Peer)]] [[WebRTC]] [[UDP]]
