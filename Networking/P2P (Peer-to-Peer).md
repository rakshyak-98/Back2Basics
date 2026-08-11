[[Networking]] [[NAT Traversal]] [[WebRTC]]

# P2P (Peer-to-Peer)

> P2P means peers talk to each other — share load and data without every byte going through your central server.

---

## Mental model

**Say it in one breath:** Each node is both client and server. Adding users adds capacity — and also adds NAT/firewall pain.

```txt
     Peer A ←──direct or relay──► Peer B
        │                            │
        └──────── signaling / tracker (optional) ─┘
```

Used for: video calls ([[WebRTC]]), file sharing, game updates, live contribution when you want edge capacity.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Peer** | Node that sends and receives | “Every peer can upload and download.” |
| **Tracker / signaling** | Helper that introduces peers | “We still need a meeting point to find each other.” |
| **Mesh** | Many peers interconnect | “Mesh fans out; fan-out cost grows fast.” |
| **Relay / SFU** | Server that forwards media | “For calls we often use an SFU, not full mesh.” |
| **NAT** | Blocks unsolicited inbound | “P2P needs [[NAT Traversal]] in the real world.” |

### How a call-style P2P story goes

1. **Meet** — peers find each other via signaling/tracker (not the media path).
2. **Path** — [[ICE (Interactive Connectivity Establishment)]] finds direct or [[TURN server (Traversal Using Relays around NAT)]].
3. **Exchange** — media/data flows peer↔peer (or via SFU for many-party).

---

## Standard config / commands

WebRTC mesh (2 peers): `RTCPeerConnection` + signaling — see [[WebRTC Signaling channels]].

Many-party: prefer SFU (Selective Forwarding Unit) over full mesh — each client uploads once.

```js
// Conceptual: one upload to SFU, not N-1 mesh links
pc.addTrack(localTrack)
// SFU forwards to other participants
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Works on LAN only | NAT / no STUN-TURN | Add ICE servers; deploy TURN |
| CPU melts at 5+ users | Full mesh | Switch to SFU / MCU |
| Uneven share | Free-riders | Incentives, server assist, or CDN hybrid |
| Security incident | Trusting any peer | Auth signaling; encrypt; validate payloads |
| Mobile battery drain | Always-on mesh | Limit links; duty-cycle; move heavy work to edge servers |

---

## Gotchas

> [!WARNING]
> **“No infrastructure” is a myth for internet P2P** — you still need signaling, STUN/TURN, and often an SFU.

> [!WARNING]
> **Mesh scales O(N²)** — fine for 2–4; painful beyond.

> [!WARNING]
> **Trust** — peers are hostile by default; authenticate and encrypt.

---

## When NOT to use

- **One-to-many OTT video** — [[HLS]] / [[DASH]] + CDN.
- **Strong audit / compliance** — central server with clear custody may be required.
- **Tiny control-plane APIs** — plain HTTPS to your backend is simpler.

---

## Related

[[NAT Traversal]] [[WebRTC]] [[ICE (Interactive Connectivity Establishment)]] [[TURN server (Traversal Using Relays around NAT)]] [[IPFS (InterPlanetry File System)]] [[UDP]]
