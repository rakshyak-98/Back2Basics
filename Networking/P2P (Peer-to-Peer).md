[[Networking]] [[NAT Traversal]] [[WebRTC]] [[ICE (Interactive Connectivity Establishment)]] [[TURN server (Traversal Using Relays around NAT)]] [[IPFS (InterPlanetry File System)]] [[UDP]] [[WebRTC Signaling channels]]

# P2P (Peer-to-Peer)

> P2P means peers talk to each other — share load and data without every byte going through your central server.

```txt
        P2P (Peer-to-Peer) ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use P2P to test whether you know signaling vs media path, mesh v…

## Sources
- [Wikipedia — P2P](https://en.wikipedia.org/wiki/P2P) — overview

## Technical Details
```txt
     Peer A ←──direct or relay──► Peer B
        │                            │
        └──────── signaling / tracker (optional) ─┘
```

| Word | Plain meaning | Review phrasing |
|------|---------------|-------------------|
| **Peer** | Node that sends and receives | Every peer can upload and download. |
| **Tracker / signaling** | Helper that introduces peers | We still need a meeting point to find each other. |
| **Mesh** | Many peers interconnect | Mesh fans out; fan-out cost grows fast. |
| **Relay / SFU** | Server that forwards media | For calls we often use an SFU, not full mesh. |
| **NAT** | Blocks unsolicited inbound | P2P needs [[NAT Traversal]] in the real world. |

- Call-style P2P flow:

1. **Meet** — peers find each other via signaling/tracker (not the media path).
2. **Path** — [[ICE (Interactive Connectivity Establishment)]] finds direct or [[TURN server (Traversal Using Relays around NAT)]].
3. **Exchange** — media/data flows peer↔peer (or via SFU for many-party).

- WebRTC mesh (2 peers): `RTCPeerConnection` + signaling

- Many-party: prefer SFU (Selective Forwarding Unit) over full mesh

```js
// Conceptual: one upload to SFU, not N-1 mesh links
pc.addTrack(localTrack)
// SFU forwards to other participants
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Works on LAN only | NAT / no STUN-TURN | Add ICE servers; deploy TURN |
| CPU melts at 5+ users | Full mesh | Switch to SFU / MCU |
| Uneven share | Free-riders | Incentives, server assist, or CDN hybrid |
| Security incident | Trusting any peer | Authenticate signaling; encrypt; validate payloads |
| Mobile battery drain | Always-on mesh | Limit links; duty-cycle; move heavy work to edge servers |

## Mistakes to Avoid
- **Mistake:** Claiming P2P needs no servers
- **Mistake:** Using full mesh beyond a handful of peers
- **Mistake:** Trusting peers by default
- **Mistake:** Choosing P2P for strong audit/compliance or tiny control-plane A…

## Pros/Cons or Trade-offs
- **Pro:** Offloads bandwidth and compute to peers; can lower central server cost and latency for direct paths.
- **Con:** NAT, trust, free-riders, and mesh scaling force signaling, TURN, and often an SFU — "no infrastructure" is a myth on the public internet.

## Comparison
- vs client–server: client–server puts all data through your backend


### Use cases
- Video calls ([[WebRTC]]), file sharing, game updates, and live contribution w…
