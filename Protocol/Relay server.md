[[TURN server (Traversal Using Relays around NAT)]] [[STUN (Session Traversal Utilities for NAT)]] [[ICE (Interactive Connectivity Establishment)]] [[NAT Traversal]] [[NAT (Network Address Translation)]] [[WebRTC]] [[P2P (Peer-to-Peer)]]

# Relay server

> A relay server is a middle box both peers dial out to — it forwards bytes when they cannot connect directly through NAT.

## Interview Relevance

Interviewers separate STUN (discover addresses) from TURN/relay (carry media), and ask why relays are the expensive ICE fallback.

## Sources

- [RFC 8656 — Traversal Using Relays around NAT (TURN)](https://datatracker.ietf.org/doc/html/rfc8656) — deep-dive
- [RFC 8445 — ICE](https://datatracker.ietf.org/doc/html/rfc8445) — overview
- [WebRTC — ICE](https://webrtc.org/getting-started/peer-connections) — overview

## Key Concepts

- **Outbound-only:** clients dial the relay — NATs allow out; relay avoids inbound hole-punching.
- **Allocation:** TURN reserves ports; that address becomes the relay candidate.
- **ICE order:** try host/srflx first; nominate relay only after cheaper paths fail.
- **Cost:** server sees full bitrate — expensive fallback, not the happy path.

## Technical Details

```txt
Peer A ──outbound──► Relay ◄──outbound── Peer B
                       │
                  forwards A↔B
```

In WebRTC this is usually [[TURN server (Traversal Using Relays around NAT)]]. [[STUN (Session Traversal Utilities for NAT)]] only discovers addresses; the relay **carries** the media. [[ICE (Interactive Connectivity Establishment)]] picks relay after cheaper paths fail.

When outbound is also blocked (strict egress):

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

## Real-World Applications

WebRTC calls behind symmetric NAT/CGNAT, enterprise Wi‑Fi that blocks UDP, and forced-relay debug of ICE.

**Example:** Two phones on cellular CGNAT fail host/srflx; ICE nominates TURN on 443/TLS and the call still connects.

## Pros/Cons or Trade-offs

- **Pro:** Connectivity of last resort when direct and STUN paths fail.
- **Con:** Latency and cloud egress cost scale with bitrate and session count.
- **Con:** Forcing relay hides root-cause NAT/firewall problems.

## Comparison

- vs [[STUN (Session Traversal Utilities for NAT)]]: STUN discovers; relay carries.
- vs HTTPS reverse proxy: fronts your API; TURN is a media/data forwarder with allocations.
- vs CDN/[[HLS]]: one-to-many broadcast should not use per-viewer relays.

## Mistakes to Avoid

- Deploying only STUN and expecting hard NATs to work.
- Long-lived TURN credentials embedded in clients.
- Using relay for same-LAN peers that already have working host candidates.
- Assuming a normal reverse proxy substitutes for TURN.
