[[TURN server (Traversal Using Relays around NAT)]] [[STUN (Session Traversal Utilities for NAT)]] [[ICE (Interactive Connectivity Establishment)]] [[NAT Traversal]] [[NAT (Network Address Translation)]] [[WebRTC]] [[P2P (Peer-to-Peer)]]

# Relay server

> A relay server is a middle box both peers dial out to — it forwards bytes when they cannot connect directly through NAT.

```txt
        Relay server ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers separate STUN (discover addresses) from TURN/relay (carry media)…

## Sources
- [RFC 8656 — Traversal Using Relays around NAT (TURN)](https://datatracker.ietf.org/doc/html/rfc8656) — deep-dive
- [RFC 8445 — ICE](https://datatracker.ietf.org/doc/html/rfc8445) — overview
- [WebRTC — ICE](https://webrtc.org/getting-started/peer-connections) — overview

## Technical Details
```txt
Peer A ──outbound──► Relay ◄──outbound── Peer B
                       │
                  forwards A↔B
```

- In WebRTC this is usually [[TURN server (Traversal Using Relays around NAT)]].
- [[STUN (Session Traversal Utilities for NAT)]] only discovers addresses
- [[ICE (Interactive Connectivity Establishment)]] picks relay after cheaper pa…

- When outbound is also blocked (strict egress):

1. Allowlist TURN IPs/ports (best).
2. TURN over TLS/WebSocket on 443.
3. Corporate forward HTTP proxy (if supported).
4. VPN that exits where TURN is reachable.

```js
const pc = new RTCPeerConnection({
  iceServers: [{
    urls: [
      'turn:turn.example.com:3478?transport=udp',
      'turns:turn.example.com:443?transport=tcp',
    ],
    username: shortLivedUser,
    credential: shortLivedPass,
  }],
  iceTransportPolicy: 'all', // 'relay' = force relay for debug
})
```

```bash
turnutils_uclient -v -u user -w pass turn.example.com
```

| Knob | Why it matters |
|------|----------------|
| Short-lived credentials | Long-lived secrets in clients get stolen |
| UDP + TCP/TLS listeners | Corporate nets block UDP |
| Bandwidth alerts | Silent “everyone on relay” burns money |

| Symptom | Check | Fix |
|---------|-------|-----|
| ICE fails, no relay candidates | Auth / DNS / firewall to TURN | Fix creds; open 3478/443; test `turnutils_uclient` |
| Works only with `iceTransportPolicy: 'relay'` | Direct/STUN path broken | Keep relay; fix UDP/STUN for cost |
| Connect fails on corp Wi‑Fi | UDP egress filtered | Enable TURN TCP/TLS 443 |
| Huge egress bill | Most sessions nominated relay | Fix NAT/firewall; investigate ICE failure rate |
| One-way media via relay | Permissions / wrong peer addr | Check TURN permissions/channels |
| Outbound totally blocked | Proxy/VPN required | Allowlist or tunnel; otherwise no P2P |

## Mistakes to Avoid
- **Mistake:** Deploying only STUN and expecting hard NATs to work
- **Mistake:** Long-lived TURN credentials embedded in clients
- **Mistake:** Using relay for same-LAN peers that already have working host ca…
- **Mistake:** Assuming a normal reverse proxy substitutes for TURN

## Pros/Cons or Trade-offs
- **Pro:** Connectivity of last resort when direct and STUN paths fail.
- **Con:** Latency and cloud egress cost scale with bitrate and session count.
- **Con:** Forcing relay hides root-cause NAT/firewall problems.

## Comparison
- vs [[STUN (Session Traversal Utilities for NAT)]]: STUN discovers; relay carries.
- vs HTTPS reverse proxy: fronts your API; TURN is a media/data forwarder with allocations.
- vs CDN/[[HLS]]: one-to-many broadcast should not use per-viewer relays.


### Use cases
- WebRTC calls behind symmetric NAT/CGNAT, enterprise Wi‑Fi that blocks UDP, an…

- **Example:** Two phones on cellular CGNAT fail host/srflx
